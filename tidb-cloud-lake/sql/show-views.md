---
title: SHOW VIEWS
sidebar_position: 4
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.415"/>

Returns a list of view names within the specified database, or within the current database if no database name is provided.

## Syntax

```sql
SHOW [ FULL ] VIEWS 
     [ { FROM | IN } <database_name> ] 
     [ HISTORY ] 
     [ LIKE '<pattern>' | WHERE <expr> ]
```

| Parameter | Description                                                                                  |
|-----------|----------------------------------------------------------------------------------------------|
| FULL      | Lists the results with additional information. See [Examples](#examples) for more details.   |
| FROM / IN | Specifies a database. If omitted, the command returns the results from the current database. |
| HISTORY   | Displays the timestamps of view deletions within the retention period (24 hours by default). If a view has not been deleted yet, the value for `drop_time` is NULL. |
| LIKE      | Filters the view names using case-sensitive pattern matching with the `%` wildcard.          |
| WHERE     | Filters the view names using an expression in the WHERE clause.                              |

## Examples

```sql
SHOW VIEWS;

┌───────────────────────────────────────────────────────────────────┐
│ Views_in_default │                   view_query                   │
├──────────────────┼────────────────────────────────────────────────┤
│ books_view       │ SELECT id, title, genre FROM default.books     │
│ users_view       │ SELECT username, email, age FROM default.users │
└───────────────────────────────────────────────────────────────────┘

SHOW FULL VIEWS;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│    views   │ database │ catalog │       owner      │ engine │         create_time        │                   view_query                   │
├────────────┼──────────┼─────────┼──────────────────┼────────┼────────────────────────────┼────────────────────────────────────────────────┤
│ books_view │ default  │ default │ NULL             │ VIEW   │ 2024-04-14 23:29:52.916989 │ SELECT id, title, genre FROM default.books     │
│ users_view │ default  │ default │ NULL             │ VIEW   │ 2024-04-14 23:31:02.918994 │ SELECT username, email, age FROM default.users │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Delete the view 'books_view'
DROP VIEW books_view;

SHOW VIEWS HISTORY;

┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Views_in_default │                   view_query                   │          drop_time         │
├──────────────────┼────────────────────────────────────────────────┼────────────────────────────┤
│ books_view       │ SELECT id, title, genre FROM default.books     │ 2024-04-15 02:29:56.051081 │
│ users_view       │ SELECT username, email, age FROM default.users │ NULL                       │
└────────────────────────────────────────────────────────────────────────────────────────────────┘
```