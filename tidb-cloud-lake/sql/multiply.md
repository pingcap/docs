---
title: MULTIPLY
summary: MULTIPLY 関数は 2 つの数値の乗算を実行します。これは `*` 演算子を使用するのと同等です。
---

# MULTIPLY

MULTIPLY 関数は 2 つの数値の乗算を実行します。これは `*` 演算子を使用するのと同等です。

## 構文 {#syntax}

```sql
MULTIPLY(x, y)
-- Or using the operator syntax
x * y
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| x, y      | 乗算する数値式です。 |

## 戻り値の型 {#return-type}

入力引数に基づいて適切なデータ型の数値を返します。

## 例 {#examples}

```sql
-- Using the function syntax
SELECT MULTIPLY(5, 3);
+----------------+
| MULTIPLY(5, 3) |
+----------------+
|             15 |
+----------------+

-- Using the operator syntax
SELECT 5 * 3;
+-------+
| 5 * 3 |
+-------+
|    15 |
+-------+

-- With decimal numbers
SELECT MULTIPLY(2.5, 4);
+------------------+
| MULTIPLY(2.5, 4) |
+------------------+
|             10.0 |
+------------------+

-- With column references
SELECT number, MULTIPLY(number, 10) AS multiplied
FROM numbers(5);
+--------+------------+
| number | multiplied |
+--------+------------+
|      0 |          0 |
|      1 |         10 |
|      2 |         20 |
|      3 |         30 |
|      4 |         40 |
+--------+------------+
```

## 関連項目 {#see-also}

- [PLUS](/tidb-cloud-lake/sql/plus.md) / [ADD](/tidb-cloud-lake/sql/add.md)
- [MINUS](/tidb-cloud-lake/sql/minus.md) / [SUBTRACT](/tidb-cloud-lake/sql/subtract.md)
- [DIV](/tidb-cloud-lake/sql/div.md)