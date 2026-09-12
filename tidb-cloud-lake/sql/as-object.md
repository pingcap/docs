---
title: AS_OBJECT
summary: 将 `VARIANT` 值严格转换为 OBJECT 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。
---

# AS_OBJECT

将 `VARIANT` 值严格转换为 OBJECT 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。

## 语法 {#syntax}

```sql
AS_OBJECT( <variant> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------|
| `<variant>` | `VARIANT` 值 |

## 返回类型 {#return-type}

Variant 包含 Object

## 示例 {#examples}

```sql
SELECT as_object(parse_json('{"k":"v","a":"b"}'));
+--------------------------------------------+
| as_object(parse_json('{"k":"v","a":"b"}')) |
+--------------------------------------------+
| {"k":"v","a":"b"}                          |
+--------------------------------------------+

SELECT as_object(parse_json('{"name":"John","age":30}'));
+-----------------------------------------------+
| as_object(parse_json('{"name":"John","age":30}')) |
+-----------------------------------------------+
| {"name":"John","age":30}                      |
+-----------------------------------------------+

-- Returns NULL for non-object values
SELECT as_object(parse_json('[1,2,3]'));
+----------------------------------+
| as_object(parse_json('[1,2,3]')) |
+----------------------------------+
| NULL                             |
+----------------------------------+
```