---
title: CREATE TEMP TABLE
summary: セッションの終了時に自動的に削除される一時テーブルを作成します。
---

# CREATE TEMP TABLE

セッションの終了時に自動的に削除される一時テーブルを作成します。

- 一時テーブルは、それを作成したセッション内でのみ可視であり、セッションの終了時に、すべてのデータが vacuum されたうえで自動的に削除されます。
       - 一時テーブルの自動クリーンアップに失敗した場合（たとえば、query node のクラッシュが原因の場合）は、[FUSE_VACUUM_TEMPORARY_TABLE](/tidb-cloud-lake/sql/fuse-vacuum-temporary-table.md) 関数を使用して、一時テーブルの残存ファイルを手動でクリーンアップできます。
- セッション内の既存の一時テーブルを表示するには、[system.temporary_tables](/tidb-cloud-lake/sql/system-tables.md) システムテーブルをクエリします。[Example-1](#example-1) を参照してください。
- 通常テーブルと同じ名前の一時テーブルは優先され、一時テーブルが削除されるまで通常テーブルは隠されます。[Example-2](#example-2) を参照してください。
- 一時テーブルの作成や操作に権限は不要です。
- {{{ .lake }}} は、[Fuse Engine](/tidb-cloud-lake/sql/table-engines.md) を使用した一時テーブルの作成をサポートしています。
- LakeSQL を使用して一時テーブルを作成するには、LakeSQL の最新バージョンを使用していることを確認してください。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] { TEMPORARY | TEMP } TABLE
       [ IF NOT EXISTS ]
       [ <database_name>. ]<table_name>
       ...
```

省略された部分は、[CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) の構文に従います。

## 例 {#examples}

### Example-1 {#example-1}

この例では、一時テーブルを作成し、[system.temporary_tables](/tidb-cloud-lake/sql/system-tables.md) システムテーブルをクエリしてその存在を確認する方法を示します。

```sql
CREATE TEMP TABLE my_table (id INT, description STRING);

SELECT * FROM system.temporary_tables;

┌────────────────────────────────────────────────────┐
│ database │   name   │       table_id      │ engine │
├──────────┼──────────┼─────────────────────┼────────┤
│ default  │ my_table │ 4611686018427407904 │ FUSE   │
└────────────────────────────────────────────────────┘
```

### Example-2 {#example-2}

この例では、通常テーブルと同じ名前の一時テーブルがどのように優先されるかを示します。両方のテーブルが存在する場合、操作対象は一時テーブルとなり、通常テーブルは実質的に隠されます。一時テーブルが削除されると、通常テーブルに再びアクセスできるようになります。

```sql
-- Create a normal table
CREATE TABLE my_table (id INT, name STRING);

-- Insert data into the normal table
INSERT INTO my_table VALUES (1, 'Alice'), (2, 'Bob');

-- Create a temporary table with the same name
CREATE TEMP TABLE my_table (id INT, description STRING);

-- Insert data into the temporary table
INSERT INTO my_table VALUES (1, 'Temp Data');

-- Query the table: This will access the temporary table, hiding the normal table
SELECT * FROM my_table;

┌────────────────────────────────────┐
│        id       │    description   │
├─────────────────┼──────────────────┤
│               1 │ Temp Data        │
└────────────────────────────────────┘

-- Drop the temporary table
DROP TABLE my_table;

-- Query the table again: Now the normal table is accessible
SELECT * FROM my_table;

┌────────────────────────────────────┐
│        id       │       name       │
├─────────────────┼──────────────────┤
│               1 │ Alice            │
│               2 │ Bob              │
└────────────────────────────────────┘
```