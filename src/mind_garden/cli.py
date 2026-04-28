"""CLI 入口模块 — typer 应用，注册 index / search / ask 三个命令。

注意：Windows + Python 3.13 + onnxruntime 场景下需要提高递归限制。
异常处理中避免使用 rich 输出以防二次触发 RecursionError。
"""

import sys
from pathlib import Path

import typer
from rich.console import Console

from .ai_assistant import ask_question
from .indexer import index_directory
from .retriever import (
    check_index_exists,
    display_search_results,
    search as retrieve_search,
)

# Windows + onnxruntime 场景需要更高的递归限制
sys.setrecursionlimit(5000)

app = typer.Typer(
    name="mind-garden",
    help="个人知识库助手 — 将 Markdown 笔记转化为可语义搜索和 AI 对话的知识库",
    no_args_is_help=True,
)
console = Console(stderr=True)


def _fatal(msg: str) -> None:
    """打印错误消息并退出（使用 stderr 避免递归渲染问题）。"""
    print(f"错误: {msg}", file=sys.stderr)
    sys.exit(1)


@app.command()
def index(
    path: Path = typer.Argument(
        ...,
        help="Markdown 文件夹路径",
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
) -> None:
    """递归索引 Markdown 文件夹，构建知识库。"""
    try:
        stats = index_directory(path)
        console.print(
            f"\n[bold green]索引完成![/bold green] "
            f"[dim]{stats['file_count']}[/dim] 个文件 -> "
            f"[dim]{stats['chunk_count']}[/dim] 个知识块, "
            f"耗时 [dim]{stats['elapsed_time']}s[/dim]"
        )
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        _fatal(str(exc))


@app.command()
def search(
    query: str = typer.Argument(..., help="搜索问题"),
    top_k: int = typer.Option(5, "--top-k", help="返回结果数量", min=1, max=50),
) -> None:
    """语义搜索知识库中的相关内容。"""
    if not check_index_exists():
        _fatal("知识库为空，请先运行: mind-garden index <Markdown文件夹路径>")

    try:
        results = retrieve_search(query, top_k=top_k)
        display_search_results(results, console)
    except RuntimeError as exc:
        _fatal(f"搜索失败: {exc}")


@app.command()
def ask(
    query: str = typer.Argument(..., help="你的问题"),
) -> None:
    """基于知识库内容，通过 AI 回答问题。"""
    if not check_index_exists():
        _fatal("知识库为空，请先运行: mind-garden index <Markdown文件夹路径>")

    ask_question(query)


def main() -> None:
    """CLI 入口函数（支持 ``python -m mind_garden`` 调用）。"""
    app()


if __name__ == "__main__":
    main()
