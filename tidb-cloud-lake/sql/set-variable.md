---
title: SET VARIABLE
summary: セッション内で 1 つ以上の SQL 変数の値を設定します。値には、単純な定数、式、クエリ結果、またはデータベースオブジェクトを指定できます。変数はセッションの継続中保持され、後続のクエリで使用できます。
---

# SET VARIABLE

セッション内で 1 つ以上の SQL 変数の値を設定します。値には、単純な定数、式、クエリ結果、またはデータベースオブジェクトを指定できます。変数はセッションの継続中保持され、後続のクエリで使用できます。

## 構文 {#syntax}

```sql
-- Set one variable
SET VARIABLE <variable_name> = <expression>

-- Set more than one variable
SET VARIABLE (<variable1>, <variable2>, ...) = (<expression1>, <expression2>, ...)

-- Set multiple variables from a query result
SET VARIABLE (<variable1>, <variable2>, ...) = <query>
```

## 変数へのアクセス {#accessing-variables}

変数には、ドル記号構文 `$variable_name` を使用してアクセスできます。

## 例 {#examples}

### 単一の変数を設定する {#setting-a-single-variable}

```sql
-- Sets variable a to the string 'datalake'
SET VARIABLE a = 'datalake';

-- Access the variable
SELECT $a;
┌─────────┐
│ $a      │
├─────────┤
│ datalake│
└─────────┘
```

### 複数の変数を設定する {#setting-multiple-variables}

```sql
-- Sets variable x to 'xx' and y to 'yy'
SET VARIABLE (x, y) = ('xx', 'yy');

-- Access multiple variables
SELECT $x, $y;
┌────┬────┐
│ $x │ $y │
├────┼────┤
│ xx │ yy │
└────┴────┘
```

### クエリ結果から変数を設定する {#setting-variables-from-query-results}

```sql
-- Sets variable a to 3 and b to 55
SET VARIABLE (a, b) = (SELECT 3, 55);

-- Access the variables
SELECT $a, $b;
┌────┬────┐
│ $a │ $b │
├────┼────┤
│ 3  │ 55 │
└────┴────┘
```

### 動的なテーブル参照 {#dynamic-table-references}

変数は `IDENTIFIER()` 関数と組み合わせて使用することで、データベースオブジェクトを動的に参照できます。

```sql
-- Create a sample table
CREATE OR REPLACE TABLE monthly_sales(empid INT, amount INT, month TEXT) AS SELECT 1, 2, '3';

-- Set a variable 't' to the name of the table 'monthly_sales'
SET VARIABLE t = 'monthly_sales';

-- Access the variable directly
SELECT $t;
┌──────────────┐
│ $t           │
├──────────────┤
│ monthly_sales│
└──────────────┘

-- Use IDENTIFIER to dynamically reference the table name stored in the variable 't'
SELECT * FROM IDENTIFIER($t);
┌───────┬────────┬───────┐
│ empid │ amount │ month │
├───────┼────────┼───────┤
│     1 │      2 │ 3     │
└───────┴────────┴───────┘
```