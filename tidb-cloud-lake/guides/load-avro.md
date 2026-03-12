---
title: Loading Avro into Databend
sidebar_label: Avro
---

## What is Avro?

[Apache Avro™](https://avro.apache.org/) is the leading serialization format for record data, and first choice for streaming data pipelines.

## Loading Avro File

The common syntax for loading AVRO file is as follows:

```sql
COPY INTO [<database>.]<table_name>
     FROM { internalStage | externalStage | externalLocation }
[ PATTERN = '<regex_pattern>' ]
FILE_FORMAT = (TYPE = AVRO)
```

- For more Avro file format options, refer to [Avro File Format Options](/sql/sql-reference/file-format-options#avro-options).
- For more COPY INTO table options, refer to [COPY INTO table](/sql/sql-commands/dml/dml-copy-into-table).

## Tutorial: Loading Avro Data into Databend from Remote HTTP URL

In this tutorial, you will create a table in Databend using an Avro schema and load Avro data directly from a GitHub-hosted `.avro` file via HTTPS.

###  Step 1: Review the Avro Schema

Before creating a table in Databend, let’s take a quick look at the Avro schema we’re working with: [userdata.avsc](https://github.com/Teradata/kylo/blob/master/samples/sample-data/avro/userdata.avsc). This schema defines a record named `User` with 13 fields, mostly of type string, along with `int` and `float`.

```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "registration_dttm", "type": "string"},
    {"name": "id", "type": "int"},
    {"name": "first_name", "type": "string"},
    {"name": "last_name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "gender", "type": "string"},
    {"name": "ip_address", "type": "string"},
    {"name": "cc", "type": "string"},
    {"name": "country", "type": "string"},
    {"name": "birthdate", "type": "string"},
    {"name": "salary", "type": "float"},
    {"name": "title", "type": "string"},
    {"name": "comments", "type": "string"}
  ]
}
```

###  Step 2: Create a Table in Databend

Create a table that matches the structure defined in the schema:

```sql
CREATE TABLE userdata (
  registration_dttm STRING,
  id INT,
  first_name STRING,
  last_name STRING,
  email STRING,
  gender STRING,
  ip_address STRING,
  cc VARIANT,
  country STRING,
  birthdate STRING,
  salary FLOAT,
  title STRING,
  comments STRING
);
```

###  Step 3: Load Data from a Remote HTTPS URL

```sql
COPY INTO userdata
FROM 'https://raw.githubusercontent.com/Teradata/kylo/master/samples/sample-data/avro/userdata1.avro'
FILE_FORMAT = (type = avro);
```

```sql
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             File                             │ Rows_loaded │ Errors_seen │    First_error   │ First_error_line │
├──────────────────────────────────────────────────────────────┼─────────────┼─────────────┼──────────────────┼──────────────────┤
│ Teradata/kylo/master/samples/sample-data/avro/userdata1.avro │        1000 │           0 │ NULL             │             NULL │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Step 4: Query the Data

You can now explore the data you just imported:

```sql
SELECT id, first_name, email, salary FROM userdata LIMIT 5;
```

```sql
┌───────────────────────────────────────────────────────────────────────────────────┐
│        id       │    first_name    │           email          │       salary      │
├─────────────────┼──────────────────┼──────────────────────────┼───────────────────┤
│               1 │ Amanda           │ ajordan0@com.com         │          49756.53 │
│               2 │ Albert           │ afreeman1@is.gd          │         150280.17 │
│               3 │ Evelyn           │ emorgan2@altervista.org  │         144972.52 │
│               4 │ Denise           │ driley3@gmpg.org         │          90263.05 │
│               5 │ Carlos           │ cburns4@miitbeian.gov.cn │              NULL │
└───────────────────────────────────────────────────────────────────────────────────┘
```