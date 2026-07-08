---
title: Unloading Lance Dataset
summary: Learn about how to unload Lance datasets.
---

## Unloading Lance Dataset

Lance exports are aimed at dataset-oriented consumers such as machine learning and vector workflows. Unlike CSV, TSV, NDJSON, or Parquet unloading, {{{ .lake }}} writes a Lance **dataset directory** that contains `.lance` data files plus metadata such as `_versions/`.

Syntax:

```sql
COPY INTO { internalStage | externalStage | externalLocation }
FROM { [<database_name>.]<table_name> | ( <query> ) }
FILE_FORMAT = (TYPE = LANCE)
[MAX_FILE_SIZE = <num>]
[USE_RAW_PATH = true | false]
[OVERWRITE = true | false]
[DETAILED_OUTPUT = true | false]
```

- Lance is supported only for `COPY INTO <location>`.
- `SINGLE` and `PARTITION BY` are not supported with Lance.
- When `USE_RAW_PATH = false` (default), {{{ .lake }}} appends the query ID to the target path so each export gets its own dataset root.
- When you want a stable dataset URI for downstream readers such as Python `lance`, set `USE_RAW_PATH = true`.
- More details about the syntax can be found in [COPY INTO location](/tidb-cloud-lake/sql/copy-into-location.md).
- More Lance behavior notes are listed in [Input & Output File Formats](/tidb-cloud-lake/sql/input-output-file-formats.md#lance-options).

## Tutorial

This example builds a small document-classification dataset. The raw text files are stored in a stage, `READ_FILE` turns them into `BINARY` values during query execution, and {{{ .lake }}} exports the final dataset in Lance format for Python consumers.

### Prerequisites

Prepare an S3-compatible bucket that is reachable from both {{{ .lake }}} and your Python environment.

### Step 1. Create an External Stage

```sql
CREATE OR REPLACE STAGE ml_assets
URL = 's3://your-bucket/lance-demo/'
CONNECTION = (
    ENDPOINT_URL = '<your-endpoint-url>',
    ACCESS_KEY_ID = '<your-access-key-id>',
    SECRET_ACCESS_KEY = '<your-secret-access-key>',
    REGION = '<your-region>'
);
```

### Step 2. Create Sample Source Files

Create three raw text files in the stage:

```sql
COPY INTO @ml_assets/raw/ticket_001.txt
FROM (SELECT 'customer asked for a refund after the package arrived damaged')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' RECORD_DELIMITER = '\n')
SINGLE = TRUE
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;

COPY INTO @ml_assets/raw/ticket_002.txt
FROM (SELECT 'customer praised the fast response and confirmed the issue was resolved')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' RECORD_DELIMITER = '\n')
SINGLE = TRUE
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;

COPY INTO @ml_assets/raw/ticket_003.txt
FROM (SELECT 'customer requested escalation because the replacement order was delayed')
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' RECORD_DELIMITER = '\n')
SINGLE = TRUE
USE_RAW_PATH = TRUE
OVERWRITE = TRUE;
```

### Step 3. Create a Manifest Table

```sql
CREATE OR REPLACE TABLE support_ticket_manifest (
    ticket_id INT,
    label STRING,
    file_path STRING
);

INSERT INTO support_ticket_manifest VALUES
    (1, 'refund', 'raw/ticket_001.txt'),
    (2, 'resolved', 'raw/ticket_002.txt'),
    (3, 'escalation', 'raw/ticket_003.txt');
```

### Step 4. Export the Dataset to Lance

`READ_FILE` reads the staged text files as raw bytes. `COPY INTO` then writes those rows into a Lance dataset:

```sql
COPY INTO @ml_assets/datasets/support-ticket-train
FROM (
    SELECT
        ticket_id,
        label,
        file_path,
        READ_FILE('@ml_assets', file_path) AS content
    FROM support_ticket_manifest
    ORDER BY ticket_id
)
FILE_FORMAT = (TYPE = LANCE)
USE_RAW_PATH = TRUE
OVERWRITE = TRUE
DETAILED_OUTPUT = TRUE;
```

Result:

```text
┌───────────────────────────────────────────────────────────────┐
│ file_name                          │ file_size │ row_count   │
├────────────────────────────────────┼───────────┼─────────────┤
│ datasets/support-ticket-train      │ ...       │ 3           │
└───────────────────────────────────────────────────────────────┘
```

### Step 5. Inspect the Exported Dataset Layout

```sql
LIST @ml_assets/datasets/support-ticket-train;
```

You will see a dataset directory that includes paths similar to:

```text
datasets/support-ticket-train/_versions/...
datasets/support-ticket-train/data/... .lance
datasets/support-ticket-train/*.manifest
```

### Step 6. Verify with Python `lance`

Install the Python package:

```bash
pip install pylance
```

Read the exported dataset from the same object storage location:

```python
import os
import lance

storage_options = {
    "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
    "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
    "region": os.environ.get("AWS_REGION", "us-east-1"),
}

if endpoint := os.environ.get("AWS_ENDPOINT_URL"):
    storage_options["aws_endpoint"] = endpoint
    storage_options["aws_allow_http"] = "true" if endpoint.startswith("http://") else "false"

dataset = lance.dataset(
    "s3://your-bucket/lance-demo/datasets/support-ticket-train",
    storage_options=storage_options,
)

table = dataset.to_table()
print(table.num_rows)
print(table["label"].to_pylist())
print(table["content"].to_pylist()[0].decode("utf-8").strip())
```

Expected output:

```text
3
['refund', 'resolved', 'escalation']
customer asked for a refund after the package arrived damaged
```

At this point you have a complete Lance dataset that keeps the label, original path, and raw file bytes together for downstream ML processing.
