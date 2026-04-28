"""Markdown 文件切块模块 — 按 H1/H2 标题层级切分知识块。"""

import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from markdown_it import MarkdownIt


@dataclass
class Chunk:
    """表示一个知识块。

    Attributes:
        chunk_id:       UUID 唯一标识。
        content:        Markdown 原文内容。
        file_path:      来源文件路径。
        heading_level:  标题层级（0=无标题, 1=H1, 2=H2）。
        heading_text:   标题文字（若无标题则为空字符串）。
    """

    chunk_id: str
    content: str
    file_path: str
    heading_level: int = 0
    heading_text: str = ""


def read_markdown_file(file_path: Path) -> str:
    """读取 Markdown 文件内容。

    Args:
        file_path: Markdown 文件路径。

    Returns:
        文件文本内容。

    Raises:
        FileNotFoundError: 文件不存在。
    """
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    return file_path.read_text(encoding="utf-8")


def chunk_markdown_file(file_path: Path) -> list[Chunk]:
    """将单个 Markdown 文件按 H1/H2 标题切分为知识块。

    遍历 markdown-it-py 的 token 流，定位 H1/H2 标题，
    以每个标题及其后续内容为一个知识块。标题之前的内容单独成块。

    Args:
        file_path: Markdown 文件路径。

    Returns:
        知识块列表（可能为空，若文件内容为空）。
    """
    content = read_markdown_file(file_path)
    if not content.strip():
        return []

    md = MarkdownIt()
    tokens = md.parse(content)
    lines = content.split("\n")

    # 定位所有 H1/H2 标题的（行号, 层级, 标题文字）
    headings: list[tuple[int, int, str]] = []
    for i, token in enumerate(tokens):
        if token.type == "heading_open" and token.tag in ("h1", "h2"):
            level = int(token.tag[1])
            if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
                heading_text = tokens[i + 1].content.strip()
                headings.append((token.map[0], level, heading_text))

    # 无 H1/H2 标题 → 整个文件作为一个块
    if not headings:
        return [
            Chunk(
                chunk_id=str(uuid.uuid4()),
                content=content.strip(),
                file_path=str(file_path),
            )
        ]

    chunks: list[Chunk] = []

    # 第一个标题之前的内容（作为独立块）
    first_heading_line = headings[0][0]
    if first_heading_line > 0:
        pre = "\n".join(lines[:first_heading_line]).strip()
        if pre:
            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    content=pre,
                    file_path=str(file_path),
                )
            )

    # 按标题分割：每个标题及其后内容直到下一标题（或文件末尾）
    for idx, (line_num, level, heading_text) in enumerate(headings):
        end_line = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        section = "\n".join(lines[line_num:end_line]).strip()
        if section:
            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    content=section,
                    file_path=str(file_path),
                    heading_level=level,
                    heading_text=heading_text,
                )
            )

    return chunks


def extract_plain_text(markdown_content: str) -> str:
    """从 Markdown 内容中提取纯文本（用于向量化）。

    利用 markdown-it-py 提取所有 inline 文本及代码块内容，
    并剥离 Markdown 链接/图片语法，得到干净的纯文本。

    Args:
        markdown_content: Markdown 原文。

    Returns:
        纯文本内容。
    """
    md = MarkdownIt()
    tokens = md.parse(markdown_content)
    parts: list[str] = []
    for token in tokens:
        if token.type == "inline":
            parts.append(token.content)
        elif token.type in ("fence", "code_block"):
            parts.append(token.content)

    text = "\n".join(parts)
    # 剥离 Markdown 链接语法 [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # 剥离图片语法 ![alt](url) → alt
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    # 去除常见标记符号，保留文字
    text = re.sub(r"[#*_~`>|]", "", text)
    # 压缩连续空行
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
