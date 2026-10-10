---
title: PIVOT
summary: "{{{ .lake }}} の `PIVOT` 操作では、指定したカラムに基づいてテーブルを回転し、結果を集計して変換できます。"
---

# PIVOT

{{{ .lake }}} の `PIVOT` 操作では、指定したカラムに基づいてテーブルを回転し、結果を集計して変換できます。

これは、大量のデータをより読みやすい形式で要約および分析するのに便利な操作です。このドキュメントでは、構文を説明し、`PIVOT` 操作の使用例を示します。

**See also:** [UNPIVOT](/tidb-cloud-lake/sql/unpivot.md)

## 構文 {#syntax}

```sql
SELECT ...
FROM ...
   PIVOT ( <aggregate_function> ( <pivot_column> )
            FOR <value_column> IN ( <pivot_value_1> [ , <pivot_value_2> ... ] ) )

[ ... ]
```

説明:

* `<aggregate_function>`: `pivot_column` からグループ化された値を結合するための集計関数です。
* `<pivot_column>`: 指定した `<aggregate_function>` を使用して集計されるカラムです。
* `<value_column>`: その一意な値が、ピボット後の結果セットで新しいカラムになるカラムです。
* `<pivot_value_N>`: `<value_column>` の一意な値で、ピボット後の結果セットで新しいカラムになります。

## 例 {#examples}

異なる月における複数の従業員の売上データを含む `monthly_sales` というテーブルがあるとします。`PIVOT` 操作を使用すると、データを要約し、各月における各従業員の合計売上を計算できます。

### データの作成と挿入 {#creating-and-inserting-data}

```sql
-- Create the monthly_sales table
CREATE TABLE monthly_sales(
  empid INT,
  amount INT,
  month VARCHAR
);

-- Insert sales data
INSERT INTO monthly_sales VALUES
  (1, 10000, 'JAN'),
  (1, 400, 'JAN'),
  (2, 4500, 'JAN'),
  (2, 35000, 'JAN'),
  (1, 5000, 'FEB'),
  (1, 3000, 'FEB'),
  (2, 200, 'FEB'),
  (2, 90500, 'FEB'),
  (1, 6000, 'MAR'),
  (1, 5000, 'MAR'),
  (2, 2500, 'MAR'),
  (2, 9500, 'MAR'),
  (1, 8000, 'APR'),
  (1, 10000, 'APR'),
  (2, 800, 'APR'),
  (2, 4500, 'APR');
```

### PIVOT の使用 {#using-pivot}

次に、`PIVOT` 操作を使用して、各月における各従業員の合計売上を計算できます。合計売上の計算には `SUM` 集計関数を使用し、MONTH カラムをピボットして各月の新しいカラムを作成します。

```sql
SELECT *
FROM monthly_sales
PIVOT(SUM(amount) FOR MONTH IN ('JAN', 'FEB', 'MAR', 'APR'))
ORDER BY EMPID;
```

出力:

```sql
+-------+-------+-------+-------+-------+
| empid | jan   | feb   | mar   | apr   |
+-------+-------+-------+-------+-------+
|     1 | 10400 |  8000 | 11000 | 18000 |
|     2 | 39500 | 90700 | 12000 |  5300 |
+-------+-------+-------+-------+-------+
```