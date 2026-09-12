---
title: ASCII
summary: 返回字符串 str 最左侧字符的数值。
---

# ASCII

返回字符串 str 最左侧字符的数值。

## 语法 {#syntax}

```sql
ASCII(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<expr>`  | 该字符串。 |

## 返回类型 {#return-type}

`TINYINT`

## 示例 {#examples}

```sql
SELECT ASCII('2');
+------------+
| ASCII('2') |
+------------+
|         50 |
+------------+
```