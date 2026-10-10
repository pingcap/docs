---
title: GET_IGNORE_CASE
summary: OBJECT を含む VARIANT から、field_name によって値を抽出します。いずれかの引数が NULL の場合、値は Variant または NULL として返されます。
---

# GET_IGNORE_CASE

`OBJECT` を含む `VARIANT` から、field_name によって値を抽出します。いずれかの引数が `NULL` の場合、値は `Variant` または `NULL` として返されます。

`GET_IGNORE_CASE` は `GET` に似ていますが、フィールド名の照合に大文字と小文字を区別しないマッチングを適用します。まず完全に同一のフィールド名を照合し、見つからない場合は、大文字と小文字を区別しないフィールド名をアルファベット順で照合します。

## 構文 {#syntax}

```sql
GET_IGNORE_CASE( <variant>, <field_name> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|----------------|------------------------------------------------------------------|
| `<variant>`    | ARRAY または OBJECT のいずれかを含む VARIANT 値 |
| `<field_name>` | OBJECT のキーと値のペアにおけるキーを指定する String 値 |

## 戻り値の型 {#return-type}

VARIANT

## 例 {#examples}

```sql
SELECT get_ignore_case(parse_json('{"aa":1, "aA":2, "Aa":3}'), 'AA');
+---------------------------------------------------------------+
| get_ignore_case(parse_json('{"aa":1, "aA":2, "Aa":3}'), 'AA') |
+---------------------------------------------------------------+
| 3                                                             |
+---------------------------------------------------------------+
```