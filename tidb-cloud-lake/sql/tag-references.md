---
title: TAG_REFERENCES
summary: 返回分配给指定数据库对象的所有标签。
---

# TAG_REFERENCES

返回分配给指定数据库对象的所有标签。你可以使用此函数审计标签分配情况，以满足治理和合规要求。

另请参阅：[SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md)。

## 语法 {#syntax}

```sql
SELECT * FROM TAG_REFERENCES('<object_name>', '<domain>')
```

| 参数       | 描述                                                        |
|-----------------|--------------------------------------------------------------------|
| `object_name`   | 对象名称。对于 tables/views/streams，使用 `db.name` 格式。对于 procedures，包含类型签名（例如 `my_proc(INT)`）。 |
| `domain`        | 对象类型：`DATABASE`、`TABLE`、`VIEW`、`STREAM`、`STAGE`、`CONNECTION`、`USER`、`ROLE`、`UDF` 或 `PROCEDURE`。        |

## 输出列 {#output-columns}

| 列            | 类型             | 描述                                 |
|-------------------|------------------|---------------------------------------------|
| `tag_name`        | String           | 标签名称                                              |
| `tag_value`       | String           | 分配给标签的值                                    |
| `object_database` | Nullable(String) | 数据库名称（对于 STAGE、CONNECTION、USER、ROLE、UDF、PROCEDURE 为 NULL） |
| `object_id`       | Nullable(UInt64) | 对象 ID（仅 DATABASE、TABLE、VIEW 为非 NULL）          |
| `object_name`     | String           | 对象名称                                           |
| `domain`          | String           | 对象类型                                                  |

## 示例 {#examples}

### 查询表上的标签 {#query-tags-on-a-table}

```sql
CREATE TAG env ALLOWED_VALUES = ('dev', 'staging', 'prod');
CREATE TAG owner;

CREATE TABLE default.users (id INT, name STRING);
ALTER TABLE default.users SET TAG env = 'prod', owner = 'team_a';

SELECT * EXCLUDE(object_id) FROM TAG_REFERENCES('default.users', 'TABLE');

┌───────────────────────────────────────────────────────────────────────┐
│ tag_name │ tag_value │ object_database │ object_name │    domain    │
├──────────┼───────────┼─────────────────┼─────────────┼──────────────┤
│ env      │ prod      │ default         │ users       │ TABLE        │
│ owner    │ team_a    │ default         │ users       │ TABLE        │
└───────────────────────────────────────────────────────────────────────┘
```

### 查询 stage 上的标签 {#query-tags-on-a-stage}

```sql
CREATE STAGE data_stage;
ALTER STAGE data_stage SET TAG env = 'staging', owner = 'data_team';

SELECT * EXCLUDE(object_id) FROM TAG_REFERENCES('data_stage', 'STAGE');

┌───────────────────────────────────────────────────────────────────────┐
│ tag_name │ tag_value │ object_database │ object_name │    domain    │
├──────────┼───────────┼─────────────────┼─────────────┼──────────────┤
│ env      │ staging   │ NULL            │ data_stage  │ STAGE        │
│ owner    │ data_team │ NULL            │ data_stage  │ STAGE        │
└───────────────────────────────────────────────────────────────────────┘
```

### 查询数据库上的标签 {#query-tags-on-a-database}

```sql
ALTER DATABASE default SET TAG env = 'prod';

SELECT * EXCLUDE(object_id) FROM TAG_REFERENCES('default', 'DATABASE');

┌───────────────────────────────────────────────────────────────────────┐
│ tag_name │ tag_value │ object_database │ object_name │    domain    │
├──────────┼───────────┼─────────────────┼─────────────┼──────────────┤
│ env      │ prod      │ default         │ default     │ DATABASE     │
└───────────────────────────────────────────────────────────────────────┘
```