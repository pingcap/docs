---
title: DROP TABLE
summary: 删除表。
---

# DROP TABLE

删除表。

**另请参阅：**

- [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)
- [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md)
- [TRUNCATE TABLE](/tidb-cloud-lake/sql/truncate-table.md)

## 语法 {#syntax}

```sql
DROP TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
```

此命令仅在元信息服务中将表结构标记为已删除，以确保实际数据保持不变。如果你需要恢复已删除的表结构，可以使用 [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md) 命令。

如果要连同数据文件一起彻底删除表，请考虑使用 [VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md) 命令。

## 示例 {#examples}

### 删除表 {#deleting-a-table}

本示例展示了如何使用 DROP TABLE 命令删除 `"test"` 表。删除该表后，任何对其执行 SELECT 的尝试都会返回 `"Unknown table"` 错误。该示例还演示了如何使用 UNDROP TABLE 命令恢复已删除的 `"test"` 表，从而可以再次对其执行 SELECT 查询。

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