---
title: JSON Utility Functions
summary: Learn about JSON utility functions.
---

# JSON 实用函数

TiDB 支持 MySQL 8.0 中所有的 [JSON 实用函数](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html)。

## `JSON_PRETTY()`

`JSON_PRETTY(json_doc)` 函数用于对 JSON 文档进行美化格式化。

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

`JSON_STORAGE_FREE(json_doc)` 函数返回在原地更新 JSON 值后，其二进制表示中释放的存储空间大小。

> **Note:**
>
> 由于 TiDB 的存储架构与 MySQL 不同，该函数对于有效的 JSON 值始终返回 `0`，其实现是为了 [兼容 MySQL 8.0](/mysql-compatibility.md)。需要注意的是，TiDB 不支持原地更新。更多信息请参见 [RocksDB 空间使用](/storage-engine/rocksdb-overview.md#rocksdb-space-usage)。

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

`JSON_STORAGE_SIZE(json_doc)` 函数返回存储该 JSON 值所需的字节数的近似值。由于该大小未考虑 TiKV 的压缩机制，因此该函数的输出与 MySQL 并不完全兼容。

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

## 另请参阅

- [JSON 函数概览](/functions-and-operators/json-functions.md)
- [JSON 数据类型](/data-type-json.md)