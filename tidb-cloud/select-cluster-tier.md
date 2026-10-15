---
title: 选择方案
summary: 了解如何在 TiDB Cloud 上选择方案。
aliases: ['/tidbcloud/developer-tier-cluster']
---

# 选择方案

方案决定了你的 TiDB 资源的吞吐量和性能。

TiDB Cloud 提供了以下几种方案选项。无论你是刚刚开始使用，还是需要扩展以满足不断增长的应用需求，这些服务方案都能为你提供所需的灵活性和能力。在创建 TiDB 资源之前，你需要考虑哪种选项更适合你的需求。

- [{{{ .starter }}}](#starter)
- [{{{ .essential }}}](#essential)
- [{{{ .premium }}}](#premium)
- [{{{ .byoc }}}](#byoc)
- [{{{ .dedicated }}}](#tidb-cloud-dedicated)
- [{{{ .lake }}}](#lake)

> **注意：**
>
> 部分 TiDB Cloud 功能在 TiDB Cloud Starter 和 TiDB Cloud Essential 上仅部分支持或不支持。详情请参见 [TiDB Cloud Starter 和 Essential 限制](/tidb-cloud/serverless-limitations.md)。

## {{{ .starter }}} {#starter}

TiDB Cloud Starter 是一款全托管的多租户数据库产品，为开发者和小型团队提供即开即用、自动扩缩容的数据库实例。

TiDB Cloud Starter 支持以下兼容模式：

- **兼容 MySQL**：提供 MySQL 协议兼容性。每个符合条件的实例都包含每月免费额度；超出免费额度后，你可以启用按量计费以继续使用该实例。

- **兼容 PostgreSQL（公测）**：提供 PostgreSQL wire 协议兼容性。兼容 PostgreSQL 的 Starter 实例在公测期间当前免费。

免费方案非常适合刚开始使用 {{{ .starter }}} 的开发者和小型团队。每种兼容模式都包含每月免费的存储和 Request Units (RUs) 配额。具体配额因兼容模式而异。

- **免费**：该方案在使用量不超过[免费额度](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)时免费。无需信用卡即可开始使用。

- **存储**：包含每月免费存储配额。
- **Request Units**：包含用于数据库操作的 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)。

### MySQL-compatible Starter {#usage-quota}

对于 TiDB Cloud 中的每个组织，默认情况下，你最多可以创建五个免费的 MySQL-compatible {{{ .starter }}} 实例。要创建更多 {{{ .starter }}} 实例，你需要添加信用卡并指定支出上限。

对于你组织中的前五个 MySQL-compatible {{{ .starter }}} 实例，无论它们是免费版还是可扩缩版，TiDB Cloud 都会为其中的每个实例提供如下免费使用配额：

- 基于行的存储：5 GiB
- 列式存储：5 GiB
- Request Units (RUs)：每月 5000 万 RUs

Request Unit (RU) 是一个计量单位，用于表示向数据库发起单个请求所消耗的资源量。一个请求消耗的 RU 数量取决于多种因素，例如操作类型，或者读取或修改的数据量。

一旦某个 {{{ .starter }}} 实例达到其使用配额，它会立即拒绝任何新的连接尝试，直到你[提高配额](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)或在新月份开始时使用量被重置。在达到配额之前已建立的现有连接将保持活动状态，但会受到限流影响。例如，当某个免费的 {{{ .starter }}} 实例的基于行的存储超过 5 GiB 时，该实例会自动限制任何新的连接尝试。

要了解不同资源（包括读、写、SQL CPU 和网络出口流量）的 RU 消耗、定价详情以及限流信息，请参见 [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)。

### PostgreSQL-compatible Starter {#postgresql-compatible-starter}

> **Note:**
>
> PostgreSQL-compatible TiDB Cloud Starter 当前处于公测阶段。

在公测期间，PostgreSQL-compatible {{{ .starter }}} 实例当前免费。

对于你组织中的前 10 个 PostgreSQL-compatible {{{ .starter }}} 实例，TiDB Cloud 为每个实例提供以下每月免费配额：

- 基于行的存储：50 GiB

- Request Units (RUs)：每月 5 亿 RUs

当 PostgreSQL-compatible {{{ .starter }}} 实例达到其免费配额时，超出的资源消耗可能会受到使用限制或服务暂停。如果你预计会超出这些额度，请联系 <a href="mailto:support@pingcap.com">support@pingcap.com</a> 讨论你的需求。

### Instance Capacity Plan

以下实例容量限制适用于兼容 MySQL 的 {{{ .starter }}} 实例。

默认情况下，TiDB Cloud 中的每个组织在所有 TiDB Cloud Starter 和 Essential 实例中总共最多可以创建五个 [branch](/tidb-cloud/branch-overview.md)。

TiDB Cloud 中的每个付费组织总共最多可以创建 100 个 TiDB Cloud Starter 实例和 branch，其中每个 branch 都算作一个单独的实例。

对于构建 agent 平台或其他需要大量实例和 branch 的服务的付费组织，TiDB Cloud 提供 **Instance Capacity Plan**。通过此方案，每个付费 TiDB Cloud 组织可以创建超过五个 branch，并且不受 100 个 TiDB Cloud Starter 实例和 branch 限制。要了解更多信息并申请 Instance Capacity Plan，请填写[申请表](https://www.pingcap.com/programs/agentic-ai-instance-capacity)。

当你的 TiDB Cloud Instance Capacity Plan 申请获批后，你将收到一封电子邮件通知。

## TiDB Cloud Essential {#essential}

对于需要实时扩展以应对不断增长的工作负载的应用，Essential 方案提供了灵活性和性能，助力你的业务增长，主要特性包括：

- **增强能力**：包含 Starter 方案的所有功能，并具备处理更大、更复杂工作负载的能力，以及高级安全特性。
- **自动扩展**：自动调整存储和计算资源，高效应对变化的工作负载需求。
- **高可用性**：内置容错和冗余机制，确保你的应用即使在基础设施故障时也能保持可用和弹性。
- **可预测的定价**：根据存储和计算资源的 Request Capacity Units (RCUs) 计费，提供透明、按用量计费的定价模式，随用随付，无额外费用。

## User name prefix

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

对于每个 TiDB Cloud Starter 或 TiDB Cloud Essential 实例，TiDB Cloud 会生成一个唯一的前缀，以区分不同的实例。

每当你使用或设置数据库用户名时，必须在用户名中包含该前缀。例如，假设你的 TiDB Cloud Starter 或 TiDB Cloud Essential 实例前缀为 `3pTAoNNegb47Uc8`。

- 连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 实例：

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **注意：**
    >
    > TiDB Cloud Starter 和 TiDB Cloud Essential 要求使用 TLS 连接。要查找你系统上的 CA 根证书路径，请参见 [Root certificate default path](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)。

- 创建数据库用户：

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

获取你的 TiDB Cloud Starter 或 TiDB Cloud Essential 实例前缀，请按照以下步骤操作：

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。
2. 点击目标 TiDB Cloud Starter 或 Essential 实例名称进入其概览页面，然后点击右上角的 **Connect**。此时会弹出连接对话框。
3. 在对话框中，从连接字符串中获取前缀。

## {{{ .premium }}} {#premium}

对于需要大规模容量和持续高性能的关键企业工作负载，Premium 方案提供云原生体验，并具有以下特性：

- **即时弹性**：自动扩展计算资源，以吸收突发流量高峰，并在需求高峰期间保持稳定性能。
- **无限扩展性**：扩展存储和吞吐量，以跟上业务增长，而不受物理基础设施限制。
- **零基础设施管理**：提供全托管服务，无需手动扩缩容、打补丁和进行容量规划。
- **可预测的定价**：基于存储和 Request Capacity Units (RCUs) 计费，提供透明的按使用量计费模式，可随你的需求扩展，因此你只需为实际使用量付费，不会有意外费用。
- **高级安全性与合规性**：支持高级加密、客户管理的加密密钥 (CMEK)、私有网络和合规认证，以保护敏感数据。

## {{{ .byoc }}} {#byoc}

{{{ .byoc }}} 专为需要更强数据位置控制、云资源控制、网络边界控制以及合规态势控制的企业级工作负载而设计。使用 {{{ .byoc }}} 时，TiDB Cloud 控制平面由 PingCAP 管理，而数据平面运行在你自己的云账户中。

{{{ .byoc }}} 提供托管式 TiDB Cloud 体验，并具有以下特性：

- **Data plane 部署在客户自己的账户中**：将 TiDB 服务资源、存储、网络和数据保留在你的云账户中。
- **托管运维**：使用 TiDB Cloud 进行部署、扩缩容、监控、升级、备份与恢复以及生命周期管理。
- **灵活的高可用性**：同时支持 Single-AZ 和 Multi-AZ 部署，使你能够在更低延时的单可用区部署与跨多个可用区的更高韧性部署之间进行选择。
- **云账户级安全控制**：允许你将自己的云策略、网络控制、审计日志记录和合规控制应用到 BYOC 数据平面。
- **私有网络连接**：根据你的 BYOC 配置，支持 VPC peering 等私有网络访问模式。

## TiDB Cloud Dedicated

TiDB Cloud Dedicated 适用于生产环境，具备跨可用区高可用性、水平扩展能力和 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 优势。

对于 TiDB Cloud Dedicated 集群，你可以根据业务需求灵活定制 TiDB、TiKV 和 TiFlash 的集群规模。对于每个 TiKV 节点和 TiFlash 节点，节点上的数据会在不同可用区进行复制和分布，以实现 [高可用性](/tidb-cloud/high-availability-with-multi-az.md)。

要创建 TiDB Cloud Dedicated 集群，你需要 [添加支付方式](/tidb-cloud/tidb-cloud-billing.md#payment-method) 或 [申请 PoC（概念验证）试用](/tidb-cloud/tidb-cloud-poc.md)。

> **注意：**
>
> TiDB Cloud Dedicated 集群创建后，节点存储空间无法减少。

## {{{ .lake }}} {#lake}

[TiDB Cloud Lake](https://docs.pingcap.com/tidbcloudlake/) 是一项面向分析工作负载的云原生数据仓库服务。它将计算与存储分离，使你能够独立配置 warehouse，随工作负载变化进行扩展，并以经济高效的方式将数据存储在对象存储中。

TiDB Cloud Lake 在一个平台中支持 ANSI SQL、半结构化数据处理、向量搜索和面向 AI 的工作流。它专为希望获得托管式分析体验而无需自行运维底层基础设施的团队而设计。

参见 [TiDB Cloud Lake Overview](https://docs.pingcap.com/tidbcloudlake/lake-overview/) 和 [TiDB Cloud Lake Quick Start](https://docs.pingcap.com/tidbcloudlake/lake-quick-start/)。
