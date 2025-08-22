---
title: 选择你的集群方案
summary: 了解如何在 TiDB Cloud 上选择你的集群方案。
aliases: ['/tidbcloud/developer-tier-cluster']
---

# 选择你的集群方案

集群方案决定了你的集群的吞吐量和性能。

TiDB Cloud 提供以下几种集群方案选项。无论你是刚刚起步，还是需要扩展以满足不断增长的应用需求，这些服务方案都能为你提供所需的灵活性和能力。在创建集群之前，你需要考虑哪种选项更适合你的需求。

- [TiDB Cloud Serverless](#tidb-cloud-serverless)（现称 Starter）
- [Essential](#essential)
- [TiDB Cloud Dedicated](#tidb-cloud-dedicated)

> **Note:**
>
> 部分 TiDB Cloud 功能在 Starter 和 Essential 上仅部分支持或不支持。详情请参见 [Starter 和 Essential 限制](/tidb-cloud/serverless-limitations.md)。

## TiDB Cloud Serverless

TiDB Cloud Serverless（现称 Starter）是一款全托管的多租户 TiDB 服务。它提供了一个即时、自动弹性扩展的 MySQL 兼容数据库，并在超出免费额度后，按消耗计费。

免费集群方案非常适合刚开始使用 Starter 的用户。它为开发者和小型团队提供以下基本功能：

- **No cost**：该方案完全免费，无需信用卡即可开始使用。
- **Storage**：提供初始 5 GiB 的行存储和 5 GiB 的列存储。
- **Request Units**：包含 5000 万 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) 用于数据库操作。

### 使用额度

对于 TiDB Cloud 中的每个组织，默认最多可以创建 5 个免费的 Starter 集群。要创建更多 Starter 集群，你需要添加信用卡并设置消费上限。

对于组织中的前 5 个 Starter 集群，无论是免费还是可扩展，TiDB Cloud 都为每个集群提供如下免费使用额度：

- 行存储：5 GiB
- 列存储：5 GiB
- Request Units (RUs)：每月 5000 万 RU

Request Unit (RU) 是用于表示单次数据库请求所消耗资源量的计量单位。单个请求消耗的 RU 数量取决于多种因素，例如操作类型或检索/修改的数据量。

一旦集群达到其使用额度，将立即拒绝任何新的连接尝试，直到你 [增加额度](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) 或在新月开始时重置使用量。已建立的连接在达到额度前会保持活跃，但会受到限流。例如，当免费集群的行存储超过 5 GiB 时，集群会自动限制任何新的连接尝试。

如需了解不同资源（包括读、写、SQL CPU 和网络出口）的 RU 消耗、定价详情及限流信息，请参见 [Starter 价格详情](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)。

## Essential {#essential}

对于面临不断增长的工作负载并需要实时扩展的应用，Essential 集群方案提供了灵活性和性能，助力你的业务增长，具备以下特性：

- **Enhanced capabilities**：包含 Starter 方案的所有功能，并具备处理更大、更复杂工作负载的能力，以及高级安全特性。
- **Automatic scaling**：自动调整存储和计算资源，高效应对变化的工作负载需求。
- **High availability**：内置容错和冗余机制，即使在基础设施故障时，也能确保你的应用高可用和具备弹性。
- **Predictable pricing**：基于存储和计算资源的 Request Capacity Units (RCUs) 计费，提供透明、按用量计费的定价方式，随需扩展，让你只为实际使用的资源付费，无额外意外支出。

## User name prefix

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

对于每个 Starter 或 Essential 集群，TiDB Cloud 会生成一个唯一的前缀，以便与其他集群区分。

每当你使用或设置数据库用户名时，必须在用户名中包含该前缀。例如，假设你的集群前缀为 `3pTAoNNegb47Uc8`。

- 连接到你的集群：

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **Note:**
    >
    > Starter 和 Essential 需要使用 TLS 连接。要查找你系统上的 CA 根证书路径，请参见 [Root certificate default path](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)。

- 创建数据库用户：

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

获取你的集群前缀，请按照以下步骤操作：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 点击目标集群名称进入其概览页面，然后点击右上角的 **Connect**。此时会弹出连接对话框。
3. 在对话框中，从连接字符串中获取前缀。

## TiDB Cloud Dedicated

TiDB Cloud Dedicated 适用于生产环境，具备跨可用区高可用性、水平扩展能力和 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 优势。

对于 TiDB Cloud Dedicated 集群，你可以根据业务需求灵活定制 TiDB、TiKV 和 TiFlash 的集群规模。对于每个 TiKV 节点和 TiFlash 节点，节点上的数据会在不同可用区进行复制和分布，以实现 [高可用性](/tidb-cloud/high-availability-with-multi-az.md)。

要创建 TiDB Cloud Dedicated 集群，你需要 [添加支付方式](/tidb-cloud/tidb-cloud-billing.md#payment-method) 或 [申请 PoC（概念验证）试用](/tidb-cloud/tidb-cloud-poc.md)。

> **Note:**
>
> 集群创建后，不能减少节点存储空间。