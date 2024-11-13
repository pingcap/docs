---
title: JSON Functions That Aggregate JSON Values
summary: Learn about JSON functions that aggregate JSON values.
---

# JSON Functions That Aggregate JSON Values

The functions listed on this page are part of the [aggregate functions](/functions-and-operators/aggregate-group-by-functions.md) that TiDB supports, but are specific to working with JSON.

## [JSON_ARRAYAGG()](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-arrayagg)

The `JSON_ARRAYAGG(key)` function aggregates values of keys into a JSON array according to the given `key`. `key` is typically an expression or a column name.

Example:

Here the two rows in one column of a table get aggregated into a JSON array.

```sql
SELECT JSON_ARRAYAGG(v) FROM (SELECT 1 'v' UNION SELECT 2);
```

```
+------------------+
| JSON_ARRAYAGG(v) |
+------------------+
| [2, 1]           |
+------------------+
1 row in set (0.00 sec)
```

## [JSON_OBJECTAGG()](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-objectagg)

The `JSON_OBJECTAGG(key,value)` function aggregates keys and values of keys into a JSON object according to the given `key` and `value`. Both `key` or `value` are typically an expression or a column name.

Example:

First, create two tables and add a few rows to them.

```sql
CREATE TABLE plants (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE plant_attributes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plant_id INT, attribute VARCHAR(255),
    value VARCHAR(255),
    FOREIGN KEY (plant_id) REFERENCES plants(id)
);

INSERT INTO plants
VALUES
(1,"rose"),
(2,"tulip"),
(3,"orchid");

INSERT INTO plant_attributes(plant_id,attribute,value)
VALUES
(1,"color","red"),
(1,"thorns","yes"),
(2,"color","orange"),
(2,"thorns","no"),
(2,"grows_from","bulb"),
(3,"color","white"),
(3, "thorns","no");
```

Now you can check what the created tables look like.

```sql
TABLE plants;
```

```
+----+--------+
| id | name   |
+----+--------+
|  1 | rose   |
|  2 | tulip  |
|  3 | orchid |
+----+--------+
3 rows in set (0.00 sec)
```

```sql
TABLE plant_attributes;
```

```
+----+----------+------------+--------+
| id | plant_id | attribute  | value  |
+----+----------+------------+--------+
|  1 |        1 | color      | red    |
|  2 |        1 | thorns     | yes    |
|  3 |        2 | color      | orange |
|  4 |        2 | thorns     | no     |
|  5 |        2 | grows_from | bulb   |
|  6 |        3 | color      | white  |
|  7 |        3 | thorns     | no     |
+----+----------+------------+--------+
7 rows in set (0.00 sec)
```

You can use the `JSON_OBJECTAGG()` function with this data. Here you can see that for every group multiple key/value pairs are aggregated into a JSON object.

```sql
SELECT
    p.name,
    JSON_OBJECTAGG(attribute,value)
FROM
    plant_attributes pa
    LEFT JOIN plants p ON pa.plant_id=p.id
GROUP BY
    plant_id;
```

```
+--------+-----------------------------------------------------------+
| name   | JSON_OBJECTAGG(attribute,value)                           |
+--------+-----------------------------------------------------------+
| rose   | {"color": "red", "thorns": "yes"}                         |
| orchid | {"color": "white", "thorns": "no"}                        |
| tulip  | {"color": "orange", "grows_from": "bulb", "thorns": "no"} |
+--------+-----------------------------------------------------------+
3 rows in set (0.00 sec)
```

## See also

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)