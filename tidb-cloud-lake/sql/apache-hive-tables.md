---
title: Apache Hive Tables
summary: Databend can query data that is cataloged by Apache Hive without copying it. Register the Hive Metastore as a Databend catalog, point to the object storage that holds the table data, and then query the tables as if they were native Databend objects.
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
| `BOOLEAN` | [BOOLEAN](/tidb-cloud-lake/sql/boolean.md) |
| `TINYINT`, `SMALLINT`, `INT`, `BIGINT` | [Integer types](/tidb-cloud-lake/sql/numeric.md#integer-data-types) |
| `FLOAT`, `DOUBLE` | [Floating-point types](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) |
| `DECIMAL(p,s)` | [DECIMAL](/tidb-cloud-lake/sql/decimal.md) |
| `STRING`, `VARCHAR`, `CHAR` | [STRING](/tidb-cloud-lake/sql/string.md) |
| `DATE`, `TIMESTAMP` | [DATETIME](/tidb-cloud-lake/sql/datetime.md) |
| `ARRAY<type>` | [ARRAY](/tidb-cloud-lake/sql/array.md) |
| `MAP<key,value>` | [MAP](/tidb-cloud-lake/sql/map.md) |

Nested structures such as `STRUCT` are surfaced through the [VARIANT](/tidb-cloud-lake/sql/variant.md) type.

## Notes and Limitations

- Hive catalogs are **read-only** in Databend (writes must happen through Hive-compatible engines).
- Access to the underlying object storage is required; configure credentials by using [connection parameters](/tidb-cloud-lake/sql/connection-parameters.md).
- Use `ALTER TABLE ... REFRESH CACHE` whenever table layout changes (for example, new partitions) to keep query results up to date.
