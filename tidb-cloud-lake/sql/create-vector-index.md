---
title: CREATE VECTOR INDEX
summary: 在表的 VECTOR 列上创建 Vector 索引，以使用 HNSW（Hierarchical Navigable Small World）算法实现高效的相似性搜索。
---

# CREATE VECTOR INDEX

在表的 [VECTOR](/tidb-cloud-lake/sql/vector.md) 列上创建 Vector 索引，以使用 HNSW（Hierarchical Navigable Small World）算法实现高效的相似性搜索。

## 语法 {#syntax}

```sql
-- Create a Vector index on an existing table
CREATE [OR REPLACE] VECTOR INDEX [IF NOT EXISTS] <index_name>
ON [<database>.]<table_name>(<column>)
distance = '<metric>' [m = <number>] [ef_construct = <number>]

-- Create a Vector index when creating a table
CREATE [OR REPLACE] TABLE <table_name> (
    <column_definitions>,
    VECTOR INDEX <index_name> (<column>)
        distance = '<metric>' [m = <number>] [ef_construct = <number>]
)...
```

### 参数 {#parameters}

- **`distance`**（必需）- 指定用于相似性搜索的距离度量。可以使用逗号组合多个度量：
    - `'cosine'` - 余弦距离（最适合语义相似性、文本嵌入）
    - `'l1'` - L1 距离 / 曼哈顿距离（适合特征比较、稀疏数据）
    - `'l2'` - L2 距离 / 欧几里得距离（最适合几何相似性、图像特征）
    - 示例：`distance = 'cosine,l1,l2'` 支持这三种度量

- **`m`**（可选，默认值：16）- 控制 HNSW 图中每个节点拥有的双向连接数：
    - 更高的值会增加内存使用，但可以提高搜索准确性
    - 必须大于 0
    - 典型范围：8-64

- **`ef_construct`**（可选，默认值：100）- 控制索引构建期间动态候选列表的大小：
    - 更高的值会提高索引质量，但会增加构建时间和内存消耗
    - 必须 >= 40
    - 典型范围：40-500

## Vector 索引的工作原理 {#how-vector-index-works}

{{{ .lake }}} 中的 Vector 索引使用 HNSW 算法构建多层图结构：

1. **图结构**：每个向量都是一个节点，并与其最近邻建立连接
2. **搜索过程**：查询会在图的各层之间导航，从粗到细快速找到近似最近邻
3. **量化**：对原始向量进行量化，以减少存储并提升查询性能（准确性损失可忽略不计）
4. **自动构建**：索引会在数据写入时自动构建。每次 INSERT、COPY 或数据加载操作都会自动为新行生成索引，无需手动维护

## 示例 {#examples}

### 创建带有 Vector 索引的表 {#creating-a-table-with-vector-index}

```sql
-- Simple vector index for embeddings
CREATE TABLE documents (
    id INT,
    title VARCHAR,
    content TEXT,
    embedding VECTOR(1024),
    VECTOR INDEX idx_embedding(embedding) distance = 'cosine'
);
```

### 使用自定义参数创建 Vector 索引 {#creating-a-vector-index-with-custom-parameters}

```sql
-- Vector index with multiple distance metrics and tuned parameters
CREATE TABLE images (
    id INT,
    filename VARCHAR,
    feature_vector VECTOR(512),
    VECTOR INDEX idx_features(feature_vector)
        distance = 'cosine,l2'
        m = 32
        ef_construct = 200
);
```

### 在现有表上创建 Vector 索引 {#creating-a-vector-index-on-an-existing-table}

```sql
CREATE TABLE products (
    id INT,
    name VARCHAR,
    description TEXT,
    embedding VECTOR(768)
);

-- Add vector index after table creation
CREATE VECTOR INDEX idx_product_embedding
ON products(embedding)
distance = 'cosine,l1,l2'
m = 20
ef_construct = 150;
```

### 在不同列上创建多个 Vector 索引 {#multiple-vector-indexes-on-different-columns}

```sql
CREATE TABLE multimodal_data (
    id INT,
    text_embedding VECTOR(384),
    image_embedding VECTOR(512),
    VECTOR INDEX idx_text(text_embedding) distance = 'cosine',
    VECTOR INDEX idx_image(image_embedding) distance = 'l2'
);
```

### 查看索引 {#viewing-indexes}

使用 [SHOW INDEXES](/tidb-cloud-lake/sql/show-indexes.md) 查看所有索引：

```sql
SHOW INDEXES;
```

结果：

```
┌──────────────────────┬────────┬──────────┬────────────────────────────┬──────────────────────────┐
│ name                 │ type   │ original │ definition                 │ created_on               │
├──────────────────────┼────────┼──────────┼────────────────────────────┼──────────────────────────┤
│ idx_embedding        │ VECTOR │          │ documents(embedding)       │ 2025-05-13 01:22:34.123  │
│ idx_product_embedding│ VECTOR │          │ products(embedding)        │ 2025-05-13 01:23:45.678  │
└──────────────────────┴────────┴──────────┴────────────────────────────┴──────────────────────────┘
```

### 使用 Vector 索引进行相似性搜索 {#using-vector-index-for-similarity-search}

```sql
-- Create a table with vector index
CREATE TABLE wiki_articles (
    id INT,
    title VARCHAR,
    embedding VECTOR(8),
    VECTOR INDEX idx_embedding(embedding) distance = 'cosine'
);

-- Insert sample data (8-dimensional vectors for demonstration)
INSERT INTO wiki_articles VALUES
(1, 'Machine Learning', [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]),
(2, 'Deep Learning', [0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]),
(3, 'Natural Language Processing', [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]),
(4, 'Computer Vision', [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]);

-- Find the 2 most similar articles to a query vector using cosine distance
SELECT id, title, cosine_distance(embedding, [0.12, 0.22, 0.32, 0.42, 0.52, 0.62, 0.72, 0.82]) AS distance
FROM wiki_articles
ORDER BY distance ASC
LIMIT 2;
```

结果：

```
┌────┬─────────────────┬──────────────┐
│ id │ title           │ distance     │
├────┼─────────────────┼──────────────┤
│  1 │ Machine Learning│ 0.00012345   │
│  2 │ Deep Learning   │ 0.00023456   │
└────┴─────────────────┴──────────────┘
```

## 性能调优 {#performance-tuning}

### 选择距离度量 {#choosing-distance-metrics}

请根据你的使用场景选择合适的距离度量。有关如何使用距离函数进行查询，请参见 [向量函数](/tidb-cloud-lake/sql/vector-functions.md)。

- **余弦距离**：最适合来自 BERT、GPT 等模型的文本嵌入，此时向量的模长并不重要
- **L2（欧几里得）距离**：最适合图像特征、空间数据等绝对差异很重要的场景
- **L1（曼哈顿）距离**：适合稀疏向量，以及希望强调各个维度差异的场景

### 调优 HNSW 参数 {#tuning-hnsw-parameters}

| 参数 | 较低值 | 较高值 |
|----------------|--------------------------------------|--------------------------------------|
| `m`            | 更少内存，更快构建     | 更高准确性，更多内存         |
| `ef_construct` | 构建更快，质量较低   | 质量更高，构建更慢  |

**推荐配置：**

- **小型数据集（< 100K 个向量）**：默认设置（`m=16`，`ef_construct=100`）
- **中型数据集（100K - 1M 个向量）**：`m=24`，`ef_construct=150`
- **大型数据集（> 1M 个向量）**：`m=32`，`ef_construct=200`
- **高准确性要求**：`m=48`，`ef_construct=300`

## 限制 {#limitations}

- Vector 索引仅支持 [VECTOR](/tidb-cloud-lake/sql/vector.md) 数据类型的列
- `distance` 参数是必需的；如果索引未指定该参数，将被忽略
- 量化可能会在距离计算中引入可忽略不计的误差（通常 < 0.01%）
- 更高的 `m` 值会增加索引大小（每个向量大约增加 `m * vector_dimension * 4 bytes`）