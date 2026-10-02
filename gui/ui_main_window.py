"""UI 构建模块"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from core.constants import DEFAULT_NAMING_FORMAT
from gui.style import DARK_STYLE
from gui.drop_area import DropArea


class UIBuilder:
    """UI 构建器"""

    @staticmethod
    def build(window):
        """构建完整 UI"""
        window.setWindowTitle("歌词/字符图片生成器")
        window.setMinimumSize(1100, 800)
        window.setStyleSheet(DARK_STYLE)

        central = QWidget()
        central.setStyleSheet("background-color: #1e1e2e;")
        window.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 15, 20, 15)

        # 构建各组件
        UIBuilder._build_file_section(window, layout)
        UIBuilder._build_options_section(window, layout)
        UIBuilder._build_font_section(window, layout)
        UIBuilder._build_naming_section(window, layout)
        UIBuilder._build_list_section(window, layout)
        UIBuilder._build_status_bar(window)

    @staticmethod
    def _build_file_section(window, layout):
        group = QGroupBox("文件选择")
        window.file_section = group
        file_layout = QVBoxLayout(group)

        window.drop_area = DropArea()
        window.drop_area.files_dropped.connect(window.on_drop_files)
        file_layout.addWidget(window.drop_area)

        btn_layout = QHBoxLayout()
        window.file_path = QLineEdit()
        window.file_path.setPlaceholderText("或手动输入文件路径...")
        btn_layout.addWidget(window.file_path)

        window.browse_btn = QPushButton("浏览")
        btn_layout.addWidget(window.browse_btn)

        window.extract_btn = QPushButton("提取")
        btn_layout.addWidget(window.extract_btn)

        file_layout.addLayout(btn_layout)
        layout.addWidget(group)

    @staticmethod
    def _build_options_section(window, layout):
        group = QGroupBox("提取选项")
        window.options_section = group
        options_layout = QHBoxLayout(group)

        options_layout.addWidget(QLabel("提取模式:"))
        window.mode_cb = QComboBox()
        window.mode_cb.addItems(["按行（歌词）", "按字符"])
        options_layout.addWidget(window.mode_cb)

        options_layout.addSpacing(20)

        options_layout.addWidget(QLabel("语言:"))
        window.lang_cb = QComboBox()
        window.lang_cb.addItems(["日文", "中文", "英文"])
        options_layout.addWidget(window.lang_cb)

        options_layout.addSpacing(10)

        window.mixed_cb = QCheckBox("混合提取")
        options_layout.addWidget(window.mixed_cb)

        window.dedup_cb = QCheckBox("去重")
        window.dedup_cb.setChecked(True)
        options_layout.addWidget(window.dedup_cb)

        options_layout.addStretch()
        layout.addWidget(group)

    @staticmethod
    def _build_font_section(window, layout):
        group = QGroupBox("字体/样式")
        window.font_section = group
        font_layout = QGridLayout(group)

        font_layout.setColumnStretch(1, 1)
        font_layout.setColumnStretch(3, 1)

        font_layout.addWidget(QLabel("字体文件:"), 0, 0)
        window.font_path = QLineEdit()
        window.font_path.setPlaceholderText("选择字体文件...")
        font_layout.addWidget(window.font_path, 0, 1, 1, 2)
        window.font_browse_btn = QPushButton("浏览")
        font_layout.addWidget(window.font_browse_btn, 0, 3)
        font_layout.addWidget(QLabel("(默认: meiryo.ttc)"), 0, 4)

        font_layout.addWidget(QLabel("字号:"), 1, 0)
        window.font_size = QSpinBox()
        window.font_size.setRange(20, 500)
        window.font_size.setValue(120)
        font_layout.addWidget(window.font_size, 1, 1)

        font_layout.addWidget(QLabel("颜色(R,G,B,A):"), 1, 2)
        window.color = QLineEdit()
        window.color.setText("255,255,255,255")
        font_layout.addWidget(window.color, 1, 3)

        font_layout.addWidget(QLabel("内边距:"), 2, 0)
        window.padding = QSpinBox()
        window.padding.setRange(0, 100)
        window.padding.setValue(30)
        font_layout.addWidget(window.padding, 2, 1)

        font_layout.addWidget(QLabel("导出倍率:"), 2, 2)
        window.scale_cb = QComboBox()
        window.scale_cb.addItems(["1.0x", "1.5x", "2.0x", "2.5x", "3.0x", "4.0x"])
        window.scale_cb.setCurrentIndex(2)
        font_layout.addWidget(window.scale_cb, 2, 3)
        font_layout.addWidget(QLabel("(1x=标准, 2x=高清, 4x=超清)"), 2, 4)

        layout.addWidget(group)

    @staticmethod
    def _build_naming_section(window, layout):
        group = QGroupBox("文件名格式")
        window.naming_section = group
        naming_layout = QVBoxLayout(group)

        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("预设:"))
        window.preset_cb = QComboBox()
        window.preset_cb.addItems(["序号+内容", "仅序号", "仅内容", "序号_内容", "自定义"])
        preset_layout.addWidget(window.preset_cb)
        preset_layout.addStretch()
        naming_layout.addLayout(preset_layout)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("自定义格式:"))
        window.format_entry = QLineEdit()
        window.format_entry.setText(DEFAULT_NAMING_FORMAT)
        format_layout.addWidget(window.format_entry)
        window.reset_btn = QPushButton("重置")
        format_layout.addWidget(window.reset_btn)
        naming_layout.addLayout(format_layout)

        help_label = QLabel("变量: {index} {index:04d} {content} {content_safe} {total}")
        help_label.setStyleSheet("color: #a6adc8; font-size: 11px;")
        naming_layout.addWidget(help_label)

        preview_layout = QHBoxLayout()
        preview_layout.addWidget(QLabel("示例:"))
        window.preview_label = QLabel("0001_示例歌词.png")
        window.preview_label.setStyleSheet("color: #89b4fa;")
        preview_layout.addWidget(window.preview_label)
        preview_layout.addStretch()
        naming_layout.addLayout(preview_layout)

        layout.addWidget(group)

    @staticmethod
    def _build_list_section(window, layout):
        group = QGroupBox("待导出列表（勾选要生成的项目）")
        window.list_section = group  # 修复：改成 list_section
        list_layout = QVBoxLayout(group)

        window.list_widget = QListWidget()
        window.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        list_layout.addWidget(window.list_widget)

        btn_layout = QHBoxLayout()
        window.select_all_btn = QPushButton("全选")
        btn_layout.addWidget(window.select_all_btn)
        window.deselect_all_btn = QPushButton("全不选")
        btn_layout.addWidget(window.deselect_all_btn)
        window.clear_list_btn = QPushButton("清空列表")
        btn_layout.addWidget(window.clear_list_btn)
        btn_layout.addStretch()

        window.generate_btn = QPushButton("生成图片")
        window.generate_btn.setProperty("class", "primary")
        btn_layout.addWidget(window.generate_btn)

        list_layout.addLayout(btn_layout)
        layout.addWidget(group)

    @staticmethod
    def _build_status_bar(window):
        window.status_bar = QStatusBar()
        window.setStatusBar(window.status_bar)
        window.status_bar.showMessage("就绪")