---
title: "COPY INTO <table>"
summary: COPY INTO を使用すると、以下のいずれかの場所にあるファイルからデータをロードできます。
---

# `COPY INTO <table>`

COPY INTO を使用すると、以下のいずれかの場所にあるファイルからデータをロード (load) できます。

- User / Internal / External stages: {{{ .lake }}} の stage については、[What is Stage?](/tidb-cloud-lake/guides/stage-overview.md) を参照してください。
- ストレージサービスで作成されたバケットまたはコンテナ。
- URL（`https://` で始まる）でファイルにアクセスできるリモートサーバー。
- [IPFS](https://ipfs.tech) および Hugging Face リポジトリ。

関連情報: [`COPY INTO <location>`](/tidb-cloud-lake/sql/copy-into-location.md)

## 構文 {#syntax}

```sql
/* Standard data load */
COPY INTO [<database_name>.]<table_name> [ ( <col_name> [ , <col_name> ... ] ) ]
     FROM { userStage | internalStage | externalStage | externalLocation }
[ FILES = ( '<file_name>' [ , '<file_name>' ] [ , ... ] ) ]
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO } [ formatTypeOptions ]
       ) ]
[ copyOptions ]

/* Data load with transformation */
COPY INTO [<database_name>.]<table_name> [ ( <col_name> [ , <col_name> ... ] ) ]
     FROM (
        SELECT {
            [<alias>.]<column> [, [<alias>.]<column> ...] -- Query columns by name
            | [<alias>.]$<col_position> [, [<alias>.]$<col_position> ...] -- Query columns by position
            | [<alias>.]$1[:<column>] [, [<alias>.]$1[:<column>]  ...] -- Query rows as Variants
            } ]
        FROM {@<stage_name>[/<path>] | '<uri>'}
    )
[ FILES = ( '<file_name>' [ , '<file_name>' ] [ , ... ] ) ]
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO } [ formatTypeOptions ]
       ) ]
[ copyOptions ]
```

> **Note:**
>
> {{{ .lake }}} `v1.2.890-nightly` 以降では、`FILE_FORMAT` 内で `TEXT` を `TSV` のエイリアスとして使用できます。古いサーバーでは `TYPE = TEXT` が拒否される場合があるため、このページでは互換性を考慮して、構文と例で引き続き `TSV` を使用しています。

Where:

```sql
userStage ::= @~[/<path>]

internalStage ::= @<internal_stage_name>[/<path>]

externalStage ::= @<external_stage_name>[/<path>]

externalLocation ::=
  /* Amazon S3-like Storage */
  's3://<bucket>[/<path>]'
  CONNECTION = (
    [ CONNECTION_NAME = '<connection-name>' ]
    | [ ENDPOINT_URL = '<endpoint-url>' ]
    [ ACCESS_KEY_ID = '<your-access-key-ID>' ]
    [ SECRET_ACCESS_KEY = '<your-secret-access-key>' ]
    [ ENABLE_VIRTUAL_HOST_STYLE = TRUE | FALSE ]
    [ MASTER_KEY = '<your-master-key>' ]
    [ REGION = '<region>' ]
    [ SECURITY_TOKEN = '<security-token>' ]
    [ ROLE_ARN = '<role-arn>' ]
    [ EXTERNAL_ID = '<external-id>' ]
  )

  /* Azure Blob Storage */
  | 'azblob://<container>[/<path>]'
    CONNECTION = (
      [ CONNECTION_NAME = '<connection-name>' ]
      | ENDPOINT_URL = '<endpoint-url>'
      ACCOUNT_NAME = '<account-name>'
      ACCOUNT_KEY = '<account-key>'
    )

  /* Google Cloud Storage */
  | 'gcs://<bucket>[/<path>]'
    CONNECTION = (
      [ CONNECTION_NAME = '<connection-name>' ]
      | CREDENTIAL = '<your-base64-encoded-credential>'
    )

  /* Alibaba Cloud OSS */
  | 'oss://<bucket>[/<path>]'
    CONNECTION = (
      [ CONNECTION_NAME = '<connection-name>' ]
      | ACCESS_KEY_ID = '<your-ak>'
      ACCESS_KEY_SECRET = '<your-sk>'
      ENDPOINT_URL = '<endpoint-url>'
      [ PRESIGN_ENDPOINT_URL = '<presign-endpoint-url>' ]
    )

  /* Tencent Cloud Object Storage */
  | 'cos://<bucket>[/<path>]'
    CONNECTION = (
      [ CONNECTION_NAME = '<connection-name>' ]
      | SECRET_ID = '<your-secret-id>'
      SECRET_KEY = '<your-secret-key>'
      ENDPOINT_URL = '<endpoint-url>'
    )

  /* Remote Files */
  | 'https://<url>'

  /* IPFS */
  | 'ipfs://<your-ipfs-hash>'
    CONNECTION = (ENDPOINT_URL = 'https://<your-ipfs-gateway>')

  /* Hugging Face */
  | 'hf://<repo-id>[/<path>]'
    CONNECTION = (
      [ REPO_TYPE = 'dataset' | 'model' ]
      [ REVISION = '<revision>' ]
      [ TOKEN = '<your-api-token>' ]
    )

formatTypeOptions ::=
  /* Common options for all formats */
  [ COMPRESSION = AUTO | GZIP | BZ2 | BROTLI | ZSTD | DEFLATE | RAW_DEFLATE | XZ | NONE ]

  /* CSV specific options */
  [ RECORD_DELIMITER = '<character>' ]
  [ FIELD_DELIMITER = '<character>' ]
  [ SKIP_HEADER = <integer> ]
  [ QUOTE = '<character>' ]
  [ ESCAPE = '<character>' ]
  [ NAN_DISPLAY = '<string>' ]
  [ NULL_DISPLAY = '<string>' ]
  [ ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE | FALSE ]
  [ EMPTY_FIELD_AS = null | string | field_default ]
  [ BINARY_FORMAT = HEX | BASE64 ]
  [ TRIM_SPACE = TRUE | FALSE ]
  [ ENCODING = '<encoding_label>' ]
  [ ENCODING_ERROR_MODE = STRICT | REPLACE ]

  /* TSV specific options */
  [ RECORD_DELIMITER = '<character>' ]
  [ FIELD_DELIMITER = '<character>' ]
  [ TRIM_SPACE = TRUE | FALSE ]
  [ ENCODING = '<encoding_label>' ]
  [ ENCODING_ERROR_MODE = STRICT | REPLACE ]

  /* NDJSON specific options */
  [ NULL_FIELD_AS = NULL | FIELD_DEFAULT ]
  [ MISSING_FIELD_AS = ERROR | NULL | FIELD_DEFAULT ]
  [ NULL_IF = ('value1', 'value2', ...) ]

  /* PARQUET specific options */
  [ MISSING_FIELD_AS = ERROR | FIELD_DEFAULT ]
  [ NULL_IF = ('value1', 'value2', ...) ]
  [ USE_LOGIC_TYPE = TRUE | FALSE ]

  /* ORC specific options */
  [ MISSING_FIELD_AS = ERROR | FIELD_DEFAULT ]

  /* AVRO specific options */
  [ MISSING_FIELD_AS = ERROR | FIELD_DEFAULT ]
  [ NULL_IF = ('value1', 'value2', ...) ]
  [ USE_LOGIC_TYPE = TRUE | FALSE ]

copyOptions ::=
  [ PURGE = <bool> ]
  [ FORCE = <bool> ]
  [ DISABLE_VARIANT_CHECK = <bool> ]
  [ ON_ERROR = { continue | abort | abort_N } ]
  [ MAX_FILES = <num> ]
  [ RETURN_FAILED_ONLY = <bool> ]
  [ COLUMN_MATCH_MODE = { case-sensitive | case-insensitive } ]
  [ SCHEMA_EVOLUTION = (
      [ SAMPLE_FILES = AUTO | <positive_integer> ]
      [ , SAMPLE_RECORDS_PER_FILE = AUTO | <positive_integer> ]
      [ , SAMPLE_TOTAL_RECORDS = AUTO | <positive_integer> ]
    ) ]
```

## 主なパラメータ {#key-parameters}

- **FILES**: ロードする 1 つ以上のファイル名（カンマ区切り）を指定します。

- **PATTERN**: 一致させるファイル名を指定する、[PCRE2](https://www.pcre.org/current/doc/html/) ベースの正規表現パターン文字列です。stage からロードする場合、このパターンは `@<stage_name>[/<path>]` より後ろのファイルパス部分に対して一致します。[PATTERN を使用した stage ファイルのフィルタリング](/tidb-cloud-lake/guides/stage-overview.md#filtering-staged-files-with-pattern) および [例 4: PATTERN を使用したファイルのフィルタリング](#example-4-filtering-files-with-pattern) を参照してください。

## Format Type Options {#format-type-options}

`FILE_FORMAT` パラメータはさまざまなファイルタイプをサポートしており、それぞれに固有のフォーマットオプションがあります。以下に、サポートされている各ファイル形式で使用可能なオプションを示します。すべてのオプションの詳細については、[Input & Output File Formats](/tidb-cloud-lake/sql/input-output-file-formats.md) を参照してください。

<SimpleTab>

<div label="Common Options" value="common">

これらのオプションは、すべてのファイル形式で使用できます。

| オプション | 説明 | 値 | デフォルト |
|--------|-------------|--------|--------|
| COMPRESSION | データファイルの圧縮アルゴリズム | AUTO, GZIP, BZ2, BROTLI, ZSTD, DEFLATE, RAW_DEFLATE, XZ, NONE | AUTO |

</div>

<div label="CSV" value="csv">

| オプション | 説明 | デフォルト |
|--------|-------------|--------|
| RECORD_DELIMITER | レコードを区切る文字 | newline |
| FIELD_DELIMITER | フィールドを区切る文字 | comma (,) |
| SKIP_HEADER | スキップするヘッダー行数 | 0 |
| QUOTE | フィールドを囲むために使用する文字 | double-quote (") |
| ESCAPE | 囲まれたフィールドのエスケープ文字 | NONE |
| NAN_DISPLAY | NaN 値を表す文字列 | NaN |
| NULL_DISPLAY | NULL 値を表す文字列 | \N |
| ERROR_ON_COLUMN_COUNT_MISMATCH | カラム数が一致しない場合にエラーにする | TRUE |
| EMPTY_FIELD_AS | 空フィールドの処理方法 | null |
| BINARY_FORMAT | バイナリデータのエンコード形式 (HEX または BASE64) | HEX |
| TRIM_SPACE | フィールドの先頭および末尾の ASCII 空白を削除する | FALSE |
| ENCODING | ソースファイルの文字セットエンコーディング | UTF-8 |
| ENCODING_ERROR_MODE | 無効なバイトの処理方法: STRICT または REPLACE | STRICT |

</div>

<div label="TSV" value="tsv">

| オプション | 説明 | デフォルト |
|--------|-------------|--------|
| RECORD_DELIMITER | レコードを区切る文字 | newline |
| FIELD_DELIMITER | フィールドを区切る文字 | tab (\t) |
| SKIP_HEADER | スキップするヘッダー行数 | 0 |
| TRIM_SPACE | フィールドの先頭および末尾の ASCII 空白を削除する | FALSE |
| NAN_DISPLAY | NaN 値を表す文字列 | NaN |
| NULL_DISPLAY | NULL 値を表す文字列 | \N |
| EMPTY_FIELD_AS | 空フィールドの処理方法 | FIELD_DEFAULT |
| ERROR_ON_COLUMN_COUNT_MISMATCH | カラム数が一致しない場合にエラーにする | TRUE |
| ENCODING | ソースファイルの文字セットエンコーディング | UTF-8 |
| ENCODING_ERROR_MODE | 無効なバイトの処理方法: STRICT または REPLACE | STRICT |

</div>

<div label="NDJSON" value="ndjson">

| オプション | 説明 | デフォルト |
|--------|-------------|--------|
| NULL_FIELD_AS | null フィールドの処理方法 | NULL |
| MISSING_FIELD_AS | 欠落しているフィールドの処理方法 | ERROR |
| NULL_IF | NULL として扱う文字列のリスト | empty |

</div>

<div label="PARQUET" value="parquet">

| オプション | 説明 | デフォルト |
|--------|-------------|--------|
| MISSING_FIELD_AS | 欠落しているフィールドの処理方法 | ERROR |
| NULL_IF | NULL として扱う文字列のリスト | empty |
| USE_LOGIC_TYPE | カラム型推論に Parquet の論理型を使用する | TRUE |

</div>

<div label="ORC" value="orc">

| オプション | 説明 | デフォルト |
|--------|-------------|--------|
| MISSING_FIELD_AS | 欠落しているフィールドの処理方法 | ERROR |

</div>

<div label="AVRO" value="avro">

| オプション | 説明 | デフォルト |
|--------|-------------|--------|
| MISSING_FIELD_AS | 欠落しているフィールドの処理方法 | ERROR |
| NULL_IF | NULL として扱う文字列のリスト | empty |
| USE_LOGIC_TYPE | カラム型推論に Avro の論理型を使用する | TRUE |

</div>
</SimpleTab>

## Copy Options {#copy-options}

| パラメータ | 説明 | デフォルト |
|-----------|-------------|----------|
| PURGE | ロード成功後にファイルを削除する | `false` |
| FORCE | 重複ファイルの再ロードを許可する | `false` (重複をスキップ) |
| DISABLE_VARIANT_CHECK | 無効な JSON を null に置き換える | `false` (無効な JSON では失敗) |
| ON_ERROR | エラーの処理方法: `continue`、`abort`、または `abort_N` | `abort` |
| MAX_FILES | ロードするファイルの最大数 (最大 15,000) | - |
| RETURN_FAILED_ONLY | 出力で失敗したファイルのみを返す | `false` |
| COLUMN_MATCH_MODE | Parquet 用: カラム名のマッチングモード | `case-insensitive` |
| SCHEMA_EVOLUTION | NDJSON 用: ターゲットテーブルに存在しないカラムを推論するために使用されるサンプリングオプション。`ENABLE_SCHEMA_EVOLUTION = true` と、ターゲットテーブルに対する `ALTER` 権限が必要です。 | `AUTO` サンプリング |

### SCHEMA_EVOLUTION Options {#schema-evolution-options}

`SCHEMA_EVOLUTION` は、{{{ .lake }}} がロード前に stage 上の NDJSON ファイルをどのようにサンプリングするかを制御します。ターゲットテーブルで `ENABLE_SCHEMA_EVOLUTION = true` が設定されている場合に、`FILE_FORMAT = (TYPE = NDJSON ...)` と組み合わせて使用します。

stage または location のロードで schema evolution の推論が実行される場合、`COPY INTO <table>` を実行するロールには、ターゲットテーブルに対する `INSERT` 権限と `ALTER` 権限の両方が必要です。`COPY INTO <table> FROM (SELECT ... FROM @stage)` のようなクエリベースの COPY では、既存の権限要件が維持されます。

| オプション | 説明 | 値 |
|--------|-------------|--------|
| SAMPLE_FILES | サンプリングする stage 上のファイル数。 | `AUTO` または正の整数 |
| SAMPLE_RECORDS_PER_FILE | 選択された各ファイルからサンプリングするレコードの最大数。 | `AUTO` または正の整数 |
| SAMPLE_TOTAL_RECORDS | 選択されたすべてのファイルにまたがってサンプリングするレコードの最大数。 | `AUTO` または正の整数 |

`SCHEMA_EVOLUTION` を省略した場合、{{{ .lake }}} は 3 つのサンプリングオプションすべてに `AUTO` を使用します。現在の `AUTO` の動作では、最大 64 ファイル、各ファイルあたり 1,000 レコード、合計 10,000 レコードまでサンプリングします。これらの内部デフォルト値は、将来のバージョンで変更される可能性があります。ロードがサンプリング戦略に敏感な場合は、`SAMPLE_FILES`、`SAMPLE_RECORDS_PER_FILE`、`SAMPLE_TOTAL_RECORDS` を明示的に設定してください。サンプルで検出されなかったカラムがロード中の後続データに現れた場合、COPY は失敗し、追加のカラム名を報告するため、サンプリング値を増やすことができます。

> **Tip:**
>
> ログのような大量のデータをインポートする場合は、`PURGE` と `FORCE` の両方を `true` に設定することを推奨します。これにより、Meta server とのやり取り（copied-files セットの更新）を必要とせず、効率的にデータをインポートできます。ただし、これにより重複データがインポートされる可能性がある点に注意してください。

## Output {#output}

COPY INTO は、以下のカラムを含むデータロード結果のサマリーを提供します。

| カラム           | Type    | Nullable | Description                                     |
| ---------------- | ------- | -------- | ----------------------------------------------- |
| FILE             | VARCHAR | NO       | ソースファイルへの相対パス。                    |
| ROWS_LOADED      | INT     | NO       | ソースファイルからロードされた行数。            |
| ERRORS_SEEN      | INT     | NO       | ソースファイル内のエラー行数                    |
| FIRST_ERROR      | VARCHAR | YES      | ソースファイルで最初に見つかったエラー。        |
| FIRST_ERROR_LINE | INT     | YES      | 最初のエラーの行番号。                          |

`RETURN_FAILED_ONLY` が `true` に設定されている場合、出力にはロードに失敗したファイルのみが含まれます。

## Examples {#examples}

外部ストレージソースでは、COPY 文で認証情報を直接指定する代わりに、`CONNECTION_NAME` パラメータを使用して事前作成済みの接続を利用することを推奨します。この方法により、セキュリティ、管理性、再利用性が向上します。接続の作成方法の詳細については、[CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) を参照してください。

### Example 1: Loading from Stages {#example-1-loading-from-stages}

以下の例は、さまざまな種類の stage から {{{ .lake }}} にデータをロードする方法を示しています。

<SimpleTab>

<div label="User Stage" value="user">

```sql
COPY INTO mytable
    FROM @~
    PATTERN = '.*[.]parquet'
    FILE_FORMAT = (TYPE = PARQUET);
```

</div>

<div label="Internal Stage" value="internal">

```sql
COPY INTO mytable
    FROM @my_internal_stage
    PATTERN = '.*[.]parquet'
    FILE_FORMAT = (TYPE = PARQUET);
```

</div>

<div label="External Stage" value="external">

```sql
COPY INTO mytable
    FROM @my_external_stage
    PATTERN = '.*[.]parquet'
    FILE_FORMAT = (TYPE = PARQUET);
```

</div>
</SimpleTab>

### 例 2: 外部ロケーションからのロード {#example-2-loading-from-external-locations}

以下の例では、さまざまな種類の外部ソースから {{{ .lake }}} にデータをロードする方法を示します。

<SimpleTab groupId="external-example">

<div label="Amazon S3" value="Amazon S3">

この例では、事前に作成した接続を使用して Amazon S3 からデータをロードします。

```sql
-- First create a connection (you only need to do this once)
CREATE CONNECTION my_s3_conn
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-ID>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

-- Use the connection to load data
COPY INTO mytable
    FROM 's3://mybucket/data.csv'
    CONNECTION = (CONNECTION_NAME = 'my_s3_conn')
    FILE_FORMAT = (
        TYPE = CSV,
        FIELD_DELIMITER = ',',
        RECORD_DELIMITER = '\n',
        SKIP_HEADER = 1
    );
```

**IAM Role を使用する場合（本番環境では推奨）**

```sql
-- Create connection using IAM role (more secure, recommended for production)
CREATE CONNECTION my_iam_conn
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::123456789012:role/my_iam_role';

-- Load CSV files using the IAM role connection
COPY INTO mytable
    FROM 's3://mybucket/'
    CONNECTION = (CONNECTION_NAME = 'my_iam_conn')
    PATTERN = '.*[.]csv'
    FILE_FORMAT = (
        TYPE = CSV,
        FIELD_DELIMITER = ',',
        RECORD_DELIMITER = '\n',
        SKIP_HEADER = 1
    );
```

</div>

<div label="Azure Blob Storage" value="Azure Blob Storage">

この例では、Azure Blob Storage に接続し、`data.csv` から {{{ .lake }}} にデータをロードします。

```sql
-- Create connection for Azure Blob Storage
CREATE CONNECTION my_azure_conn
    STORAGE_TYPE = 'azblob'
    ENDPOINT_URL = 'https://<account_name>.blob.core.windows.net'
    ACCOUNT_NAME = '<account_name>'
    ACCOUNT_KEY = '<account_key>';

-- Use the connection to load data
COPY INTO mytable
    FROM 'azblob://mybucket/data.csv'
    CONNECTION = (CONNECTION_NAME = 'my_azure_conn')
    FILE_FORMAT = (type = CSV);
```

</div>

<div label="Google Cloud Storage" value="Google Cloud Storage">

この例では、Google Cloud Storage に接続してデータをロードします。

```sql
-- Create connection for Google Cloud Storage
CREATE CONNECTION my_gcs_conn
    STORAGE_TYPE = 'gcs'
    CREDENTIAL = '<your-base64-encoded-credential>';

-- Use the connection to load data
COPY INTO mytable
    FROM 'gcs://mybucket/data.csv'
    CONNECTION = (CONNECTION_NAME = 'my_gcs_conn')
    FILE_FORMAT = (
        TYPE = CSV,
        FIELD_DELIMITER = ',',
        RECORD_DELIMITER = '\n',
        SKIP_HEADER = 1
    );
```

</div>

<div label="Remote Files" value="Remote Files">

この例では、3 つのリモート CSV ファイルからデータをロードし、エラーが発生した場合はそのファイルをスキップします。

```sql
COPY INTO mytable
    FROM 'https://lakesql-bin.tidbcloud.com/datasets/ontime_200{6,7,8}_200.csv'
    FILE_FORMAT = (type = CSV)
    ON_ERROR = continue;
```

</div>

<div label="IPFS" value="IPFS">

この例では、IPFS 上の CSV ファイルからデータをロードします。

```sql
COPY INTO mytable
    FROM 'ipfs://<your-ipfs-hash>'
    CONNECTION = (
        ENDPOINT_URL = 'https://<your-ipfs-gateway>'
    )
    FILE_FORMAT = (
        TYPE = CSV,
        FIELD_DELIMITER = ',',
        RECORD_DELIMITER = '\n',
        SKIP_HEADER = 1
    );
```

</div>
</SimpleTab>

### 例 3: 圧縮データのロード {#example-3-loading-compressed-data}

この例では、Amazon S3 上の GZIP 圧縮された CSV ファイルを {{{ .lake }}} にロードします。

```sql
-- Create connection for compressed data loading
CREATE CONNECTION compressed_s3_conn
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-ID>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

-- Load GZIP-compressed CSV file using the connection
COPY INTO mytable
    FROM 's3://mybucket/data.csv.gz'
    CONNECTION = (CONNECTION_NAME = 'compressed_s3_conn')
    FILE_FORMAT = (
        TYPE = CSV,
        FIELD_DELIMITER = ',',
        RECORD_DELIMITER = '\n',
        SKIP_HEADER = 1,
        COMPRESSION = AUTO
    );
```

### 例 4: PATTERN を使用したファイルのフィルタリング {#example-4-filtering-files-with-pattern}

この例では、PATTERN パラメータによるパターンマッチングを使用して、Amazon S3 から CSV ファイルをロードする方法を示します。ファイル名に `sales` を含み、拡張子が `.csv` のファイルをフィルタリングします。

```sql
-- Create connection for pattern-based file loading
CREATE CONNECTION pattern_s3_conn
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-ID>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

-- Load CSV files with 'sales' in their names using pattern matching
COPY INTO mytable
    FROM 's3://mybucket/'
    CONNECTION = (CONNECTION_NAME = 'pattern_s3_conn')
    PATTERN = '.*sales.*[.]csv'
    FILE_FORMAT = (
        TYPE = CSV,
        FIELD_DELIMITER = ',',
        RECORD_DELIMITER = '\n',
        SKIP_HEADER = 1
    );
```

ここで、`.*` は任意の文字が 0 回以上出現することを意味します。角括弧は、ファイル拡張子の前にあるピリオド文字 `.` をエスケープしています。

接続を使用してすべての CSV ファイルからロードするには、次のようにします。

```sql
COPY INTO mytable
    FROM 's3://mybucket/'
    CONNECTION = (CONNECTION_NAME = 'pattern_s3_conn')
    PATTERN = '.*[.]csv'
    FILE_FORMAT = (
        TYPE = CSV,
        FIELD_DELIMITER = ',',
        RECORD_DELIMITER = '\n',
        SKIP_HEADER = 1
    );
```

複数のフォルダを含むパス内の staged files に対してパターンを指定する場合、パターンは `@<stage_name>[/<path>]` より後のパス部分にのみ一致することに注意してください。たとえば、`FROM @sales_stage/raw/` の場合、ファイル `@sales_stage/raw/year=2025/month=01/sales_20250101.parquet` は `year=2025/month=01/sales_20250101.parquet` としてマッチされます。

- プレフィックスに続く特定のサブパスに一致させたい場合は、そのプレフィックスをパターンに含めて（例: `'year=2025/month=01/'`）、そのサブパス内で一致させたいパターン（例: `'sales_'`）を指定します。

    ```sql
    -- File path: raw/year=2025/month=01/sales_20250101.parquet
    COPY INTO ... FROM @sales_stage/raw/ PATTERN = 'year=2025/month=01/.*sales_.*[.]parquet') ...
    ```

- ファイルパス内の任意の場所に目的のパターンを含む部分に一致させたい場合は、パターンの前後に `.*` を付けて（例: `'.*sales_20250101.*'`）、パス内の `sales_20250101` の任意の出現箇所に一致させます。

    ```sql
    -- File path: raw/year=2025/month=01/sales_20250101.parquet
    COPY INTO ... FROM @sales_stage/raw/ PATTERN = '.*sales_20250101.*') ...
    ```

### 例 5: 追加カラムを持つテーブルへのロード {#example-5-loading-to-table-with-extra-columns}

このセクションでは、サンプルファイル [books.csv](https://lakesql-bin.tidbcloud.com/datasets/books.csv) を使用して、追加カラムを持つテーブルにデータをロードする方法を示します。

```text title='books.csv'
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

![Alt text](/media/tidb-cloud-lake/load-extra.png)

デフォルトでは、COPY INTO はファイル内のフィールドの順序をテーブル内の対応するカラムに対応付けて、テーブルにデータをロードします。ファイルとテーブルの間でデータが正しく対応していることを確認することが重要です。たとえば、次のようになります。

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR
);

COPY INTO books
    FROM 'https://lakesql-bin.tidbcloud.com/datasets/books.csv'
    FILE_FORMAT = (TYPE = CSV);
```

テーブルのカラム数がファイルより多い場合は、データをロードする対象のカラムを指定できます。たとえば、次のようになります。

```sql
CREATE TABLE books_with_language
(
    title VARCHAR,
    language VARCHAR,
    author VARCHAR,
    date VARCHAR
);

COPY INTO books_with_language (title, author, date)
    FROM 'https://lakesql-bin.tidbcloud.com/datasets/books.csv'
    FILE_FORMAT = (TYPE = CSV);
```

テーブルのカラム数がファイルより多く、追加カラムがテーブルの末尾にある場合は、[FILE_FORMAT](/tidb-cloud-lake/sql/input-output-file-formats.md) オプション `ERROR_ON_COLUMN_COUNT_MISMATCH` を使用してデータをロードできます。これにより、各カラムを個別に指定しなくてもデータをロードできます。なお、ERROR_ON_COLUMN_COUNT_MISMATCH は現在、CSV ファイル形式でのみ機能します。

```sql
CREATE TABLE books_with_extra_columns
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR,
    language VARCHAR,
    region VARCHAR
);

COPY INTO books_with_extra_columns
    FROM 'https://lakesql-bin.tidbcloud.com/datasets/books.csv'
    FILE_FORMAT = (TYPE = CSV, ERROR_ON_COLUMN_COUNT_MISMATCH = false);
```

> **Note:**
>
> テーブル内の追加カラムには、[CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) または [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#column-operations) によってデフォルト値を指定できます。追加カラムに対してデフォルト値が明示的に設定されていない場合は、そのデータ型に関連付けられたデフォルト値が適用されます。たとえば、整数型のカラムは、他の値が指定されていない場合、デフォルトで 0 になります。

### 例 6: カスタム形式での JSON のロード {#example-6-loading-json-with-custom-format}

この例では、次の内容を持つ CSV ファイル `data.csv` からデータをロードします。

```json
1,"U00010","{\"carPriceList\":[{\"carTypeId":10,\"distance":5860},{\"carTypeId":11,\"distance\":5861}]}"
2,"U00011","{\"carPriceList\":[{\"carTypeId":12,\"distance\":5862},{\"carTypeId":13,\"distance\":5863}]}"
```

各行には 3 つのカラムのデータが含まれており、3 番目のカラムは JSON データを含む文字列です。JSON フィールドを含む CSV データを正しくロードするには、適切なエスケープ文字を設定する必要があります。この例では、JSON データにダブルクォート `"` が含まれているため、バックスラッシュ `\` をエスケープ文字として使用します。

#### ステップ 1: カスタムファイル形式を作成する {#step-1-create-custom-file-format}

```sql
-- Define a custom CSV file format with the escape character set to backslash \
CREATE FILE FORMAT my_csv_format
    TYPE = CSV
    ESCAPE = '\\';
```

#### ステップ 2: ターゲットテーブルを作成する {#step-2-create-target-table}

```sql
CREATE TABLE t
  (
     id       INT,
     seq      VARCHAR,
     p_detail VARCHAR
  );
```

#### ステップ 3: カスタムファイル形式でロードする {#step-3-load-with-custom-file-format}

```sql
COPY INTO t FROM @t_stage FILES=('data.csv')
FILE_FORMAT=(FORMAT_NAME='my_csv_format');
```

### 例 7: 無効な JSON のロード {#example-7-loading-invalid-json}

Variant カラムにデータをロード (load) する際、{{{ .lake }}} はデータの妥当性を自動的にチェックし、無効なデータがある場合はエラーを返します。たとえば、ユーザー stage に `invalid_json_string.parquet` という名前の Parquet ファイルがあり、その中に次のような無効な JSON データが含まれているとします。

```sql
SELECT *
FROM @~/invalid_json_string.parquet;

┌────────────────────────────────────┐
│        a        │         b        │
├─────────────────┼──────────────────┤
│               5 │ {"k":"v"}        │
│               6 │ [1,              │
└────────────────────────────────────┘

DESC t2;

┌──────────────────────────────────────────────┐
│  Field │   Type  │  Null  │ Default │  Extra │
├────────┼─────────┼────────┼─────────┼────────┤
│ a      │ VARCHAR │ YES    │ NULL    │        │
│ b      │ VARIANT │ YES    │ NULL    │        │
└──────────────────────────────────────────────┘
```

このデータをテーブルにロードしようとすると、エラーが発生します。

```sql
COPY INTO t2 FROM @~/invalid_json_string.parquet FILE_FORMAT = (TYPE = PARQUET) ON_ERROR = CONTINUE;
error: APIError: ResponseError with 1006: EOF while parsing a value, pos 3 while evaluating function `parse_json('[1,')`
```

JSON の妥当性チェックを行わずにロードするには、COPY INTO 文で `DISABLE_VARIANT_CHECK` オプションを `true` に設定します。

```sql
COPY INTO t2 FROM @~/invalid_json_string.parquet
FILE_FORMAT = (TYPE = PARQUET)
DISABLE_VARIANT_CHECK = true
ON_ERROR = CONTINUE;

┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│             File            │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├─────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ invalid_json_string.parquet │           2 │           0 │ NULL             │             NULL │
└───────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT * FROM t2;
-- Invalid JSON is stored as null in the Variant column.
┌──────────────────────────────────────┐
│         a        │         b         │
├──────────────────┼───────────────────┤
│ 5                │ {"k":"v"}         │
│ 6                │ null              │
└──────────────────────────────────────┘
```

### 例 8: Schema Evolution を使用したロード {#example-8-loading-with-schema-evolution}

スキーマにターゲットテーブルに存在しないカラムを含む Parquet または NDJSON ファイルをロードする場合、Schema Evolution を使用して不足しているカラムを自動的に追加できます。Schema Evolution の推論を実行する stage または location からのロードでは、ロードを実行するロールにターゲットテーブルに対する `INSERT` および `ALTER` 権限が必要です。まず、テーブルで Schema Evolution を有効にします。

```sql
CREATE OR REPLACE TABLE invoices(order_id INT);

-- Enable schema evolution
ALTER TABLE invoices SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);
```

#### Parquet {#parquet}

次に、異なるスキーマを持つ Parquet ファイルをロードします。{{{ .lake }}} は新しいカラムを自動的に追加し、不足している値を `NULL` で埋めます。

```sql
-- Assume @my_stage contains Parquet files with extra columns (e.g., amount, currency)
COPY INTO invoices
    FROM @my_stage/
    FILE_FORMAT = (TYPE = PARQUET MISSING_FIELD_AS = FIELD_DEFAULT);
```

#### NDJSON {#ndjson}

NDJSON の場合、`COPY INTO` はデフォルトのサンプリング値を使用して不足しているカラムを推論します。{{{ .lake }}} が stage 上のファイルをどのようにサンプリングするかを上書きしたい場合にのみ、`SCHEMA_EVOLUTION` を追加してください。

```sql
CREATE OR REPLACE TABLE events(id INT);
ALTER TABLE events SET OPTIONS(ENABLE_SCHEMA_EVOLUTION = true);

-- Assume @events_stage contains NDJSON records such as:
-- {"id":1,"city":"SF","score":9}
COPY INTO events
    FROM @events_stage/
    FILE_FORMAT = (TYPE = NDJSON MISSING_FIELD_AS = FIELD_DEFAULT)
    SCHEMA_EVOLUTION = (
        SAMPLE_FILES = AUTO,
        SAMPLE_RECORDS_PER_FILE = AUTO,
        SAMPLE_TOTAL_RECORDS = AUTO
    );
```

{{{ .lake }}} は stage 上の NDJSON ファイルをサンプリングし、`city` や `score` などの推論されたフィールドを NULL 許容カラムとして追加してから、データをロードします。

詳細は、[Schema Evolution](/tidb-cloud-lake/guides/schema-evolution.md) を参照してください。