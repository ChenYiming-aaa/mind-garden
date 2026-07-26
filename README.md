<h1 align="center">mind-garden</h1>

> 个人知识库助手 — 将本地 Markdown 笔记转化为可语义搜索和 AI 对话的私有知识库

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="license" />
  <img src="https://img.shields.io/github/last-commit/ChenYiming-aaa/mind-garden" alt="last commit" />
  <img src="https://img.shields.io/github/languages/count/ChenYiming-aaa/mind-garden" alt="languages" />
  <img src="https://img.shields.io/github/languages/code-size/ChenYiming-aaa/mind-garden" alt="code size" />
</p>

<p align="center">
  <b>中文</b> · <a href="docs/i18n/README.en.md">English</a>
</p>

---

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