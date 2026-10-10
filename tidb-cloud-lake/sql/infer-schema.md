---
title: INFER_SCHEMA
summary: ファイルメタデータのスキーマを自動検出し、カラム定義を取得します。
---

# INFER_SCHEMA

ファイルメタデータのスキーマを自動検出し、カラム定義を取得します。

`infer_schema` は現在、次のファイル形式をサポートしています。

- **Parquet** - スキーマ推論をネイティブにサポート
- **CSV** - 区切り文字のカスタマイズとヘッダー検出に対応
- **NDJSON** - 改行区切りの JSON ファイル

**Compression Support**: すべての形式で、拡張子 `.zip`, `.xz`, `.zst` の圧縮ファイルもサポートされます。

> **Note:**
>
> スキーマ推論では、各ファイルの最大サイズは **100MB** に制限されています。

> **Note:**
>
> 複数ファイルを処理する場合、`infer_schema` は異なるスキーマを自動的にマージします。
>
> - **互換性のある型** は昇格されます（例: INT8 + INT16 → INT16）
> - **互換性のない型** は **VARCHAR** にフォールバックします（例: INT + FLOAT → VARCHAR）
> - 一部のファイルに存在しない **欠落カラム** は **nullable** としてマークされます
> - 後続のファイルで見つかった **新しいカラム** は最終スキーマに追加されます
>
> これにより、すべてのファイルを統一されたスキーマで読み取れるようになります。

## 構文 {#syntax}

```sql
INFER_SCHEMA(
  LOCATION => '{ internalStage | externalStage }'
  [ PATTERN => '<regex_pattern>']
  [ FILE_FORMAT => '<format_name>' ]
  [ MAX_RECORDS_PRE_FILE => <number> ]
  [ MAX_FILE_COUNT => <number> ]
)
```

## パラメータ {#parameters}

| パラメータ | 説明 | デフォルト | 例 |
|-----------|-------------|---------|---------|
| `LOCATION` | stage の場所: `@<stage_name>[/<path>]` | 必須 | `'@my_stage/data/'` |
| `PATTERN` | stage 済みファイルに一致する正規表現パターンです。`@<stage_name>[/<path>]` の後のファイルパス部分に対してマッチします。[PATTERN を使用した stage ファイルのフィルタリング](/tidb-cloud-lake/guides/stage-overview.md#filtering-staged-files-with-pattern) を参照してください。 | すべてのファイル | `'.*[.]csv'`, `'.*[.]parquet'` |
| `FILE_FORMAT` | 解析に使用するファイル形式名 | stage の形式 | `'csv_format'`, `'NDJSON'` |
| `MAX_RECORDS_PRE_FILE` | ファイルごとにサンプリングする最大レコード数 | すべてのレコード | `100`, `1000` |
| `MAX_FILE_COUNT` | 処理する最大ファイル数 | すべてのファイル | `5`, `10` |

## 例 {#examples}

### Parquet ファイル {#parquet-files}

```sql
-- Create stage and export data
CREATE STAGE test_parquet;
COPY INTO @test_parquet FROM (SELECT number FROM numbers(10)) FILE_FORMAT = (TYPE = 'PARQUET');

-- Infer schema from parquet files using pattern
SELECT * FROM INFER_SCHEMA(
    location => '@test_parquet',
    pattern => '.*[.]parquet'
);
```

結果:

```
+-------------+-----------------+----------+----------+----------+
| column_name | type            | nullable | filenames| order_id |
+-------------+-----------------+----------+----------+----------+
| number      | BIGINT UNSIGNED |    false | data_... |        0 |
+-------------+-----------------+----------+----------+----------+
```

### CSV ファイル {#csv-files}

```sql
-- Create stage and export CSV data
CREATE STAGE test_csv;
COPY INTO @test_csv FROM (SELECT number FROM numbers(10)) FILE_FORMAT = (TYPE = 'CSV');

-- Create a CSV file format
CREATE FILE FORMAT csv_format TYPE = 'CSV';

-- Infer schema using pattern and file format
SELECT * FROM INFER_SCHEMA(
    location => '@test_csv',
    pattern => '.*[.]csv',
    file_format => 'csv_format'
);
```

結果:

```
+-------------+---------+----------+----------+----------+
| column_name | type    | nullable | filenames| order_id |
+-------------+---------+----------+----------+----------+
| column_1    | BIGINT  |     true | data_... |        0 |
+-------------+---------+----------+----------+----------+
```

ヘッダー付き CSV ファイルの場合:

```sql
-- Create CSV file format with header support
CREATE FILE FORMAT csv_headers_format
TYPE = 'CSV'
field_delimiter = ','
skip_header = 1;

-- Export data with headers
CREATE STAGE test_csv_headers;
COPY INTO @test_csv_headers FROM (
  SELECT number as user_id, 'user_' || number::string as user_name
  FROM numbers(5)
) FILE_FORMAT = (TYPE = 'CSV', output_header = true);

-- Infer schema with headers
SELECT * FROM INFER_SCHEMA(
    location => '@test_csv_headers',
    file_format => 'csv_headers_format'
);
```

より高速に推論するためにレコード数を制限する場合:

```sql
-- Sample only first 5 records for schema inference
SELECT * FROM INFER_SCHEMA(
    location => '@test_csv',
    pattern => '.*[.]csv',
    file_format => 'csv_format',
    max_records_pre_file => 5
);
```

### NDJSON ファイル {#ndjson-files}

```sql
-- Create stage and export NDJSON data
CREATE STAGE test_ndjson;
COPY INTO @test_ndjson FROM (SELECT number FROM numbers(10)) FILE_FORMAT = (TYPE = 'NDJSON');

-- Infer schema using pattern and NDJSON format
SELECT * FROM INFER_SCHEMA(
    location => '@test_ndjson',
    pattern => '.*[.]ndjson',
    file_format => 'NDJSON'
);
```

結果:

```
+-------------+---------+----------+----------+----------+
| column_name | type    | nullable | filenames| order_id |
+-------------+---------+----------+----------+----------+
| number      | BIGINT  |     true | data_... |        0 |
+-------------+---------+----------+----------+----------+
```

より高速に推論するためにレコード数を制限する場合:

```sql
-- Sample only first 5 records for schema inference
SELECT * FROM INFER_SCHEMA(
    location => '@test_ndjson',
    pattern => '.*[.]ndjson',
    file_format => 'NDJSON',
    max_records_pre_file => 5
);
```

### 複数ファイルでのスキーママージ {#schema-merging-with-multiple-files}

ファイルごとにスキーマが異なる場合、`infer_schema` はそれらを賢くマージします。

```sql
-- Suppose you have multiple CSV files with different schemas:
-- file1.csv: id(INT), name(VARCHAR)
-- file2.csv: id(INT), name(VARCHAR), age(INT)
-- file3.csv: id(FLOAT), name(VARCHAR), age(INT)

SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/',
    pattern => '.*[.]csv',
    file_format => 'csv_format'
);
```

結果には、マージされたスキーマが表示されます。

```
+-------------+---------+----------+-----------+----------+
| column_name | type    | nullable | filenames | order_id |
+-------------+---------+----------+-----------+----------+
| id          | VARCHAR |     true | file1,... |        0 |  -- INT+FLOAT→VARCHAR
| name        | VARCHAR |     true | file1,... |        1 |
| age         | BIGINT  |     true | file1,... |        2 |  -- Missing in file1→nullable
+-------------+---------+----------+-----------+----------+
```

### パターンマッチングとファイル数の制限 {#pattern-matching-and-file-limits}

パターンマッチングを使用すると、複数ファイルからスキーマを推論できます。

```sql
-- Infer schema from all CSV files in the directory
SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/',
    pattern => '.*[.]csv'
);
```

パフォーマンスを向上させるために、処理するファイル数を制限できます。

```sql
-- Process only the first 5 matching files
SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/',
    pattern => '.*[.]csv',
    max_file_count => 5
);
```

### 圧縮ファイル {#compressed-files}

`infer_schema` は圧縮ファイルを自動的に処理します。

```sql
-- Works with compressed CSV files
SELECT * FROM INFER_SCHEMA(location => '@my_stage/data.csv.zip');

-- Works with compressed NDJSON files
SELECT * FROM INFER_SCHEMA(
    location => '@my_stage/data.ndjson.xz',
    file_format => 'NDJSON',
    max_records_pre_file => 50
);
```

### 推論されたスキーマからテーブルを作成する {#create-table-from-inferred-schema}

`infer_schema` 関数はスキーマを表示しますが、テーブルは作成しません。推論されたスキーマからテーブルを作成するには、次のようにします。

```sql
-- Create table structure from file schema
CREATE TABLE my_table AS
SELECT * FROM @my_stage/ (pattern=>'.*[.]parquet')
LIMIT 0;

-- Verify the table structure
DESC my_table;
```