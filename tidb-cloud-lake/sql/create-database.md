---
title: CREATE DATABASE
summary: Create a database.
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.339"/>

Create a database.

## Syntax

```sql
CREATE [ OR REPLACE ] DATABASE [ IF NOT EXISTS ] <database_name>
```

## Access control requirements

| Privilege       | Object Type | Description         |
|:----------------|:------------|:--------------------|
| CREATE DATABASE | Global      | Creates a database. |


To create a database, the user performing the operation or the [current_role](/tidb-cloud-lake/guides/roles.md) must have the CREATE DATABASE [privilege](/tidb-cloud-lake/guides/privileges.md).

## Examples

The following example creates a database named `test`:

```sql
CREATE DATABASE test;
```