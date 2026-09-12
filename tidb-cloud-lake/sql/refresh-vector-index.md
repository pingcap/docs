---
title: REFRESH VECTOR INDEX
summary: 为在索引创建之前已插入的现有数据构建 Vector 索引。
---

# REFRESH VECTOR INDEX

为在索引创建之前已插入的现有数据构建 Vector 索引。

## 语法 {#syntax}

```sql
REFRESH VECTOR INDEX <index_name> ON [<database>.]<table_name>
```

## 何时使用 REFRESH {#when-to-use-refresh}

`REFRESH VECTOR INDEX` **仅在一种特定场景下**需要使用：当你在一个**已经包含数据**的表上创建 Vector 索引时。

现有行（即在索引创建之前写入的行）不会被自动建立索引。你必须运行 `REFRESH VECTOR INDEX`，为这些预先存在的数据构建索引。刷新完成后，之后的所有数据写入都会自动生成索引。

## 示例 {#examples}

### 示例：为现有数据建立索引 {#example-index-existing-data}

```sql
-- Step 1: Create a table without an index
CREATE TABLE products (
    id INT,
    name VARCHAR,
    embedding VECTOR(4)
) ENGINE = FUSE;

-- Step 2: Insert data (without index)
INSERT INTO products VALUES
    (1, 'Product A', [0.1, 0.2, 0.3, 0.4]),
    (2, 'Product B', [0.5, 0.6, 0.7, 0.8]),
    (3, 'Product C', [0.9, 1.0, 1.1, 1.2]);

-- Step 3: Create vector index on existing data
CREATE VECTOR INDEX idx_embedding ON products(embedding) distance='cosine';

-- Step 4: Refresh to build index for the 3 existing rows
REFRESH VECTOR INDEX idx_embedding ON products;

-- Step 5: New insertions are automatically indexed (no refresh needed)
INSERT INTO products VALUES (4, 'Product D', [1.3, 1.4, 1.5, 1.6]);
```