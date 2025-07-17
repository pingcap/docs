---
title: TiDB Limitations
summary: Learn the usage limitations of TiDB.
---

# TiDB Limitations

This document describes the common usage limitations of TiDB, including the maximum identifier length and the maximum number of supported databases, tables, indexes, partitioned tables, and sequences.

> **Note:**
>
> TiDB offers high compatibility with the MySQL protocol and syntax, including many MySQL limitations. For example, a single index can include a maximum of 16 columns. For more information, see [MySQL Compatibility](/mysql-compatibility.md) and the official MySQL documentation.

## Limitations on identifier length

| Identifier type | Maximum length (number of characters allowed) |
|:---------|:--------------|
| Database | 64 |
| Table    | 64 |
| Column   | 64 |
| Index    | 64 |
| View     | 64 |
| Sequence | 64 |

## Limitations on the total number of databases, tables, views, and connections

| Type  | Maximum number  |
|:----------|:----------|
| Databases | unlimited |
| Tables    | unlimited |
| Views     | unlimited |
| Connections| unlimited|

## Limitations on a single database

| Type       | Upper limit   |
|:----------|:----------|
| Tables    | unlimited  |

## Limitations on a single table

| Type       | Upper limit (default value)  |
|:----------|:----------|
| Columns   | Defaults to 1017 and can be adjusted up to 4096     |
| Indexes   |  Defaults to 64 and can be adjusted up to 512        |
| Rows      | unlimited |
| Size      | unlimited |
| Partitions | 8192     |

<CustomContent platform="tidb">

* The upper limit of `Columns` can be modified via [`table-column-count-limit`](/tidb-configuration-file.md#table-column-count-limit-new-in-v50).
* The upper limit of `Indexes` can be modified via [`index-limit`](/tidb-configuration-file.md#index-limit-new-in-v50).

</CustomContent>

## Limitation on a single row

| Type       | Upper limit (default value)   |
|:----------|:----------|
| Size       | Defaults to 6 MiB and can be adjusted to 120 MiB  |

<CustomContent platform="tidb">

You can adjust the size limit via the [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500) configuration item.

</CustomContent>

## Limitations on indexes

The maximum index length is 3072 bytes, equivalent to 768 characters using 4-byte UTF-8 encoding. The maximum number of columns in a single index is limited to 16.

<CustomContent platform="tidb">

You can adjust this limit using the [`max-index-length`](/tidb-configuration-file.md#max-index-length) configuration item.

</CustomContent>

## Limitations on data types

| Type       | Upper limit   |
|:----------|:----------|
| CHAR       | 255 characters      |
| BINARY     | 255 characters      |
| VARBINARY  | 65535 characters    |
| VARCHAR    | 16383 characters    |
| TEXT       | Defaults to 6 MiB and can be adjusted to 120 MiB                |
| BLOB       | Defaults to 6 MiB and can be adjusted to 120 MiB               |

## Limitations on SQL statements

| Type       | Upper limit   |
|:----------|:----------|
| The maximum number of SQL statements in a single transaction |  When the optimistic transaction is used and the transaction retry is enabled, the upper limit is 5000. |

<CustomContent platform="tidb">

You can modify the limit via the [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit) configuration item.

</CustomContent>

## Limitations on TiKV version

In your cluster, if the version of the TiDB component is v6.2.0 or later, the version of TiKV must be v6.2.0 or later.
