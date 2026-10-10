---
title: COPY INTO <location>
summary: COPY INTO を使用すると、テーブルまたはクエリからデータを、以下のいずれかの場所にある 1 つ以上のファイルへアンロードできます。
---

# `COPY INTO <location>`

COPY INTO を使用すると、テーブルまたはクエリからデータを、以下のいずれかの場所にある 1 つ以上のファイルへアンロードできます。

- User / Internal / External stages: {{{ .lake }}} の stage については、[Stage とは？](/tidb-cloud-lake/guides/stage-overview.md) を参照してください。
- ストレージサービスで作成されたバケットまたはコンテナ。

関連情報: [`COPY INTO <table>`](/tidb-cloud-lake/sql/copy-into-table.md)

## 構文 {#syntax}

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
[ PARTITION BY ( <expr> ) ]
[ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | LANCE } [ formatTypeOptions ]
       ) ]
[ copyOptions ]
[ VALIDATION_MODE = RETURN_ROWS ]
[ DETAILED_OUTPUT = true | false ]
```

### internalStage {#internalstage}

```sql
internalStage ::= @<internal_stage_name>[/<path>]
```

### externalStage {#externalstage}

```sql
externalStage ::= @<external_stage_name>[/<path>]
```

### externalLocation {#externallocation}

<SimpleTab groupId="externallocation">

<div label="Amazon S3-like Storage Services" value="Amazon S3-like Storage Services">

```sql
externalLocation ::=
  's3://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

Amazon S3 互換ストレージサービスへのアクセスに使用できる接続パラメータについては、[Connection Parameters](/tidb-cloud-lake/sql/connection-parameters.md) を参照してください。

</div>

<div label="Azure Blob Storage" value="Azure Blob Storage">

```sql
externalLocation ::=
  'azblob://<container>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

Azure Blob Storage へのアクセスに使用できる接続パラメータについては、[Connection Parameters](/tidb-cloud-lake/sql/connection-parameters.md) を参照してください。

</div>

<div label="Google Cloud Storage" value="Google Cloud Storage">

```sql
externalLocation ::=
  'gcs://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

Google Cloud Storage へのアクセスに使用できる接続パラメータについては、[Connection Parameters](/tidb-cloud-lake/sql/connection-parameters.md) を参照してください。

</div>

<div label="Alibaba Cloud OSS" value="Alibaba Cloud OSS">

```sql
externalLocation ::=
  'oss://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

Alibaba Cloud OSS へのアクセスに使用できる接続パラメータについては、[Connection Parameters](/tidb-cloud-lake/sql/connection-parameters.md) を参照してください。

</div>

<div label="Tencent Cloud Object Storage" value="Tencent Cloud Object Storage">

```sql
externalLocation ::=
  'cos://<bucket>[<path>]'
  CONNECTION = (
        <connection_parameters>
  )
```

Tencent Cloud Object Storage へのアクセスに使用できる接続パラメータについては、[Connection Parameters](/tidb-cloud-lake/sql/connection-parameters.md) を参照してください。

</div>
</SimpleTab>

### FILE_FORMAT {#file-format}

詳細は [入出力ファイル形式](/tidb-cloud-lake/sql/input-output-file-formats.md) を参照してください。

`LANCE` は `COPY INTO <location>` でのみサポートされます。{{{ .lake}}} は、単一のファイルではなく、対象パス配下に Lance データセットディレクトリを書き込みます。

### PARTITION BY {#partition-by}

アンロードされたデータを個別のフォルダに分割するために使用する式を指定します。この式は `STRING` 型として評価される必要があります。式によって生成される値ごとに、宛先パスの下にサブフォルダが作成され、対応する行はそのサブフォルダ配下のファイルに書き込まれます。

- 式が `NULL` と評価された場合、行は特別な `_NULL_` フォルダに配置されます。
- この式では、ソーステーブルまたはクエリの任意のカラムを参照できます。
- パーティション値でのパストラバーサル (`..`) は許可されません。

以下のオプションは `PARTITION BY` と互換性がなく、設定するとエラーになります。

| Option              | 制約                                              |
| ------------------- | ------------------------------------------------- |
| SINGLE              | `PARTITION BY` 使用時は `TRUE` にできません。     |
| OVERWRITE           | `PARTITION BY` 使用時は `TRUE` にできません。     |
| INCLUDE_QUERY_ID    | `PARTITION BY` 使用時は `FALSE` にできません。    |

### copyOptions {#copyoptions}

```sql
copyOptions ::=
  [ SINGLE = true | false ]
  [ MAX_FILE_SIZE = <num> ]
  [ OVERWRITE = true | false ]
  [ INCLUDE_QUERY_ID = true | false ]
  [ USE_RAW_PATH = true | false ]
```

| パラメータ       | デフォルト             | 説明                                                                                                                                                                           |
| ---------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SINGLE           | false                  | `true` の場合、このコマンドはデータを 1 つの単一ファイルにアンロードします。                                                                                                   |
| MAX_FILE_SIZE    | 67108864 bytes (64 MB) | 作成される各ファイルの最大サイズ（バイト単位）です。`SINGLE` が false の場合に有効です。                                                                                       |
| OVERWRITE        | false                  | `true` の場合、対象パスに同名の既存ファイルがあると上書きされます。Note: `OVERWRITE = true` には `USE_RAW_PATH = true` と `INCLUDE_QUERY_ID = false` が必要です。            |
| INCLUDE_QUERY_ID | true                   | `true` の場合、エクスポートされるファイル名に一意の UUID が含まれます。                                                                                                       |
| USE_RAW_PATH     | false                  | `true` の場合、ユーザーが指定したパスそのもの（完全なファイル名を含む）がデータのエクスポートに使用されます。`false` に設定した場合、ユーザーはディレクトリパスを指定する必要があります。 |

> **Note:**
>
> - `TYPE = LANCE` の場合、`SINGLE` はサポートされません。
> - `TYPE = LANCE` の場合、`PARTITION BY` はサポートされません。
> - `TYPE = LANCE` の場合、下流の Lance リーダー向けに安定したデータセット URI が必要であれば、`USE_RAW_PATH = TRUE` を推奨します。
> - `TYPE = LANCE` かつ `USE_RAW_PATH = FALSE` の場合、{{{ .lake}}} は対象パスにクエリ ID を付加し、エクスポートごとに個別のデータセットルートを作成します。

### DETAILED_OUTPUT {#detailed-output}

データのアンロード結果の詳細を返すかどうかを決定します。デフォルト値は `false` です。詳細については、[出力](#output) を参照してください。

## 出力 {#output}

COPY INTO は、データのアンロード結果の要約を以下のカラムで提供します。

| カラム        | 説明                                                                                         |
| ------------- | -------------------------------------------------------------------------------------------- |
| rows_unloaded | 宛先へのアンロードに成功した行数。                                                           |
| input_bytes   | アンロード操作中にソーステーブルから読み取られたデータの合計サイズ（バイト単位）。          |
| output_bytes  | 宛先に書き込まれたデータの合計サイズ（バイト単位）。                                         |

`DETAILED_OUTPUT` を `true` に設定すると、COPY INTO は以下のカラムを含む結果を返します。これは、特に `MAX_FILE_SIZE` を使用してアンロードされたデータを複数ファイルに分割する場合に、アンロードされたファイルの場所を特定するのに役立ちます。

| カラム    | 説明                                           |
| --------- | ---------------------------------------------- |
| file_name | アンロードされたファイルの名前。               |
| file_size | アンロードされたファイルのサイズ（バイト単位）。 |
| row_count | アンロードされたファイルに含まれる行数。       |

## 例 {#examples}

このセクションでは、以下のテーブルとデータを使用して例を示します。

```sql
-- Create sample table
CREATE TABLE canadian_city_population (
     city_name VARCHAR(50),
     population INT
);

-- Insert sample data
INSERT INTO canadian_city_population (city_name, population)
VALUES
('Toronto', 2731571),
('Montreal', 1704694),
('Vancouver', 631486),
('Calgary', 1237656),
('Ottawa', 934243),
('Edmonton', 972223),
('Quebec City', 542298),
('Winnipeg', 705244),
('Hamilton', 536917),
('Halifax', 403390);
```

### 例 1: Internal stage へのアンロード (unload) {#example-1-unloading-to-internal-stage}

この例では、データを internal stage にアンロードします。

```sql
-- Create an internal stage
CREATE STAGE my_internal_stage;

-- Unload data from the table to the stage using the PARQUET file format
COPY INTO @my_internal_stage
    FROM canadian_city_population
    FILE_FORMAT = (TYPE = PARQUET);

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         211 │          572 │
└────────────────────────────────────────────┘

LIST @my_internal_stage;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               name                              │  size  │        md5       │         last_modified         │      creator     │
├─────────────────────────────────────────────────────────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ data_abe520a3-ee88-488c-9221-b07c562c9a30_0000_00000000.parquet │    572 │ NULL             │ 2024-01-18 16:20:48.979 +0000 │ NULL             │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 例 2: 圧縮ファイルへのアンロード (unload) {#example-2-unloading-to-compressed-file}

この例では、データを圧縮ファイルにアンロードします。

```sql
-- Create an internal stage
CREATE STAGE my_internal_stage;

-- Unload data from the table to the stage using the CSV file format with gzip compression
COPY INTO @my_internal_stage
    FROM canadian_city_population
    FILE_FORMAT = (TYPE = CSV COMPRESSION = gzip);

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         182 │          168 │
└────────────────────────────────────────────┘

LIST @my_internal_stage;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │  size  │        md5       │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ data_7970afa5-32e3-4e7d-b793-e42a2a82a8e6_0000_00000000.csv.gz │    168 │ NULL             │ 2024-01-18 16:27:01.663 +0000 │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- COPY INTO also works with custom file formats. See below:
-- Create a custom file format named my_csv_gzip with CSV format and gzip compression
CREATE FILE FORMAT my_csv_gzip TYPE = CSV COMPRESSION = gzip;

-- Unload data from the table to the stage using the custom file format my_csv_gzip
COPY INTO @my_internal_stage
    FROM canadian_city_population
    FILE_FORMAT = (FORMAT_NAME = 'my_csv_gzip');

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         182 │          168 │
└────────────────────────────────────────────┘

LIST @my_internal_stage;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │  size  │        md5       │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼────────┼──────────────────┼───────────────────────────────┼──────────────────┤
│ data_d006ba1c-0609-46d7-a67b-75c7078d86ff_0000_00000000.csv.gz │    168 │ NULL             │ 2024-01-18 16:29:29.721 +0000 │ NULL             │
│ data_7970afa5-32e3-4e7d-b793-e42a2a82a8e6_0000_00000000.csv.gz │    168 │ NULL             │ 2024-01-18 16:27:01.663 +0000 │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 例 3: バケットへのアンロード (unload) {#example-3-unloading-to-bucket}

この例では、データを MinIO 上のバケットにアンロードします。

```sql
-- Unload data from the table to a bucket named 'lake' on MinIO using the PARQUET file format
COPY INTO 's3://lake'
    CONNECTION = (
    ENDPOINT_URL = 'http://localhost:9000/',
    ACCESS_KEY_ID = 'ROOTUSER',
    SECRET_ACCESS_KEY = 'CHANGEME123',
    region = 'us-west-2'
    )
    FROM canadian_city_population
    FILE_FORMAT = (TYPE = PARQUET);

┌────────────────────────────────────────────┐
│ rows_unloaded │ input_bytes │ output_bytes │
├───────────────┼─────────────┼──────────────┤
│            10 │         211 │          572 │
└────────────────────────────────────────────┘
```

### 例 4: PARTITION BY を使用したアンロード (unload) {#example-4-unloading-with-partition-by}

この例では、導出式に基づいてデータをパーティション化されたフォルダにアンロードします。

```sql
-- Create a sample table
CREATE TABLE sales_data (
    sale_date DATE,
    region VARCHAR,
    amount INT
);

INSERT INTO sales_data VALUES
    ('2025-01-15', 'east', 100),
    ('2025-01-20', 'west', 200),
    ('2025-02-10', 'east', 150),
    (NULL, 'west', 50);

-- Create an internal stage
CREATE STAGE partitioned_stage;

-- Unload data partitioned by year-month derived from sale_date
-- When sale_date is NULL, to_varchar() returns NULL, so the entire
-- concatenation evaluates to NULL and the row lands in the _NULL_ folder.
COPY INTO @partitioned_stage
    FROM sales_data
    PARTITION BY ('month=' || to_varchar(sale_date, 'YYYY-MM'))
    FILE_FORMAT = (TYPE = PARQUET);

-- Verify the partitioned folder layout
SELECT name FROM list_stage(location => '@partitioned_stage') ORDER BY name;

┌──────────────────────────────────────────────────────────────────┐
│                              name                                │
├──────────────────────────────────────────────────────────────────┤
│ _NULL_/data_<query_id>_0000_00000000.parquet                     │
│ month=2025-01/data_<query_id>_0000_00000000.parquet              │
│ month=2025-02/data_<query_id>_0000_00000000.parquet              │
└──────────────────────────────────────────────────────────────────┘
```

パーティション式の評価結果が `NULL` の場合、データは `_NULL_` フォルダに配置されます。各一意のパーティション値ごとに、それぞれ対応するデータファイルを含む独自のサブフォルダが作成されます。

### 例 5: Lance データセットへのアンロード (unload) {#example-5-unloading-to-a-lance-dataset}

この例では、データを単独のファイルではなく、Lance データセットディレクトリとしてアンロードします。

```sql
CREATE STAGE ml_stage;

COPY INTO @ml_stage/datasets/train
FROM (
    SELECT number, number + 1 AS label
    FROM numbers(10)
)
FILE_FORMAT = (TYPE = LANCE)
USE_RAW_PATH = TRUE
OVERWRITE = TRUE
DETAILED_OUTPUT = TRUE;
```

出力パスには、次のようなエントリを含む Lance データセットのレイアウトが作成されます。

```text
datasets/train/_versions/...
datasets/train/data/... .lance
datasets/train/*.manifest
```

Python の `lance` を使用した検証を含む、完全なエンドツーエンドの例については、[Lance データセットのアンロード](/tidb-cloud-lake/guides/unload-lance-dataset.md) を参照してください。