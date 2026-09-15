---
title: JSON_OBJECT_AGG
summary: 将键值对转换为 JSON 对象。对于输入中的每一行，它都会生成一个键值对，其中键派生自 `<key_expression>`，值派生自 `<value_expression>`。然后，这些键值对会合并为一个 JSON 对象。
---

# JSON_OBJECT_AGG

将键值对转换为 JSON 对象。对于输入中的每一行，它都会生成一个键值对，其中键派生自 `<key_expression>`，值派生自 `<value_expression>`。然后，这些键值对会合并为一个 JSON 对象。

另请参阅：[JSON_ARRAY_AGG](/tidb-cloud-lake/sql/json-array-agg.md)

## 语法 {#syntax}

```sql
JSON_OBJECT_AGG(<key_expression>, <value_expression>)
```

| 参数             | 描述                                                                                                                                                   |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| key_expression   | 指定 JSON 对象中的键。**仅支持字符串** 表达式。如果 `key_expression` 的计算结果为 NULL，则会跳过该键值对。                                             |
| value_expression | 指定 JSON 对象中的值。它可以是任何受支持的数据类型。如果 `value_expression` 的计算结果为 NULL，则会跳过该键值对。                                     |

## 返回类型 {#return-type}

JSON 对象。

## 示例 {#examples}

以下示例演示了如何使用 JSON_OBJECT_AGG 将不同类型的数据（例如小数、整数型、JSON 变体和数组）聚合为 JSON 对象，并以列 b 作为每个 JSON 对象的键：

```sql
CREATE TABLE d (
    a DECIMAL(10, 2),
    b STRING,
    c INT,
    d VARIANT,
    e ARRAY(STRING)
);

INSERT INTO d VALUES
    (20, 'abc', NULL, '{"k":"v"}', ['a','b']),
    (10, 'de', 100, 'null', []),
    (4.23, NULL, 200, '"uvw"', ['x','y']),
    (5.99, 'xyz', 300, '[1,2,3]', ['z']);

SELECT
    json_object_agg(b, a) AS json_a,
    json_object_agg(b, c) AS json_c,
    json_object_agg(b, d) AS json_d,
    json_object_agg(b, e) AS json_e
FROM
    d;

-[ RECORD 1 ]-----------------------------------
json_a: {"abc":20.0,"de":10.0,"xyz":5.99}
json_c: {"de":100,"xyz":300}
json_d: {"abc":{"k":"v"},"de":null,"xyz":[1,2,3]}
json_e: {"abc":["a","b"],"de":[],"xyz":["z"]}
```