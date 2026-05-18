---
title: Integration Tasks
summary: This page provides an overview of integration tasks in {{{ .lake }}}. Integration tasks define how data flows from external sources into {{{ .lake }}}, including source settings, target tables, and runtime parameters.
---

# Integration Tasks

An integration task in {{{ .lake }}} defines how data flows from a source into a target table in {{{ .lake }}}. Each task references an existing data source and specifies source settings, a target warehouse, a target database / table, and runtime parameters that are specific to the task type.

Unlike data sources, integration tasks are the executable units that actually perform data movement and synchronization. Data sources store access settings, while tasks handle scheduling, ingestion, synchronization, stopping, resuming, and monitoring.

## Supported Task Types

| Task Type | Description |
|-----------|-------------|
| [Amazon S3](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md) | Imports CSV, Parquet, or NDJSON files from Amazon S3 with support for one-time or continuous ingestion. |
| [MySQL](/tidb-cloud-lake/guides/integrate-with-mysql.md) | Synchronizes table data from MySQL using `Snapshot`, `CDC Only`, or `Snapshot + CDC`. |
| [PostgreSQL](/tidb-cloud-lake/guides/integrate-with-postgresql.md) | Synchronizes table data from PostgreSQL using `Snapshot`, `CDC Only`, or `Snapshot + CDC`. |

## Reading Guide

Recommended reading order:

1. Start with [Task Management](/tidb-cloud-lake/guides/task-management.md) to understand the task creation flow, start / stop behavior, status, and run history.
2. Then read the task-specific guide for the source type you want to configure.

## Task Type Differences

- Amazon S3 tasks are designed for file import scenarios and mainly focus on file path patterns, file formats, and ingestion behavior.
- MySQL and PostgreSQL tasks are designed for table synchronization scenarios and mainly focus on sync modes, primary keys, incremental capture, and archive scheduling.
