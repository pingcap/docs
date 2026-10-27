---
title: Delete a TiDB Cloud Premium or {{{ .byoc }}} instance
summary: TiDB Cloud Premiumまたは{{{ .byoc }}}インスタンスを削除する方法を学びましょう。
---

# {{{ .premium }}} または {{{ .byoc }}} インスタンスを削除する

このドキュメントでは、{{{ .premium }}} または {{{ .byoc }}} インスタンスを削除する方法について説明します。

以下の手順を実行することで、いつでもインスタンスを削除できます。

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動します。
2. 削除対象のインスタンスの行で、**...** をクリックします。

    > **Tip:**
    >
    > または、対象インスタンスの名前をクリックして概要ページに移動し、右上隅の **...** をクリックすることもできます。

3. ドロップダウンメニューの **Delete** をクリックします。
4. 削除確認ウィンドウで、削除を確定します。

    インスタンスが正しく削除されるように、`<organization name>/<instance name>` を入力します。

    将来インスタンスを復元する可能性がある場合は、そのインスタンスのバックアップがあることを確認してください。そうしないと、復元できません。{{{ .premium }}} または {{{ .byoc }}} インスタンスのバックアップ方法の詳細については、[{{{ .premium }}} または {{{ .byoc }}} データをバックアップおよび復元する](/tidb-cloud/premium/backup-and-restore-premium.md)を参照してください。

5. **I understand, delete it** をクリックします。

    バックアップ済みの {{{ .premium }}} または {{{ .byoc }}} インスタンスを削除すると、そのインスタンスの既存のバックアップファイルはごみ箱に移動されます。

    自動バックアップは、保持期間が終了すると期限切れとなり、自動的に削除されます。保持期間は、変更しない場合はデフォルトで 7日間です。

    <CustomContent plan="premium">

    > **Note:**
    >
    > バックアップは削除されるまで引き続き料金が発生します。

    </CustomContent>

    <CustomContent plan="byoc">

    > **Note:**
    >
    > BYOC インスタンスの場合、TiDB Cloud はバックアップに対して課金しません。お客様のクラウドアカウントで発生するストレージおよびデータ転送のコストは、お客様の負担となります。ストレージ料金は、バックアップファイルが削除されるまで継続して発生します。

    </CustomContent>

    ごみ箱から {{{ .premium }}} または {{{ .byoc }}} インスタンスを復元する場合は、[ごみ箱から復元](/tidb-cloud/premium/backup-and-restore-premium.md#restore-from-recycle-bin)を参照してください。
