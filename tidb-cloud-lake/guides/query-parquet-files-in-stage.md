---
title: stage 内の Parquet ファイルをクエリする
summary: Parquet ファイルが保存されている独自の S3 バケットと認証情報を使用して external stage を作成します。
---

# stage 内の Parquet ファイルをクエリする

## 構文 {#syntax}

- [行を Variants としてクエリ](/tidb-cloud-lake/guides/query-stage.md#query-rows-as-variants)
- [名前でカラムをクエリ](/tidb-cloud-lake/guides/query-stage.md#query-columns-by-name)
- [メタデータのクエリ](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## チュートリアル {#tutorial}

### Step 1. External Stage を作成する {#step-1-create-an-external-stage}

Parquet ファイルが保存されている独自の S3 バケットと認証情報を使用して external stage を作成します。

```sql
CREATE STAGE parquet_query_stage
URL = 's3://load/parquet/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. カスタム Parquet File Format を作成する {#step-2-create-custom-parquet-file-format}

```sql
CREATE FILE FORMAT parquet_query_format TYPE = PARQUET;
```

- Parquet file format のその他のオプションについては、[Parquet File Format Options](/tidb-cloud-lake/sql/input-output-file-formats.md#parquet-options) を参照してください。

### Step 3. Parquet ファイルをクエリする {#step-3-query-parquet-files}

カラム名を使用してクエリします。

```sql
SELECT *
FROM @parquet_query_stage
(
    FILE_FORMAT => 'parquet_query_format',
    PATTERN => '.*[.]parquet'
);
```

パス式を使用してクエリします。

```sql
SELECT $1
FROM @parquet_query_stage
(
    FILE_FORMAT => 'parquet_query_format',
    PATTERN => '.*[.]parquet'
);
```

### メタデータを使用してクエリする {#query-with-metadata}

`METADATA$FILENAME` や `METADATA$FILE_ROW_NUMBER` などのメタデータカラムを含めて、stage から Parquet ファイルを直接クエリします。

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    *
FROM @parquet_query_stage
(
    FILE_FORMAT => 'parquet_query_format',
    PATTERN => '.*[.]parquet'
);
```