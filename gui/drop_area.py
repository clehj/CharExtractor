#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拖拽区域组件 - 支持拖拽文本文件"""

import os
from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class DropArea(QLabel):
    """拖拽区域，支持拖拽文本文件"""
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("📁 拖拽文本文件到这里\n\n或点击上方按钮选择文件")
        self.setMinimumHeight(80)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #45475a;
                border-radius: 8px;
                background-color: #1e1e2e;
                color: #a6adc8;
                font-size: 13px;
                padding: 20px;
            }
            QLabel:hover {
                border-color: #6366f1;
                background-color: #2a2a3e;
                color: #89b4fa;
            }
        """)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.setStyleSheet("""
                QLabel {
                    border: 2px solid #6366f1;
                    border-radius: 8px;
                    background-color: #2a2a3e;
                    color: #89b4fa;
                    font-size: 13px;
                    padding: 20px;
                }
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #45475a;
                border-radius: 8px;
                background-color: #1e1e2e;
                color: #a6adc8;
                font-size: 13px;
                padding: 20px;
            }
        """)

    def dropEvent(self, event):
        self.dragLeaveEvent(event)
        urls = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.exists(path):
                # 只接受文本文件
                ext = os.path.splitext(path)[1].lower()
                if ext in ['.txt', '.md', '.json', '.xml', '.html', '.css', '.js', '.py', '.lrc']:
                    urls.append(path)
                else:
                    # 忽略非文本文件
                    pass
        if urls:
            self.files_dropped.emit(urls)