---
title: MAP_TRANSFORM_KEYS
summary: ラムダ式を使用して、JSON オブジェクト内の各キーに変換を適用します。
---

# MAP_TRANSFORM_KEYS

[ラムダ式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions)を使用して、JSON オブジェクト内の各キーに変換を適用します。

## 構文 {#syntax}

```sql
MAP_TRANSFORM_KEYS(<json_object>, (<key>, <value>) -> <key_transformation>)
```

## 戻り値の型 {#return-type}

入力 JSON オブジェクトと同じ値を持ち、指定したラムダ変換に従ってキーが変更された JSON オブジェクトを返します。

## 例 {#examples}

この例では、各キーに `"_v1"` を追加して、キーが変更された新しい JSON オブジェクトを作成します。

```sql
SELECT MAP_TRANSFORM_KEYS('{"name":"John", "role":"admin"}'::VARIANT, (k, v) -> CONCAT(k, '_v1')) AS versioned_metadata;

┌──────────────────────────────────────┐
│          versioned_metadata          │
├──────────────────────────────────────┤
│ {"name_v1":"John","role_v1":"admin"} │
└──────────────────────────────────────┘
```