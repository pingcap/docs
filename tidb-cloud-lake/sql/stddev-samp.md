---
title: STDDEV_SAMP
summary: 式の標本標準偏差（VAR_SAMP() の平方根）を返します。
---

# STDDEV_SAMP

式の標本標準偏差（VAR_SAMP() の平方根）を返します。

- NULL 値は無視されます。
- 入力レコードが 1 件しかない場合、STDDEV_SAMP() は `0` ではなく `NULL` を返します。

## 構文 {#syntax}

```sql
STDDEV_SAMP(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
| --------- | ------------------------ |
| `<expr>`  | 任意の数値式 |

## 戻り値の型 {#return-type}

Double。

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
CREATE TABLE height_data (
  id INT,
  person_id INT,
  height FLOAT
);

INSERT INTO height_data (id, person_id, height)
VALUES (1, 1, 5.8),
       (2, 2, 6.1),
       (3, 3, 5.9),
       (4, 4, 5.7),
       (5, 5, 6.3);
```

**クエリ例: 身長の標本標準偏差を計算する**

```sql
SELECT STDDEV_SAMP(height) AS height_stddev_samp
FROM height_data;
```

**結果**

```sql
| height_stddev_samp |
|--------------------|
|      0.240         |
```