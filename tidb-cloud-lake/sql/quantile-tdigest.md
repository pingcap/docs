---
title: QUANTILE_TDIGEST
summary: t-digest アルゴリズムを使用して、数値データのシーケンスの近似分位数を計算します。
---

# QUANTILE_TDIGEST

[t-digest](https://github.com/tdunning/t-digest/blob/master/docs/t-digest-paper/histo.pdf) アルゴリズムを使用して、数値データのシーケンスの近似分位数を計算します。

> **Note:**
>
> NULL 値は計算に含まれません。

## 構文 {#syntax}

```sql
QUANTILE_TDIGEST(<level1>[, <level2>, ...])(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `<level n>` | 分位数のレベルは、0 から 1 までの定数浮動小数点数を表します。レベル値には [0.01, 0.99] の範囲を使用することを推奨します。 |
| `<expr>`    | 任意の数値式 |

## 戻り値の型 {#return-type}

指定した分位数レベルの数に応じて、Float64 値または Float64 値の配列を返します。

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

SELECT QUANTILE_TDIGEST(0.5)(sales_amount) AS median_sales_amount
FROM sales_data;

median_sales_amount|
-------------------+
             6000.0|

SELECT QUANTILE_TDIGEST(0.5, 0.8)(sales_amount)
FROM sales_data;

quantile_tdigest(0.5, 0.8)(sales_amount)|
----------------------------------------+
[6000.0,7000.0]                         |
```