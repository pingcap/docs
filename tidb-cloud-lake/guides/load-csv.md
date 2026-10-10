---
title: TiDB Cloud Lake への CSV のロード
summary: CSV (Comma Separated Values) は、スプレッドシートやデータベースのような表形式データを保存するためのシンプルなファイル形式です。CSV ファイルはプレーンテキストファイルであり、データを表形式で保持します。各行は改行で表され、カラムは区切り文字で区切られます。
---

# TiDB Cloud Lake への CSV のロード

## CSV とは何ですか？ {#what-is-csv}

CSV (Comma Separated Values) は、スプレッドシートやデータベースのような表形式データを保存するためのシンプルなファイル形式です。CSV ファイルはプレーンテキストファイルであり、データを表形式で保持します。各行は改行で表され、カラムは区切り文字で区切られます。

次の例は、2 件のレコードを含む CSV ファイルを示しています。

```text
Title_0,Author_0
Title_1,Author_1
```

## CSV ファイルのロード {#loading-csv-file}

CSV ファイルをロード (load) する一般的な構文は次のとおりです。

```sql
COPY INTO [<database>.]<table_name>
FROM { userStage | internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
    TYPE = CSV,
    RECORD_DELIMITER = '<character>',
    FIELD_DELIMITER = '<character>',
    SKIP_HEADER = <integer>,
    COMPRESSION = AUTO
) ]
```

- CSV ファイル形式のオプションの詳細については、[CSV ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#csv-options) を参照してください。
- COPY INTO table オプションの詳細については、[COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md) を参照してください。

## チュートリアル: CSV ファイルからのデータのロード {#tutorial-loading-data-from-csv-files}

### Step 1. 内部 stage を作成する {#step-1-create-an-internal-stage}

CSV ファイルを保存するための内部 stage を作成します。

```sql
CREATE STAGE my_csv_stage;
```

### Step 2. CSV ファイルを作成する {#step-2-create-csv-files}

次の SQL 文を使用して CSV ファイルを生成します。

```sql
COPY INTO @my_csv_stage
FROM (
    SELECT
        'Title_' || CAST(number AS VARCHAR) AS title,
        'Author_' || CAST(number AS VARCHAR) AS author
    FROM numbers(100000)
)
    FILE_FORMAT = (TYPE = CSV, COMPRESSION = gzip)
;
```

CSV ファイルが作成されたことを確認します。

```sql
LIST @my_csv_stage;
```

結果:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │  size  │                 md5                │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_4bb7f864-f5f2-41e8-a442-68c2a709be5a_0000_00000000.csv.gz │ 483110 │ "0c8e28daed524468269e44ac13d2f463" │ 2023-12-26 11:37:21.000 +0000 │ NULL             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 3: 対象テーブルを作成する {#step-3-create-target-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### Step 4. CSV から直接コピーする {#step-4-copying-directly-from-csv}

CSV ファイルからテーブルに直接データをコピーするには、次の SQL コマンドを使用します。

```sql
COPY INTO books
FROM @my_csv_stage
PATTERN = '.*[.]csv.gz'
FILE_FORMAT = (
    TYPE = CSV,
    FIELD_DELIMITER = ',',
    RECORD_DELIMITER = '\n',
    SKIP_HEADER = 0, -- Skip the first line if it is a header, here we don't have a header
    COMPRESSION = AUTO
);
```

結果:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              File                              │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├────────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_4bb7f864-f5f2-41e8-a442-68c2a709be5a_0000_00000000.csv.gz │      100000 │           0 │ NULL             │             NULL │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4 (Option). SELECT を使用してデータをコピーする {#step-4-option-using-select-to-copy-data}

コピー中にデータを変換するなど、より細かく制御したい場合は、SELECT 文を使用します。詳細は [`CSV からの SELECT`](/tidb-cloud-lake/guides/query-csv-files-in-stage.md) を参照してください。

```sql
COPY INTO books (title, author)
FROM (
    SELECT $1, $2
    FROM @my_csv_stage
)
PATTERN = '.*[.]csv.gz'
FILE_FORMAT = (
    TYPE = 'CSV',
    FIELD_DELIMITER = ',',
    RECORD_DELIMITER = '\n',
    SKIP_HEADER = 0, -- Skip the first line if it is a header, here we don't have a header
    COMPRESSION = 'AUTO'
);
```