---
title: MySQL Integration Task
summary: MySQL 数据集成支持将 MySQL 数据库中的数据实时同步到 {{{ .lake }}}，支持全量 `Snapshot` 导入、持续 `Change Data Capture (CDC)`，或两者结合。
---

# MySQL Integration Task

本页介绍如何创建一个 MySQL 集成任务，将 MySQL 数据库中的数据同步到 {{{ .lake }}}。MySQL 任务支持全量 `Snapshot` 导入、持续 `Change Data Capture (CDC)`，或两者结合。

如果你需要先创建可复用的 MySQL 连接设置，请参见 [MySQL - Credentials](/tidb-cloud-lake/guides/mysql-credentials.md)。

## Sync Modes {#sync-modes}

| 同步模式      | 描述                                                                                                  |
|----------------|--------------------------------------------------------------------------------------------------------------|
| Snapshot       | 对源表执行一次性全量数据导入。适用于初始数据迁移或周期性批量导入。 |
| CDC Only       | 持续捕获 MySQL binlog 中的实时变更（插入、修改、删除）。合并操作需要主键。 |
| Snapshot + CDC | 先执行全量快照，然后无缝切换到持续 CDC。推荐用于大多数使用场景。 |

## Prerequisites {#prerequisites}

在设置 MySQL 数据集成之前，请确保你的 MySQL 实例满足以下要求：

- 已创建 **MySQL - Credentials** 数据源
- 目标 MySQL 实例可从 {{{ .lake }}} 访问

### Enable Binlog {#enable-binlog}

对于所有同步模式，都需要启用 MySQL 二进制日志。对于 **CDC Only** 和 **Snapshot + CDC**，二进制日志**必须**使用 `ROW` 格式和 `FULL` 行镜像：

```ini title='my.cnf'
[mysqld]
server-id=1
log-bin=mysql-bin
binlog-format=ROW
binlog-row-image=FULL
```

修改配置后，重启 MySQL 使更改生效。

### Create a Dedicated User (Recommended) {#create-a-dedicated-user-recommended}

创建一个具有数据复制所需权限的 MySQL 用户：

```sql
CREATE USER 'lake_cdc'@'%' IDENTIFIED BY 'your_password';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'lake_cdc'@'%';
FLUSH PRIVILEGES;
```

### Network Access {#network-access}

确保 MySQL 实例可从 {{{ .lake }}} 访问。检查防火墙规则和安全组，允许 MySQL 端口上的入站连接。

## Creating a MySQL Integration Task {#creating-a-mysql-integration-task}

### Step 1: Basic Info {#step-1-basic-info}

1. 进入 **Data** > **Data Integration**，然后点击 **Create Task**。

    ![Data Integration Page](/media/tidb-cloud-lake/dataintegration-page-with-create-button.png)

2. 配置基本设置：

    | 字段                      | 必填    | 描述                                                                                      |
    |----------------------------|-------------|--------------------------------------------------------------------------------------------------|
    | **Data Source**             | Yes         | 从下拉列表中选择一个已有的 **MySQL - Credentials** 数据源                         |
    | **Name**                   | Yes         | 此集成任务的名称                                                                 |
    | **Source Database**        | —           | 根据所选数据源自动显示                                        |
    | **Source Table**           | Yes         | 选择要从 MySQL 数据库同步的表                                                 |
    | **Sync Mode**             | Yes         | 从 **Snapshot**、**CDC Only** 或 **Snapshot + CDC** 中选择                                    |
    | **Primary Key**          | Conditional | 用于合并操作的唯一标识列。CDC Only 和 Snapshot + CDC 模式下必填 |
    | **Sync Interval**        | Yes         | 写入操作之间的间隔（秒）（默认值：3）                                      |
    | **Batch Size**            | No          | 每批处理的行数                                                                         |
    | **Allow Delete**          | No          | 是否允许在 CDC 中执行 DELETE 操作。适用于 CDC Only 和 Snapshot + CDC 模式       |

    ![Create Task - Basic Info](/media/tidb-cloud-lake/create-mysql-task-step1-basic-info.png)

#### Snapshot Mode Options {#snapshot-mode-options}

使用 **Snapshot** 模式时，还可以配置以下选项：

- **Snapshot WHERE Condition**：在快照期间用于过滤数据的 SQL WHERE 子句（例如 `created_at > '2024-01-01'`）。这样你可以只导入源数据的一个子集。

- **Archive Schedule**：启用周期性归档后，系统会按重复调度自动运行快照。启用后，会显示以下字段：

| 字段               | 描述                                                              |
|---------------------|--------------------------------------------------------------------------|
| **Cron Expression** | cron 格式的调度表达式（例如 `0 1 * * *` 表示每天凌晨 1:00）        |
| **Timezone**        | 调度使用的时区（默认值：UTC）                                 |
| **Mode**            | 归档频率 — **Daily**、**Weekly** 或 **Monthly**                |
| **Time Column**     | 用于按时间分区归档的时间列（例如 `created_at`） |

### Step 2: Preview Data {#step-2-preview-data}

配置完基本设置后，点击 **Next** 预览源数据。

![Preview Data](/media/tidb-cloud-lake/create-mysql-task-preview-data-step.png)

系统会从所选 MySQL 表中获取一行示例数据，并显示列名和数据类型。继续之前，请检查数据，确保选择了正确的表和列。

### Step 3: Set Target Table {#step-3-set-target-table}

在 {{{ .lake }}} 中配置目标位置：

| 字段               | 描述                                                        |
|---------------------|--------------------------------------------------------------------|
| **Warehouse**       | 选择用于运行同步任务的目标 {{{ .lake }}} 计算集群 (Warehouse)    |
| **Target Database** | 选择 {{{ .lake }}} 中的目标数据库                             |
| **Target Table**    | {{{ .lake }}} 中的表名（默认为源表名）     |

![Set Target Table](/media/tidb-cloud-lake/dataintegration-mysql-set-target-table.png)

系统会自动将源列映射到目标表结构。检查列映射后，点击 **Create** 完成集成任务创建。

## Task Behavior by Sync Mode {#task-behavior-by-sync-mode}

| 同步模式      | 行为                                                                                          |
|----------------|---------------------------------------------------------------------------------------------------|
| Snapshot       | 运行一次，并在全量数据导入完成后自动下线。                           |
| CDC Only       | 持续运行，捕获实时变更，直到手动下线。                            |
| Snapshot + CDC | 先完成初始快照，然后切换到持续 CDC，直到手动下线。   |

对于 CDC 任务，下线时会将当前 binlog 位置保存为检查点，因此在重启后，任务可以从上次中断的位置继续运行。

## Sync Mode Details {#sync-mode-details}

### Snapshot {#snapshot}

Snapshot 模式会对源表执行一次性全量读，并将所有数据导入到 {{{ .lake }}} 中的目标表。

**Use cases:**

- 从 MySQL 到 {{{ .lake }}} 的初始数据迁移
- 周期性全量数据刷新
- 带 WHERE 条件过滤的一次性数据导入

**Features:**

- 支持通过 WHERE 条件过滤，仅导入部分数据
- 支持为重复快照配置周期性归档调度
- 任务完成后会自动下线

### CDC (Change Data Capture) {#cdc-change-data-capture}

CDC 模式会持续监控 MySQL binlog，并捕获源表中的实时行级变更（INSERT、UPDATE、DELETE）。

**Use cases:**

- 实时数据复制
- 使 {{{ .lake }}} 与业务 MySQL 数据库保持同步
- 事件驱动的数据管道

**How it works:**

1. 使用唯一的 server ID 连接到 MySQL binlog
2. 实时捕获行级变更
3. 将变更写入 {{{ .lake }}} 中的原始暂存表
4. 使用主键定期将变更合并到目标表
5. 保存检查点（binlog 位置）以便故障恢复

> **Note:**
>
> CDC 模式要求启用 MySQL binlog 且使用 ROW 格式，并且必须指定主键（唯一列）。MySQL 用户必须具有 `REPLICATION SLAVE` 和 `REPLICATION CLIENT` 权限。

### Snapshot + CDC {#snapshot-cdc}

该模式结合了两种方式：先对源表执行全量快照，然后无缝切换到 CDC 模式以持续捕获变更。对于大多数数据集成场景，这是推荐模式，因为它既能确保完整的初始数据导入，又能提供后续持续的实时同步。

## Advanced Configuration {#advanced-configuration}

### Primary Key {#primary-key}

主键用于指定 CDC 期间 MERGE 操作所使用的唯一标识列。当捕获到变更事件时，{{{ .lake }}} 会使用该键来判断是插入新行还是修改现有行。通常，这应当是源表的主键。

### Sync Interval {#sync-interval}

同步间隔（秒）用于控制将捕获到的变更合并到目标表的频率。较短的间隔可以带来更低的延时，但可能会增加资源使用。默认值 3 秒适用于大多数工作负载。

### Batch Size {#batch-size}

用于控制数据加载期间每批处理的行数。调整该值有助于优化大表的吞吐。留空则使用系统默认值。

### Allow Delete {#allow-delete}

启用后（CDC 模式下默认启用），从 MySQL binlog 捕获到的 DELETE 操作会应用到 {{{ .lake }}} 中的目标表。禁用后，删除操作会被忽略，目标表会保留所有历史记录。这适用于需要保留完整审计轨迹的场景。

### Archive Schedule {#archive-schedule}

对于 Snapshot 模式，你可以配置周期性归档，使系统按重复调度自动运行快照。这适用于需要定期刷新数据、但又不希望承担持续 CDC 开销的场景。

- **Cron Expression**：用于调度的标准 cron 格式（例如 `0 1 * * *` 表示每天凌晨 1:00）
- **Mode**：选择 **Daily**、**Weekly** 或 **Monthly** 归档
- **Time Column**：指定用于基于时间分区的列（例如 `created_at`）
- **Timezone**：设置调度使用的时区（默认值：UTC）
