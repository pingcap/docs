---
title: Delete a TiDB Cloud Premium instance
summary: TiDB Cloud Premiumインスタンスを削除する方法を学びましょう。
---

# {{{ .premium }}} インスタンスを削除する {#delete-a-tidb-cloud-premium-instance}

このドキュメントでは、{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスを削除する方法について説明します。

以下の手順を実行することで、いつでもインスタンスを削除できます。

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動します。
2. 削除対象のインスタンスの行で、**...** をクリックします。

    > **Tip:**
    >
    > または、対象インスタンスの名前をクリックして概要ページに移動し、右上隅の **...** をクリックすることもできます。

3. ドロップダウンメニューの **Delete** をクリックします。
4. 削除確認ウィンドウで、削除を確定します。

    インスタンスが正しく削除されるように、`<organization name>/<instance name>` を入力します。

    将来インスタンスを復元したい場合は、インスタンスのバックアップがあることを確認してください。そうしないと復元できません。{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスのバックアップ方法の詳細については、[{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> データのバックアップと復元](/tidb-cloud/premium/backup-and-restore-premium.md) を参照してください。

5. **I understand, delete it** をクリックします。

    バックアップ済みの {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスを削除すると、そのインスタンスの既存のバックアップファイルはごみ箱に移動されます。

    自動バックアップは、保存期間が終了すると期限切れとなり、自動的に削除されます。保存期間は、変更しない場合はデフォルトで 7日間です。

    > **Note:**
    >
    > バックアップは削除されるまで料金が発生し続けることにご注意ください。

    ごみ箱から {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスを復元する場合は、[ごみ箱から復元](/tidb-cloud/premium/backup-and-restore-premium.md#restore-from-recycle-bin) を参照してください。
