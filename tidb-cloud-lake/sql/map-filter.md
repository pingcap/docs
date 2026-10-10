---
title: MAP_FILTER
summary: ラムダ式を使用して定義された指定条件に基づき、JSON オブジェクト内のキーと値のペアをフィルタリングします。
---

# MAP_FILTER

[ラムダ式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) を使用して定義された指定条件に基づき、JSON オブジェクト内のキーと値のペアをフィルタリングします。

## 構文 {#syntax}

```sql
MAP_FILTER(<json_object>, (<key>, <value>) -> <condition>)
```

## 戻り値の型 {#return-type}

指定した条件を満たすキーと値のペアのみを含む JSON オブジェクトを返します。

## 例 {#examples}

次の例では、JSON オブジェクトから `"status": "active"` のキーと値のペアのみを抽出し、他のフィールドを除外します。

```sql
SELECT MAP_FILTER('{"status":"active", "user":"admin", "time":"2024-11-01"}'::VARIANT, (k, v) -> k = 'status') AS filtered_metadata;

┌─────────────────────┐
│  filtered_metadata  │
├─────────────────────┤
│ {"status":"active"} │
└─────────────────────┘
```