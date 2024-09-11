---
title: Manage TiDB Cloud Serverless Branches
summary: TiDB Cloud Serverless ブランチを管理する方法を学習します。
---

# TiDB Cloudサーバーレス ブランチの管理 {#manage-tidb-cloud-serverless-branches}

このドキュメントでは、 [TiDB Cloudコンソール](https://tidbcloud.com)使用してTiDB Cloud Serverless ブランチを管理する方法について説明します。TiDB TiDB Cloud CLI を使用して管理するには、 [`ticloud branch`](/tidb-cloud/ticloud-branch-create.md)を参照してください。

## 必要なアクセス {#required-access}

-   [ブランチを作成する](#create-a-branch)または[ブランチに接続する](#connect-to-a-branch)実行するには、組織の`Organization Owner`のロールまたは対象プロジェクトの`Project Owner`のロールに所属している必要があります。
-   プロジェクト内のクラスターを[ブランチを表示](#create-a-branch)作成するには、そのプロジェクトに属している必要があります。

権限の詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)参照してください。

## ブランチを作成する {#create-a-branch}

> **注記：**
>
> 2023 年 7 月 5 日以降に作成されたTiDB Cloud Serverless クラスターに対してのみブランチを作成できます。その他の制限については[制限と割り当て](/tidb-cloud/branch-overview.md#limitations-and-quotas)参照してください。

ブランチを作成するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲットのTiDB Cloud Serverless クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ] を**クリックします。
3.  右上隅の**「ブランチの作成」を**クリックします。
4.  ブランチ名を入力し、 **「作成」を**クリックします。

クラスター内のデータ サイズに応じて、ブランチの作成は数分で完了します。

## ブランチをビュー {#view-branches}

クラスターのブランチを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲットのTiDB Cloud Serverless クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ] を**クリックします。

    クラスターのブランチ リストが右側のペインに表示されます。

## ブランチに接続する {#connect-to-a-branch}

ブランチに接続するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲットのTiDB Cloud Serverless クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ] を**クリックします。
3.  接続するターゲット ブランチの行で、 **[アクション]**列の**[...]**をクリックします。
4.  ドロップダウン リストで**[接続] を**クリックします。接続情報のダイアログが表示されます。
5.  ルート パスワードを作成またはリセットするには、 **「パスワードの生成」**または**「パスワードのリセット」**をクリックします。
6.  接続情報を使用してブランチに接続します。

あるいは、クラスターの概要ページから接続文字列を取得することもできます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲットのTiDB Cloud Serverless クラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅の**「接続」を**クリックします。
3.  `Branch`ドロップダウン リストから接続するブランチを選択します。
4.  ルート パスワードを作成またはリセットするには、 **「パスワードの生成」**または**「パスワードのリセット」**をクリックします。
5.  接続情報を使用してブランチに接続します。

## ブランチを削除する {#delete-a-branch}

ブランチを削除するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲットのTiDB Cloud Serverless クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ] を**クリックします。
3.  削除するターゲット ブランチの行で、 **[アクション]**列の**[...]**をクリックします。
4.  ドロップダウンリストで**「削除」を**クリックします。
5.  削除を確認します。

## 次は何か {#what-s-next}

-   [TiDB Cloud Serverless ブランチを GitHub CI/CD パイプラインに統合する](/tidb-cloud/branch-github-integration.md)
