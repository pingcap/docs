---
title: SUBSTR
---

Extracts a string containing a specific number of characters from a particular position of a given string.

- The forms without a `len` argument return a substring from string `str` starting at position `pos`.
- The forms with a `len` argument return a substring `len` characters long from string `str`, starting at position `pos`.

It is also possible to use a negative value for `pos`. In this case, the beginning of the substring is pos characters from the end of the string, rather than the beginning. A negative value may be used for `pos` in any of the forms of this function. A value of 0 for `pos` returns an empty string. The position of the first character in the string from which the substring is to be extracted is reckoned as 1.

## Syntax

```sql
SUBSTR(<str>, <pos>)

SUBSTR(<str>, <pos>, <len>)
```

## Arguments

| Arguments | Description                                                                                |
|-----------|--------------------------------------------------------------------------------------------|
| `<str>`   | The main string from where the character to be extracted                                   |
| `<pos>`   | The position (starting from 1) the substring to start at. If negative, counts from the end |
| `<len>`   | The maximum length of the substring to extract                                             |

## Aliases

- [SUBSTRING](substring.md)
- [MID](mid.md)

## Return Type

VARCHAR

## Examples

```sql
SELECT
  SUBSTRING('Quadratically', 5),
  SUBSTR('Quadratically', 5),
  MID('Quadratically', 5);

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ substring('quadratically' from 5) │ substring('quadratically' from 5) │ mid('quadratically', 5) │
├───────────────────────────────────┼───────────────────────────────────┼─────────────────────────┤
│ ratically                         │ ratically                         │ ratically               │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT
  SUBSTRING('Quadratically', 5, 6),
  SUBSTR('Quadratically', 5, 6),
  MID('Quadratically', 5, 6);

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ substring('quadratically' from 5 for 6) │ substring('quadratically' from 5 for 6) │ mid('quadratically', 5, 6) │
├─────────────────────────────────────────┼─────────────────────────────────────────┼────────────────────────────┤
│ ratica                                  │ ratica                                  │ ratica                     │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```