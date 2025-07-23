---
title: JSON Utility Functions
summary: 了解 JSON 工具函数。
---

# JSON Utility Functions

本文档描述了 JSON 工具函数。

## [JSON_PRETTY()](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-pretty)

`JSON_PRETTY(json_doc)` 函数对 JSON 文档进行美化格式化。

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

## [JSON_STORAGE_FREE()](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free)

`JSON_STORAGE_FREE(json_doc)` 函数返回在就地更新后，二进制表示的 JSON 值释放的存储空间大小（以字节为单位）。

> **注意：**
>
> 由于 TiDB 的存储架构与 MySQL 不同，此函数对于有效的 JSON 值总是返回 `0`，并且它是为了 [兼容 MySQL 8.0](/mysql-compatibility.md) 而实现的。请注意，TiDB 不进行就地更新。更多信息请参见 [RocksDB 空间使用情况](/storage-engine/rocksdb-overview.md#rocksdb-space-usage)。

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

## [JSON_STORAGE_SIZE()](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-size)

`JSON_STORAGE_SIZE(json_doc)` 函数返回存储 JSON 值所需的近似字节数。由于此大小未考虑 TiKV 使用压缩，故此函数的输出与 MySQL 不完全兼容。

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

## 相关链接

- [JSON Functions Overview](/functions-and-operators/json-functions.md)
- [JSON Data Type](/data-type-json.md)