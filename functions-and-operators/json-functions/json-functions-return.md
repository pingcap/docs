---
title: JSON Functions That Return JSON Values
summary: JSON 値を返す JSON関数について学習します。
---

# JSON 値を返す JSON 関数 {#json-functions-that-return-json-values}

このドキュメントでは、JSON 値を返す JSON関数について説明します。

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-depth">JSON_DEPTH()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-attribute-functions-html-function-json-depth-json-depth-a}

`JSON_DEPTH(json_doc)`関数は、JSON ドキュメントの最大深度を返します。

例:

次の例では、レベルが 3 つあるため、 `JSON_DEPTH()` `3`返します。

-   ルート ( `$` )
-   天気 ( `$.weather` )
-   気象の流れ ( `$.weather.sunny` )

```sql
SELECT JSON_DEPTH('{"weather": {"current": "sunny"}}');
```

    +-------------------------------------------------+
    | JSON_DEPTH('{"weather": {"current": "sunny"}}') |
    +-------------------------------------------------+
    |                                               3 |
    +-------------------------------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-length">JSON_LENGTH()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-attribute-functions-html-function-json-length-json-length-a}

`JSON_LENGTH(json_doc [,path])`関数は`path`ドキュメントの長さを返します。3 引数が指定されている場合は、パス内の値の長さを返します。

例:

次の例では、ドキュメントのルートにある唯一の項目が`weather`であるため、返される値は`1`になります。

```sql
SELECT JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$');
```

    +----------------------------------------------------------------------------+
    | JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$') |
    +----------------------------------------------------------------------------+
    |                                                                          1 |
    +----------------------------------------------------------------------------+
    1 row in set (0.00 sec)

次の例では、 `$.weather`に`current`と`tomorrow` 2 つの項目があるため、返される値は`2`になります。

```sql
SELECT JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$.weather');
```

    +------------------------------------------------------------------------------------+
    | JSON_LENGTH('{"weather": {"current": "sunny", "tomorrow": "cloudy"}}','$.weather') |
    +------------------------------------------------------------------------------------+
    |                                                                                  2 |
    +------------------------------------------------------------------------------------+
    1 row in set (0.01 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-type">JSON_TYPE()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-attribute-functions-html-function-json-type-json-type-a}

`JSON_TYPE(json_val)`関数は[JSON値の型](/data-type-json.md#json-value-types)示す文字列を返します。

例：

```sql
WITH demo AS (
    SELECT 'null' AS 'v' 
    UNION SELECT '"foobar"' 
    UNION SELECT 'true' 
    UNION SELECT '5' 
    UNION SELECT '1.14' 
    UNION SELECT '[]' 
    UNION SELECT '{}' 
    UNION SELECT POW(2,63)
)
SELECT v, JSON_TYPE(v) FROM demo ORDER BY 2;
```

    +----------------------+--------------+
    | v                    | JSON_TYPE(v) |
    +----------------------+--------------+
    | []                   | ARRAY        |
    | true                 | BOOLEAN      |
    | 1.14                 | DOUBLE       |
    | 9.223372036854776e18 | DOUBLE       |
    | 5                    | INTEGER      |
    | null                 | NULL         |
    | {}                   | OBJECT       |
    | "foobar"             | STRING       |
    +----------------------+--------------+
    8 rows in set (0.00 sec)

次の例に示すように、同じに見える値が同じ型ではない場合があることに注意してください。

```sql
SELECT '"2025-06-14"',CAST(CAST('2025-06-14' AS date) AS json);
```

    +--------------+------------------------------------------+
    | "2025-06-14" | CAST(CAST('2025-06-14' AS date) AS json) |
    +--------------+------------------------------------------+
    | "2025-06-14" | "2025-06-14"                             |
    +--------------+------------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT JSON_TYPE('"2025-06-14"'),JSON_TYPE(CAST(CAST('2025-06-14' AS date) AS json));
```

    +---------------------------+-----------------------------------------------------+
    | JSON_TYPE('"2025-06-14"') | JSON_TYPE(CAST(CAST('2025-06-14' AS date) AS json)) |
    +---------------------------+-----------------------------------------------------+
    | STRING                    | DATE                                                |
    +---------------------------+-----------------------------------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-attribute-functions.html#function_json-valid">JSON_VALID()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-attribute-functions-html-function-json-valid-json-valid-a}

`JSON_VALID(str)`関数は、引数が有効な JSON であるかどうかを確認します。これは、列を`JSON`型に変換する前にチェックするのに役立ちます。

```sql
SELECT JSON_VALID('{"foo"="bar"}');
```

    +-----------------------------+
    | JSON_VALID('{"foo"="bar"}') |
    +-----------------------------+
    |                           0 |
    +-----------------------------+
    1 row in set (0.01 sec)

```sql
SELECT JSON_VALID('{"foo": "bar"}');
```

    +------------------------------+
    | JSON_VALID('{"foo": "bar"}') |
    +------------------------------+
    |                            1 |
    +------------------------------+
    1 row in set (0.01 sec)

## 参照 {#see-also}

-   [JSON 関数の概要](/functions-and-operators/json-functions.md)
-   [JSON データ型](/data-type-json.md)
