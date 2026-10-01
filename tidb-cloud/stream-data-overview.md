---
title: 同步数据
summary: 了解将数据变更从 TiDB Cloud 同步到下游系统的选项，包括 Changefeed 和 Data Pipeline。
---

# 同步数据

TiDB Cloud 可以持续将数据变更从你的 TiDB Cloud 实例同步到下游系统。它提供以下数据同步选项：

- **Changefeed**：将增量行变更流式传输到下游系统，例如 Apache Kafka、MySQL、TiDB Cloud 和云存储。
- **Data Pipeline**：导出所选数据的完整快照，然后持续将行变更复制到 TiDB Cloud Lake。

## Changefeed {#changefeed}

Changefeed 会将增量数据变更从 TiDB Cloud 流式传输到下游系统。当你只需要持续复制增量变更，且下游系统能够消费增量事件时，可以使用它。

你可以在 TiDB Cloud 控制台的 **Changefeed** 页面创建和管理 changefeed。更多信息，参见 [Changefeed](/tidb-cloud/changefeed-overview.md)。

## Data Pipeline (PREVIEW) {#data-pipeline-preview}

Data Pipeline 会将完整数据和增量变更从你的 TiDB Cloud 实例复制到 TiDB Cloud Lake。它使用外部 stage（例如 Amazon S3 或 Alibaba Cloud OSS）在源端和目标端之间缓冲数据，从而提高可靠性，并让你能够控制成本和延时。更多信息，参见 [Data Pipeline](/tidb-cloud/data-pipeline.md)。

> **注意：**
>
> TiDB Cloud 控制台中的 Data Pipeline 功能目前处于私有预览阶段，可按需申请使用。要申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Support Tickets** 进入 [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals)。创建一个工单，在 **Description** 字段中输入 "Apply for `Data Pipeline to TiDB Cloud Lake`"，然后点击 **Submit**。