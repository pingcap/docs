---
title: 删除 TiDB 集群
summary: 了解如何删除 TiDB 集群。
---

# 删除 TiDB 集群

本文档介绍如何在 TiDB Cloud 上删除 TiDB 集群。

你可以随时通过以下步骤删除集群：

1. 进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。
2. 在你想要删除的目标集群所在行，点击 **...**。

    > **提示：**
    >
    > 你也可以点击目标集群的名称进入其概览页面，然后点击右上角的 **...**。

3. 在下拉菜单中点击 **Delete**。
4. 在集群删除窗口中，确认删除操作：

    - 如果你至少有一次手动或自动备份，你可以看到备份的数量以及备份的计费策略。点击 **Continue** 并输入 `<organization name>/<project name>/<cluster name>`。
    - 如果你没有任何备份，只需输入 `<organization name>/<project name>/<cluster name>`。

    如果你希望将来恢复该集群，请确保你已经对集群进行了备份。否则，将无法再恢复。关于如何备份 TiDB Cloud Dedicated 集群的更多信息，请参见 [Back Up and Restore TiDB Cloud Dedicated Data](/tidb-cloud/backup-and-restore.md)。

    > **注意：**
    >
    > [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 和 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 集群在删除后不支持数据恢复。如果你希望删除 TiDB Cloud Starter 或 TiDB Cloud Essential 集群并在未来恢复其数据，请参见 [Export Data from TiDB Cloud Starter or Essential](/tidb-cloud/serverless-export.md) 将你的数据导出作为备份。

5. 点击 **I understand, delete it**。

    一旦已备份的 TiDB Cloud Dedicated 集群被删除，该集群现有的备份文件会被移动到回收站。

    - 自动备份将在保留期结束后过期并自动删除。如果你未修改，默认保留期为 7 天。
    - 手动备份会一直保留在回收站，直到被手动删除。

    > **注意：**
    >
    > 请注意，备份在被删除前会持续产生费用。

    如果你希望从回收站恢复 TiDB Cloud Dedicated 集群，请参见 [Restore a deleted cluster](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster)。