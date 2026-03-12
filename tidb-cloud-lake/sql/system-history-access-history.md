---
title: system_history.access_history
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.764"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='ACCESS HISTORY'/>

**Data lineage and access control audit** - Tracks all database objects (tables, columns, stages) accessed or modified by queries. Essential for:

- **Data Lineage**: Understand data flow and dependencies across your database
- **Compliance Reporting**: Track who accessed sensitive data and when
- **Change Management**: Monitor DDL operations and schema modifications
- **Security Analysis**: Identify unusual access patterns or unauthorized data access


## Fields

| Field                   | Type      | Description                                                                 |
|-------------------------|-----------|-----------------------------------------------------------------------------|
| query_id                | VARCHAR   | The ID of the query.                                                        |
| query_start             | TIMESTAMP | The start time of the query.                                                |
| user_name               | VARCHAR   | The name of the user who executed the query.                                |
| base_objects_accessed   | VARIANT   | The objects accessed by the query.                                          |
| direct_objects_accessed | VARIANT   | Reserved for future use; currently not in use.                              |
| objects_modified        | VARIANT   | The objects modified by the query.                                          |
| object_modified_by_ddl  | VARIANT   | The objects modified by the DDL (e.g `CREATE TABLE`, `ALTER TABLE`).        |

The fields `base_objects_accessed`, `objects_modified`, and `object_modified_by_ddl` are all arrays of JSON objects. Each object may include the following fields:

- `object_domain`: The type of object, one of [`Database`, `Table`, `Stage`].
- `object_name`: The name of the object. For stages, this is the stage name.
- `columns`: Column information, present only when `object_domain` is `Table`.
- `stage_type`: The type of stage, present only when `object_domain` is `Stage`.
- `operation_type`: The DDL operation type, one of [`Create`, `Alter`, `Drop`, `Undrop`], present only in the `object_modified_by_ddl` field.
- `properties`: Detailed information about the DDL operation, present only in the `object_modified_by_ddl` field.

## Examples


```sql
CREATE TABLE t (a INT, b string);
```

Will be recorded as:

```
               query_id: c2c1c7be-cee4-4868-a28e-8862b122c365
            query_start: 2025-06-12 03:31:19.042128
              user_name: root
  base_objects_accessed: []
direct_objects_accessed: []
       objects_modified: []
 object_modified_by_ddl: [{"object_domain":"Table","object_name":"default.default.t","operation_type":"Create","properties":{"columns":[{"column_name":"a","sub_operation_type":"Add"},{"column_name":"b","sub_operation_type":"Add"}],"create_options":{"compression":"zstd","database_id":"1","storage_format":"parquet"}}}]
```

`CREATE TABLE` is a DDL operation, so it will be recorded in the `object_modified_by_ddl` field.


```sql
INSERT INTO t VALUES (1, 'book');
```

Will be recorded as:

```
               query_id: e92ebc00-a07e-4138-92a9-ea17a06f0165
            query_start: 2025-06-12 03:31:29.849848
              user_name: root
  base_objects_accessed: []
direct_objects_accessed: []
       objects_modified: [{"columns":[{"column_name":"a"},{"column_name":"b"}],"object_domain":"Table","object_name":"default.default.t"}]
 object_modified_by_ddl: []
```

`INSERT INTO` is a DML operation, so it will be recorded in the `objects_modified` field.


```sql
COPY INTO @s FROM t;
```

```
               query_id: 7fd74374-c04a-4989-a6f7-bfe8cc27e511
            query_start: 2025-06-12 03:32:25.682248
              user_name: root
  base_objects_accessed: [{"columns":[{"column_name":"a"},{"column_name":"b"}],"object_domain":"Table","object_name":"default.default.t"}]
direct_objects_accessed: []
       objects_modified: [{"object_domain":"Stage","object_name":"s","stage_type":"Internal"}]
 object_modified_by_ddl: []
```

The `COPY INTO` operation from table `t` to internal stage `s` involves both read and write actions. After executing this query, the source table will be recorded in the `base_objects_accessed` field, and the target stage will be recorded in the `objects_modified` field.