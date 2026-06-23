---
title: REGEXP
summary: Returns true if the string <expr> matches the regular expression specified by the <pattern>, false otherwise.
---

# REGEXP

Returns `true` if the string `<expr>` matches the regular expression specified by the `<pattern>`, `false` otherwise.

## Syntax

```sql
<expr> REGEXP <pattern>
```

## Aliases

- [RLIKE](/tidb-cloud-lake/sql/rlike.md)

## Examples

```sql
SELECT 'datalake' REGEXP 'd*', 'datalake' RLIKE 'd*';

┌────────────────────────────────────────────────────┐
│ ('datalake' regexp 'd*') │ ('datalake' rlike 'd*') │
├──────────────────────────┼─────────────────────────┤
│ true                     │ true                    │
└────────────────────────────────────────────────────┘
```
