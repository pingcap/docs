---
title: SQL Variables
summary: SQL 変数を使用すると、セッション内で一時データを保存および管理でき、スクリプトをより動的で再利用しやすくできます。
---

# SQL Variables

SQL 変数を使用すると、セッション内で一時データを保存および管理でき、スクリプトをより動的で再利用しやすくできます。

## 変数コマンド {#variable-commands}

| コマンド | 説明 |
|---------|-------------|
| [SET VARIABLE](/tidb-cloud-lake/sql/set-variable.md) | セッション変数またはユーザー変数を作成または変更します。 |
| [UNSET VARIABLE](/tidb-cloud-lake/sql/unset-variable.md) | ユーザー定義変数を削除します。 |
| [SHOW VARIABLES](/tidb-cloud-lake/sql/show-variables.md) | システム変数とユーザー変数の現在の値を表示します。 |

SHOW VARIABLES コマンドには、対応するテーブル関数 [`SHOW_VARIABLES`](/tidb-cloud-lake/sql/show-variables.md) もあり、より高度なフィルタリングやクエリのために、同じ情報を表形式で返します。

## 変数を使ったクエリ {#querying-with-variables}

文の中で変数を参照して、値を動的に置き換えたり、実行時にオブジェクト名を構築したりできます。

### `$` と `getvariable()` を使った変数へのアクセス {#accessing-variables-with-and-getvariable}

`$` 記号または `getvariable()` 関数を使用して、変数の値をクエリに直接埋め込みます。

```sql title='Example:'
-- Set a variable to use as a filter value
SET VARIABLE threshold = 100;

-- Use the variable in a query with $
SELECT * FROM sales WHERE amount > $threshold;

-- Alternatively, use the getvariable() function
SELECT * FROM sales WHERE amount > getvariable('threshold');
```

### `IDENTIFIER` を使ったオブジェクトへのアクセス {#accessing-objects-with-identifier}

`IDENTIFIER` キーワードを使用すると、名前が変数に格納されているデータベースオブジェクトを参照でき、柔軟なクエリ構築が可能になります。（Note: LakeSQL はまだ `IDENTIFIER` をサポートしていません。）

```sql title='Example:'
-- Create a table with sales data
CREATE TABLE sales_data (region TEXT, sales_amount INT, month TEXT) AS
SELECT 'North', 5000, 'January' UNION ALL
SELECT 'South', 3000, 'January';

select * from sales_data;

-- Set variables for the table name and column name
SET VARIABLE table_name = 'sales_data';
SET VARIABLE column_name = 'sales_amount';

-- Use IDENTIFIER to dynamically reference the table and column in the query
SELECT region, IDENTIFIER($column_name)
FROM IDENTIFIER($table_name)
WHERE IDENTIFIER($column_name) > 4000;
```