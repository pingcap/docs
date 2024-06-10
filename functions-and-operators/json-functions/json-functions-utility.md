---
title: Utility JSON Functions
summary: Learn about JSON utility functions.
---

## [JSON_PRETTY()](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-pretty)

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

## [JSON_STORAGE_FREE()](https://dev.mysql.com/doc/refman/8.0/en/json-utility-functions.html#function_json-storage-free)

The `JSON_STORAGE_FREE(json_doc)` function returns how much storage space was freed in the binary representation of the JSON value after it was updated in place. 

> **Note:**
>
> As TiDB has different storage architecture from MySQL, this function always returns 0 for a valid JSON value, and it is implemented for [compatibility with MySQL 8.0](/mysql-compatibility.md).

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

The `JSON_STORAGE_SIZE(json_doc)` function returns an approximate size of bytes required to store the json value. As the size does not account for TiKV using compression, the output of this function is not strictly compatible with MySQL.

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