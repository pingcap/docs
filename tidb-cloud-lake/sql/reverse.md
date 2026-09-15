---
title: REVERSE
summary: 返回字符串 str，其字符顺序与原字符串相反。
---

# REVERSE

返回字符串 str，其字符顺序与原字符串相反。

## 语法 {#syntax}

```sql
REVERSE(<str>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------------|
| `<str>`   | 字符串值。 |

## 返回类型 {#return-type}

`VARCHAR`

## 示例 {#examples}

```sql
SELECT REVERSE('abc');
+----------------+
| REVERSE('abc') |
+----------------+
| cba            |
+----------------+
```