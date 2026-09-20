---
title: PostgreSQL Built-in Functions
summary: Learn about the PostgreSQL-compatible built-in functions supported by PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL Built-in Functions

PostgreSQL-compatible {{{ .starter }}} provides built-in functions for common string, numeric, date and time, aggregate, window, JSON, array, regular expression, sequence, and system operations.

## String functions

The following common string functions are supported:

| Function | Description |
| --- | --- |
| `UPPER(text)` | Converts text to uppercase. |
| `LOWER(text)` | Converts text to lowercase. |
| `LENGTH(text)` | Returns the number of characters. |
| `CHAR_LENGTH(text)` | Returns the number of characters. |
| `LEFT(text, n)` | Returns the first `n` characters. |
| `RIGHT(text, n)` | Returns the last `n` characters. |
| `TRIM(text)` | Removes leading and trailing spaces or specified characters. |
| `BTRIM(text [, chars])` | Removes characters from both ends. |
| `LTRIM(text [, chars])` | Removes characters from the left. |
| `RTRIM(text [, chars])` | Removes characters from the right. |
| `LPAD(text, length [, fill])` | Pads text on the left. |
| `RPAD(text, length [, fill])` | Pads text on the right. |
| `REPEAT(text, n)` | Repeats a string. |
| `REVERSE(text)` | Reverses a string. |
| `INITCAP(text)` | Converts the first letter of each word to uppercase. |
| `ASCII(text)` | Returns the character code of the first character. |
| `CHR(int)` | Returns the character for a character code. |
| `STRPOS(text, substring)` | Returns the 1-based position of a substring. |
| `POSITION(substring IN text)` | SQL-standard form of `STRPOS`. |
| `SPLIT_PART(text, delimiter, field)` | Splits text and returns one field. |
| `TRANSLATE(text, from, to)` | Replaces individual characters. |
| `OVERLAY(...)` | Replaces part of a string. |
| `STARTS_WITH(text, prefix)` | Checks whether text starts with a prefix. |
| `CONCAT(...)` | Concatenates values and ignores `NULL` arguments. |
| `CONCAT_WS(separator, ...)` | Concatenates values using a separator. |
| `SUBSTRING(...)` | Extracts a substring. |
| `REPLACE(text, from, to)` | Replaces occurrences of a substring. |
| `FORMAT(format, ...)` | Formats a string using PostgreSQL-style format specifiers. |
| `QUOTE_IDENT(text)` | Quotes a SQL identifier when necessary. |
| `QUOTE_LITERAL(text)` | Quotes a SQL literal. |
| `QUOTE_NULLABLE(text)` | Quotes a SQL literal and returns `NULL` for a null input. |

For example:

{{< copyable "sql" >}}

```sql
SELECT
    UPPER('hello') AS upper_text,
    LENGTH('PostgreSQL') AS text_length,
    CONCAT_WS('-', '2026', '09', '19') AS date_text,
    SPLIT_PART('a,b,c', ',', 2) AS second_part;
```

## Mathematical functions

The following common mathematical functions are supported:

| Function | Description |
| --- | --- |
| `ABS(x)` | Returns the absolute value. |
| `CEIL(x)` / `CEILING(x)` | Rounds up to the nearest integer. |
| `FLOOR(x)` | Rounds down to the nearest integer. |
| `ROUND(x [, scale])` | Rounds a numeric value. |
| `TRUNC(x [, scale])` | Truncates a numeric value. |
| `SQRT(x)` | Returns the square root. |
| `CBRT(x)` | Returns the cube root. |
| `POWER(x, y)` | Raises `x` to the power `y`. |
| `EXP(x)` | Returns the exponential value. |
| `LN(x)` | Returns the natural logarithm. |
| `LOG(x)` | Returns a logarithm. |
| `MOD(x, y)` | Returns the remainder. |
| `SIGN(x)` | Returns the sign of a number. |

For example:

{{< copyable "sql" >}}

```sql
SELECT
    ABS(-42),
    ROUND(4.567, 2),
    SQRT(16),
    POWER(2, 8);
```

## Date and time functions

The following common date and time functions and expressions are supported:

| Function or expression | Description |
| --- | --- |
| `CURRENT_DATE` | Returns the current date. |
| `CURRENT_TIME` | Returns the current time. |
| `CURRENT_TIMESTAMP` | Returns the current timestamp. |
| `LOCALTIME` | Returns the current local time. |
| `LOCALTIMESTAMP` | Returns the current local timestamp. |
| `NOW()` | Returns the current transaction timestamp. |
| `DATE_TRUNC(field, value)` | Truncates a date or timestamp to the specified unit. |
| `DATE_PART(field, value)` | Extracts one date or time field. |
| `EXTRACT(field FROM value)` | SQL-standard form for extracting a date or time field. |
| `AGE(timestamp [, timestamp])` | Returns a symbolic interval between timestamps. |
| `MAKE_DATE(year, month, day)` | Constructs a date. |
| `MAKE_INTERVAL(...)` | Constructs an interval. |

For example:

{{< copyable "sql" >}}

```sql
SELECT
    CURRENT_DATE,
    NOW(),
    DATE_TRUNC('day', NOW()),
    EXTRACT(YEAR FROM CURRENT_DATE);
```

Date and time arithmetic with `INTERVAL` is also supported:

{{< copyable "sql" >}}

```sql
SELECT NOW() - INTERVAL '7 days';
```

## Aggregate functions

The following common aggregate functions are supported:

| Function | Description |
| --- | --- |
| `COUNT(*)` | Counts rows. |
| `COUNT(expression)` | Counts non-null values. |
| `COUNT(DISTINCT expression)` | Counts distinct non-null values. |
| `SUM(expression)` | Returns the sum. |
| `AVG(expression)` | Returns the average. |
| `MIN(expression)` | Returns the minimum value. |
| `MAX(expression)` | Returns the maximum value. |
| `STRING_AGG(expression, delimiter)` | Concatenates values using a delimiter. |
| `ARRAY_AGG(expression)` | Aggregates values into an array. |
| `JSON_AGG(expression)` | Aggregates values into a JSON array. |
| `JSONB_AGG(expression)` | Aggregates values into a JSONB array. |
| `JSON_OBJECT_AGG(key, value)` | Aggregates key/value pairs into a JSON object. |
| `JSONB_OBJECT_AGG(key, value)` | Aggregates key/value pairs into a JSONB object. |
| `BOOL_AND(expression)` | Returns true if all non-null inputs are true. |
| `BOOL_OR(expression)` | Returns true if any non-null input is true. |

For example:

{{< copyable "sql" >}}

```sql
SELECT
    department,
    COUNT(*) AS employee_count,
    AVG(salary) AS average_salary,
    MAX(salary) AS maximum_salary
FROM employees
GROUP BY department;
```

Aggregate `FILTER` is supported:

{{< copyable "sql" >}}

```sql
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE active = true) AS active_count
FROM users;
```

## Window functions

PostgreSQL-compatible {{{ .starter }}} supports common ranking and value-access window functions.

### Ranking functions

- `ROW_NUMBER()`
- `RANK()`
- `DENSE_RANK()`
- `NTILE()`
- `PERCENT_RANK()`
- `CUME_DIST()`

For example:

{{< copyable "sql" >}}

```sql
SELECT
    name,
    department,
    salary,
    RANK() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS salary_rank
FROM employees;
```

### Value-access functions

- `LAG()`
- `LEAD()`
- `FIRST_VALUE()`
- `LAST_VALUE()`
- `NTH_VALUE()`

For example:

{{< copyable "sql" >}}

```sql
SELECT
    id,
    created_at,
    LAG(created_at) OVER (ORDER BY created_at) AS previous_created_at
FROM events;
```

### Aggregate functions as window functions

The following aggregate functions can be used with an `OVER` clause:

- `SUM`
- `AVG`
- `COUNT`
- `MIN`
- `MAX`
- `STRING_AGG`

For example:

{{< copyable "sql" >}}

```sql
SELECT
    department,
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS department_average
FROM employees;
```

Other aggregate functions cannot be used as window functions.

## JSON and JSONB functions

The following common JSON and JSONB functions are supported:

| Function | Description |
| --- | --- |
| `JSON_TYPEOF(json)` | Returns the type of the top-level JSON value. |
| `JSONB_TYPEOF(jsonb)` | Returns the type of the top-level JSONB value. |
| `JSON_BUILD_OBJECT(...)` | Builds a JSON object from key/value pairs. |
| `JSONB_BUILD_OBJECT(...)` | Builds a JSONB object from key/value pairs. |
| `JSON_BUILD_ARRAY(...)` | Builds a JSON array. |
| `JSONB_BUILD_ARRAY(...)` | Builds a JSONB array. |
| `JSON_ARRAY_LENGTH(json)` | Returns the length of a JSON array. |
| `JSONB_ARRAY_LENGTH(jsonb)` | Returns the length of a JSONB array. |
| `JSON_ARRAY_ELEMENTS(json)` | Expands a JSON array into rows. |
| `JSONB_ARRAY_ELEMENTS(jsonb)` | Expands a JSONB array into rows. |
| `JSON_OBJECT_KEYS(json)` | Returns object keys. |
| `JSONB_OBJECT_KEYS(jsonb)` | Returns object keys. |
| `JSONB_EACH(jsonb)` | Expands a JSONB object into key/value rows. |
| `JSONB_SET(jsonb, path, value [, create_missing])` | Replaces or inserts a JSONB value at a path. |

For example:

{{< copyable "sql" >}}

```sql
SELECT
    JSONB_TYPEOF('{"a":1}'::jsonb),
    JSONB_BUILD_OBJECT('name', 'Alice', 'active', true),
    JSONB_ARRAY_LENGTH('[1,2,3]'::jsonb);
```

### JSON operators

Common PostgreSQL JSON and JSONB operators are supported, including:

| Operator | Description |
| --- | --- |
| `->` | Gets a JSON value by key or array index. |
| `->>` | Gets a JSON value as text. |
| `#>` | Gets a JSON value by path. |
| `#>>` | Gets a JSON value by path as text. |
| `@>` | Checks JSONB containment. |
| `<@` | Checks whether JSONB is contained by another value. |
| `?` | Checks whether a key exists. |
| `?|` | Checks whether any listed key exists. |
| `?&` | Checks whether all listed keys exist. |

For example:

{{< copyable "sql" >}}

```sql
SELECT settings->>'theme'
FROM profiles
WHERE settings @> '{"active":true}';
```

## Array functions

The following common array functions are supported:

| Function | Description |
| --- | --- |
| `ARRAY_LENGTH(array, dimension)` | Returns the length of an array dimension. |
| `ARRAY_UPPER(array, dimension)` | Returns the upper bound of a dimension. |
| `ARRAY_LOWER(array, dimension)` | Returns the lower bound of a dimension. |
| `ARRAY_APPEND(array, element)` | Appends an element. |
| `ARRAY_PREPEND(element, array)` | Prepends an element. |
| `ARRAY_CAT(array1, array2)` | Concatenates arrays. |
| `ARRAY_POSITION(array, element)` | Returns the first matching position. |
| `ARRAY_POSITIONS(array, element)` | Returns all matching positions. |
| `ARRAY_REMOVE(array, element)` | Removes matching elements. |
| `ARRAY_REPLACE(array, from, to)` | Replaces matching elements. |
| `ARRAY_TO_STRING(array, delimiter [, null_string])` | Converts an array to text. |
| `STRING_TO_ARRAY(text, delimiter [, null_string])` | Splits text into an array. |
| `UNNEST(array)` | Expands an array into rows. |
| `GENERATE_SUBSCRIPTS(array, dimension)` | Generates valid array indexes. |

For example:

{{< copyable "sql" >}}

```sql
SELECT
    ARRAY_LENGTH(ARRAY['a', 'b', 'c'], 1),
    ARRAY_APPEND(ARRAY['a', 'b'], 'c'),
    ARRAY_POSITION(ARRAY['a', 'b', 'c'], 'b');
```

## Regular expression functions and operators

The following regular expression functions are supported:

| Function | Description |
| --- | --- |
| `REGEXP_REPLACE(text, pattern, replacement [, flags])` | Replaces text matching a regular expression. |
| `REGEXP_SPLIT_TO_ARRAY(text, pattern [, flags])` | Splits text using a regular expression. |
| `REGEXP_SPLIT_TO_TABLE(text, pattern [, flags])` | Splits text into multiple rows. |

For example:

{{< copyable "sql" >}}

```sql
SELECT REGEXP_REPLACE(
    'foo   bar',
    '\s+',
    ' ',
    'g'
);
```

The following regular expression operators are supported:

| Operator | Description |
| --- | --- |
| `~` | Case-sensitive match. |
| `~*` | Case-insensitive match. |
| `!~` | Case-sensitive non-match. |
| `!~*` | Case-insensitive non-match. |

For example:

{{< copyable "sql" >}}

```sql
SELECT 'PostgreSQL' ~* 'postgres';
```

## UUID, encoding, and hashing functions

Common UUID, encoding, and hashing functions include:

| Function | Description |
| --- | --- |
| `GEN_RANDOM_UUID()` | Generates a random UUID. |
| `MD5(text)` | Returns an MD5 hash as hexadecimal text. |
| `ENCODE(bytea, format)` | Encodes binary data. |
| `DECODE(text, format)` | Decodes text into binary data. |

Additional UUID functions are provided through the `uuid-ossp` compatibility extension.

## Sequence functions

The following sequence functions are supported:

| Function | Description |
| --- | --- |
| `NEXTVAL(sequence)` | Advances a sequence and returns the new value. |
| `CURRVAL(sequence)` | Returns the last value returned by `NEXTVAL` for the sequence in the current session. |
| `SETVAL(sequence, value [, called])` | Sets the current sequence value. |
| `LASTVAL()` | Returns the last value returned by `NEXTVAL` in the current session. |

For example:

{{< copyable "sql" >}}

```sql
CREATE SEQUENCE order_seq START WITH 1000;

SELECT nextval('order_seq');
SELECT currval('order_seq');
SELECT setval('order_seq', 2000);
```

Sequence operations such as `NEXTVAL` are non-transactional.

## Conditional expressions

The following PostgreSQL conditional expressions are supported:

- `CASE`
- `COALESCE`
- `NULLIF`
- `GREATEST`
- `LEAST`

For example:

{{< copyable "sql" >}}

```sql
SELECT
    COALESCE(nickname, name) AS display_name,
    NULLIF(score, 0) AS nonzero_score
FROM users;
```

## System and compatibility functions

Common PostgreSQL-compatible system functions include:

| Function or expression | Description |
| --- | --- |
| `CURRENT_USER` | Returns the current role name. |
| `SESSION_USER` | Returns the session user. |
| `CURRENT_DATABASE()` | Returns the current database. |
| `CURRENT_SCHEMA()` | Returns the current schema. |
| `CURRENT_SCHEMAS(boolean)` | Returns schemas in the current search path. |
| `VERSION()` | Returns PostgreSQL-compatible server version information. |
| `PG_TYPEOF(value)` | Returns the data type of a value. |
| `PG_BACKEND_PID()` | Returns a PostgreSQL-compatible backend process identifier. |
| `CURRENT_SETTING(name)` | Returns a session parameter value. |

For example:

{{< copyable "sql" >}}

```sql
SELECT
    CURRENT_USER,
    CURRENT_DATABASE(),
    CURRENT_SCHEMA(),
    PG_TYPEOF(42);
```

## Set-returning functions

Some functions return multiple rows.

Use `GENERATE_SERIES()` in the `FROM` clause:

{{< copyable "sql" >}}

```sql
SELECT value
FROM generate_series(1, 5) AS t(value);
```

`UNNEST()` can expand an array:

{{< copyable "sql" >}}

```sql
SELECT value
FROM unnest(ARRAY['a', 'b', 'c']) AS t(value);
```

Function call position can differ from PostgreSQL for some scalar and set-returning functions. For portability, use scalar functions in expression position and follow the documented form for set-returning functions.

## Extension-specific functions

The following capabilities provide additional SQL functions:

- Vector search and embedding
- Full-text search
- HTTP requests
- Parquet import
- UUID generation

For more information, see [PostgreSQL Extensions](/tidb-cloud/pg-on-starter/pg-extensions-overview.md).