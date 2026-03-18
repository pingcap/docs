---
title: Stage
---

This page provides a comprehensive overview of stage operations in Databend, organized by functionality for easy reference.

## Stage Management

| Command | Description |
|---------|-------------|
| [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) | Creates a new stage for storing files |
| [DROP STAGE](/tidb-cloud-lake/sql/drop-stage.md) | Removes a stage |
| [PRESIGN](/tidb-cloud-lake/sql/presign.md) | Generates a pre-signed URL for stage access |

## Stage Operations

| Command | Description |
|---------|-------------|
| [LIST STAGE](/tidb-cloud-lake/sql/list-stage-files.md) | Lists files in a stage |
| [REMOVE STAGE](/tidb-cloud-lake/sql/remove-stage-files.md) | Removes files from a stage |

## Stage Information

| Command | Description |
|---------|-------------|
| [DESC STAGE](/tidb-cloud-lake/sql/desc-stage.md) | Shows detailed information about a stage |
| [SHOW STAGES](/tidb-cloud-lake/sql/show-stages.md) | Lists all stages in the current or specified database |

## Related Topics

- [Load from Stage](/tidb-cloud-lake/guides/load-from-stage.md)
- [Query & Transform](/tidb-cloud-lake/guides/query-stage.md)
- [File Format (DDL)](/tidb-cloud-lake/sql/file-format.md)

> **Note:**
>
> Stages in Databend are used as temporary storage locations for data files that you want to load into tables or unload from tables.
