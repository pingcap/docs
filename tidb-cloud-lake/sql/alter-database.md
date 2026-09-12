---
title: ALTER DATABASE
summary: 修改数据库名称，或为数据库设置默认存储选项。
---

# ALTER DATABASE

修改数据库名称，或为数据库设置默认存储选项。

## 语法 {#syntax}

```sql
-- Rename a database
ALTER DATABASE [ IF EXISTS ] <name> RENAME TO <new_db_name>

-- Set default storage options
ALTER DATABASE [ IF EXISTS ] <name> SET OPTIONS (
    DEFAULT_STORAGE_CONNECTION = '<connection_name>'
  | DEFAULT_STORAGE_PATH = '<path>'
)
```

## 参数 {#parameters}

| 参数                        | 描述                                                                                                                                             |
|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| `DEFAULT_STORAGE_CONNECTION` | 现有连接的名称（通过 `CREATE CONNECTION` 创建），用作此数据库中表的默认存储连接。                                                               |
| `DEFAULT_STORAGE_PATH`       | 此数据库中表的默认存储路径 URI（例如 `s3://bucket/path/`）。必须以 `/` 结尾，并且与连接的存储类型匹配。                                        |

> **注意：**
>
> - `SET OPTIONS` 仅影响在语句执行后创建的表。现有表不会被修改。
> - 你一次只能修改一个选项，前提是另一个选项已存在于该数据库上。

## 示例 {#examples}

### 重命名数据库 {#rename-a-database}

```sql
CREATE DATABASE LAKE;
```

```sql
SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| LAKE           |
| information_schema |
| default            |
| system             |
+--------------------+
```

```sql
ALTER DATABASE `LAKE` RENAME TO `NEW_LAKE`;
```

```sql
SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| NEW_LAKE       |
| default            |
| system             |
+--------------------+
```

### 设置默认存储选项 {#set-default-storage-options}

```sql
ALTER DATABASE analytics SET OPTIONS (
    DEFAULT_STORAGE_CONNECTION = 'my_s3',
    DEFAULT_STORAGE_PATH = 's3://mybucket/analytics_v2/'
);
```

## 标签操作 {#tag-operations}

为数据库分配或移除标签。必须先使用 [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) 创建标签。完整详情请参见 [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md)。

### 语法 {#syntax}

```sql
ALTER DATABASE [ IF EXISTS ] <name> SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

ALTER DATABASE [ IF EXISTS ] <name> UNSET TAG <tag_name> [, <tag_name> ...]
```

### 示例 {#examples}

```sql
ALTER DATABASE mydb SET TAG env = 'prod', owner = 'team_a';
ALTER DATABASE mydb UNSET TAG env, owner;
```