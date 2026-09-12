---
title: system_history.access_history
summary: 字段 base_objects_accessed、objects_modified 和 object_modified_by_ddl 都是 JSON 对象数组。每个对象都可能包含以下字段。
---

# system_history.access_history

**数据血缘和访问控制审计** - 跟踪查询访问或修改的所有数据库对象（表、列、stage）。这对于以下场景至关重要：

- **数据血缘**：了解数据库中的数据流向和依赖关系
- **合规报告**：跟踪谁在何时访问了敏感数据
- **变更管理**：监控 DDL 操作和 schema 修改
- **安全分析**：识别异常访问模式或未授权的数据访问

## 字段 {#fields}

| 字段                    | 类型      | 描述                                                                        |
|-------------------------|-----------|-----------------------------------------------------------------------------|
| query_id                | VARCHAR   | 查询的 ID。                                                                 |
| query_start             | TIMESTAMP | 查询的开始时间。                                                            |
| user_name               | VARCHAR   | 执行该查询的用户名。                                                        |
| base_objects_accessed   | VARIANT   | 查询访问的对象。                                                            |
| direct_objects_accessed | VARIANT   | 保留供未来使用；当前未使用。                                                |
| objects_modified        | VARIANT   | 查询修改的对象。                                                            |
| object_modified_by_ddl  | VARIANT   | 被 DDL 修改的对象（例如 `CREATE TABLE`、`ALTER TABLE`）。                   |

字段 `base_objects_accessed`、`objects_modified` 和 `object_modified_by_ddl` 都是 JSON 对象数组。每个对象都可能包含以下字段：

- `object_domain`：对象的类型，取值之一为 [`Database`, `Table`, `Stage`]。
- `object_name`：对象名称。对于 stage，这里是 stage 名称。
- `columns`：列信息，仅当 `object_domain` 为 `Table` 时存在。
- `stage_type`：stage 的类型，仅当 `object_domain` 为 `Stage` 时存在。
- `operation_type`：DDL 操作类型，取值之一为 [`Create`, `Alter`, `Drop`, `Undrop`]，仅在 `object_modified_by_ddl` 字段中存在。
- `properties`：DDL 操作的详细信息，仅在 `object_modified_by_ddl` 字段中存在。

## 示例 {#examples}

```sql
CREATE TABLE t (a INT, b string);
```

将记录为：

```
               query_id: c2c1c7be-cee4-4868-a28e-8862b122c365
            query_start: 2025-06-12 03:31:19.042128
              user_name: root
  base_objects_accessed: []
direct_objects_accessed: []
       objects_modified: []
 object_modified_by_ddl: [{"object_domain":"Table","object_name":"default.default.t","operation_type":"Create","properties":{"columns":[{"column_name":"a","sub_operation_type":"Add"},{"column_name":"b","sub_operation_type":"Add"}],"create_options":{"compression":"zstd","database_id":"1","storage_format":"parquet"}}}]
```

`CREATE TABLE` 是 DDL 操作，因此会记录在 `object_modified_by_ddl` 字段中。

```sql
INSERT INTO t VALUES (1, 'book');
```

将记录为：

```
               query_id: e92ebc00-a07e-4138-92a9-ea17a06f0165
            query_start: 2025-06-12 03:31:29.849848
              user_name: root
  base_objects_accessed: []
direct_objects_accessed: []
       objects_modified: [{"columns":[{"column_name":"a"},{"column_name":"b"}],"object_domain":"Table","object_name":"default.default.t"}]
 object_modified_by_ddl: []
```

`INSERT INTO` 是 DML 操作，因此会记录在 `objects_modified` 字段中。

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

从表 `t` 执行 `COPY INTO` 到内部 stage `s` 的操作同时涉及读和写。执行该查询后，源表会记录在 `base_objects_accessed` 字段中，而目标 stage 会记录在 `objects_modified` 字段中。