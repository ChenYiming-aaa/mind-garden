"""语义检索模块 — 在 Chroma 知识库中执行向量相似度搜索。

为避免 Chroma 内置 query 在 Windows + onnxruntime 下的递归问题，
手动计算余弦相似度：从 Chroma 读出所有向量后本地排序。
"""

import math
from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.panel import Panel

from .db import COLLECTION_NAME, get_chroma_client
from .embedder import get_model


@dataclass
class SearchResult:
    """语义搜索结果。

    Attributes:
        content:       Markdown 原文内容。
        file_path:     来源文件路径。
        heading_level: 标题层级（0=无标题）。
        heading_text:  标题文字。
        score:         余弦相似度分数。
        chunk_id:      知识块 ID。
    """

    content: str
    file_path: str
    heading_level: int
    heading_text: str
    score: float
    chunk_id: str


def check_index_exists() -> bool:
    """检查知识库是否已存在且非空。

    Returns:
        索引存在且有数据返回 ``True``，否则 ``False``。
    """
    try:
        client = get_chroma_client()
        collection = client.get_collection(COLLECTION_NAME)
        return collection.count() > 0
    except Exception:
        return False


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算两个向量的余弦相似度。

    Args:
        a: 向量 A。
        b: 向量 B。

    Returns:
        [0, 1] 范围的余弦相似度。
    """
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search(query: str, top_k: int = 5) -> list[SearchResult]:
    """在知识库中执行语义检索。

    对用户查询生成向量，从 Chroma 读出所有数据后手动计算余弦相似度，
    返回最相似的 top_k 个知识块。

    Args:
        query:  用户查询字符串。
        top_k:  返回结果数量（默认 5）。

    Returns:
        排序后的搜索结果列表（按相似度降序）。

    Raises:
        ValueError: 知识库为空或不存在。
        RuntimeError: 检索过程中出错。
    """
    if not check_index_exists():
        raise ValueError("知识库为空，请先运行「mind-garden index <目录>」")

    try:
        model = get_model()
        query_embedding = model.encode(query).tolist()

        client = get_chroma_client()
        collection = client.get_collection(COLLECTION_NAME)
        count = collection.count()
    except Exception as exc:
        raise RuntimeError(f"初始化检索失败: {exc}") from exc

    if count == 0:
        return []

    # 从 Chroma 读出全部数据（含向量）
    try:
        all_data = collection.get(
            include=["embeddings", "metadatas", "documents"],
        )
    except Exception as exc:
        raise RuntimeError(f"读取向量数据失败: {exc}") from exc

    ids = all_data["ids"]
    embeddings = all_data["embeddings"]
    metadatas = all_data["metadatas"]
    documents = all_data["documents"]

    if not ids:
        return []

    # 手动计算余弦相似度并排序
    scored: list[tuple[float, int]] = []
    for idx, emb in enumerate(embeddings):
        score = _cosine_similarity(query_embedding, emb)
        scored.append((score, idx))

    scored.sort(key=lambda x: x[0], reverse=True)

    # 取 top_k
    results: list[SearchResult] = []
    for score, idx in scored[:top_k]:
        meta = metadatas[idx]
        results.append(
            SearchResult(
                chunk_id=ids[idx],
                content=documents[idx],
                file_path=meta.get("file_path", ""),
                heading_level=meta.get("heading_level", 0),
                heading_text=meta.get("heading_text", ""),
                score=round(score, 4),
            )
        )

    return results


def display_search_results(results: list[SearchResult], console: Console) -> None:
    """用 rich Panel 美化输出搜索结果。

    Args:
        results:  搜索结果列表。
        console:  rich Console 实例。
    """
    if not results:
        console.print("[yellow]没有找到相关结果。[/yellow]")
        return

    console.print(f"\n[bold cyan]搜索结果 (共 {len(results)} 条):[/bold cyan]\n")

    for i, r in enumerate(results, 1):
        title = (
            f"[bold]{r.heading_text}[/bold]"
            if r.heading_text
            else "[dim]未命名块[/dim]"
        )
        content_preview = (
            r.content[:300] + "..." if len(r.content) > 300 else r.content
        )
        score_color = (
            "green" if r.score > 0.7 else "yellow" if r.score > 0.4 else "red"
        )

        panel = Panel(
            f"[dim]{r.file_path}[/dim]\n\n{content_preview}\n\n"
            f"[{score_color}]相关度: {r.score}[/{score_color}]",
            title=f"{i}. {title}",
            border_style="blue",
        )
        console.print(panel)
        if i < len(results):
            console.print()
