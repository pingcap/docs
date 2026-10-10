---
title: AS_BOOLEAN
summary: "`VARIANT` 値を BOOLEAN データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。"
---

# AS_BOOLEAN

`VARIANT` 値を BOOLEAN データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。

## 構文 {#syntax}

```sql
AS_BOOLEAN( <variant> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------|
| `<variant>` | VARIANT 値 |

## 戻り値の型 {#return-type}

BOOLEAN

## 例 {#examples}

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

-- Returns NULL for non-boolean values
SELECT as_boolean(parse_json('123'));
+-------------------------------+
| as_boolean(parse_json('123')) |
+-------------------------------+
| NULL                          |
+-------------------------------+
```