---
title: Manage TiDB Cloud Branches
summary: TiDB Cloudブランチの管理方法を学びましょう。
---

# TiDB Cloudブランチの管理 {#manage-tidb-cloud-branches}

このドキュメントでは、TiDB Cloud を使用して[TiDB Cloudコンソール](https://tidbcloud.com)TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのブランチを管理する方法について説明します。 TiDB Cloud CLI を使用して管理するには、 [`ticloud branch`](/tidb-cloud/ticloud-branch-create.md)参照してください。

## 必要なアクセス {#required-access}

-   [ブランチを作成する](#create-a-branch)または[ブランチに接続する](#connect-to-a-branch)には、組織の`Organization Owner`ロール、またはターゲット プロジェクトの`Project Owner`ロールに属している必要があります。
-   プロジェクト内の[ブランチを表示](#create-a-branch)の場合は、そのプロジェクトに属している必要があります。

権限の詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)を参照してください。

## ブランチを作成する {#create-a-branch}

> **注記：**
>
> 2023 年 7 月 5 日以降に作成されたTiDB Cloud StarterインスタンスまたはTiDB Cloud Essentialインスタンスのブランチのみを作成できます。その他の制限事項については[制限事項と割り当て](/tidb-cloud/branch-overview.md#limitations-and-quotas)参照してください。

ブランチを作成するには、以下の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで**「支店」**をクリックします。

3.  **「ブランチ」**ページの右上隅にある**「ブランチの作成」を**クリックします。ダイアログが表示されます。

    または、既存の親ブランチからブランチを作成するには、対象の親ブランチの行を見つけて、 **[アクション**] 列の**[...]** &gt; **[ブランチの作成] を**クリックします。

4.  **「ブランチの作成」**ダイアログで、以下のオプションを設定します。

    -   **名前**：支店の名前を入力してください。
    -   **親ブランチ**：元のTiDB Cloud StarterまたはEssentialインスタンス、あるいは既存のブランチを選択します。 `main`現在のインスタンスを表します。
    -   **データを含める最大**: 次のいずれかを選択してください:
        -   **現在の時点**：現在の状態からブランチを作成します。
        -   **特定の日時**：指定した時間からブランチを作成します。

5.  **「作成」**をクリックします。

TiDB Cloud StarterまたはEssentialインスタンスのデータサイズにもよりますが、ブランチの作成は数分で完了します。

## 支店をビュー {#view-branches}

TiDB Cloud StarterまたはEssentialインスタンスのブランチを表示するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで**「支店」**をクリックします。

    TiDB Cloud StarterまたはEssentialインスタンスのブランチリストは、右側のペインに表示されます。

## 支店に接続する {#connect-to-a-branch}

支店に接続するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで**「支店」**をクリックします。
3.  接続する対象ブランチの行で、 **「アクション」**列の**「…」**をクリックします。
4.  ドロップダウンリストから**「接続」**をクリックします。接続情報の入力ダイアログが表示されます。
5.  ルートパスワードを作成またはリセットするには、 **「パスワードを生成」**または**「パスワードをリセット」**をクリックしてください。
6.  接続情報を使用してブランチに接続します。

または、 TiDB Cloud StarterまたはEssentialインスタンスの概要ページから接続文字列を取得することもできます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。
2.  右上隅の**「接続」**をクリックしてください。
3.  `Branch`ドロップダウンリストから接続先のブランチを選択してください。
4.  ルートパスワードを作成またはリセットするには、 **「パスワードを生成」**または**「パスワードをリセット」**をクリックしてください。
5.  接続情報を使用してブランチに接続します。

## ブランチを削除する {#delete-a-branch}

ブランチを削除するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで**「支店」**をクリックします。
3.  削除する対象ブランチの行で、 **「アクション」**列の**「…」**をクリックします。
4.  ドロップダウンリストの**「削除」**をクリックしてください。
5.  削除を確認してください。

## ブランチをリセットする {#reset-a-branch}

ブランチをリセットすると、親ブランチの最新データと同期されます。

> **注記：**
>
> この操作は元に戻せません。ブランチをリセットする前に、重要なデータはすべてバックアップしておいてください。

ブランチをリセットするには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで**「支店」**をクリックします。
3.  リセットする対象ブランチの行で、 **「アクション」**列の**「…」**をクリックします。
4.  ドロップダウンリストの**「リセット」**をクリックしてください。
5.  リセットを確認してください。

## 次は？ {#what-s-next}

-   [TiDB Cloud BranchingをGitHub CI/CDパイプラインに統合する](/tidb-cloud/branch-github-integration.md)
