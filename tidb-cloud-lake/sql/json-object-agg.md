---
title: JSON_OBJECT_AGG
summary: キーと値のペアを JSON オブジェクトに変換します。入力内の各行について、キーは `<key_expression>` から導出され、値は `<value_expression>` から導出されるキーと値のペアを生成します。これらのキーと値のペアは、その後 1 つの JSON オブジェクトに結合されます。
---

# JSON_OBJECT_AGG

キーと値のペアを JSON オブジェクトに変換します。入力内の各行について、キーは `<key_expression>` から導出され、値は `<value_expression>` から導出されるキーと値のペアを生成します。これらのキーと値のペアは、その後 1 つの JSON オブジェクトに結合されます。

関連情報: [JSON_ARRAY_AGG](/tidb-cloud-lake/sql/json-array-agg.md)

## 構文 {#syntax}

```sql
JSON_OBJECT_AGG(<key_expression>, <value_expression>)
```

| パラメータ        | 説明                                                                                                                                              |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| key_expression   | JSON オブジェクト内のキーを指定します。**文字列**式のみをサポートします。`key_expression` の評価結果が NULL の場合、そのキーと値のペアはスキップされます。 |
| value_expression | JSON オブジェクト内の値を指定します。サポートされている任意のデータ型を使用できます。`value_expression` の評価結果が NULL の場合、そのキーと値のペアはスキップされます。 |

## 戻り値の型 {#return-type}

JSON オブジェクト。

## 例 {#examples}

この例では、JSON_OBJECT_AGG を使用して、小数、整数、JSON バリアント、配列などの異なる種類のデータを、各 JSON オブジェクトのキーとしてカラム b を使用しながら JSON オブジェクトに集約する方法を示します。

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