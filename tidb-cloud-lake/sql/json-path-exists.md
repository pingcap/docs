---
title: JSON_PATH_EXISTS
summary: JSON データ内に指定したパスが存在するかどうかを確認します。
---

# JSON_PATH_EXISTS

JSON データ内に指定したパスが存在するかどうかを確認します。

## 構文 {#syntax}

```sql
JSON_PATH_EXISTS(<json_data>, <json_path_expression>)
```

- json_data: 検索対象の JSON データを指定します。JSON オブジェクトまたは配列を指定できます。

- json_path_expression: JSON データのルートを表す `$` から始まるパスを指定し、JSON データ内で確認したい対象を表します。式の中に条件を含めることもでき、その場合は `@` を使って現在評価中のノードまたは要素を参照し、結果を絞り込めます。

## 戻り値の型 {#return-type}

この関数は次の値を返します。

- 指定した JSON パス（条件がある場合はその条件を含む）が JSON データ内に存在する場合は `true`。
- 指定した JSON パス（条件がある場合はその条件を含む）が JSON データ内に存在しない場合は `false`。
- json_data または json_path_expression のいずれかが NULL または無効な場合は NULL。

## 例 {#examples}

```sql
SELECT JSON_PATH_EXISTS(parse_json('{"a": 1, "b": 2}'), '$.a ? (@ == 1)');

----
true

SELECT JSON_PATH_EXISTS(parse_json('{"a": 1, "b": 2}'), '$.a ? (@ > 1)');

----
false

SELECT JSON_PATH_EXISTS(NULL, '$.a');

----
NULL

SELECT JSON_PATH_EXISTS(parse_json('{"a": 1, "b": 2}'), NULL);

----
NULL
```