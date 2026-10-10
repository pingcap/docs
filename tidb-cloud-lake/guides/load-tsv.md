---
title: TiDB Cloud Lake への TSV のロード
summary: TSV（Tab Separated Values）は、スプレッドシートやデータベースのような表形式データを保存するためのシンプルなファイル形式です。TSV ファイル形式は CSV と非常によく似ており、レコードは改行で区切られ、各フィールドはタブで区切られます。次の例は、2 つのレコードを含む TSV ファイルを示しています。
---

# TiDB Cloud Lake への TSV のロード

## TSV とは何ですか？ {#what-is-tsv}

TSV（Tab Separated Values、{{{ .lake }}} `v1.2.890-nightly` 以降では `TEXT` と呼ばれます）は、スプレッドシートやデータベースのような表形式データを保存するためのシンプルなファイル形式です。TSV ファイル形式は CSV と非常によく似ており、レコードは改行で区切られ、各フィールドはタブで区切られます。

次の例は、2 つのレコードを含む TSV ファイルを示しています。

```text
Title_0 Author_0
Title_1 Author_1
```

## TSV ファイルのロード {#loading-tsv-file}

TSV ファイルをロード (load) する一般的な構文は次のとおりです。

```sql
COPY INTO [<database>.]<table_name>
FROM { userStage | internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
[ FILE_FORMAT = (
    TYPE = TSV,
    SKIP_HEADER = <integer>,
    COMPRESSION = AUTO
) ]
```

> **Note:**
>
> {{{ .lake }}} `v1.2.890-nightly` 以降では、`TEXT` が `TSV` のエイリアスとしてサポートされています。このガイドでは、古いサーバーバージョンでも引き続き動作するよう、例では `TYPE = TSV` を使用しています。対象が `v1.2.890-nightly` 以降のみであれば、代わりに `TYPE = TEXT` を使用できます。

- TSV ファイル形式のオプションの詳細については、[TSV ファイル形式オプション](/tidb-cloud-lake/sql/input-output-file-formats.md#tsv-options) を参照してください。
- COPY INTO table のオプションの詳細については、[COPY INTO table](/tidb-cloud-lake/sql/copy-into-table.md) を参照してください。

## チュートリアル: TSV ファイルからのデータのロード {#tutorial-loading-data-from-tsv-files}

### ステップ 1. Internal Stage を作成する {#step-1-create-an-internal-stage}

TSV ファイルを保存するための internal stage を作成します。

```sql
CREATE STAGE my_tsv_stage;
```

### ステップ 2. TSV ファイルを作成する {#step-2-create-tsv-files}

次の SQL 文を使用して TSV ファイルを生成します。

```sql
COPY INTO @my_tsv_stage
FROM (
    SELECT
        'Title_' || CAST(number AS VARCHAR) AS title,
        'Author_' || CAST(number AS VARCHAR) AS author
    FROM numbers(100000)
)
    FILE_FORMAT = (TYPE = TSV)
;
```

TSV ファイルが作成されたことを確認します。

```sql
LIST @my_tsv_stage;
```

結果:

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             name                            │   size  │                 md5                │         last_modified         │      creator     │
├─────────────────────────────────────────────────────────────┼─────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ data_7413d5d0-f992-4d92-b28e-0e501d66bdc1_0000_00000000.tsv │ 2477780 │ "a906769144de7aa6a0056a86ddae97d2" │ 2023-12-26 11:56:19.000 +0000 │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### ステップ 3: 対象テーブルを作成する {#step-3-create-target-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR
);
```

### ステップ 4. TSV から直接コピーする {#step-4-copying-directly-from-tsv}

TSV ファイルからテーブルに直接データをコピーするには、次の SQL コマンドを使用します。

```sql
COPY INTO books
FROM @my_tsv_stage
PATTERN = '.*[.]tsv'
FILE_FORMAT = (
    TYPE = TSV,
    SKIP_HEADER = 0, -- Skip the first line if it is a header, here we don't have a header
    COMPRESSION = AUTO
);
```

結果:

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             File                            │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├─────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ data_7413d5d0-f992-4d92-b28e-0e501d66bdc1_0000_00000000.tsv │      100000 │           0 │ NULL             │             NULL │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### ステップ 4（オプション）. SELECT を使用してデータをコピーする {#step-4-option-using-select-to-copy-data}

コピー中にデータを変換するなど、より細かく制御したい場合は、SELECT 文を使用します。詳細は [`TSV からの SELECT`](/tidb-cloud-lake/guides/query-tsv-files-in-stage.md) を参照してください。

```sql
COPY INTO books (title, author)
FROM (
    SELECT $1, $2
    FROM @my_tsv_stage
)
PATTERN = '.*[.]tsv'
FILE_FORMAT = (
    TYPE = 'TSV',
    SKIP_HEADER = 0, -- Skip the first line if it is a header, here we don't have a header
    COMPRESSION = 'AUTO'
);
```