---
title: RIGHT
summary: 返回字符串 str 最右侧的 len 个字符；如果任一参数为 NULL，则返回 NULL。
---

# RIGHT

返回字符串 str 最右侧的 len 个字符；如果任一参数为 NULL，则返回 NULL。

## 语法 {#syntax}

```sql
RIGHT(<str>, <len>);
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------------------------------------------------|
| `<str>`   | 要从中提取字符的主字符串 |
| `<len>`   | 字符个数 |

## 返回类型 {#return-type}

`VARCHAR`

## 示例 {#examples}

```sql
SELECT RIGHT('foobarbar', 4);
+-----------------------+
| RIGHT('foobarbar', 4) |
+-----------------------+
| rbar                  |
+-----------------------+
```