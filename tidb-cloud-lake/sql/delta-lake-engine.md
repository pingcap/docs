---
id: delta
title: Delta Lake Engine
sidebar_label: Delta Lake Engine
slug: /sql-reference/table-engines/delta
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.262"/>

Databend's [Delta Lake](https://delta.io/) engine allows you to seamlessly query and analyze data in Delta Lake tables stored in your object storage. When you create a table with the Delta Lake engine in Databend, you specify a location where the data files of a Delta Lake table are stored. This setup allows you to gain direct access to the table and perform queries seamlessly from within Databend.

- Databend's Delta Lake engine currently supported read-only operations. This means that querying data from your Delta Lake tables is supported, while writing to the tables is not.
- The schema for a table created with the Delta Lake engine is set at the time of its creation. Any modifications to the schema of the original Delta Lake table require the recreation of the corresponding table in Databend to ensure synchronization.
- The Delta Lake engine in Databend is built upon the official [delta-rs](https://github.com/delta-io/delta-rs) library. It is important to note that certain features defined in the delta-protocol, including Deletion Vector, Change Data Feed, Generated Columns, and Identity Columns, are NOT currently supported by this engine.

## Syntax

```sql
CREATE TABLE <table_name> 
ENGINE = Delta 
LOCATION = 's3://<path_to_table>' 
CONNECTION_NAME = '<connection_name>'
```

Before creating a table with the Delta Lake engine, you need to create a connection object used to establish a connection with your S3 storage. To create a connection in Databend, use the [CREATE CONNECTION](/sql/sql-reference/connect-parameters) command.

## Examples

```sql
--Set up connection
CREATE CONNECTION my_s3_conn 
STORAGE_TYPE = 's3' 
ACCESS_KEY_ID ='your-ak' SECRET_ACCESS_KEY ='your-sk';

-- Create table with Delta Lake engine
CREATE TABLE test_delta 
ENGINE = Delta 
LOCATION = 's3://testbucket/admin/data/delta/delta-table/' 
CONNECTION_NAME = 'my_s3_conn';
```
