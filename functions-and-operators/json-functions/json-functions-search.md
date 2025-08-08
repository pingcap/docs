---
title: JSON Functions That Search JSON Values
summary: JSON 値を検索する JSON関数について学習します。
---

# JSON値を検索するJSON関数 {#json-functions-that-search-json-values}

このドキュメントでは、JSON 値を検索する JSON関数について説明します。

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains">JSON_CONTAINS()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-search-functions-html-function-json-contains-json-contains-a}

`JSON_CONTAINS(json_doc, candidate [,path])`関数は、 `1`または`0`返すことで、指定された`candidate` JSON ドキュメントがターゲット JSON ドキュメント内に含まれているかどうかを示します。

例:

ここで`a`対象ドキュメントに含まれています。

```sql
SELECT JSON_CONTAINS('["a","b","c"]','"a"');
```

    +--------------------------------------+
    | JSON_CONTAINS('["a","b","c"]','"a"') |
    +--------------------------------------+
    |                                    1 |
    +--------------------------------------+
    1 row in set (0.00 sec)

ここで`e`対象文書に含まれていません。

```sql
SELECT JSON_CONTAINS('["a","b","c"]','"e"');
```

    +--------------------------------------+
    | JSON_CONTAINS('["a","b","c"]','"e"') |
    +--------------------------------------+
    |                                    0 |
    +--------------------------------------+
    1 row in set (0.00 sec)

ここで`{"foo": "bar"}`対象ドキュメントに含まれています。

```sql
SELECT JSON_CONTAINS('{"foo": "bar", "aaa": 5}','{"foo": "bar"}');
```

    +------------------------------------------------------------+
    | JSON_CONTAINS('{"foo": "bar", "aaa": 5}','{"foo": "bar"}') |
    +------------------------------------------------------------+
    |                                                          1 |
    +------------------------------------------------------------+
    1 row in set (0.00 sec)

ここで、 `"bar"`対象ドキュメントのルートに含まれていません。

```sql
SELECT JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"');
```

    +---------------------------------------------------+
    | JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"') |
    +---------------------------------------------------+
    |                                                 0 |
    +---------------------------------------------------+
    1 row in set (0.00 sec)

ここで、 `"bar"`対象ドキュメントの`$.foo`属性に含まれます。

```sql
SELECT JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"', '$.foo');
```

    +------------------------------------------------------------+
    | JSON_CONTAINS('{"foo": "bar", "aaa": 5}','"bar"', '$.foo') |
    +------------------------------------------------------------+
    |                                                          1 |
    +------------------------------------------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-contains-path">JSON_CONTAINS_PATH()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-search-functions-html-function-json-contains-path-json-contains-path-a}

`JSON_CONTAINS_PATH(json_doc, all_or_one, path [,path, ...])`関数は、JSON ドキュメントに指定されたパスのデータが含まれているかどうかを示す`0`または`1`返します。

例:

ここで文書には`$.foo`含まれます。

```sql
SELECT JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo');
```

    +--------------------------------------------------------------+
    | JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo') |
    +--------------------------------------------------------------+
    |                                                            1 |
    +--------------------------------------------------------------+
    1 row in set (0.00 sec)

ここではドキュメントに`$.bar`が含まれていません。

```sql
SELECT JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.bar');
```

    +--------------------------------------------------------------+
    | JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.bar') |
    +--------------------------------------------------------------+
    |                                                            0 |
    +--------------------------------------------------------------+
    1 row in set (0.00 sec)

ここで、ドキュメントには`$.foo`と`$.aaa`両方が含まれています。

```sql
SELECT JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo', '$.aaa');
```

    +-----------------------------------------------------------------------+
    | JSON_CONTAINS_PATH('{"foo": "bar", "aaa": 5}','all','$.foo', '$.aaa') |
    +-----------------------------------------------------------------------+
    |                                                                     1 |
    +-----------------------------------------------------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-extract">JSON_EXTRACT()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-search-functions-html-function-json-extract-json-extract-a}

`JSON_EXTRACT(json_doc, path[, path] ...)`関数は、 `path`引数に一致するドキュメントの部分から選択して、JSON ドキュメントからデータを抽出します。

```sql
SELECT JSON_EXTRACT('{"foo": "bar", "aaa": 5}', '$.foo');
```

    +---------------------------------------------------+
    | JSON_EXTRACT('{"foo": "bar", "aaa": 5}', '$.foo') |
    +---------------------------------------------------+
    | "bar"                                             |
    +---------------------------------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-column-path">-&gt;</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-search-functions-html-operator-json-column-path-a}

`column->path`関数は、 `path`引数に一致する`column`のデータを返します。これは[`JSON_EXTRACT()`](#json_extract)のエイリアスです。

```sql
SELECT
    j->'$.foo',
    JSON_EXTRACT(j, '$.foo')
FROM (
    SELECT
        '{"foo": "bar", "aaa": 5}' AS j
    ) AS tbl;
```

    +------------+--------------------------+
    | j->'$.foo' | JSON_EXTRACT(j, '$.foo') |
    +------------+--------------------------+
    | "bar"      | "bar"                    |
    +------------+--------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_json-inline-path">-&gt;&gt;</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-search-functions-html-operator-json-inline-path-a}

`column->>path`関数は、 `path`引数に一致する`column`内のデータを引用符で囲まないようにします。これは`JSON_UNQUOTE(JSON_EXTRACT(doc, path_literal))`のエイリアスです。

```sql
SELECT
    j->'$.foo',
    JSON_EXTRACT(j, '$.foo')
    j->>'$.foo',
    JSON_UNQUOTE(JSON_EXTRACT(j, '$.foo'))
FROM (
    SELECT
        '{"foo": "bar", "aaa": 5}' AS j
    ) AS tbl;
```

    +------------+--------------------------+-------------+----------------------------------------+
    | j->'$.foo' | JSON_EXTRACT(j, '$.foo') | j->>'$.foo' | JSON_UNQUOTE(JSON_EXTRACT(j, '$.foo')) |
    +------------+--------------------------+-------------+----------------------------------------+
    | "bar"      | "bar"                    | bar         | bar                                    |
    +------------+--------------------------+-------------+----------------------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-keys">JSON_KEYS()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-search-functions-html-function-json-keys-json-keys-a}

`JSON_KEYS(json_doc [,path])`関数は、JSONオブジェクトの最上位キーをJSON配列として返します。3 `path`が指定された場合は、選択されたパスの最上位キーを返します。

例:

次の例では、JSON ドキュメント内の 2 つの最上位キーを返します。

```sql
SELECT JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}');
```

    +---------------------------------------------------------------------------+
    | JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}') |
    +---------------------------------------------------------------------------+
    | ["name", "type"]                                                          |
    +---------------------------------------------------------------------------+
    1 row in set (0.00 sec)

次の例では、JSON ドキュメントの`$.name`のパスにある最上位キーを返します。

```sql
SELECT JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}', '$.name');
```

    +-------------------------------------------------------------------------------------+
    | JSON_KEYS('{"name": {"first": "John", "last": "Doe"}, "type": "Person"}', '$.name') |
    +-------------------------------------------------------------------------------------+
    | ["first", "last"]                                                                   |
    +-------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-search">JSON_SEARCH()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-search-functions-html-function-json-search-json-search-a}

`JSON_SEARCH(json_doc, one_or_all, str)`関数は、JSON ドキュメントで文字列の 1 つまたはすべての一致を検索します。

例:

次の例では、配列`a`のインデックス 2 の位置にある`cc`の最初の結果を検索できます。

```sql
SELECT JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','one','cc');
```

    +------------------------------------------------------------------------+
    | JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','one','cc') |
    +------------------------------------------------------------------------+
    | "$.a[2]"                                                               |
    +------------------------------------------------------------------------+
    1 row in set (0.00 sec)

ここで同じ操作を行いますが、最初の結果だけでなくすべての結果を取得するには、 `one_or_all`を`all`に設定します。

```sql
SELECT JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','all','cc');
```

    +------------------------------------------------------------------------+
    | JSON_SEARCH('{"a": ["aa", "bb", "cc"], "b": ["cc", "dd"]}','all','cc') |
    +------------------------------------------------------------------------+
    | ["$.a[2]", "$.b[0]"]                                                   |
    +------------------------------------------------------------------------+
    1 row in set (0.01 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#operator_member-of">メンバー()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-search-functions-html-operator-member-of-member-of-a}

`str MEMBER OF (json_array)`関数は、渡された値`str`が`json_array`の要素かどうかをテストし、 `1`返します。そうでない場合は`0`返します。引数のいずれかが`NULL`の場合は`NULL`返します。

    SELECT '🍍' MEMBER OF ('["🍍","🥥","🥭"]') AS 'Contains pineapple';

```
+--------------------+
| Contains pineapple |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.00 sec)

```

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html#function_json-overlaps">JSON_OVERLAPS()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-search-functions-html-function-json-overlaps-json-overlaps-a}

`JSON_OVERLAPS(json_doc, json_doc)`関数は、2つのJSONドキュメントに重複部分があるかどうかを示します。重複がある場合は`1` 、重複しない場合は`0`返します。引数のいずれかが`NULL`の場合は`NULL`返します。

例:

次の例では、配列値の要素数が同じではないため、重複がないことがわかります。

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust"]}'
) AS 'Overlaps';
```

    +----------+
    | Overlaps |
    +----------+
    |        0 |
    +----------+
    1 row in set (0.00 sec)

次の例は、両方の JSON ドキュメントが同一であるため重複していることを示しています。

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust","C#"]}'
) AS 'Overlaps';
```

    +----------+
    | Overlaps |
    +----------+
    |        1 |
    +----------+
    1 row in set (0.00 sec)

次の例では、重複があり、2 番目のドキュメントに追加の属性があることを示しています。

```sql
SELECT JSON_OVERLAPS(
    '{"languages": ["Go","Rust","C#"]}',
    '{"languages": ["Go","Rust","C#"], "arch": ["arm64"]}'
) AS 'Overlaps';
```

    +----------+
    | Overlaps |
    +----------+
    |        1 |
    +----------+
    1 row in set (0.00 sec)

## 参照 {#see-also}

-   [JSON関数の概要](/functions-and-operators/json-functions.md)
-   [JSONデータ型](/data-type-json.md)
