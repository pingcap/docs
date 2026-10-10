---
title: COVAR_POP
summary: 数値ペアの集合の母共分散を返します。
---

# COVAR_POP

数値ペアの集合の母共分散を返します。

## 構文 {#syntax}

```sql
COVAR_POP(<expr1>, <expr2>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------| ------------------------ |
| `<expr1>` | 任意の数値式 |
| `<expr2>` | 任意の数値式 |

## エイリアス {#aliases}

- [VAR_POP](/tidb-cloud-lake/sql/var-pop.md)
- [VARIANCE_POP](/tidb-cloud-lake/sql/variance-pop.md)

## 戻り値の型 {#return-type}

float64

## 例 {#example}

**テーブルを作成してサンプルデータを挿入**

```sql
CREATE TABLE product_sales (
  id INT,
  product_id INT,
  units_sold INT,
  revenue FLOAT
);

INSERT INTO product_sales (id, product_id, units_sold, revenue)
VALUES (1, 1, 10, 1000),
       (2, 2, 20, 2000),
       (3, 3, 30, 3000),
       (4, 4, 40, 4000),
       (5, 5, 50, 5000);
```

**クエリ例: 販売数量と売上高の間の母共分散を計算**

```sql
SELECT COVAR_POP(units_sold, revenue) AS covar_pop_units_revenue
FROM product_sales;
```

**結果**

```sql
| covar_pop_units_revenue |
|-------------------------|
|        20000.0          |
```