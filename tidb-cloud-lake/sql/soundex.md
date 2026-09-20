---
title: SOUNDEX
summary: Generates the Soundex code for a string.
---

# SOUNDEX

Generates the Soundex code for a string.

- A Soundex code consists of a letter followed by three numerical digits. {{{ .lake }}}'s implementation returns more than 4 digits, but you can [SUBSTR](/tidb-cloud-lake/sql/substr.md) the result to get a standard Soundex code.
- All non-alphabetic characters in the string are ignored.
- All international alphabetic characters outside the A-Z range are ignored unless they're the first letter.

> **Tip:**
>
> Soundex converts an alphanumeric string to a four-character code that is based on how the string sounds when spoken in English. For more information, see <https://en.wikipedia.org/wiki/Soundex>

See also: [SOUNDS LIKE](/tidb-cloud-lake/sql/sounds-like.md)

## Syntax

```sql
SOUNDEX(<str>)
```

## Arguments

| Arguments | Description |
|-----------|-------------|
| str  | The string. |

## Return Type

Returns a code of type VARCHAR or a NULL value.

## Examples

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
