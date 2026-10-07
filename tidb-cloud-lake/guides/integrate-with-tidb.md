---
title: TiDB 集成任务（预览版）
summary: 使用全量快照导入、持续 CDC 或两者结合的方式，将数据从 TiDB 集群复制到 TiDB Cloud Lake。
---

# TiDB 集成任务（预览版）

TiDB 集成任务用于将数据从 TiDB 集群复制到 TiDB Cloud Lake。它支持通过 Dumpling 导出的全量 `Snapshot` 导入、通过 TiCDC changefeed 的持续 `Change Data Capture (CDC)`，或两者结合使用。

如果你需要先创建可复用的暂存存储桶设置，请参见 [TiDB 数据源](/tidb-cloud-lake/guides/tidb-data-source.md)。

## 使用场景 {#use-cases}

- 将 TiDB 数据库和表迁移到 TiDB Cloud Lake 以进行分析
- 通过 TiCDC 使 TiDB Cloud Lake 与 TiDB 持续保持同步
- 在一个任务中将分片数据库整合到按源划分的目标数据库中
- 仅运行一次全量导入，或将全量导入与持续变更捕获结合使用

## 同步模式 {#sync-modes}

| 同步模式 | 描述 |
|-----------|-------------|
| Snapshot | 执行一次性全量数据导入，数据来源于 Dumpling 导出。适用于初始迁移或周期性批量刷新。 |
| CDC Only | 持续消费 TiCDC changefeed，并应用实时变更（插入、修改、删除）。 |
| Snapshot + CDC | 先执行全量快照导入，然后切换到持续 CDC。推荐用于大多数使用场景。 |

## 前提条件 {#prerequisites}

在创建 TiDB 集成任务之前，请确保：

- 已创建 **TiDB** 数据源。
- 数据源中配置的对象存储存储桶可从 TiDB Cloud Lake 访问。
- 你要同步的表对应的 TiCDC / Dumpling 导出内容，已写入该存储桶中，并位于任务中将要引用的前缀下。

## 创建 TiDB 集成任务 {#creating-a-tidb-integration-task}

本节将指导你在 TiDB Cloud Lake 中创建 TiDB 集成任务。

### 步骤 1：配置基本设置 {#step-1-configure-basic-settings}

1. 进入 **Data** > **Data Integration**，然后点击 **Create Task**。
2. 选择一个 **TiDB** 数据源，然后配置以下基本设置：

| 字段 | 必填 | 描述 |
|-------|----------|-------------|
| **Data Source** | 是 | 选择一个已有的 **TiDB - Credentials** 数据源。你也可以在此处创建一个 |
| **Name** | 是 | 此集成任务的名称 |
| **Sync Mode** | 是 | 选择 **Snapshot**、**CDC Only** 或 **Snapshot + CDC** |
| **Table Rules** | 是 | 用于选择要同步哪些源对象的规则。参见 [表规则](#table-rules) |
| **Max Matched Tables** | 否 | 规则可匹配的表数量上限。留空则使用系统默认值（500） |
| **Dumpling S3 Prefix** | 是（Snapshot 模式） | 保存 Dumpling 导出的存储桶前缀，例如 `dumpling/export` |
| **Table Parallelism** | 否 | 并发导入的表数量（默认值：4） |
| **Warehouse** | 是 | 用于运行该任务的 TiDB Cloud Lake 计算集群 |

### 表规则 {#table-rules}

每行输入一条规则。每条规则的格式为 `schemaPattern.tablePattern`，可选择使用前缀 `!` 表示排除：

```text
app.orders             an exact table
shard_*.*              every table of every shard_ database
!*.tmp_*               exclude temporary tables
```

规则按从后到前的顺序进行求值。第一个同时匹配数据库模式和表模式的规则决定最终结果。未匹配任何规则的对象会被排除。如果规则列表中只有排除规则，则会隐式添加一个前置 `*.*`。

每个匹配到的源数据库都会写入各自独立的目标数据库，因此不同源数据库中同名的表会保持分离。这也是在单个任务中同步多个源数据库的唯一方式。

点击 **Preview Matched Tables**，可根据当前规则对前缀下实际存在的对象进行匹配评估。预览结果会列出匹配到的源数据库和表，以及推导出的目标数据库和表。

### Snapshot 选项 {#snapshot-options}

当同步模式包含快照时，还可以通过以下附加选项控制 Dumpling 导出的导入方式：

| 字段                          | 默认值 | 描述                                                                                                              |
| ------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Auto Create Table**          | Yes     | 根据源 schema 自动创建目标表                                                                                             |
| **Purge After Load**           | No      | 成功导入后，从存储桶中删除源对象。需要具备删除权限                                                                       |
| **On Error**                   | Abort   | **Abort** 表示在遇到第一个错误时退出；**Continue** 表示跳过失败的行并继续导入                                           |
| **CSV Separator**              | `,`     | Dumpling 导出使用的字段分隔符                                                                                            |
| **Skip Header Rows**           | Yes     | 第一行是否包含列名。当导出包含表头行时，选择 **YES**                                                                     |
| **Export Escaped Backslashes** | No      | 必须与 Dumpling 的 `--escape-backslash` 设置保持一致。                                                                   |

### 目标名称前后缀 {#target-name-affixes}

目标数据库名和表名由源名称派生而来，并可附加可选的前后缀：

```text
target database = targetDatabasePrefix + sourceDatabase + targetDatabaseSuffix
target table    = targetTablePrefix    + sourceTable    + targetTableSuffix
```

如果将这些前后缀留空，则直接使用源名称。前后缀只能包含字母、数字和下划线。

例如，当数据库前缀为 `src_` 时，源数据库 `shard_1` 和表 `orders` 会写入到 `src_shard_1.orders`。

### 步骤 2：创建任务 {#step-2-create-the-task}

检查设置无误后，点击 **Create** 创建集成任务。

## 不同同步模式下的任务行为 {#task-behavior-by-sync-mode}

| 同步模式 | 行为 |
|-----------|----------|
| 快照 | 运行一次，并在全量导入完成后自动下线。 |
| CDC Only | 持续运行，消费 changefeed 事件，直到手动下线。 |
| Snapshot + CDC | 先完成全量快照导入，然后切换到持续 CDC，直到手动下线。 |

对于 CDC 任务，进度会保存为 checkpoint。当任务被下线并重启后，会从保存的位置继续，而不是从头重新导入。

## 高级配置 {#advanced-configuration}

以下设置为任务级参数，用于调优发现、导入和合并过程。

| 参数 | Default | 描述 |
|-----------|---------|-------------|
| **Table Parallelism** | 4 | 控制并发处理的表数量。更高的值会提高吞吐，但也会消耗更多计算集群资源。 |
| **Poll Interval** | 60 seconds | 任务列出暂存存储桶（以及消费可选 SQS 队列）以发现新的 changefeed / 导出对象的频率。更短的间隔可降低延时，但会增加 list 请求次数。对于 OSS，仅使用轮询进行发现。 |
| **Batch File Count** | 100 | 每批处理的 CDC 事件文件最大数量。可根据需要调整，以平衡内存使用和吞吐。 |
| **Merge Interval** | 30 seconds | 将捕获到的变更合并到目标表的频率。更短的间隔可降低延时，但会增加合并活动。 |
| **Allow Delete** | Disabled | 是否将从 changefeed 捕获到的 `DELETE` 操作应用到目标表。禁用时，会忽略删除操作并保留历史行。 |
| **Max Matched Tables** | 500 | 规则可匹配的源表数量上限。如果规则匹配数量超过此限制，任务会失败，并列出超限的匹配项。 |