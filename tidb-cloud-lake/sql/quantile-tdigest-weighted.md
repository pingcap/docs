---
title: QUANTILE_TDIGEST_WEIGHTED
summary: t-digest アルゴリズムを使用して、数値データのシーケンスの近似分位数を計算します。この関数は、シーケンスの各メンバーの重みを考慮します。メモリ消費量は log(n) で、n は値の数です。
---

# QUANTILE_TDIGEST_WEIGHTED

[t-digest](https://github.com/tdunning/t-digest/blob/master/docs/t-digest-paper/histo.pdf) アルゴリズムを使用して、数値データのシーケンスの近似分位数を計算します。

この関数は、シーケンスの各メンバーの重みを考慮します。メモリ消費量は **log(n)** で、**n** は値の数です。

> **Note:**
>
> NULL 値は計算に含まれません。

## 構文 {#syntax}

```sql
QUANTILE_TDIGEST_WEIGHTED(<level1>[, <level2>, ...])(<expr>, <weight_expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<level n>`     | 分位数のレベルは、0 から 1 の範囲の定数浮動小数点数を表します。[0.01, 0.99] の範囲のレベル値を使用することを推奨します。 |
| `<expr>`        | 任意の数値式 |
| `<weight_expr>` | 任意の符号なし整数式。重みは値の出現回数を表します。 |

## 戻り値の型 {#return-type}

指定された分位数レベルの数に応じて、Float64 値または Float64 値の配列を返します。

## 例 {#example}

```sql
-- Create a table and insert sample data
CREATE TABLE sales_data (
  id INT,
  sales_person_id INT,
  sales_amount FLOAT
);

INSERT INTO sales_data (id, sales_person_id, sales_amount)
VALUES (1, 1, 5000),
       (2, 2, 5500),
       (3, 3, 6000),
       (4, 4, 6500),
       (5, 5, 7000);

SELECT QUANTILE_TDIGEST_WEIGHTED(0.5)(sales_amount, 1) AS median_sales_amount
FROM sales_data;

median_sales_amount|
-------------------+
             6000.0|

SELECT QUANTILE_TDIGEST_WEIGHTED(0.5, 0.8)(sales_amount, 1)
FROM sales_data;

quantile_tdigest_weighted(0.5, 0.8)(sales_amount)|
-------------------------------------------------+
[6000.0,7000.0]                                  |
```