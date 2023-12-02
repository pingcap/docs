---
title: Integrate TiDB Serverless Branching (Beta) with GitHub 
summary: Learn how to integrate the TiDB Serverless branching feature with GitHub.
---

# TiDB サーバーレス ブランチング (ベータ版) を GitHub と統合する {#integrate-tidb-serverless-branching-beta-with-github}

> **注記：**
>
> 統合は[TiDB サーバーレス分岐](/tidb-cloud/branch-overview.md)に基づいて構築されます。このドキュメントを読む前に、TiDB サーバーレス分岐について十分に理解してください。

アプリケーション開発に GitHub を使用する場合、TiDB サーバーレス ブランチを GitHub CI/CD パイプラインに統合できます。これにより、本番データベースに影響を与えることなく、ブランチを使用してプル リクエストを自動的にテストできます。

統合プロセスでは、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching) GitHub アプリをインストールするように求められます。このアプリは、GitHub リポジトリ内のプル リクエストに従って TiDB サーバーレス ブランチを自動的に管理できます。たとえば、プル リクエストを作成すると、アプリは TiDB サーバーレス クラスターに対応するブランチを作成します。そこでは、本番データベースに影響を与えることなく、独立して新機能やバグ修正に取り組むことができます。

このドキュメントでは次のトピックについて説明します。

1.  TiDB サーバーレス ブランチングを GitHub と統合する方法
2.  TiDB Cloud Branching アプリはどのように機能しますか
3.  本番クラスターではなくブランチを使用してすべてのプルリクエストをテストするブランチベースの CI ワークフローを構築する方法

## あなたが始める前に {#before-you-begin}

統合する前に、次のものが揃っていることを確認してください。

-   GitHub アカウント
-   アプリケーションの GitHub リポジトリ
-   [TiDB サーバーレスクラスター](/tidb-cloud/create-tidb-cluster-serverless.md)

## TiDB サーバーレス ブランチングを GitHub リポジトリと統合する {#integrate-tidb-serverless-branching-with-your-github-repository}

TiDB サーバーレス ブランチングを GitHub リポジトリと統合するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット TiDB サーバーレス クラスターの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーション ペインで**[ブランチ]**をクリックします。

3.  **「ブランチ」**ページの右上隅にある**「GitHub に接続」を**クリックします。

    -   GitHub にログインしていない場合は、まず GitHub にログインするように求められます。
    -   初めて統合を使用する場合は、 **TiDB Cloud Branching**アプリを承認するように求められます。

    <img src="https://download.pingcap.com/images/docs/tidb-cloud/branch/github-authorize.png" width="80%" />

4.  **「GitHub に接続」**ダイアログで、「 **GitHub アカウント」**ドロップダウン リストから GitHub アカウントを選択します。

    アカウントがリストに存在しない場合は、 **[他のアカウントのインストール]**をクリックし、画面の指示に従ってアカウントをインストールします。

5.  **[GitHub リポジトリ]**ドロップダウン リストでターゲット リポジトリを選択します。リストが長い場合は、名前を入力してリポジトリを検索できます。

6.  **[接続]**をクリックして、TiDB サーバーレス クラスターと GitHub リポジトリの間に接続します。

    <img src="https://download.pingcap.com/images/docs/tidb-cloud/branch/github-connect.png" width="40%" />

## TiDB Cloud Branching アプリの動作 {#tidb-cloud-branching-app-behaviors}

TiDB サーバーレス クラスターを GitHub リポジトリに接続すると、このリポジトリ内のプル リクエストごとに、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching) GitHub アプリが対応する TiDB サーバーレス ブランチを自動的に管理できるようになります。以下に、プル リクエストの変更に対するデフォルトの動作を示します。

| プルリクエストの変更             | TiDB Cloud Branching アプリの動作                                                                                                                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| プルリクエストを作成する           | リポジトリでプル リクエストを作成すると、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)アプリは TiDB サーバーレス クラスターのブランチを作成します。ブランチ名は`${github_branch_name}_${pr_id}_${commit_sha}`形式です。ブランチの数が[限界](/tidb-cloud/branch-overview.md#limitations-and-quotas)であることに注意してください。 |
| 新しいコミットをプルリクエストにプッシュする | リポジトリ内のプル リクエストに新しいコミットをプッシュするたびに、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)アプリは以前の TiDB サーバーレス ブランチを削除し、最新のコミット用に新しいブランチを作成します。                                                                                                            |
| プルリクエストを閉じるかマージする      | プル リクエストを閉じるかマージすると、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)アプリはこのプル リクエストのブランチを削除します。                                                                                                                                                    |
| プルリクエストを再度オープンする       | プル リクエストを再度開くと、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)アプリはプル リクエストの最後に行われたコミットのブランチを作成します。                                                                                                                                               |

## TiDB Cloud Branching アプリを構成する {#configure-tidb-cloud-branching-app}

[TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)アプリの動作を構成するには、 `tidbcloud.yml`ファイルをリポジトリのルート ディレクトリに追加し、次の手順に従ってこのファイルに必要な構成を追加します。

### ブランチ.ブロックリスト {#branch-blocklist}

**タイプ:**文字列の配列。**デフォルト:** `[]` 。

`allowList`にある場合でも、 TiDB Cloud Branching アプリを禁止する GitHub ブランチを指定します。

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

### ブランチ.autoReserved {#branch-autoreserved}

**タイプ:**ブール値。**デフォルト:** `false` 。

これが`true`に設定されている場合、 TiDB Cloud Branching アプリは、前のコミットで作成された TiDB サーバーレス ブランチを削除しません。

```yaml
github:
    branch:
        autoReserved: false
```

### ブランチ.autoDestroy {#branch-autodestroy}

**タイプ:**ブール値。**デフォルト:** `true` 。

これが`false`に設定されている場合、 TiDB Cloud Branching アプリは、プル リクエストが閉じられるかマージされるときに TiDB サーバーレス ブランチを削除しません。

```yaml
github:
    branch:
        autoDestroy: true
```

## 分岐 CI ワークフローを作成する {#create-a-branching-ci-workflow}

ブランチを使用するためのベスト プラクティスの 1 つは、ブランチ CI ワークフローを作成することです。このワークフローを使用すると、プル リクエストをマージする前に、本番クラスターを使用する代わりに TiDB サーバーレス ブランチを使用してコードをテストできます。ライブデモを見つけることができます[ここ](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example) 。

ワークフローを作成する主な手順は次のとおりです。

1.  [TiDB サーバーレス ブランチングを GitHub リポジトリと統合する](#integrate-tidb-serverless-branching-with-your-github-repository) 。

2.  ブランチ接続情報を取得します。

    [tidbcloud ブランチを待つ](https://github.com/tidbcloud/wait-for-tidbcloud-branch)アクションを使用して、TiDB サーバーレス ブランチの準備が完了するまで待機し、ブランチの接続情報を取得できます。

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

3.  テストコードを変更します。

    GitHub Actions からの接続情報を受け入れるようにテスト コードを変更します。たとえば、 [ライブデモ](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)で示すように、環境を通じて接続情報を受け入れることができます。

## 次は何ですか {#what-s-next}

分岐 GitHub 統合を使用せずに分岐 CI/CD ワークフローを構築することもできます。たとえば、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)と GitHub Actions を使用して CI/CD ワークフローをカスタマイズできます。
