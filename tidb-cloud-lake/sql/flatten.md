---
title: FLATTEN
summary: ネストされた JSON または配列データを表形式に変換し、各要素またはフィールドを個別の行として表します。
---

# FLATTEN

ネストされた JSON または配列データを表形式に変換し、各要素またはフィールドを個別の行として表します。

## 構文 {#syntax}

```sql
[LATERAL] FLATTEN (
  INPUT => <expr>
  [, PATH => <expr>]
  [, OUTER => TRUE | FALSE]
  [, RECURSIVE => TRUE | FALSE]
  [, MODE => 'OBJECT' | 'ARRAY' | 'BOTH']
)
```

## パラメータ {#parameters}

| Parameter | 説明 | デフォルト |
|-----------|-------------|---------|
| `INPUT` | フラット化する JSON または配列データ | Required |
| `PATH` | フラット化する配列/オブジェクトへのパス | None |
| `OUTER` | 結果が 0 件の行も含める（値は NULL） | `FALSE` |
| `RECURSIVE` | ネストされた要素をフラット化する | `FALSE` |
| `MODE` | オブジェクト、配列、またはその両方をフラット化する | `'BOTH'` |
| `LATERAL` | 先行するテーブル式との相互参照を有効にする | Optional |

## 出力カラム {#output-columns}

| Column | 説明 |
|--------|-------------|
| `SEQ` | 入力に対するシーケンス番号 |
| `KEY` | 展開された値のキー（存在しない場合は NULL） |
| `PATH` | フラット化された要素へのパス |
| `INDEX` | 配列インデックス（オブジェクトの場合は NULL） |
| `VALUE` | フラット化された要素の値 |
| `THIS` | フラット化対象の要素 |

**Note:** LATERAL を使用する場合、動的な相互参照により出力カラムが変わることがあります。

## 例 {#examples}

### 基本的なフラット化 {#basic-flattening}

```sql
-- Flatten a JSON object with nested structures
SELECT * FROM FLATTEN(
  INPUT => PARSE_JSON(
    '{"name": "John", "languages": ["English", "Spanish"], "address": {"city": "New York"}}'
  )
);
```

最上位レベルのキーがフラット化される結果になります。

```text
| seq | key       | path      | index | value                | this                 |
|-----|-----------|-----------|-------|----------------------|----------------------|
| 1   | name      | name      | NULL  | "John"               | {original JSON}      |
| 1   | languages | languages | NULL  | ["English","Spanish"]| {original JSON}      |
| 1   | address   | address   | NULL  | {"city":"New York"}  | {original JSON}      |
```

### PATH パラメータの使用 {#using-path-parameter}

```sql
-- Flatten only the languages array by specifying the PATH
SELECT * FROM FLATTEN(
  INPUT => PARSE_JSON(
    '{"name": "John", "languages": ["English", "Spanish"]}'
  ),
  PATH => 'languages'
);
```

配列要素がフラット化される結果になります。

```text
| seq | key  | path         | index | value     | this               |
|-----|------|--------------|-------|-----------|-------------------|
| 1   | NULL | languages[0] | 0     | "English" | ["English","Spanish"] |
| 1   | NULL | languages[1] | 1     | "Spanish" | ["English","Spanish"] |
```

### 再帰的なフラット化 {#recursive-flattening}

```sql
-- Recursively flatten nested objects and arrays
SELECT * FROM FLATTEN(
  INPUT => PARSE_JSON(
    '{"name": "John", "address": {"city": "New York", "zip": 10001}}'
  ),
  RECURSIVE => TRUE
);
```

ネストされたオブジェクトがフラット化される結果になります。

```text
| seq | key     | path         | index | value       | this            |
|-----|---------|--------------|-------|-------------|-----------------|
| 1   | name    | name         | NULL  | "John"      | {original JSON} |
| 1   | address | address      | NULL  | {"city":...}| {original JSON} |
| 1   | city    | address.city | NULL  | "New York"  | {"city":...}    |
| 1   | zip     | address.zip  | NULL  | 10001       | {"city":...}    |
```

### LATERAL FLATTEN の使用 {#using-lateral-flatten}

```sql
-- Use LATERAL FLATTEN to transform a JSON array into rows
-- This allows direct access to array elements without a table
SELECT
  f.value:item::STRING AS item_name,
  f.value:price::FLOAT AS price
FROM
  LATERAL FLATTEN(
    INPUT => PARSE_JSON('[
      {"item":"coffee", "price":2.50},
      {"item":"donut", "price":1.20}
    ]')
  ) f;
```

結果:

```text
| item_name | price |
|-----------|-------|
| coffee    | 2.5   |
| donut     | 1.2   |
```