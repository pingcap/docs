---
title: データ型
summary: "{{{ .lake }}} は強い型付けを持つカラムにデータを格納します。このページでは、サポートされるデータ型、自動変換および明示的変換の仕組み、NULL 値やデフォルト値の扱いについて要約します。"
---

# データ型

{{{ .lake }}} は強い型付けを持つカラムにデータを格納します。このページでは、サポートされるデータ型、自動変換および明示的変換の仕組み、NULL 値やデフォルト値の扱いについて要約します。

## 基本型 {#foundational-types}

| データ型                                   | エイリアス      | ストレージ / 精度              | 最小値                | 最大値                      |
|--------------------------------------------|------------|-----------------------------------|--------------------------|--------------------------------|
| [BOOLEAN](/tidb-cloud-lake/sql/boolean.md)                      | BOOL       | 1 バイト                          | –                        | –                              |
| [BINARY](/tidb-cloud-lake/sql/binary.md)                        | VARBINARY  | 可変                          | –                        | –                              |
| [VARCHAR](/tidb-cloud-lake/sql/string.md)                       | STRING     | 可変                          | –                        | –                              |
| [TINYINT](/tidb-cloud-lake/sql/numeric.md#integer-data-types)   | INT8       | 1 バイト                          | -128                     | 127                            |
| [SMALLINT](/tidb-cloud-lake/sql/numeric.md#integer-data-types)  | INT16      | 2 バイト                          | -32768                   | 32767                          |
| [INT](/tidb-cloud-lake/sql/numeric.md#integer-data-types)       | INT32      | 4 バイト                          | -2147483648              | 2147483647                     |
| [BIGINT](/tidb-cloud-lake/sql/numeric.md#integer-data-types)    | INT64      | 8 バイト                          | -9223372036854775808     | 9223372036854775807            |
| [FLOAT](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) | –        | 4 バイト (Float32)               | -3.40e38                 | 3.40e38                        |
| [DOUBLE](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) | –       | 8 バイト (Float64)               | -1.79e308                | 1.79e308                       |
| [DECIMAL](/tidb-cloud-lake/sql/decimal.md)                      | –          | 16/32 バイト (精度 ≤38/76)   | `-(10^P-1)/10^S`         | `(10^P-1)/10^S`                |

## 日付・時刻型 {#date-time-types}

| データ型                 | エイリアス     | 精度 / 備考                   |
|---------------------------|-----------|--------------------------------------|
| [DATE](/tidb-cloud-lake/sql/datetime.md)       | –         | 日単位の精度                        |
| [TIMESTAMP](/tidb-cloud-lake/sql/datetime.md)  | DATETIME  | マイクロ秒、セッションタイムゾーンで出力 |
| [TIMESTAMP_TZ](/tidb-cloud-lake/sql/datetime.md) | –       | マイクロ秒 + オフセットを保存          |
| [INTERVAL](/tidb-cloud-lake/sql/interval.md)   | –         | マイクロ秒、負の期間をサポート |

## 構造化型・半構造化型 {#structured-semi-structured-types}

| データ型             | サンプル                                | 説明 |
|-----------------------|----------------------------------------|-------------|
| [ARRAY](/tidb-cloud-lake/sql/array.md)     | `[1, 2, 3]`                            | 同じ内部型を持つ値の順序付きリストです。 |
| [TUPLE](/tidb-cloud-lake/sql/tuple.md)     | `('2023-02-14','Valentine's Day')`     | 要素型が宣言された固定長の順序付きリストです。 |
| [MAP](/tidb-cloud-lake/sql/map.md)         | `{'a': 1, 'b': 2}`                     | キーと値のコレクションです（内部的にはキー型と値型のタプル）。 |
| [VARIANT](/tidb-cloud-lake/sql/variant.md) | `[1, {"name":"datalake"}]`             | プリミティブ、配列、オブジェクトを混在できる JSON ライクなコンテナです。 |
| [BITMAP](/tidb-cloud-lake/sql/bitmap.md)   | `<bitmap binary>`                      | メンバーシップ判定と集合演算向けに最適化された圧縮ビットマップです。 |

## ドメイン固有型 {#domain-specific-types}

| データ型                           | 説明 |
|------------------------------------|-------------|
| [VECTOR](/tidb-cloud-lake/sql/vector.md)                | 類似検索 / ML ワークロード向けの Float32 埋め込みです。 |
| [GEOMETRY](/tidb-cloud-lake/sql/geospatial.md) / GEOGRAPHY | WKB/EWKB 形式で格納される空間オブジェクトです。 |

## キャストと変換 {#casting-and-conversion}

### 明示的キャスト {#explicit-casting}

- `CAST(expr AS TYPE)` は ANSI 構文を使用し、変換が無効な場合は失敗します。
- `expr::TYPE` は PostgreSQL スタイルの短縮記法です。
- `TRY_CAST(expr AS TYPE)` は、変換に失敗したときにエラーを発生させる代わりに NULL を返します。

### 暗黙的キャスト（型強制） {#implicit-casting-coercion}

{{{ .lake }}} は、明確に定義された状況で自動変換を実行します。

1. 整数は `INT64` に拡張されます。例: `UInt8 -> INT64`。
2. 数値は必要に応じて `FLOAT64` に拡張されます。
3. 式の中に NULL が現れる場合、任意の型 `T` は `Nullable(T)` になります。
4. すべての型は `VARIANT` に拡張できます。
5. 複合型は要素ごとに型強制されます（`T -> U` のとき `Array<T> -> Array<U>`。タプルやマップも同様です）。

対象カラムが `NOT NULL` の場合、データに NULL が含まれる可能性があるなら、明示的に `Nullable<T>` にキャストするか、`TRY_CAST` を使用してください。

```sql
SELECT CONCAT('1', col);      -- safe (strings)
SELECT CONCAT(1, col);        -- may fail if `col` can't coerce to number
```

## NULL の扱いとデフォルト値 {#null-handling-and-defaults}

カラムは、`NOT NULL` と宣言されていない限り NULL 値を許可します。`NOT NULL` カラムが INSERT 時に省略されると、{{{ .lake }}} は型ごとのデフォルト値を書き込みます。

| 型カテゴリ            | デフォルト |
|--------------------------|---------|
| 整数                  | `0`     |
| 浮動小数点           | `0.0`   |
| 文字列 / バイナリ          | 空文字列 / 空バイナリ |
| 日付                     | `1970-01-01` |
| タイムスタンプ                | `1970-01-01 00:00:00` |
| 真偽値                  | `FALSE` |

例:

```sql
CREATE TABLE test (
    id   INT64,
    name STRING NOT NULL,
    age  INT32
);

INSERT INTO test (id, name, age) VALUES (2, 'Alice', NULL);  -- allowed
INSERT INTO test (id, name) VALUES (1, 'John');              -- age becomes NULL
INSERT INTO test (id, age) VALUES (3, 45);                   -- name uses default ''
```

カラムのデフォルト値と NULL 許容性は、いつでも `DESC test` または `SHOW CREATE TABLE test` を使って確認できます。