---
title: Parquet ファイルのアンロード
summary: parquet ファイルをアンロードする方法について説明します。
---

# Parquet ファイルのアンロード

## Parquet ファイルのアンロード {#unloading-parquet-file}

構文:

```sql
COPY INTO {internalStage | externalStage | externalLocation}
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (TYPE = PARQUET)
[MAX_FILE_SIZE = <num>]
[DETAILED_OUTPUT = true | false]
```

- Parquet のその他のオプションについては、[Parquet ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#parquet-options) を参照してください
- 複数ファイルへのアンロードには、[MAX_FILE_SIZE Copy Option](/tidb-cloud-lake/sql/copy-into-location.md#copyoptions) を使用します
- 構文の詳細については、[COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md) を参照してください

## チュートリアル {#tutorial}

### Step 1. 外部 stage を作成する {#step-1-create-an-external-stage}

```sql
CREATE STAGE parquet_unload_stage
URL = 's3://unload/parquet/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. カスタム Parquet ファイル形式を作成する {#step-2-create-custom-parquet-file-format}

```sql
CREATE FILE FORMAT parquet_unload_format
    TYPE = PARQUET
    ;
```

### Step 3. Parquet ファイルにアンロードする {#step-3-unload-into-parquet-file}

```sql
COPY INTO @parquet_unload_stage
FROM (
    SELECT *
    FROM generate_series(1, 100)
)
FILE_FORMAT = (FORMAT_NAME = 'parquet_unload_format')
DETAILED_OUTPUT = true;
```

結果:

```text
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                             file_name                             │ file_size │ row_count │
│                               String                              │   UInt64  │   UInt64  │
├───────────────────────────────────────────────────────────────────┼───────────┼───────────┤
│   data_a3760513-78a8-4a89-8f92-b1a17e0a61b6_0000_00000000.parquet │       445 │       100 │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4. アンロードした Parquet ファイルを確認する {#step-4-verify-the-unloaded-parquet-files}

```sql
SELECT COUNT($1)
FROM @parquet_unload_stage
(
    FILE_FORMAT => 'parquet_unload_format',
    PATTERN => '.*[.]parquet'
);
```

結果:

```text
┌───────────┐
│ count($1) │
├───────────┤
│       100 │
└───────────┘
```