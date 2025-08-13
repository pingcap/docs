---
title: Manage TiDB Cloud Branches
summary: TiDB Cloudブランチを管理する方法を学習します。
---

# TiDB Cloudブランチの管理 {#manage-tidb-cloud-branches}

このドキュメントでは、 [TiDB Cloudコンソール](https://tidbcloud.com)を使用してTiDB Cloud Starter またはTiDB Cloud Essential クラスターのブランチを管理する方法について説明します。TiDB TiDB Cloud CLI を使用して管理するには、 [`ticloud branch`](/tidb-cloud/ticloud-branch-create.md)参照してください。

## 必要なアクセス {#required-access}

-   [ブランチを作成する](#create-a-branch)または[ブランチに接続する](#connect-to-a-branch)実行するには、組織の`Organization Owner`ロールまたは対象プロジェクトの`Project Owner`ロールに所属している必要があります。
-   プロジェクト内のクラスターを[ブランチを表示](#create-a-branch)作成するには、そのプロジェクトに属している必要があります。

権限の詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)参照してください。

## ブランチを作成する {#create-a-branch}

> **注記：**
>
> 2023 年 7 月 5 日以降に作成されたTiDB Cloud Starter またはTiDB Cloud Essential クラスターのブランチのみを作成できます。詳細な制限については、 [制限と割り当て](/tidb-cloud/branch-overview.md#limitations-and-quotas)参照してください。

ブランチを作成するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットのTiDB Cloud Starter またはTiDB Cloud Essential クラスターの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。

3.  **「ブランチ」**ページの右上隅にある**「ブランチの作成」を**クリックします。ダイアログが表示されます。

    または、既存の親ブランチからブランチを作成するには、対象の親ブランチの行を見つけて、 **[アクション**] 列で**[...]** &gt; **[ブランチの作成] を**クリックします。

4.  **[ブランチの作成]**ダイアログで、次のオプションを設定します。

    -   **名前**: ブランチの名前を入力します。
    -   **親ブランチ**: 元のクラスターまたは既存のブランチを選択します。2 `main`現在のクラスターを表します。
    -   **最大 のデータを含める**: 次のいずれかを選択します。
        -   **現在の時点**: 現在の状態からブランチを作成します。
        -   **特定の日時**: 指定された時間からブランチを作成します。

5.  **[作成]を**クリックします。

クラスター内のデータ サイズに応じて、ブランチの作成は数分で完了します。

## ブランチをビュー {#view-branches}

クラスターのブランチを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットのTiDB Cloud Starter またはTiDB Cloud Essential クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。

    クラスターのブランチ リストが右側のペインに表示されます。

## ブランチに接続する {#connect-to-a-branch}

ブランチに接続するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットのTiDB Cloud Starter またはTiDB Cloud Essential クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。
3.  接続するターゲット ブランチの行で、 **[アクション**] 列の**[...]**をクリックします。
4.  ドロップダウンリストの**「接続」**をクリックします。接続情報を入力するダイアログが表示されます。
5.  ルート パスワードを作成またはリセットするには、[パスワード**の生成]**または**[パスワードのリセット]**をクリックします。
6.  接続情報を使用してブランチに接続します。

あるいは、クラスターの概要ページから接続文字列を取得することもできます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットのTiDB Cloud Starter またはTiDB Cloud Essential クラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。
3.  `Branch`ドロップダウン リストで、接続するブランチを選択します。
4.  ルート パスワードを作成またはリセットするには、[パスワード**の生成]**または**[パスワードのリセット]**をクリックします。
5.  接続情報を使用してブランチに接続します。

## ブランチを削除する {#delete-a-branch}

ブランチを削除するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットのTiDB Cloud Starter またはTiDB Cloud Essential クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。
3.  削除するターゲット ブランチの行で、[**アクション**] 列の**[...]**をクリックします。
4.  ドロップダウンリストで**[削除] を**クリックします。
5.  削除を確認します。

## ブランチをリセットする {#reset-a-branch}

ブランチをリセットすると、その親の最新データと同期されます。

> **注記：**
>
> この操作は元に戻せません。ブランチをリセットする前に、重要なデータをすべてバックアップしておいてください。

ブランチをリセットするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットのTiDB Cloud Starter またはTiDB Cloud Essential クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。
3.  リセットするターゲット ブランチの行で、[**アクション**] 列の**[...]**をクリックします。
4.  ドロップダウン リストで**[リセット] を**クリックします。
5.  リセットを確認します。

## 次は何？ {#what-s-next}

-   [TiDB Cloud Branching を GitHub CI/CD パイプラインに統合する](/tidb-cloud/branch-github-integration.md)
