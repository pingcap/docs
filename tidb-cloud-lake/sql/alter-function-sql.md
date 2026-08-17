---
title: ALTER FUNCTION
summary: Learn how to change the handler, return schema, description, or HTTPS UDF Server endpoint of an external function in TiDB Cloud Lake.
---

# ALTER FUNCTION

The `ALTER FUNCTION` statement changes an external function registration.

## Scalar function syntax

```sql
ALTER FUNCTION [ IF EXISTS ] <function_name>
    ( [<parameter_list>] )
    RETURNS <return_type>
    LANGUAGE python
    HANDLER = '<handler_name>'
    ADDRESS = '<https_udf_server_endpoint>'
    [ DESC='<description>' ]
```

## Table function syntax

```sql
ALTER FUNCTION [ IF EXISTS ] <function_name>
    ( [<parameter_list>] )
    RETURNS TABLE ( <column_definition_list> )
    LANGUAGE python
    HANDLER = '<handler_name>'
    ADDRESS = '<https_udf_server_endpoint>'
    [ DESC='<description>' ]
```

The endpoint hostname must be in your tenant UDF server allowlist.

## Example

```sql
ALTER FUNCTION external_add(left INT, right INT)
RETURNS BIGINT
LANGUAGE python
HANDLER = 'add_bigint'
ADDRESS = 'https://udf.example.com';
```

To change a SQL scalar or table UDF, use [ALTER FUNCTION for UDFs](/tidb-cloud-lake/sql/alter-function.md).
