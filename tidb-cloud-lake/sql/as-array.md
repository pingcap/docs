---
title: AS_ARRAY
summary: 将 `VARIANT` 值严格转换为 ARRAY 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。
---

# AS_ARRAY

将 `VARIANT` 值严格转换为 ARRAY 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。

## 语法 {#syntax}

```sql
AS_ARRAY( <variant> )
```

## 参数 {#arguments}

| 参数        | 描述 |
|-------------|------|
| `<variant>` | `VARIANT` 值 |

## 返回类型 {#return-type}

Variant 包含 Array

## 示例 {#examples}

```sql
SELECT as_array(parse_json('[1,2,3]'));
+---------------------------------+
| as_array(parse_json('[1,2,3]')) |
+---------------------------------+
| [1,2,3]                         |
+---------------------------------+

SELECT as_array(parse_json('["a","b","c"]'));
+---------------------------------------+
| as_array(parse_json('["a","b","c"]')) |
+---------------------------------------+
| ["a","b","c"]                         |
+---------------------------------------+

-- Returns NULL for non-array values
SELECT as_array(parse_json('{"key":"value"}'));
+-----------------------------------------+
| as_array(parse_json('{"key":"value"}')) |
+-----------------------------------------+
| NULL                                    |
+-----------------------------------------+
```