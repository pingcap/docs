---
title: CREATE DATABASE
summary: 创建数据库。
---

# CREATE DATABASE

创建数据库。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] DATABASE [ IF NOT EXISTS ] <database_name>
    [ OPTIONS (
        DEFAULT_STORAGE_CONNECTION = '<connection_name>',
        DEFAULT_STORAGE_PATH = '<path>'
    ) ]
```

## 参数 {#parameters}

| 参数                        | 描述                                                                                                                                             |
|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| `DEFAULT_STORAGE_CONNECTION` | 要用作此数据库中表的默认存储连接的现有连接名称（通过 `CREATE CONNECTION` 创建）。                                                                |
| `DEFAULT_STORAGE_PATH`       | 此数据库中表的默认存储路径 URI（例如 `s3://bucket/path/`）。必须以 `/` 结尾，并且与连接的存储类型匹配。                                         |

> **注意：**
>
> - `DEFAULT_STORAGE_CONNECTION` 和 `DEFAULT_STORAGE_PATH` 必须同时指定。仅指定其中一个会报错。
> - 当同时设置这两个选项时，{{{ .lake }}} 会验证连接是否存在、路径 URI 格式是否正确，以及存储位置是否可访问。

## 访问控制要求 {#access-control-requirements}

| 权限            | 对象类型    | 描述         |
|:----------------|:------------|:-------------|
| CREATE DATABASE | 全局        | 创建数据库。 |

要创建数据库，执行该操作的用户或 [current_role](/tidb-cloud-lake/guides/roles.md) 必须具有 CREATE DATABASE [权限](/tidb-cloud-lake/guides/privileges.md)。

## 示例 {#examples}

### 创建基本数据库 {#creating-a-basic-database}

以下示例创建一个名为 `test` 的数据库：

```sql
CREATE DATABASE test;
```

### 创建带默认存储连接的数据库 {#creating-a-database-with-a-default-storage-connection}

以下示例先使用 AWS IAM role 创建一个连接，然后创建一个将该连接用作默认存储的数据库。与 access keys 相比，使用 IAM role 更安全，因为它不需要将凭证存储在 {{{ .lake }}} 中。

```sql
CREATE CONNECTION my_s3
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::987654321987:role/lake-test';

CREATE DATABASE analytics OPTIONS (
    DEFAULT_STORAGE_CONNECTION = 'my_s3',
    DEFAULT_STORAGE_PATH = 's3://mybucket/analytics/'
);
```

> **注意：**
>
> 要在 {{{ .lake }}} 中使用 IAM roles，你需要在你的 AWS account 与 {{{ .lake }}} 之间建立信任关系。详细说明请参见[使用 AWS IAM Role 进行身份验证](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md)。