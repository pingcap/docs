---
title: REGEXP
summary: Returns true if the string <expr> matches the regular expression specified by the <pattern>, false otherwise.
---
Returns `true` if the string `<expr>` matches the regular expression specified by the `<pattern>`, `false` otherwise.

## Syntax

```sql
<expr> REGEXP <pattern>
```

## Aliases

- [RLIKE](/tidb-cloud-lake/sql/rlike.md)

## Examples

```sql
SELECT 'databend' REGEXP 'd*', 'databend' RLIKE 'd*';

┌────────────────────────────────────────────────────┐
│ ('databend' regexp 'd*') │ ('databend' rlike 'd*') │
├──────────────────────────┼─────────────────────────┤
│ true                     │ true                    │
└────────────────────────────────────────────────────┘
```