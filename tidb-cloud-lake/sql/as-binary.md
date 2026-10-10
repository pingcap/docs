---
title: AS_BINARY
summary: `VARIANT` 値を BINARY データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。
---

# AS_BINARY

`VARIANT` 値を BINARY データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。

## 構文 {#syntax}

```sql
AS_BINARY( <variant> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------|
| `<variant>` | VARIANT 値 |

## 戻り値の型 {#return-type}

BINARY

## 例 {#examples}

```sql
SELECT as_binary(to_binary('abcd')::variant);
+---------------------------------------+
| as_binary(to_binary('abcd')::variant) |
+---------------------------------------+
| 61626364                              |
+---------------------------------------+

SELECT as_binary(to_binary('hello')::variant);
+-----------------------------------------+
| as_binary(to_binary('hello')::variant) |
+-----------------------------------------+
| 68656C6C6F                              |
+-----------------------------------------+

-- Returns NULL for non-binary values
SELECT as_binary(parse_json('"text"'));
+---------------------------------+
| as_binary(parse_json('"text"')) |
+---------------------------------+
| NULL                            |
+---------------------------------+
```