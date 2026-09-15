---
title: BETWEEN
summary: 如果给定的数值或字符串 `<expr>` 落在定义的下限和上限之间，则返回 true。
---

# BETWEEN

如果给定的数值或字符串 `<expr>` 落在定义的下限和上限之间，则返回 `true`。

## 语法 {#syntax}

```sql
<expr> [ NOT ] BETWEEN <lower_limit> AND <upper_limit>
```

## 示例 {#examples}

```sql
SELECT 'true' WHERE 5 BETWEEN 0 AND 5;

┌────────┐
│ 'true' │
├────────┤
│ true   │
└────────┘

SELECT 'true' WHERE 'data' BETWEEN 'data' AND 'datalakecloud';

┌────────┐
│ 'true' │
├────────┤
│ true   │
└────────┘
```