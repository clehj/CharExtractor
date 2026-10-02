#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主窗口 - 精简版"""

import os
import threading
from typing import List, Optional

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from core import CharExtractor, ImageGenerator
from core.constants import DEFAULT_NAMING_FORMAT
from gui.ui_main_window import UIBuilder
from gui.about_dialog import AboutDialog
from gui.style import MENU_BAR_STYLE
from utils.string_utils import parse_color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.extractor = CharExtractor()
        self.generator: Optional[ImageGenerator] = None
        self.is_extracting = False

        # 构建 UI
        UIBuilder.build(self)
        self._setup_connections()
        self._setup_menu_bar()
        self._init_defaults()

    def _setup_connections(self):
        """连接信号"""
        self.browse_btn.clicked.connect(self.browse_file)
        self.extract_btn.clicked.connect(self.extract_chars)
        self.font_browse_btn.clicked.connect(self.browse_font)
        self.mode_cb.currentIndexChanged.connect(self.on_mode_change)
        self.preset_cb.currentIndexChanged.connect(self.on_preset_change)
        self.reset_btn.clicked.connect(self.reset_custom_format)
        self.select_all_btn.clicked.connect(self.select_all)
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        self.clear_list_btn.clicked.connect(self.clear_list)
        self.generate_btn.clicked.connect(self.generate_images)
        self.format_entry.textChanged.connect(self.update_format_preview)
        self.drop_area.files_dropped.connect(self.on_drop_files)

    def _setup_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet(MENU_BAR_STYLE)

        file_menu = menubar.addMenu("文件")
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(lambda: AboutDialog.show(self))
        help_menu.addAction(about_action)

    def _init_defaults(self):
        default_font = self._get_default_font()
        if default_font:
            self.font_path.setText(default_font)

    def _get_default_font(self) -> str:
        candidates = ["fonts/meiryo.ttc", "fonts/meiryob.ttc"]
        for font in candidates:
            if os.path.exists(font):
                return font
        system_fonts = [
            "C:/Windows/Fonts/meiryo.ttc",
            "C:/Windows/Fonts/meiryob.ttc",
            "C:/Windows/Fonts/msgothic.ttc",
            "C:/Windows/Fonts/msyh.ttc",
        ]
        for font in system_fonts:
            if os.path.exists(font):
                return font
        return ""

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择文本文件", "", "文本文件 (*.txt);;所有文件 (*.*)"
        )
        if path:
            self.file_path.setText(path)

    def browse_font(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择字体文件", "", "字体文件 (*.ttf *.ttc *.otf);;所有文件 (*.*)"
        )
        if path:
            self.font_path.setText(path)

    def on_mode_change(self):
        is_char = self.mode_cb.currentIndex() == 1
        self.lang_cb.setEnabled(is_char)
        self.mixed_cb.setEnabled(is_char)
        self.dedup_cb.setEnabled(is_char)
        self.extractor.set_extract_mode("char" if is_char else "line")

    def on_preset_change(self):
        presets = [
            "{index:04d}_{content_safe}",
            "{index:04d}",
            "{content_safe}",
            "{index}_{content_safe}",
            ""
        ]
        idx = self.preset_cb.currentIndex()
        if idx < 4:
            self.format_entry.setText(presets[idx])
            self.format_entry.setReadOnly(True)
        else:
            self.format_entry.setReadOnly(False)
        self.update_format_preview()

    def reset_custom_format(self):
        self.preset_cb.setCurrentIndex(0)
        self.format_entry.setText(DEFAULT_NAMING_FORMAT)
        self.update_format_preview()

    def update_format_preview(self):
        fmt = self.format_entry.text()
        result = fmt.replace("{content_safe}", "示例歌词")
        result = result.replace("{content}", "示例歌词")
        result = result.replace("{index:04d}", "0001")
        result = result.replace("{index}", "1")
        if not result.endswith('.png'):
            result += '.png'
        self.preview_label.setText(result)

    def extract_chars(self):
        if self.is_extracting:
            return

        filepath = self.file_path.text()
        if not filepath or not os.path.exists(filepath):
            QMessageBox.warning(self, "错误", "请先选择有效的输入文件")
            return

        self.is_extracting = True
        self.extract_btn.setEnabled(False)
        self.status_bar.showMessage("正在提取...")

        def worker():
            try:
                lang_index = self.lang_cb.currentIndex()
                lang = ["jp", "zh", "en"][lang_index]
                mixed = self.mixed_cb.isChecked()
                mode = "char" if self.mode_cb.currentIndex() == 1 else "line"

                self.extractor.set_extract_mode(mode)
                items = self.extractor.extract_from_file(filepath, lang, mixed)

                if self.dedup_cb.isChecked() and mode == "char":
                    items = self.extractor.deduplicate()

                QMetaObject.invokeMethod(self, "on_extract_complete", Qt.QueuedConnection,
                                         Q_ARG(list, items))
            except Exception as e:
                QMetaObject.invokeMethod(self, "on_extract_error", Qt.QueuedConnection,
                                         Q_ARG(str, str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def on_extract_complete(self, items):
        self.is_extracting = False
        self.extract_btn.setEnabled(True)

        if not items:
            QMessageBox.information(self, "提示", "没有提取到任何内容")
            self.status_bar.showMessage("未提取到内容")
            return

        self.status_bar.showMessage(f"提取到 {len(items)} 个项目")
        self.list_widget.clear()

        try:
            scale = float(self.scale_cb.currentText().replace('x', ''))
            self.generator = ImageGenerator(
                font_path=self.font_path.text(),
                font_size=self.font_size.value(),
                color=parse_color(self.color.text()),
                padding=self.padding.value(),
                scale=scale
            )
            self.generator.set_extract_mode("char" if self.mode_cb.currentIndex() == 1 else "line")
            self.generator.set_naming_format(self.format_entry.text())
        except Exception as e:
            QMessageBox.critical(self, "错误", f"初始化字体失败: {e}")
            return

        for i, item in enumerate(items):
            display = f"'{item}'" if self.mode_cb.currentIndex() == 1 else item
            if len(display) > 60:
                display = display[:57] + "..."
            filename = self.generator._format_filename(item, i + 1, len(items))
            self.list_widget.addItem(f"{i + 1}. {display} → {filename.split('/')[-1]}")

    def on_extract_error(self, msg):
        self.is_extracting = False
        self.extract_btn.setEnabled(True)
        QMessageBox.critical(self, "错误", f"提取失败: {msg}")
        self.status_bar.showMessage("提取失败")

    def select_all(self):
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setSelected(True)

    def deselect_all(self):
        self.list_widget.clearSelection()

    def clear_list(self):
        self.list_widget.clear()
        self.extractor = CharExtractor()
        self.status_bar.showMessage("列表已清空")

    def generate_images(self):
        selected = self.list_widget.selectedItems()
        if not selected:
            QMessageBox.warning(self, "警告", "没有选中任何项目")
            return

        items = []
        for item in selected:
            text = item.text()
            if ' → ' in text:
                content = text.split(' → ')[0].split('. ', 1)[1]
                items.append(content)
            else:
                items.append(text)

        output_dir = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if not output_dir:
            return

        try:
            scale = float(self.scale_cb.currentText().replace('x', ''))
            self.generator = ImageGenerator(
                font_path=self.font_path.text(),
                font_size=self.font_size.value(),
                color=parse_color(self.color.text()),
                padding=self.padding.value(),
                scale=scale
            )
            self.generator.set_extract_mode("char" if self.mode_cb.currentIndex() == 1 else "line")
            self.generator.set_naming_format(self.format_entry.text())
        except Exception as e:
            QMessageBox.critical(self, "错误", f"初始化字体失败: {e}")
            return

        self.generate_btn.setEnabled(False)
        self.status_bar.showMessage("正在生成图片...")

        def worker():
            def progress_cb(current, total, item):
                QMetaObject.invokeMethod(self, "update_progress", Qt.QueuedConnection,
                                         Q_ARG(int, current), Q_ARG(int, total), Q_ARG(str, item[:30]))

            try:
                files = self.generator.generate_batch(items, output_dir, progress_cb)
                QMetaObject.invokeMethod(self, "on_generate_complete", Qt.QueuedConnection,
                                         Q_ARG(list, files), Q_ARG(str, output_dir))
            except Exception as e:
                QMetaObject.invokeMethod(self, "on_generate_error", Qt.QueuedConnection,
                                         Q_ARG(str, str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def update_progress(self, current, total, item):
        self.status_bar.showMessage(f"生成中: {current}/{total} - {item}...")

    def on_generate_complete(self, files, output_dir):
        self.generate_btn.setEnabled(True)
        self.status_bar.showMessage(f"完成！生成 {len(files)} 张图片")
        QMessageBox.information(self, "完成", f"已生成 {len(files)} 张图片\n保存在: {output_dir}")

    def on_generate_error(self, msg):
        self.generate_btn.setEnabled(True)
        self.status_bar.showMessage("生成失败")
        QMessageBox.critical(self, "错误", f"生成失败: {msg}")

    def on_drop_files(self, paths):
        """拖拽文件处理"""
        if paths:
            self.file_path.setText(paths[0])
            self.extract_chars()