---
title: 管理资源池
summary: 了解如何查看和管理 TiDB Cloud BYOC 的资源池。
---

# 管理资源池

资源池表示 TiDB Cloud BYOC 实例所使用的底层物理资源、网络和容量。你可以通过资源池管理来查看资源使用情况、管理容量、修改 AWS 资源标签，以及删除未使用的资源池。

资源池是组织级别的 BYOC 资源，不与项目关联。

## 所需角色 {#required-role}

只有具有 `Organization Owner` 角色的用户才能管理资源池。

其他角色可能对资源池具有只读访问权限，但不能创建、编辑、删除或修改资源池。

## 查看资源池 {#view-resource-pools}

如需查看资源池，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，点击左侧导航栏中的 **BYOC Management** > **Resource Pools**。

2. 在 **Resource Pools** 页面，查看资源池列表。

    列表会显示资源池名称、状态、云服务提供商、区域、实例数量和创建时间等信息。

3. 如需筛选资源池，请使用页面顶部的搜索框和筛选器。

4. 如需刷新列表，请点击刷新图标。

## 资源池状态 {#resource-pool-statuses}

资源池会显示以下状态：

- **Creating**：资源池正在置备中。你可以查看基本信息，但不能创建实例或进行配置更改。
- **Active**：资源池可用。可以执行正常的管理操作。
- **Modifying**：资源池正在修改中。你可以查看概览、指标、实例、标签和其他详细信息，但不能创建实例，也不能更改容量或 Pool vCPU Limit。

## 查看资源池详情 {#view-resource-pool-details}

如需查看资源池详情，请在 **Resource Pools** 页面点击资源池名称。

资源池详情页包含以下信息：

- **High Availability**：显示资源池使用的是单可用区高可用还是跨 Region 高可用。该值为只读。资源池创建后，你不能更改高可用模式或可用区部署方式。
- **Pool vCPU Usage**：显示当前已置备的 TiDB vCPU 和额外置备的 vCPU。
- **Instances in This Pool**：列出在此资源池中运行的 BYOC 实例。
- **Metrics**：显示 vCPU 使用量和物理存储使用量趋势。
- **Pool Capacity**：显示 TiKV 和 TiFlash 的容量信息。
- **AWS Resource Tags**：显示应用于此资源池中受支持资源的 AWS 标签。

## 查看指标 {#view-metrics}

资源池详情页中的 **Metrics** 区域提供以下图表：

- **vCPU Usage Trend**：显示该资源池已置备的 TiDB vCPU 使用趋势。图表还会显示当前 vCPU 值。
- **Physical Storage Usage Trend**：显示该资源池实际物理存储使用趋势。图表还会显示当前存储值。

你可以选择时间范围来查看历史指标。默认显示过去 30 天的指标。

如需刷新指标数据，请点击 **Refresh**。

如果指标数据尚不可用，图表会显示 **No Data Available Yet**。

## 修改 Pool vCPU Limit {#update-the-pool-vcpu-limit}

Pool vCPU Limit 是一个可选的用户自定义限制，用于限制资源池允许的最大已置备 TiDB vCPU 容量。额外置备的 vCPU（例如管理节点和可观测性节点）不计入此限制。

如需修改 Pool vCPU Limit，请执行以下步骤：

1. 进入资源池详情页。
2. 在 **Pool vCPU Usage** 区域，点击 **Update vCPU Limit**。
3. 在弹出的对话框中，开启或关闭 **Setup Limit**。

    - 如果你开启 **Setup Limit**，请输入新的 Pool vCPU Limit。
    - 如果你关闭 **Setup Limit**，则该资源池不再应用用户自定义的 vCPU 限制，计费仍基于实际使用量。

4. 确认修改。

设置新的 Pool vCPU Limit 时，该值必须大于或等于 `100` vCPU，并且大于或等于当前已置备的 TiDB vCPU。否则，修改会被拒绝。

> **Note:**
>
> 即使当前已置备的 vCPU 低于 Pool vCPU Limit，创建或恢复实例时也可能导致总已置备 vCPU 超过该限制。这可能会限制资源扩展，并降低资源池中所有实例的性能。在创建或恢复实例之前，请确保资源池具有足够的 vCPU 容量。

如果资源池当前已置备的 vCPU 大于或等于其 Pool vCPU Limit，则你不能在该资源池中创建或恢复实例。如需创建或恢复实例，请提高或关闭 Pool vCPU Limit，或选择其他资源池。

如果资源池处于 **Modifying** 状态，**Update vCPU Limit** 会被禁用。

## 修改容量 {#update-capacity}

你可以修改资源池的 TiKV 和 TiFlash 容量。

如需修改容量，请执行以下步骤：

1. 进入资源池详情页。
2. 在 **Pool Capacity** 区域，点击 **Update Capacity**。
3. 在 **Update _resource-pool-name_ Capacity** 对话框中，修改 TiKV 或 TiFlash 容量。
4. 如果已配置 Pool vCPU Limit，请查看容量评估。
5. 点击 **Save**。

如果已配置 Pool vCPU Limit，对话框会显示以下容量评估信息：

- **Current vCPU Usage**：资源池当前已置备的 TiDB vCPU 使用量。
- **Scaling vCPU Preview**：容量修改后预计的已置备 TiDB vCPU 使用量。
- **Max vCPU Limit**：当前的 Pool vCPU Limit。
- **Scale Evaluation**：在当前 Pool vCPU Limit 下是否允许此次容量修改。

如果未配置 Pool vCPU Limit，则不会显示容量评估信息。

适用以下规则：

- TiDB Cloud 控制台仅支持扩容操作。如果你有额外的节点或规格需求，或者需要缩容，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。
- TiKV 节点数量必须按每次增加三个进行调整。
- TiKV 存储只能增加。
- 资源池创建后，TiKV 机型不能更改。
- TiFlash 为可选项。如果未启用 TiFlash，则不会置备 TiFlash 节点。
- 你可以稍后根据工作负载需求启用 TiFlash。
- 你可以在 TiDB Cloud 控制台中禁用 TiFlash。禁用 TiFlash 会影响资源池中的所有 BYOC 实例。TiFlash 资源会被移除，依赖 TiFlash 的分析型工作负载可能不可用或出现性能下降。
- TiFlash 机型可以在线更改。
- TiFlash 存储只能增加。
- TiFlash 节点数量只能增加。
- 如果已配置 Pool vCPU Limit，**Scaling vCPU Preview** 不能超过 **Max vCPU Limit**。

如果资源池处于 **Modifying** 状态，**Update Capacity** 会被禁用。

## 管理 AWS 资源标签 {#manage-aws-resource-tags}

AWS 资源标签会应用到资源池中受支持的 AWS 资源。

如需管理 AWS 资源标签，请执行以下步骤：

1. 进入资源池详情页。
2. 在 **AWS Resource Tags** 区域，点击 **Edit Tags**。
3. 添加、编辑或删除标签。
4. 保存更改。

适用以下规则：

- 标签会应用到资源池内所有支持打标签的 AWS 资源。
- 标签键为必填项。
- 标签值为可选项。
- 标签键和值均大小写敏感。
- 标签键必须唯一，并按大小写敏感方式进行检查。
- 标签键长度必须为 1 到 128 个 UTF-8 字符。
- 标签值长度不得超过 256 个 UTF-8 字符。
- 用户定义的标签键不能以 `aws:` 开头。
- 系统保留的 AWS 标签不能被覆盖或编辑。
- 空行会被忽略且不会提交。
- 标签必须符合 AWS 的标签限制。

## 重命名资源池 {#rename-a-resource-pool}

如需重命名资源池，请执行以下步骤：

1. 进入资源池详情页或 **Resource Pools** 页面。
2. 点击 **...**。
3. 点击 **Rename**。
4. 输入新名称并确认更改。

重命名资源池只会更改其显示名称，不会修改底层云资源 ID。

## 删除资源池 {#delete-a-resource-pool}

只有当资源池中不包含任何 BYOC 实例时，你才能删除该资源池。

如需删除资源池，请执行以下步骤：

1. 进入 **Resource Pools** 页面。
2. 找到你要删除的资源池。
3. 点击 **...** > **Delete**。
4. 输入资源池名称以确认删除。

删除资源池不会删除历史实例备份。备份保留和回收站行为遵循现有的 BYOC 备份与恢复规则。

## 操作限制 {#operation-restrictions}

当资源池存在正在进行的修改操作时，TiDB Cloud 会实时或近实时刷新资源池数据。在此期间：

- 你可以查看资源池概览、指标、实例、标签和其他详细信息。
- 你不能创建实例。只有当资源池处于 **Active** 状态时，才能创建实例。
- 如果实例处于可删除状态，你可以删除该实例。
- 你不能修改 Pool vCPU Limit。
- 你不能修改容量。

当你提交操作时，后端会执行最终校验。如果资源池状态在操作期间发生变化，请求可能会被拒绝。