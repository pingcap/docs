---
title: User-Controlled Log Redaction
summary: 了解如何为 TiDB Cloud Dedicated 集群启用或禁用用户控制的日志隐藏功能，以管理执行日志中的敏感数据可见性。
---

# User-Controlled Log Redaction

用户控制的日志隐藏功能让你可以管理 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群日志中敏感数据的可见性。通过切换此隐藏功能，你可以保护你的信息，在操作需求与安全之间取得平衡，并控制在集群日志中显示的内容。

日志隐藏默认已启用，确保运行中的日志和执行计划中的敏感信息被隐藏。如果你在集群维护或SQL调优时需要更详细的日志信息，可以随时禁用此功能。

> **Note:**
>
> 日志隐藏功能仅支持 TiDB Cloud Dedicated 集群。

## 前提条件

* 你必须是 TiDB Cloud 中组织的 **Organization Owner** 或 **Project Owner** 角色。
* 当集群处于 `paused` 状态时，不能启用或禁用日志隐藏。

## 禁用日志隐藏

> **Warning:**
>
> 禁用日志隐藏可能会暴露敏感信息，增加数据泄露的风险。在继续操作前，请确保你理解并已确认此风险。完成诊断或维护任务后，请务必尽快重新启用。

要禁用日志隐藏，请按照以下步骤操作：

1. 登录到 [TiDB Cloud 控制台](https://tidbcloud.com/)。
2. 转到 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的组合框在组织、项目和集群之间切换。

3. 在左侧导航栏中，点击 **Settings** > **Security**。
4. 在 **Execution Log Redaction** 部分，你会看到默认状态为 **Enabled**。
5. 点击 **Disable**。会弹出一个警告，说明禁用日志隐藏的风险。
6. 确认禁用。

禁用日志隐藏后，请注意以下事项：

* 该更改仅影响新的数据库连接。
* 现有连接不受影响。你需要重新连接以使更改生效。
* 新会话的日志将不再被隐藏。

## 查看更新后的日志

在禁用日志隐藏后，若要查看更新的日志，请执行以下操作：

1. 模拟由慢查询引起的性能问题。例如，执行以下SQL语句：

    ```sql
    SELECT *, SLEEP(2) FROM users WHERE email LIKE "%useremail%";
    ```

2. 等待几分钟，让慢查询日志更新。
3. 查看日志，确认敏感数据已不再被隐藏。

## 启用日志隐藏

为确保数据安全，在完成诊断或维护任务后，应立即**启用日志隐藏**，操作如下：

1. 登录到 [TiDB Cloud 控制台](https://tidbcloud.com/)。
2. 转到 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称，进入其概览页面。

    > **Tip:**
    >
    > 你可以使用左上角的组合框在组织、项目和集群之间切换。

3. 在左侧导航栏中，点击 **Settings** > **Security**。
4. 在 **Execution Log Redaction** 部分，你会看到当前状态为 **Disabled**。
5. 点击 **Enable** 以启用。
6. 重新连接数据库，使更改在新会话中生效。
