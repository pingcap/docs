---
title: File Format
---

This page provides a comprehensive overview of File Format operations in Databend, organized by functionality for easy reference.

## File Format Management

| Command | Description |
|---------|-------------|
| [CREATE FILE FORMAT](/tidb-cloud-lake/sql/create-file-format.md) | Creates a named file format object for use in data loading and unloading |
| [DROP FILE FORMAT](/tidb-cloud-lake/sql/drop-file-format.md) | Removes a file format object |

## File Format Information

| Command | Description |
|---------|-------------|
| [SHOW FILE FORMATS](/tidb-cloud-lake/sql/show-file-formats.md) | Lists all file formats in the current database |

> **Note:**
>
> File formats in Databend define how data files should be parsed during data loading operations or formatted during data unloading operations. They provide a reusable way to specify file type, field delimiters, compression, and other formatting options.