---
title: JSON Functions That Modify JSON Values
summary: JSON 値を変更する JSON関数について学習します。
---

# JSON値を変更するJSON関数 {#json-functions-that-modify-json-values}

TiDB は、MySQL 8.0 で利用可能な[JSON値を変更するJSON関数](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html)すべてをサポートします。

## <code>JSON_APPEND()</code> {#code-json-append-code}

[`JSON_ARRAY_APPEND()`](#json_array_append)の別名。

## <code>JSON_ARRAY_APPEND()</code> {#code-json-array-append-code}

`JSON_ARRAY_APPEND(json_array, path, value [,path, value] ...)`関数は、JSON ドキュメント内の指定された配列の末尾に指定された`path`に値を追加し、結果を返します。

この関数は引数をペアで受け取ります。各ペアは`path`と`value`です。

例:

次の例では、JSON ドキュメントのルートである配列に項目を追加します。

```sql
SELECT JSON_ARRAY_APPEND('["Car", "Boat", "Train"]', '$', "Airplane") AS "Transport options";
```

    +--------------------------------------+
    | Transport options                    |
    +--------------------------------------+
    | ["Car", "Boat", "Train", "Airplane"] |
    +--------------------------------------+
    1 row in set (0.00 sec)

次の例では、指定されたパスの配列に項目を追加します。

```sql
SELECT JSON_ARRAY_APPEND('{"transport_options": ["Car", "Boat", "Train"]}', '$.transport_options', "Airplane") AS "Transport options";
```

    +-------------------------------------------------------------+
    | Transport options                                           |
    +-------------------------------------------------------------+
    | {"transport_options": ["Car", "Boat", "Train", "Airplane"]} |
    +-------------------------------------------------------------+
    1 row in set (0.00 sec)

## <code>JSON_ARRAY_INSERT()</code> {#code-json-array-insert-code}

`JSON_ARRAY_INSERT(json_array, path, value [,path, value] ...)`関数は、 `path`の`json_array`の指定された位置に`value`挿入し、結果を返します。

この関数は引数をペアで受け取ります。各ペアは`path`と`value`です。

例:

次の例では、配列のインデックス 0 の位置に値を挿入します。

```sql
SELECT JSON_ARRAY_INSERT('["Car", "Boat", "Train"]', '$[0]', "Airplane") AS "Transport options";
```

    +--------------------------------------+
    | Transport options                    |
    +--------------------------------------+
    | ["Airplane", "Car", "Boat", "Train"] |
    +--------------------------------------+
    1 row in set (0.01 sec)

次の例では、配列のインデックス 1 の位置に値を挿入します。

```sql
SELECT JSON_ARRAY_INSERT('["Car", "Boat", "Train"]', '$[1]', "Airplane") AS "Transport options";
```

    +--------------------------------------+
    | Transport options                    |
    +--------------------------------------+
    | ["Car", "Airplane", "Boat", "Train"] |
    +--------------------------------------+
    1 row in set (0.00 sec)

## <code>JSON_INSERT()</code> {#code-json-insert-code}

`JSON_INSERT(json_doc, path, value [,path, value] ...)`関数は、JSON ドキュメントに 1 つ以上の値を挿入し、結果を返します。

この関数は引数をペアで受け取ります。各ペアは`path`と`value`です。

```sql
SELECT JSON_INSERT(
    '{"language": ["Go", "Rust", "C++"]}',
    '$.architecture', 'riscv',
    '$.os', JSON_ARRAY("linux","freebsd")
) AS "Demo";
```

    +------------------------------------------------------------------------------------------+
    | Demo                                                                                     |
    +------------------------------------------------------------------------------------------+
    | {"architecture": "riscv", "language": ["Go", "Rust", "C++"], "os": ["linux", "freebsd"]} |
    +------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

この関数は既存の属性の値を上書きしないことに注意してください。例えば、次の文は属性`"a"`を上書きしているように見えますが、実際には上書きしません。

```sql
SELECT JSON_INSERT('{"a": 61, "b": 62}', '$.a', 41, '$.c', 63);
```

    +---------------------------------------------------------+
    | JSON_INSERT('{"a": 61, "b": 62}', '$.a', 41, '$.c', 63) |
    +---------------------------------------------------------+
    | {"a": 61, "b": 62, "c": 63}                             |
    +---------------------------------------------------------+
    1 row in set (0.00 sec)

## <code>JSON_MERGE_PATCH()</code> {#code-json-merge-patch-code}

`JSON_MERGE_PATCH(json_doc, json_doc [,json_doc] ...)`関数は、重複するキーの値を保持せずに、2つ以上のJSONドキュメントを1つのJSONドキュメントにマージします。重複するキーを持つ`json_doc`引数の場合、マージされた結果には、後に指定された`json_doc`引数の値のみが保持されます。

例:

次の例では、値`a`が引数 2 によって上書きされ、マージされた結果に`c`新しい属性として追加されていることがわかります。

```sql
SELECT JSON_MERGE_PATCH(
    '{"a": 1, "b": 2}',
    '{"a": 100}',
    '{"c": 300}'
);
```

    +-----------------------------------------------------------------+
    | JSON_MERGE_PATCH('{"a": 1, "b": 2}','{"a": 100}', '{"c": 300}') |
    +-----------------------------------------------------------------+
    | {"a": 100, "b": 2, "c": 300}                                    |
    +-----------------------------------------------------------------+
    1 row in set (0.00 sec)

## <code>JSON_MERGE_PRESERVE()</code> {#code-json-merge-preserve-code}

`JSON_MERGE_PRESERVE(json_doc, json_doc [,json_doc] ...)`関数は、各キーに関連付けられたすべての値を保持しながら 2 つ以上の JSON ドキュメントをマージし、マージされた結果を返します。

例:

次の例では、引数 2 の値が`a`に追加され、 `c`新しい属性として追加されていることがわかります。

```sql
SELECT JSON_MERGE_PRESERVE('{"a": 1, "b": 2}','{"a": 100}', '{"c": 300}');
```

    +--------------------------------------------------------------------+
    | JSON_MERGE_PRESERVE('{"a": 1, "b": 2}','{"a": 100}', '{"c": 300}') |
    +--------------------------------------------------------------------+
    | {"a": [1, 100], "b": 2, "c": 300}                                  |
    +--------------------------------------------------------------------+
    1 row in set (0.00 sec)

## <code>JSON_MERGE()</code> {#code-json-merge-code}

> **警告：**
>
> この機能は非推奨です。

[`JSON_MERGE_PRESERVE()`](#json_merge_preserve)の非推奨のエイリアス。

## <code>JSON_REMOVE()</code> {#code-json-remove-code}

`JSON_REMOVE(json_doc, path [,path] ...)`関数は、JSON ドキュメントから指定された`path`のデータを削除し、結果を返します。

例:

この例では、JSON ドキュメントから`b`属性を削除します。

```sql
SELECT JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b');
```

    +--------------------------------------------------+
    | JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b') |
    +--------------------------------------------------+
    | {"a": 61, "c": 63}                               |
    +--------------------------------------------------+
    1 row in set (0.00 sec)

この例では、JSON ドキュメントから`b`属性と`c`属性を削除します。

```sql
SELECT JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b','$.c');
```

    +--------------------------------------------------------+
    | JSON_REMOVE('{"a": 61, "b": 62, "c": 63}','$.b','$.c') |
    +--------------------------------------------------------+
    | {"a": 61}                                              |
    +--------------------------------------------------------+
    1 row in set (0.00 sec)

## <code>JSON_REPLACE()</code> {#code-json-replace-code}

`JSON_REPLACE(json_doc, path, value [, path, value] ...)`関数は、JSON ドキュメント内の指定されたパス内の値を置き換え、結果を返します。指定されたパスが存在しない場合、そのパスに対応する値は結果に追加されません。

この関数は引数をペアで受け取ります。各ペアは`path`と`value`です。

例:

次の例では、 `$.b`値を`62`から`42`に変更します。

```sql
SELECT JSON_REPLACE('{"a": 41, "b": 62}','$.b',42);
```

    +---------------------------------------------+
    | JSON_REPLACE('{"a": 41, "b": 62}','$.b',42) |
    +---------------------------------------------+
    | {"a": 41, "b": 42}                          |
    +---------------------------------------------+
    1 row in set (0.00 sec)

次の例では、 `$.b`値を`62`から`42`に変更できます。さらに、この文は`$.c`の値を`43`に置き換えようとしますが、 `$.c`パスが`{"a": 41, "b": 62}`に存在しないため、これは機能しません。

```sql
SELECT JSON_REPLACE('{"a": 41, "b": 62}','$.b',42,'$.c',43);
```

    +------------------------------------------------------+
    | JSON_REPLACE('{"a": 41, "b": 62}','$.b',42,'$.c',43) |
    +------------------------------------------------------+
    | {"a": 41, "b": 42}                                   |
    +------------------------------------------------------+
    1 row in set (0.00 sec)

## <code>JSON_SET()</code> {#code-json-set-code}

`JSON_SET(json_doc, path, value [,path, value] ...)`関数は、JSON ドキュメントにデータを挿入または更新し、結果を返します。

この関数は引数をペアで受け取ります。各ペアは`path`と`value`です。

例:

次の例では、 `$.version`を`1.1`から`1.2`に更新できます。

```sql
SELECT JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2);
```

    +-----------------------------------------------------------------+
    | JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2) |
    +-----------------------------------------------------------------+
    | {"name": "example", "version": 1.2}                             |
    +-----------------------------------------------------------------+
    1 row in set (0.00 sec)

次の例では、 `$.version`を`1.1`から`1.2`に更新できます。また、以前は存在しなかった`$.branch`を`main`に更新できます。

```sql
SELECT JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2,'$.branch', "main");
```

    +------------------------------------------------------------------------------------+
    | JSON_SET('{"version": 1.1, "name": "example"}','$.version',1.2,'$.branch', "main") |
    +------------------------------------------------------------------------------------+
    | {"branch": "main", "name": "example", "version": 1.2}                              |
    +------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

## <code>JSON_UNQUOTE()</code> {#code-json-unquote-code}

`JSON_UNQUOTE(json)`関数はJSON値の引用符を解除し、結果を文字列として返します。これは[`JSON_QUOTE()`](/functions-and-operators/json-functions/json-functions-create.md#json_quote)関数の逆の動作です。

例:

この例では、 `"foo"`は引用符で囲まれず`foo`になります。

```sql
SELECT JSON_UNQUOTE('"foo"');
```

    +-----------------------+
    | JSON_UNQUOTE('"foo"') |
    +-----------------------+
    | foo                   |
    +-----------------------+
    1 row in set (0.00 sec)

この関数は[`JSON_EXTRACT()`](/functions-and-operators/json-functions/json-functions-search.md#json_extract)と一緒に使用されることが多いです。以下の例では、最初の例では引用符付きのJSON値を抽出し、2番目の例では2つの関数を組み合わせて引用符を解除しています。3 `JSON_UNQUOTE(JSON_EXTRACT(...))`代わりに[`->>`](/functions-and-operators/json-functions/json-functions-search.md#--1)演算子を使用できることに注意してください。

```sql
SELECT JSON_EXTRACT('{"database": "TiDB"}', '$.database');
```

    +----------------------------------------------------+
    | JSON_EXTRACT('{"database": "TiDB"}', '$.database') |
    +----------------------------------------------------+
    | "TiDB"                                             |
    +----------------------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT JSON_UNQUOTE(JSON_EXTRACT('{"database": "TiDB"}', '$.database'));
```

    +------------------------------------------------------------------+
    | JSON_UNQUOTE(JSON_EXTRACT('{"database": "TiDB"}', '$.database')) |
    +------------------------------------------------------------------+
    | TiDB                                                             |
    +------------------------------------------------------------------+
    1 row in set (0.00 sec)

## 参照 {#see-also}

-   [JSON関数の概要](/functions-and-operators/json-functions.md)
-   [JSONデータ型](/data-type-json.md)
