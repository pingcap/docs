---
title: Variant
summary: VARIANT 可以存储任何其他类型的值，包括 NULL、BOOLEAN、NUMBER、STRING、ARRAY 和 OBJECT，并且其内部值可以是任意级别的嵌套结构，因此能够非常灵活地存储各种数据。VARIANT 也可以称为 JSON，更多信息请参阅 JSON website。
---

# Variant

VARIANT 可以存储任何其他类型的值，包括 NULL、BOOLEAN、NUMBER、STRING、ARRAY 和 OBJECT，并且其内部值可以是任意级别的嵌套结构，因此能够非常灵活地存储各种数据。VARIANT 也可以称为 JSON，更多信息请参阅 [JSON website](https://www.json.org/json-en.html)。

下面是在 {{{ .lake }}} 中插入和查询 Variant 数据的示例：

创建表：

```sql
CREATE TABLE customer_orders(id INT64, order_data VARIANT);
```

向表中插入不同类型的值：

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

查询结果：

```sql
SELECT * FROM customer_orders;
```

结果：

```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        id       │                                                   order_data                                                  │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│               1 │ {"customer_id":123,"items":[{"name":"Shoes","price":59.99},{"name":"T-shirt","price":19.99}],"order_id":1001} │
│               2 │ {"customer_id":456,"items":[{"name":"Backpack","price":79.99},{"name":"Socks","price":4.99}],"order_id":1002} │
│               3 │ {"customer_id":123,"items":[{"name":"Shoes","price":59.99},{"name":"Socks","price":4.99}],"order_id":1003}    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 访问 JSON 中的元素 {#accessing-elements-in-json}

### 按索引访问 {#accessing-by-index}

VARIANT 类型可以包含数组，这是一种从零开始计数的数组，与许多其他编程语言类似。数组中的每个元素也都是 VARIANT 类型。可以使用**方括号**按索引访问元素。

#### 示例 {#example}

创建表：

```sql
-- Create a table to store user hobbies
CREATE TABLE user_hobbies(user_id INT64, hobbies VARIANT NULL);
```

向表中插入示例数据：

```sql
INSERT INTO user_hobbies
VALUES
    (1, '["Cooking", "Reading", "Cycling"]'),
    (2, '["Photography", "Travel", "Swimming"]');
```

获取每个用户的第一个爱好：

```sql
SELECT
  user_id,
  hobbies [0] AS first_hobby
FROM
  user_hobbies;
```

结果：

```sql
┌─────────────────────────────────────┐
│     user_id     │    first_hobby    │
├─────────────────┼───────────────────┤
│               1 │ "Cooking"         │
│               2 │ "Photography"     │
└─────────────────────────────────────┘
```

获取每个用户的第三个爱好：

```sql
SELECT
  hobbies [2],
  count() AS third_hobby
FROM
  user_hobbies
GROUP BY
  hobbies [2];
```

结果：

```sql
┌─────────────────────────────────┐
│     hobbies[2]    │ third_hobby │
├───────────────────┼─────────────┤
│ "Swimming"        │           1 │
│ "Cycling"         │           1 │
└─────────────────────────────────┘
```

按组查询爱好：

```sql
SELECT
  hobbies [2],
  count() AS third_hobby
FROM
  user_hobbies
GROUP BY
  hobbies [2];
```

结果：

```sql
┌────────────┬─────────────┐
│ hobbies[2] │ third_hobby │
├────────────┼─────────────┤
│ "Cycling"  │           1 │
│ "Swimming" │           1 │
└────────────┴─────────────┘
```

### 按字段名访问 {#accessing-by-field-name}

VARIANT 类型可以包含以对象形式表示的键值对，其中每个键都是 VARCHAR，每个值都是 VARIANT。它的工作方式类似于其他编程语言中的“dictionary”“hash”或“map”。可以使用**方括号**或**冒号**按字段名访问值；对于第 2 级及更深层级，还可以使用**点号**访问（为避免与表和列之间的点号表示法混淆，点号不能用于第 1 级名称表示法）。

#### 示例 {#example}

创建一个表，使用 VARIANT 类型存储用户偏好：

```sql
CREATE TABLE user_preferences(
  user_id INT64,
  preferences VARIANT NULL,
  profile Tuple(name STRING, age INT)
);
```

向表中插入示例数据：

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

查询每个用户偏好的颜色：

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

结果：

```sql
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ preferences['settings']['color'] │ preferences['settings']:color │ preferences['settings']:color │ preferences:settings['color'] │ preferences:settings:color │ preferences:settings:color │
├──────────────────────────────────┼───────────────────────────────┼───────────────────────────────┼───────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ "red"                            │ "red"                         │ "red"                         │ "red"                         │ "red"                      │ "red"                      │
│ "blue"                           │ "blue"                        │ "blue"                        │ "blue"                        │ "blue"                     │ "blue"                     │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

请注意，字段名是**大小写敏感**的。如果字段名包含空格或特殊字符，请将其用双引号括起来。

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

## 数据类型转换 {#data-type-conversion}

默认情况下，从 VARIANT 列中检索到的元素会按原样返回。要将返回的元素转换为特定类型，请添加 `::` 运算符和目标数据类型（例如 `expression::type`）。

创建一个表，使用 VARIANT 列存储用户偏好：

```sql
CREATE TABLE user_pref(user_id INT64, pref VARIANT NULL);
```

向表中插入示例数据：

```sql
INSERT INTO user_pref
VALUES
    (1, parse_json('{"age": 25, "isPremium": "true", "lastActive": "2023-04-10"}')),
    (2, parse_json('{"age": 30, "isPremium": "false", "lastActive": "2023-03-15"}'));
```

将 age 转换为 INT64：

```sql
SELECT user_id, pref:age::INT64 as age FROM user_pref;
```

结果：

```sql
┌─────────┬─────┐
│ user_id │ age │
├─────────┼─────┤
│       1 │  25 │
│       2 │  30 │
└─────────┴─────┘
```

## JSON 函数 {#json-functions}

参见 [Variant 函数](/tidb-cloud-lake/sql/structured-semi-structured-functions.md)。