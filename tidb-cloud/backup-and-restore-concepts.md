---
title: Backup & Restore
summary: 了解 TiDB Cloud 的备份与恢复相关概念。
---

# 备份与恢复

TiDB Cloud 的备份与恢复功能旨在保护你的数据安全，并通过支持数据的备份与恢复，确保业务的连续性。

<CustomContent plan="byoc">

使用 TiDB Cloud BYOC 时，你可以通过 TiDB Cloud 控制台管理备份与恢复操作，而数据平面运行在你自己的云账户中。这样既能提供托管式的备份与恢复体验，又能将数据平面保留在你的云环境中。

</CustomContent>

## 自动备份

在 TiDB Cloud 中，默认会自动进行快照备份，并根据你的备份保留策略进行存储。

欲了解更多信息，请参见以下内容：

- [{{{ .starter }}} 和 {{{ .essential }}} 实例的自动备份](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups)
- [{{{ .premium }}} <CustomContent plan="byoc">和 {{{ .byoc }}} </CustomContent>实例的自动备份](/tidb-cloud/premium/backup-and-restore-premium.md#automatic-backups)
- [TiDB Cloud Dedicated 集群的自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)

## 手动备份

手动备份使你能够根据需要将数据备份到某个已知状态，并可在任何时候恢复到该状态。你可以在执行高风险操作（如系统升级、关键数据删除或不可逆的 schema 变更）之前使用手动备份。

{{{ .premium }}}<CustomContent plan="byoc">, {{{ .byoc }}},</CustomContent> 和 TiDB Cloud Dedicated 支持手动备份。手动备份可提供一个可控的恢复点，并会一直保留，直到你显式将其删除。手动备份不支持 PITR 或部分备份，并且每次恢复操作都会创建一个新的实例。

更多信息，请参见以下内容：

- [{{{ .premium }}}<CustomContent plan="byoc"> 和 {{{ .byoc }}}</CustomContent> 实例的手动备份](/tidb-cloud/premium/backup-and-restore-premium.md#manual-backups)
- [TiDB Cloud Dedicated 集群的手动备份](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup)

## 双区域备份

双区域备份是 TiDB Cloud Dedicated 的一项功能，允许你将集群所在区域的备份复制到另一个不同的区域。启用后，所有备份会自动复制到指定区域。这为跨区域数据保护和灾难恢复提供了能力。预计大约 99% 的数据可以在一小时内复制到次级区域。

欲了解更多信息，请参见 [开启双区域备份](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

## 时间点恢复

时间点恢复是一项功能，允许你将任意时间点的数据恢复到一个新的 TiDB 集群或实例。你可以用它来：

- 降低灾难恢复中的 RPO。
- 通过恢复到错误事件发生前的时间点，解决数据写入错误的问题。
- 审计业务的历史数据。

如果你想执行时间点恢复，请注意以下事项：

- 对于 TiDB Cloud Starter 实例，不支持时间点恢复。
- 对于 TiDB Cloud Essential 实例，你可以恢复到最近 30 天内的任意时间点。欲了解更多信息，请参见 [恢复模式](/tidb-cloud/backup-and-restore-serverless.md#restore-mode)。
- 对于 TiDB Cloud Dedicated 集群，你需要提前 [开启 PITR](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)。

## 恢复 {#restore}

TiDB Cloud 支持通过备份快照或时间点恢复将数据恢复到新的集群或实例。恢复操作可帮助你从意外数据丢失、数据损坏或应用程序错误中进行恢复。

对于 {{{ .premium }}}<CustomContent plan="byoc"> 和 {{{ .byoc }}}</CustomContent> 实例，你可以将数据恢复到新的实例。你可以从自动备份、手动备份或受支持的外部云存储备份进行恢复。PITR 仅支持自动备份，不支持手动备份。
