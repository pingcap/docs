---
title: stage 内の TSV ファイルをクエリする
summary: TSV ファイルが保存されている独自の S3 バケットと認証情報を使用して external stage を作成します。
---

# stage 内の TSV ファイルをクエリする

このガイドでは、stage から TSV（{{{ .lake }}} `v1.2.890-nightly` 以降では `TEXT` と呼ばれます）ファイルをクエリします。例では、古いサーバーバージョンとの互換性のために `TSV` を使用しています。

## 構文 {#syntax}

- [位置でカラムをクエリする](/tidb-cloud-lake/guides/query-stage.md#query-columns-by-position)
- [メタデータのクエリ](/tidb-cloud-lake/guides/query-stage.md#query-metadata)

## チュートリアル {#tutorial}

### Step 1. External Stage を作成する {#step-1-create-an-external-stage}

TSV ファイルが保存されている独自の S3 バケットと認証情報を使用して external stage を作成します。

```sql
CREATE STAGE tsv_query_stage
URL = 's3://load/tsv/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. カスタム TSV File Format を作成する {#step-2-create-custom-tsv-file-format}

```sql
CREATE FILE FORMAT tsv_query_format
    TYPE = TSV,
    RECORD_DELIMITER = '\n',
    FIELD_DELIMITER = ',',
    COMPRESSION = AUTO;
```

- TSV ファイル形式のその他のオプションについては、[TSV File Format Options](/tidb-cloud-lake/sql/input-output-file-formats.md#tsv-options) を参照してください

### Step 3. TSV ファイルをクエリする {#step-3-query-tsv-files}

```sql
SELECT $1, $2, $3
FROM @tsv_query_stage
(
    FILE_FORMAT => 'tsv_query_format',
    PATTERN => '.*[.]tsv'
);
```

TSV ファイルが gzip で圧縮されている場合は、次のクエリを使用できます。

```sql
SELECT $1, $2, $3
FROM @tsv_query_stage
(
    FILE_FORMAT => 'tsv_query_format',
    PATTERN => '.*[.]tsv[.]gz'
);
```

### メタデータ付きでクエリする {#query-with-metadata}

`METADATA$FILENAME` や `METADATA$FILE_ROW_NUMBER` などのメタデータカラムを含めて、stage から TSV ファイルを直接クエリします。

```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    $1, $2, $3
FROM @tsv_query_stage
(
    FILE_FORMAT => 'tsv_query_format',
    PATTERN => '.*[.]tsv'
);
```