"""
图片生成器
"""

import os
import re
from typing import List, Tuple, Optional, Callable
from PIL import Image, ImageDraw, ImageFont

from core.constants import (
    DEFAULT_FONT_SIZE, DEFAULT_PADDING, DEFAULT_SCALE,
    DEFAULT_COLOR, MAX_FILENAME_LENGTH, DEFAULT_NAMING_FORMAT,
    PREVIEW_MAX_SIZE, PREVIEW_PADDING, PREVIEW_MAX_WIDTH,
    IMAGE_DPI, PNG_COMPRESS_LEVEL
)


class ImageGenerator:
    """图片生成器（支持高清晰度导出）"""

    def __init__(
        self,
        font_path: str,
        font_size: int = DEFAULT_FONT_SIZE,
        color: Tuple[int, int, int, int] = DEFAULT_COLOR,
        padding: int = DEFAULT_PADDING,
        scale: float = DEFAULT_SCALE
    ):
        self.font_path = font_path
        self.font_size = font_size
        self.color = color
        self.padding = padding
        self.scale = max(0.5, min(4.0, scale))

        self._font = None
        self._font_cache = {}
        self.extract_mode = "char"
        self.naming_format = DEFAULT_NAMING_FORMAT
        self.custom_formatter: Optional[Callable] = None

    # ============ 设置 ============

    def set_extract_mode(self, mode: str) -> None:
        self.extract_mode = mode

    def set_naming_format(self, format_str: str) -> None:
        self.naming_format = format_str

    def set_custom_formatter(self, formatter: Callable) -> None:
        self.custom_formatter = formatter

    # ============ 字体 ============

    @property
    def font(self):
        if self._font is None:
            self._font = self._load_font(self.font_size)
        return self._font

    def get_font(self, size: int):
        if size not in self._font_cache:
            self._font_cache[size] = self._load_font(size)
        return self._font_cache[size]

    def _load_font(self, size: int):
        try:
            return ImageFont.truetype(self.font_path, size)
        except Exception as e:
            raise RuntimeError(f"加载字体失败: {self.font_path}") from e

    # ============ 文本尺寸 ============

    def get_text_dimensions(self, text: str, font_size: int = None) -> Tuple[int, int, Tuple[int, int, int, int]]:
        temp = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(temp)
        font = self.get_font(font_size) if font_size else self.font
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1], bbox

    # ============ 文件名 ============

    def _sanitize_filename(self, text: str) -> str:
        cleaned = re.sub(r'[\\/*?:"<>|\n\r\t]', '_', text)
        cleaned = cleaned.strip('. ')
        if len(cleaned) > MAX_FILENAME_LENGTH:
            cleaned = cleaned[:MAX_FILENAME_LENGTH]
        return cleaned or "unnamed"

    def _format_filename(self, content: str, index: int, total: int = None) -> str:
        if self.custom_formatter:
            return self.custom_formatter(content, index, total)

        safe = self._sanitize_filename(content)
        result = self.naming_format
        result = result.replace("{content_safe}", safe)
        result = result.replace("{content}", content)

        # 处理 index
        if total:
            digits = len(str(total))
            zero_filled = f"{index:0{digits}d}"
        else:
            zero_filled = str(index)

        def replacer(match):
            spec = match.group(1) or ""
            try:
                return f"{index:{spec}}" if spec else zero_filled
            except ValueError:
                return str(index)

        result = re.sub(r'\{index(:[^}]+)?\}', replacer, result)
        if not result.endswith('.png'):
            result += '.png'
        return result

    # ============ 生成单张 ============

    def generate_single(self, text: str, output_dir: str, index: int = None, total: int = None) -> str:
        scaled_size = int(self.font_size * self.scale)
        scaled_pad = int(self.padding * self.scale)
        font = self.get_font(scaled_size)

        # 计算尺寸
        temp = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(temp)
        bbox = draw.textbbox((0, 0), text, font=font)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # 创建画布
        img = Image.new('RGBA', (width + scaled_pad * 2, height + scaled_pad * 2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((scaled_pad - bbox[0], scaled_pad - bbox[1]), text, fill=self.color, font=font)

        # 缩放
        if self.scale != 1.0:
            target_w = int((width + scaled_pad * 2) / self.scale)
            target_h = int((height + scaled_pad * 2) / self.scale)
            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        # 保存
        filename = self._format_filename(text, index, total) if index is not None else f"{self._sanitize_filename(text)}.png"
        full_path = os.path.join(output_dir, filename)

        # 防冲突
        counter = 1
        while os.path.exists(full_path):
            name, ext = os.path.splitext(full_path)
            full_path = f"{name}_{counter}{ext}"
            counter += 1

        img.save(full_path, format='PNG', compress_level=PNG_COMPRESS_LEVEL, dpi=(IMAGE_DPI, IMAGE_DPI))
        return full_path

    # ============ 批量生成 ============

    def generate_batch(self, items: List[str], output_dir: str, progress_callback=None) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        results = []
        total = len(items)

        for i, item in enumerate(items):
            results.append(self.generate_single(item, output_dir, i + 1, total))
            if progress_callback:
                progress_callback(i + 1, total, item)

        return results

    # ============ 预览 ============

    def create_preview(self, text: str, max_size: int = PREVIEW_MAX_SIZE):
        try:
            return self._create_preview_internal(text, max_size)
        except Exception:
            return None

    def _create_preview_internal(self, text: str, max_size: int):
        width, height, bbox = self.get_text_dimensions(text)

        if self.extract_mode == "line" and len(text) > 10:
            max_size = min(max_size * 2, 120)

        preview_width = min(width + PREVIEW_PADDING * 2, PREVIEW_MAX_WIDTH)
        preview_height = height + PREVIEW_PADDING * 2

        if width + PREVIEW_PADDING * 2 > PREVIEW_MAX_WIDTH:
            return self._create_scaled_preview(text, max_size)

        img = Image.new('RGBA', (preview_width, preview_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((PREVIEW_PADDING - bbox[0], PREVIEW_PADDING - bbox[1]), text, fill=self.color, font=self.font)
        img.thumbnail((max_size, max_size))
        return img

    def _create_scaled_preview(self, text: str, max_size: int):
        scale = PREVIEW_MAX_WIDTH / (self.get_text_dimensions(text)[0] + PREVIEW_PADDING * 2)
        temp_size = int(self.font_size * scale)

        try:
            font = self.get_font(temp_size)
            temp = Image.new('RGBA', (1, 1))
            draw = ImageDraw.Draw(temp)
            bbox = draw.textbbox((0, 0), text, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

            pad = 5
            img = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.text((pad - bbox[0], pad - bbox[1]), text, fill=self.color, font=font)
            img.thumbnail((max_size, max_size))
            return img
        except:
            return None