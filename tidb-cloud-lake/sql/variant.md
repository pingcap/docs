---
title: Variant
summary: VARIANT は、NULL、BOOLEAN、NUMBER、STRING、ARRAY、OBJECT を含む任意の型の値を格納できます。また、内部の値は任意のレベルでネストした構造にできるため、さまざまなデータを柔軟に格納できます。VARIANT は JSON とも呼ばれます。詳細は JSON website を参照してください。
---

# Variant

VARIANT は、NULL、BOOLEAN、NUMBER、STRING、ARRAY、OBJECT を含む任意の型の値を格納できます。また、内部の値は任意のレベルでネストした構造にできるため、さまざまなデータを柔軟に格納できます。VARIANT は JSON とも呼ばれます。詳細は [JSON website](https://www.json.org/json-en.html) を参照してください。

以下は、{{{ .lake }}} で Variant データを挿入およびクエリする例です。

テーブルを作成します。

```sql
CREATE TABLE customer_orders(id INT64, order_data VARIANT);
```

異なる型の値をテーブルに挿入します。

```sql
INSERT INTO
  customer_orders
VALUES
  (
    1,
    '{"customer_id": 123, "order_id": 1001, "items": [{"name": "Shoes", "price": 59.99}, {"name": "T-shirt", "price": 19.99}]}'
  ),
  (
    2,
    '{"customer_id": 456, "order_id": 1002, "items": [{"name": "Backpack", "price": 79.99}, {"name": "Socks", "price": 4.99}]}'
  ),
  (
    3,
    '{"customer_id": 123, "order_id": 1003, "items": [{"name": "Shoes", "price": 59.99}, {"name": "Socks", "price": 4.99}]}'
  );
```

結果をクエリします。

```sql
SELECT * FROM customer_orders;
```

結果:

```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        id       │                                                   order_data                                                  │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│               1 │ {"customer_id":123,"items":[{"name":"Shoes","price":59.99},{"name":"T-shirt","price":19.99}],"order_id":1001} │
│               2 │ {"customer_id":456,"items":[{"name":"Backpack","price":79.99},{"name":"Socks","price":4.99}],"order_id":1002} │
│               3 │ {"customer_id":123,"items":[{"name":"Shoes","price":59.99},{"name":"Socks","price":4.99}],"order_id":1003}    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## JSON 内の要素へのアクセス {#accessing-elements-in-json}

### インデックスによるアクセス {#accessing-by-index}

VARIANT 型には配列を含めることができ、この配列は多くのプログラミング言語と同様に 0 ベースです。配列内の各要素も VARIANT 型です。要素には、**角括弧** を使用してインデックスでアクセスできます。

#### 例 {#example}

テーブルを作成します。

```sql
-- Create a table to store user hobbies
CREATE TABLE user_hobbies(user_id INT64, hobbies VARIANT NULL);
```

サンプルデータをテーブルに挿入します。

```sql
INSERT INTO user_hobbies
VALUES
    (1, '["Cooking", "Reading", "Cycling"]'),
    (2, '["Photography", "Travel", "Swimming"]');
```

各ユーザーの最初の趣味を取得します。

```sql
SELECT
  user_id,
  hobbies [0] AS first_hobby
FROM
  user_hobbies;
```

結果:

```sql
┌─────────────────────────────────────┐
│     user_id     │    first_hobby    │
├─────────────────┼───────────────────┤
│               1 │ "Cooking"         │
│               2 │ "Photography"     │
└─────────────────────────────────────┘
```

各ユーザーの 3 番目の趣味を取得します。

```sql
SELECT
  hobbies [2],
  count() AS third_hobby
FROM
  user_hobbies
GROUP BY
  hobbies [2];
```

結果:

```sql
┌─────────────────────────────────┐
│     hobbies[2]    │ third_hobby │
├───────────────────┼─────────────┤
│ "Swimming"        │           1 │
│ "Cycling"         │           1 │
└─────────────────────────────────┘
```

GROUP BY を使用して趣味を取得します。

```sql
SELECT
  hobbies [2],
  count() AS third_hobby
FROM
  user_hobbies
GROUP BY
  hobbies [2];
```

結果:

```sql
┌────────────┬─────────────┐
│ hobbies[2] │ third_hobby │
├────────────┼─────────────┤
│ "Cycling"  │           1 │
│ "Swimming" │           1 │
└────────────┴─────────────┘
```

### フィールド名によるアクセス {#accessing-by-field-name}

VARIANT 型には、オブジェクトとして表現されるキーと値のペアを含めることができます。各キーは VARCHAR、各値は VARIANT です。これは、他のプログラミング言語における「dictionary」、「hash」、「map」と同様に機能します。値には、**角括弧** または **コロン** を使用してフィールド名でアクセスできます。また、2 階層目以降では **ドット** も使用できます（テーブルとカラム間のドット記法との混同を避けるため、1 階層目の名前表記としてドットは使用できません）。

#### 例 {#example}

VARIANT 型でユーザー設定を保存するテーブルを作成します。

```sql
CREATE TABLE user_preferences(
  user_id INT64,
  preferences VARIANT NULL,
  profile Tuple(name STRING, age INT)
);
```

テーブルにサンプルデータを挿入します。

```sql
INSERT INTO
  user_preferences
VALUES
  (
    1,
    '{"settings":{"color":"red", "fontSize":16, "theme":"dark"}}',
    ('Amy', 12)
  ),
  (
    2,
    '{"settings":{"color":"blue", "fontSize":14, "theme":"light"}}',
    ('Bob', 11)
  );
```

各ユーザーの希望する色を取得します。

```sql
SELECT
  preferences['settings']['color'],
  preferences['settings']:color,
  preferences['settings'].color,
  preferences:settings['color'],
  preferences:settings:color,
  preferences:settings.color
FROM
  user_preferences;
```

結果:

```sql
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ preferences['settings']['color'] │ preferences['settings']:color │ preferences['settings']:color │ preferences:settings['color'] │ preferences:settings:color │ preferences:settings:color │
├──────────────────────────────────┼───────────────────────────────┼───────────────────────────────┼───────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ "red"                            │ "red"                         │ "red"                         │ "red"                         │ "red"                      │ "red"                      │
│ "blue"                           │ "blue"                        │ "blue"                        │ "blue"                        │ "blue"                     │ "blue"                     │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

フィールド名は **case-sensitive** であることに注意してください。フィールド名にスペースや特殊文字が含まれる場合は、二重引用符で囲みます。

```sql
INSERT INTO
  user_preferences
VALUES
  (
    3,
    '{"new settings":{"color":"red", "fontSize":16, "theme":"dark"}}',
    ('Cole', 13)
  );

-- Double-quote the field name "new settings"
SELECT preferences:"new settings":color
FROM user_preferences;

┌──────────────────────────────────┐
│ preferences:"new settings":color │
├──────────────────────────────────┤
│ NULL                             │
│ NULL                             │
│ "red"                            │
└──────────────────────────────────┘

-- No results are returned when 'c' in 'color' is capitalized
SELECT preferences:"new settings":Color
FROM user_preferences;

┌──────────────────────────────────┐
│ preferences:"new settings":color │
│         Nullable(Variant)        │
├──────────────────────────────────┤
│ NULL                             │
│ NULL                             │
│ NULL                             │
└──────────────────────────────────┘
```

## データ型変換 {#data-type-conversion}

デフォルトでは、VARIANT カラムから取得された要素がそのまま返されます。返された要素を特定の型に変換するには、`::` 演算子と対象のデータ型（例: expression::type）を追加します。

VARIANT カラムでユーザー設定を保存するテーブルを作成します。

```sql
CREATE TABLE user_pref(user_id INT64, pref VARIANT NULL);
```

テーブルにサンプルデータを挿入します。

```sql
INSERT INTO user_pref
VALUES
    (1, parse_json('{"age": 25, "isPremium": "true", "lastActive": "2023-04-10"}')),
    (2, parse_json('{"age": 30, "isPremium": "false", "lastActive": "2023-03-15"}'));
```

age を INT64 に変換します。

```sql
SELECT user_id, pref:age::INT64 as age FROM user_pref;
```

結果:

```sql
┌─────────┬─────┐
│ user_id │ age │
├─────────┼─────┤
│       1 │  25 │
│       2 │  30 │
└─────────┴─────┘
```

## JSON 関数 {#json-functions}

[Variant Functions](/tidb-cloud-lake/sql/structured-semi-structured-functions.md) を参照してください。