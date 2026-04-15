---
title: Delete a TiDB Cloud Resource
summary: TiDB Cloudリソースを削除する方法を学びましょう。
---

# TiDB Cloudリソースを削除します {#delete-a-tidb-cloud-resource}

このドキュメントでは、以下のTiDB Cloudリソースを削除する方法について説明します。

-   [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)インスタンス
-   [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンス
-   [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスター

以下の手順を実行することで、いつでもTiDB Cloudリソースを削除できます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

2.  削除する対象リソースの行で、 **...**をクリックします。

    > **ヒント：**
    >
    > または、対象のリソース名をクリックして概要ページに移動し、右上隅の**「…」**をクリックすることもできます。

3.  ドロップダウンメニューの**「削除」**をクリックしてください。

4.  削除確認ウィンドウで、削除を確定してください。

    -   手動または自動バックアップが少なくとも 1 つある場合は、バックアップの数とバックアップの課金ポリシーを確認できます。 **[続行]**をクリックして`<organization name>/<project name>/<resource name>`と入力します。
    -   バックアップがない場合は、 `<organization name>/<project name>/<resource name>`と入力してください。

    削除されたTiDB Cloud Dedicatedクラスターを将来復元したい場合は、そのバックアップがあることを確認してください。そうしないと、もう復元できません。 TiDB Cloud Dedicatedクラスターをバックアップする方法の詳細については、 [TiDB Cloud Dedicatedデータのバックアップと復元](/tidb-cloud/backup-and-restore.md)参照してください。

    > **注記：**
    >
    > [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)と[TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンスは、削除後のデータの復元をサポートしていません。 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを削除し、将来そのデータを復元したい場合は、 [TiDB Cloud StarterまたはEssentialからデータをエクスポートする](/tidb-cloud/serverless-export.md)参照してデータをバックアップとしてエクスポートします。

5.  **「了解しました、削除します」**をクリックしてください。

    バックアップ済みのTiDB Cloud Dedicatedクラスターが削除されると、クラスターの既存のバックアップファイルはごみ箱に移動されます。

    -   自動バックアップは、最新のものを除き、保持期間が終了すると期限切れとなり自動的に削除されます。保持期間は、変更しない場合はデフォルトで7日間です。最新の自動バックアップは、明示的に削除しない限り削除されません。

    -   手動で作成したバックアップファイルは、手動で削除されるまでごみ箱に保存されます。

    > **注記：**
    >
    > バックアップは削除されるまで料金が発生し続けることにご注意ください。

    TiDB Cloud Dedicatedクラスターをごみ箱から復元する場合は、 [削除されたクラスターを復元する](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster)参照してください。
