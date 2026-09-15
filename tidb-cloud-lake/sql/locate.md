---
title: LOCATE
summary: 第一种语法返回子字符串 substr 在字符串 str 中首次出现的位置。第二种语法返回子字符串 substr 在字符串 str 中从位置 pos 开始首次出现的位置。如果 substr 不在 str 中，则返回 0。如果任一参数为 NULL，则返回 NULL。
---

# LOCATE

第一种语法返回子字符串 substr 在字符串 str 中首次出现的位置。第二种语法返回子字符串 substr 在字符串 str 中从位置 pos 开始首次出现的位置。如果 substr 不在 str 中，则返回 0。如果任一参数为 NULL，则返回 NULL。

## 语法 {#syntax}

```sql
LOCATE(<substr>, <str>)
LOCATE(<substr>, <str>, <pos>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|------------|----------------|
| `<substr>` | 子字符串。 |
| `<str>`    | 字符串。    |
| `<pos>`    | 位置。  |

## 返回类型 {#return-type}

`BIGINT`

## 示例 {#examples}

```sql
SELECT LOCATE('bar', 'foobarbar')
+----------------------------+
| LOCATE('bar', 'foobarbar') |
+----------------------------+
|                          4 |
+----------------------------+

SELECT LOCATE('xbar', 'foobar')
+--------------------------+
| LOCATE('xbar', 'foobar') |
+--------------------------+
|                        0 |
+--------------------------+

SELECT LOCATE('bar', 'foobarbar', 5)
+-------------------------------+
| LOCATE('bar', 'foobarbar', 5) |
+-------------------------------+
|                             7 |
+-------------------------------+
```