---
title: Delete a TiDB Cloud Premium instance
summary: TiDB Cloud Premium インスタンスを削除する方法を学習します。
---

# TiDB Cloud Premiumインスタンスを削除する {#delete-a-tidb-cloud-premium-instance}

このドキュメントでは、 TiDB Cloud Premium インスタンスを削除する方法について説明します。

次の手順を実行することにより、いつでもインスタンスを削除できます。

1.  [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動します。

2.  削除する対象インスタンスの行で、 **...**をクリックします。

    > **ヒント：**
    >
    > または、ターゲットインスタンスの名前をクリックして概要ページに移動し、右上隅の**...**をクリックすることもできます。

3.  ドロップダウンメニューで**「削除」**をクリックします。

4.  削除確認ウィンドウで、削除を確認します。

    インスタンスが正しく削除されたことを確認するには、 `<organization name>/<instance name>`を入力します。

    将来インスタンスを復元する場合は、インスタンスのバックアップがあることを確認してください。バックアップがない場合、復元できません。TiDB TiDB Cloud Premiumインスタンスのバックアップ方法の詳細については、 [TiDB Cloud Premium データのバックアップと復元](/tidb-cloud/premium/backup-and-restore-premium.md)ご覧ください。

5.  **「理解しましたので削除します」**をクリックします。

    バックアップされたTiDB Cloud Premium インスタンスを削除すると、インスタンスの既存のバックアップ ファイルはごみ箱に移動されます。

    自動バックアップは保持期間が終了すると期限切れとなり、自動的に削除されます。デフォルトの保持期間は、変更しない場合は7日間です。

    > **注記：**
    >
    > バックアップは削除されるまで料金が発生し続けることにご注意ください。

    TiDB Cloud Premium インスタンスをごみ箱から復元する場合は、 [ごみ箱から復元](/tidb-cloud/premium/backup-and-restore-premium.md#restore-from-recycle-bin)参照してください。
