---
title: ADMIN | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
category: reference
---

# ADMIN

TODO

## Synopsis

TODO

## Examples

## `ADMIN RELOAD` statement

{{< copyable "sql" >}}

```sql
ADMIN RELOAD expr_pushdown_blacklist;
```

The above statement is used to reload the blacklist pushed down by the expression.

{{< copyable "sql" >}}

```sql
ADMIN RELOAD opt_rule_blacklist;
```

The above statement is used to reload the blacklist of logic optimization rules.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* ADMIN BINDINGS