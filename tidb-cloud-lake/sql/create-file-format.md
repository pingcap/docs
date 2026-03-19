---
title: CREATE FILE FORMAT
summary: Create a named file format.
---

# CREATE FILE FORMAT

> **Note:**
>
> Introduced or updated in v1.2.339.

Create a named file format.

## Syntax

```sql
CREATE [ OR REPLACE ] FILE FORMAT [ IF NOT EXISTS ] <format_name> FileFormatOptions
```

For details about `FileFormatOptions`, see [Input & Output File Formats](/tidb-cloud-lake/sql/input-output-file-formats.md).

## Use the file format

Create once, then reuse the format for both querying and loading:

```sql
-- 1) Create a reusable format
CREATE OR REPLACE FILE FORMAT my_custom_csv TYPE = CSV FIELD_DELIMITER = '\t';

-- 2) Query staged files (stage table function syntax uses =>)
SELECT * FROM @mystage/data.csv (FILE_FORMAT => 'my_custom_csv') LIMIT 10;

-- 3) Load staged files with COPY INTO (copy options use =)
COPY INTO my_table
FROM @mystage/data.csv
FILE_FORMAT = (FORMAT_NAME = 'my_custom_csv');
```

Why the different operators? Stage table functions take key/value parameters written with `=>`, while `COPY INTO` options use standard assignments with `=`.

**Quick workflow: create, query, and load with the same format**

```sql
-- Create a reusable format
CREATE FILE FORMAT my_parquet TYPE = PARQUET;

-- Query staged files with the format (stage table function syntax uses =>)
SELECT * FROM @sales_stage/2024/order.parquet (FILE_FORMAT => 'my_parquet') LIMIT 10;

-- Load staged files with COPY INTO (copy options use =)
COPY INTO analytics.orders
FROM @sales_stage/2024/order.parquet
FILE_FORMAT = (FORMAT_NAME = 'my_parquet');
```
