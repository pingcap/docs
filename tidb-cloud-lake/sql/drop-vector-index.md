---
title: DROP VECTOR INDEX
summary: 从表中移除一个 Vector 索引。
---

# DROP VECTOR INDEX

从表中移除一个 Vector 索引。

## 语法 {#syntax}

```sql
DROP VECTOR INDEX [IF EXISTS] <index_name> ON [<database>.]<table_name>
```

## 示例 {#examples}

```sql
-- Create a table with a vector index
CREATE TABLE articles (
    id INT,
    title VARCHAR,
    embedding VECTOR(768),
    VECTOR INDEX idx_embedding(embedding) distance = 'cosine'
);

-- Drop the vector index
DROP VECTOR INDEX idx_embedding ON articles;

-- Drop with IF EXISTS to avoid errors if index doesn't exist
DROP VECTOR INDEX IF EXISTS idx_embedding ON articles;
```