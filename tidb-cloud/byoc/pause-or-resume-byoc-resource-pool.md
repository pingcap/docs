---
title: 暂停或恢复 BYOC 资源池
summary: 了解如何暂停和恢复 TiDB Cloud BYOC 资源池、7 天自动恢复限制，以及计费和限制。
---

# 暂停或恢复 BYOC 资源池

你可以在空闲期间暂停 TiDB Cloud BYOC 资源池，以降低数据库计算成本，同时保留数据、备份和网络配置。暂停资源池会同时暂停池中的所有实例。你不能单独暂停或恢复某个实例。

资源池最多可以保持暂停状态 7 天。如果你没有提前恢复，TiDB Cloud 会在达到 7 天限制时自动开始恢复整个资源池。

## 开始之前 {#before-you-begin}

- 确保你拥有 `Organization Owner` 角色。更多信息，参见[管理资源池](/tidb-cloud/byoc/manage-resource-pools-byoc.md#required-role)。
- 确保资源池处于 **Active** 状态，并且池中的所有实例都可以下线。
- 在暂停资源池之前，完成或停止存在冲突的操作，例如数据导入或导出、DM、pipeline 或 changefeed 任务、升级以及容量变更。
- 在请求暂停之前，降低工作负载活动。TiDB Cloud 会在继续之前检查工作负载活动和其他依赖项。如果某项必需检查失败或无法完成，则不会继续暂停。

## 暂停 BYOC 资源池 {#pause-a-byoc-resource-pool}

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，点击左侧导航栏的 **BYOC Management** > **Resource Pools**。
2. 找到一个处于 **Active** 状态的资源池，点击其所在行中的 **...**，然后选择 **Pause**。

    或者，点击资源池名称打开 **Resource Pool Details** 页面，然后点击右上角的 **Pause**。

3. 在 **Pause Resource Pool?** 对话框中，查看此次操作会影响的托管实例数量。
4. （可选）选择 **Create a Manual Backup before pausing**。

    如果选择此项，TiDB Cloud 会在继续暂停之前为资源池中的每个实例创建一个手动备份。此过程可能需要较长时间。无论你是否选择此选项，都会执行强制性的数据保护。

5. 点击 **Pause Resource Pool**。

    TiDB Cloud 会在移除运行时计算资源之前完成所需的保护检查。等待资源池进入 **Paused** 状态。资源池中的所有实例会一起暂停。

在准备期间，TiDB Cloud 会执行所需检查以及你选择的任何手动备份。如果准备失败，资源池会返回 **Active** 状态，并且不会移除运行时计算资源。

一旦资源池进入 **Pausing** 状态，SQL 连接以及需要活动计算资源的操作将不可用。池中的所有实例都会参与暂停过程。在移除所需的运行时数据库计算资源后，资源池会进入 **Paused** 状态。

## 暂停期间的行为 {#behavior-while-paused}

当资源池处于 **Paused** 状态时：

- 池中的所有实例都会被暂停。你不能读写数据，也不能运行需要活动数据库计算资源的操作。
- 你的数据以及恢复资源池所需的持久化存储都会被保留。资源池不会被删除。
- 现有的网络配置和连接信息会被保留，以便资源池恢复后继续使用。
- 现有备份、日志和历史指标会按照各自的保留策略继续可用。不会生成新的运行时计算指标。
- 定时备份会被暂停，并且你不能创建新的手动备份。
- 你不能在已暂停的资源池中创建实例，也不能将备份恢复到该资源池。请先恢复资源池。
- 无法进行资源池配置和容量变更。

## 恢复 BYOC 资源池 {#resume-a-byoc-resource-pool}

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，点击左侧导航栏的 **BYOC Management** > **Resource Pools**。
2. 找到一个处于 **Paused** 状态的资源池，点击其所在行中的 **...**，然后选择 **Resume**。

    或者，点击资源池名称打开 **Resource Pool Details** 页面，然后点击右上角的 **Resume**。

3. 在 **Resume Resource Pool?** 对话框中，查看对所有托管实例的影响，然后点击 **Resume Resource Pool**。
4. 等待资源池及其托管实例恢复到 **Active** 状态。

    恢复操作最多可能需要 30 分钟。当资源池处于 **Resuming** 状态时，SQL 连接仍然不可用。

当 TiDB Cloud 恢复运行时计算资源并检查就绪状态时，资源池及其实例会进入 **Resuming** 状态。在恢复完成之前，SQL 连接始终不可用。在此过程中，配置和扩缩容操作也会被阻止。

资源池返回 **Active** 状态后，所有托管实例也会返回 **Active** 状态。SQL 连接、定时备份和常规监控都会恢复。你可以继续使用已保留的连接信息。

## 7 天后自动恢复 {#automatic-resume-after-7-days}

连续暂停的最长时长为 7 天，从资源池进入 **Paused** 状态时开始计算。处于 **Pausing** 状态的时间不计入此限制。

如果你在截止时间之前没有恢复资源池，TiDB Cloud 会自动开始恢复操作。资源池会进入 **Resuming** 状态，并且只有在完成所需的就绪检查后才会重新可用。

## 计费 {#billing}

BYOC 数据库 vCPU 费用遵循实际已配置的数据库计算容量：

- 在 **Pausing** 期间，随着计算节点被移除，数据库计算费用会降低。
- 在 **Paused** 期间，数据库 vCPU 费用为零，因为此时不再配置任何数据库计算节点。
- 在 **Resuming** 期间，随着重新配置计算节点，数据库计算费用会增加。

当资源池处于暂停状态时，你的云账户中与保留的存储、网络、备份及其他基础设施相关的费用可能仍会继续产生。更多信息，参见[TiDB Cloud BYOC 定价](/tidb-cloud/tidb-cloud-billing.md#pricing-for-byoc)。

## 故障排查 {#troubleshooting}

如果资源池在 **Pausing** 或 **Resuming** 状态停留时间异常长，或者资源池返回 **Active** 状态后 SQL 连接仍未恢复，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。