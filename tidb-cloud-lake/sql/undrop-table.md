---
title: UNDROP TABLE
summary: 恢复最近版本的已删除表。此功能利用 {{{ .lake }}} Time Travel 特性；已删除对象只能在保留时间内恢复（默认为 24 小时）。
---

# UNDROP TABLE

恢复最近版本的已删除表。此功能利用 {{{ .lake }}} Time Travel 特性；已删除对象只能在保留时间内恢复（默认为 24 小时）。

**另请参阅：**

- [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)
- [DROP TABLE](/tidb-cloud-lake/sql/drop-table.md)
- [SHOW TABLES](/tidb-cloud-lake/sql/show-tables.md)
- [SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md)

## 语法 {#syntax}

```sql
UNDROP TABLE [ <database_name>. ]<table_name>
```

- 如果已存在同名表，则会返回错误。

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

- 恢复已删除表不会自动将所有权恢复给原始角色。执行恢复后，必须手动将所有权授予之前的角色或其他角色。在此之前，只有 `account-admin` 角色可以访问该表。

    ```sql title='Examples:'
    GRNAT OWNERSHIP on doc.t to ROLE writer;
    ```

## 示例 {#examples}

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