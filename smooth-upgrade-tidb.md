---
title: TiDB 平滑升级
summary: 本文档介绍了 TiDB 的平滑升级功能，该功能支持在无需手动取消 DDL 操作的情况下升级 TiDB 集群。
---

# TiDB 平滑升级

本文档介绍了 TiDB 的平滑升级功能，该功能支持在无需手动取消 DDL 操作的情况下升级 TiDB 集群。

从 v7.1.0 版本开始，当你将 TiDB 升级到后续版本时，TiDB 支持平滑升级。该功能消除了升级过程中的限制，提供了更友好的升级体验。注意，在升级过程中，你需要确保没有用户发起的 DDL 操作。

## 支持的版本

根据该功能是否需要通过开关控制，有两种方式使用平滑升级：

- 该功能默认开启，无需通过开关控制。目前，支持此方法的版本有 v7.1.0、v7.1.1、v7.2.0 和 v7.3.0。具体支持的版本如下：
    - 从 v7.1.0 升级到 v7.1.1、v7.2.0 或 v7.3.0
    - 从 v7.1.1 升级到 v7.2.0 或 v7.3.0
    - 从 v7.2.0 升级到 v7.3.0

- 该功能默认关闭，可以通过发送 `/upgrade/start` 请求启用。详情请参见 [TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-8.1/docs/tidb_http_api.md)。支持的版本如下：
    - 从 v7.1.2 及之后的 v7.1 版本（即 v7.1.x，x >= 2）升级到 v7.4.0 及之后的版本
    - 从 v7.4.0 升级到后续版本

请参考下表，了解特定版本支持的升级方式：

| 原始版本 | 升级版本 | 升级方式 | 备注 |
|------|--------|-------------|-------------|
| < v7.1.0  | 任何版本                 | 不支持平滑升级。 | |
| v7.1.0    | v7.1.1、v7.2.0 或 v7.3.0   | 自动支持平滑升级。无需额外操作。 | 实验性功能。可能遇到[#44760](https://github.com/pingcap/tidb/pull/44760)问题。 |
| v7.1.1    | v7.2.0 或 v7.3.0         | 自动支持平滑升级。无需额外操作。 | 实验性功能。  |
| v7.2.0    | v7.3.0                   | 自动支持平滑升级。无需额外操作。 | 实验性功能。  |
| [v7.1.2, v7.2.0)                     | [v7.1.2, v7.2.0) | 通过发送 `/upgrade/start` HTTP 请求启用平滑升级。有两种方法：[使用 TiUP](#use-tiup-to-upgrade) 和 [其他升级方法](#other-upgrade-methods) | 在未启用平滑升级时，确保升级期间不执行任何 DDL 操作。 |
| [v7.1.2, v7.2.0) 或 >= v7.4.0             | >= v7.4.0 | 通过发送 `/upgrade/start` HTTP 请求启用平滑升级。有两种方法：[使用 TiUP](#use-tiup-to-upgrade) 和 [其他升级方法](#other-upgrade-methods) | 在未启用平滑升级时，确保升级期间不执行任何 DDL 操作。 |
| v7.1.0、v7.1.1、v7.2.0 和 v7.3.0     | >= v7.4.0 | 不支持平滑升级。 | |

## 功能介绍

在引入平滑升级功能之前，升级过程中对 DDL 操作存在以下限制：

- 在升级过程中运行 DDL 操作可能导致 TiDB 出现未定义行为。
- 在升级 TiDB 时进行 DDL 操作可能导致 TiDB 出现未定义行为。

这些限制可以总结为：你需要确保在升级过程中没有用户发起的 DDL 操作。引入平滑升级功能后，TiDB 在升级过程中不再受此限制。

更多信息请参见 [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md#upgrade-tidb-using-tiup) 中的 **Warning** 内容。

### 升级步骤

#### 使用 TiUP 升级

从 v1.14.0 版本开始，TiUP 自动支持此功能。也就是说，你可以直接使用 `tiup cluster upgrade` 命令升级 TiDB 集群。注意，目前不支持 `tiup cluster patch` 命令。

#### 使用 TiDB Operator 升级

目前不支持此功能。会尽快支持。

#### 其他升级方法

你可以按照以下步骤手动或通过脚本升级 TiDB：

1. 发送 HTTP 升级开始请求到集群中的任意 TiDB 节点：`curl -X POST http://{TiDBIP}:10080/upgrade/start`。
   * TiDB 集群进入 **Upgrading** 状态。
   * 待执行的 DDL 操作会暂停。

2. 替换 TiDB 二进制文件并进行滚动升级。此过程与原有升级流程相同。
    * 升级过程中会执行系统 DDL 操作。

3. 当集群中的所有 TiDB 节点都成功升级后，向任意 TiDB 节点发送 HTTP 升级完成请求：`curl -X POST http://{TiDBIP}:10080/upgrade/finish`。
    * 用户暂停的 DDL 操作会恢复。

## 限制

使用平滑升级功能时，请注意以下限制。

> **Note:**
>
> 本节中的限制不仅适用于使用平滑升级功能的场景，也适用于 [使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md#upgrade-tidb-using-tiup)。

### 用户操作限制

* 升级前应考虑以下限制：

    * 如果集群中存在取消中的 DDL 作业，即用户正在取消的 DDL 作业，由于取消中的作业无法暂停，TiDB 会重试取消作业。如果重试失败，会报错并退出升级。
    * 如果你当前的 TiDB 版本早于 v8.1.0，且启用了 TiDB 分布式执行框架（DXF），请通过设置 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 为 `OFF` 来禁用它。确保所有正在进行的分布式 `ADD INDEX` 和 `IMPORT INTO` 任务已完成。或者，你可以取消这些任务，等待升级完成后再重新启动。否则，升级期间的 `ADD INDEX` 操作可能导致数据索引不一致。如果你当前的 TiDB 版本为 v8.1.0 或更高，则无需禁用 DXF，可以忽略此限制。

* 在使用 TiUP 升级 TiDB 时，由于 TiUP 升级存在超时限制，如果在升级前集群中有大量（超过 300 个）排队等待的 DDL 作业，升级可能失败。

* 升级期间，不允许进行以下操作：

    * 在系统表（`mysql.*`、`information_schema.*`、`performance_schema.*` 和 `metrics_schema.*`）上运行 DDL 操作。
    * 手动取消 DDL 作业：`ADMIN CANCEL DDL JOBS job_id [, job_id] ...;`。
    * 导入数据。

### 工具限制

* 在升级过程中，不支持使用以下工具：

    * BR：BR 可能会复制暂停的 DDL 作业到 TiDB。暂停的 DDL 作业无法自动恢复，可能导致 DDL 作业后续卡住。

    * DM 和 TiCDC：如果在升级过程中使用 DM 或 TiCDC 导入 SQL 语句到 TiDB，且其中某个 SQL 语句包含 DDL 操作，导入操作会被阻塞，可能出现未定义的错误。

### 插件限制

TiDB 中安装的插件可能包含 DDL 操作。然而，在升级过程中，如果插件中的 DDL 操作是在非系统表上执行的，升级可能会失败。