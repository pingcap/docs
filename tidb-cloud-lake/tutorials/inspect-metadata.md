---
title: Inspect Databend Metadata
---

In this tutorial, we'll walk you through uploading a sample Parquet file to an internal stage, inferring the column definitions, and creating a table that includes file-level metadata fields. This is useful when you want to track the origin of each row or include metadata like file names and row numbers in your dataset.

### Before You Start

Before you start, ensure you have the following prerequisites in place:

- [Download the sample dataset](https://datasets.databend.com/iris.parquet) and save it to your local folder.
- BendSQL is installed on your local machine. See [Installing BendSQL](/guides/connect/sql-clients/bendsql/#installing-bendsql) for instructions on how to install BendSQL using various package managers.

### Step 1: Create an internal stage

```sql
CREATE STAGE my_internal_stage;
```

### Step 2: Upload the sample file using BendSQL

Assuming your sample dataset is located at `/Users/eric/Documents/iris.parquet`, run the following command in BendSQL to upload it to the stage:

```sql
PUT fs:///Users/eric/Documents/iris.parquet @my_internal_stage;
```

```sql
┌───────────────────────────────────────────────────────┐
│                file                │  status │  size  │
├────────────────────────────────────┼─────────┼────────┤
│ /Users/eric/Documents/iris.parquet │ SUCCESS │   6164 │
└───────────────────────────────────────────────────────┘
```

### Step 3: Query column definitions from the staged file
:::caution

`infer_schema` currently only supports parquet file format.

:::

```sql
SELECT * FROM INFER_SCHEMA(location => '@my_internal_stage/iris.parquet');
```

```sql
┌──────────────────────────────────────────────┐
│  column_name │   type  │ nullable │ order_id │
├──────────────┼─────────┼──────────┼──────────┤
│ id           │ BIGINT  │ true     │        0 │
│ sepal_length │ DOUBLE  │ true     │        1 │
│ sepal_width  │ DOUBLE  │ true     │        2 │
│ petal_length │ DOUBLE  │ true     │        3 │
│ petal_width  │ DOUBLE  │ true     │        4 │
│ species      │ VARCHAR │ true     │        5 │
└──────────────────────────────────────────────┘
```

### Step 4: Preview file content with metadata fields

You can use metadata fields such as `metadata$filename` and `metadata$file_row_number` to inspect file-level information:

```sql
SELECT
  metadata$filename,
  metadata$file_row_number,
  *
FROM @my_internal_stage/iris.parquet
LIMIT 5;
```

```sql
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ metadata$filename │ metadata$file_row_number │        id       │    sepal_length   │    sepal_width    │    petal_length   │    petal_width    │      species     │ metadata$filename │ metadata$file_row_number │
├───────────────────┼──────────────────────────┼─────────────────┼───────────────────┼───────────────────┼───────────────────┼───────────────────┼──────────────────┼───────────────────┼──────────────────────────┤
│ iris.parquet      │                        0 │               1 │               5.1 │               3.5 │               1.4 │               0.2 │ setosa           │ iris.parquet      │                        0 │
│ iris.parquet      │                        1 │               2 │               4.9 │                 3 │               1.4 │               0.2 │ setosa           │ iris.parquet      │                        1 │
│ iris.parquet      │                        2 │               3 │               4.7 │               3.2 │               1.3 │               0.2 │ setosa           │ iris.parquet      │                        2 │
│ iris.parquet      │                        3 │               4 │               4.6 │               3.1 │               1.5 │               0.2 │ setosa           │ iris.parquet      │                        3 │
│ iris.parquet      │                        4 │               5 │                 5 │               3.6 │               1.4 │               0.2 │ setosa           │ iris.parquet      │                        4 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 5: Create a table including metadata fields

Let’s create a table that includes the inferred columns plus metadata fields like filename and row number:

```sql
CREATE TABLE iris_with_meta AS
SELECT
  metadata$filename AS iris_file,
  metadata$file_row_number AS row_index,
  sepal_length,
  sepal_width,
  petal_length,
  petal_width,
  species
FROM @my_internal_stage/iris.parquet;
```

### Step 6: Query the data with metadata

```sql
SELECT * FROM iris_with_meta LIMIT 5;
```

```sql
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     iris_file    │     row_index    │    sepal_length   │    sepal_width    │    petal_length   │    petal_width    │      species     │
├──────────────────┼──────────────────┼───────────────────┼───────────────────┼───────────────────┼───────────────────┼──────────────────┤
│ iris.parquet     │                0 │               5.1 │               3.5 │               1.4 │               0.2 │ setosa           │
│ iris.parquet     │                1 │               4.9 │                 3 │               1.4 │               0.2 │ setosa           │
│ iris.parquet     │                2 │               4.7 │               3.2 │               1.3 │               0.2 │ setosa           │
│ iris.parquet     │                3 │               4.6 │               3.1 │               1.5 │               0.2 │ setosa           │
│ iris.parquet     │                4 │                 5 │               3.6 │               1.4 │               0.2 │ setosa           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
