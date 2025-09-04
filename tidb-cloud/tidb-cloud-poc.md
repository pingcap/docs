---
title: 使用 TiDB Cloud 进行概念验证（PoC）
summary: 了解如何使用 TiDB Cloud 进行概念验证（PoC）。
---

# 使用 TiDB Cloud 进行概念验证（PoC）

TiDB Cloud 是一款数据库即服务（DBaaS）产品，将 TiDB 的所有优势以全托管云数据库的形式交付。它帮助你专注于应用程序开发，而无需关注数据库的复杂性。<CustomContent language="en,zh">TiDB Cloud 目前可在 Amazon Web Services (AWS)、Google Cloud、Microsoft Azure 和阿里云上使用。</CustomContent><CustomContent language="ja">TiDB Cloud is currently available on Amazon Web Services (AWS), Google Cloud, and Microsoft Azure.</CustomContent>

发起概念验证（PoC）是判断 TiDB Cloud 是否适合你业务需求的最佳方式。通过 PoC，你还可以在短时间内熟悉 TiDB Cloud 的关键特性。通过运行性能测试，你可以评估你的业务负载是否能高效运行在 TiDB Cloud 上，同时也能评估数据迁移和配置适配所需的工作量。

本文档介绍了典型的 PoC 流程，旨在帮助你快速完成 TiDB Cloud 的 PoC。这是经过 TiDB 专家和大量客户验证的最佳实践。

如果你有意进行 PoC，欢迎在开始前联系 <a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>。支持团队可以帮助你制定测试计划，并顺利引导你完成 PoC 流程。

你也可以[创建 TiDB Cloud Starter](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster) 快速体验 TiDB Cloud 进行初步评估。请注意，TiDB Cloud Starter 有一些[特殊条款和条件](/tidb-cloud/serverless-limitations.md)。

## PoC 流程概览

PoC 的目的是测试 TiDB Cloud 是否满足你的业务需求。一个典型的 PoC 通常持续 14 天，在此期间你需要专注于完成 PoC。

一个典型的 TiDB Cloud PoC 包含以下步骤：

1. 定义成功标准并制定测试计划
2. 明确你的业务负载特性
3. 注册并为 PoC 创建 TiDB Cloud Dedicated 集群
4. 适配你的数据库结构和 SQL
5. 导入数据
6. 运行业务负载并评估结果
7. 探索更多功能
8. 清理环境并完成 PoC

## 第 1 步：定义成功标准并制定测试计划

在通过 PoC 评估 TiDB Cloud 时，建议根据你的业务需求确定关注点及相应的技术评估标准，并明确你对 PoC 的期望和目标。清晰且可量化的技术标准配合详细的测试计划，可以帮助你聚焦关键点，覆盖业务层面的需求，并最终通过 PoC 流程获得答案。

你可以通过以下问题来帮助确定 PoC 的目标：

- 你的业务负载场景是什么？
- 你的业务数据集规模或负载是多少？增长速度如何？
- 性能需求是什么，包括关键业务的吞吐量或延迟要求？
- 可用性和稳定性需求是什么，包括可接受的计划内或计划外停机时间的最小值？
- 运营效率需要关注哪些指标？你如何衡量这些指标？
- 你的业务负载有哪些安全和合规性要求？

如需了解更多关于成功标准和如何制定测试计划的信息，欢迎联系 <a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>。

## 第 2 步：明确你的业务负载特性

TiDB Cloud 适用于需要高可用性、强一致性和大数据量的多种场景。[TiDB 简介](https://docs.pingcap.com/tidb/stable/overview) 列出了关键特性和应用场景。你可以检查这些特性是否适用于你的业务场景：

- 水平扩展和缩容
- 金融级高可用性
- 实时 HTAP
- 兼容 MySQL 协议和 MySQL 生态

你可能还会对 [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) 感兴趣，它是一款加速分析型处理的列存储引擎。在 PoC 过程中，你可以随时使用 TiFlash 功能。

## 第 3 步：注册并为 PoC 创建 TiDB Cloud Dedicated 集群

要为 PoC 创建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，请按照以下步骤操作：

1. 通过以下任一方式填写 PoC 申请表：

    - 在 PingCAP 官网，访问 [申请 PoC](https://pingcap.com/apply-for-poc/) 页面填写申请表。
    - 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，点击右下角的 **?**，选择 **Contact Sales**，然后选择 **Apply for PoC** 填写申请表。

    提交表单后，TiDB Cloud 支持团队会审核你的申请，与你联系，并在申请通过后将额度发放到你的账户。你也可以联系 PingCAP 支持工程师协助你的 PoC 流程，确保 PoC 顺利进行。

2. 参考 [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md) 为 PoC 创建 TiDB Cloud Dedicated 集群。

   > **Note:**
   >
   > 在创建 TiDB Cloud Dedicated 集群前，你必须添加以下任一付款方式：
   >  - 按照集群创建页面的指引添加信用卡。
   >  - 联系 TiDB Cloud 支持团队通过电汇付款。
   >  - 通过云市场（AWS、Azure 或 Google Cloud）注册 TiDB Cloud，使用云服务商账户付款。
   >
   > 你的 PoC 额度会自动用于抵扣 PoC 期间产生的合规费用。

在创建集群前，建议进行容量规划以确定集群规模。你可以根据预估的 TiDB、TiKV 或 TiFlash 节点数量起步，后续根据性能需求进行扩容。你可以参考以下文档或咨询我们的支持团队获取更多细节。

- 有关容量预估的最佳实践，参见 [Size Your TiDB](/tidb-cloud/size-your-cluster.md)。
- 有关 TiDB Cloud Dedicated 集群的配置，参见 [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。分别为 TiDB、TiKV 和 TiFlash（可选）配置集群规模。
- 有关如何有效规划和优化 PoC 额度消耗，参见本文档的 [FAQ](#faq)。
- 有关扩容的更多信息，参见 [扩容 TiDB 集群](/tidb-cloud/scale-tidb-cluster.md)。

当专用 PoC 集群创建完成后，你就可以加载数据并进行一系列测试。关于如何连接 TiDB 集群，参见 [连接 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-to-tidb-cluster.md)。

对于新创建的集群，请注意以下配置：

- 默认时区（Dashboard 上的 **Create Time** 列）为 UTC。你可以按照 [设置本地时区](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization) 将其更改为本地时区。
- 新集群的默认备份设置为每日全库备份。你可以指定首选备份时间或手动备份数据。关于默认备份时间及更多细节，参见 [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

## 第 4 步：适配你的数据库结构和 SQL

接下来，你可以将数据库结构（包括表和索引）加载到 TiDB 集群。

由于 PoC 额度有限，为了最大化额度价值，建议你创建一个 [TiDB Cloud Starter 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 用于兼容性测试和初步分析。

TiDB Cloud 高度兼容 MySQL 8.0。如果你的数据源兼容 MySQL 或可以适配为兼容 MySQL，可以直接导入数据到 TiDB。

关于兼容性，参见以下文档：

- [TiDB 与 MySQL 的兼容性](https://docs.pingcap.com/tidb/stable/mysql-compatibility)。
- [TiDB 与 MySQL 不同的特性](https://docs.pingcap.com/tidb/stable/mysql-compatibility#features-that-are-different-from-mysql)。
- [TiDB 的关键字和保留字](https://docs.pingcap.com/tidb/stable/keywords)。
- [TiDB 限制](https://docs.pingcap.com/tidb/stable/tidb-limitations)。

以下是一些最佳实践：

- 检查数据库结构设计是否存在低效之处。
- 移除不必要的索引。
- 规划分区策略，实现有效分区。
- 避免由于右侧索引增长（如时间戳索引）导致的[热点问题](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)。
- 通过使用 [SHARD_ROW_ID_BITS](https://docs.pingcap.com/tidb/stable/shard-row-id-bits) 和 [AUTO_RANDOM](https://docs.pingcap.com/tidb/stable/auto-random) 避免[热点问题](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)。

对于 SQL 语句，你可能需要根据数据源与 TiDB 的兼容性程度进行适配。

如有疑问，请联系 [PingCAP](/tidb-cloud/tidb-cloud-support.md) 咨询。

## 第 5 步：导入数据

你可以导入小数据集以快速测试可行性，也可以导入大数据集以测试 TiDB 数据迁移工具的吞吐能力。虽然 TiDB 提供了示例数据，但强烈建议你使用真实业务负载进行测试。

你可以将多种格式的数据导入 TiDB Cloud：

- [使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
- [导入本地文件到 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)
- [导入 SQL 文件格式的示例数据](/tidb-cloud/import-sample-data.md)
- [从云存储导入 CSV 文件](/tidb-cloud/import-csv-files.md)
- [导入 Apache Parquet 文件](/tidb-cloud/import-parquet-files.md)

> **Note:**
>
> 在 **Import** 页面导入数据不会产生额外的计费费用。

## 第 6 步：运行业务负载并评估结果

现在你已经创建了环境、适配了数据库结构并导入了数据，是时候测试你的业务负载了。

在测试业务负载前，建议先手动备份一次，这样在需要时可以将数据库恢复到初始状态。更多信息参见 [备份与恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

启动业务负载后，你可以通过以下方式观察系统：

- 集群常用指标可在集群概览页面查看，包括 Total QPS、Latency、Connections、TiFlash Request QPS、TiFlash Request Duration、TiFlash Storage Size、TiKV Storage Size、TiDB CPU、TiKV CPU、TiKV IO Read 和 TiKV IO Write。参见 [监控 TiDB 集群](/tidb-cloud/monitor-tidb-cluster.md)。
- 进入集群的 [**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) 页面，查看 **SQL Statement** 标签页，可以观察 SQL 执行情况，无需查询系统表即可定位性能问题。参见 [SQL 语句分析](/tidb-cloud/tune-performance.md#statement-analysis)。
- 进入集群的 [**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) 页面，查看 **Key Visualizer** 标签页，可以查看 TiDB 的数据访问模式和数据热点。参见 [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer)。
- 你还可以将这些指标集成到自己的 Datadog 和 Prometheus。参见 [第三方监控集成](/tidb-cloud/third-party-monitoring-integrations.md)。

现在可以评估测试结果了。

为了获得更准确的评估，建议在测试前确定指标基线，并为每次测试妥善记录结果。通过分析结果，你可以判断 TiDB Cloud 是否适合你的应用。同时，这些结果也反映了系统的运行状态，你可以根据指标调整系统。例如：

- 评估系统性能是否满足需求。检查总 QPS 和延迟。如果系统性能不理想，可以通过以下方式进行调优：

    - 监控并优化网络延迟。
    - 排查并优化 SQL 性能。
    - 监控并[解决热点问题](https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#troubleshoot-hotspot-issues)。

- 评估存储容量和 CPU 使用率，并据此扩容或缩容 TiDB 集群。扩容细节参见 [FAQ](#faq) 部分。

以下是性能调优建议：

- 提高写入性能

    - 通过扩容 TiDB 集群提升写入吞吐量（参见 [扩容 TiDB 集群](/tidb-cloud/scale-tidb-cluster.md)）。
    - 通过使用 [乐观事务模型](https://docs.pingcap.com/tidb/stable/optimistic-transaction#tidb-optimistic-transaction-model) 减少锁冲突。

- 提高查询性能

    - 在 [**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) 页的 [**SQL Statement**](/tidb-cloud/tune-performance.md#statement-analysis) 标签查看 SQL 执行计划。
    - 在 [**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) 页的 [**Key Visualizer**](/tidb-cloud/tune-performance.md#key-visualizer) 标签查看热点问题。
    - 在 [**Metrics**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page) 页面监控 TiDB 集群是否容量不足。
    - 使用 TiFlash 功能优化分析型处理。参见 [使用 HTAP 集群](/tiflash/tiflash-overview.md)。

## 第 7 步：探索更多功能

现在业务负载测试已完成，你可以探索更多功能，例如升级和备份。

- 升级

    TiDB Cloud 会定期升级 TiDB 集群，你也可以提交工单请求集群升级。参见 [升级 TiDB 集群](/tidb-cloud/upgrade-tidb-cluster.md)。

- 备份

    为避免厂商锁定，你可以使用每日全量备份将数据迁移到新集群，并使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 导出数据。更多信息参见 [备份与恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup) 及 [备份与恢复 TiDB Cloud Starter 或 Essential 数据](/tidb-cloud/backup-and-restore-serverless.md)。

## 第 8 步：清理环境并完成 PoC

当你使用真实业务负载测试 TiDB Cloud 并获得测试结果后，PoC 的完整流程就已完成。这些结果可以帮助你判断 TiDB Cloud 是否符合你的预期。同时，你也积累了 TiDB Cloud 的最佳实践。

如果你希望在更大规模上体验 TiDB Cloud，进行新一轮部署和测试（如使用 TiDB Cloud 提供的其他节点存储规格），可以通过创建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群获得完整访问权限。

如果你的额度即将用尽且希望继续 PoC，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 咨询。

你可以随时结束 PoC 并移除测试环境。更多信息参见 [删除 TiDB 集群](/tidb-cloud/delete-tidb-cluster.md)。

欢迎通过填写 [TiDB Cloud 反馈表](https://www.surveymonkey.com/r/L3VVW8R) 向我们的支持团队反馈 PoC 流程、功能需求及产品改进建议。

## FAQ

### 1. 备份和恢复数据需要多长时间？

TiDB Cloud 提供两种数据库备份方式：自动备份和手动备份。两种方式均为全库备份。

备份和恢复所需时间会因表数量、镜像副本数量和 CPU 密集程度而异。单个 TiKV 节点的备份和恢复速率约为 50 MB/s。

数据库备份和恢复操作通常是 CPU 密集型的，并且总是需要额外的 CPU 资源。根据环境的 CPU 密集程度，可能会对 QPS 和事务延迟产生 10% 到 50% 的影响。

### 2. 什么时候需要扩容和缩容？

关于扩容和缩容，有以下几点建议：

- 在高峰时段或数据导入期间，如果你观察到 Dashboard 上的容量指标已达到上限（参见 [监控 TiDB 集群](/tidb-cloud/monitor-tidb-cluster.md)），你可能需要扩容集群。
- 如果你观察到资源使用率持续较低，例如 CPU 使用率仅为 10%-20%，可以缩容集群以节省资源。

你可以在控制台自行扩容集群。如果需要缩容集群，则需要联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 协助。关于扩容的更多信息，参见 [扩容 TiDB 集群](/tidb-cloud/scale-tidb-cluster.md)。你可以与支持团队保持联系，跟踪具体进度。扩容操作完成前请勿开始测试，因为数据重平衡会影响性能。

### 3. 如何最大化利用 PoC 额度？

PoC 申请通过后，你的账户会获得额度。一般来说，这些额度足以支持 14 天的 PoC。额度按节点类型和节点数量按小时计费。更多信息参见 [TiDB Cloud 计费](/tidb-cloud/tidb-cloud-billing.md#credits)。

要查看 PoC 的总额度、可用额度和当前额度使用情况，请在 TiDB Cloud 控制台左上角通过下拉框切换到目标组织，点击左侧导航栏的 **Billing**，然后点击 **Credits** 标签页。

为节省额度，请移除不再使用的集群。目前无法停止集群。你需要确保备份已更新后再移除集群，这样在需要恢复 PoC 时可以还原集群。

如果 PoC 结束后仍有未用完的额度，只要额度未过期，你可以继续用这些额度支付 TiDB 集群费用。

### 4. PoC 可以超过 2 周吗？

如果你希望延长 PoC 试用期或额度即将用尽，请[联系 PingCAP](https://www.pingcap.com/contact-us/) 获取帮助。

### 5. 如果遇到技术问题，如何获得 PoC 支持？

你可以随时[联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 获取帮助。