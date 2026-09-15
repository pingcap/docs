---
title: NOT RLIKE
summary: 如果字符串 expr 与 pattern pat 指定的正则表达式不匹配，则返回 1；否则返回 0。
---

# NOT RLIKE

如果字符串 expr 与 pattern pat 指定的正则表达式不匹配，则返回 1；否则返回 0。

## 语法 {#syntax}

```sql
<expr> NOT RLIKE <pattern>
```

## 示例 {#examples}

```sql
SELECT 'datalake' not rlike 'd*';
+-----------------------------+
| ('datalake' not rlike 'd*') |
+-----------------------------+
|                           0 |
+-----------------------------+
```