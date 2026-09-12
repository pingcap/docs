---
title: 持续数据管道
summary: 在 {{{ .lake }}} 中使用两种原语构建端到端的变更数据捕获（CDC）流程。
---

# 持续数据管道

在 {{{ .lake }}} 中使用两种原语构建端到端的变更数据捕获（CDC）流程：

- **Streams** 会捕获每一次 INSERT/UPDATE/DELETE，直到你将其消费。
- **Tasks** 会按调度运行 SQL，或在 stream 报告有新行时运行 SQL。

## 快速导航 {#quick-navigation}

- [示例 1：仅追加 Stream 复制](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md#example-1-append-only-stream) – 捕获插入操作并将其消费到另一张表中。
- [示例 2：标准 Stream 修改](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md#example-2-standard-stream-updates--deletes) – 了解修改/删除如何呈现，以及为什么一个 stream 只能由一个消费者清空。
- [示例 3：增量 Stream 指标](/tidb-cloud-lake/guides/track-and-transform-data-via-streams.md#example-3-incremental-stream-join) – 使用 `WITH CONSUME` 连接多个 stream，按批次计算增量。
- [示例 1：定时复制 Task](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md#example-1-scheduled-copy) – 使用两个周期性 task 生成并加载文件。
- [示例 2：由 Stream 触发的合并](/tidb-cloud-lake/guides/automate-data-loading-with-tasks.md#example-2-stream-triggered-merge) – 仅当 `STREAM_STATUS` 为 true 时触发 task。

## 为什么在 {{{ .lake }}} 中使用 CDC {#why-cdc-in-lake}

- **轻量** – stream 仅保留最新的变更集，而不会复制整张表。
- **事务性** – stream 消费会与你的 SQL 语句一起成功提交或回滚。
- **增量** – 使用 `WITH CONSUME` 重复运行同一查询时，只会处理新行。
- **可调度** – task 让你能够将已经用 SQL 表达的复制、合并或告警逻辑自动化。

建议先阅读 stream 示例，再将其与 task 结合起来，实现管道自动化。