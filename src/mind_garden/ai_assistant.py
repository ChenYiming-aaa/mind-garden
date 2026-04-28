"""AI 问答模块 — 基于检索到的上下文，调用 DeepSeek API 流式回答。"""

import os
from typing import Optional

from openai import OpenAI, Stream
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .retriever import search, display_search_results

DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
TOP_K_RETRIEVAL = 3


def get_deepseek_client() -> Optional[OpenAI]:
    """根据环境变量创建 DeepSeek API 客户端。

    所需环境变量:
        - ``DEEPSEEK_API_KEY``: API 密钥（必需）
        - ``DEEPSEEK_BASE_URL``: API 地址（可选，有默认值）

    Returns:
        配置好的 OpenAI 客户端，若缺少 API Key 则返回 ``None``。
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return None

    base_url = os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL)
    return OpenAI(api_key=api_key, base_url=base_url)


def build_context(results: list, max_chars: int = 4000) -> str:
    """将检索结果拼接为 AI 回答的上下文文本。

    Args:
        results:  检索结果列表。
        max_chars: 上下文最大字符数（超出截断）。

    Returns:
        格式化的上下文字符串。
    """
    parts: list[str] = []
    total = 0
    for i, r in enumerate(results, 1):
        heading = f"标题: {r.heading_text}" if r.heading_text else "（无标题）"
        block = (
            f"[来源 {i}]\n"
            f"文件: {r.file_path}\n"
            f"{heading}\n"
            f"内容:\n{r.content}\n"
        )
        # 如果超出上限则截断此块
        if total + len(block) > max_chars:
            remaining = max_chars - total
            block = block[:remaining] + "\n...（截断）"
            parts.append(block)
            break
        parts.append(block)
        total += len(block)

    return "\n---\n".join(parts)


def ask_question(query: str) -> None:
    """基于知识库检索结果，通过 AI 回答用户问题。

    流程：
        1. 语义检索 top-3 相关块
        2. 若未设置 ``DEEPSEEK_API_KEY``，降级为仅输出检索结果
        3. 构建提示词并调用 DeepSeek API（流式输出）
        4. 输出完成后列出引用来源

    Args:
        query: 用户问题。

    Raises:
        SystemExit: API 调用失败时退出。
    """
    console = Console()

    # 1. 检索知识库
    with console.status("检索知识库...", spinner="dots"):
        try:
            results = search(query, top_k=TOP_K_RETRIEVAL)
        except ValueError as exc:
            console.print(f"[bold red]{exc}[/bold red]")
            raise SystemExit(1) from exc
        except RuntimeError as exc:
            console.print(f"[bold red]{exc}[/bold red]")
            raise SystemExit(1) from exc

    if not results:
        console.print("[yellow]未找到相关上下文，无法回答。[/yellow]")
        return

    console.print(f"\n[dim]检索到 {len(results)} 个相关块[/dim]\n")

    # 2. 检查 API Key
    client = get_deepseek_client()
    if client is None:
        # 降级模式：仅展示检索到的上下文
        console.print(
            "[yellow]DEEPSEEK_API_KEY 未设置，无法使用 AI 回答。[/yellow]\n"
            "[yellow]  设置后即可启用: export DEEPSEEK_API_KEY='your-key'[/yellow]\n"
        )
        display_search_results(results, console)
        return

    # 3. 构建提示词
    context = build_context(results)
    model = os.environ.get("MIND_GARDEN_MODEL", DEFAULT_MODEL)

    system_prompt = (
        "你是一个个人知识库助手。请基于提供的上下文内容回答问题。"
        "如果上下文信息不足，请明确告知，不要编造信息。"
        "回答时请注明信息来源（引用文件名）。"
        "使用中文回答。"
    )

    user_prompt = (
        "以下是我个人知识库中的相关上下文：\n\n"
        f"{context}\n\n"
        f"请基于以上内容回答：{query}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # 4. 调用 DeepSeek 流式 API
    console.print("[bold]AI 回答:[/bold]\n")

    try:
        stream: Stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=0.7,
        )
    except Exception as exc:
        console.print(f"\n[bold red]API 调用失败: {exc}[/bold red]")
        raise SystemExit(1) from exc

    # 5. 流式输出
    full_response = ""
    try:
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                content_piece = delta.content
                full_response += content_piece
                console.print(content_piece, end="")
    except Exception as exc:
        console.print(f"\n[bold red]流式输出中断: {exc}[/bold red]")

    # 6. 列出引用来源
    console.print("\n\n[dim]── 引用来源 ──[/dim]")
    seen: set[str] = set()
    for r in results:
        if r.file_path not in seen:
            seen.add(r.file_path)
            console.print(f"  [dim]{r.file_path}[/dim]")
    console.print()
