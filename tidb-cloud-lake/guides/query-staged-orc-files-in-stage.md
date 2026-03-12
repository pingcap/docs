---
title: Querying Staged ORC Files in Stage
sidebar_label: ORC
---
import StepsWrap from '@site/src/components/StepsWrap';
import StepContent from '@site/src/components/Steps/step-content';

## Syntax

- [Query rows as Variants](./index.md#query-rows-as-variants)
- [Query columns by name](./index.md#query-columns-by-name)
- [Query Metadata](./index.md#query-metadata)

## Tutorial

In this tutorial, we will walk you through the process of downloading the Iris dataset in ORC format, uploading it to an Amazon S3 bucket, creating an external stage, and querying the data directly from the ORC file.

<StepsWrap>
<StepContent number="1">

### Download Iris Dataset

Download the iris dataset from https://github.com/tensorflow/io/raw/master/tests/test_orc/iris.orc then upload it to your Amazon S3 bucket.

The iris dataset contains 3 classes of 50 instances each, where each class refers to a type of iris plant. It has 4 attributes: (1) sepal length, (2) sepal width, (3) petal length, (4) petal width, and the last column contains the class label.

</StepContent>
<StepContent number="2">

### Create External Stage

Create an external stage with your Amazon S3 bucket where your iris dataset file is stored.

```sql
CREATE STAGE orc_query_stage
    URL = 's3://databend-doc'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-key>'
    );
```

</StepContent>
<StepContent number="3">

### Query ORC File

query with columns

```sql
SELECT *
FROM @orc_query_stage
(
    FILE_FORMAT => 'orc',
    PATTERN => '.*[.]orc'
);

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│    sepal_length   │    sepal_width    │    petal_length   │    petal_width    │      species     │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼──────────────────┤
│               5.1 │               3.5 │               1.4 │               0.2 │ setosa           │
│                 · │                 · │                 · │                 · │ ·                │
│               5.9 │                 3 │               5.1 │               1.8 │ virginica        │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

query with path expressions:

```sql
SELECT $1
FROM @orc_query_stage
(
    FILE_FORMAT => 'orc',
    PATTERN => '.*[.]orc'
    
);
```

You can also query the remote ORC file directly:

```sql
SELECT
  *
FROM
  'https://github.com/tensorflow/io/raw/master/tests/test_orc/iris.orc' (file_format => 'orc');
```

</StepContent>
<StepContent number="4">

### Query with Metadata

Query ORC files directly from a stage, including metadata columns like `METADATA$FILENAME` and `METADATA$FILE_ROW_NUMBER`:



```sql
SELECT
    METADATA$FILENAME,
    METADATA$FILE_ROW_NUMBER,
    *
FROM @orc_query_stage
(
    FILE_FORMAT => 'orc',
    PATTERN => '.*[.]orc'
);
```

</StepContent>
</StepsWrap>