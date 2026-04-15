---
title: Integrate TiDB Cloud Branching (Beta) with GitHub 
summary: TiDB Cloudのブランチ機能をGitHubと連携させる方法を学びましょう。
---

# TiDB Cloud Branching（ベータ版）とGitHubの統合 {#integrate-tidb-cloud-branching-beta-with-github}

> **注記：**
>
> この統合は[TiDB Cloudブランチング](/tidb-cloud/branch-overview.md)ベースに構築されています。このドキュメントを読む前に、 TiDB Cloud Branching について理解していることを確認してください。

アプリケーション開発にGitHubを使用している場合、 TiDB Cloud BranchingをGitHubのCI/CDパイプラインに統合することで、本番データベースに影響を与えることなく、ブランチを使用したプルリクエストを自動的にテストできます。

統合プロセスでは、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)GitHub アプリのインストールを求められます。このアプリは、GitHub リポジトリのプルリクエストに基づいて、 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのブランチを自動的に管理できます。たとえば、プルリクエストを作成すると、アプリはTiDB Cloud StarterまたはEssentialインスタンスに対応するブランチを作成します。このブランチでは、本番データベースに影響を与えることなく、新機能の開発やバグ修正を個別に行うことができます。

この文書では、以下のトピックについて説明します。

1.  TiDB Cloud BranchingをGitHubと統合する方法
2.  TiDB Cloud Branchingアプリはどのように動作しますか？
3.  本番のTiDB Cloud StarterまたはEssentialインスタンスではなく、ブランチを使用してすべてのプルリクエストをテストするブランチベースのCIワークフローを構築する方法

## 始める前に {#before-you-begin}

統合を行う前に、以下のものがすべて揃っていることを確認してください。

-   GitHubアカウント
-   アプリケーション用のGitHubリポジトリ
-   [TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンス](/tidb-cloud/create-tidb-cluster-serverless.md)

## TiDB Cloud BranchingをGitHubリポジトリと統合する {#integrate-branching-with-your-github-repository} {#integrate-branching-with-your-github-repository}

TiDB Cloud BranchingをGitHubリポジトリと統合するには、以下の手順に従ってください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで**「支店」**をクリックします。

3.  **ブランチ**ページの右上隅にある**「GitHubに接続」**をクリックします。

    -   GitHubにログインしていない場合は、まずGitHubにログインするよう求められます。
    -   初めてこの連携機能を使用する場合は、 **TiDB Cloud Branching**アプリの認証を求められます。

    <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/branch/github-authorize.png" width="80%" />

4.  **「GitHubに接続」**ダイアログで、 **「GitHubアカウント」**ドロップダウンリストからGitHubアカウントを選択します。

    リストにあなたのアカウントが存在しない場合は、 **「他のアカウントをインストール」**をクリックし、画面の指示に従ってアカウントをインストールしてください。

5.  **GitHubリポジトリの**ドロップダウンリストから、対象のリポジトリを選択してください。リストが長い場合は、リポジトリ名を入力して検索することもできます。

6.  **「接続」**をクリックすると、 TiDB Cloud StarterまたはEssentialインスタンスとGitHubリポジトリが接続されます。

    <img src="https://docs-download.pingcap.com/media/images/docs/tidb-cloud/branch/github-connect.png" width="40%" />

## TiDB Cloudのブランチングアプリの動作 {#tidb-cloud-branching-app-behaviors}

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを GitHub リポジトリに接続すると、このリポジトリ内の各プルリクエストに対して、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)GitHub アプリは、 TiDB Cloud StarterまたはEssentialインスタンスに対応するブランチを自動的に管理できます。プルリクエストの変更に関するデフォルトの動作は次のとおりです。

| プルリクエストの変更             | TiDB Cloudのブランチングアプリの動作                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| プルリクエストを作成する           | リポジトリでプルリクエストを作成すると、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)アプリは、 TiDB Cloud StarterまたはEssentialインスタンス用のブランチを作成します。 `branch.mode`が`reset`に設定されている場合、ブランチ名は`${github_branch_name}_${pr_id}`の形式に従います。 `branch.mode`が`reserve`に設定されている場合、ブランチ名は`${github_branch_name}_${pr_id}_${commit_sha}`の形式に従います。ブランチの数には が[制限](/tidb-cloud/branch-overview.md#limitations-and-quotas)ことに注意してください。 |
| プルリクエストに新しいコミットをプッシュする | `branch.mode`が`reset`に設定されている場合、リポジトリのプルリクエストに新しいコミットをプッシュするたびに、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)アプリはブランチをリセットします。 `branch.mode`が`reserve`に設定されている場合、アプリは最新のコミット用に新しいブランチを作成します。                                                                                                                                                                                              |
| プルリクエストを閉じるかマージする      | プルリクエストを閉じたりマージしたりすると、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)アプリはこのプルリクエストのブランチを削除します。                                                                                                                                                                                                                                                                                              |
| プルリクエストを再開する           | プルリクエストを再開すると、 [TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)アプリはプルリクエストの最後のコミットのブランチを作成します。                                                                                                                                                                                                                                                                                                |

## TiDB Cloud Branchingアプリの設定 {#configure-tidb-cloud-branching-app}

[TiDB Cloudブランチング](https://github.com/apps/tidb-cloud-branching)の動作を設定するには リポジトリのルートディレクトリに`tidbcloud.yml`ファイルを追加し、以下の手順に従って必要な設定をこのファイルに追加します。

### ブランチブロックリスト {#branch-blocklist}

**型:**文字列の配列。**デフォルト:** `[]` 。

TiDB Cloud Branching アプリを禁止する GitHub ブランチを指定します。たとえそれらが`allowList`内にある場合でも同様です。

```yaml
github:
    branch:
        blockList:
            - ".*_doc"
            - ".*_blackList"
```

### ブランチ.allowList {#branch-allowlist}

**型:**文字列の配列。**デフォルト:** `[.*]` 。

TiDB Cloud Branchingアプリを許可するGitHubブランチを指定してください。

```yaml
github:
    branch:
        allowList:
            - ".*_db"
```

### ブランチモード {#branch-mode}

**型:**文字列。**デフォルト:** `reset` 。

TiDB Cloud Branchingアプリがブランチの更新をどのように処理するかを指定します。

-   `reset`に設定されている場合、 TiDB Cloud Branching アプリは既存のブランチを最新のデータで更新します。
-   `reserve`に設定されている場合、 TiDB Cloud Branching アプリは最新のコミット用に新しいブランチを作成します。

```yaml
github:
    branch:
        mode: reset
```

### ブランチ.自動破棄 {#branch-autodestroy}

**型:**ブール値。**デフォルト:** `true` 。

`false`に設定されている場合、プルリクエストがクローズまたはマージされたときに、 TiDB Cloud Branching アプリはTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのブランチを削除しません。

```yaml
github:
    branch:
        autoDestroy: true
```

## 分岐型CIワークフローを作成する {#create-a-branching-ci-workflow}

ブランチを活用するためのベストプラクティスの1つは、ブランチングCIワークフローを作成することです。このワークフローを使用すると、プルリクエストをマージする前に、本番インスタンス自体を使用する代わりに、 TiDB Cloud StarterまたはEssentialインスタンスのブランチを使用してコードをテストできます。ライブデモは[ここ](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)ご覧ください。

ワークフローを作成するための主な手順は以下のとおりです。

1.  [TiDB Cloud BranchingをGitHubリポジトリと統合する](#integrate-branching-with-your-github-repository)。

2.  支店の接続情報を取得します。

    [wait-for-tidbcloud-branch](https://github.com/tidbcloud/wait-for-tidbcloud-branch)アクションを使用すると、ブランチの準備が整うまで待機し、ブランチの接続情報を取得できます。

    TiDB Cloud Starterインスタンスのブランチを例にとると、次のようになります。

    ```yaml
    steps:
      - name: Wait for TiDB Cloud Starter branch to be ready
        uses: tidbcloud/wait-for-tidbcloud-branch@v0
        id: wait-for-branch
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          public-key: ${{ secrets.TIDB_CLOUD_API_PUBLIC_KEY }}
          private-key: ${{ secrets.TIDB_CLOUD_API_PRIVATE_KEY }}

      - name: Test with TiDB Cloud Starter branch
         run: |
            echo "The host is ${{ steps.wait-for-branch.outputs.host }}"
            echo "The user is ${{ steps.wait-for-branch.outputs.user }}"
            echo "The password is ${{ steps.wait-for-branch.outputs.password }}"
    ```

    -   `token` : GitHub が自動的に[GitHubトークン](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)を作成します。そのまま使用できます。
    -   `public-key`および`private-key` : TiDB Cloud [APIキー](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)。

3.  テストコードを修正してください。

    テストコードを修正して、GitHub Actions からの接続情報を受け入れるようにしてください。たとえば、 [ライブデモ](https://github.com/shiyuhang0/tidbcloud-branch-gorm-example)で示されているように、環境を介して接続情報を受け入れることができます。

## 次は？ {#what-s-next}

以下の例を通して、ブランチング機能を備えたGitHub連携の使い方を学びましょう。

-   [分岐GORMの例](https://github.com/tidbcloud/branching-gorm-example)
-   [分岐するDjangoの例](https://github.com/tidbcloud/branching-django-example)
-   [分岐レールの例](https://github.com/tidbcloud/branching-rails-example)

ブランチングGitHubとの連携機能を使わずに、ブランチングCI/CDワークフローを構築することも可能です。例えば、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)とGitHub Actionsを使用して、CI/CDワークフローをカスタマイズできます。
