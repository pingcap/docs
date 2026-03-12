---
title: Variant
sidebar_position: 11
---

A VARIANT can store a value of any other type, including NULL, BOOLEAN, NUMBER, STRING, ARRAY, and OBJECT, and the internal value can be any level of nested structure, which is very flexible to store various data. VARIANT can also be called JSON, for more information, please refer to [JSON website](https://www.json.org/json-en.html).

Here's an example of inserting and querying Variant data in Databend:

Create a table:
```sql
CREATE TABLE customer_orders(id INT64, order_data VARIANT);
```

Insert a value with different type into the table:
```sql
INSERT INTO
  customer_orders
VALUES
  (
    1,
    '{"customer_id": 123, "order_id": 1001, "items": [{"name": "Shoes", "price": 59.99}, {"name": "T-shirt", "price": 19.99}]}'
  ),
  (
    2,
    '{"customer_id": 456, "order_id": 1002, "items": [{"name": "Backpack", "price": 79.99}, {"name": "Socks", "price": 4.99}]}'
  ),
  (
    3,
    '{"customer_id": 123, "order_id": 1003, "items": [{"name": "Shoes", "price": 59.99}, {"name": "Socks", "price": 4.99}]}'
  );
```

Query the result:
```sql
SELECT * FROM customer_orders;
```

Result:
```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        id       │                                                   order_data                                                  │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│               1 │ {"customer_id":123,"items":[{"name":"Shoes","price":59.99},{"name":"T-shirt","price":19.99}],"order_id":1001} │
│               2 │ {"customer_id":456,"items":[{"name":"Backpack","price":79.99},{"name":"Socks","price":4.99}],"order_id":1002} │
│               3 │ {"customer_id":123,"items":[{"name":"Shoes","price":59.99},{"name":"Socks","price":4.99}],"order_id":1003}    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Accessing Elements in JSON

### Accessing by Index

The VARIANT type contains an array, which is a zero-based array like many other programming languages. Each element within the array is also of the VARIANT type. Elements can be accessed by their index using **square brackets**.

#### Example

Create a table:
```sql
-- Create a table to store user hobbies
CREATE TABLE user_hobbies(user_id INT64, hobbies VARIANT NULL);
```

Insert sample data into the table:
```sql
INSERT INTO user_hobbies 
VALUES
    (1, '["Cooking", "Reading", "Cycling"]'),
    (2, '["Photography", "Travel", "Swimming"]');
```

Retrieve the first hobby for each user:
```sql
SELECT
  user_id,
  hobbies [0] AS first_hobby
FROM
  user_hobbies;
```
Result:
```sql
┌─────────────────────────────────────┐
│     user_id     │    first_hobby    │
├─────────────────┼───────────────────┤
│               1 │ "Cooking"         │
│               2 │ "Photography"     │
└─────────────────────────────────────┘
```

Retrieve the third hobby for each user:
```sql
SELECT
  hobbies [2],
  count() AS third_hobby
FROM
  user_hobbies
GROUP BY
  hobbies [2];
```

Result:
```sql
┌─────────────────────────────────┐
│     hobbies[2]    │ third_hobby │
├───────────────────┼─────────────┤
│ "Swimming"        │           1 │
│ "Cycling"         │           1 │
└─────────────────────────────────┘
```

Retrieve hobbies with a group by:
```sql
SELECT
  hobbies [2],
  count() AS third_hobby
FROM
  user_hobbies
GROUP BY
  hobbies [2];
```
Result:
```sql
┌────────────┬─────────────┐
│ hobbies[2] │ third_hobby │
├────────────┼─────────────┤
│ "Cycling"  │           1 │
│ "Swimming" │           1 │
└────────────┴─────────────┘
```

### Accessing by Field Name

The VARIANT type contains key-value pairs represented as objects, where each key is a VARCHAR and each value is a VARIANT. It functions similarly to a "dictionary," "hash," or "map" in other programming languages. Values can be accessed by the field name using either **square brackets** or **colons**, as well as **dots** for the 2nd level and deeper only (Dots cannot be used as a first-level name notation to avoid confusion with dot notation between table and column).

#### Example

Create a table to store user preferences with VARIANT type:
```sql
CREATE TABLE user_preferences(
  user_id INT64,
  preferences VARIANT NULL,
  profile Tuple(name STRING, age INT)
);
```

Insert sample data into the table:
```sql
INSERT INTO
  user_preferences
VALUES
  (
    1,
    '{"settings":{"color":"red", "fontSize":16, "theme":"dark"}}',
    ('Amy', 12)
  ),
  (
    2,
    '{"settings":{"color":"blue", "fontSize":14, "theme":"light"}}',
    ('Bob', 11)
  );
```

Retrieve the preferred color for each user:
```sql
SELECT
  preferences['settings']['color'],
  preferences['settings']:color,
  preferences['settings'].color,
  preferences:settings['color'],
  preferences:settings:color,
  preferences:settings.color
FROM
  user_preferences;
```

Result:
```sql
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ preferences['settings']['color'] │ preferences['settings']:color │ preferences['settings']:color │ preferences:settings['color'] │ preferences:settings:color │ preferences:settings:color │
├──────────────────────────────────┼───────────────────────────────┼───────────────────────────────┼───────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ "red"                            │ "red"                         │ "red"                         │ "red"                         │ "red"                      │ "red"                      │
│ "blue"                           │ "blue"                        │ "blue"                        │ "blue"                        │ "blue"                     │ "blue"                     │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Please note that field names are **case-sensitive**. If a field name contains spaces or special characters, enclose it in double quotes.

```sql
INSERT INTO
  user_preferences
VALUES
  (
    3,
    '{"new settings":{"color":"red", "fontSize":16, "theme":"dark"}}',
    ('Cole', 13)
  );

-- Double-quote the field name "new settings"
SELECT preferences:"new settings":color 
FROM user_preferences;

┌──────────────────────────────────┐
│ preferences:"new settings":color │
├──────────────────────────────────┤
│ NULL                             │
│ NULL                             │
│ "red"                            │
└──────────────────────────────────┘

-- No results are returned when 'c' in 'color' is capitalized
SELECT preferences:"new settings":Color 
FROM user_preferences;

┌──────────────────────────────────┐
│ preferences:"new settings":color │
│         Nullable(Variant)        │
├──────────────────────────────────┤
│ NULL                             │
│ NULL                             │
│ NULL                             │
└──────────────────────────────────┘
```

## Data Type Conversion

By default, elements retrieved from a VARIANT column are returned. To convert a returned element to a specific type, add the `::` operator and the target data type (e.g. expression::type).

Create a table to store user preferences with a VARIANT column:
```sql
CREATE TABLE user_pref(user_id INT64, pref VARIANT NULL);
```

Insert sample data into the table:
```sql
INSERT INTO user_pref 
VALUES
    (1, parse_json('{"age": 25, "isPremium": "true", "lastActive": "2023-04-10"}')),
    (2, parse_json('{"age": 30, "isPremium": "false", "lastActive": "2023-03-15"}'));
```

Convert the age to an INT64:
```sql
SELECT user_id, pref:age::INT64 as age FROM user_pref;
```
Result:
```sql
┌─────────┬─────┐
│ user_id │ age │
├─────────┼─────┤
│       1 │  25 │
│       2 │  30 │
└─────────┴─────┘
```

## JSON Functions

See [Variant Functions](/sql/sql-functions/semi-structured-functions).
