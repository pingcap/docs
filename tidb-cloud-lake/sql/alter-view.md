---
title: ALTER VIEW
summary: Alter the existing view by using another QUERY.
---

# ALTER VIEW

Alter the existing view by using another `QUERY`.

## Syntax

```sql
ALTER VIEW [ <database_name>. ]view_name [ (<column>, ...) ] AS SELECT query
```

## Examples

```sql
CREATE VIEW tmp_view AS SELECT number % 3 AS a, avg(number) FROM numbers(1000) GROUP BY a ORDER BY a;

SELECT * FROM tmp_view;
+------+-------------+
| a    | avg(number) |
+------+-------------+
|    0 |       499.5 |
|    1 |       499.0 |
|    2 |       500.0 |
+------+-------------+

ALTER VIEW tmp_view(c1) AS SELECT * from numbers(3);

SELECT * FROM tmp_view;
+------+
| c1   |
+------+
|    0 |
|    1 |
|    2 |
+------+
```

## Tag Operations {#tag-operations}

Assigns or removes tags on a view. Tags must be created with [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) first. For full details, see [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md).

### Syntax

```sql
ALTER VIEW [ IF EXISTS ] [ <database_name>. ]<view_name>
    SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

ALTER VIEW [ IF EXISTS ] [ <database_name>. ]<view_name>
    UNSET TAG <tag_name> [, <tag_name> ...]
```

### Examples

```sql
ALTER VIEW default.active_users SET TAG env = 'prod', owner = 'analytics';
ALTER VIEW default.active_users UNSET TAG env, owner;
```
