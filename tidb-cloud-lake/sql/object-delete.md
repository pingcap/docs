---
title: OBJECT_DELETE
summary: JSON オブジェクトから指定したキーを削除し、変更後のオブジェクトを返します。指定したキーがオブジェクト内に存在しない場合は、無視されます。
---

# OBJECT_DELETE

JSON オブジェクトから指定したキーを削除し、変更後のオブジェクトを返します。指定したキーがオブジェクト内に存在しない場合は、無視されます。

## エイリアス {#aliases}

- `JSON_OBJECT_DELETE`

## 構文 {#syntax}

```sql
OBJECT_DELETE(<json_object>, <key1> [, <key2>, ...])
```

## パラメーター {#parameters}

| パラメーター | 説明 |
|-----------|-------------|
| json_object | キーを削除する対象の JSON オブジェクト（VARIANT 型）。 |
| key1, key2, ... | オブジェクトから削除するキーを表す、1 つ以上の文字列リテラル。 |

## 戻り値の型 {#return-type}

指定したキーが削除された、変更後の JSON オブジェクトを含む VARIANT を返します。

## 例 {#examples}

単一のキーを削除します。

```sql
SELECT OBJECT_DELETE('{"a":1,"b":2,"c":3}'::VARIANT, 'a');
-- Result: {"b":2,"c":3}
```

複数のキーを削除します。

```sql
SELECT OBJECT_DELETE('{"a":1,"b":2,"d":4}'::VARIANT, 'a', 'c');
-- Result: {"b":2,"d":4}
```

存在しないキーを削除します（キーは無視されます）。

```sql
SELECT OBJECT_DELETE('{"a":1,"b":2}'::VARIANT, 'x');
-- Result: {"a":1,"b":2}
```