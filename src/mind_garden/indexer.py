"""文件索引模块 — 遍历目录、切分文件、向量化、存储到 Chroma。"""

import time
from pathlib import Path

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

from .chunker import Chunk, chunk_markdown_file, extract_plain_text
from .db import COLLECTION_NAME, get_chroma_client, get_or_create_collection
from .embedder import get_model

BATCH_SIZE = 32


def find_md_files(directory: Path) -> list[Path]:
    """递归查找目录下所有 ``.md`` 文件。

    Args:
        directory: 要扫描的目录路径。

    Returns:
        所有匹配的 Markdown 文件路径列表（按路径排序）。

    Raises:
        FileNotFoundError: 目录不存在。
        NotADirectoryError: 路径不是目录。
    """
    if not directory.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"路径不是目录: {directory}")

    return sorted(directory.rglob("*.md"))


def index_directory(directory: Path) -> dict[str, int | float]:
    """索引指定目录下的所有 Markdown 文件。

    流程：
        1. 递归扫描目录，获取所有 ``.md`` 文件
        2. 对每个文件按 H1/H2 标题切分为知识块
        3. 提取纯文本，使用 sentence-transformers 批量向量化
        4. 清除旧的索引数据，将新数据写入 Chroma 持久化集合

    Args:
        directory: Markdown 文件夹路径。

    Returns:
        包含统计信息的字典：
        - ``file_count``: 处理的文件数
        - ``chunk_count``: 产生的知识块数
        - ``elapsed_time``: 总耗时（秒）

    Raises:
        FileNotFoundError: 目录不存在。
        ValueError: 目录中没有 ``.md`` 文件，或切分后无有效块。
    """
    start_time = time.time()

    # 1. 扫描文件
    md_files = find_md_files(directory)
    if not md_files:
        raise ValueError(f"未在 {directory} 中找到 .md 文件")

    # 2. 切分文件（带进度条）
    all_chunks: list[Chunk] = []
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task("扫描并切分文件...", total=len(md_files))
        for md_file in md_files:
            try:
                chunks = chunk_markdown_file(md_file)
                all_chunks.extend(chunks)
            except Exception as exc:
                progress.console.print(
                    f"[yellow]跳过 {md_file.name}: {exc}[/yellow]"
                )
            progress.update(task, advance=1)

    if not all_chunks:
        raise ValueError("所有文件切分后未产生有效知识块")

    # 3. 提取纯文本用于向量化
    plain_texts = [extract_plain_text(c.content) for c in all_chunks]

    # 4. 模型加载 + 批量向量化（每 BATCH_SIZE 个块一批）
    model = get_model()
    embeddings: list[list[float]] = []
    num_batches = (len(plain_texts) + BATCH_SIZE - 1) // BATCH_SIZE

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task("向量化知识块...", total=num_batches)
        for i in range(0, len(plain_texts), BATCH_SIZE):
            batch = plain_texts[i : i + BATCH_SIZE]
            batch_embeddings = model.encode(batch, show_progress_bar=False)
            embeddings.extend(batch_embeddings.tolist())
            progress.update(task, advance=1)

    # 5. 写入 Chroma（先清空旧数据后重建）
    client = get_chroma_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = get_or_create_collection(client)

    chunk_ids = [c.chunk_id for c in all_chunks]
    documents = [c.content for c in all_chunks]
    metadatas = [
        {
            "file_path": c.file_path,
            "heading_level": c.heading_level,
            "heading_text": c.heading_text,
        }
        for c in all_chunks
    ]

    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=chunk_ids,
    )

    elapsed = time.time() - start_time

    return {
        "file_count": len(md_files),
        "chunk_count": len(all_chunks),
        "elapsed_time": round(elapsed, 2),
    }
