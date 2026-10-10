---
title: リモートファイルからのロード
summary: リモートファイルから {{{ .lake }}} にデータをロードするには、COPY INTO コマンドを使用できます。このコマンドを使用すると、リモートファイルを含むさまざまなソースから {{{ .lake }}} に簡単にデータをコピーできます。COPY INTO では、ソースファイルの場所、ファイル形式、そのほかの関連パラメータを指定して、インポート処理を要件に合わせて調整できます。ファイルは {{{ .lake }}} でサポートされている形式である必要があり、そうでない場合はデータをインポートできません。{{{ .lake }}} でサポートされているファイル形式の詳細については、Input & Output File Formats を参照してください。
---

# リモートファイルからのロード

リモートファイルから {{{ .lake }}} にデータをロードするには、[COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) コマンドを使用できます。このコマンドを使用すると、リモートファイルを含むさまざまなソースから {{{ .lake }}} に簡単にデータをコピーできます。COPY INTO では、ソースファイルの場所、ファイル形式、そのほかの関連パラメータを指定して、インポート処理を要件に合わせて調整できます。ファイルは {{{ .lake }}} でサポートされている形式である必要があり、そうでない場合はデータをインポートできません。{{{ .lake }}} でサポートされているファイル形式の詳細については、[入出力ファイル形式](/tidb-cloud-lake/sql/input-output-file-formats.md) を参照してください。

## glob パターンを使用したロード {#loading-with-glob-patterns}

{{{ .lake }}} では、glob パターンを使用してリモートファイルからデータをロードできます。これらのパターンにより、特定の命名規則に従う複数のファイルから、効率的かつ柔軟にデータをインポートできます。{{{ .lake }}} は次の glob パターンをサポートしています。

### セットパターン {#set-pattern}

glob 式のセットパターンを使用すると、セット内のいずれか 1 文字に一致させることができます。たとえば、`data_file_a.csv`、`data_file_b.csv`、`data_file_c.csv` という名前のファイルがあるとします。セットパターンを使用して、これら 3 つのファイルすべてからデータをロードできます。

```sql
COPY INTO your_table
FROM 'https://your-remote-location/data_file_{a,b,c}.csv' ...
```

### 範囲パターン {#range-pattern}

`data_file_001.csv`、`data_file_002.csv`、`data_file_003.csv` のような名前のファイルを扱う場合は、範囲パターンが便利です。次のように範囲パターンを使用して、この一連のファイルからデータをロードできます。

```sql
COPY INTO your_table
FROM 'https://your-remote-location/data_file_[001-003].csv' ...
```

## チュートリアル - リモートファイルからのロード {#tutorial-load-from-a-remote-file}

このチュートリアルでは、リモート CSV ファイルから {{{ .lake }}} にデータをインポートする方法を示します。サンプルファイル [books.csv](https://lakesql-bin.tidbcloud.com/datasets/books.csv) には 2 件のレコードが含まれています。

```text title='books.csv'
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

### ステップ 1. テーブルを作成する {#step-1-create-table}

```sql
CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR
);
```

### ステップ 2. テーブルにデータをロードする {#step-2-load-data-into-table}

```sql
COPY INTO books
FROM 'https://lakesql-bin.tidbcloud.com/datasets/books.csv'
FILE_FORMAT = (
    TYPE = 'CSV',
    FIELD_DELIMITER = ',',
    RECORD_DELIMITER = '\n',
    SKIP_HEADER = 0
);
```

### ステップ 3. ロードされたデータを確認する {#step-3-verify-loaded-data}

```sql
SELECT * FROM books;
```

```text title='Result:'
┌──────────────────────────────────┬─────────────────────┬───────┐
│ title                            │ author              │ date  │
├──────────────────────────────────┼─────────────────────┼───────┤
│ Transaction Processing           │ Jim Gray            │ 1992  │
│ Readings in Database Systems     │ Michael Stonebraker │ 2004  │
└──────────────────────────────────┴─────────────────────┴───────┘
```