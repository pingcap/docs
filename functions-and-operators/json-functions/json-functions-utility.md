---
title: JSON Utility Functions
summary: JSON ユーティリティ関数について学習します。
---

# JSON ユーティリティ関数 {#json-utility-functions}

このドキュメントでは、JSON ユーティリティ関数について説明します。

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-pretty">JSON_PRETTY()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-utility-functions-html-function-json-pretty-json-pretty-a}

`JSON_PRETTY(json_doc)`関数は JSON ドキュメントをきれいにフォーマットします。

```sql
SELECT JSON_PRETTY('{"person":{"name":{"first":"John","last":"Doe"},"age":23}}')\G
```

    *************************** 1. row ***************************
    JSON_PRETTY('{"person":{"name":{"first":"John","last":"Doe"},"age":23}}'): {
      "person": {
        "age": 23,
        "name": {
          "first": "John",
          "last": "Doe"
        }
      }
    }
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free">JSON_STORAGE_FREE()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-utility-functions-html-function-json-storage-free-json-storage-free-a}

`JSON_STORAGE_FREE(json_doc)`関数は、JSON 値がその場で更新された後に、バイナリ表現で解放されるstorage容量を返します。

> **注記：**
>
> TiDB は MySQL とは異なるstorageアーキテクチャを持っているため、この関数は有効な JSON 値に対して常に`0`を返し、 [MySQL 8.0との互換性](/mysql-compatibility.md)用に実装されています。TiDB はインプレース更新を行わないことに注意してください。詳細については、 [RocksDB のスペース使用量](/storage-engine/rocksdb-overview.md#rocksdb-space-usage)参照してください。

```sql
SELECT JSON_STORAGE_FREE('{}');
```

    +-------------------------+
    | JSON_STORAGE_FREE('{}') |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)

## <a href="https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-size">JSON_STORAGE_SIZE()</a> {#a-href-https-dev-mysql-com-doc-refman-8-0-en-json-utility-functions-html-function-json-storage-size-json-storage-size-a}

`JSON_STORAGE_SIZE(json_doc)`関数は、JSON 値を格納するために必要なバイトのおおよそのサイズを返します。サイズは圧縮を使用する TiKV を考慮していないため、この関数の出力は MySQL と厳密には互換性がありません。

```sql
SELECT JSON_STORAGE_SIZE('{}');
```

    +-------------------------+
    | JSON_STORAGE_SIZE('{}') |
    +-------------------------+
    |                       9 |
    +-------------------------+
    1 row in set (0.00 sec)

## 参照 {#see-also}

-   [JSON 関数の概要](/functions-and-operators/json-functions.md)
-   [JSON データ型](/data-type-json.md)
