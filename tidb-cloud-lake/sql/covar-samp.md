---
title: COVAR_SAMP
summary: 2 つのデータカラムの標本共分散 (Σ((x - x̅)(y - y̅)) / (n - 1)) を返します。
---

# COVAR_SAMP

2 つのデータカラムの標本共分散 (Σ((x - x̅)(y - y̅)) / (n - 1)) を返します。

> **Note:**
>
> NULL 値はカウントされません。

## 構文 {#syntax}

```sql
COVAR_SAMP(<expr1>, <expr2>)
```

## 引数 {#arguments}

| 引数 | 説明 |
| --------- | ------------------------ |
| `<expr1>` | 任意の数値式 |
| `<expr2>` | 任意の数値式 |

## エイリアス {#aliases}

- [VAR_SAMP](/tidb-cloud-lake/sql/var-samp.md)
- [VARIANCE_SAMP](/tidb-cloud-lake/sql/variance-samp.md)

## 戻り値の型 {#return-type}

float64。`n <= 1` の場合は +∞ を返します。

## 例 {#example}

**Create a Table and Insert Sample Data**

```sql
CREATE TABLE store_sales (
  id INT,
  store_id INT,
  items_sold INT,
  profit FLOAT
);

INSERT INTO store_sales (id, store_id, items_sold, profit)
VALUES (1, 1, 100, 1000),
       (2, 2, 200, 2000),
       (3, 3, 300, 3000),
       (4, 4, 400, 4000),
       (5, 5, 500, 5000);
```

**Query Demo: Calculate Sample Covariance between Items Sold and Profit**

```sql
SELECT COVAR_SAMP(items_sold, profit) AS covar_samp_items_profit
FROM store_sales;
```

**結果**

```sql
| covar_samp_items_profit |
|-------------------------|
|        250000.0         |
```