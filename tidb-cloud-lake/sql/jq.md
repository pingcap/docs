---
title: JQ
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.622"/>

The JQ function is a set-returning SQL function that allows you to apply [jq](https://jqlang.github.io/jq/) filters to JSON data stored in Variant columns. With this function, you can process JSON data by applying a specified jq filter, returning the results as a set of rows.

## Syntax

```sql
JQ (<jq_expression>, <json_data>)
```

| Parameter       | Description                                                                                                                                                                                                                                                                                                                                                 |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `jq_expression` | A `jq` filter expression that defines how to process and transform JSON data using the `jq` syntax. This expression can specify how to select, modify, and manipulate data within JSON objects and arrays. For information on the syntax, filters, and functions supported by jq, please refer to the [jq Manual](https://jqlang.github.io/jq/manual/#basic-filters). |
| `json_data`     | The JSON-formatted input that you want to process or transform using the `jq` filter expression. It can be a JSON object, array, or any valid JSON data structure.                                                                                                                                                                                          |

## Return Type

The JQ function returns a set of JSON values, where each value corresponds to an element of the transformed or extracted result based on the `<jq_expression>`.

## Examples

To start, we create a table named `customer_data` with columns for `id` and `profile`, where `profile` is a JSON type to store user information:

```sql
CREATE TABLE customer_data (
    id INT,
    profile JSON
);

INSERT INTO customer_data VALUES
    (1, '{"name": "Alice", "age": 30, "city": "New York"}'),
    (2, '{"name": "Bob", "age": 25, "city": "Los Angeles"}'),
    (3, '{"name": "Charlie", "age": 35, "city": "Chicago"}');
```

This example extracts specific fields from the JSON data:

```sql
SELECT
    id,
    jq('.name', profile) AS customer_name
FROM
    customer_data;

┌─────────────────────────────────────┐
│        id       │   customer_name   │
├─────────────────┼───────────────────┤
│               1 │ "Alice"           │
│               2 │ "Bob"             │
│               3 │ "Charlie"         │
└─────────────────────────────────────┘
```

This example selects the user ID and the age incremented by 1 for each user:

```sql
SELECT
    id,
    jq('.age + 1', profile) AS updated_age
FROM
    customer_data;

┌─────────────────────────────────────┐
│        id       │    updated_age    │
├─────────────────┼───────────────────┤
│               1 │ 31                │
│               2 │ 26                │
│               3 │ 36                │
└─────────────────────────────────────┘
```

This example converts city names to uppercase:

```sql
SELECT
    id,
    jq('.city | ascii_upcase', profile) AS city_uppercase
FROM
    customer_data;

┌─────────────────────────────────────┐
│        id       │   city_uppercase  │
├─────────────────┼───────────────────┤
│               1 │ "NEW YORK"        │
│               2 │ "LOS ANGELES"     │
│               3 │ "CHICAGO"         │
└─────────────────────────────────────┘
```
