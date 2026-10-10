---
title: Schema Evolution
summary: COPY INTO を使用したデータロード時に、テーブルスキーマを自動的に進化させます。
---

# Schema Evolution

Schema Evolution を使用すると、{{{ .lake }}} は `COPY INTO` の実行時に、ソースファイルには存在するがターゲットテーブルには存在しないカラムを自動的に追加できます。現在は **Parquet** と **NDJSON** ファイルをサポートしています。

## 仕組み {#how-it-works}

有効にすると、{{{ .lake }}} はロード前にソースファイルのスキーマを推論し、新しいカラムをテーブルの末尾に追加します。新しいカラムは NULL 許容となり、欠損値は `NULL` で埋められます。

ワークフローはファイル形式によって少し異なります。

- **Parquet**: テーブルオプションを有効にすると、`COPY INTO` は Parquet ファイルのスキーマから新しいカラムを直接推論します。
- **NDJSON**: テーブルオプションを有効にすると、`COPY INTO` はスキーマ推論のために `AUTO` のサンプリング値を使用します。必要に応じて `SCHEMA_EVOLUTION = (...)` を追加し、ファイルおよびレコードのサンプリング上限を上書きできます。

## Schema Evolution を有効にする {#enabling-schema-evolution}

テーブルオプション `ENABLE_SCHEMA_EVOLUTION` を `true` に設定します。

```sql
-- On an existing table
ALTER TABLE my_table SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

-- Or when creating a new table
CREATE TABLE my_table(id INT) ENABLE_SCHEMA_EVOLUTION = true;
```

Schema Evolution を無効にするには、`false` に戻します。

```sql
ALTER TABLE my_table SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = false);
```

## 権限 {#privileges}

`COPY INTO <table>` が stage または外部ロケーションからファイルをロード (load) し、Schema Evolution の推論を実行する場合、ロードを実行するロールにはターゲットテーブルに対する `INSERT` 権限と `ALTER` 権限の両方が必要です。`ALTER` が必要なのは、{{{ .lake }}} がロード前に新しいカラムを追加する可能性があるためです。

クエリベースの COPY は影響を受けません。たとえば、`COPY INTO <table> FROM (SELECT ... FROM @stage)` では、既存の権限要件がそのまま適用されます。

## Parquet の例 {#parquet-example}

次の例では、異なるスキーマを持つ Parquet ファイルをロードし、不足しているカラムを自動的に追加します。

### ステップ 1: テーブルと stage を作成する {#step-1-create-a-table-and-stage}

```sql
CREATE OR REPLACE TABLE invoices(order_id INT);
CREATE OR REPLACE STAGE my_stage;
```

### ステップ 2: 異なるスキーマを持つ Parquet ファイルを生成する {#step-2-generate-parquet-files-with-different-schemas}

```sql
-- File with columns: order_id, amount, currency
COPY INTO @my_stage FROM (
    SELECT 1 AS order_id, 100.50::DOUBLE AS amount, 'USD' AS currency
    UNION ALL
    SELECT 2, 250.50::DOUBLE, 'EUR'
) FILE_FORMAT = (TYPE = parquet);

-- File with columns: order_id, amount (no currency)
COPY INTO @my_stage FROM (
    SELECT 3 AS order_id, 75.50::DOUBLE AS amount
) FILE_FORMAT = (TYPE = parquet);
```

### ステップ 3: Schema Evolution を有効にしてロードする {#step-3-enable-schema-evolution-and-load}

```sql
ALTER TABLE invoices SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

COPY INTO invoices
FROM @my_stage/
FILE_FORMAT = (TYPE = parquet MISSING_FIELD_AS = FIELD_DEFAULT);
```

### ステップ 4: 結果を確認する {#step-4-verify-results}

これでテーブルには 3 つのカラムがあります。`amount` と `currency` は自動的に追加されました。

```sql
DESC invoices;
```

```text
┌─────────────────────────────────────────────────────────────┐
│   Field  │      Type      │  Null  │ Default │    Extra     │
├──────────┼────────────────┼────────┼─────────┼──────────────┤
│ order_id │ INT            │ YES    │ NULL    │              │
│ amount   │ DOUBLE         │ YES    │ NULL    │              │
│ currency │ VARCHAR        │ YES    │ NULL    │              │
└─────────────────────────────────────────────────────────────┘
```

```sql
SELECT * FROM invoices ORDER BY order_id;
```

```text
┌──────────────────────────────────────────────────┐
│ order_id │  amount  │ currency                    │
├──────────┼──────────┼─────────────────────────────┤
│        1 │   100.50 │ USD                         │
│        2 │   250.50 │ EUR                         │
│        3 │    75.50 │ NULL                        │
└──────────────────────────────────────────────────┘
```

3 行目の `currency = NULL` になっているのは、ソースファイルにそのカラムが含まれていなかったためです。

## NDJSON の例 {#ndjson-example}

{{{ .lake }}} は `TYPE = ndjson` を使用して NDJSON ファイルをロードします。NDJSON ファイルには Parquet ファイルのような埋め込みのカラムスキーマがないため、{{{ .lake }}} はファイル内容をサンプリングし、ターゲットテーブルに存在しないフィールドを推論して、NULL 許容カラムとして追加します。

### ステップ 1: テーブルと stage を作成する {#step-1-create-a-table-and-stage}

```sql
CREATE OR REPLACE TABLE events(id INT);
CREATE OR REPLACE STAGE events_stage;
```

### ステップ 2: 異なるフィールドを持つ NDJSON ファイルを生成する {#step-2-generate-ndjson-files-with-different-fields}

```sql
-- File with fields: id, city, score
COPY INTO @events_stage FROM (
    SELECT 1 AS id, 'SF' AS city, 9 AS score
    UNION ALL
    SELECT 2, 'NYC', 8
) FILE_FORMAT = (TYPE = ndjson);

-- File with fields: id, score (no city)
COPY INTO @events_stage FROM (
    SELECT 3 AS id, 7 AS score
) FILE_FORMAT = (TYPE = ndjson);
```

### ステップ 3: Schema Evolution を有効にしてロードする {#step-3-enable-schema-evolution-and-load}

```sql
ALTER TABLE events SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

COPY INTO events
FROM @events_stage/
FILE_FORMAT = (TYPE = ndjson MISSING_FIELD_AS = FIELD_DEFAULT)
SCHEMA_EVOLUTION = (
  SAMPLE_FILES = AUTO,
  SAMPLE_RECORDS_PER_FILE = AUTO,
  SAMPLE_TOTAL_RECORDS = AUTO
);
```

3 つの `SCHEMA_EVOLUTION` サンプリングオプションは、`AUTO` または正の整数を受け付けます。

| オプション | 説明 |
|------|------|
| `SAMPLE_FILES` | サンプリングするファイル数。 |
| `SAMPLE_RECORDS_PER_FILE` | 選択した各ファイルからサンプリングするレコードの最大数。 |
| `SAMPLE_TOTAL_RECORDS` | 選択したすべてのファイル全体でサンプリングするレコードの最大数。 |

`SCHEMA_EVOLUTION` を省略した場合、{{{ .lake }}} は 3 つすべてのサンプリングオプションに `AUTO` を使用します。現在の `AUTO` の動作では、最大 64 ファイル、各ファイルあたり 1,000 レコード、合計 10,000 レコードまでサンプリングします。これらの内部デフォルト値は、将来のバージョンで変更される可能性があります。ロードがサンプリング戦略に敏感な場合は、`SAMPLE_FILES`、`SAMPLE_RECORDS_PER_FILE`、`SAMPLE_TOTAL_RECORDS` を明示的に設定してください。

#### NDJSON 推論ルール {#ndjson-inference-rules}

NDJSON に対して Schema Evolution を実行すると、{{{ .lake }}} は次のルールを使用して新しいカラムを推論します。

- スキーマは、サンプリングされた NDJSON レコードからのみ推論されます。サンプルに含まれないフィールドは、事前にターゲットテーブルへ追加されません。
- 各行は JSON オブジェクトである必要があります。{{{ .lake }}} は、トップレベルのオブジェクトのフィールド名を Candidate カラム名として使用します。
- ターゲットテーブルにすでに存在するカラムは再度追加されません。ターゲットテーブルに存在しないフィールドのみが追加されます。
- 新しいフィールドの型は、整数、浮動小数点数、文字列、ブール値など、サンプリングされた JSON 値から推論されます。
- Schema Evolution は浅い NDJSON 推論を使用します。トップレベルのフィールド値がオブジェクトまたは配列の場合、再帰的に展開するのではなく、`VARIANT` カラムとして追加されます。
- `NULL` のサンプルは、そのフィールドが nullable であることを示すだけです。後続の非 null 値が `VARCHAR` や `VARIANT` になることを強制しません。
- ファイルまたはレコード間で同名のフィールドはマージされます。整数と浮動小数点数の競合は `DOUBLE` になり、その他のスカラー型の競合は `VARCHAR` になり、オブジェクト、配列、または `VARIANT` を含む競合は `VARIANT` になります。
- ロード時に、サンプリング中に推論されなかった追加フィールドが見つかった場合、ロードは失敗し、それらのフィールド名が報告されます。`SAMPLE_FILES`、`SAMPLE_RECORDS_PER_FILE`、または `SAMPLE_TOTAL_RECORDS` を増やして再試行してください。

> **Note:**
>
> `INFER_SCHEMA` テーブル関数は、デフォルトでは NDJSON のネスト深度を制限しません。ここで説明しているルールは、`COPY INTO` の Schema Evolution で使用される浅い推論についてのものです。

たとえば、次の NDJSON レコードからは、`name`、`age`、`active`、`score`、`profile`、`tags` の 6 つの新しいカラムが推論されます。

```json
{"id":1,"name":"Alice","age":30,"active":true,"score":1,"profile":{"city":"SF"},"tags":["new"]}
{"id":2,"name":"Bob","age":null,"active":false,"score":1.5,"profile":{"city":"NYC"},"tags":["vip"]}
```

ターゲットテーブルに `id INT` しかない場合、{{{ .lake }}} は次を追加します。

```text
name    VARCHAR   NULL
age     BIGINT    NULL
active  BOOLEAN   NULL
score   DOUBLE    NULL
profile VARIANT   NULL
tags    VARIANT   NULL
```

2 行目の `age = NULL` は、1 行目から推論された `BIGINT` 型を変更しません。`score` には整数と浮動小数点数の両方が含まれるため、`DOUBLE` になります。`profile` と `tags` はそれぞれオブジェクトと配列であるため、Schema Evolution はそれらを `VARIANT` カラムとして追加します。

### Step 4: 結果を確認する {#step-4-verify-results}

テーブルには現在 3 つのカラムがあります。`city` と `score` は自動的に追加されました。

```sql
DESC events;
```

```text
┌─────────────────────────────────────────────────────────┐
│ Field │     Type     │  Null  │ Default │    Extra     │
├───────┼──────────────┼────────┼─────────┼──────────────┤
│ id    │ INT          │ YES    │ NULL    │              │
│ city  │ VARCHAR      │ YES    │ NULL    │              │
│ score │ BIGINT       │ YES    │ NULL    │              │
└─────────────────────────────────────────────────────────┘
```

```sql
SELECT * FROM events ORDER BY id;
```

```text
┌────────────────────────────┐
│ id │ city │ score          │
├────┼──────┼────────────────┤
│  1 │ SF   │              9 │
│  2 │ NYC  │              8 │
│  3 │ NULL │              7 │
└────────────────────────────┘
```

サンプルに、後でデータ内に現れるフィールドが含まれていない場合、ロードは失敗し、追加フィールド名を返します。`SAMPLE_FILES`、`SAMPLE_RECORDS_PER_FILE`、または `SAMPLE_TOTAL_RECORDS` を増やして再試行してください。

## カラム一致モード {#column-match-mode}

デフォルトでは、カラム名は大文字と小文字を区別せずに一致します。大文字と小文字を区別して一致させるには、`COLUMN_MATCH_MODE` を使用します。

```sql
COPY INTO invoices
FROM @my_stage/
FILE_FORMAT = (TYPE = parquet MISSING_FIELD_AS = FIELD_DEFAULT)
COLUMN_MATCH_MODE = CASE_SENSITIVE;
```

## 制限事項 {#limitations}

- 現在サポートしているのは **Parquet** ファイルと **NDJSON** ファイルです。
- 新しいカラムはテーブルの末尾に追加され、常に nullable です。
- 同じカラム名が複数のファイルに **異なるデータ型** で現れる場合、ロードは失敗します。
- `INT` から `BIGINT` へのような自動的な型昇格はありません。
- Schema Evolution では、カラムの削除および名前変更はサポートされていません。
- NDJSON はスキーマ推論にサンプリングを使用します。サンプリングですべてのフィールドをカバーできない場合は、`SCHEMA_EVOLUTION` のサンプリングオプションを増やしてください。