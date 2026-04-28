"""模型加载模块 — 独立的 sentence-transformers 模型懒加载封装。"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """获取（并缓存）sentence-transformers 模型。

    仅在首次调用时下载/加载，后续复用缓存实例。

    Returns:
        SentenceTransformer 模型实例。
    """
    return SentenceTransformer(MODEL_NAME)
