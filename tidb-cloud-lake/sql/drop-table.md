---
title: DROP TABLE
summary: Deletes a table.
---

# DROP TABLE

> **Note:**
>
> Introduced or updated in v1.2.155.

Deletes a table.

**See also:**

- [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)
- [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md)
- [TRUNCATE TABLE](/tidb-cloud-lake/sql/truncate-table.md)

## Syntax

```sql
DROP TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
```

This command only marks the table schema as deleted in the metadata service, ensuring that the actual data remains intact. If you need to recover the deleted table schema, you can use the [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md) command.

For completely removing a table along with its data files, consider using the [VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md) command.

## Examples

### Deleting a Table

This example highlights the use of the DROP TABLE command to delete the "test" table. After dropping the table, any attempt to SELECT from it results in an "Unknown table" error. It also demonstrates how to recover the dropped "test" table using the UNDROP TABLE command, allowing you to SELECT data from it again.

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
