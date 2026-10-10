---
title: GET_BY_KEYPATH
summary: キーパス文字列を使用して `VARIANT` からネストされた値を抽出します。`GET_BY_KEYPATH` は結果を `VARIANT` として返し、`GET_BY_KEYPATH_STRING` は `STRING` として返します。
---

# GET_BY_KEYPATH

**キーパス**文字列を使用して `VARIANT` からネストされた値を抽出します。`GET_BY_KEYPATH` は結果を `VARIANT` として返し、`GET_BY_KEYPATH_STRING` は `STRING` として返します。

キーパスは Postgres スタイルの波かっこ構文に従います。各セグメントは `{}` で囲まれ、セグメントはカンマで区切られます。たとえば `'{user,profile,name}'` のように指定します。配列インデックスは数値で指定できます。たとえば `'{items,0}'` です。

## 構文 {#syntax}

```sql
GET_BY_KEYPATH(<variant>, <keypath>)
GET_BY_KEYPATH_STRING(<variant>, <keypath>)
```

## 戻り値の型 {#return-type}

- `GET_BY_KEYPATH`: `VARIANT`
- `GET_BY_KEYPATH_STRING`: `STRING`

## 例 {#examples}

```sql
SELECT GET_BY_KEYPATH(PARSE_JSON('{"user":{"name":"Ada","tags":["a","b"]}}'), '{user,name}') AS profile_name;

┌──────────────┐
│ profile_name │
├──────────────┤
│ "Ada"        │
└──────────────┘
```

```sql
SELECT GET_BY_KEYPATH(PARSE_JSON('[10, {"a":{"k1":[1,2,3]}}]'), '{1,a,k1}') AS inner_array;

┌─────────────┐
│ inner_array │
├─────────────┤
│ [1,2,3]     │
└─────────────┘
```

```sql
SELECT GET_BY_KEYPATH_STRING(PARSE_JSON('{"user":{"name":"Ada"}}'), '{user,name}') AS name_text;

┌──────────┐
│ name_text│
├──────────┤
│ Ada      │
└──────────┘
```

```sql
SELECT GET_BY_KEYPATH_STRING(PARSE_JSON('[10, {"scores":[100,98]}]'), '{1,scores,0}') AS first_score;

┌──────────────┐
│ first_score  │
├──────────────┤
│ 100          │
└──────────────┘
```

キーパスを解決できない場合、どちらの関数も `NULL` を返します。