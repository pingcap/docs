---
title: Integrate TiDB Cloud Serverless Branching (Beta) with GitHub 
summary: TiDB Cloud Serverless ブランチ機能を GitHub と統合する方法を学びます。
---

# TiDB Cloud Serverless Branching（ベータ版）をGitHubと統合する {#integrate-tidb-cloud-serverless-branching-beta-with-github}

> **注記：**
>
> この統合は[TiDB Cloudサーバーレスブランチ](/tidb-cloud/branch-overview.md)に基づいて構築されています。このドキュメントを読む前に、 TiDB Cloud Serverless ブランチングについて理解しておいてください。

アプリケーション開発に GitHub を使用する場合は、 TiDB Cloud Serverless ブランチを GitHub CI/CD パイプラインに統合できます。これにより、本番データベースに影響を与えることなく、ブランチを使用してプル リクエストを自動的にテストできます。

統合プロセスでは、GitHub App [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)をインストールするように求められます。このアプリは、GitHub リポジトリ内のプルリクエストに基づいてTiDB Cloud Serverless のブランチを自動的に管理できます。例えば、プルリクエストを作成すると、アプリはTiDB Cloud Serverless クラスターに対応するブランチを作成します。このブランチでは、本番のデータベースに影響を与えることなく、新機能やバグ修正に個別に取り組むことができます。

このドキュメントでは、次のトピックについて説明します。

1.  TiDB Cloud ServerlessブランチをGitHubと統合する方法
2.  TiDB Cloudブランチアプリはどのように機能しますか？
3.  本番のクラスタではなくブランチを使用してすべてのプルリクエストをテストするためのブランチベースの CI ワークフローを構築する方法

## 始める前に {#before-you-begin}

統合する前に、次のものを用意してください。

-   GitHubアカウント
-   アプリケーション用のGitHubリポジトリ
-   A [TiDB Cloudサーバーレス クラスター](/tidb-cloud/create-tidb-cluster-serverless.md)

## TiDB Cloud ServerlessブランチをGitHubリポジトリに統合する {#integrate-tidb-cloud-serverless-branching-with-your-github-repository}

TiDB Cloud Serverless ブランチを GitHub リポジトリに統合するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットのTiDB Cloud Serverless クラスターの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。

3.  **「ブランチ」**ページの右上隅にある**「GitHub に接続」を**クリックします。

    -   GitHub にログインしていない場合は、まず GitHub にログインするように求められます。
    -   統合を初めて使用する場合は、 **TiDB Cloud Branching**アプリを承認するように求められます。

    <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/branch/github-authorize.png" width="80%" />

4.  **「GitHub に接続」**ダイアログで、 **「GitHub アカウント」**ドロップダウン リストから GitHub アカウントを選択します。

    リストに自分のアカウントが存在しない場合は、 **[その他のアカウントのインストール]**をクリックし、画面の指示に従ってアカウントをインストールします。

5.  **GitHubリポジトリの**ドロップダウンリストから対象のリポジトリを選択します。リストが長い場合は、名前を入力してリポジトリを検索できます。

6.  **「接続」**をクリックして、 TiDB Cloud Serverless クラスターと GitHub リポジトリを接続します。

    <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/branch/github-connect.png" width="40%" />

## TiDB Cloudブランチングアプリの動作 {#tidb-cloud-branching-app-behaviors}

TiDB Cloud Serverless クラスターを GitHub リポジトリに接続すると、このリポジトリ内の各プルリクエストに対して、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching) GitHub App が対応するTiDB Cloud Serverless ブランチを自動的に管理できるようになります。プルリクエストの変更に対するデフォルトの動作は次のとおりです。

| プルリクエストの変更             | TiDB Cloudブランチングアプリの動作                                                                                                                                                                                                                                                                                                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| プルリクエストを作成する           | リポジトリにプルリクエストを作成すると、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)アプリがTiDB Cloud Serverless クラスターのブランチを作成します。 `branch.mode` `reset`に設定されている場合、ブランチ名は`${github_branch_name}_${pr_id}`形式に従います。 `branch.mode` `reserve`に設定されている場合、ブランチ名は`${github_branch_name}_${pr_id}_${commit_sha}`形式に従います。ブランチの数には[制限](/tidb-cloud/branch-overview.md#limitations-and-quotas)が含まれることに注意してください。 |
| 新しいコミットをプルリクエストにプッシュする | `branch.mode` `reset`に設定すると、リポジトリ内のプルリクエストに新しいコミットをプッシュするたびに、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)アプリはTiDB Cloud Serverless ブランチをリセットします。 `branch.mode` `reserve`に設定すると、アプリは最新のコミット用に新しいブランチを作成します。                                                                                                                                                                    |
| プルリクエストをクローズまたはマージする   | プル リクエストをクローズまたはマージすると、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)アプリによってこのプル リクエストのブランチが削除されます。                                                                                                                                                                                                                                                                             |
| プルリクエストを再開する           | プル リクエストを再度開くと、 [TiDB Cloudブランチ](https://github.com/apps/tidb-cloud-branching)アプリによってプル リクエストの最後のコミットのブランチが作成されます。                                                                                                                                                                                                                                                                               |

## TiDB Cloud Branchingアプリを構成する {#configure-tidb-cloud-branching-app}

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

### ブランチ.許可リスト {#branch-allowlist}

**タイプ:**文字列の配列。**デフォルト:** `[.*]` 。

TiDB Cloud Branching アプリを許可する GitHub ブランチを指定します。

```yaml
github:
    branch:
        allowList:
            - ".*_db"
```

### ブランチモード {#branch-mode}

**タイプ:**文字列。**デフォルト:** `reset` 。

TiDB Cloud Branching アプリがブランチの更新を処理する方法を指定します。

-   `reset`に設定すると、 TiDB Cloud Branching アプリは既存のブランチを最新のデータで更新します。
-   `reserve`に設定すると、 TiDB Cloud Branching アプリは最新のコミット用に新しいブランチを作成します。

```yaml
github:
    branch:
        mode: reset
```

### ブランチ.自動破棄 {#branch-autodestroy}

**タイプ:**ブール値。**デフォルト:** `true` 。

`false`に設定すると、プル リクエストがクローズまたはマージされたときに、 TiDB Cloud Branching アプリはTiDB Cloud Serverless ブランチを削除しません。

```yaml
github:
    branch:
        autoDestroy: true
```

## ブランチCIワークフローを作成する {#create-a-branching-ci-workflow}

ブランチを使用するベストプラクティスの一つは、ブランチCIワークフローを作成することです。このワークフローを使用すると、プルリクエストをマージする前に、本番クラスタではなくTiDB Cloud Serverlessブランチを使用してコードをテストできます。ライブデモ[ここ](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)ご覧ください。

ワークフローを作成する主な手順は次のとおりです。

1.  [TiDB Cloud ServerlessブランチをGitHubリポジトリに統合する](#integrate-tidb-cloud-serverless-branching-with-your-github-repository) 。

2.  ブランチ接続情報を取得します。

    [tidbcloud-branch を待つ](https://github.com/tidbcloud/wait-for-tidbcloud-branch)アクションを使用して、 TiDB Cloud Serverless ブランチの準備が整うまで待機し、ブランチの接続情報を取得できます。

    使用例:

    ```yaml
    steps:
      - name: Wait for TiDB Cloud Serverless branch to be ready
        uses: tidbcloud/wait-for-tidbcloud-branch@v0
        id: wait-for-branch
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          public-key: ${{ secrets.TIDB_CLOUD_API_PUBLIC_KEY }}
          private-key: ${{ secrets.TIDB_CLOUD_API_PRIVATE_KEY }}

      - name: Test with TiDB Cloud Serverless branch
         run: |
            echo "The host is ${{ steps.wait-for-branch.outputs.host }}"
            echo "The user is ${{ steps.wait-for-branch.outputs.user }}"
            echo "The password is ${{ steps.wait-for-branch.outputs.password }}"
    ```

    -   `token` : GitHubは自動的に[GITHUB_トークン](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)シークレットを作成します。そのまま使用できます。
    -   `public-key`および`private-key` : TiDB Cloud[APIキー](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management) 。

3.  テストコードを変更します。

    テストコードを修正し、GitHub Actionsからの接続情報を受け入れるようにします。例えば、 [ライブデモ](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)に示すように、環境を通して接続情報を受け入れることができます。

## 次は何？ {#what-s-next}

次の例を使用して、ブランチング GitHub 統合の使用方法を学習します。

-   [分岐-gorm-例](https://github.com/tidbcloud/branching-gorm-example)
-   [分岐-Django-例](https://github.com/tidbcloud/branching-django-example)
-   [分岐レールの例](https://github.com/tidbcloud/branching-rails-example)

ブランチング GitHub 統合を使わずに、ブランチング CI/CD ワークフローを構築することもできます。例えば、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)と GitHub Actions を使用して CI/CD ワークフローをカスタマイズできます。
