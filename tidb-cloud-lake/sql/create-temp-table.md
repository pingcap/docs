---
title: CREATE TEMP TABLE
summary: Creates a temporary table that is automatically dropped at the end of the session.
---

# CREATE TEMP TABLE

> **Note:**
>
> Introduced or updated in v1.2.666.

Creates a temporary table that is automatically dropped at the end of the session.

- A temporary table is visible only within the session that created it and is automatically dropped, with all data vacuumed, when the session ends.
       - In cases where automatic cleanup of temporary tables fails—for example, due to a query node crash—you can use the [FUSE_VACUUM_TEMPORARY_TABLE](/tidb-cloud-lake/sql/fuse-vacuum-temporary-table.md) function to manually clean up leftover files from temporary tables.
- To show the existing temporary tables in the session, query the [system.temporary_tables](/tidb-cloud-lake/sql/system-tables.md) system table. See [Example-1](#example-1).
- A temporary table with the same name as a normal table takes precedence, hiding the normal table until dropped. See [Example-2](#example-2).
- No privileges are required to create or operate on a temporary table.
- Databend supports creating temporary tables with the [Fuse Engine](/tidb-cloud-lake/sql/table-engines.md).
- To create temporary tables using BendSQL, ensure you are using the latest version of BendSQL.

## Syntax

```sql
CREATE [ OR REPLACE ] { TEMPORARY | TEMP } TABLE
       [ IF NOT EXISTS ]
       [ <database_name>. ]<table_name>
       ...
```

The omitted parts follow the syntax of [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md).

## Examples

### Example-1

This example demonstrates how to create a temporary table and verify its existence by querying the [system.temporary_tables](/tidb-cloud-lake/sql/system-tables.md) system table:

```sql
CREATE TEMP TABLE my_table (id INT, description STRING);

SELECT * FROM system.temporary_tables;

┌────────────────────────────────────────────────────┐
│ database │   name   │       table_id      │ engine │
├──────────┼──────────┼─────────────────────┼────────┤
│ default  │ my_table │ 4611686018427407904 │ FUSE   │
└────────────────────────────────────────────────────┘
```

### Example-2

This example demonstrates how a temporary table with the same name as a normal table takes precedence. When both tables exist, operations target the temporary table, effectively hiding the normal table. Once the temporary table is dropped, the normal table becomes accessible again:

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
