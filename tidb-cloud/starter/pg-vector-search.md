---
title: 向量搜索
summary: 了解如何在 PostgreSQL-compatible TiDB Cloud Starter 中存储向量嵌入、执行相似性搜索以及创建 HNSW 索引。
---

# 向量搜索

PostgreSQL-compatible {{{ .starter }}} 提供与 pgvector 兼容的向量存储和相似性搜索能力，包括 `VECTOR` 类型、距离运算符、HNSW 索引以及服务端嵌入函数。

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} 当前处于公测阶段。

## 启用向量搜索 {#enable-vector-search}

`VECTOR` 类型和向量运算符是内置的。要注册 `vector` 扩展元信息，请运行：

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

要使用服务端嵌入函数，请启用 `embedding` 扩展：

```sql
CREATE EXTENSION IF NOT EXISTS embedding;
```

## 存储向量 {#store-vectors}

使用 `VECTOR(n)` 存储固定维度的向量。

例如：

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(3)
);
```

你可以使用向量字面量插入向量：

```sql
INSERT INTO documents (content, embedding)
VALUES ('hello world', '[0.1, 0.2, 0.3]'::vector);
```

向量的维度数必须与目标 `VECTOR(n)` 列声明的维度一致。

## 距离运算符 {#distance-operators}

PostgreSQL-compatible {{{ .starter }}} 支持以下与 pgvector 兼容的距离运算符：

| 运算符 | 距离度量 | 等价函数 |
| --- | --- | --- |
| `<->` | L2（欧氏距离） | `l2_distance(a, b)` |
| `<=>` | 余弦距离 | `cosine_distance(a, b)` |
| `<#>` | 负内积 | `vector_negative_inner_product(a, b)` |

例如，以下查询执行一次余弦距离搜索：

```sql
SELECT
    id,
    content,
    embedding <=> '[0.1, 0.2, 0.3]'::vector AS distance
FROM documents
ORDER BY distance
LIMIT 5;
```

还提供以下实用函数：

| 函数 | 说明 |
| --- | --- |
| `l2_distance(a, b)` | 计算欧氏距离。 |
| `cosine_distance(a, b)` | 计算余弦距离。 |
| `inner_product(a, b)` | 计算内积。 |
| `vector_negative_inner_product(a, b)` | 计算 `<#>` 使用的负内积。 |
| `vector_dims(v)` | 返回维度数。 |
| `vector_norm(v)` | 返回 L2 范数。 |
| `l2_normalize(v)` | 返回经过 L2 归一化的向量。 |

## 创建 HNSW 索引 {#create-an-hnsw-index}

HNSW（Hierarchical Navigable Small World）索引用于加速近似最近邻搜索。

创建索引时，其操作符类应与查询使用的距离度量匹配。

对于余弦距离：

```sql
CREATE INDEX idx_documents_embedding
ON documents
USING hnsw (embedding vector_cosine_ops);
```

对于 L2 距离：

```sql
CREATE INDEX idx_documents_embedding_l2
ON documents
USING hnsw (embedding vector_l2_ops);
```

对于内积：

```sql
CREATE INDEX idx_documents_embedding_ip
ON documents
USING hnsw (embedding vector_ip_ops);
```

### 配置 HNSW 索引参数 {#configure-hnsw-index-parameters}

你可以在创建索引时配置 HNSW 索引构建参数：

```sql
CREATE INDEX idx_documents_embedding
ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `m` | 16 | 每个 layer 的最大连接数。更高的值可以提升召回率，但会消耗更多内存。 |
| `ef_construction` | 64 | 索引构建期间的搜索宽度。更高的值可以提升索引质量，但会降低构建速度。 |

你可以为当前会话配置 HNSW 搜索扩展因子：

```sql
SET hnsw.ef_search = 100;
```

`hnsw.ef_search` 的默认值为 `40`。更高的值可以提升召回率，但会增加查询延时。

### HNSW 索引何时会被使用 {#when-an-hnsw-index-is-used}

当满足以下所有条件时，优化器可以使用 HNSW 索引：

- 查询按已建立索引的向量列与一个常量向量之间的距离表达式排序，或者在该列上使用 `vec_embed_cosine_distance()` 且查询文本为常量。
- 查询包含 `LIMIT` 子句。
- HNSW 索引使用的操作符类与查询中的距离度量匹配。
- HNSW 索引已完成构建，并可用于查询。
- 查询不包含 `WHERE` 子句。

例如：

```sql
SELECT id, content
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, 0.3]'::vector
LIMIT 10;
```

如果不满足这些条件，查询会回退为精确的顺序扫描。结果仍然正确，但不会使用 HNSW 索引。

> **Note:**
>
> 用作查询向量的绑定参数在 HNSW 规划中不会被视为常量。例如，`ORDER BY embedding <=> $1::vector LIMIT 10` 会回退为顺序扫描。

## 在 SQL 中生成向量嵌入 {#generate-embeddings-in-sql}

`embedding` 扩展提供服务端嵌入函数。

从文本生成向量嵌入：

```sql
SELECT embedding('hello world');
```

你也可以使用 `embed_text()` 并显式指定模型：

```sql
SELECT embed_text('text-embedding-v4', 'hello world');
```

当前支持的向量嵌入维度为 256、512 和 1024。默认输出维度为 1024。

要为当前会话更改输出维度：

```sql
SET embedding.dimensions = 512;

SELECT embedding('hello world');
```

## 端到端示例 {#end-to-end-example}

以下示例会创建一个表、生成向量嵌入、创建 HNSW 索引，并执行语义搜索：

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS embedding;

SET embedding.dimensions = 1024;

CREATE TABLE docs (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    vec VECTOR(1024)
);

INSERT INTO docs (content, vec) VALUES
    ('PostgreSQL is a relational database',
     embedding('PostgreSQL is a relational database')),
    ('TiDB Cloud provides a managed database service',
     embedding('TiDB Cloud provides a managed database service')),
    ('Vector search finds semantically similar documents',
     embedding('Vector search finds semantically similar documents'));

CREATE INDEX idx_docs_vec
ON docs
USING hnsw (vec vector_cosine_ops);

SELECT content
FROM docs
ORDER BY vec_embed_cosine_distance(vec, 'managed database')
LIMIT 3;
```

`vec_embed_cosine_distance()` 查询可以使用 `idx_docs_vec` 执行余弦距离搜索。你可以在 `SELECT` 语句前添加 `EXPLAIN`，以检查执行计划中是否包含使用该索引的 `HNSW Scan`。

## 使用自动嵌入进行搜索 {#search-with-automatic-embedding}

你可以在一次函数调用中完成查询文本的向量嵌入和距离计算。

以下示例使用前一节中创建的 `docs` 表。`docs.vec` 列存储由默认嵌入模型生成的 1024 维向量嵌入。

```sql
SELECT id, content
FROM docs
ORDER BY vec_embed_cosine_distance(vec, 'database for AI applications')
LIMIT 5;
```

查询向量嵌入必须与已存储的向量嵌入使用相同的模型和维度。

可用的函数如下：

| 函数 | 等效操作 |
| --- | --- |
| `vec_embed_l2_distance(vec, text)` | `l2_distance(vec, embedding(text))` |
| `vec_embed_cosine_distance(vec, text)` | `cosine_distance(vec, embedding(text))` |
| `vec_embed_inner_product(vec, text)` | `inner_product(vec, embedding(text))` |

## 限制 {#limitations}

以下限制适用于向量搜索公测期间：

- 不支持 IVFFlat 索引。当前支持的近似最近邻索引类型为 HNSW。
- 一个 HNSW 索引只能包含一个向量列。
- 被索引的向量列必须显式声明维度，例如 `VECTOR(1024)`。不要对未指定维度的 `VECTOR` 列使用 HNSW 索引。
- 表必须具有单列主键。没有主键或使用复合主键的表无法使用 HNSW 索引。
- 如果主键是 `INTEGER` 或 `BIGINT`，其值必须为非负数。`UUID` 和 `TEXT` 主键不受此限制。
- 不支持部分 HNSW 索引。
- 距离运算要求向量的维度一致。
- `embedding()` 和 `embed_text()` 函数要求数据库用户具有足够的权限。
- HNSW 加速对查询形态有限制。不满足[HNSW 索引何时会被使用](#when-an-hnsw-index-is-used)中所述要求的查询，将改为使用精确的顺序扫描。