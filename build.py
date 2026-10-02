import os
import shutil
import subprocess
from pathlib import Path

# 配置
APP_NAME = "CharExtractor"
VERSION = "1.0.0"
OUTPUT_DIR = "dist"


def clean():
    """清理构建目录"""
    for dir_name in ["build", OUTPUT_DIR, "__pycache__"]:
        shutil.rmtree(dir_name, ignore_errors=True)

    for pycache in Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)


def build():
    """使用 PyInstaller 打包"""
    cmd = [
        "pyinstaller",
        "--name", f"{APP_NAME}_v{VERSION}",
        "--windowed",
        "--icon", "icon.ico",
        "--add-data", f"fonts;fonts",
        "--hidden-import", "PyQt5.sip",
        "--hidden-import", "PIL",
        "--noconfirm",
        "main.py"
    ]

    subprocess.run(cmd, check=True)
    print(f"打包完成！输出目录: {OUTPUT_DIR}")


def create_portable():
    """创建便携版"""
    portable_dir = Path(OUTPUT_DIR) / f"{APP_NAME}_Portable_v{VERSION}"
    portable_dir.mkdir(parents=True, exist_ok=True)

    build_dir = Path(OUTPUT_DIR) / f"{APP_NAME}_v{VERSION}"
    for item in build_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, portable_dir / item.name)
        elif item.is_dir():
            shutil.copytree(item, portable_dir / item.name, dirs_exist_ok=True)

    # 创建使用说明
    readme = portable_dir / "使用说明.txt"
    readme.write_text("""
歌词/字符图片生成器 - 便携版

使用说明：
1. 双击运行 CharExtractor.exe
2. 拖拽或选择文本文件
3. 选择提取模式（按行/按字符）
4. 勾选要导出的项目
5. 点击"生成图片"

配置文件：
- fonts/: 字体文件目录
- settings.json: 用户设置

提示：默认使用 meiryo.ttc 字体
    """, encoding='utf-8')

    print(f"便携版创建完成: {portable_dir}")


if __name__ == "__main__":
    clean()
    build()
    create_portable()