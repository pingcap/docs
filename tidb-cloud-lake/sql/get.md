---
title: GET
summary: 从包含 ARRAY 的 Variant 中按索引提取值，或从包含 OBJECT 的 Variant 中按 field_name 提取值。如果任一参数为 NULL，则返回的值为 Variant 或 NULL。
---

# GET

从包含 `ARRAY` 的 `Variant` 中按 `index` 提取值，或从包含 `OBJECT` 的 `Variant` 中按 `field_name` 提取值。如果任一参数为 `NULL`，则返回的值为 `Variant` 或 `NULL`。

`GET` 对 `field_name` 采用大小写敏感匹配。若要进行大小写不敏感匹配，请使用 `GET_IGNORE_CASE`。

## 语法 {#syntax}

```sql
GET( <variant>, <index> )

GET( <variant>, <field_name> )
```

## 参数 {#arguments}

| 参数 | 描述 |
|----------------|------------------------------------------------------------------|
| `<variant>`    | 包含 ARRAY 或 OBJECT 的 VARIANT 值 |
| `<index>`      | Uint32 值，指定 ARRAY 中值的位置 |
| `<field_name>` | String 值，指定 OBJECT 中键值对的键 |

## 返回类型 {#return-type}

VARIANT

## 示例 {#examples}

```sql
SELECT get(parse_json('[2.71, 3.14]'), 0);
+------------------------------------+
| get(parse_json('[2.71, 3.14]'), 0) |
+------------------------------------+
| 2.71                               |
+------------------------------------+

SELECT get(parse_json('{"aa":1, "aA":2, "Aa":3}'), 'aa');
+---------------------------------------------------+
| get(parse_json('{"aa":1, "aA":2, "Aa":3}'), 'aa') |
+---------------------------------------------------+
| 1                                                 |
+---------------------------------------------------+

SELECT get(parse_json('{"aa":1, "aA":2, "Aa":3}'), 'AA');
+---------------------------------------------------+
| get(parse_json('{"aa":1, "aA":2, "Aa":3}'), 'AA') |
+---------------------------------------------------+
| NULL                                              |
+---------------------------------------------------+
```