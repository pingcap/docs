---
title: UNDROP DATABASE
summary: 恢复已删除数据库的最新版本。此功能利用 {{{ .lake }}} Time Travel 特性；已删除对象只能在保留时间内恢复（默认为 24 小时）。
---

# UNDROP DATABASE

恢复已删除数据库的最新版本。此功能利用 {{{ .lake }}} Time Travel 特性；已删除对象只能在保留时间内恢复（默认为 24 小时）。

**另请参阅：**

- [DROP DATABASE](/tidb-cloud-lake/sql/drop-database.md)
- [SHOW DROP DATABASES](/tidb-cloud-lake/sql/show-drop-databases.md)

## 语法 {#syntax}

```sql
UNDROP DATABASE <database_name>
```

- 如果已存在同名数据库，则会返回错误。

    ```sql title='Examples:'
    root@localhost:8000/default> CREATE DATABASE doc;
    processed in (0.030 sec)

    root@localhost:8000/default> DROP DATABASE doc;
    processed in (0.028 sec)

    root@localhost:8000/default> CREATE DATABASE doc;
    processed in (0.028 sec)

    root@localhost:8000/default> UNDROP DATABASE doc;
    error: APIError: QueryFailed: [2301]Database 'doc' already exists
    ```

- 执行 undrop 数据库操作不会自动将所有权恢复给原始角色。undrop 之后，必须手动将所有权授予之前的角色或其他角色。在此之前，只有 `account-admin` 角色可以访问该数据库。

    ```sql title='Examples:'
    GRANT OWNERSHIP on doc.* to ROLE writer;
    ```

## 示例 {#examples}

以下示例创建、删除，然后恢复一个名为 "orders_2024" 的数据库：

```sql
root@localhost:8000/default> CREATE DATABASE orders_2024;

CREATE DATABASE orders_2024

0 row written in 0.014 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)

root@localhost:8000/default> DROP DATABASE orders_2024;

DROP DATABASE orders_2024

0 row written in 0.012 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)

root@localhost:8000/default> UNDROP DATABASE orders_2024;

UNDROP DATABASE orders_2024

0 row read in 0.011 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)
```