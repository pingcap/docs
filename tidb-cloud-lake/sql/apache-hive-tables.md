---
id: hive
title: Apache Hive Tables
sidebar_label: Apache Hive Tables
slug: /sql-reference/table-engines/hive
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.668"/>

Databend can query data that is cataloged by Apache Hive without copying it. Register the Hive Metastore as a Databend catalog, point to the object storage that holds the table data, and then query the tables as if they were native Databend objects.

## Quick Start

1. **Register the Hive Metastore**

   ```sql
   CREATE CATALOG hive_prod
   TYPE = HIVE
   CONNECTION = (
     METASTORE_ADDRESS = '127.0.0.1:9083'
     URL = 's3://lakehouse/'
     ACCESS_KEY_ID = '<your_key_id>'
     SECRET_ACCESS_KEY = '<your_secret_key>'
   );
   ```

2. **Explore the catalog**

   ```sql
   USE CATALOG hive_prod;
   SHOW DATABASES;
   SHOW TABLES FROM tpch;
   ```

3. **Query Hive tables**

   ```sql
   SELECT l_orderkey, SUM(l_extendedprice) AS revenue
   FROM tpch.lineitem
   GROUP BY l_orderkey
   ORDER BY revenue DESC
   LIMIT 10;
   ```

## Keep Metadata Fresh

Hive schemas or partitions can change outside of Databend. Refresh Databend’s cached metadata when that happens:

```sql
ALTER TABLE tpch.lineitem REFRESH CACHE;
```

## Data Type Mapping

Databend automatically converts Hive primitive types to their closest native equivalents when queries run:

| Hive Type | Databend Type |
| --------- | ------------- |
| `BOOLEAN` | [BOOLEAN](/sql/sql-reference/data-types/boolean) |
| `TINYINT`, `SMALLINT`, `INT`, `BIGINT` | [Integer types](/sql/sql-reference/data-types/numeric#integer-data-types) |
| `FLOAT`, `DOUBLE` | [Floating-point types](/sql/sql-reference/data-types/numeric#floating-point-data-types) |
| `DECIMAL(p,s)` | [DECIMAL](/sql/sql-reference/data-types/decimal) |
| `STRING`, `VARCHAR`, `CHAR` | [STRING](/sql/sql-reference/data-types/string) |
| `DATE`, `TIMESTAMP` | [DATETIME](/sql/sql-reference/data-types/datetime) |
| `ARRAY<type>` | [ARRAY](/sql/sql-reference/data-types/array) |
| `MAP<key,value>` | [MAP](/sql/sql-reference/data-types/map) |

Nested structures such as `STRUCT` are surfaced through the [VARIANT](/sql/sql-reference/data-types/variant) type.

## Notes and Limitations

- Hive catalogs are **read-only** in Databend (writes must happen through Hive-compatible engines).
- Access to the underlying object storage is required; configure credentials by using [connection parameters](/sql/sql-reference/connect-parameters).
- Use `ALTER TABLE ... REFRESH CACHE` whenever table layout changes (for example, new partitions) to keep query results up to date.
