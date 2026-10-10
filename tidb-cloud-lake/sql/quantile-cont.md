---
title: QUANTILE_CONT
summary: QUANTILE_CONT() 関数は、数値データのシーケンスの補間された分位数を計算します。
---

# QUANTILE_CONT

`QUANTILE_CONT()` 関数は、数値データのシーケンスの補間された分位数を計算します。

> **Note:**
>
> NULL 値はカウントされません。

## 構文 {#syntax}

```sql
QUANTILE_CONT(<levels>)(<expr>)
QUANTILE_CONT(level1, level2, ...)(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `<level(s)` | 分位数の level(s)。各 level は 0 から 1 までの定数浮動小数点数です。[0.01, 0.99] の範囲の level 値を使用することを推奨します。 |
| `<expr>`    | 任意の数値式 |

## 戻り値の型 {#return-type}

level の数に応じて、Float64 または float64 配列を返します。

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
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
```

**クエリのデモ: 補間を使用して売上金額の 50 パーセンタイル（中央値）を計算する**

```sql
SELECT QUANTILE_CONT(0.5)(sales_amount) AS median_sales_amount
FROM sales_data;
```

**結果**

```sql
|  median_sales_amount  |
|-----------------------|
|        6000.0         |
```