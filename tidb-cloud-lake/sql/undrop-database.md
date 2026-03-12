---
title: UNDROP DATABASE
---

Restores the most recent version of a dropped database. This leverages the Databend Time Travel feature; a dropped object can be restored only within a retention period (defaults to 24 hours).

**See also:**
[DROP DATABASE](ddl-drop-database.md)
[SHOW DROP DATABASES](show-drop-databases.md)

## Syntax

```sql
UNDROP DATABASE <database_name>
```

- If a database with the same name already exists, an error is returned.

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
- Undropping a database does not automatically restore ownership to the original role. After undropping, ownership must be manually granted to the previous role or another role. Until then, the database will be accessible only to the `account-admin` role.

    ```sql title='Examples:'
    GRNAT OWNERSHIP on doc.* to ROLE writer;
    ```

## Examples

This example creates, drops, and then restores a database named "orders_2024":

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