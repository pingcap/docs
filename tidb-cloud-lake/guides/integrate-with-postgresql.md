---
title: PostgreSQL 集成任务
summary: 本页介绍如何创建一个 PostgreSQL 集成任务，将 PostgreSQL 数据库中的数据同步到 {{{ .lake }}}。
---

# PostgreSQL 集成任务

本页介绍如何创建一个 PostgreSQL 集成任务，将 PostgreSQL 数据库中的数据同步到 {{{ .lake }}}。PostgreSQL 任务支持全量 `Snapshot` 导入、持续的 `Change Data Capture (CDC)`，或两者结合使用。

如果你需要先创建可复用的 PostgreSQL 连接设置，请参见 [PostgreSQL - Credentials](/tidb-cloud-lake/guides/postgresql-credentials.md)。

## 同步模式 {#sync-modes}

| 同步模式      | 描述                                                                                                  |
|----------------|--------------------------------------------------------------------------------------------------------------|
| Snapshot       | 对源表执行一次性全量数据导入。适用于初始数据迁移或周期性批量导入。 |
| CDC Only       | 通过 PostgreSQL 逻辑复制持续捕获实时变更（插入、修改、删除）。合并操作需要主键。 |
| Snapshot + CDC | 先执行一次完整快照，然后无缝切换到持续 CDC。推荐用于大多数使用场景。 |

## 前提条件 {#prerequisites}

在设置 PostgreSQL 数据集成之前，请确保你的 PostgreSQL 实例满足以下要求：

- 已创建 **PostgreSQL - Credentials** 数据源
- 目标 PostgreSQL 实例可从 {{{ .lake }}} 访问
- PostgreSQL 版本为 10 或更高

### 启用逻辑复制 {#enable-logical-replication}

对于 CDC 和 Snapshot + CDC 模式，必须将 PostgreSQL WAL (Write-Ahead Log) 配置为 logical 级别：

```ini title='postgresql.conf'
wal_level = logical
max_replication_slots = 4
max_wal_senders = 4
```

修改配置后，重启 PostgreSQL 使更改生效。

### 创建专用用户（推荐） {#create-a-dedicated-user-recommended}

创建一个具有数据复制所需权限的 PostgreSQL 用户：

```sql
CREATE USER lake_cdc WITH PASSWORD 'your_password' REPLICATION;
GRANT CONNECT ON DATABASE your_database TO lake_cdc;
GRANT USAGE ON SCHEMA public TO lake_cdc;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO lake_cdc;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO lake_cdc;
```

### 创建发布和复制槽（CDC 必需） {#create-publication-and-replication-slot-required-for-cdc}

对于 CDC 和 Snapshot + CDC 模式，必须存在发布和复制槽。由于 `CREATE PUBLICATION ... FOR ALL TABLES` 需要超级用户权限，而添加单独的表又需要表所有权，因此在启动 CDC 任务之前，应由数据库所有者或超级用户创建这些对象。

请以超级用户或数据库所有者身份运行以下命令：

```sql
-- Create a publication that includes the tables you want to replicate
CREATE PUBLICATION bend_cdc_pub FOR ALL TABLES;

-- Create a logical replication slot
SELECT * FROM pg_create_logical_replication_slot('bend_cdc_slot', 'pgoutput');

-- Grant the dedicated user permission to use the replication slot
ALTER ROLE lake_cdc WITH REPLICATION;
```

> **Note:**
>
> 如果你只需要复制特定表而不是所有表，可以使用：
>
> ```sql
> CREATE PUBLICATION bend_cdc_pub FOR TABLE table1, table2;
> ```
>
> 这样可以避免超级用户要求，但仍然需要对所列出的表拥有所有权。

### 网络访问 {#network-access}

请确保 PostgreSQL 实例可从 {{{ .lake }}} 访问。检查防火墙规则和安全组设置，允许 PostgreSQL 端口上的入站连接。

## 创建 PostgreSQL 集成任务 {#creating-a-postgresql-integration-task}

### 第 1 步：基本信息 {#step-1-basic-info}

1. 进入 **Data** > **Data Integration**，然后点击 **Create Task**。

2. 配置基本设置：

    | 字段                      | 必填    | 描述                                                                                      |
    |----------------------------|-------------|--------------------------------------------------------------------------------------------------|
    | **Data Source**             | Yes         | 从下拉列表中选择一个现有的 **PostgreSQL - Credentials** 数据源                    |
    | **Name**                   | Yes         | 此集成任务的名称                                                                 |
    | **Source Database**        | —           | 根据所选数据源自动显示                                        |
    | **Source Table**           | Yes         | 选择要从 PostgreSQL 数据库同步的表                                            |
    | **Sync Mode**             | Yes         | 从 **Snapshot**、**CDC Only** 或 **Snapshot + CDC** 中选择                                    |
    | **Primary Key**          | Conditional | 用于合并操作的唯一标识列。CDC Only 和 Snapshot + CDC 模式下必填 |
    | **Sync Interval**        | Yes         | 写入操作之间的时间间隔（秒）（默认值：3）                                      |
    | **Batch Size**            | No          | 每批处理的行数                                                                         |
    | **Allow Delete**          | No          | 是否允许在 CDC 中执行 DELETE 操作。适用于 CDC Only 和 Snapshot + CDC 模式       |

#### Snapshot 模式选项 {#snapshot-mode-options}

使用 **Snapshot** 模式时，还可以使用以下附加选项：

- **Snapshot WHERE Condition**：在执行快照时用于过滤数据的 SQL WHERE 子句（例如，`created_at > '2024-01-01'`）。这样你可以只导入源数据的一个子集。

### 第 2 步：预览数据 {#step-2-preview-data}

配置完基本设置后，点击 **Next** 预览源数据。

系统会从所选 PostgreSQL 表中获取一行示例数据，并显示列名和数据类型。在继续之前，请检查数据以确保选择了正确的表和列。

### 第 3 步：设置目标表 {#step-3-set-target-table}

在 {{{ .lake }}} 中配置目标位置：

| 字段               | 描述                                                        |
|---------------------|--------------------------------------------------------------------|
| **Warehouse**       | 选择用于运行同步任务的目标 {{{ .lake }}} 计算集群 (Warehouse)    |
| **Target Database** | 选择 {{{ .lake }}} 中的目标数据库                             |
| **Target Table**    | {{{ .lake }}} 中的表名（默认为源表名）     |

系统会自动将源列映射到目标表结构。检查列映射后，点击 **Create** 完成集成任务创建。

## 按同步模式划分的任务行为 {#task-behavior-by-sync-mode}

| 同步模式      | 行为                                                                                          |
|----------------|---------------------------------------------------------------------------------------------------|
| Snapshot       | 运行一次，并在全量数据导入完成后自动下线。                           |
| CDC Only       | 持续运行，捕获实时变更，直到手动下线。                            |
| Snapshot + CDC | 先完成初始快照，然后切换到持续 CDC，直到手动下线。   |

对于 CDC 任务，下线时会将当前 LSN (Log Sequence Number) 保存为检查点，因此在重启后，任务可以从上次停止的位置继续运行。

## 同步模式详情 {#sync-mode-details}

### Snapshot {#snapshot}

Snapshot 模式会对源表执行一次性全量读，并将所有数据加载到 {{{ .lake }}} 中的目标表。

**Use cases:**

- 从 PostgreSQL 到 {{{ .lake }}} 的初始数据迁移
- 周期性的全量数据刷新
- 使用 WHERE 条件过滤的一次性数据导入

**Features:**

- 支持使用 WHERE 条件过滤以导入部分数据
- 任务完成后会自动下线

### CDC (Change Data Capture) {#cdc-change-data-capture}

CDC 模式通过逻辑复制持续监控 PostgreSQL WAL (Write-Ahead Log)，并从源表中捕获实时的行级变更（INSERT、UPDATE、DELETE）。

**Use cases:**

- 实时数据复制
- 使 {{{ .lake }}} 与业务 PostgreSQL 数据库保持同步
- 事件驱动的数据管道

**How it works:**

1. 使用逻辑复制槽连接到 PostgreSQL
2. 通过 `pgoutput` 插件实时捕获行级变更
3. 将变更写入 {{{ .lake }}} 中的原始暂存表
4. 使用主键定期将变更合并到目标表
5. 保存检查点（LSN 位置）以便进行故障恢复

> **Note:**
>
> CDC 模式要求 PostgreSQL WAL 级别设置为 `logical`，并且必须指定主键（唯一列）。PostgreSQL 用户必须具有 `REPLICATION` 权限。

### Snapshot + CDC {#snapshot-cdc}

该模式结合了两种方式：先对源表执行完整快照，然后无缝切换到 CDC 模式以持续捕获变更。对于大多数数据集成场景，这是推荐模式，因为它既能确保完整的初始数据加载，又能提供后续持续的实时同步。

## 高级配置 {#advanced-configuration}

### 主键 {#primary-key}

主键指定了 CDC 期间用于 MERGE 操作的唯一标识列。当捕获到变更事件时，{{{ .lake }}} 使用该键来判断是插入新行还是修改现有行。通常，这应当是源表的主键。

### 同步间隔 {#sync-interval}

同步间隔（秒）控制将已捕获的变更合并到目标表的频率。较短的间隔可以提供更低的延时，但可能会增加资源使用量。默认值 3 秒适用于大多数工作负载。

### 批大小 {#batch-size}

用于控制数据加载期间每批处理的行数。调整此值有助于优化大表场景下的吞吐。留空则使用系统默认值。

### 允许删除 {#allow-delete}

启用后（CDC 模式下默认启用），从 PostgreSQL WAL 捕获到的 DELETE 操作会应用到 {{{ .lake }}} 中的目标表。禁用后，删除操作会被忽略，目标表将保留所有历史记录。这适用于希望保留完整审计轨迹的场景。
