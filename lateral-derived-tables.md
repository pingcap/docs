---
title: LATERAL Derived Tables
summary: Learn how to use LATERAL derived tables in TiDB.
---

# LATERAL Derived Tables

A **lateral derived table** is a subquery in the `FROM` clause that can reference columns from tables that appear earlier in the same `FROM` clause. This makes it more powerful than a standard derived table, whose subquery cannot reference outer columns in the same `FROM` clause.

TiDB recognizes the `LATERAL` syntax for derived tables, following MySQL 8.0 compatibility ([WL#8652](https://dev.mysql.com/worklog/task/?id=8652)).

> **Note:**
>
> Currently, TiDB supports parsing LATERAL derived table syntax, but execution is not yet supported and will return an error. Full execution support is tracked in [#40328](https://github.com/pingcap/tidb/issues/40328).

## Syntax

```sql
SELECT ... FROM table_ref, LATERAL (subquery) [AS] alias [(col_list)] ...
SELECT ... FROM table_ref [LEFT] JOIN LATERAL (subquery) [AS] alias [(col_list)] ON ...
```

- The `LATERAL` keyword must precede the derived table subquery.
- A table alias is required after the closing parenthesis of the subquery.
- The `AS` keyword before the alias is optional.
- An optional derived column list can follow the alias: `LATERAL (...) AS dt(col1, col2)`.

## Examples

### Comma join

```sql
SELECT * FROM t1, LATERAL (SELECT * FROM t2 WHERE t2.id = t1.id) AS dt;
```

In this example, the subquery references `t1.id`, a column from the preceding table `t1`. A regular derived table (without `LATERAL`) cannot do this.

### LEFT JOIN with a derived column list

```sql
SELECT t1.id, dt.val
FROM t1
LEFT JOIN LATERAL (SELECT t2.val FROM t2 WHERE t2.id = t1.id LIMIT 1) AS dt(val)
ON TRUE;
```

The derived column list `(val)` renames the columns that the subquery returns.

## Comparison with standard derived tables

| Feature | Standard derived table | LATERAL derived table |
|---|---|---|
| Can reference outer `FROM` columns | No | Yes |
| Alias required | Yes | Yes |
| Derived column list | Supported | Supported |

## MySQL compatibility

TiDB's LATERAL derived table syntax is compatible with MySQL 8.0. Once full execution support is available, queries that use `LATERAL` in MySQL should also work in TiDB.

## See also

- [Subquery Related Optimizations](/subquery-optimization.md)
- [Decorrelation of Correlated Subquery](/correlated-subquery-optimization.md)
- [Explain Statements That Use Subqueries](/explain-subqueries.md)
- [MySQL Compatibility](/mysql-compatibility.md)
