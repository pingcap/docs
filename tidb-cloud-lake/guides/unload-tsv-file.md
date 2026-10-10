---
title: TSV ファイルのアンロード
summary: TSV ファイルをアンロードする方法について説明します。
---

# TSV ファイルのアンロード

## TSV ファイルのアンロード {#unloading-tsv-file}

構文:

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (
    TYPE = TSV,
    RECORD_DELIMITER = '<character>',
    FIELD_DELIMITER = '<character>',
    COMPRESSION = gzip,
    OUTPUT_HEADER = true -- Unload with header
)
[MAX_FILE_SIZE = <num>]
[DETAILED_OUTPUT = true | false]
```

- TSV のその他のオプションについては、[TSV ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#tsv-options) を参照してください
- 複数ファイルへのアンロードには、[MAX_FILE_SIZE Copy Option](/tidb-cloud-lake/sql/copy-into-location.md#copyoptions) を使用します
- 構文の詳細については、[COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md) を参照してください

## チュートリアル {#tutorial}

### Step 1. 外部 stage を作成する {#step-1-create-an-external-stage}

```sql
CREATE STAGE tsv_unload_stage
URL = 's3://unload/tsv/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. カスタム TSV ファイル形式を作成する {#step-2-create-custom-tsv-file-format}

```sql
CREATE FILE FORMAT tsv_unload_format
    TYPE = TSV,
    COMPRESSION = gzip;     -- Unload with gzip compression
```

### Step 3. TSV ファイルにアンロードする {#step-3-unload-into-tsv-file}

```sql
COPY INTO @tsv_unload_stage
FROM (
    SELECT *
    FROM generate_series(1, 100)
)
FILE_FORMAT = (FORMAT_NAME = 'tsv_unload_format')
DETAILED_OUTPUT = true;
```

結果:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             file_name                            │ file_size │ row_count │
├──────────────────────────────────────────────────────────────────┼───────────┼───────────┤
│   data_99e8f5c8-79d6-43d8-80d7-13e3f4c91dd5_0002_00000000.tsv.gz │       160 │       100 │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4. アンロードされた TSV ファイルを確認する {#step-4-verify-the-unloaded-tsv-files}

```
SELECT COUNT($1)
FROM @tsv_unload_stage
(
    FILE_FORMAT => 'tsv_unload_format',
    PATTERN => '.*[.]tsv[.]gz'
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