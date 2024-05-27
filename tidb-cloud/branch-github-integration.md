---
title: Integrate TiDB Serverless Branching (Beta) with GitHub 
summary: TiDB サーバーレス ブランチ機能を GitHub と統合する方法を学びます。
---

# TiDB サーバーレス ブランチング (ベータ版) を GitHub と統合する {#integrate-tidb-serverless-branching-beta-with-github}

> **注記：**
>
> 統合は[TiDB サーバーレスブランチ](/tidb-cloud/branch-overview.md)に基づいて構築されています。このドキュメントを読む前に、TiDB Serverless ブランチングについて理解していることを確認してください。

アプリケーション開発に GitHub を使用する場合は、TiDB Serverless ブランチを GitHub CI/CD パイプラインに統合できます。これにより、本番データベースに影響を与えることなく、ブランチを使用してプル リクエストを自動的にテストできます。

統合プロセスでは、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching) GitHub アプリをインストールするように求められます。このアプリは、GitHub リポジトリのプル リクエストに従って TiDB Serverless ブランチを自動的に管理できます。たとえば、プル リクエストを作成すると、アプリは TiDB Serverless クラスターの対応するブランチを作成します。このブランチでは、本番データベースに影響を与えることなく、新機能やバグ修正を個別に行うことができます。

このドキュメントでは、次のトピックについて説明します。

1.  TiDB サーバーレス ブランチを GitHub と統合する方法
2.  TiDB Cloudブランチングアプリはどのように機能しますか
3.  本番のクラスターではなくブランチを使用してすべてのプルリクエストをテストするためのブランチベースの CI ワークフローを構築する方法

## あなたが始める前に {#before-you-begin}

統合する前に、次のものを用意してください。

-   GitHubアカウント
-   アプリケーション用のGitHubリポジトリ
-   [TiDB サーバーレス クラスター](/tidb-cloud/create-tidb-cluster-serverless.md)

## TiDB サーバーレス ブランチを GitHub リポジトリに統合する {#integrate-tidb-serverless-branching-with-your-github-repository}

TiDB Serverless ブランチを GitHub リポジトリに統合するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲットの TiDB Serverless クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ペインで**[ブランチ] を**クリックします。

3.  **「ブランチ」**ページの右上隅にある**「GitHub に接続」を**クリックします。

    -   GitHub にログインしていない場合は、まず GitHub にログインするように求められます。
    -   統合を初めて使用する場合は、 **TiDB Cloud Branching**アプリを承認するように求められます。

    <img src="https://download.pingcap.com/images/docs/tidb-cloud/branch/github-authorize.png" width="80%" />

4.  **「GitHub に接続」**ダイアログで、 **「GitHub アカウント」**ドロップダウン リストから GitHub アカウントを選択します。

    アカウントがリストに存在しない場合は、 **「その他のアカウントのインストール」**をクリックし、画面の指示に従ってアカウントをインストールします。

5.  **GitHub リポジトリ**のドロップダウン リストでターゲット リポジトリを選択します。リストが長い場合は、名前を入力してリポジトリを検索できます。

6.  **「接続」**をクリックして、TiDB Serverless クラスターと GitHub リポジトリを接続します。

    <img src="https://download.pingcap.com/images/docs/tidb-cloud/branch/github-connect.png" width="40%" />

## TiDB Cloudブランチングアプリの動作 {#tidb-cloud-branching-app-behaviors}

TiDB Serverless クラスターを GitHub リポジトリに接続すると、このリポジトリ内の各プル リクエストに対して、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching) GitHub App が対応する TiDB Serverless ブランチを自動的に管理できるようになります。プル リクエストの変更に対するデフォルトの動作を次に示します。

| プルリクエストの変更             | TiDB Cloudブランチングアプリの動作                                                                                                                                                                                                                                                       |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| プルリクエストを作成する           | リポジトリにプル リクエストを作成すると、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)アプリによって TiDB Serverless クラスターのブランチが作成されます。ブランチ名は`${github_branch_name}_${pr_id}_${commit_sha}`形式です。ブランチの数には[制限](/tidb-cloud/branch-overview.md#limitations-and-quotas)含まれていることに注意してください。 |
| 新しいコミットをプルリクエストにプッシュする | リポジトリ内のプル リクエストに新しいコミットをプッシュするたびに、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)アプリは以前の TiDB Serverless ブランチを削除し、最新のコミット用の新しいブランチを作成します。                                                                                                                    |
| プルリクエストをクローズまたはマージする   | プル リクエストをクローズまたはマージすると、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)アプリによってこのプル リクエストのブランチが削除されます。                                                                                                                                                         |
| プルリクエストを再開する           | プル リクエストを再度開くと、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)アプリによってプル リクエストの最新のコミットのブランチが作成されます。                                                                                                                                                           |

## TiDB Cloud Branching アプリを構成する {#configure-tidb-cloud-branching-app}

[TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)アプリの動作を構成するには、リポジトリのルート ディレクトリに`tidbcloud.yml`ファイルを追加し、次の手順に従ってこのファイルに必要な構成を追加します。

### ブランチ.ブロックリスト {#branch-blocklist}

**タイプ:**文字列の配列。**デフォルト:** `[]` 。

`allowList`内にある場合でも、 TiDB Cloud Branching アプリを禁止する GitHub ブランチを指定します。

```yaml
github:
    branch:
        blockList:
            - ".*_doc"
            - ".*_blackList"
```

### ブランチ.allowList {#branch-allowlist}

**タイプ:**文字列の配列。**デフォルト:** `[.*]` 。

TiDB Cloud Branching アプリを許可する GitHub ブランチを指定します。

```yaml
github:
    branch:
        allowList:
            - ".*_db"
```

### ブランチ.自動予約 {#branch-autoreserved}

**タイプ:**ブール値。**デフォルト:** `false` 。

`true`に設定すると、 TiDB Cloud Branching アプリは、前のコミットで作成された TiDB Serverless ブランチを削除しません。

```yaml
github:
    branch:
        autoReserved: false
```

### ブランチ.自動破棄 {#branch-autodestroy}

**タイプ:**ブール値。**デフォルト:** `true` 。

`false`に設定すると、プル リクエストがクローズまたはマージされたときに、 TiDB Cloud Branching アプリは TiDB Serverless ブランチを削除しません。

```yaml
github:
    branch:
        autoDestroy: true
```

## 分岐CIワークフローを作成する {#create-a-branching-ci-workflow}

ブランチを使用するベスト プラクティスの 1 つは、ブランチ CI ワークフローを作成することです。このワークフローを使用すると、プル リクエストをマージする前に、本番クラスターを使用する代わりに、TiDB Serverless ブランチを使用してコードをテストできます。ライブ デモ[ここ](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)を参照してください。

ワークフローを作成する主な手順は次のとおりです。

1.  [TiDB サーバーレス ブランチを GitHub リポジトリに統合する](#integrate-tidb-serverless-branching-with-your-github-repository) 。

2.  ブランチ接続情報を取得します。

    [tidbcloud ブランチを待つ](https://github.com/tidbcloud/wait-for-tidbcloud-branch)アクションを使用して、TiDB Serverless ブランチの準備が完了するまで待機し、ブランチの接続情報を取得できます。

    使用例:

    ```yaml
    steps:
      - name: Wait for TiDB Serverless branch to be ready
        uses: tidbcloud/wait-for-tidbcloud-branch@v0
        id: wait-for-branch
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          public-key: ${{ secrets.TIDB_CLOUD_API_PUBLIC_KEY }}
          private-key: ${{ secrets.TIDB_CLOUD_API_PRIVATE_KEY }}

      - name: Test with TiDB Serverless branch
         run: |
            echo "The host is ${{ steps.wait-for-branch.outputs.host }}"
            echo "The user is ${{ steps.wait-for-branch.outputs.user }}"
            echo "The password is ${{ steps.wait-for-branch.outputs.password }}"
    ```

    -   `token` : GitHub は自動的に[トークン](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)シークレットを作成します。これを直接使用できます。
    -   `public-key`および`private-key` : TiDB Cloud[APIキー](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management) 。

3.  テストコードを変更します。

    GitHub Actions からの接続情報を受け入れるようにテスト コードを変更します。たとえば、 [ライブデモ](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)に示すように、環境を通じて接続情報を受け入れることができます。

## 次は何ですか {#what-s-next}

次の例を使用して、ブランチング GitHub 統合の使用方法を学習します。

-   [分岐-ゴーム-例](https://github.com/tidbcloud/branching-gorm-example)
-   [分岐-Django-例](https://github.com/tidbcloud/branching-django-example)
-   [分岐レールの例](https://github.com/tidbcloud/branching-rails-example)

ブランチング GitHub 統合を使用せずに、ブランチング CI/CD ワークフローを構築することもできます。たとえば、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)と GitHub Actions を使用して CI/CD ワークフローをカスタマイズできます。
