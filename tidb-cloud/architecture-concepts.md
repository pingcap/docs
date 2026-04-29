---
title: 架构
summary: 了解 TiDB Cloud 的架构概念。
---

# 架构

<CustomContent language="en,zh">

TiDB Cloud 是一款全托管的数据库即服务（DBaaS），将 [TiDB](https://docs.pingcap.com/tidb/stable/overview) 的灵活性与强大功能带到 Amazon Web Services (AWS)、Google Cloud、Microsoft Azure 和阿里云。TiDB 是一款开源 HTAP（混合事务与分析处理）数据库。

</CustomContent>

<CustomContent language="ja">

TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) that brings the flexibility and power of [TiDB](https://docs.pingcap.com/tidb/stable/overview), an open-source HTAP (Hybrid Transactional and Analytical Processing) database, to Amazon Web Services (AWS), Google Cloud, and Microsoft Azure.

</CustomContent>

TiDB 兼容 MySQL，使得迁移和对接现有应用变得简单，同时具备无缝扩展性，能够应对从小型负载到大规模高性能系统的各种需求。它在一个系统中同时支持事务型（OLTP）和分析型（OLAP）负载，简化运维并实现实时洞察。

TiDB Cloud 让你轻松扩展数据库，处理复杂的管理任务，专注于开发可靠且高性能的应用。

<CustomContent language="en,zh">

- 对于 AWS，TiDB Cloud 提供 **TiDB Cloud Starter**，适用于自动扩展、成本高效的负载，**TiDB Cloud Essential**，适用于具备预配置容量的生产级负载，**TiDB Cloud Premium**，适用于需要高性能和增强安全性的关键业务负载，以及 **TiDB Cloud Dedicated**，适用于企业级应用，具备专属资源和高级功能。
- 对于 Google Cloud 和 Azure，TiDB Cloud 提供 **TiDB Cloud Dedicated**，适用于企业级应用，具备专属资源和高级功能。
- 对于阿里云，TiDB Cloud 提供 **TiDB Cloud Starter**，适用于自动扩展、成本高效的负载，**TiDB Cloud Essential**，适用于具备预配置容量的生产级负载，以及 **TiDB Cloud Premium**，适用于需要高性能和增强安全性的关键业务负载。

</CustomContent>

<CustomContent language="ja">

- For AWS, TiDB Cloud provides **TiDB Cloud Starter** for auto-scaling, cost-efficient workloads, **TiDB Cloud Essential** for production-ready workloads with provisioned capacity, **TiDB Cloud Premium** for mission-critical workloads that require high performance and enhanced security, and **TiDB Cloud Dedicated** for enterprise-grade applications with dedicated resources and advanced capabilities.
- For Google Cloud and Azure, TiDB Cloud provides **TiDB Cloud Dedicated** for enterprise-grade applications with dedicated resources and advanced capabilities.

</CustomContent>

## TiDB Cloud Starter

TiDB Cloud Starter 是一款全托管的多租户 TiDB 产品，提供即开即用、自动扩展的 MySQL 兼容数据库。

Starter 方案非常适合刚开始使用 TiDB Cloud 的用户。它为开发者和小型团队提供以下特性：

- **免费**：该方案完全免费，无需信用卡即可开始使用。
- **存储**：提供初始 5 GiB 的行存储和 5 GiB 的列存储。
- **Request Units**：包含 5000 万 [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) 用于数据库操作。

## TiDB Cloud Essential

对于负载持续增长、需要实时扩展的应用，Essential 方案提供灵活性和性能，助力你的业务增长，具备以下特性：

- **增强功能**：包含 Starter 方案的全部功能，并具备处理更大、更复杂负载的能力，以及高级安全特性。
- **自动扩展**：自动调整存储和计算资源，高效应对不断变化的负载需求。
- **高可用性**：内置容错和冗余机制，确保你的应用在基础设施故障时依然可用且具备弹性。
- **可预测的定价**：根据存储和计算资源的 Request Capacity Units (RCUs) 计费，提供透明、按用量计费的定价模式，随需扩展，按实际使用付费，无隐藏费用。

TiDB Cloud Essential 提供两种高可用性选项，以满足不同的运维需求。

- Zonal High Availability：将所有组件部署在同一可用区内，从而降低网络延时。
- Regional High Availability：将节点分布在多个可用区，提供最大的基础设施隔离和冗余。

更多信息，参见 [TiDB Cloud 的高可用性](/tidb-cloud/serverless-high-availability.md)。

## {{{ .premium }}}

对于需要在托管环境中获得高性能和增强安全性的关键业务应用，Premium 计划提供强大的基础设施和高级控制能力，具有以下特性：

- **无限增长和自动扩缩容**：提供无缝扩展能力以应对不断变化的工作负载，确保关键业务运行的持续可靠性。
- **性能优化**：针对高吞吐和低延迟工作负载进行调优，提供更高的资源上限和更细粒度的扩缩容控制。
- **按量付费**：根据实际的 [Request Capacity Unit (RCU)](/tidb-cloud/tidb-cloud-glossary.md#request-capacity-unit-rcu) 消耗量和存储使用量计费。这种灵活的模式无需手动对后端资源进行过度预配。
- **高级安全性**：提供更深入的安全配置和合规能力，以满足大型企业和受监管行业的要求。

为最大限度地提升关键业务工作负载的可用性和弹性，{{{ .premium }}} 提供[区域级高可用](/tidb-cloud/serverless-high-availability.md#regional-high-availability-architecture)，通过将节点分布在多个可用区中，提供比同区部署更高的冗余能力。

## TiDB Cloud Dedicated

TiDB Cloud Dedicated 专为关键业务设计，提供跨多个可用区的高可用性、水平扩展能力以及完整的 HTAP 功能。

该方案基于隔离的云资源（如 VPC、VM、托管 Kubernetes 服务和云存储）构建，充分利用主流云服务商的基础设施。TiDB Cloud Dedicated 集群支持完整的 TiDB 功能集，实现快速扩展、可靠备份、在指定 VPC 内部署以及地域级容灾。

![TiDB Cloud Dedicated 架构](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloud 控制台

[TiDB Cloud 控制台](https://tidbcloud.com/) 是 TiDB Cloud 资源的基于 Web 的管理界面。你可以通过该平台管理 TiDB Cloud 资源、导入或迁移数据、监控性能指标、配置备份、设置安全控制，并与其他云服务集成，所有操作均可在一个用户友好的平台上完成。

## TiDB Cloud CLI（Beta）

TiDB Cloud CLI，命令为 `ticloud`，允许你通过终端使用简单命令直接管理 TiDB Cloud Starter 和 Essential 实例。你可以执行如下任务：

- 创建、删除和列出 TiDB Cloud Starter 和 Essential 实例。
- 向 TiDB Cloud Starter 和 Essential 实例导入数据。
- 从 TiDB Cloud Starter 和 Essential 实例导出数据。

更多信息，参见 [TiDB Cloud CLI 参考](/tidb-cloud/cli-reference.md)。

## TiDB Cloud API（Beta）

TiDB Cloud API 是基于 REST 的接口，提供对 {{{ .starter }}}、{{{ .essential }}}、{{{ .premium }}} 和 TiDB Cloud Dedicated 资源的编程访问能力。它支持自动化、高效地处理项目、集群、备份、恢复、数据导入、计费以及 [TiDB Cloud Data Service](/tidb-cloud/data-service-overview.md) 中的其他资源管理任务。

更多信息，参见 [TiDB Cloud API 概览](https://docs.pingcap.com/api/tidb-cloud-api-overview)。

## 节点

节点是 TiDB 架构的核心组件。TiDB 节点、TiKV 节点和 TiFlash 节点协同工作，用于处理 SQL 查询、存储数据并加速分析型负载。

- 在 TiDB Cloud Dedicated 集群中，你可以根据性能需求完全管理专属 TiDB、TiKV 和 TiFlash 节点的数量和规格。更多信息，参见 [扩展性](/tidb-cloud/scalability-concepts.md)。
- 在 {{{ .starter }}}、{{{ .essential }}} 或 {{{ .premium }}} 实例中，TiDB、TiKV 和 TiFlash 节点的数量和规格由系统自动管理。这确保了无缝扩展，无需用户手动配置或管理节点。

### TiDB 节点

[TiDB 节点](/tidb-computing.md) 是无状态的 SQL 层，通过 MySQL 兼容端点与应用连接。它负责解析、优化 SQL 查询，并生成分布式执行计划。

你可以部署多个 TiDB 节点以实现水平扩展，处理更高负载。这些节点与负载均衡器（如 TiProxy 或 HAProxy）协同工作，提供无缝接口。TiDB 节点本身不存储数据——它们会将数据请求转发给 TiKV 节点（行存储）或 TiFlash 节点（列存储）。

### TiKV 节点

[TiKV 节点](/tikv-overview.md) 是 TiDB 架构中数据存储的核心，作为分布式事务型键值存储引擎，具备可靠性、扩展性和高可用性。

**主要特性：**

- **基于 Region 的数据存储**

    - 数据被划分为多个 [Region](https://docs.pingcap.com/tidb/dev/glossary#regionpeerraft-group)，每个 Region 覆盖特定的 Key Range（左闭右开区间：`StartKey` 到 `EndKey`）。
    - 每个 TiKV 节点内可包含多个 Region，以实现高效的数据分布。

- **事务支持**

    - TiKV 节点在键值层面原生支持分布式事务，默认隔离级别为 Snapshot Isolation。
    - TiDB 节点将 SQL 执行计划转换为对 TiKV 节点 API 的调用，实现无缝的 SQL 级事务支持。

- **高可用性**

    - TiKV 节点中的所有数据都会被复制（默认 3 副本），以保证持久性。
    - TiKV 原生支持高可用性和自动故障转移，防止节点故障带来的影响。

- **扩展性与可靠性**

    - TiKV 节点设计用于处理不断扩展的数据集，同时保持分布式一致性和容错能力。

### TiFlash 节点

[TiFlash 节点](/tiflash/tiflash-overview.md) 是 TiDB 架构中的一种专用存储节点。与普通 TiKV 节点不同，TiFlash 采用列存储模型，专为分析加速设计。

**主要特性：**

- **列存储**

    TiFlash 节点以列式格式存储数据，针对分析型查询进行了优化，大幅提升读密集型负载的性能。

- **向量检索索引支持**

    向量检索索引功能利用表的 TiFlash 副本，实现高级检索能力，并提升复杂分析场景下的效率。

<CustomContent plan="premium">

## {{{ .premium }}} 中的请求单位与容量 {#request-units-and-capacity-in-premium}

### Request Capacity Unit (RCU)

[Request Capacity Unit (RCU)](/tidb-cloud/tidb-cloud-glossary.md#request-capacity-unit-rcu) 是用于表示 {{{ .premium }}} 实例预配置计算容量的计量单位。一个 RCU 提供固定数量的计算资源，可每秒处理一定数量的 RU。你预配置的 RCU 数量决定了 {{{ .premium }}} 实例的基线性能和吞吐能力。

一个 RCU 表示每秒可持续提供的 RU 容量。例如，*X* 个 RCU 的基线可保证平均每秒 *X* 个 RU，按一分钟窗口（或实例配置的最小计算窗口）进行度量。

### RCU 自动扩缩容

配置 {{{ .premium }}} 实例时，你需要指定工作负载所需的最大 RCU 数量（`RCU_max`）。TiDB Cloud 会在 `0.25 * RCU_max` 到 `RCU_max` 的范围内自动扩缩容。

例如，如果你将最大容量设置为 20,000 RCU，TiDB Cloud 会根据实时需求在 5,000 到 20,000 RCU 之间动态调整容量。此扩缩容过程是自动且即时的，使你能够在任何时候消耗最多达到最大 RCU 数量的容量，而无需手动干预或等待。

### RCU 计费

{{{ .premium }}} 采用按量计费模式，根据实际的 Request Capacity Unit (RCU) 消耗量和存储使用量向你收费。

#### 按分钟计算

TiDB Cloud 每分钟计算一次你的使用量。它会统计 60 秒窗口内消耗的 Request Unit (RU) 总数，计算平均每秒 RU 数，并将该平均值作为该分钟的 RCU 消耗量。此计算方式可确保计费准确反映实时流量波动。

#### 最低使用量要求

为维持基线容量并确保实例始终有可用资源，TiDB Cloud 会根据你设置的最大 RCU 自动设定一个最低计费 RCU。该值定义了实例的基线保留容量。

如果某一分钟内的实际消耗低于该阈值，则按最低计费 RCU 计费。此机制可确保你的实例能够立即应对突发流量峰值，最高可达你指定的最大值，而不会出现性能下降或延迟。

### Request Unit (RU)

[Request Unit (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) 是用于表示单个数据库请求所消耗资源的计量单位。一个请求消耗的 RU 数量取决于操作类型以及读取或修改的数据量等因素。

{{{ .premium }}} 使用 Request Unit 对所有数据库操作的成本进行统一归一化，并基于吞吐量（每秒 Request Unit，RU/s）来衡量该成本。这个统一指标使你的吞吐成本更可预测，帮助你更有效地管理应用成本。

#### 基线性能示例

下表列出了常见操作的基线性能示例，帮助你估算工作负载。

| 操作类型 | 描述 | 预估成本 |
|----------------|------------------------------------------|----------------|
| 点读 | 通过唯一 ID 读取一个 1 KiB 的条目 | 1.5 RU |
| OLTP 写入 | 标准 Sysbench 模型（1 KiB 条目大小） | 2.5 RU |

> **注意：**
>
> 点读是通过唯一 ID 检索数据的最高效方式。对于写入操作，RU 成本会计入持久化数据所需的 I/O 和索引开销。RU 消耗会随着数据大小和操作复杂度按比例增长。

### Request Unit 注意事项

TiDB Cloud 会根据执行某项操作所需的数据库处理开销来计算该操作的总 RU 费用。计算时会考虑以下维度：

- **数据访问与大小**

    - **读写数据量**：RU 会随着数据负载大小直接增长。处理一条 100 KiB 的记录比处理一条 1 KiB 的记录消耗更多 RU。
    - **读写行数**：操作涉及的行数是主要成本驱动因素。即使数据负载较小，查询或更新多行也会增加总 RU 消耗，因为每一行都需要处理、加锁和校验。
    - **索引影响**：

        - **写入**：写操作期间，表上的每个受影响索引都必须更新。索引越多，`INSERT`、`UPDATE` 和 `DELETE` 操作的 RU 成本越高。
        - **读取**：设计良好的索引可显著降低查询 RU，因为它能让引擎高效定位行并避免全表扫描。

- **查询复杂度**

    - **扫描效率**：RU 消耗在很大程度上受引擎必须扫描的行数影响。

        - **读取指标（预估行数）**：使用主键或唯一索引的点读是最高效的操作。扫描数百万行的查询比使用优化索引的查询消耗更多 RU。

        - **写入指标（受影响行数）**：数据修改的 RU 成本与受影响的行数相关。在单条语句中修改 10,000 行的费用远高于修改单行。

    - **计算逻辑**：复杂 SQL 操作（包括多表连接、深层子查询和聚合）需要更多 CPU 周期来计算执行路径和处理数据。

</CustomContent>

## {{{ .premium }}} 中的请求单位和容量 {#request-units-and-capacity-in-premium}

### 请求容量单位（RCU）

[请求容量单位（RCU）](/tidb-cloud/tidb-cloud-glossary.md#request-capacity-unit-rcu) 是用于表示 {{{ .premium }}} 实例预配置计算容量的度量单位。一个 RCU 提供固定数量的计算资源，可用于每秒处理一定数量的 RU。你预配置的 RCU 数量决定了 {{{ .premium }}} 实例的基线性能和吞吐能力。

一个 RCU 表示每秒可持续提供的 RU 容量。例如，*X* 个 RCU 的基线表示平均可保证每秒 *X* 个 RU，按一分钟窗口（或为你的实例配置的最小计算窗口）进行衡量。

### RCU 自动扩缩容

配置 {{{ .premium }}} 实例时，你需要指定工作负载所需的最大 RCU 数量（`RCU_max`）。TiDB Cloud 会在 `0.25 * RCU_max` 到 `RCU_max` 的范围内自动扩缩容。

例如，如果你将最大容量设置为 20,000 RCU，TiDB Cloud 会根据实时需求在 5,000 到 20,000 RCU 之间动态调整容量。此扩缩容过程是自动且即时的，使你能够在任何时候消耗最多达到最大 RCU 数量的容量，而无需人工干预或等待。

### RCU 计费

{{{ .premium }}} 采用按使用量计费模式，根据实际请求容量单位（RCU）消耗量和存储使用量收费。

#### 按分钟计算

TiDB Cloud 每分钟计算一次你的使用量。它会统计 60 秒窗口内消耗的请求单位（RU）总数，计算平均每秒 RU 数，并将该平均值作为该分钟的 RCU 消耗量。此计算方式可确保你的账单准确反映实时流量波动。

#### 最低使用量要求

为了维持基线容量并确保实例资源始终可用，TiDB Cloud 会根据你设置的最大 RCU 自动设定一个最低计费 RCU。该值定义了实例的基线预留容量。

如果某一分钟内的实际消耗低于该阈值，则按最低计费 RCU 计费。该机制可确保你的实例能够立即处理最高达到你所指定最大值的突发流量，而不会出现性能下降或延迟。

### 请求单位（RU）

[请求单位（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) 是用于表示单个数据库请求所消耗资源的度量单位。一个请求消耗的 RU 数量取决于操作类型以及检索或修改的数据量等因素。

{{{ .premium }}} 使用请求单位对所有数据库操作的成本进行统一归一化，并基于吞吐量（每秒请求单位数，即 RU/s）来衡量该成本。这个统一指标使你的吞吐成本更可预测，从而帮助你更有效地管理应用成本。

#### 基线性能示例

下表列出了常见操作的基线性能示例，帮助你估算工作负载。

| 操作类型 | 描述 | 预估成本 |
|----------------|------------------------------------------|----------------|
| 点读 | 通过唯一 ID 读取一个 1 KiB 的项 | 1.5 RU |
| OLTP 写入 | 标准 Sysbench 模型（项大小为 1 KiB） | 2.5 RU |

> **注意：**
>
> 点读是通过唯一 ID 检索数据的最高效方式。对于写操作，RU 成本会计入持久化数据所需的 I/O 和索引开销。RU 消耗会随数据大小和操作复杂度按比例增长。

### 请求单元注意事项

TiDB Cloud 根据执行操作所需的数据库工作量来计算该操作的总 RU 费用。计算会考虑以下维度：

- **数据访问和大小**

    - **读写数据量**：RU 会随着数据负载大小直接线性增长。处理一条 100 KiB 的记录比处理一条 1 KiB 的记录消耗更多 RU。
    - **读写行数**：操作涉及的行数是主要成本驱动因素。即使数据负载较小，查询或更新多行也会增加 RU 总消耗，因为每一行都需要处理、加锁和校验。
    - **索引影响**：

        - **写入**：写操作期间，表上的每个受影响索引都必须更新。索引越多的表，在执行 `INSERT`、`UPDATE` 和 `DELETE` 操作时 RU 成本越高。
        - **读取**：设计良好的索引可以显著降低查询 RU，因为它能让引擎高效定位行并避免全表扫描。

- **查询复杂度**

    - **扫描效率**：RU 消耗在很大程度上受引擎必须扫描的行数影响。

        - **读取指标（估算行数）**：使用主键或唯一索引的点读是最高效的操作。扫描数百万行的查询比使用优化索引的查询消耗显著更多 RU。

        - **写入指标（受影响行数）**：数据修改的 RU 成本与受影响行数相关。在单条语句中修改 10,000 行会比修改单行产生高得多的费用。

    - **计算逻辑**：复杂 SQL 操作（包括多表连接、深层子查询和聚合）需要更多 CPU 周期来计算执行路径并处理数据。

</CustomContent>
