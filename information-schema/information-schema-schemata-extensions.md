---
title: SCHEMATA_EXTENSIONS
summary: Learn how to query the SCHEMATA_EXTENSIONS table to check database-level read-only settings for databases visible to your TiDB user.
---

# SCHEMATA_EXTENSIONS

The `SCHEMATA_EXTENSIONS` table provides [database-level read-only settings](/database-read-only.md) for databases visible to the current user.

| Column | Type | Description |
| --- | --- | --- |
| `CATALOG_NAME` | `varchar(64)` | The catalog name. This value is always `def`. |
| `SCHEMA_NAME` | `varchar(64)` | The database name. |
| `OPTIONS` | `varchar(256)` | `READ ONLY=1` if the database is read-only; an empty string if the database is writable. |

## Example

```sql
CREATE DATABASE app;
ALTER DATABASE app READ ONLY = 1;
SELECT CATALOG_NAME, SCHEMA_NAME, OPTIONS
FROM INFORMATION_SCHEMA.SCHEMATA_EXTENSIONS
WHERE SCHEMA_NAME = 'app';
```

```text
+--------------+-------------+-------------+
| CATALOG_NAME | SCHEMA_NAME | OPTIONS     |
+--------------+-------------+-------------+
| def          | app         | READ ONLY=1 |
+--------------+-------------+-------------+
```

`OPTIONS` describes the database-level setting. It does not indicate whether cluster-wide read-only restrictions are enabled.

## See also

- [`SCHEMATA`](/information-schema/information-schema-schemata.md)
- [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md)
- [Database-Level Read-Only Mode](/database-read-only.md)
