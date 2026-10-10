---
title: JQ
summary: JQ 関数は、Variant カラムに格納された JSON データに jq フィルタを適用できる、集合を返す SQL 関数です。この関数を使用すると、指定した jq フィルタを適用して JSON データを処理し、その結果を行の集合として返すことができます。
---

# JQ

JQ 関数は、Variant カラムに格納された JSON データに [jq](https://jqlang.github.io/jq/) フィルタを適用できる、集合を返す SQL 関数です。この関数を使用すると、指定した jq フィルタを適用して JSON データを処理し、その結果を行の集合として返すことができます。

## 構文 {#syntax}

```sql
JQ (<jq_expression>, <json_data>)
```

| Parameter       | 説明 |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `jq_expression` | `jq` 構文を使用して JSON データをどのように処理および変換するかを定義する `jq` フィルタ式です。この式では、JSON オブジェクトや配列内のデータをどのように選択、変更、操作するかを指定できます。jq でサポートされる構文、フィルタ、および関数については、[jq Manual](https://jqlang.github.io/jq/manual/#basic-filters) を参照してください。 |
| `json_data`     | `jq` フィルタ式を使用して処理または変換したい JSON 形式の入力です。JSON オブジェクト、配列、または任意の有効な JSON データ構造を指定できます。 |

## 戻り値の型 {#return-type}

JQ 関数は JSON 値の集合を返します。各値は、`<jq_expression>` に基づいて変換または抽出された結果の要素に対応します。

## 例 {#examples}

まず、`id` と `profile` のカラムを持つ `customer_data` という名前のテーブルを作成します。`profile` はユーザー情報を格納するための JSON 型です。

```sql
CREATE TABLE customer_data (
    id INT,
    profile JSON
);

INSERT INTO customer_data VALUES
    (1, '{"name": "Alice", "age": 30, "city": "New York"}'),
    (2, '{"name": "Bob", "age": 25, "city": "Los Angeles"}'),
    (3, '{"name": "Charlie", "age": 35, "city": "Chicago"}');
```

次の例では、JSON データから特定のフィールドを抽出します。

```sql
SELECT
    id,
    jq('.name', profile) AS customer_name
FROM
    customer_data;

┌─────────────────────────────────────┐
│        id       │   customer_name   │
├─────────────────┼───────────────────┤
│               1 │ "Alice"           │
│               2 │ "Bob"             │
│               3 │ "Charlie"         │
└─────────────────────────────────────┘
```

次の例では、各ユーザーについてユーザー ID と 1 増やした年齢を選択します。

```sql
SELECT
    id,
    jq('.age + 1', profile) AS updated_age
FROM
    customer_data;

┌─────────────────────────────────────┐
│        id       │    updated_age    │
├─────────────────┼───────────────────┤
│               1 │ 31                │
│               2 │ 26                │
│               3 │ 36                │
└─────────────────────────────────────┘
```

次の例では、都市名を大文字に変換します。

```sql
SELECT
    id,
    jq('.city | ascii_upcase', profile) AS city_uppercase
FROM
    customer_data;

┌─────────────────────────────────────┐
│        id       │   city_uppercase  │
├─────────────────┼───────────────────┤
│               1 │ "NEW YORK"        │
│               2 │ "LOS ANGELES"     │
│               3 │ "CHICAGO"         │
└─────────────────────────────────────┘
```