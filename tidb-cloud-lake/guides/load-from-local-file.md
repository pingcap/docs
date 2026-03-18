---
title: Loading from Local File
sidebar_label: Local
---

Uploading your local data files to a stage or bucket before loading them into Databend can be unnecessary. Instead, you can use [BendSQL](/tidb-cloud-lake/guides/connect-using-bendsql.md), the Databend native CLI tool, to directly import the data. This simplifies the workflow and can save you storage fees.

Please note that the files must be in a format supported by Databend, otherwise the data cannot be imported. For more information on the file formats supported by Databend, see [Input & Output File Formats](/tidb-cloud-lake/sql/input-output-file-formats.md).

You can also load local files into tables programmatically using JDBC or Python drivers.

## Load Methods

There are two methods to load data from local files:

1. **Stage**: Upload the local file to an internal stage, then copy data from the staged file into the table. File upload occurs either through databend-query or using a presigned URL, depending on the `presigned_url_disabled` connection option (default: `false`).
2. **Streaming**: Load the file directly into the table during upload. Use this method when the file is too large to store as a single object in your object storage.

## Tutorial 1 - Load from a Local File

This tutorial uses a CSV file as an example to demonstrate how to import data into Databend using [BendSQL](/tidb-cloud-lake/guides/connect-using-bendsql.md) from a local source.

### Before You Begin

Download and save the sample file [books.csv](https://datafuse-1253727613.cos.ap-hongkong.myqcloud.com/data/books.csv) to a local folder. The file contains two records:

```text title='books.csv'
Transaction Processing,Jim Gray,1992
Readings in Database Systems,Michael Stonebraker,2004
```

### Step 1. Create Database and Table

```shell
❯ bendsql
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

### Step 2. Load Data into Table

Send loading data request with the following command:

```shell
❯ bendsql --query='INSERT INTO book_db.books from @_databend_load file_format=(type=csv)' --data=@books.csv
```

- The `@_databend_load` is a placeholder representing local file data.
- The [file_format clause](/tidb-cloud-lake/sql/input-output-file-formats.md) uses the same syntax as the COPY command.

Alternatively, use a Python script:

```python
    import databend_driver
    dsn = "databend://root:@localhost:8000/?sslmode=disable",
    client = databend_driver.BlockingDatabendClient(dsn)
    conn = client.get_conn()
    query = "INSERT INTO book_db.books from @_databend_load file_format=(type=csv)"
    progress = conn.load_file(query, "book.csv")
    conn.close()
```

Or use Java code:

```java
import java.sql.Connection;
import java.sql.Statement;
import java.io.FileInputStream;
import java.nio.file.Files;
import com.databend.jdbc.DatabendConnection;
String url = "jdbc:databend://localhost:8000";
try (FileInputStream fileInputStream = new FileInputStream(new File("book.csv")));
     Connection connection = DriverManager.getConnection(url, "databend", "databend");
      Statement statement = connection.createStatement()) {
    DatabendConnection databendConnection = connection.unwrap(DatabendConnection.class);
    String sql = "insert into  book_db.books from @_databend_load file_format=(type=csv)";
    int nUpdate = databendConnection.loadStreamToTable(sql, fileInputStream, f.length(), DatabendConnection.LoadMethod.Stage);
}
```

> **Note:**
>
> Be sure that you are able to connect to the backend object storage for Databend from local BendSQL directly.
> If not, you need to specify the `--set presigned_url_disabled=1` option to disable the presigned url feature.


### Step 3. Verify Loaded Data

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

## Tutorial 2 - Load into Specified Columns

In [Tutorial 1](#tutorial-1---load-from-a-local-file), you created a table containing three columns that exactly match the data in the sample file. You can also load data into specified columns of a table, so the table does not need to have the same columns as the data to be loaded as long as the specified columns can match. This tutorial shows how to do that.

### Before You Begin

Before you start this tutorial, make sure you have completed [Tutorial 1](#tutorial-1---load-from-a-local-file).

### Step 1. Create Table

Create a table including an extra column named "comments" compared to the table "books":

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

### Step 2. Load Data into Table

Send loading data request with the following command:

```shell
❯ bendsql --query='INSERT INTO book_db.bookcomments(title,author,date) file_format=(type=csv)'  --data=@books.csv
```

Notice that the `query` part above specifies the columns (title, author, and date) to match the loaded data.

### Step 3. Verify Loaded Data

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
