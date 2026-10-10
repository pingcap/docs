---
title: APPROX_COUNT_DISTINCT
summary: HyperLogLog アルゴリズムを使用して、データセット内の異なる値の数を推定します。
---

# APPROX_COUNT_DISTINCT

[HyperLogLog](https://en.wikipedia.org/wiki/HyperLogLog) アルゴリズムを使用して、データセット内の異なる値の数を推定します。

HyperLogLog アルゴリズムは、少ないメモリと時間で一意な要素数の近似値を提供します。推定結果を許容できる大規模なデータセットを扱う場合は、この関数の使用を検討してください。精度と引き換えに、高速かつ効率的に distinct count を返す方法です。

正確な結果を取得するには、[COUNT_DISTINCT](/tidb-cloud-lake/sql/count-distinct.md) を使用してください。詳細は [例](#example) を参照してください。

## 構文 {#syntax}

```sql
APPROX_COUNT_DISTINCT(<expr>)
```

## 戻り値の型 {#return-type}

整数。

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
CREATE TABLE user_events (
  id INT,
  user_id INT,
  event_name VARCHAR
);

INSERT INTO user_events (id, user_id, event_name)
VALUES (1, 1, 'Login'),
       (2, 2, 'Login'),
       (3, 3, 'Login'),
       (4, 1, 'Logout'),
       (5, 2, 'Logout'),
       (6, 4, 'Login'),
       (7, 1, 'Login');
```

**クエリのデモ: 異なるユーザー ID の数を推定する**

```sql
SELECT APPROX_COUNT_DISTINCT(user_id) AS approx_distinct_user_count
FROM user_events;
```

**結果**

```sql
| approx_distinct_user_count |
|----------------------------|
|             4              |
```