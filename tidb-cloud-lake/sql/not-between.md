---
title: "[ NOT ] BETWEEN"
---

Returns `true` if the given numeric or string ` <expr>` falls inside the defined lower and upper limits.

## Syntax

```sql
<expr> [ NOT ] BETWEEN <lower_limit> AND <upper_limit>
```

## Examples

```sql
SELECT 'true' WHERE 5 BETWEEN 0 AND 5;

┌────────┐
│ 'true' │
├────────┤
│ true   │
└────────┘

SELECT 'true' WHERE 'data' BETWEEN 'data' AND 'databendcloud';

┌────────┐
│ 'true' │
├────────┤
│ true   │
└────────┘
```