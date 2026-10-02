"""
核心模块常量定义
"""

# ============ 字符范围 ============

CHAR_RANGES = {
    "jp": {
        "name": "日文",
        "pattern": r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3400-\u4DBF]+'
    },
    "zh": {
        "name": "中文",
        "pattern": r'[\u4E00-\u9FFF\u3400-\u4DBF]+'
    },
    "en": {
        "name": "英文",
        "pattern": r'[A-Za-z]+'
    }
}

# ============ 默认值 ============

DEFAULT_FONT_SIZE = 200
DEFAULT_PADDING = 50
DEFAULT_SCALE = 2.0
DEFAULT_COLOR = (255, 255, 255, 255)

# ============ 文件命名 ============

MAX_FILENAME_LENGTH = 50
DEFAULT_NAMING_FORMAT = "{index:04d}_{content_safe}.png"

# ============ 预览 ============

PREVIEW_MAX_SIZE = 60
PREVIEW_PADDING = 10
PREVIEW_MAX_WIDTH = 200

# ============ 导出 ============

IMAGE_DPI = 300
PNG_COMPRESS_LEVEL = 0

# ============ GUI 选项 ============

SCALE_OPTIONS = ["1.0x", "1.5x", "2.0x", "2.5x", "3.0x", "4.0x"]