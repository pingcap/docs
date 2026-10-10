---
title: AS_STRING
summary: "`VARIANT` 値を VARCHAR データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。"
---

# AS_STRING

`VARIANT` 値を VARCHAR データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。

## 構文 {#syntax}

```sql
AS_STRING( <variant> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------|
| `<variant>` | VARIANT 値 |

## 戻り値の型 {#return-type}

VARCHAR

## 例 {#examples}

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