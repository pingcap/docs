---
title: SOUNDS LIKE
summary: 通过两个字符串的 Soundex 代码比较它们的发音。Soundex 是一种语音算法，会生成一个表示字符串发音的代码，从而可以根据发音而非拼写对字符串进行近似匹配。{{{ .lake }}} 提供了 [SOUNDEX](/tidb-cloud-lake/sql/soundex.md) 函数，用于从字符串中获取 Soundex 代码。
---

# SOUNDS LIKE

通过两个字符串的 Soundex 代码比较它们的发音。Soundex 是一种语音算法，会生成一个表示字符串发音的代码，从而可以根据发音而非拼写对字符串进行近似匹配。{{{ .lake }}} 提供了 [SOUNDEX](/tidb-cloud-lake/sql/soundex.md) 函数，用于从字符串中获取 Soundex 代码。

SOUNDS LIKE 常用于 SQL 查询的 WHERE 子句中，通过模糊字符串匹配来缩小结果行范围，例如用于姓名和地址。参见 [示例](#examples) 中的 [过滤行](#filtering-rows)。

> **Note:**
>
> 虽然该函数可用于近似字符串匹配，但需要注意的是，它并不总是准确。Soundex 算法基于英语发音规则，对于其他语言或方言的字符串可能效果不佳。

## 语法 {#syntax}

```sql
<str1> SOUNDS LIKE <str2>
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| str1, 2   | 要比较的字符串。 |

## 返回类型 {#return-type}

如果两个字符串的 Soundex 代码相同（即它们听起来相似），则返回 Boolean 值 1；否则返回 0。

## 示例 {#examples}

### 比较字符串 {#comparing-strings}

```sql
SELECT 'two' SOUNDS LIKE 'too'
----
1

SELECT CONCAT('A', 'B') SOUNDS LIKE 'AB';
----
1

SELECT 'Monday' SOUNDS LIKE 'Sunday';
----
0
```

### 过滤行 {#filtering-rows}

```sql
SELECT * FROM  employees;

id|first_name|last_name|age|
--+----------+---------+---+
 0|John      |Smith    | 35|
 0|Mark      |Smythe   | 28|
 0|Johann    |Schmidt  | 51|
 0|Eric      |Doe      | 30|
 0|Sue       |Johnson  | 45|

SELECT * FROM  employees
WHERE  first_name SOUNDS LIKE 'John';

id|first_name|last_name|age|
--+----------+---------+---+
 0|John      |Smith    | 35|
 0|Johann    |Schmidt  | 51|
```