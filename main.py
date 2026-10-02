#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""字符图片生成器 - 入口文件"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from gui.main_window import MainWindow


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("歌词/字符图片生成器")
    app.setApplicationVersion("1.0.0")
    app.setStyle('Fusion')

    # 全局字体大小
    font = QFont("Microsoft YaHei", 12)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()