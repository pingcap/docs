---
title: NOT RLIKE
summary: 文字列 expr が pattern pat で指定された正規表現に一致しない場合は 1 を返し、それ以外の場合は 0 を返します。
---

# NOT RLIKE

文字列 expr が pattern pat で指定された正規表現に一致しない場合は 1 を返し、それ以外の場合は 0 を返します。

## 構文 {#syntax}

```sql
<expr> NOT RLIKE <pattern>
```

## 例 {#examples}

```sql
SELECT 'datalake' not rlike 'd*';
+-----------------------------+
| ('datalake' not rlike 'd*') |
+-----------------------------+
|                           0 |
+-----------------------------+
```