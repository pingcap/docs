---
title: 删除 TiDB Cloud 资源
summary: 了解如何删除 TiDB Cloud 资源。
---

# 删除 TiDB Cloud 资源

本文档介绍如何删除以下 TiDB Cloud 资源：

- [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) 实例
- [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) 实例
- [{{{ .dedicated }}}](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群

你可以随时按照以下步骤删除 TiDB Cloud 资源：

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。
2. 在目标资源所在行，点击 **...**。

    > **提示：**
    >
    > 你也可以点击目标资源的名称进入其概览页面，然后点击右上角的 **...**。

3. 在下拉菜单中点击 **Delete**。
4. 在删除确认窗口中，确认删除操作：

    - 如果你至少有一个手动或自动备份，你可以看到备份数量以及备份的计费策略。点击 **Continue** 并输入 `<organization name>/<project name>/<resource name>`。
    - 如果你没有任何备份，只需输入 `<organization name>/<project name>/<resource name>`。

    如果你希望将来恢复已删除的 {{{ .dedicated }}} 集群，请确保你已经对其进行了备份。否则，你将无法再恢复。关于如何备份 TiDB Cloud Dedicated 集群的更多信息，请参见 [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md)。

    > **注意：**
    >
    > [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) 和 [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) 实例在删除后不支持数据恢复。如果你希望删除 {{{ .starter }}} 或 {{{ .essential }}} 实例并在未来恢复其数据，请参见 [Export Data from {{{ .starter }}} or Essential](/tidb-cloud/serverless-export.md) 将你的数据导出作为备份。

5. 点击 **I understand, delete it**。

    一旦已备份的 TiDB Cloud Dedicated 集群被删除，该集群现有的备份文件会被移动到回收站。

    - 自动备份将在保留时间结束后过期并被自动删除，最新的一份除外。如果你未修改，默认保留时间为 7 天。除非你明确删除，最新的自动备份不会被删除。
    - 手动备份会一直保留在回收站，直到被手动删除。

    > **注意：**
    >
    > 请注意，备份在被删除前会持续产生费用。

    如果你希望从回收站恢复 TiDB Cloud Dedicated 集群，请参见 [Restore a deleted cluster](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster)。
