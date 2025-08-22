---
title: 备份与恢复
summary: 了解 TiDB Cloud 的备份与恢复相关概念。
---

# 备份与恢复

TiDB Cloud 的备份与恢复功能旨在保护你的数据安全，并通过支持集群数据的备份与恢复，保障业务的连续性。

## 自动备份

对于 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 集群，默认会自动进行快照备份，并根据你的备份保留策略进行存储。

如需了解更多信息，请参见以下内容：

- [TiDB Cloud Serverless 集群的自动备份](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups)
- [TiDB Cloud Dedicated 集群的自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)

## 手动备份

手动备份是 TiDB Cloud Dedicated 的一项功能，允许你根据需要将数据备份到已知状态，并可在任何时间恢复到该状态。

如需了解更多信息，请参见 [执行手动备份](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup)。

## 双区域备份

双区域备份是 TiDB Cloud Dedicated 的一项功能，允许你将集群所在区域的备份复制到另一个不同的区域。启用后，所有备份会自动复制到指定区域。这为跨区域数据保护和灾难恢复提供了能力。预计大约 99% 的数据可以在一小时内复制到次级区域。

如需了解更多信息，请参见 [开启双区域备份](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

## 时间点恢复

时间点恢复是一项功能，允许你将任意时间点的数据恢复到一个新集群。你可以使用该功能：

- 降低灾难恢复中的 RPO。
- 通过恢复到错误事件发生前的时间点，解决数据写入错误的问题。
- 审计业务的历史数据。

如果你想执行时间点恢复，请注意以下事项：

- 对于 TiDB Cloud Serverless 集群，时间点恢复仅适用于可扩展集群，不适用于免费集群。更多信息请参见 [恢复模式](/tidb-cloud/backup-and-restore-serverless.md#restore-mode)。
- 对于 TiDB Cloud Dedicated 集群，你需要提前 [开启 PITR](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)。