---
title: TiDB Cloud Lake への Parquet のロード
summary: Parquet は、データ分析で一般的に使用されるカラム指向のストレージ形式です。複雑なデータ構造をサポートするように設計されており、大規模なデータセットの処理に効率的です。
---

# TiDB Cloud Lake への Parquet のロード

## Parquet とは {#what-is-parquet}

Parquet は、データ分析で一般的に使用されるカラム指向のストレージ形式です。複雑なデータ構造をサポートするように設計されており、大規模なデータセットの処理に効率的です。

Parquet ファイルは {{{ .lake }}} に最も適しています。{{{ .lake }}} のデータソースとして Parquet ファイルを使用することを推奨します。

## Parquet ファイルのロード {#loading-parquet-file}

Parquet ファイルをロードする一般的な構文は次のとおりです。

```sql
COPY INTO [<database>.]<table_name>
     FROM { internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
FILE_FORMAT = (TYPE = PARQUET)
```

- Parquet ファイル形式のオプションの詳細については、[Parquet ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#parquet-options) を参照してください。
- COPY INTO table オプションの詳細については、[COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md) を参照してください。

## チュートリアル: Parquet ファイルからのデータのロード {#tutorial-loading-data-from-parquet-files}

### Step 1. 内部 stage を作成する {#step-1-create-an-internal-stage}

Parquet ファイルを保存するための内部 stage を作成します。

```sql
CREATE STAGE my_parquet_stage;
```

### Step 2. Parquet ファイルを作成する {#step-2-create-parquet-files}

次の SQL ステートメントを使用して Parquet ファイルを生成します。

```sql
COPY INTO @my_parquet_stage
FROM (
    SELECT
        'Title_' || CAST(number AS VARCHAR) AS title,
        'Author_' || CAST(number AS VARCHAR) AS author
    FROM numbers(100000)
)
    FILE_FORMAT = (TYPE = PARQUET);
```

Parquet ファイルが作成されたことを確認します。

```sql
LIST @my_parquet_stage;
```

結果:

```text

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               name                              │  size  │                 md5                │         last_modified         │      creator     │
├─────────────────────────────────────────────────────────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_3890e0b1-0233-422c-b506-3a4501602f28_0000_00000000.parquet │  65443 │ "ab4631846ca8a2beed6a48be75d2acac" │ 2023-12-26 10:28:18.000 +0000 │ NULL             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

データを stage にアンロード (unload) する詳細については、[COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md) を参照してください。

### Step 3. ターゲットテーブルを作成する {#step-3-create-target-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### Step 4. Parquet から直接コピーする {#step-4-copying-directly-from-parquet}

Parquet ファイルからテーブルに直接データをコピーするには、次の SQL コマンドを使用します。

```sql
COPY INTO books
    FROM @my_parquet_stage
    PATTERN = '.*[.]parquet'
    FILE_FORMAT = (TYPE = PARQUET);
```

結果:

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               File                              │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├─────────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_3890e0b1-0233-422c-b506-3a4501602f28_0000_00000000.parquet │      100000 │           0 │ NULL             │             NULL │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 5 (任意). SELECT を使用してデータをコピーする {#step-5-optional-using-select-to-copy-data}

コピー中にデータを変換するなど、より細かく制御したい場合は、SELECT ステートメントを使用します。詳細は [`Parquet からの SELECT`](/tidb-cloud-lake/guides/query-parquet-files-in-stage.md) を参照してください。

```sql
COPY INTO books (title, author)
FROM (
    SELECT title, author
    FROM @my_parquet_stage
)
PATTERN = '.*[.]parquet'
FILE_FORMAT = (TYPE = PARQUET);
```