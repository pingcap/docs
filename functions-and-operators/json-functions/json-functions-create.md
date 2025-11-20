---
title: JSON Functions That Create JSON Values
summary: JSON 値を作成する JSON関数について学習します。
---

# JSON値を作成するJSON関数 {#json-functions-that-create-json-values}

TiDB は、MySQL 8.0 で利用可能な[JSON値を作成するJSON関数](https://dev.mysql.com/doc/refman/8.0/en/json-creation-functions.html)すべてをサポートします。

## <code>JSON_ARRAY()</code> {#code-json-array-code}

`JSON_ARRAY([val[, val] ...])`関数は、(空の可能性のある)値のリストを評価し、それらの値を含む JSON 配列を返します。

```sql
SELECT JSON_ARRAY(1,2,3,4,5), JSON_ARRAY("foo", "bar");
```

    +-----------------------+--------------------------+
    | JSON_ARRAY(1,2,3,4,5) | JSON_ARRAY("foo", "bar") |
    +-----------------------+--------------------------+
    | [1, 2, 3, 4, 5]       | ["foo", "bar"]           |
    +-----------------------+--------------------------+
    1 row in set (0.00 sec)

## <code>JSON_OBJECT()</code> {#code-json-object-code}

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

## <code>JSON_QUOTE()</code> {#code-json-quote-code}

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

-   [JSON関数の概要](/functions-and-operators/json-functions.md)
-   [JSONデータ型](/data-type-json.md)
