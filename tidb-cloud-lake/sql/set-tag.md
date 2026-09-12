---
title: SET TAG and UNSET TAG
summary: 为数据库对象分配或移除标签。
---

# SET TAG and UNSET TAG

为数据库对象分配或移除标签。标签必须先使用 [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) 创建，然后才能分配。

另请参阅：[CREATE TAG](/tidb-cloud-lake/sql/create-tag.md)、[TAG_REFERENCES](/tidb-cloud-lake/sql/tag-references.md)。

## 语法 {#syntax}

```sql
-- Assign tags
ALTER { DATABASE | TABLE | VIEW | STAGE | CONNECTION
      | USER | ROLE | STREAM | FUNCTION | PROCEDURE }
    [ IF EXISTS ] <object_name>
    SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

-- Remove tags
ALTER { DATABASE | TABLE | VIEW | STAGE | CONNECTION
      | USER | ROLE | STREAM | FUNCTION | PROCEDURE }
    [ IF EXISTS ] <object_name>
    UNSET TAG <tag_name> [, <tag_name> ...]
```

## 支持的对象类型 {#supported-object-types}

| 对象类型 | 对象名称格式 | 示例 |
|-------------|-------------------|---------|
| DATABASE    | `<database>` | `ALTER DATABASE mydb SET TAG env = 'prod'` |
| TABLE       | `[<database>.]<table>` | `ALTER TABLE mydb.users SET TAG env = 'prod'` |
| VIEW        | `[<database>.]<view>` | `ALTER VIEW mydb.active_users SET TAG env = 'prod'` |
| STAGE       | `<stage>` | `ALTER STAGE my_stage SET TAG env = 'prod'` |
| CONNECTION  | `<connection>` | `ALTER CONNECTION my_conn SET TAG env = 'prod'` |
| USER        | `'<user>'` | `ALTER USER 'alice' SET TAG env = 'prod'` |
| ROLE        | `<role>` | `ALTER ROLE analyst SET TAG env = 'prod'` |
| STREAM      | `[<database>.]<stream>` | `ALTER STREAM mydb.my_stream SET TAG env = 'prod'` |
| FUNCTION    | `<function>` | `ALTER FUNCTION my_udf SET TAG env = 'prod'` |
| PROCEDURE   | `<name>(<arg_types>)` | `ALTER PROCEDURE my_proc(INT) SET TAG env = 'prod'` |

> **注意：**
>
> - 如果标签定义了 `ALLOWED_VALUES`，则该值必须是允许值之一。
> - 对不存在的标签名执行 `UNSET TAG` 会返回错误，除非对象本身不存在且指定了 `IF EXISTS`。
> - 对于 PROCEDURE，必须在对象名称中包含参数类型签名。

## 示例 {#examples}

### 为数据库和表添加标签 {#tag-a-database-and-table}

```sql
CREATE TAG env ALLOWED_VALUES = ('dev', 'staging', 'prod');
CREATE TAG owner;

ALTER DATABASE default SET TAG env = 'prod';
ALTER TABLE default.my_table SET TAG env = 'staging', owner = 'team_a';
```

### 为 stage 和 connection 添加标签 {#tag-a-stage-and-connection}

```sql
ALTER STAGE data_stage SET TAG env = 'dev', owner = 'data_team';
ALTER CONNECTION my_s3 SET TAG env = 'prod';
```

### 为视图添加标签 {#tag-a-view}

```sql
ALTER VIEW default.active_users SET TAG env = 'prod', owner = 'analytics';
```

### 为用户和角色添加标签 {#tag-a-user-and-role}

```sql
ALTER USER 'alice' SET TAG env = 'prod', owner = 'security';
ALTER ROLE analyst SET TAG env = 'dev';
```

### 为 UDF 和存储过程添加标签 {#tag-a-udf-and-procedure}

```sql
ALTER FUNCTION my_udf SET TAG env = 'dev';
ALTER PROCEDURE my_proc(DECIMAL(10,2)) SET TAG env = 'prod';
```

### 移除标签 {#remove-tags}

```sql
ALTER TABLE default.my_table UNSET TAG env, owner;
ALTER STAGE data_stage UNSET TAG env;
ALTER USER 'alice' UNSET TAG env, owner;
```