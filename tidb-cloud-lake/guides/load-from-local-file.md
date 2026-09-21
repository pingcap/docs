---
title: 从本地文件加载
summary: 在将本地数据文件加载到 {{{ .lake }}} 之前，先将其上传到 stage 或存储桶可能并非必要。相反，你可以使用 {{{ .lake }}} 原生 CLI 工具 LakeSQL 直接导入数据。这样可以简化工作流，并节省存储费用。
---

# 从本地文件加载

在将本地数据文件加载到 {{{ .lake }}} 之前，先将其上传到 stage 或存储桶可能并非必要。相反，你可以使用 [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md)（{{{ .lake }}} 原生 CLI 工具）直接导入数据。这样可以简化工作流，并节省存储费用。

请注意，文件必须采用 {{{ .lake }}} 支持的格式，否则无法导入数据。有关 {{{ .lake }}} 支持的文件格式的更多信息，请参见 [输入与输出文件格式](/tidb-cloud-lake/sql/input-output-file-formats.md)。

你还可以使用 JDBC 或 Python 驱动，以编程方式将本地文件加载到表中。

## 加载方法 {#load-methods}

从本地文件加载数据有两种方法：

1. **Stage**：先将本地文件上传到内部 stage，然后将已暂存文件中的数据复制到表中。文件上传通过 lake-query 或 presigned URL 进行，具体取决于连接选项 `presigned_url_disabled`（默认值：`false`）。
2. **Streaming**：在上传过程中将文件直接加载到表中。当文件过大，无法作为单个对象存储在对象存储中时，请使用此方法。

## 教程 1：从本地文件加载 {#tutorial-1-load-from-a-local-file}

本教程以 CSV 文件为例，演示如何使用 [LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) 从本地源将数据导入到 {{{ .lake }}}。

### 开始之前 {#before-you-begin}

下载示例文件 [books.csv](https://lakesql-bin.tidbcloud.com/datasets/books.csv) 并将其保存到本地文件夹中。该文件包含两条记录：

```text title='books.csv'
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

### 步骤 1：创建数据库和表 {#step-1-create-database-and-table}

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

### 步骤 2：将数据加载到表中 {#step-2-load-data-into-table}

使用以下命令发送加载数据请求：

```shell
❯ lakesql --query='INSERT INTO book_db.books from @_databend_load file_format=(type=csv)' --data=@books.csv
```

- `@_databend_load` 是一个占位符，表示本地文件数据。
- [file_format 子句](/tidb-cloud-lake/sql/input-output-file-formats.md) 使用与 COPY 命令相同的语法。

或者，使用 Python 脚本：

```python
import tidbcloudlake_driver
dsn = "lake://root:@localhost:8000/?sslmode=disable"
client = tidbcloudlake_driver.BlockingLakeClient(dsn)
conn = client.get_conn()
query = "INSERT INTO book_db.books from @_databend_load file_format=(type=csv)"
progress = conn.load_file(query, "book.csv")
conn.close()
```

或者，使用 Java 代码：

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
> 请确保你本地的 LakeSQL 可以直接连接到 {{{ .lake }}} 的后端对象存储。
> 如果不能，则需要指定 `--set presigned_url_disabled=1` 选项以禁用 presigned url 功能。

### 步骤 3：验证已加载的数据 {#step-3-verify-loaded-data}

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

## 教程 2：加载到指定列 {#tutorial-2-load-into-specified-columns}

在 [教程 1](#tutorial-1-load-from-a-local-file) 中，你创建了一个包含三列的表，这三列与示例文件中的数据完全对应。你也可以将数据加载到表中的指定列，因此表不需要与待加载数据具有完全相同的列，只要指定的列能够匹配即可。本教程将介绍如何实现这一点。

### 开始之前 {#before-you-begin}

开始本教程之前，请确保你已完成 [教程 1](#tutorial-1-load-from-a-local-file)。

### 步骤 1：创建表 {#step-1-create-table}

创建一个名为 "bookcomments" 的表，与 "books" 表相比，它额外包含一列 "comments"：

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

### 步骤 2：将数据加载到表中 {#step-2-load-data-into-table}

使用以下命令发送加载数据请求：

```shell
❯ lakesql --query='INSERT INTO book_db.bookcomments(title,author,date) file_format=(type=csv)'  --data=@books.csv
```

请注意，上述 `query` 部分指定了列（title、author 和 date）以匹配加载的数据。

### 步骤 3：验证已加载的数据 {#step-3-verify-loaded-data}

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