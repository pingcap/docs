---
title: Delete a TiDB Cluster
summary: Learn how to delete a TiDB cluster.
---

# TiDBクラスタの削除 {#delete-a-tidb-cluster}

このドキュメントでは、 TiDB Cloudで TiDB クラスターを削除する方法について説明します。

次の手順を実行することで、いつでもクラスターを削除できます。

1.  プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  削除するターゲット クラスターの行で**[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[...]**をクリックすることもできます。

3.  ドロップダウン メニューで**[削除]**をクリックします。

4.  クラスタ削除画面でクラスタ名を入力します。

    将来クラスターを復元する場合は、クラスターのバックアップがあることを確認してください。そうしないと、もう復元できません。 TiDB Dedicatedクラスターをバックアップする方法の詳細については、 [<a href="/tidb-cloud/backup-and-restore.md">TiDBクラスタデータのバックアップと復元</a>](/tidb-cloud/backup-and-restore.md)を参照してください。

    > **ノート：**
    >
    > [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverlessクラスタ</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)の場合、バックアップおよび復元機能は使用できません。 [<a href="https://docs.pingcap.com/tidb/stable/dumpling-overview">Dumpling</a>](https://docs.pingcap.com/tidb/stable/dumpling-overview)使用して、データをバックアップとしてエクスポートできます。

5.  **「結果を理解しました」をクリックします。このクラスターを削除します**。

バックアップされた TiDB Dedicatedクラスターが削除されると、クラスターの既存のバックアップ ファイルはごみ箱に移動されます。

-   自動バックアップからのバックアップ ファイルの場合、ごみ箱には 7 日間保存できます。
-   手動バックアップからのバックアップ ファイルには有効期限はありません。

クラスターをごみ箱から復元する場合は、 [<a href="/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster">削除されたクラスターを復元する</a>](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster)を参照してください。
