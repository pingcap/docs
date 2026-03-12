---
title: Loading ORC into Databend
sidebar_label: ORC
---

## What is ORC?

ORC (Optimized Row Columnar) is a columnar storage format commonly used in data analytics.

## Loading ORC File

The common syntax for loading ORC file is as follows:

```sql
COPY INTO [<database>.]<table_name>
     FROM { internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
FILE_FORMAT = (TYPE = ORC)
```

- For more ORC file format options, refer to [ORC File Format Options](/sql/sql-reference/file-format-options#orc-options).
- For more COPY INTO table options, refer to [COPY INTO table](/sql/sql-commands/dml/dml-copy-into-table).

## Tutorial: Loading Data from ORC Files

This tutorial demonstrates how to load data from ORC files stored in an S3 bucket into a Databend table.

### Step 1. Create an External Stage

Create an external stage which points to the ORC files in the S3 bucket.

```sql
CREATE OR REPLACE CONNECTION aws_s3
    STORAGE_TYPE='s3'
    ACCESS_KEY_ID='your-ak'
    SECRET_ACCESS_KEY='your-sk';

CREATE OR REPLACE STAGE orc_data_stage
    URL='s3://wizardbend/databend-doc/sample-data/orc/'
    CONNECTION=(CONNECTION_NAME='aws_s3');
```

List the files in the stage:

```sql
LIST @orc_data_stage;
```

Result:

```text

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│      name     │  size  │                 md5                │         last_modified         │      creator     │
├───────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ README.txt    │    494 │ "72529dd37b12faf08b090f941507a4f4" │ 2024-06-05 03:05:02.000 +0000 │ NULL             │
│ userdata1.orc │  47448 │ "1595b4de335ac1825af2b846e82fbf48" │ 2024-06-05 03:05:36.000 +0000 │ NULL             │
│ userdata2.orc │  46545 │ "8a8a1db8475a46365fcb3bcf773fa703" │ 2024-06-05 03:06:47.000 +0000 │ NULL             │
│ userdata3.orc │  47159 │ "fb8a92554f90c9385388bd91eb1a25f1" │ 2024-06-05 03:12:52.000 +0000 │ NULL             │
│ userdata4.orc │  47219 │ "222b1fbde459fd9233f5da5613dbcfa1" │ 2024-06-05 03:13:05.000 +0000 │ NULL             │
│ userdata5.orc │  47206 │ "f12d768b5d210f488dcf55ed86ceaca6" │ 2024-06-05 03:13:16.000 +0000 │ NULL             │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 2: Querying the Stage Files

Create a file format for ORC and query the stage to view the data and schema.

```sql
-- Create a ORC file format
CREATE OR REPLACE FILE FORMAT orc_ff TYPE = 'ORC';


SELECT *
FROM @orc_data_stage (
    FILE_FORMAT => 'orc_ff',
    PATTERN => '.*[.]orc'
) t
LIMIT 10;
```

Result:

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        _col0        │      _col1      │       _col2      │       _col3      │           _col4          │       _col5      │       _col6      │       _col7      │          _col8         │       _col9      │       _col10      │          _col11          │      _col12      │
├─────────────────────┼─────────────────┼──────────────────┼──────────────────┼──────────────────────────┼──────────────────┼──────────────────┼──────────────────┼────────────────────────┼──────────────────┼───────────────────┼──────────────────────────┼──────────────────┤
│ 2016-02-03 07:55:29 │               1 │ Amanda           │ Jordan           │ ajordan0@com.com         │ Female           │ 1.197.201.2      │ 6759521864920116 │ Indonesia              │ 3/8/1971         │          49756.53 │ Internal Auditor         │ 1E+02            │
│ 2016-02-03 17:04:03 │               2 │ Albert           │ Freeman          │ afreeman1@is.gd          │ Male             │ 218.111.175.34   │                  │ Canada                 │ 1/16/1968        │         150280.17 │ Accountant IV            │                  │
│ 2016-02-03 01:09:31 │               3 │ Evelyn           │ Morgan           │ emorgan2@altervista.org  │ Female           │ 7.161.136.94     │ 6767119071901597 │ Russia                 │ 2/1/1960         │         144972.51 │ Structural Engineer      │                  │
│ 2016-02-03 00:36:21 │               4 │ Denise           │ Riley            │ driley3@gmpg.org         │ Female           │ 140.35.109.83    │ 3576031598965625 │ China                  │ 4/8/1997         │          90263.05 │ Senior Cost Accountant   │                  │
│ 2016-02-03 05:05:31 │               5 │ Carlos           │ Burns            │ cburns4@miitbeian.gov.cn │                  │ 169.113.235.40   │ 5602256255204850 │ South Africa           │                  │              NULL │                          │                  │
│ 2016-02-03 07:22:34 │               6 │ Kathryn          │ White            │ kwhite5@google.com       │ Female           │ 195.131.81.179   │ 3583136326049310 │ Indonesia              │ 2/25/1983        │          69227.11 │ Account Executive        │                  │
│ 2016-02-03 08:33:08 │               7 │ Samuel           │ Holmes           │ sholmes6@foxnews.com     │ Male             │ 232.234.81.197   │ 3582641366974690 │ Portugal               │ 12/18/1987       │          14247.62 │ Senior Financial Analyst │                  │
│ 2016-02-03 06:47:06 │               8 │ Harry            │ Howell           │ hhowell7@eepurl.com      │ Male             │ 91.235.51.73     │                  │ Bosnia and Herzegovina │ 3/1/1962         │         186469.43 │ Web Developer IV         │                  │
│ 2016-02-03 03:52:53 │               9 │ Jose             │ Foster           │ jfoster8@yelp.com        │ Male             │ 132.31.53.61     │                  │ South Korea            │ 3/27/1992        │         231067.84 │ Software Test Engineer I │ 1E+02            │
│ 2016-02-03 18:29:47 │              10 │ Emily            │ Stewart          │ estewart9@opensource.org │ Female           │ 143.28.251.245   │ 3574254110301671 │ Nigeria                │ 1/28/1997        │          27234.28 │ Health Coach IV          │                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4: Create Target Table

Create a target table in Databend to store the data from the ORC files. We choose some of the columns from the ORC files to create the table.

```sql
CREATE OR REPLACE TABLE orc_test_table (
    firstname STRING,
    lastname STRING,
    email STRING,
    gender STRING,
    country STRING
);
```

### Step 5. Using SELECT to Copy Data

Copy the data from the ORC files in the external stage into the target table.

```sql
COPY INTO orc_test_table
FROM (
    SELECT _col2, _col3, _col4, _col5, _col8
    FROM @orc_data_stage
)
PATTERN = '.*[.]orc'
FILE_FORMAT = (TYPE = ORC);
```

Result:

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│      File     │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├───────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ userdata1.orc │        1000 │           0 │ NULL             │             NULL │
│ userdata2.orc │        1000 │           0 │ NULL             │             NULL │
│ userdata3.orc │        1000 │           0 │ NULL             │             NULL │
│ userdata4.orc │        1000 │           0 │ NULL             │             NULL │
│ userdata5.orc │        1000 │           0 │ NULL             │             NULL │
└─────────────────────────────────────────────────────────────────────────────────┘
```
