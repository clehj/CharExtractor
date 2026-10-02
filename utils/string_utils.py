"""
字符串处理工具
"""

import re
from typing import Tuple


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """清理文件名中的非法字符"""
    cleaned = re.sub(r'[\\/*?:"<>|\n\r\t]', '_', text)
    cleaned = cleaned.strip('. ')
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned or "unnamed"


def parse_color(color_str: str) -> Tuple[int, int, int, int]:
    """解析颜色字符串 'R,G,B,A' 或 'R,G,B'"""
    try:
        parts = [int(p.strip()) for p in color_str.split(',')]
        if len(parts) == 3:
            return (parts[0], parts[1], parts[2], 255)
        elif len(parts) == 4:
            return tuple(parts)
    except (ValueError, AttributeError):
        pass
    return (255, 255, 255, 255)


def truncate_text(text: str, max_len: int = 80) -> str:
    """截断文本"""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."