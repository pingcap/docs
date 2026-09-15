---
title: Connection
summary: {{{ .lake }}} 中的 connection 是一种指定配置，用于封装与外部存储服务交互所需的详细信息。它作为一组集中且可复用的参数集合，例如访问凭证、端点 URL 和存储类型，从而便于 {{{ .lake }}} 与各种存储服务集成。
---

# Connection

## 什么是 Connection？ {#what-is-connection}

{{{ .lake }}} 中的 connection 是一种指定配置，用于封装与外部存储服务交互所需的详细信息。它作为一组集中且可复用的参数集合，例如访问凭证、端点 URL 和存储类型，从而便于 {{{ .lake }}} 与各种存储服务集成。

Connection 可用于创建 external stage、external table 以及 attach table，为通过 {{{ .lake }}} 管理和访问存储在外部存储服务中的数据提供了一种更简洁、模块化的方法。

## Connection 管理 {#connection-management}

| Command | Description |
|---------|-------------|
| [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) | 创建到外部存储服务的新连接 |
| [DROP CONNECTION](/tidb-cloud-lake/sql/drop-connection.md) | 删除现有的连接 |

## Connection 信息 {#connection-information}

| Command | Description |
|---------|-------------|
| [DESCRIBE CONNECTION](/tidb-cloud-lake/sql/desc-connection.md) | 显示指定连接的详细信息 |
| [SHOW CONNECTIONS](/tidb-cloud-lake/sql/show-connections.md) | 列出当前数据库中的所有连接 |

### 使用示例 {#usage-examples}

本节中的示例首先创建一个包含连接 Amazon S3 所需凭证的 connection。随后，这些示例使用已建立的 connection 来创建 external stage 并 attach 一个现有表。

以下语句会发起到 Amazon S3 的连接，并指定必要的连接参数：

```sql
CREATE CONNECTION toronto
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

```

#### 示例 1：使用 Connection 创建 External Stage {#example-1-creating-external-stage-with-connection}

以下示例使用前面定义的名为 `toronto` 的 connection 创建一个 external stage：

```sql
CREATE STAGE my_s3_stage
    URL = 's3://lake-toronto'
    CONNECTION = (CONNECTION_NAME = 'toronto');

-- Equivalent to the following statement without using a connection:

CREATE STAGE my_s3_stage
    URL = 's3://lake-toronto'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>'
    );

```

#### 示例 2：使用 Connection Attach Table {#example-2-attaching-table-with-connection}

[ATTACH TABLE](/tidb-cloud-lake/sql/attach-table.md) 页面提供了[示例](/tidb-cloud-lake/sql/attach-table.md#examples)，演示如何将 {{{ .lake }}} 中的新表与 {{{ .lake }}} 中的现有表连接，其中数据存储在名为 "lake-toronto" 的 Amazon S3 存储桶中。在每个示例中，步骤 3 都可以通过使用前面定义的名为 `toronto` 的 connection 进行简化：

```sql title='In {{{ .lake }}}:'
ATTACH TABLE employees_backup
    's3://lake-toronto/1/216/'
    CONNECTION = (CONNECTION_NAME = 'toronto');

```

```sql title='In {{{ .lake }}}:'
ATTACH TABLE population_readonly
    's3://lake-toronto/1/556/'
    CONNECTION = (CONNECTION_NAME = 'toronto')
    READ_ONLY;

```

#### 示例 3：使用 Connection 创建 External Table {#example-3-creating-external-table-with-connection}

本示例演示如何使用前面定义的名为 `toronto` 的 connection 创建名为 `BOOKS` 的 external table：

```sql
CREATE TABLE BOOKS (
    id BIGINT UNSIGNED,
    title VARCHAR,
    genre VARCHAR DEFAULT 'General'
)
's3://lake-toronto'
CONNECTION = (CONNECTION_NAME = 'toronto');

```