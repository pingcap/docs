---
title: ローカルファイルからのロード
summary: ローカルのデータファイルを {{{ .lake }}} にロードする前に stage やバケットへアップロードするのは、不要な場合があります。代わりに、{{{ .lake }}} ネイティブの CLI ツールである LakeSQL を使用して、データを直接インポートできます。これによりワークフローが簡素化され、ストレージ料金を節約できる場合があります。
---

# ローカルファイルからのロード

ローカルのデータファイルを {{{ .lake }}} にロードする前に stage やバケットへアップロードするのは、不要な場合があります。代わりに、{{{ .lake }}} ネイティブの CLI ツールである [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) を使用して、データを直接インポートできます。これによりワークフローが簡素化され、ストレージ料金を節約できる場合があります。

ファイルは {{{ .lake }}} がサポートする形式である必要があります。そうでない場合、データはインポートできません。{{{ .lake }}} がサポートするファイル形式の詳細については、[入出力ファイル形式](/tidb-cloud-lake/sql/input-output-file-formats.md) を参照してください。

また、JDBC または Python ドライバーを使用して、プログラムからローカルファイルをテーブルにロードすることもできます。

## ロード方法 {#load-methods}

ローカルファイルからデータをロードする方法は 2 つあります。

1. **Stage**: ローカルファイルを内部 stage にアップロードし、その後 stage 済みファイルからテーブルへデータをコピーします。ファイルのアップロードは、`presigned_url_disabled` 接続オプション（デフォルト: `false`）に応じて、lake-query 経由または presigned URL を使用して行われます。
2. **Streaming**: アップロード中にファイルを直接テーブルへロードします。オブジェクトストレージに単一オブジェクトとして保存するにはファイルが大きすぎる場合は、この方法を使用します。

## チュートリアル 1: ローカルファイルからロードする {#tutorial-1-load-from-a-local-file}

このチュートリアルでは、CSV ファイルを例として、ローカルソースから [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) を使用して {{{ .lake }}} にデータをインポートする方法を示します。

### 始める前に {#before-you-begin}

サンプルファイル [books.csv](https://lakesql-bin.tidbcloud.com/datasets/books.csv) をダウンロードし、ローカルフォルダーに保存します。このファイルには 2 件のレコードが含まれています。

```text title='books.csv'
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

### ステップ 1. データベースとテーブルを作成する {#step-1-create-database-and-table}

```shell
❯ lakesql
root@localhost:8000/default> CREATE DATABASE book_db;

root@localhost:8000/default> USE book_db;

root@localhost:8000/book_db> CREATE TABLE books
(
    title VARCHAR,
    author VARCHAR,
    date VARCHAR
);

CREATE TABLE books (
  title VARCHAR,
  author VARCHAR,
  date VARCHAR
)
```

### ステップ 2. テーブルにデータをロードする {#step-2-load-data-into-table}

次のコマンドでデータロードリクエストを送信します。

```shell
❯ lakesql --query='INSERT INTO book_db.books from @_databend_load file_format=(type=csv)' --data=@books.csv
```

- `@_databend_load` は、ローカルファイルデータを表すプレースホルダーです。
- [file_format 句](/tidb-cloud-lake/sql/input-output-file-formats.md) は、COPY コマンドと同じ構文を使用します。

または、Python スクリプトを使用します。

```python
import tidbcloudlake_driver
dsn = "lake://root:@localhost:8000/?sslmode=disable"
client = tidbcloudlake_driver.BlockingLakeClient(dsn)
conn = client.get_conn()
query = "INSERT INTO book_db.books from @_databend_load file_format=(type=csv)"
progress = conn.load_file(query, "book.csv")
conn.close()
```

または、Java コードを使用します。

```java
import java.io.File;
import java.io.FileInputStream;
import java.sql.Connection;
import java.sql.DriverManager;

import com.tidbcloud.jdbc.LakeConnection;

String url = "jdbc:lake://localhost:8000";
File file = new File("book.csv");

try (FileInputStream fileInputStream = new FileInputStream(file);
     Connection connection = DriverManager.getConnection(url, "tidbcloud", "tidbcloud")) {

    LakeConnection lakeConnection = connection.unwrap(LakeConnection.class);

    String sql =
        "INSERT INTO book_db.books FROM @_databend_load FILE_FORMAT=(TYPE=CSV)";

    int nUpdate = lakeConnection.loadStreamToTable(
        sql,
        fileInputStream,
        file.length(),
        LakeConnection.LoadMethod.Stage
    );
}
```

> **Note:**
>
> ローカルの LakeSQL から {{{ .lake }}} のバックエンドオブジェクトストレージへ直接接続できることを確認してください。
> できない場合は、`--set presigned_url_disabled=1` オプションを指定して presigned url 機能を無効にする必要があります。

### ステップ 3. ロードしたデータを確認する {#step-3-verify-loaded-data}

```shell
root@localhost:8000/book_db> SELECT * FROM books;

┌───────────────────────────────────────────────────────────────────────┐
│             title            │        author       │       date       │
│       Nullable(String)       │   Nullable(String)  │ Nullable(String) │
├──────────────────────────────┼─────────────────────┼──────────────────┤
│ Transaction Processing       │ Jim Gray            │ 1992             │
│ Readings in Database Systems │ Michael Stonebraker │ 2004             │
└───────────────────────────────────────────────────────────────────────┘
```

## チュートリアル 2: 指定したカラムにロードする {#tutorial-2-load-into-specified-columns}

[チュートリアル 1](#tutorial-1-load-from-a-local-file) では、サンプルファイル内のデータと完全に一致する 3 つのカラムを持つテーブルを作成しました。テーブルの指定したカラムにデータをロードすることもできるため、指定したカラムが一致していれば、ロード対象のデータとテーブルが同じカラムを持っている必要はありません。このチュートリアルでは、その方法を示します。

### 始める前に {#before-you-begin}

このチュートリアルを始める前に、[チュートリアル 1](#tutorial-1-load-from-a-local-file) を完了していることを確認してください。

### ステップ 1. テーブルを作成する {#step-1-create-table}

テーブル `books` と比べて、`comments` という追加カラムを含むテーブルを作成します。

```shell
root@localhost:8000/book_db> CREATE TABLE bookcomments
(
    title VARCHAR,
    author VARCHAR,
    comments VARCHAR,
    date VARCHAR
);

CREATE TABLE bookcomments (
  title VARCHAR,
  author VARCHAR,
  comments VARCHAR,
  date VARCHAR
)
```

### ステップ 2. テーブルにデータをロードする {#step-2-load-data-into-table}

次のコマンドでデータロードリクエストを送信します。

```shell
❯ lakesql --query='INSERT INTO book_db.bookcomments(title,author,date) file_format=(type=csv)'  --data=@books.csv
```

上記の `query` 部分では、ロードするデータに対応するカラムとして (title, author, date) が指定されていることに注意してください。

### ステップ 3. ロードしたデータを確認する {#step-3-verify-loaded-data}

```shell
root@localhost:8000/book_db> SELECT * FROM bookcomments;

┌──────────────────────────────────────────────────────────────────────────────────────────┐
│             title            │        author       │     comments     │       date       │
│       Nullable(String)       │   Nullable(String)  │ Nullable(String) │ Nullable(String) │
├──────────────────────────────┼─────────────────────┼──────────────────┼──────────────────┤
│ Transaction Processing       │ Jim Gray            │ NULL             │ 1992             │
│ Readings in Database Systems │ Michael Stonebraker │ NULL             │ 2004             │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```