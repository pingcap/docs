---
title: AS_FLOAT
summary: 将 `VARIANT` 值严格转换为 DOUBLE 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中值的类型与输出值不匹配，则输出为 `NULL`。
---

# AS_FLOAT

将 `VARIANT` 值严格转换为 DOUBLE 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中值的类型与输出值不匹配，则输出为 `NULL`。

## 语法 {#syntax}

```sql
AS_FLOAT( <variant> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------|
| `<variant>` | VARIANT 值 |

## 返回类型 {#return-type}

DOUBLE

## 示例 {#examples}

```sql
SELECT as_float(parse_json('12.34'));
+-------------------------------+
| as_float(parse_json('12.34')) |
+-------------------------------+
| 12.34                         |
+-------------------------------+

SELECT as_float(parse_json('123'));
+-----------------------------+
| as_float(parse_json('123')) |
+-----------------------------+
| 123.0                       |
+-----------------------------+

-- 对于非数值类型，返回 NULL
SELECT as_float(parse_json('"abc"'));
+-------------------------------+
| as_float(parse_json('"abc"')) |
+-------------------------------+
| NULL                          |
+-------------------------------+
```