---
title: Manage TiDB Serverless Branches
summary: Learn How to manage TiDB Serverless branches.
---

# TiDB サーバーレス ブランチの管理 {#manage-tidb-serverless-branches}

このドキュメントでは、 [TiDB Cloudコンソール](https://tidbcloud.com)を使用して TiDB サーバーレス ブランチを管理する方法について説明します。 TiDB Cloud CLI を使用して管理するには、 [`ticloud branch`](/tidb-cloud/ticloud-branch-create.md)を参照してください。

## 必要なアクセス {#required-access}

-   [ブランチを作成する](#create-a-branch)または[ブランチに接続する](#connect-to-a-branch)を行うには、組織の`Organization Owner`役割、または対象プロジェクトの`Project Owner`役割に属している必要があります。
-   プロジェクト内のクラスターの[ブランチを表示する](#create-a-branch)は、そのプロジェクトに属している必要があります。

権限の詳細については、 [ユーザーの役割](/tidb-cloud/manage-user-access.md#user-roles)を参照してください。

## ブランチを作成する {#create-a-branch}

> **注記：**
>
> 2023 年 7 月 5 日以降に作成された TiDB サーバーレス クラスターのブランチのみを作成できます。その他の制限事項については、 [制限と割り当て](/tidb-cloud/branch-overview.md#limitations-and-quotas)を参照してください。

ブランチを作成するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット TiDB サーバーレス クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。
3.  右上隅にある**「ブランチの作成」**をクリックします。
4.  ブランチ名を入力し、 **[作成]**をクリックします。

クラスター内のデータ サイズに応じて、ブランチの作成は数分で完了します。

## ブランチをビュー {#view-branches}

クラスターのブランチを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット TiDB サーバーレス クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。

    クラスターのブランチリストが右側のペインに表示されます。

## ブランチに接続する {#connect-to-a-branch}

ブランチに接続するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット TiDB サーバーレス クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。
3.  接続するターゲット ブランチの行で、 **[アクション]**列の**[...]**をクリックします。
4.  ドロップダウン リストで**[接続]**をクリックします。接続情報のダイアログが表示されます。
5.  **「パスワードの生成」**または**「パスワードのリセット」**をクリックして、root パスワードを作成またはリセットします。
6.  接続情報を使用してブランチに接続します。

あるいは、クラスターの概要ページから接続文字列を取得できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット TiDB サーバーレス クラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅にある**「接続」**をクリックします。
3.  `Branch`ドロップダウン リストで接続するブランチを選択します。
4.  **「パスワードの生成」**または**「パスワードのリセット」**をクリックして、root パスワードを作成またはリセットします。
5.  接続情報を使用してブランチに接続します。

## ブランチを削除する {#delete-a-branch}

ブランチを削除するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット TiDB サーバーレス クラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。
3.  削除するターゲット ブランチの行で、 **[アクション]**列の**[...]**をクリックします。
4.  ドロップダウン リストで**[削除]**をクリックします。
5.  削除を確認します。

## 次は何ですか {#what-s-next}

-   [TiDB サーバーレス ブランチを GitHub CI/CD パイプラインに統合](/tidb-cloud/branch-github-integration.md)
