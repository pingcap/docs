---
title: COUNT_DISTINCT
summary: 集約関数。
---

# COUNT_DISTINCT

集約関数。

`count(distinct ...)` 関数は、値の集合における一意な値の数を計算します。

大規模なデータセットに対して、少ないメモリと時間で推定結果を取得するには、[APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/approx-count-distinct.md) の使用を検討してください。

> **Note:**
>
> NULL 値はカウントされません。

## 構文 {#syntax}

```sql
COUNT(distinct <expr> ...)
UNIQ(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|--------------------------------------------------|
| `<expr>`  | 任意の式。引数の数の範囲は [1, 32] です |

## 戻り値の型 {#return-type}

UInt64

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
CREATE TABLE products (
  id INT,
  name VARCHAR,
  category VARCHAR,
  price FLOAT
);

INSERT INTO products (id, name, category, price)
VALUES (1, 'Laptop', 'Electronics', 1000),
       (2, 'Smartphone', 'Electronics', 800),
       (3, 'Tablet', 'Electronics', 600),
       (4, 'Chair', 'Furniture', 150),
       (5, 'Table', 'Furniture', 300);
```

**クエリ例: 異なる category の数をカウントする**

```sql
SELECT COUNT(DISTINCT category) AS unique_categories
FROM products;
```

**結果**

```sql
| unique_categories |
|-------------------|
|         2         |
```