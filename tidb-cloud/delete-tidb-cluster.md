---
title: Delete a TiDB Cluster
summary: Learn how to delete a TiDB cluster.
---

# TiDBクラスタの削除 {#delete-a-tidb-cluster}

このドキュメントでは、 TiDB Cloudで TiDB クラスターを削除する方法について説明します。

次の手順を実行することで、いつでもクラスターを削除できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  削除するターゲット クラスターの行で**[...]**をクリックします。

    > **ヒント：**
    >
    > あるいは、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[...]**をクリックすることもできます。

3.  ドロップダウン メニューで**[削除]**をクリックします。

4.  クラスターの削除ウィンドウで、 `<organization name>/<project name>/<cluster name>`を入力します。

    将来クラスターを復元する場合は、クラスターのバックアップがあることを確認してください。そうしないと、もう復元できません。 TiDB 専用クラスターをバックアップする方法の詳細については、 [TiDB 専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)を参照してください。

    > **注記：**
    >
    > [TiDB サーバーレスクラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless) [バックアップからのインプレース復元](/tidb-cloud/backup-and-restore-serverless.md#restore)のみをサポートし、削除後のデータの復元をサポートしません。将来、TiDB サーバーレス クラスターを削除し、そのデータを復元したい場合は、 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)使用してデータをバックアップとしてエクスポートできます。

5.  **「結果を理解しました」をクリックします。このクラスターを削除します**。

バックアップされた TiDB 専用クラスターが削除されると、クラスターの既存のバックアップ ファイルはごみ箱に移動されます。

-   自動バックアップからのバックアップ ファイルの場合、ごみ箱には 7 日間保存できます。
-   手動バックアップからのバックアップ ファイルには有効期限はありません。

TiDB 専用クラスターをごみ箱から復元する場合は、 [削除されたクラスターを復元する](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster)を参照してください。
