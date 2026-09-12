---
title: AS_STRING
summary: 将 `VARIANT` 值严格转换为 VARCHAR 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中值的类型与输出值不匹配，则输出为 `NULL`。
---

# AS_STRING

将 `VARIANT` 值严格转换为 VARCHAR 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中值的类型与输出值不匹配，则输出为 `NULL`。

## 语法 {#syntax}

```sql
AS_STRING( <variant> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------|
| `<variant>` | `VARIANT` 值 |

## 返回类型 {#return-type}

VARCHAR

## 示例 {#examples}

```sql
SELECT as_string(parse_json('"abc"'));
+--------------------------------+
| as_string(parse_json('"abc"')) |
+--------------------------------+
| abc                            |
+--------------------------------+

SELECT as_string(parse_json('"hello world"'));
+----------------------------------------+
| as_string(parse_json('"hello world"')) |
+----------------------------------------+
| hello world                            |
+----------------------------------------+

-- Returns NULL for non-string values
SELECT as_string(parse_json('123'));
+------------------------------+
| as_string(parse_json('123')) |
+------------------------------+
| NULL                         |
+------------------------------+
```