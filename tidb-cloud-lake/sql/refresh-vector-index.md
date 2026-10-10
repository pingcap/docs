---
title: REFRESH VECTOR INDEX
summary: インデックス作成前に挿入された既存データに対して Vector index を構築します。
---

# REFRESH VECTOR INDEX

インデックス作成前に挿入された既存データに対して Vector index を構築します。

## 構文 {#syntax}

```sql
REFRESH VECTOR INDEX <index_name> ON [<database>.]<table_name>
```

## REFRESH を使用するタイミング {#when-to-use-refresh}

`REFRESH VECTOR INDEX` が**必要になるのは、特定の 1 つのシナリオのみ**です。つまり、**すでにデータが含まれている**テーブルに Vector index を作成する場合です。

既存の行（インデックス作成前に書き込まれたデータ）は、自動的にはインデックス化されません。この既存データに対してインデックスを構築するには、`REFRESH VECTOR INDEX` を実行する必要があります。リフレッシュが完了すると、それ以降に書き込まれるすべてのデータについては自動的にインデックスが生成されます。

## 例 {#examples}

### 例: 既存データにインデックスを作成する {#example-index-existing-data}

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