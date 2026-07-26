# mind-garden

<p align="right">
  <a href="../../README.md">中文</a> | <a href="README.en.md">English</a>
</p>

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