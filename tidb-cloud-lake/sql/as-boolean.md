---
title: AS_BOOLEAN
summary: 将 `VARIANT` 值严格转换为 BOOLEAN 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。
---

# AS_BOOLEAN

将 `VARIANT` 值严格转换为 BOOLEAN 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。

## 语法 {#syntax}

```sql
AS_BOOLEAN( <variant> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------|
| `<variant>` | `VARIANT` 值 |

## 返回类型 {#return-type}

BOOLEAN

## 示例 {#examples}

```sql
SELECT as_boolean(parse_json('true'));
+--------------------------------+
| as_boolean(parse_json('true')) |
+--------------------------------+
| 1                              |
+--------------------------------+

SELECT as_boolean(parse_json('false'));
+---------------------------------+
| as_boolean(parse_json('false')) |
+---------------------------------+
| 0                               |
+---------------------------------+

-- 对于非布尔值，返回 NULL
SELECT as_boolean(parse_json('123'));
+-------------------------------+
| as_boolean(parse_json('123')) |
+-------------------------------+
| NULL                          |
+-------------------------------+
```