# mind-garden

个人知识库助手 — 将本地 Markdown 笔记转化为可语义搜索和 AI 对话的私有知识库。

## 快速开始

```bash
# 安装
pip install -e .

# 索引笔记
mind-garden index ./my-notes

# 语义搜索
mind-garden search "你的问题" --top-k 5

# AI 问答（需要设置 DEEPSEEK_API_KEY）
export DEEPSEEK_API_KEY="your-key"
mind-garden ask "你的问题"
```

## 环境变量

| 变量 | 说明 | 默认值 |
|---|---|---|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | — |
| `DEEPSEEK_BASE_URL` | API 地址 | `https://api.deepseek.com/v1` |
| `MIND_GARDEN_MODEL` | AI 对话模型 | `deepseek-v4-flash` |

## 数据存储

向量数据库默认持久化为 `~/.mind-garden/chroma/`。
