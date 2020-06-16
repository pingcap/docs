---
title: TiDB Limitations
summary: Learn the limitations of TiDB.
category: introduction
---

# TiDB Limitations

This document describes the common limitations of TiDB, including the maximum identifier length and the maximum count of supported databases, tables, indexes, partitioned tables, and sequences.

## Limitation on identifier length

| Identifier type | Maximum length (character) |
|:---------|:--------------|
| Database | 64 |
| Table    | 64 |
| Column   | 64 |
| Index    | 64 |
| View     | 64 |
| Sequence | 64 |

## Limitation on the total count of databases, tables, views, and connections

| Identifier type  | Maximum count   |
|:----------|:----------|
| Databases | unlimited |
| Tables    | unlimited |
| Views     | unlimited |
| Connections| unlimited|

## Limitation on a single database

| Type       | Upper limit   |
|:----------|:----------|
| Tables    | unlimited  |

## Limitation on a single table

| Type       | Upper limit   |
|:----------|:----------|
| Columns   | 512       |
| Indexes    | 64        |
| Rows      | unlimited |
| Size      | unlimited |
| Partitions | 1024      |

## Limitation on a single row

| Type       | Upper limit   |
|:----------|:----------|
| Size       | 6 MB       |

## Limitation on a single column

| Type       | Upper limit   |
|:----------|:----------|
| Size       | 6 MB       |

## Limitation on string types

| Type       | Upper limit   |
|:----------|:----------|
| CHAR       | 256 characters      |
| BINARY     | 256 characters      |
| VARBINARY  | 65535 characters    |
| VARCHAR    | 16383 characters    |
| TEXT       | 6MB bytes      |
| BLOB       | 6MB bytes      |

## Limitation on SQL statements

| Type       | Upper limit   |
|:----------|:----------|
| The number of SQL statements in a single transaction |  When the optimistic transaction is used and the transaction retry is enabled, the default upper limit is 5000, which can be changed through [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit). |
