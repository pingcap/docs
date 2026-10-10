---
title: NDJSON ファイルのアンロード
summary: NDJSON ファイルをアンロードする方法について説明します。
---

# NDJSON ファイルのアンロード

## TSV ファイルのアンロード {#unloading-tsv-file}

構文:

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (
    TYPE = NDJSON,
    COMPRESSION = gzip,
    OUTPUT_HEADER = true
)
[MAX_FILE_SIZE = <num>]
[DETAILED_OUTPUT = true | false]
```

- NDJSON のその他のオプションについては、[NDJSON ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#ndjson-options) を参照してください
- 複数ファイルへのアンロードには、[MAX_FILE_SIZE Copy Option](/tidb-cloud-lake/sql/copy-into-location.md#copyoptions) を使用します
- 構文の詳細については、[COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md) を参照してください

## チュートリアル {#tutorial}

### Step 1. 外部 stage を作成する {#step-1-create-an-external-stage}

```sql
CREATE STAGE ndjson_unload_stage
URL = 's3://unload/ndjson/'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
);
```

### Step 2. カスタム NDJSON ファイル形式を作成する {#step-2-create-custom-ndjson-file-format}

```
CREATE FILE FORMAT ndjson_unload_format
    TYPE = NDJSON,
    COMPRESSION = gzip;     -- Unload with gzip compression
```

### Step 3. NDJSON ファイルにアンロードする {#step-3-unload-into-ndjson-file}

```sql
COPY INTO @ndjson_unload_stage
FROM (
    SELECT *
    FROM generate_series(1, 100)
)
FILE_FORMAT = (FORMAT_NAME = 'ndjson_unload_format')
DETAILED_OUTPUT = true;
```

結果:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              file_name                              │ file_size │ row_count │
├─────────────────────────────────────────────────────────────────────┼───────────┼───────────┤
│   data_068976e5-2072-4ad8-9887-16fb9129ed80_0000_00000000.ndjson.gz │       263 │       100 │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4. アンロードされた NDJSON ファイルを確認する {#step-4-verify-the-unloaded-ndjson-files}

```sql
SELECT COUNT($1)
FROM @ndjson_unload_stage
(
    FILE_FORMAT => 'ndjson_unload_format',
    PATTERN => '.*[.]ndjson[.]gz'
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