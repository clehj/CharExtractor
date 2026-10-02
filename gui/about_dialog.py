"""关于对话框"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class AboutDialog:
    """关于对话框"""

    @staticmethod
    def show(parent):
        dialog = QDialog(parent)
        dialog.setWindowTitle("关于")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setFixedSize(400, 380)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #cdd6f4;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("歌词/字符图片生成器")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #89b4fa;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        author = QLabel("软件作者: clehj")
        author.setAlignment(Qt.AlignCenter)
        layout.addWidget(author)

        version = QLabel("版本 1.0.0")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        desc = QLabel("从文本提取字符/歌词行，生成高清 PNG 图片")
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #a6adc8;")
        layout.addWidget(desc)

        layout.addSpacing(20)

        features = QLabel("功能特点：")
        features.setStyleSheet("font-weight: bold; color: #89b4fa;")
        features.setAlignment(Qt.AlignCenter)
        layout.addWidget(features)

        for text in ["• 支持按行或按字符提取", "• 支持日文/中文/英文", "• 自定义字体、颜色、大小",
                     "• 高倍率导出（最高 4x）"]:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        layout.addSpacing(20)

        copyright_label = QLabel("© 2026 BiliTool")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: #a6adc8;")
        layout.addWidget(copyright_label)

        layout.addSpacing(20)

        close_btn = QPushButton("关闭")
        close_btn.setFixedSize(100, 32)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #45475a;
                border-color: #6366f1;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        dialog.exec_()