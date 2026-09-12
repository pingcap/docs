---
title: REPLACE
summary: 返回字符串 str，其中字符串 from_str 的所有出现位置都被替换为字符串 to_str。
---

# REPLACE

返回字符串 str，其中字符串 from_str 的所有出现位置都被替换为字符串 to_str。

## 语法 {#syntax}

```sql
REPLACE(<str>, <from_str>, <to_str>)
```

## 参数 {#arguments}

| 参数         | 描述             |
|--------------|------------------|
| `<str>`      | 该字符串。       |
| `<from_str>` | 源字符串。       |
| `<to_str>`   | 目标字符串。     |

## 返回类型 {#return-type}

`VARCHAR`

## 示例 {#examples}

```sql
SELECT REPLACE('www.mysql.com', 'w', 'Ww');
+-------------------------------------+
| REPLACE('www.mysql.com', 'w', 'Ww') |
+-------------------------------------+
| WwWwWw.mysql.com                    |
+-------------------------------------+
```