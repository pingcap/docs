---
title: NOT REGEXP
summary: 如果字符串 expr 与模式 pat 指定的正则表达式不匹配，则返回 1；否则返回 0。
---

# NOT REGEXP

如果字符串 expr 与模式 pat 指定的正则表达式不匹配，则返回 1；否则返回 0。

## 语法 {#syntax}

```sql
<expr> NOT REGEXP <pattern>
```

## 示例 {#examples}

```sql
SELECT 'datalake' NOT REGEXP 'd*';
+------------------------------+
| ('datalake' not regexp 'd*') |
+------------------------------+
|                            0 |
+------------------------------+
```