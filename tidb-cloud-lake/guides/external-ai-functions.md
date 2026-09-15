---
title: 外部 AI 函数
summary: 通过将 {{{ .lake }}} 与您自己的基础设施连接，构建强大的 AI/ML 能力。外部函数让您能够部署自定义模型、利用 GPU 加速，并与任何 ML 框架集成，同时确保数据安全。
---

# 外部 AI 函数

通过将 {{{ .lake }}} 与您自己的基础设施连接，构建强大的 AI/ML 能力。外部函数让您能够部署自定义模型、利用 GPU 加速，并与任何 ML 框架集成，同时确保数据安全。

## 关键能力 {#key-capabilities}

| 功能 | 优势 |
|---------|----------|
| **自定义模型** | 使用任何开源或专有的 AI/ML 模型 |
| **GPU 加速** | 部署在配备 GPU 的机器上，以实现更快的推理 |
| **数据隐私** | 将数据保留在您的基础设施内部 |
| **扩展性** | 独立扩缩容和资源优化 |
| **灵活性** | 支持任何编程语言和 ML 框架 |

## 工作原理 {#how-it-works}

1. **Create AI Server**：使用 Python 和 [`tidbcloudlake-udf`](https://pypi.org/project/tidbcloudlake-udf/) 构建您的 AI/ML 服务器
2. **Register Function**：使用 `CREATE FUNCTION` 将您的服务器连接到 {{{ .lake }}}
3. **Use in SQL**：直接在 SQL 查询中调用您的自定义 AI 函数

## 示例：文本嵌入函数 {#example-text-embedding-function}

```python
# Simple embedding UDF server demo
from tidbcloudlake_udf import udf, UDFServer
from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer('all-mpnet-base-v2')  # 768-dimensional vectors

@udf(
    input_types=["STRING"],
    result_type="ARRAY(FLOAT)",
)
def ai_embed_768(inputs: list[str], headers) -> list[list[float]]:
    """Generate 768-dimensional embeddings for input texts"""
    try:
        # Process inputs in a single batch
        embeddings = model.encode(inputs)
        # Convert to list format
        return [embedding.tolist() for embedding in embeddings]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        # Return empty lists in case of error
        return [[] for _ in inputs]

if __name__ == '__main__':
    print("Starting embedding UDF server on port 8815...")
    server = UDFServer("0.0.0.0:8815")
    server.add_function(ai_embed_768)
    server.serve()
```

```sql
-- Register the external function in {{{ .lake }}}
CREATE OR REPLACE FUNCTION ai_embed_768 (STRING)
    RETURNS ARRAY(FLOAT)
    LANGUAGE PYTHON
    HANDLER = 'ai_embed_768'
    ADDRESS = 'https://your-ml-server.example.com';

-- Use the custom embedding in queries
SELECT
    id,
    title,
    cosine_distance(
        ai_embed_768(content),
        ai_embed_768('machine learning techniques')
    ) AS similarity
FROM articles
ORDER BY similarity ASC
LIMIT 5;
```