---
title: JSON Functions That Aggregate JSON Values
summary: JSON 値を集約する JSON関数について学習します。
---

# JSON値を集約するJSON関数 {#json-functions-that-aggregate-json-values}

このページにリストされている関数は、TiDB がサポートする[集計関数](/functions-and-operators/aggregate-group-by-functions.md)の一部ですが、JSON の操作に特化しています。

## <a href="https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-arrayagg">JSON_ARRAYAGG()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-aggregate-functions-html-function-json-arrayagg-json-arrayagg-a}

`JSON_ARRAYAGG(key)`関数は、指定された`key`に従ってキーの値を JSON 配列に集約します。5 `key`通常、式または列名です。

例：

ここでは、テーブルの 1 つの列にある 2 つの行が JSON 配列に集約されます。

```sql
SELECT JSON_ARRAYAGG(v) FROM (SELECT 1 'v' UNION SELECT 2);
```

    +------------------+
    | JSON_ARRAYAGG(v) |
    +------------------+
    | [2, 1]           |
    +------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_json-objectagg">JSON_OBJECTAGG()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-aggregate-functions-html-function-json-objectagg-json-objectagg-a}

`JSON_OBJECTAGG(key,value)`関数は、指定された`key`と`value`に従って、キーとキーの値をJSONオブジェクトに集約します。7 と`value` `key` 、式または列名です。

例：

まず、2 つのテーブルを作成し、そこにいくつかの行を追加します。

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

これで、作成されたテーブルがどのように見えるかを確認できます。

```sql
TABLE plants;
```

    +----+--------+
    | id | name   |
    +----+--------+
    |  1 | rose   |
    |  2 | tulip  |
    |  3 | orchid |
    +----+--------+
    3 rows in set (0.00 sec)

```sql
TABLE plant_attributes;
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

このデータには`JSON_OBJECTAGG()`関数を使用できます。ここでは、グループごとに複数のキーと値のペアがJSONオブジェクトに集約されていることがわかります。

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

    +--------+-----------------------------------------------------------+
    | name   | JSON_OBJECTAGG(attribute,value)                           |
    +--------+-----------------------------------------------------------+
    | rose   | {"color": "red", "thorns": "yes"}                         |
    | orchid | {"color": "white", "thorns": "no"}                        |
    | tulip  | {"color": "orange", "grows_from": "bulb", "thorns": "no"} |
    +--------+-----------------------------------------------------------+
    3 rows in set (0.00 sec)

## 参照 {#see-also}

-   [JSON関数の概要](/functions-and-operators/json-functions.md)
-   [JSONデータ型](/data-type-json.md)
