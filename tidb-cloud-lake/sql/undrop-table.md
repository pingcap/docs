---
title: UNDROP TABLE
sidebar_position: 20
---

Restores the recent version of a dropped table. This leverages the Databend Time Travel feature; a dropped object can be restored only within a retention period (defaults to 24 hours).

**See also:**
- [CREATE TABLE](./10-ddl-create-table.md)
- [DROP TABLE](./20-ddl-drop-table.md)
- [SHOW TABLES](show-tables.md)
- [SHOW DROP TABLES](show-drop-tables.md)

## Syntax

```sql
UNDROP TABLE [ <database_name>. ]<table_name>
```

- If a table with the same name already exists, an error is returned.

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

- Undropping a table does not automatically restore ownership to the original role. After undropping, ownership must be manually granted to the previous role or another role. Until then, the table will be accessible only to the `account-admin` role.

    ```sql title='Examples:'
    GRNAT OWNERSHIP on doc.t to ROLE writer;
    ```

## Examples

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