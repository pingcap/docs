---
title: SHOW FUNCTIONS
summary: Lists the currently supported built-in scalar and aggregate functions.
---

> **Note:**
>
> Introduced or updated in v1.2.315.

Lists the currently supported built-in scalar and aggregate functions.

See also: [system.functions](/tidb-cloud-lake/sql/system-functions.md)

## Syntax

```sql
SHOW FUNCTIONS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## Example

```sql
SHOW FUNCTIONS;

+-------------------------+--------------+---------------------------+
| name                    | is_aggregate | description               |
+-------------------------+--------------+---------------------------+
| !=                      |            0 |                           |
| %                       |            0 |                           |
| *                       |            0 |                           |
| +                       |            0 |                           |
| -                       |            0 |                           |
| /                       |            0 |                           |
| <                       |            0 |                           |
| <=                      |            0 |                           |
| <>                      |            0 |                           |
| =                       |            0 |                           |
+-------------------------+--------------+---------------------------+
```

Showing the functions begin with `"today"`:

```sql
SHOW FUNCTIONS LIKE 'today%';

+--------------+--------------+-------------+
| name         | is_aggregate | description |
+--------------+--------------+-------------+
| today        |            0 |             |
| todayofmonth |            0 |             |
| todayofweek  |            0 |             |
| todayofyear  |            0 |             |
+--------------+--------------+-------------+
```

Showing the functions begin with `"today"` with `WHERE`:

```sql
SHOW FUNCTIONS WHERE name LIKE 'today%';

+--------------+--------------+-------------+
| name         | is_aggregate | description |
+--------------+--------------+-------------+
| today        |            0 |             |
| todayofmonth |            0 |             |
| todayofweek  |            0 |             |
| todayofyear  |            0 |             |
+--------------+--------------+-------------+
```
