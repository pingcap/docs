---
title: stage 内の CSV ファイルをクエリする
summary: CSV ファイルが保存されている独自の S3 バケットと認証情報を使用して external stage を作成します。
---

# stage 内の CSV ファイルをクエリする

## 構文 {#syntax}

- [位置でカラムをクエリする](/tidb-cloud-lake/guides/query-stage.md#query-columns-by-position)
- [メタデータのクエリ](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## チュートリアル {#tutorial}

### ステップ 1. External Stage を作成する {#step-1-create-an-external-stage}

CSV ファイルが保存されている独自の S3 バケットと認証情報を使用して external stage を作成します。

```sql
CREATE STAGE csv_query_stage
URL = 's3://load/csv/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### ステップ 2. カスタム CSV ファイル形式を作成する {#step-2-create-custom-csv-file-format}

```sql
CREATE FILE FORMAT csv_query_format
    TYPE = CSV,
    RECORD_DELIMITER = '\n',
    FIELD_DELIMITER = ',',
    COMPRESSION = AUTO,
    SKIP_HEADER = 1;        -- Skip first line when querying if the CSV file has header
```

- CSV ファイル形式のその他のオプションについては、[CSV File Format Options](/tidb-cloud-lake/sql/input-output-file-formats.md#csv-options) を参照してください

### ステップ 3. CSV ファイルをクエリする {#step-3-query-csv-files}

```sql
SELECT $1, $2, $3
FROM @csv_query_stage
(
    FILE_FORMAT => 'csv_query_format',
    PATTERN => '.*[.]csv'
);
```

CSV ファイルが gzip で圧縮されている場合は、次のクエリを使用できます。

```sql
SELECT $1, $2, $3
FROM @csv_query_stage
(
    FILE_FORMAT => 'csv_query_format',
    PATTERN => '.*[.]csv[.]gz'
);
```

### メタデータ付きでクエリする {#query-with-metadata}

`METADATA$FILENAME` や `METADATA$FILE_ROW_NUMBER` などのメタデータカラムを含めて、stage から CSV ファイルを直接クエリします。

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    $1, $2, $3
FROM @csv_query_stage
(
    FILE_FORMAT => 'csv_query_format',
    PATTERN => '.*[.]csv'
);
```