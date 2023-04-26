---
title: Delete a TiDB Cluster
summary: Learn how to delete a TiDB cluster.
---

# TiDBクラスタを削除する {#delete-a-tidb-cluster}

このドキュメントでは、 TiDB Cloudで TiDB クラスターを削除する方法について説明します。

次の手順を実行して、いつでもクラスターを削除できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  削除するターゲット クラスターの行で、 **[...]**をクリックします。

    > **ヒント：**
    >
    > または、ターゲット クラスタの名前をクリックしてその概要ページに移動し、右上隅の**[...]**をクリックすることもできます。

3.  ドロップダウン メニューで**[削除]**をクリックします。

4.  クラスターの削除ウィンドウで、クラスター名を入力します。

    将来、クラスターを復元する場合は、クラスターのバックアップがあることを確認してください。そうしないと、元に戻すことができなくなります。 Dedicated Tierクラスターをバックアップする方法の詳細については、 [TiDBクラスタデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

    > **ノート：**
    >
    > [Serverless Tierクラスター](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)の場合、バックアップおよび復元機能は使用できません。 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)使用して、データをバックアップとしてエクスポートできます。

5.  **[結果を理解しました] をクリックします。このクラスターを削除します**。

バックアップされたDedicated Tierクラスターが削除されると、クラスターの既存のバックアップ ファイルはごみ箱に移動されます。

-   自動バックアップからのバックアップ ファイルの場合、ごみ箱はそれらを 7 日間保持できます。
-   手動バックアップからのバックアップ ファイルの場合、有効期限はありません。

ごみ箱からクラスターを復元する場合は、 [削除されたクラスターを復元する](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster)を参照してください。
