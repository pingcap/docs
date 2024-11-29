---
title: JSON Functions That Create JSON Values
summary: JSON 値を作成する JSON関数について学習します。
---

# JSON 値を作成する JSON 関数 {#json-functions-that-create-json-values}

このドキュメントでは、JSON 値を作成する JSON関数について説明します。

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-array">JSON_ARRAY()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-creation-functions-html-function-json-array-json-array-a}

`JSON_ARRAY([val[, val] ...])`関数は、(空の可能性のある) 値のリストを評価し、それらの値を含む JSON 配列を返します。

```sql
SELECT JSON_ARRAY(1,2,3,4,5), JSON_ARRAY("foo", "bar");
```

    +-----------------------+--------------------------+
    | JSON_ARRAY(1,2,3,4,5) | JSON_ARRAY("foo", "bar") |
    +-----------------------+--------------------------+
    | [1, 2, 3, 4, 5]       | ["foo", "bar"]           |
    +-----------------------+--------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-object">JSON_OBJECT()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-creation-functions-html-function-json-object-json-object-a}

`JSON_OBJECT([key, val[, key, val] ...])`関数は、キーと値のペアの (空の場合もある) リストを評価し、それらのペアを含む JSON オブジェクトを返します。

```sql
SELECT JSON_OBJECT("database", "TiDB", "distributed", TRUE);
```

    +------------------------------------------------------+
    | JSON_OBJECT("database", "TiDB", "distributed", TRUE) |
    +------------------------------------------------------+
    | {"database": "TiDB", "distributed": true}            |
    +------------------------------------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html#function_json-quote">JSON_QUOTE()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-creation-functions-html-function-json-quote-json-quote-a}

`JSON_QUOTE(str)`関数は、引用符付きの JSON 値として文字列を返します。

```sql
SELECT JSON_QUOTE('The name is "O\'Neil"');
```

    +-------------------------------------+
    | JSON_QUOTE('The name is "O\'Neil"') |
    +-------------------------------------+
    | "The name is \"O'Neil\""            |
    +-------------------------------------+
    1 row in set (0.00 sec)

## 参照 {#see-also}

-   [JSON 関数の概要](/functions-and-operators/json-functions.md)
-   [JSON データ型](/data-type-json.md)
