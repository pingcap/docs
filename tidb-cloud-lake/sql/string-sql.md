---
title: TO_STRING
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.745"/>

Converts a value to String data type, or converts a Date value to a specific string format. To customize the format of date and time in Databend, you can utilize specifiers. These specifiers allow you to define the desired format for date and time values. For a comprehensive list of supported specifiers, see [Formatting Date and Time](../../00-sql-reference/10-data-types/datetime.md#formatting-date-and-time).

## Syntax

```sql
TO_STRING( '<expr>' )

TO_STRING( '<date>', '<format>' )
```

## Date Format Styles

Databend supports two date format styles that can be selected using the `date_format_style` setting:

- **MySQL** (default): Uses MySQL-compatible format specifiers like `%Y`, `%m`, `%d`, etc.
- **Oracle**: Uses format specifiers like `YYYY`, `MM`, `DD`, etc., which follow a standardized format commonly used in many database systems.

To switch between format styles, use the `date_format_style` setting:

```sql
-- Set Oracle-style date format
SETTINGS (date_format_style = 'Oracle') SELECT to_string('2024-04-05'::DATE, 'YYYY-MM-DD');

-- Set MySQL date format style (default)
SETTINGS (date_format_style = 'MySQL') SELECT to_string('2024-04-05'::DATE, '%Y-%m-%d');
```

### Oracle-Style Format Specifiers

When `date_format_style` is set to 'Oracle', the following format specifiers are supported:

| Format Specifier | Description                                  | Example Output (for '2024-04-05 14:30:45.123456') |
|------------------|----------------------------------------------|---------------------------------------------------|
| YYYY             | 4-digit year                                 | 2024                                              |
| YY               | 2-digit year                                 | 24                                                |
| MMMM             | Full month name                              | April                                             |
| MON              | Abbreviated month name                       | Apr                                               |
| MM               | Month number (01-12)                         | 04                                                |
| DD               | Day of month (01-31)                         | 05                                                |
| DY               | Abbreviated day name                         | Fri                                               |
| HH24             | Hour of day (00-23)                          | 14                                                |
| HH12             | Hour of day (01-12)                          | 02                                                |
| AM/PM            | Meridian indicator                           | PM                                                |
| MI               | Minute (00-59)                               | 30                                                |
| SS               | Second (00-59)                               | 45                                                |
| FF               | Fractional seconds                           | 123456                                            |
| UUUU             | ISO week-numbering year                      | 2024                                              |
| TZH:TZM          | Time zone hour and minute with colon         | +08:00                                            |
| TZH              | Time zone hour                               | +08                                               |

## Aliases

- [DATE_FORMAT](../05-datetime-functions/date-format.md)
- [JSON_TO_STRING](../10-semi-structured-functions/0-json/json-to-string.md)
- [TO_TEXT](../02-conversion-functions/to-text.md)
- [TO_VARCHAR](to-varchar.md)
- TO_CHAR (Oracle compatibility)

## Return Type

String.

## Examples

```sql
SELECT
  DATE_FORMAT('1.23'),
  TO_STRING('1.23'),
  TO_TEXT('1.23'),
  TO_VARCHAR('1.23'),
  JSON_TO_STRING('1.23');

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ date_format('1.23') │ to_string('1.23') │ to_text('1.23') │ to_varchar('1.23') │ json_to_string('1.23') │
├─────────────────────┼───────────────────┼─────────────────┼────────────────────┼────────────────────────┤
│ 1.23                │ 1.23              │ 1.23            │ 1.23               │ 1.23                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT
  DATE_FORMAT('["Cooking", "Reading"]' :: JSON),
  TO_STRING('["Cooking", "Reading"]' :: JSON),
  TO_TEXT('["Cooking", "Reading"]' :: JSON),
  TO_VARCHAR('["Cooking", "Reading"]' :: JSON),
  JSON_TO_STRING('["Cooking", "Reading"]' :: JSON);

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ date_format('["cooking", "reading"]'::variant) │ to_string('["cooking", "reading"]'::variant) │ to_text('["cooking", "reading"]'::variant) │ to_varchar('["cooking", "reading"]'::variant) │ json_to_string('["cooking", "reading"]'::variant) │
├────────────────────────────────────────────────┼──────────────────────────────────────────────┼────────────────────────────────────────────┼───────────────────────────────────────────────┼───────────────────────────────────────────────────┤
│ ["Cooking","Reading"]                          │ ["Cooking","Reading"]                        │ ["Cooking","Reading"]                      │ ["Cooking","Reading"]                         │ ["Cooking","Reading"]                             │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- With one argument, the function converts input to a string without validating as a date.
SELECT
  DATE_FORMAT('20223-12-25'),
  TO_STRING('20223-12-25'),
  TO_TEXT('20223-12-25'),
  TO_VARCHAR('20223-12-25'),
  JSON_TO_STRING('20223-12-25');

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ date_format('20223-12-25') │ to_string('20223-12-25') │ to_text('20223-12-25') │ to_varchar('20223-12-25') │ json_to_string('20223-12-25') │
├────────────────────────────┼──────────────────────────┼────────────────────────┼───────────────────────────┼───────────────────────────────┤
│ 20223-12-25                │ 20223-12-25              │ 20223-12-25            │ 20223-12-25               │ 20223-12-25                   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Using MySQL format style (default)
SELECT
  DATE_FORMAT('2022-12-25', '%m/%d/%Y'),
  TO_STRING('2022-12-25', '%m/%d/%Y'),
  TO_TEXT('2022-12-25', '%m/%d/%Y'),
  TO_VARCHAR('2022-12-25', '%m/%d/%Y'),
  JSON_TO_STRING('2022-12-25', '%m/%d/%Y');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ date_format('2022-12-25', '%m/%d/%Y') │ to_string('2022-12-25', '%m/%d/%Y') │ to_text('2022-12-25', '%m/%d/%Y') │ to_varchar('2022-12-25', '%m/%d/%Y') │ json_to_string('2022-12-25', '%m/%d/%Y') │
├───────────────────────────────────────┼─────────────────────────────────────┼───────────────────────────────────┼──────────────────────────────────────┼──────────────────────────────────────────┤
│ 12/25/2022                            │ 12/25/2022                          │ 12/25/2022                        │ 12/25/2022                           │ 12/25/2022                               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Using Oracle format style (same data as MySQL example above)
SETTINGS (date_format_style = 'Oracle') 
SELECT
  TO_STRING('2022-12-25', 'MM/DD/YYYY'),
  TO_CHAR('2022-12-25', 'MM/DD/YYYY');  -- Using TO_CHAR alias

┌─────────────────────────────────────────────────────────────────┐
│ to_string('2022-12-25', 'MM/DD/YYYY') │ to_char('2022-12-25', 'MM/DD/YYYY') │
├─────────────────────────────────────┼───────────────────────────────────┤
│ 12/25/2022                        │ 12/25/2022                        │

└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘