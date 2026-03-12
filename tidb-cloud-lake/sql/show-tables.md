---
title: SHOW TABLES
sidebar_position: 15
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.415"/>

Lists the tables in the current or a specified database.

:::note
Starting from version 1.2.415, the SHOW TABLES command no longer includes views in its results. To display views, use [SHOW VIEWS](../05-view/show-views.md) instead.
:::

See also: [system.tables](../../../00-sql-reference/31-system-tables/system-tables.md)

## Syntax

```sql
SHOW [ FULL ] TABLES 
     [ {FROM | IN} <database_name> ] 
     [ HISTORY ] 
     [ LIKE '<pattern>' | WHERE <expr> ]
```

| Parameter | Description                                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FULL      | Lists the results with additional information. See [Examples](#examples) for more details.                                  |
| FROM / IN | Specifies a database. If omitted, the command returns the results from the current database.                                |
| HISTORY   | Displays the timestamps of table deletions within the retention period (24 hours by default). If a table has not been deleted yet, the value for `drop_time` is NULL. |
| LIKE      | Filters the results by their names using case-sensitive pattern matching.                                                   |
| WHERE     | Filters the results using an expression in the WHERE clause.                                                                |

## Examples

The following example lists the names of all tables in the current database (default):

```sql
SHOW TABLES;

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ books             │
│ mytable           │
│ ontime            │
│ products          │
└───────────────────┘
```

The following example lists all the tables with additional information:

```sql
SHOW FULL TABLES;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  tables  │ table_type │ database │ catalog │       owner      │ engine │ cluster_by │         create_time        │     num_rows     │     data_size    │ data_compressed_size │    index_size    │
├──────────┼────────────┼──────────┼─────────┼──────────────────┼────────┼────────────┼────────────────────────────┼──────────────────┼──────────────────┼──────────────────────┼──────────────────┤
│ books    │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:53:15.354132 │                0 │                0 │                    0 │                0 │
│ mytable  │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:53:27.968505 │                0 │                0 │                    0 │                0 │
│ ontime   │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:53:42.052399 │                0 │                0 │                    0 │                0 │
│ products │ BASE TABLE │ default  │ default │ account_admin    │ FUSE   │            │ 2024-01-16 03:54:00.883985 │                0 │                0 │                    0 │                0 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The following example demonstrates that the results will include dropped tables when the optional parameter HISTORY is present:

```sql
DROP TABLE products;

SHOW TABLES;

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ books             │
│ mytable           │
│ ontime            │
└───────────────────┘

SHOW TABLES HISTORY;

┌────────────────────────────────────────────────┐
│ Tables_in_default │          drop_time         │
├───────────────────┼────────────────────────────┤
│ books             │ NULL                       │
│ mytable           │ NULL                       │
│ ontime            │ NULL                       │
│ products          │ 2024-01-16 03:55:47.900362 │
└────────────────────────────────────────────────┘
```

The following example lists the tables containing the string "time" at the end of their name:

```sql
SHOW TABLES LIKE '%time';

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ ontime            │
└───────────────────┘

-- CASE-SENSITIVE pattern matching. 
-- No results will be returned if you code the previous statement like this: 
SHOW TABLES LIKE '%TIME';
```

The following example lists tables where the data size is greater than 1,000 bytes:

```sql
SHOW TABLES WHERE data_size > 1000 ;

┌───────────────────┐
│ Tables_in_default │
├───────────────────┤
│ ontime            │
└───────────────────┘
```