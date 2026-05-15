---
title: JSON Utility Functions
summary: Learn about JSON utility functions.
---

# JSON Utility Functions

TiDB supports all the [JSON utility functions](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html) available in MySQL 8.0.

## `JSON_PRETTY()`

The `JSON_PRETTY(json_doc)` function does pretty formatting of a JSON document.

```sql
SELECT JSON_PRETTY('{"person":{"name":{"first":"John","last":"Doe"},"age":23}}')\G
```

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
```

## `JSON_STORAGE_FREE()`

The `JSON_STORAGE_FREE(json_doc)` function returns how much storage space is freed in the binary representation of the JSON value after it is updated in place. 

> **Note:**
>
> Because TiDB has a different storage architecture from MySQL, this function always returns `0` for a valid JSON value, and it is implemented for [compatibility with MySQL 8.0](/mysql-compatibility.md). Note that TiDB does not do in-place updates. For more information, see [RocksDB space usage](/storage-engine/rocksdb-overview.md#rocksdb-space-usage).

```sql
SELECT JSON_STORAGE_FREE('{}');
```

```
+-------------------------+
| JSON_STORAGE_FREE('{}') |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.00 sec)
```

## `JSON_STORAGE_SIZE()`

The `JSON_STORAGE_SIZE(json_doc)` function returns an approximate size of bytes required to store the JSON value. Because the size does not account for TiKV using compression, the output of this function is not strictly compatible with MySQL.

```sql
SELECT JSON_STORAGE_SIZE('{}');
```

```
+-------------------------+
| JSON_STORAGE_SIZE('{}') |
+-------------------------+
|                       9 |
+-------------------------+
1 row in set (0.00 sec)
```

## See also

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)