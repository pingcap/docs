---
title: JSON Utility Functions
summary: JSON ユーティリティ関数について学習します。
---

# JSONユーティリティ関数 {#json-utility-functions}

TiDB は、MySQL 8.0 で利用可能な[JSONユーティリティ関数](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html)すべてをサポートします。

## <code>JSON_PRETTY()</code> {#code-json-pretty-code}

`JSON_PRETTY(json_doc)`関数は JSON ドキュメントのフォーマットを整えます。

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

## <code>JSON_STORAGE_FREE()</code> {#code-json-storage-free-code}

`JSON_STORAGE_FREE(json_doc)`関数は、JSON 値がその場で更新された後にバイナリ表現で解放されるstorage容量を返します。

> **注記：**
>
> TiDBはMySQLとは異なるstorageアーキテクチャを採用しているため、この関数は有効なJSON値に対して常に`0`返します。これは[MySQL 8.0との互換性](/mysql-compatibility.md)で実装されています。TiDBはインプレース更新を行わないことに注意してください。詳細については[RocksDB のスペース使用量](/storage-engine/rocksdb-overview.md#rocksdb-space-usage)参照してください。

```sql
SELECT JSON_STORAGE_FREE('{}');
```

    +-------------------------+
    | JSON_STORAGE_FREE('{}') |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)

## <code>JSON_STORAGE_SIZE()</code> {#code-json-storage-size-code}

`JSON_STORAGE_SIZE(json_doc)`関数は、JSON 値を格納するために必要なバイト数の概算値を返します。このサイズは TiKV 圧縮を考慮していないため、この関数の出力は MySQL と厳密には互換性がありません。

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

-   [JSON関数の概要](/functions-and-operators/json-functions.md)
-   [JSONデータ型](/data-type-json.md)
