<p align="center">
  <strong>🌐 Language / 语言</strong><br>
  <a href="#english">English</a> | <a href="#chinese">中文</a>
</p>

---

<a id="english"></a>
# mind-garden

> Transform local Markdown notes into a private, searchable, AI-chat-ready knowledge base

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![license](https://img.shields.io/badge/license-MIT-blue)
![last commit](https://img.shields.io/github/last-commit/ChenYiming-aaa/mind-garden)
![languages](https://img.shields.io/github/languages/count/ChenYiming-aaa/mind-garden)
![code size](https://img.shields.io/github/languages/code-size/ChenYiming-aaa/mind-garden)

## Features

- **Semantic Search** — Encode notes into vectors via `sentence-transformers`, enabling natural language retrieval instead of keyword matching
- **AI Q&A** — Retrieval-Augmented Generation (RAG) powered by DeepSeek API; ask questions and get answers grounded in your notes
- **Local-First** — ChromaDB vector database persists on your machine; your notes never leave your computer
- **CLI-Driven** — Typer-powered command-line interface: index, search, and chat with a single command

## Quick Start

### Prerequisites

- Python 3.11+
- DeepSeek API Key (required for AI Q&A)

### Install

```bash
git clone https://github.com/ChenYiming-aaa/mind-garden.git
cd mind-garden
pip install -e .
```

### Index Notes

```bash
mind-garden index ./my-notes
```

### Semantic Search

```bash
mind-garden search "your question" --top-k 5
```

Expected output: a list of relevant note snippets with similarity scores.

### AI Q&A

```bash
export DEEPSEEK_API_KEY="your-key"
mind-garden ask "your question"
```

Expected output: an answer generated from your notes with source references.

## Configuration

Environment variables for the AI provider:

| Variable | Default | Description |
|----------|---------|-------------|
| `DEEPSEEK_API_KEY` | — | DeepSeek API Key |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | API endpoint |
| `MIND_GARDEN_MODEL` | `deepseek-chat` | Chat model name |

## Data Storage

Vector database and metadata are persisted at `~/.mind-garden/chroma/` by default.

## Project Structure

```
mind-garden/
├── src/
│   └── mind_garden/
│       ├── cli.py          # CLI entry point (typer)
│       ├── indexer.py      # Note indexing & embedding
│       ├── searcher.py     # Semantic search engine
│       ├── qa.py           # RAG-based Q&A with DeepSeek
│       └── storage.py      # ChromaDB persistence layer
├── tests/
├── pyproject.toml
└── README.md
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python 3.11+ |
| CLI Framework | typer + rich |
| Embedding | sentence-transformers |
| Vector Database | ChromaDB |
| AI Inference | OpenAI-compatible API (DeepSeek) |

## Development

```bash
git clone https://github.com/ChenYiming-aaa/mind-garden.git
cd mind-garden
pip install -e .
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

MIT © ChenYiming. See [LICENSE](LICENSE) for details.

---

<a id="chinese"></a>
# mind-garden

> 个人知识库助手 — 将本地 Markdown 笔记转化为可语义搜索和 AI 对话的私有知识库

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![license](https://img.shields.io/badge/license-MIT-blue)
![last commit](https://img.shields.io/github/last-commit/ChenYiming-aaa/mind-garden)
![languages](https://img.shields.io/github/languages/count/ChenYiming-aaa/mind-garden)
![code size](https://img.shields.io/github/languages/code-size/ChenYiming-aaa/mind-garden)

## 功能特性

- **语义搜索** — 通过 `sentence-transformers` 将笔记编码为向量，支持自然语言检索，告别关键词匹配
- **AI 问答** — 基于检索增强生成（RAG），接入 DeepSeek API，基于你的笔记内容进行智能问答
- **本地优先** — ChromaDB 向量数据库本地持久化，笔记数据始终保存在你的电脑上
- **CLI 操作** — 基于 typer 的命令行界面，一条命令完成索引、搜索和问答

## 快速开始

### 前置要求

- Python 3.11+
- DeepSeek API Key（AI 问答功能需要）

### 安装

```bash
git clone https://github.com/ChenYiming-aaa/mind-garden.git
cd mind-garden
pip install -e .
```

### 索引笔记

```bash
mind-garden index ./my-notes
```

### 语义搜索

```bash
mind-garden search "你的问题" --top-k 5
```

预期输出：相关笔记片段列表及相似度评分。

### AI 问答

```bash
export DEEPSEEK_API_KEY="your-key"
mind-garden ask "你的问题"
```

预期输出：基于你的笔记生成的回答（含引用来源）。

## 配置说明

AI 提供商的环境变量配置：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DEEPSEEK_API_KEY` | — | DeepSeek API 密钥 |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | API 地址 |
| `MIND_GARDEN_MODEL` | `deepseek-chat` | 对话模型名称 |

## 数据存储

向量数据库和元数据默认持久化在 `~/.mind-garden/chroma/` 目录下。

## 项目结构

```
mind-garden/
├── src/
│   └── mind_garden/
│       ├── cli.py          # CLI 入口 (typer)
│       ├── indexer.py      # 笔记索引与向量化
│       ├── searcher.py     # 语义搜索引擎
│       ├── qa.py           # 基于 RAG 的 AI 问答
│       └── storage.py      # ChromaDB 持久化层
├── tests/
├── pyproject.toml
└── README.md
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 运行环境 | Python 3.11+ |
| CLI 框架 | typer + rich |
| 文本向量化 | sentence-transformers |
| 向量数据库 | ChromaDB |
| AI 推理 | OpenAI 兼容 API (DeepSeek) |

## 开发指南

```bash
git clone https://github.com/ChenYiming-aaa/mind-garden.git
cd mind-garden
pip install -e .
```

## 贡献指南

欢迎贡献代码！请直接提交 Issue 或 Pull Request。

## 许可证

MIT © ChenYiming。详见 [LICENSE](LICENSE) 文件。