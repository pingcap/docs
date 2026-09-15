---
title: INSTR
summary: 返回子字符串 substr 在字符串 str 中首次出现的位置。这与 LOCATE() 的双参数形式相同，只是参数顺序相反。
---

# INSTR

返回子字符串 substr 在字符串 str 中首次出现的位置。这与 LOCATE() 的双参数形式相同，只是参数顺序相反。

## 语法 {#syntax}

```sql
INSTR(<str>, <substr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|------------|----------------|
| `<str>`    | 字符串。    |
| `<substr>` | 子字符串。 |

## 返回类型 {#return-type}

`BIGINT`

## 示例 {#examples}

```sql
SELECT INSTR('foobarbar', 'bar');
+---------------------------+
| INSTR('foobarbar', 'bar') |
+---------------------------+
|                         4 |
+---------------------------+

SELECT INSTR('xbar', 'foobar');
+-------------------------+
| INSTR('xbar', 'foobar') |
+-------------------------+
|                       0 |
+-------------------------+
```