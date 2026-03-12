---
title: SHOW DROP TABLES
sidebar_position: 11
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.203"/>

Lists the dropped tables in the current or a specified database.

See also: [system.tables_with_history](../../../00-sql-reference/31-system-tables/system-tables-with-history.md)

## Syntax

```sql
SHOW DROP TABLES [ FROM <database_name> ] [ LIKE '<pattern>' | WHERE <expr> ]
```

## Examples

```sql
USE database1;

-- List dropped tables in the current database
SHOW DROP TABLES;

-- List dropped tables in the "default" database
SHOW DROP TABLES FROM default;

Name                |Value                        |
--------------------+-----------------------------+
tables              |t1                           |
table_type          |BASE TABLE                   |
database            |default                      |
catalog             |default                      |
engine              |FUSE                         |
create_time         |2023-06-13 08:43:36.556 +0000|
drop_time           |2023-07-19 04:39:18.536 +0000|
num_rows            |2                            |
data_size           |34                           |
data_compressed_size|330                          |
index_size          |464                          |
```