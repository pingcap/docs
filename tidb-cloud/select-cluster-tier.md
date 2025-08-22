---
title: 选择你的集群规格
summary: 了解如何在 TiDB Cloud 上选择你的集群规格。
aliases: ['/tidbcloud/developer-tier-cluster']
---

# 选择你的集群规格

集群规格决定了你的集群的吞吐量和性能。

TiDB Cloud 提供以下两种集群规格选项。在创建集群之前，你需要考虑哪种选项更适合你的需求。

- [TiDB Cloud Serverless](#tidb-cloud-serverless)
- [TiDB Cloud Dedicated](#tidb-cloud-dedicated)

## TiDB Cloud Serverless

<!--To be confirmed-->
TiDB Cloud Serverless 是一种全托管的多租户 TiDB 服务。它提供了一个即时、自动弹性扩缩的 MySQL 兼容数据库，并在超出免费额度后，采用按量计费模式，同时提供了丰富的免费额度。

### 集群方案

TiDB Cloud Serverless 提供两种服务方案，以满足不同用户的需求。无论你是刚刚开始使用，还是需要扩展以应对不断增长的应用需求，这些服务方案都能为你提供所需的灵活性和能力。

#### 免费集群方案

免费集群方案非常适合刚开始使用 TiDB Cloud Serverless 的用户。它为开发者和小型团队提供以下基本特性：

- **No cost**：该方案完全免费，无需信用卡即可开始使用。
- **Storage**：提供初始 5 GiB 的行存储和 5 GiB 的列存储。
- **Request Units**：包含 5000 万 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) 用于数据库操作。
- **Easy upgrade**：当你的需求增长时，可以平滑升级到 [scalable cluster plan](#scalable-cluster-plan)。

#### 可扩展集群方案

对于需要实时扩展以应对不断增长的工作负载的应用，可扩展集群方案提供了灵活性和性能，帮助你的业务持续增长，具备以下特性：

- **Enhanced capabilities**：包含免费集群方案的所有能力，并具备处理更大、更复杂工作负载的能力，以及高级安全特性。
- **Automatic scaling**：自动调整存储和计算资源，以高效应对变化的工作负载需求。
- **Predictable pricing**：虽然该方案需要信用卡，但你只需为实际使用的资源付费，确保扩展的性价比。

### 使用配额

在 TiDB Cloud 的每个组织中，默认最多可以创建 5 个 [免费集群](#free-cluster-plan)。如需创建更多 TiDB Cloud Serverless 集群，你需要添加信用卡并创建 [可扩展集群](#scalable-cluster-plan) 进行使用。

对于组织中的前 5 个 TiDB Cloud Serverless 集群（无论是免费还是可扩展），TiDB Cloud 为每个集群提供如下免费使用配额：

- 行存储：5 GiB
- 列存储：5 GiB
- Request Units (RUs)：每月 5000 万 RUs

Request Unit (RU) 是用于衡量单次数据库请求所消耗资源量的单位。每个请求消耗的 RU 数量取决于多种因素，例如操作类型或检索/修改的数据量。

一旦集群达到其使用配额，将立即拒绝任何新的连接尝试，直到你 [增加配额](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) 或在新月开始时重置使用量。已建立的连接在达到配额前会保持活跃，但会受到限流。例如，当免费集群的行存储超过 5 GiB 时，集群会自动限制任何新的连接尝试。

如需了解不同资源（包括读、写、SQL CPU 和网络出口）的 RU 消耗、定价详情及限流信息，请参见 [TiDB Cloud Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)。

### 用户名前缀

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

对于每个 TiDB Cloud Serverless 集群，TiDB Cloud 会生成一个唯一的前缀，以便与其他集群区分。

每当你使用或设置数据库用户名时，必须在用户名中包含该前缀。例如，假设你的集群前缀为 `3pTAoNNegb47Uc8`。

- 连接到你的集群：

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **Note:**
    >
    > TiDB Cloud Serverless 要求使用 TLS 连接。要查找你系统上的 CA 根证书路径，请参见 [Root certificate default path](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)。

- 创建数据库用户：

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

获取你的集群前缀，请按照以下步骤操作：

1. 进入 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 点击目标集群名称进入其概览页面，然后点击右上角的 **Connect**。此时会弹出连接对话框。
3. 在对话框中，从连接字符串中获取前缀。

### TiDB Cloud Serverless 特殊条款与条件

部分 TiDB Cloud 功能在 TiDB Cloud Serverless 上仅部分支持或不支持。详情请参见 [TiDB Cloud Serverless Limitations](/tidb-cloud/serverless-limitations.md)。

## TiDB Cloud Dedicated

TiDB Cloud Dedicated 适用于生产环境，具备跨可用区高可用性、水平扩展和 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 等优势。

对于 TiDB Cloud Dedicated 集群，你可以根据业务需求自定义 TiDB、TiKV 和 TiFlash 的集群规模。对于每个 TiKV 节点和 TiFlash 节点，节点上的数据会在不同可用区进行复制和分布，以实现 [高可用性](/tidb-cloud/high-availability-with-multi-az.md)。

要创建 TiDB Cloud Dedicated 集群，你需要 [添加支付方式](/tidb-cloud/tidb-cloud-billing.md#payment-method) 或 [申请 PoC（概念验证）试用](/tidb-cloud/tidb-cloud-poc.md)。

> **Note:**
>
> 集群创建后，节点存储空间无法减少。