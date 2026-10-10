---
title: SOUNDEX
summary: 文字列の Soundex コードを生成します。
---

# SOUNDEX

文字列の Soundex コードを生成します。

- Soundex コードは、1 文字の英字に続く 3 桁の数字で構成されます。{{{ .lake }}} の実装では 4 桁を超える数字が返されますが、標準的な Soundex コードを取得するには結果に [SUBSTR](/tidb-cloud-lake/sql/substr.md) を適用できます。
- 文字列内の英字以外の文字はすべて無視されます。
- A-Z の範囲外にある国際的なアルファベット文字は、先頭文字でない限りすべて無視されます。

> **Tip:**
>
> Soundex は、英語で発音したときの音に基づいて英数字の文字列を 4 文字のコードに変換します。詳細は <https://en.wikipedia.org/wiki/Soundex> を参照してください。

関連項目: [SOUNDS LIKE](/tidb-cloud-lake/sql/sounds-like.md)

## 構文 {#syntax}

```sql
SOUNDEX(<str>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| str  | 文字列。 |

## 戻り値の型 {#return-type}

VARCHAR 型のコード、または NULL 値を返します。

## 例 {#examples}

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