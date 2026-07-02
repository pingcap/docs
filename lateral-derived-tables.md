---
title: LATERAL Derived Tables
summary: Learn the syntax and current limitations of LATERAL derived tables in TiDB.
---

# LATERAL Derived Tables

A **lateral derived table** is a subquery in the `FROM` clause that can reference columns from tables that appear earlier in the same `FROM` clause. Compared with a standard derived table, whose subquery cannot reference columns from other tables in the same `FROM` clause, a lateral derived table is more flexible.

Starting from v8.5.7 and v9.0.0, TiDB supports parsing the `LATERAL` syntax for derived tables, following the MySQL 8.0 syntax ([WL#8652](https://dev.mysql.com/worklog/task/?id=8652)).

> **Note:**
>
> Currently, TiDB only supports parsing the `LATERAL` derived table syntax, but does not support executing queries that use this syntax. If you attempt to execute such a query, TiDB returns an error. You can track the progress of full execution support for this feature in issue [#40328](https://github.com/pingcap/tidb/issues/40328).

## Syntax

```sql
SELECT ... FROM table_ref, LATERAL (subquery) [AS] alias [(col_list)] ...
SELECT ... FROM table_ref [INNER | CROSS | LEFT [OUTER] | RIGHT [OUTER]] JOIN LATERAL (subquery) [AS] alias [(col_list)] ON ...
```

- The `LATERAL` keyword must precede the derived table subquery.
- A table alias must be specified after the closing parenthesis of the subquery.
- The `AS` keyword before the alias is optional.
- An optional derived column list can follow the alias, for example, `LATERAL (...) AS dt(col1, col2)`.

## Examples

### Use a comma join with a `LATERAL` derived table

```sql
SELECT * FROM t1, LATERAL (SELECT * FROM t2 WHERE t2.id = t1.id) AS dt;
```

In this example, `t1` and the `LATERAL` derived table are joined by a comma in the same `FROM` clause. The subquery in the `LATERAL` derived table references `t1.id`, a column from the preceding table `t1`. A regular derived table without `LATERAL` does not support this capability.

### Use a `LATERAL` derived table (with a derived column list) in `LEFT JOIN`

```sql
SELECT t1.id, dt.val
FROM t1
LEFT JOIN LATERAL (SELECT t2.val FROM t2 WHERE t2.id = t1.id LIMIT 1) AS dt(val)
ON TRUE;
```

In this example, the `LATERAL` derived table is used as the right table of the `LEFT JOIN` and can reference the column `t1.id` from the left table `t1`. The derived column list `(val)` renames the column returned by the subquery to `val`.

## Comparison with standard derived tables

| Feature | Standard derived table | LATERAL derived table |
|---|---|---|
| Can reference columns from preceding tables in the same `FROM` clause | No | Yes |
| Alias required | Yes | Yes |
| Derived column list | Supported | Supported |

## MySQL compatibility

TiDB's LATERAL derived table syntax is compatible with MySQL 8.0 at the syntax level.

## See also

- [Subquery Related Optimizations](/subquery-optimization.md)
- [Decorrelation of Correlated Subquery](/correlated-subquery-optimization.md)
- [Explain Statements That Use Subqueries](/explain-subqueries.md)
- [MySQL Compatibility](/mysql-compatibility.md)
