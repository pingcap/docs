---
title: Delete a TiDB Cluster
summary: TiDB クラスターを削除する方法を学習します。
---

# TiDBクラスタを削除する {#delete-a-tidb-cluster}

このドキュメントでは、 TiDB Cloud上の TiDB クラスターを削除する方法について説明します。

次の手順を実行することにより、いつでもクラスターを削除できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

2.  削除するターゲット クラスターの行で、 **...**をクリックします。

    > **ヒント：**
    >
    > または、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**... を**クリックすることもできます。

3.  ドロップダウンメニューで**「削除」を**クリックします。

4.  クラスター削除ウィンドウで、削除を確認します。

    -   手動または自動バックアップが少なくとも1つある場合は、バックアップの数とバックアップの課金ポリシーを確認できます。 **「続行」**をクリックし、 `<organization name>/<project name>/<cluster name>`と入力してください。
    -   バックアップがない場合は、 `<organization name>/<project name>/<cluster name>`と入力してください。

    将来クラスタを復元する場合は、クラスタのバックアップを必ず作成してください。バックアップがないと、復元できなくなります。TiDB TiDB Cloud Dedicatedクラスタのバックアップ方法の詳細については、 [TiDB Cloud専用データのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

    > **注記：**
    >
    > [TiDB Cloudサーバーレス クラスター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)削除後のデータの復元をサポートしていません。TiDB TiDB Cloud Serverless クラスターを削除し、後でデータを復元する場合は、 [TiDB Cloud Serverlessからデータをエクスポート](/tidb-cloud/serverless-export.md)参照してデータをバックアップとしてエクスポートしてください。

5.  **「理解しましたので削除します」を**クリックします。

    バックアップされたTiDB Cloud Dedicated クラスターが削除されると、クラスターの既存のバックアップ ファイルはごみ箱に移動されます。

    -   自動バックアップは保持期間が終了すると期限切れとなり、自動的に削除されます。デフォルトの保持期間は、変更しない場合は7日間です。

    -   手動バックアップは、手動で削除されるまでごみ箱に保存されます。

    > **注記：**
    >
    > バックアップは削除されるまで料金が発生し続けることにご注意ください。

    TiDB Cloud Dedicated クラスターをごみ箱から復元する場合は、 [削除されたクラスターを復元する](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster)参照してください。
