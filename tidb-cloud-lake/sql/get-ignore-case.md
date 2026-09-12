---
title: GET_IGNORE_CASE
summary: 从包含 OBJECT 的 VARIANT 中按 field_name 提取值。如果任一参数为 NULL，则返回值为 Variant 或 NULL。
---

# GET_IGNORE_CASE

从包含 `OBJECT` 的 `VARIANT` 中按 field_name 提取值。如果任一参数为 `NULL`，则返回值为 `Variant` 或 `NULL`。

`GET_IGNORE_CASE` 与 `GET` 类似，但对字段名执行不区分大小写的匹配。首先匹配完全相同的字段名；如果未找到，则按字母顺序匹配不区分大小写的字段名。

## 语法 {#syntax}

```sql
GET_IGNORE_CASE( <variant>, <field_name> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|----------------|------------------------------------------------------------------|
| `<variant>`    | 包含 ARRAY 或 OBJECT 的 VARIANT 值 |
| `<field_name>` | 指定 OBJECT 键值对中键的字符串值 |

## 返回类型 {#return-type}

VARIANT

## 示例 {#examples}

```sql
SELECT get_ignore_case(parse_json('{"aa":1, "aA":2, "Aa":3}'), 'AA');
+---------------------------------------------------------------+
| get_ignore_case(parse_json('{"aa":1, "aA":2, "Aa":3}'), 'AA') |
+---------------------------------------------------------------+
| 3                                                             |
+---------------------------------------------------------------+
```