---
title: TO_DECIMAL
---

Converts a value to DECIMAL data type.

## Syntax

```sql
TO_DECIMAL
( <expr> [, '<format>' ] [, <precision> [, <scale> ] ] )
```

## Arguments

| Arguments | Description                                                                                                                                                                             |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| expr      | An expression of a boolean, number, string, or variant type.                                                                                                                            |
| format    | Optional. A format string specifying the desired precision and scale for the decimal result. It may define the total number of digits and the number of digits after the decimal point. |
| precision | Optional. Total number of significant digits in the result, the default is 38.                                                                                                          |
| scale     | Optional. Number of digits after the decimal point. Must not exceed precision, the default is 0.                                                                                        |

### Format Specifiers

| Format Specifier   | Description                                                                     | Example Input |
|--------------------|---------------------------------------------------------------------------------|---------------|
| '9'                | Optional digit (accepts digit or nothing, but this implementation requires one) | "123"         |
| '0'                | Required digit (same as 9 in current implementation)                            | "123"         |
| 'D'                | Decimal point (accepts '.' or ',', always normalized to '.')                    | "12.34"       |
| 'G'                | Group (thousands) separator (expects ',' in input)                              | "1,234"       |
| 'S'                | Sign ('+' or '-', applied as prefix to result)                                  | "-123"        |
| Literal character	 | Any literal character must appear in the input exactly                          | "NT$123"      |

## Examples

```sql
SELECT TO_DECIMAL('1234.56');

╭───────────────────────╮
│ to_decimal('1234.56') │
├───────────────────────┤
│                  1235 │
╰───────────────────────╯

SELECT TO_DECIMAL('1234.56', '9999D99');

╭──────────────────────────────────╮
│ to_decimal('1234.56', '9999D99') │
├──────────────────────────────────┤
│                             1235 │
╰──────────────────────────────────╯

SELECT TO_DECIMAL('1234.56', 38, 1);

╭──────────────────────────────╮
│ to_decimal('1234.56', 38, 1) │
├──────────────────────────────┤
│                       1234.6 │
╰──────────────────────────────╯

SELECT TO_DECIMAL('NT$1234.56', 'NT$9999D99', 38, 1);

╭───────────────────────────────────────────────╮
│ to_decimal('NT$1234.56', 'NT$9999D99', 38, 1) │
├───────────────────────────────────────────────┤
│                                        1234.6 │
╰───────────────────────────────────────────────╯

```