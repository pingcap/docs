---
title: TiDB Cloud Lake への NDJSON のロード
summary: NDJSON は JSON を基にした形式であり、JSON の厳密なサブセットです。各行には、それぞれ独立した有効な JSON オブジェクトが含まれている必要があります。
---

# TiDB Cloud Lake への NDJSON のロード

## NDJSON とは何ですか？ {#what-is-ndjson}

NDJSON は JSON を基にした形式であり、JSON の厳密なサブセットです。各行には、それぞれ独立した有効な JSON オブジェクトが含まれている必要があります。

次の例は、2 つの JSON オブジェクトを含む NDJSON ファイルを示しています。

```text
{"title":"Title_0","author":"Author_0"}
{"title":"Title_1","author":"Author_1"}
```

## NDJSON ファイルのロード {#loading-ndjson-file}

NDJSON ファイルをロード (load) する一般的な構文は次のとおりです。

```sql
COPY INTO [<database>.]<table_name>
FROM { userStage | internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
    TYPE = NDJSON,
    COMPRESSION = AUTO
) ]
```

- NDJSON ファイル形式のオプションの詳細については、[NDJSON ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#ndjson-options) を参照してください。
- COPY INTO table オプションの詳細については、[COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md) を参照してください。

## チュートリアル: NDJSON ファイルからのデータのロード {#tutorial-loading-data-from-ndjson-files}

### ステップ 1. internal stage を作成する {#step-1-create-an-internal-stage}

NDJSON ファイルを保存するための internal stage を作成します。

```sql
CREATE STAGE my_ndjson_stage;
```

### ステップ 2. NDJSON ファイルを作成する {#step-2-create-ndjson-files}

次の SQL 文を使用して NDJSON ファイルを生成します。

```sql
COPY INTO @my_ndjson_stage
FROM (
    SELECT
        'Title_' || CAST(number AS VARCHAR) AS title,
        'Author_' || CAST(number AS VARCHAR) AS author
    FROM numbers(100000)
)
    FILE_FORMAT = (TYPE = NDJSON)
;
```

NDJSON ファイルが作成されたことを確認します。

```sql
LIST @my_ndjson_stage;
```

結果:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              name                              │   size  │                 md5                │         last_modified         │      creator     │
├────────────────────────────────────────────────────────────────┼─────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_b3d94fad-3052-42e4-b090-26409e88c7b9_0000_00000000.ndjson │ 4777780 │ "d1cc98fefc3e3aa0649cade880d754aa" │ 2023-12-26 12:15:59.000 +0000 │ NULL             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### ステップ 3: 対象テーブルを作成する {#step-3-create-target-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### ステップ 4. NDJSON から直接コピーする {#step-4-copying-directly-from-ndjson}

NDJSON ファイルからテーブルに直接データをコピーするには、次の SQL コマンドを使用します。

```sql
COPY INTO books
FROM @my_ndjson_stage
PATTERN = '.*[.]ndjson'
FILE_FORMAT = (
    TYPE = NDJSON
);
```

結果:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              File                              │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├────────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_b3d94fad-3052-42e4-b090-26409e88c7b9_0000_00000000.ndjson │      100000 │           0 │ NULL             │             NULL │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### ステップ 4（オプション）. SELECT を使用してデータをコピーする {#step-4-option-using-select-to-copy-data}

コピー中にデータを変換するなど、より細かく制御したい場合は、SELECT 文を使用します。詳細は [`SELECT from NDJSON`](/tidb-cloud-lake/guides/query-ndjson-files-in-stage.md) を参照してください。

```sql
COPY INTO books(title, author)
FROM (
    SELECT $1:title, $1:author
    FROM @my_ndjson_stage
)
PATTERN = '.*[.]ndjson'
FILE_FORMAT = (
    TYPE = NDJSON
);
```