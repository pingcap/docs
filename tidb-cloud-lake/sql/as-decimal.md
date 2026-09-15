---
title: AS_DECIMAL
summary: 将 `VARIANT` 值严格转换为 DECIMAL 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。
---

# AS_DECIMAL

将 `VARIANT` 值严格转换为 DECIMAL 数据类型。如果输入数据类型不是 `VARIANT`，则输出为 `NULL`。如果 `VARIANT` 中的值类型与输出值不匹配，则输出为 `NULL`。

## 语法 {#syntax}

```sql
AS_DECIMAL( <variant> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------|
| `<variant>` | `VARIANT` 值 |

## 返回类型 {#return-type}

DECIMAL

## 示例 {#examples}

```sql
SELECT as_decimal(parse_json('12.34'));
+---------------------------------+
| as_decimal(parse_json('12.34')) |
+---------------------------------+
| 12.34                           |
+---------------------------------+

SELECT as_decimal(parse_json('123.456789'));
+--------------------------------------+
| as_decimal(parse_json('123.456789')) |
+--------------------------------------+
| 123.456789                           |
+--------------------------------------+

-- Returns NULL for non-decimal values
SELECT as_decimal(parse_json('"abc"'));
+---------------------------------+
| as_decimal(parse_json('"abc"')) |
+---------------------------------+
| NULL                            |
+---------------------------------+
```