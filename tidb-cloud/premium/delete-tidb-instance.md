---
title: Delete a TiDB Cloud Premium instance
summary: TiDB Cloud Premiumインスタンスを削除する方法を学びましょう。
---

# TiDB Cloud Premiumインスタンスを削除します {#delete-a-tidb-cloud-premium-instance}

このドキュメントでは、 TiDB Cloud Premiumインスタンスを削除する方法について説明します。

以下の手順を実行することで、いつでもインスタンスを削除できます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

2.  削除する対象インスタンスの行で、 **...**をクリックします。

    > **ヒント：**
    >
    > または、対象インスタンスの名前をクリックして概要ページに移動し、右上隅の**「…」**をクリックすることもできます。

3.  ドロップダウンメニューの**「削除」**をクリックしてください。

4.  削除確認ウィンドウで、削除を確定してください。

    インスタンスが正しく削除されるように、 `<organization name>/<instance name>`を入力してください。

    将来インスタンスを復元する場合は、インスタンスのバックアップがあることを確認してください。そうしないと復元できません。 TiDB Cloud Premium インスタンスをバックアップする方法の詳細については、 [TiDB Cloud Premium データのバックアップと復元](/tidb-cloud/premium/backup-and-restore-premium.md)参照してください。

5.  **「了解しました、削除します」**をクリックしてください。

    バックアップ済みのTiDB Cloud Premiumインスタンスを削除すると、そのインスタンスの既存のバックアップファイルはごみ箱に移動されます。

    自動バックアップは、保存期間が終了すると期限切れとなり、自動的に削除されます。保存期間は、変更しない場合はデフォルトで7日間です。

    > **注記：**
    >
    > バックアップは削除されるまで料金が発生し続けることにご注意ください。

    TiDB Cloud Premium インスタンスをごみ箱から復元する場合は、 [ごみ箱から復元](/tidb-cloud/premium/backup-and-restore-premium.md#restore-from-recycle-bin)参照してください。
