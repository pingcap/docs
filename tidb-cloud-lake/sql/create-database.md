---
title: CREATE DATABASE
sidebar_position: 1
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


To create a database, the user performing the operation or the [current_role](/guides/security/access-control/roles) must have the CREATE DATABASE [privilege](/guides/security/access-control/privileges).

## Examples

The following example creates a database named `test`:

```sql
CREATE DATABASE test;
```