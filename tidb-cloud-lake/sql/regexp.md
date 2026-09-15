---
title: REGEXP
summary: 如果字符串 `<expr>` 与 `<pattern>` 指定的正则表达式匹配，则返回 `true`，否则返回 `false`。
---

# REGEXP

如果字符串 `<expr>` 与 `<pattern>` 指定的正则表达式匹配，则返回 `true`，否则返回 `false`。

## 语法 {#syntax}

```sql
<expr> REGEXP <pattern>
```

## 别名 {#aliases}

- [RLIKE](/tidb-cloud-lake/sql/rlike.md)

## 示例 {#examples}

```sql
SELECT 'datalake' REGEXP 'd*', 'datalake' RLIKE 'd*';

┌────────────────────────────────────────────────────┐
│ ('datalake' regexp 'd*') │ ('datalake' rlike 'd*') │
├──────────────────────────┼─────────────────────────┤
│ true                     │ true                    │
└────────────────────────────────────────────────────┘
```