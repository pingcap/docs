---
title: SQL Development Specification
summary: SQL Development Specification of TiDB.
---

# SQL Development Specification

This chapter will introduce some generalized development specifications for using SQL.

## Specification for table build and delete

- Basic principle: the table is created under the premise of following the table naming specification, and it is recommended to add judgment logic to the build and delete table statements in the internal package of business applications to prevent abnormal interruption of business processes.
- Details: `create table if not exists table_name` or `drop table if exists table_name` statements are recommended to add if judgments to avoid abnormal interruptions caused by SQL commands running abnormally on the application side.

## SELECT \* Usage specification

- Basic principle: Avoid using SELECT \* for queries.
- Details: Select the appropriate field columns as required and avoid blind SELECT \* to read all fields as it consumes network bandwidth. Consider adding the queried fields to the index as well to make effective use of the overriding index function.

## Specification for using functions on fields

- Basic principle: You can use related functions on the takeout fields, but avoid using any functions on the filter condition fields in the Where condition, including data type conversion functions, to avoid index failure. Or you can consider using the expression index function.
- Detailed description:

    NOT recommended:

    {{< copyable "sql" >}}

    ```sql
    SELECT gmt_create
    FROM ...
    WHERE DATE_FORMAT(gmt_create，'%Y%m%d %H:%i:%s') = '20090101 00:00:0'
    ```

    Recommended:

    {{< copyable "sql" >}}

    ```sql
    SELECT DATE_FORMAT(gmt_create，'%Y%m%d %H:%i:%s')
    FROM .. .
    WHERE gmt_create = str_to_date('20090101 00:00:00'，'%Y%m%d %H:%i:s')
    ```

## Other Specifications

- Do not perform mathematical operations or functions on the index column in the `WHERE` condition.
- Replace `OR` with `IN/UNION`, and note that the number of `IN` is less than `300`.
- Avoid using `%` prefix for fuzzy prefix queries.
- If the application uses **Multi Statements** to execute SQL, i.e. multiple SQLs are joined with semicolons and sent to the client for execution at once, TiDB will only return the result of the first SQL execution.
- When using expressions, check if they support compute push-down to the storage layer (TiKV, TiFlash), otherwise you should expect more memory consumption and even OOM at the TiDB layer. the list of compute push-down to the storage layer is as follows:
    - [TiFlash - Supported push-down calculations](/tiflash/use-tiflash.md#supported-push-down-calculations).
    - [TiKV - List of Expressions for Pushdown](/functions-and-operators/expressions-pushed-down.md).
    - [Predicate push down](/predicate-push-down.md).
