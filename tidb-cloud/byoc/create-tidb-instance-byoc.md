---
title: 创建一个 {{{ .byoc }}} 实例
summary: 了解如何创建一个 {{{ .byoc }}} 实例。
---

# 创建一个 {{{ .byoc }}} 实例

本文档介绍如何在 [TiDB Cloud console](https://tidbcloud.com/) 中创建一个 {{{ .byoc }}} 实例。

TiDB Cloud BYOC（Bring Your Own Cloud）将控制面保留在 TiDB Cloud 中，同时将数据面部署在你自己的云账户中。在创建 BYOC 实例之前，你的组织必须完成 BYOC onboarding，并准备好目标云环境。

在 TiDB Cloud BYOC 中，资源池为 BYOC 实例提供底层物理资源、网络和容量。在创建 BYOC 实例之前，你必须在目标云服务商和 Region 中拥有一个处于活动状态的资源池。

> **Note:**
>
> 如需了解如何创建 {{{ .premium }}} 实例，请参见 [创建一个 {{{ .premium }}} 实例](/tidb-cloud/premium/create-tidb-instance-premium.md)。

## 开始之前 {#before-you-begin}

如果你还没有 TiDB Cloud 账户，请点击[这里](https://tidbcloud.com/signup)注册账户。

在创建 BYOC 实例之前，请确保满足以下要求：

- 你拥有创建 TiDB Cloud 资源所需的组织或项目角色。
- 你的组织已完成目标云服务商和 Region 的 BYOC 前置配置，包括所需的云账户权限。对于 AWS，这包括 TiDB Cloud 在你的 AWS 账户中部署和管理 BYOC 资源所需的 IAM 角色。
- 在你希望部署 BYOC 实例的云服务商和 Region 中，已存在一个处于活动状态的资源池。

如果你的 BYOC 环境尚未准备就绪，**Create Resource** 页面中不会显示 **Bring Your Own Cloud** 页签。要为你的组织启用 BYOC，请联系你的 TiDB Cloud 账户团队或 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

如果没有可用的合适资源池，`Organization Owner` 可以通过 **BYOC Management** > **Resource Pools** 或在实例创建流程中创建资源池。其他角色无法创建资源池。更多信息，请参见 [创建资源池](/tidb-cloud/byoc/create-resource-pool-byoc.md)。

## 步骤 {#steps}

如果你拥有所需权限，可以按如下方式创建一个 {{{ .byoc }}} 实例：

1. 在 [TiDB Cloud console](https://tidbcloud.com/tidbs) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击右上角的 **Create Resource**。

2. 在 **Create Resource** 页面上，点击 **Bring Your Own Cloud** 页签。

3. 确认已选择 **BYOC** 作为你的套餐。

    BYOC 由 TiDB X 提供支持，专为大规模生产工作负载设计。它允许你在自己的云账户中运行数据面，同时使用 TiDB Cloud 实现自动化运维、弹性扩展和企业级安全性。

4. 在 **Basic Settings** 区域，为你的 {{{ .byoc }}} 实例输入名称，然后选择你希望托管实例的云服务商和 Region。

5. （可选）如需将此 {{{ .byoc }}} 实例归入某个项目以便管理，请为该实例选择目标项目。

6. 在 **Resource Pool** 区域，选择一个处于活动状态的资源池。

    仅显示与所选云服务商和 Region 匹配且状态为 **Active** 的资源池。如果没有可用的合适资源池，并且你是 `Organization Owner`，请点击 **Create Resource Pool** 创建一个资源池。资源池变为活动状态后，会自动为新实例选中该资源池。

    请确保选择具有足够 vCPU 容量的资源池。否则，可能会出现以下问题：

    - 如果所选资源池设置了 Pool vCPU Limit，且其当前已分配的 vCPU 大于或等于该限制，TiDB Cloud 会显示警告，并且你无法在该资源池中创建 {{{ .byoc }}} 实例。要继续操作，请前往该资源池的 **Resource Pool** 详情页面，提高或关闭 Pool vCPU Limit，或者选择其他资源池。
   - 即使当前已分配的 vCPU 低于 Pool vCPU Limit，创建新实例也可能导致总已分配 vCPU 超过该限制。这可能会限制资源扩展，并影响该资源池中所有实例的性能。如有必要，请提高或关闭 Pool vCPU Limit，或者选择其他资源池。

7. 在 **Capacity** 区域，为你的实例设置 Request Capacity Units (RCUs) 的最大数量。RCU 表示为你的工作负载预配的计算资源。TiDB Cloud 会根据需求在此范围内自动扩展你的实例。

8. 对于 {{{ .byoc }}} 实例，高可用模式继承自所选资源池。如果资源池使用区域级高可用，实例也使用区域级高可用；如果资源池使用可用区级高可用，实例也使用可用区级高可用。创建 BYOC 实例时，你无法配置高可用模式。更多信息，请参见 [TiDB Cloud BYOC 架构](/tidb-cloud/architecture-concepts.md#tidb-cloud-byoc)。

9. 点击 **Create**。

    实例创建过程随即开始。预配时间可能因你选择的 Region、容量和云服务商而异。

## 后续操作 {#what-s-next}

创建 BYOC 实例后，你可以执行以下操作：

- 如果尚未配置实例的 root 密码，请设置或重置该密码。
- 配置从你的应用环境到实例端点的网络访问。
- 从你的应用程序或 SQL 客户端连接到该实例。