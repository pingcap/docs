---
title: DROP DATABASE
---

Drops a database.

See also: [UNDROP DATABASE](undrop-database.md)

## Syntax

```sql
DROP { DATABASE | SCHEMA } [ IF EXISTS ] <database_name>
```

`DROP SCHEMA` is a synonym for `DROP DATABASE`.

## Examples

This example creates and then drops a database named "orders_2024":

```sql
root@localhost:8000/default> CREATE DATABASE orders_2024;

CREATE DATABASE orders_2024

0 row written in 0.014 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)

root@localhost:8000/default> DROP DATABASE orders_2024;

DROP DATABASE orders_2024

0 row written in 0.012 sec. Processed 0 row, 0 B (0 row/s, 0 B/s)
```
