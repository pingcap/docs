---
title: SHOW PROFILES
summary: An overview of the usage of SHOW PROFILES for the TiDB database.
---

# SHOW PROFILES

The `SHOW PROFILES` statement currently only returns an empty result.

## Synopsis

```ebnf+diagram
ShowProfilesStmt ::=
    "SHOW" "PROFILES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## Examples

```sql
SHOW PROFILES;
```

```
Empty set (0.00 sec)
```

## MySQL compatibility

This statement is included only for compatibility with MySQL. Executing `SHOW PROFILES` always returns an empty result.

As an alternative, TiDB provides [statement summary tables](/statement-summary-tables.md) to help understand SQL performance issues.
