---
title: QUANTILE_DISC
summary: `QUANTILE_DISC()` 関数は、数値データのシーケンスの正確な分位数を計算します。
---

# QUANTILE_DISC

`QUANTILE_DISC()` 関数は、数値データのシーケンスの正確な分位数を計算します。`QUANTILE` は `QUANTILE_DISC` のエイリアスです。

> **Note:**
>
> NULL 値はカウントされません。

## 構文 {#syntax}

```sql
QUANTILE_DISC(<levels>)(<expr>)
QUANTILE_DISC(level1, level2, ...)(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `level(s)` | 分位数の level(s) です。各 level は 0 から 1 までの定数浮動小数点数です。[0.01, 0.99] の範囲の level 値を使用することを推奨します。 |
| `<expr>`   | 任意の数値式 |
 
## 戻り値の型 {#return-type}

level の数に応じて、InputType または InputType の配列を返します。

## 例 {#example}

**Create a Table and Insert Sample Data**

```sql
CREATE TABLE salary_data (
  id INT,
  employee_id INT,
  salary FLOAT
);

INSERT INTO salary_data (id, employee_id, salary)
VALUES (1, 1, 50000),
       (2, 2, 55000),
       (3, 3, 60000),
       (4, 4, 65000),
       (5, 5, 70000);
```

**Query Demo: Calculate 25th and 75th Percentile of Salaries**

```sql
SELECT QUANTILE_DISC(0.25, 0.75)(salary) AS salary_quantiles
FROM salary_data;
```

**結果**

```sql
|  salary_quantiles   |
|---------------------|
| [55000.0, 65000.0]  |
```