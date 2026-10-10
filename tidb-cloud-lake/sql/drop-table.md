---
title: DROP TABLE
summary: テーブルを削除します。
---

# DROP TABLE

テーブルを削除します。

**See also:**

- [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)
- [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md)
- [TRUNCATE TABLE](/tidb-cloud-lake/sql/truncate-table.md)

## 構文 {#syntax}

```sql
DROP TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
```

このコマンドは、メタデータサービス内でテーブルスキーマを削除済みとしてマークするだけで、実際のデータはそのまま保持されます。削除したテーブルスキーマを復元する必要がある場合は、[UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md) コマンドを使用できます。

データファイルを含めてテーブルを完全に削除するには、[VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md) コマンドの使用を検討してください。

## 例 {#examples}

### テーブルの削除 {#deleting-a-table}

この例では、DROP TABLE コマンドを使用して `"test"` テーブルを削除する方法を示します。テーブルを削除した後にそのテーブルに対して SELECT を実行しようとすると、`"Unknown table"` エラーが発生します。また、UNDROP TABLE コマンドを使用して削除した `"test"` テーブルを復元し、再びそのデータを SELECT できるようにする方法も示しています。

```sql
CREATE TABLE test(a INT, b VARCHAR);
INSERT INTO test (a, b) VALUES (1, 'example');
SELECT * FROM test;

a|b      |
-+-------+
1|example|

-- Delete the table
DROP TABLE test;
SELECT * FROM test;
>> SQL Error [1105] [HY000]: UnknownTable. Code: 1025, Text = error:
  --> SQL:1:80
  |
1 | /* ApplicationName=DBeaver 23.2.0 - SQLEditor <Script-12.sql> */ SELECT * FROM test
  |                                                                                ^^^^ Unknown table `default`.`test` in catalog 'default'

-- Recover the table
UNDROP TABLE test;
SELECT * FROM test;

a|b      |
-+-------+
1|example|
```