---
title: AS_INTEGER
summary: 将 `VARIANT` 值严格转换为 BIGINT 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。
---

# AS_INTEGER

将 `VARIANT` 值严格转换为 BIGINT 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。

## 语法 {#syntax}

```sql
AS_INTEGER( <variant> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------|
| `<variant>` | `VARIANT` 值 |

## 返回类型 {#return-type}

BIGINT

## 示例 {#examples}

```sql
SELECT as_integer(parse_json('123'));
+-------------------------------+
| as_integer(parse_json('123')) |
+-------------------------------+
| 123                           |
+-------------------------------+

SELECT as_integer(parse_json('-456'));
+--------------------------------+
| as_integer(parse_json('-456')) |
+--------------------------------+
| -456                           |
+--------------------------------+

-- Returns NULL for non-integer values
SELECT as_integer(parse_json('12.34'));
+---------------------------------+
| as_integer(parse_json('12.34')) |
+---------------------------------+
| NULL                            |
+---------------------------------+
```