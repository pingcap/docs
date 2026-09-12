---
title: HUMANIZE_NUMBER
summary: 返回一个易读的数字。
---

# HUMANIZE_NUMBER

返回一个易读的数字。

## 语法 {#syntax}

```sql
HUMANIZE_NUMBER(x);
```

## 参数 {#arguments}

| 参数 | 描述       |
|-----------|----------------------------|
| x         | 数值大小。        |

## 返回类型 {#return-type}

字符串。

## 示例 {#examples}

```sql
SELECT HUMANIZE_NUMBER(1000 * 1000)
+-------------------------+
| HUMANIZE_NUMBER((1000 * 1000)) |
+-------------------------+
| 1 million               |
+-------------------------+
```