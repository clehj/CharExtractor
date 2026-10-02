"""
字符/歌词行提取器
"""

import re
from typing import List, Optional

from core.constants import CHAR_RANGES


class CharExtractor:
    """字符/歌词行提取器"""

    EXTRACT_MODES = ("char", "line")

    def __init__(self):
        self.items: List[str] = []
        self.selected_items: List[str] = []
        self.extract_mode: str = "char"

    def set_extract_mode(self, mode: str) -> None:
        if mode in self.EXTRACT_MODES:
            self.extract_mode = mode

    def extract_from_file(self, filepath: str, lang: str = "jp", mixed: bool = False) -> List[str]:
        """从文件提取内容"""
        if not filepath:
            raise ValueError("文件路径不能为空")

        with open(filepath, 'r', encoding='utf-8') as f:
            return self.extract_from_text(f.read(), lang, mixed)

    def extract_from_text(self, text: str, lang: str = "jp", mixed: bool = False) -> List[str]:
        """从文本提取内容"""
        if self.extract_mode == "line":
            return self._extract_lines(text)
        return self._extract_chars(text, lang, mixed)

    def _extract_lines(self, text: str) -> List[str]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        self.items = lines
        self.selected_items = lines.copy()
        return lines

    def _extract_chars(self, text: str, lang: str, mixed: bool) -> List[str]:
        patterns = self._get_patterns(lang, mixed)
        combined = '|'.join(patterns)
        matches = re.findall(combined, text)

        result = []
        for match in matches:
            if lang == "en" and not mixed:
                result.append(match)
            else:
                result.extend(match)

        self.items = result
        self.selected_items = result.copy()
        return result

    def _get_patterns(self, lang: str, mixed: bool) -> List[str]:
        if mixed:
            return [CHAR_RANGES[l]["pattern"] for l in ('jp', 'zh', 'en')]
        return [CHAR_RANGES[lang]["pattern"]]

    def deduplicate(self, items: Optional[List[str]] = None) -> List[str]:
        if self.extract_mode == "line":
            return self.items

        source = items if items is not None else self.items
        seen = set()
        result = []
        for item in source:
            if item not in seen:
                seen.add(item)
                result.append(item)

        if source is self.items:
            self.items = result
            self.selected_items = result.copy()

        return result

    def select_items(self, indices: List[int]) -> None:
        self.selected_items = [self.items[i] for i in indices if 0 <= i < len(self.items)]

    def select_all(self) -> None:
        self.selected_items = self.items.copy()

    def select_none(self) -> None:
        self.selected_items = []

    def get_selected(self) -> List[str]:
        return self.selected_items

    def get_all_items(self) -> List[str]:
        return self.items