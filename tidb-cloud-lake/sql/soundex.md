---
title: SOUNDEX
summary: 为字符串生成 Soundex 代码。
---

# SOUNDEX

为字符串生成 Soundex 代码。

- Soundex 代码由一个字母和三个数字组成。{{{ .lake }}} 的实现会返回超过 4 位的结果，但你可以对结果使用 [SUBSTR](/tidb-cloud-lake/sql/substr.md) 以获取标准的 Soundex 代码。
- 字符串中所有非字母字符都会被忽略。
- 除非是首字母，否则 A-Z 范围之外的所有国际字母字符都会被忽略。

> **Tip:**
>
> Soundex 会根据字符串用英语发音时的读音，将字母数字字符串转换为一个四字符代码。更多信息，参见 <https://en.wikipedia.org/wiki/Soundex>

另请参阅：[SOUNDS LIKE](/tidb-cloud-lake/sql/sounds-like.md)

## 语法 {#syntax}

```sql
SOUNDEX(<str>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| str  | 字符串。 |

## 返回类型 {#return-type}

返回 VARCHAR 类型的代码或 NULL 值。

## 示例 {#examples}

```sql
SELECT SOUNDEX('Datalake');

---
D42

-- All non-alphabetic characters in the string are ignored.
SELECT SOUNDEX('Datalake!');;

---
D42

-- All international alphabetic characters outside the A-Z range are ignored unless they're the first letter.
SELECT SOUNDEX('Datalake，你好');

---
D42

SELECT SOUNDEX('你好，Datalake');

---
你342

-- SUBSTR the result to get a standard Soundex code.
SELECT SOUNDEX('Datalake Cloud'),SUBSTR(SOUNDEX('Datalake Cloud'),1,4);

soundex('datalake cloud')|substring(soundex('datalake cloud') from 1 for 4)|
-------------------------+-------------------------------------------------+
D42243                   |D422                                             |

SELECT SOUNDEX(NULL);
+-------------------------------------+
| `SOUNDEX(NULL)`                     |
+-------------------------------------+
| <null>                              |
+-------------------------------------+
```