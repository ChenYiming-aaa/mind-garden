# mind-garden

> 个人知识库助手 — 将本地 Markdown 笔记转化为可语义搜索和 AI 对话的私有知识库

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![PyPI version](https://img.shields.io/pypi/v/mind-garden)
![license](https://img.shields.io/badge/license-MIT-blue)
![last commit](https://img.shields.io/github/last-commit/ChenYiming-aaa/mind-garden)
![languages](https://img.shields.io/github/languages/count/ChenYiming-aaa/mind-garden)

## Features

- **语义搜索** — 使用 `sentence-transformers` 将笔记编码为向量，支持自然语言检索而非关键词匹配
- **AI 对话** — 基于检索增强生成（RAG），结合 DeepSeek API 对笔记内容进行问答
- **本地优先** — 向量数据库 ChromaDB 本地持久化，笔记不离开你的电脑
- **CLI 操作** — 基于 `typer` 的命令行界面，索引、搜索、问答一条命令完成

## Quick Start

### Prerequisites

- Python 3.11+
- DeepSeek API Key（用于 AI 问答功能）

### Install

```bash
pip install mind-garden
```

### Index Notes

```bash
mind-garden index ./my-notes
```

### Semantic Search

```bash
mind-garden search "你的问题" --top-k 5
```

### AI Q&A

```bash
export DEEPSEEK_API_KEY="your-key"
mind-garden ask "你的问题"
```

Expected output: AI 基于你的笔记内容生成的回答（含引用来源）。

## Configuration

Environment variables for AI provider:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEEPSEEK_API_KEY` | DeepSeek API Key | — |
| `DEEPSEEK_BASE_URL` | API endpoint | `https://api.deepseek.com/v1` |
| `MIND_GARDEN_MODEL` | Chat model | `deepseek-v4-flash` |

## Data Storage

Vector database is persisted at `~/.mind-garden/chroma/` by default.

## Project Structure

```
mind-garden/
├── src/
│   └── mind_garden/
│       ├── cli.py          # CLI entry point (typer)
│       ├── indexer.py      # Note indexing & embedding
│       ├── searcher.py     # Semantic search engine
│       ├── qa.py           # RAG-based QA with DeepSeek
│       └── storage.py      # ChromaDB persistence layer
├── pyproject.toml
└── README.md
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python 3.11+ |
| CLI | typer + rich |
| Embedding | sentence-transformers |
| Vector DB | ChromaDB |
| AI Chat | OpenAI-compatible API (DeepSeek) |

## Development

```bash
# Clone and install in editable mode
git clone https://github.com/ChenYiming-aaa/mind-garden.git
cd mind-garden
pip install -e .
```

## Contributing

Contributions welcome! Feel free to open an issue or PR.

## License

MIT © ChenYiming
