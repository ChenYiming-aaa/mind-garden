"""共享模块 — Chroma 客户端与集合管理。"""

from pathlib import Path

import chromadb
from chromadb.api import Collection

COLLECTION_NAME = "mind_garden"
CHROMA_PERSIST_DIR = Path.home() / ".mind-garden" / "chroma"


def get_chroma_client() -> chromadb.ClientAPI:
    """获取 Chroma 持久化客户端。

    数据存储在 ``~/.mind-garden/chroma/`` 目录，跨进程共享。

    Returns:
        Chroma 客户端实例。
    """
    CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))


def get_or_create_collection(client: chromadb.ClientAPI) -> Collection:
    """获取或创建知识库集合。

    Args:
        client: Chroma 客户端。

    Returns:
        Chroma 集合（cosine 相似度）。

    Raises:
        RuntimeError: 集合创建失败。
    """
    try:
        return client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    except Exception as exc:
        raise RuntimeError(f"创建 Chroma 集合失败: {exc}") from exc
