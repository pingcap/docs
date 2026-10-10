---
title: UNDROP TABLE
summary: 削除されたテーブルの直近のバージョンを復元します。これは {{{ .lake }}} の Time Travel 機能を利用しており、削除されたオブジェクトは保持期間内でのみ復元できます（デフォルトは 24 時間）。
---

# UNDROP TABLE

削除されたテーブルの直近のバージョンを復元します。これは {{{ .lake }}} の Time Travel 機能を利用しており、削除されたオブジェクトは保持期間内でのみ復元できます（デフォルトは 24 時間）。

**See also:**

- [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)
- [DROP TABLE](/tidb-cloud-lake/sql/drop-table.md)
- [SHOW TABLES](/tidb-cloud-lake/sql/show-tables.md)
- [SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md)

## 構文 {#syntax}

```sql
UNDROP TABLE [ <database_name>. ]<table_name>
```

- 同じ名前のテーブルがすでに存在する場合は、エラーが返されます。

    ```sql title='Examples:'
    root@localhost:8000/default> CREATE TABLE t(id INT);
    processed in (0.036 sec)

    root@localhost:8000/default> DROP TABLE t;
    processed in (0.033 sec)

    root@localhost:8000/default> CREATE TABLE t(id INT, name STRING);
    processed in (0.030 sec)

    root@localhost:8000/default> UNDROP TABLE t;
    error: APIError: QueryFailed: [2308]Undrop Table 't' already exists
    ```

- テーブルを UNDROP しても、元のロールへの所有権は自動的には復元されません。UNDROP 後は、以前のロールまたは別のロールに対して所有権を手動で付与する必要があります。それまでは、そのテーブルにアクセスできるのは `account-admin` ロールのみです。

    ```sql title='Examples:'
    GRNAT OWNERSHIP on doc.t to ROLE writer;
    ```

## 例 {#examples}

```sql
CREATE TABLE test(a INT, b VARCHAR);

-- drop table
DROP TABLE test;

-- show dropped tables from current database
SHOW TABLES HISTORY;

┌────────────────────────────────────────────────────┐
│ Tables_in_orders_2024 │          drop_time         │
├───────────────────────┼────────────────────────────┤
│ test                  │ 2024-01-23 04:56:34.766820 │
└────────────────────────────────────────────────────┘

-- restore table
UNDROP TABLE test;
```