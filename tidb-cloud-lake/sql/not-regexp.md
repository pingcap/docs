---
title: NOT REGEXP
summary: 文字列 expr が pattern pat で指定された正規表現に一致しない場合は 1 を返し、それ以外の場合は 0 を返します。
---

# NOT REGEXP

文字列 expr が pattern pat で指定された正規表現に一致しない場合は 1 を返し、それ以外の場合は 0 を返します。

## 構文 {#syntax}

```sql
<expr> NOT REGEXP <pattern>
```

## 例 {#examples}

```sql
SELECT 'datalake' NOT REGEXP 'd*';
+------------------------------+
| ('datalake' not regexp 'd*') |
+------------------------------+
|                            0 |
+------------------------------+
```