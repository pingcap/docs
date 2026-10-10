---
title: IS_ARRAY
summary: 入力値が JSON 配列かどうかを確認します。JSON 配列は ARRAY データ型と同じではないことに注意してください。JSON 配列は JSON で一般的に使用されるデータ構造で、角括弧 [] で囲まれた順序付きの値のコレクションを表します。文字列、数値、ブール値、オブジェクト、null など、さまざまなデータ型を整理および交換するための柔軟な形式です。
---

# IS_ARRAY

入力値が JSON 配列かどうかを確認します。JSON 配列は [ARRAY](/tidb-cloud-lake/sql/array.md) データ型と同じではないことに注意してください。JSON 配列は JSON で一般的に使用されるデータ構造で、角括弧 `[ ]` で囲まれた順序付きの値のコレクションを表します。文字列、数値、ブール値、オブジェクト、null など、さまざまなデータ型を整理および交換するための柔軟な形式です。

```json title='JSON Array Example:'
[
  "Apple",
  42,
  true,
  {"name": "John", "age": 30, "isStudent": false},
  [1, 2, 3],
  null
]
```

## 構文 {#syntax}

```sql
IS_ARRAY( <expr> )
```

## 戻り値の型 {#return-type}

入力値が JSON 配列の場合は `true` を返し、それ以外の場合は `false` を返します。

## 例 {#examples}

```sql
SELECT
  IS_ARRAY(PARSE_JSON('true')),
  IS_ARRAY(PARSE_JSON('[1,2,3]'));

┌────────────────────────────────────────────────────────────────┐
│ is_array(parse_json('true')) │ is_array(parse_json('[1,2,3]')) │
├──────────────────────────────┼─────────────────────────────────┤
│ false                        │ true                            │
└────────────────────────────────────────────────────────────────┘
```