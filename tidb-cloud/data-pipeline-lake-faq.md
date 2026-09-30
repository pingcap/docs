---
title: Data Pipeline 常见问题
summary: 关于 TiDB Cloud Data Pipeline 到 TiDB Cloud Lake 的常见问题，包括外部 stage、事件驱动摄取和计费。
---

# Data Pipeline 常见问题

本文档解答了关于 TiDB Cloud Data Pipeline 到 TiDB Cloud Lake 的常见问题。

## 为什么数据管道需要外部 stage？ {#why-does-a-data-pipeline-require-an-external-stage}

出于可靠性考虑，需要使用外部 stage。由于两端都通过 stage 工作，而不是直接传输数据，因此 TiDB Cloud 侧的写入速率与 TiDB Cloud Lake 的消费速率实现了解耦：

- 在高写入吞吐下，变更数据会持久存储在 stage 中，即使加载到 TiDB Cloud Lake 的过程延迟或中断，TiDB Cloud Lake 仍然可以继续加载这些数据。
- stage 会缓冲写入负载，防止数据生产速率与摄取速率之间的临时差异直接影响 TiDB Cloud Lake 的数据摄取。
- TiDB Cloud Lake 侧的摄取频率与写入速率解耦，这为你提供了一种控制 TiDB Cloud Lake 侧成本的方式。

## 我需要通过 SQS 队列启用事件驱动摄取吗？ {#do-i-need-to-enable-event-driven-ingestion-with-an-sqs-queue}

当你需要比默认轮询模式提供的**更低数据延时**时，请启用事件驱动摄取。

在默认模式下，Data Pipeline 依赖以下两个时间间隔：changefeed 将增量数据刷新到外部 stage 的间隔，以及 TiDB Cloud Lake 扫描 stage 以发现新数据的间隔。对于 {{{ .premium }}}<CustomContent plan="byoc"> 和 {{{ .byoc }}}</CustomContent>，配置的 **Sync Interval** 是这些阶段上的端到端延时目标。

在事件驱动模式下，changefeed 仍会按照其配置的时间间隔将数据刷新到外部 stage，但每次刷新还会触发发送到 SQS 队列的 **S3 event notification**。借助 SQS 通知，TiDB Cloud Lake 可以更快检测到新数据，而不必等待下一次按计划执行的扫描。

**权衡：** 在事件驱动模式下，TiDB Cloud Lake 可以更频繁地摄取新数据，这可能会使计算集群 (Warehouse) 更长时间保持在 **active** 状态。这会增加计算集群托管成本。

## 数据管道是否会产生额外的 TiDB Cloud Lake 费用？ {#does-a-data-pipeline-incur-additional-tidb-cloud-lake-charges}

数据管道不会引入单独的计费类别。成本来自管道中涉及的现有组件：

- **Export**（一次性）：按完整快照导出的费用计费。
- **Changefeed**（持续）：如果启用了增量复制，则按用于持续复制的 changefeed 资源计费。
- **TiDB Cloud Lake**（持续）：按数据存储和计算集群计算资源计费。详情请参见 [TiDB Cloud Lake Pricing & Billing](https://docs.pingcap.com/tidbcloudlake/pricing-billing/)。