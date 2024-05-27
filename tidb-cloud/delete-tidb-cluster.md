---
title: Delete a TiDB Cluster
summary: TiDB クラスターを削除する方法を学習します。
---

# TiDBクラスタを削除する {#delete-a-tidb-cluster}

このドキュメントでは、TiDB Cloud上の TiDB クラスターを削除する方法について説明します。

次の手順を実行することで、いつでもクラスターを削除できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  削除するターゲット クラスターの行で、 **...**をクリックします。

    > **ヒント：**
    >
    > または、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[...]**をクリックすることもできます。

3.  ドロップダウンメニューで**「削除」を**クリックします。

4.  クラスター削除ウィンドウで、 `<organization name>/<project name>/<cluster name>`入力します。

    将来クラスターを復元する場合は、クラスターのバックアップがあることを確認してください。バックアップがないと、復元できなくなります。TiDB 専用クラスターのバックアップ方法の詳細については、 [TiDB専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

    > **注記：**
    >
    > [TiDB サーバーレス クラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless) [バックアップからのインプレース復元](/tidb-cloud/backup-and-restore-serverless.md#restore)のみをサポートし、削除後のデータの復元はサポートしていません。TiDB Serverless クラスターを削除し、将来そのデータを復元する場合は、 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)を使用してデータをバックアップとしてエクスポートできます。

5.  **[結果を理解しました。このクラスターを削除します]**をクリックします。

バックアップされた TiDB 専用クラスターが削除されると、クラスターの既存のバックアップ ファイルはごみ箱に移動されます。

-   自動バックアップからのバックアップ ファイルの場合、ごみ箱には 7 日間保存されます。
-   手動バックアップからのバックアップ ファイルには有効期限はありません。

ごみ箱から TiDB 専用クラスターを復元する場合は、 [削除されたクラスターを復元する](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster)参照してください。
