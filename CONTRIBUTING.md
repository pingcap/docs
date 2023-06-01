# TiDB ドキュメント貢献ガイド {#tidb-documentation-contributing-guide}

[<a href="https://github.com/pingcap/tidb">TiDB</a>](https://github.com/pingcap/tidb)ドキュメントへようこそ!私たちは、あなたが[<a href="https://github.com/pingcap/community/">TiDB コミュニティ</a>](https://github.com/pingcap/community/)に参加してくれることを楽しみにしています。

## あなたが貢献できること {#what-you-can-contribute}

[<a href="https://docs.pingcap.com/tidb/stable">PingCAP Web サイトの TiDB ドキュメント</a>](https://docs.pingcap.com/tidb/stable)を改善するには、次のいずれかの項目から始めることができます。

-   タイプミスやフォーマット (句読点、スペース、インデント、コード ブロックなど) を修正します。
-   不適切または古い説明を修正または更新する
-   不足しているコンテンツ (文、段落、または新しいドキュメント) を追加します。
-   ドキュメントの変更を英語から中国語に翻訳する
-   送信、返信、解決[<a href="https://github.com/pingcap/docs/issues">ドキュメントの問題</a>](https://github.com/pingcap/docs/issues)
-   (上級) 他の人が作成したプル リクエストを確認する

## 貢献する前に {#before-you-contribute}

貢献する前に、TiDB ドキュメントのメンテナンスに関する一般情報を簡単に読んでください。これは、すぐに貢献者になるのに役立ちます。

### スタイルに慣れる {#get-familiar-with-style}

-   [<a href="https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message">コミットメッセージのスタイル</a>](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)
-   [<a href="https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style">プルリクエストのタイトルスタイル</a>](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)
-   [<a href="/resources/markdownlint-rules.md">マークダウンルール</a>](/resources/markdownlint-rules.md)
-   [<a href="https://github.com/pingcap/community/blob/master/contributors/code-comment-style.md">コードコメントのスタイル</a>](https://github.com/pingcap/community/blob/master/contributors/code-comment-style.md)
-   図のスタイル: [<a href="https://github.com/pingcap/community/blob/master/contributors/figma-quick-start-guide.md">Figma クイック スタート ガイド</a>](https://github.com/pingcap/community/blob/master/contributors/figma-quick-start-guide.md)

    図のスタイルの一貫性を維持するには、 [<a href="https://www.figma.com/">フィグマ</a>](https://www.figma.com/)を使用して図を描画または設計することをお勧めします。図を描く必要がある場合は、ガイドを参照し、テンプレートに用意されている図形や色を使用してください。

### ドキュメントのバージョンについて学ぶ {#learn-about-docs-versions}

現在、私たちは次のバージョンの TiDB ドキュメントを維持しており、それぞれに個別のブランチがあります。

| ドキュメントブランチ名     | バージョンの説明               |
| :-------------- | :--------------------- |
| `master`支店      | 最新の開発バージョン             |
| `release 6.1`支店 | 6.1 LTS (長期サポート) バージョン |
| `release 6.0`支店 | 6.0 開発マイルストーン リリース     |
| `release-5.4`支店 | 5.4安定版                 |
| `release-5.3`支店 | 5.3安定版                 |
| `release-5.2`支店 | 5.2安定版                 |
| `release-5.1`支店 | 5.1安定版                 |
| `release-5.0`支店 | 5.0安定版                 |
| `release-4.0`支店 | 4.0安定版                 |
| `release-3.1`支店 | 3.1 安定版                |
| `release-3.0`支店 | 3.0安定版                 |
| `release-2.1`支店 | 2.1安定版                 |

> **ノート：**
>
> 以前は、すべてのバージョンを`master`ブランチに、 `dev` (最新の開発バージョン)、 `v3.0`などのディレクトリで管理していました。ドキュメントの各バージョンは非常に頻繁に更新され、あるバージョンに対する変更は別のバージョンにも適用されることがよくあります。
>
> 2020 年 2 月 21 日以降、バージョン間の手動による編集と更新の作業を減らすために、各バージョンを別のブランチで保守し始め、次の期間に限り PR を他のバージョンに自動的にファイルする sre-bot (現在は ti-chi-bot) を導入しました。対応する厳選ラベルを PR に追加します。

### チェリーピックラベルを使用する {#use-cherry-pick-labels}

-   変更が 1 つのドキュメント バージョンにのみ適用される場合は、対応するバージョン ブランチに PR を送信するだけです。

-   変更が複数のドキュメント バージョンに適用される場合、各ブランチに PR を送信する必要はありません。代わりに、PR を送信した後、必要に応じて次のラベルの 1 つまたは複数を追加することで、ti-chi-bot が他のバージョン ブランチに PR を送信するようにトリガーします。現在の PR がマージされると、ti-chi-bot が動作し始めます。

    -   `needs-cherry-pick-6.1`ラベル: ti-chi-bot が`release-6.1`支店に PR を提出します。
    -   `needs-cherry-pick-6.0`ラベル: ti-chi-bot が`release-6.0`支店に PR を提出します。
    -   `needs-cherry-pick-5.4`ラベル: ti-chi-bot が`release-5.4`支店に PR を提出します。
    -   `needs-cherry-pick-5.3`ラベル: ti-chi-bot が`release-5.3`支店に PR を提出します。
    -   `needs-cherry-pick-5.2`ラベル: ti-chi-bot が`release-5.2`支店に PR を提出します。
    -   `needs-cherry-pick-5.1`ラベル: ti-chi-bot が`release-5.1`支店に PR を提出します。
    -   `needs-cherry-pick-5.0`ラベル: ti-chi-bot が`release-5.0`支店に PR を提出します。
    -   `needs-cherry-pick-4.0`ラベル: ti-chi-bot が`release-4.0`支店に PR を提出します。
    -   `needs-cherry-pick-3.1`ラベル: ti-chi-bot が`release-3.1`支店に PR を提出します。
    -   `needs-cherry-pick-3.0`ラベル: ti-chi-bot が`release-3.0`支店に PR を提出します。
    -   `needs-cherry-pick-2.1`ラベル: ti-chi-bot が`release-2.1`支店に PR を提出します。
    -   `needs-cherry-pick-master`ラベル: ti-chi-bot が`master`支店に PR を提出します。

    ドキュメントのバージョンの選択方法については、 [<a href="#guideline-for-choosing-the-affected-versions">影響を受けるバージョンを選択するためのガイドライン</a>](#guideline-for-choosing-the-affected-versions)を参照してください。

-   変更のほとんどが複数のドキュメント バージョンに適用されるが、バージョン間にいくつかの違いが存在する場合でも、チェリーピック ラベルを使用して、ti-chi-bot に他のバージョンへの PR を作成させることができます。別のバージョンへの PR が ti-chi-bot によって正常に送信された後、その PR に変更を加えることができます。

## 貢献方法 {#how-to-contribute}

このリポジトリへのプル リクエストを作成するには、次の手順を実行してください。コマンドを使用したくない場合は、簡単に開始できる[<a href="https://desktop.github.com/">GitHub デスクトップ</a>](https://desktop.github.com/)使用することもできます。

> **ノート：**
>
> このセクションでは、例として`master`ブランチへの PR の作成を取り上げます。他のブランチへの PR を作成する手順も同様です。

### ステップ 0: CLA に署名する {#step-0-sign-the-cla}

プル リクエストは、 [<a href="https://cla-assistant.io/pingcap/docs">コントリビューターライセンス契約</a>](https://cla-assistant.io/pingcap/docs) (CLA) に署名した後にのみマージできます。続行する前に、必ず CLA に署名してください。

### ステップ 1: リポジトリをフォークする {#step-1-fork-the-repository}

1.  プロジェクトにアクセスしてください: [<a href="https://github.com/pingcap/docs">https://github.com/pingcap/docs</a>](https://github.com/pingcap/docs)
2.  右上の**「Fork」**ボタンをクリックし、完了するまで待ちます。

### ステップ 2: フォークされたリポジトリのクローンをローカルstorageに作成する {#step-2-clone-the-forked-repository-to-local-storage}

```
cd $working_dir # Comes to the directory that you want put the fork in, for example, "cd ~/Documents/GitHub"
git clone git@github.com:$user/docs.git # Replace "$user" with your GitHub ID

cd $working_dir/docs
git remote add upstream git@github.com:pingcap/docs.git # Adds the upstream repo
git remote -v # Confirms that your remote makes sense
```

### ステップ 3: 新しいブランチを作成する {#step-3-create-a-new-branch}

1.  ローカルマスターをupstream/masterで最新の状態にします。

    ```
    cd $working_dir/docs
    git fetch upstream
    git checkout master
    git rebase upstream/master
    ```

2.  master ブランチに基づいて新しいブランチを作成します。

    ```
    git checkout -b new-branch-name
    ```

### ステップ 4: 何かをする {#step-4-do-something}

`new-branch-name`ブランチ上のいくつかのファイルを編集し、変更を保存します。 Visual Studio Code などのエディターを使用して、 `.md`ファイルを開いて編集できます。

### ステップ 5: 変更をコミットする {#step-5-commit-your-changes}

```
git status # Checks the local status
git add <file> ... # Adds the file(s) you want to commit. If you want to commit all changes, you can directly use `git add.`
git commit -m "commit-message: update the xx"
```

[<a href="https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message">コミットメッセージのスタイル</a>](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)を参照してください。

### ステップ 6: ブランチをアップストリーム/マスターと同期した状態に保つ {#step-6-keep-your-branch-in-sync-with-upstream-master}

```
# While on your new branch
git fetch upstream
git rebase upstream/master
```

### ステップ 7: 変更をリモートにプッシュする {#step-7-push-your-changes-to-the-remote}

```
git push -u origin new-branch-name # "-u" is used to track the remote branch from origin
```

### ステップ 8: プル リクエストを作成する {#step-8-create-a-pull-request}

1.  [<a href="https://github.com/$user/docs">https://github.com/$user/docs</a>](https://github.com/$user/docs)のフォークにアクセスします ( `$user` GitHub ID に置き換えます)。
2.  `new-branch-name`ブランチの横にある`Compare & pull request`ボタンをクリックして PR を作成します。 [<a href="https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style">プルリクエストのタイトルスタイル</a>](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)を参照してください。

これで、PR が正常に送信されました。この PR がマージされると、自動的に TiDB ドキュメントの寄稿者になります。

## 影響を受けるバージョンを選択するためのガイドライン {#guideline-for-choosing-the-affected-version-s}

プル リクエストを作成するときは、プル リクエスト ページの説明テンプレートでドキュメントの変更を適用するリリース バージョンを選択する必要があります。

変更が次のいずれかの状況に当てはまる場合は、 **MASTER ブランチのみを選択する**ことをお勧めします。 PR がマージされると、変更はすぐに[<a href="https://docs.pingcap.com/tidb/dev/">PingCAP ドキュメント Web サイトの開発ページ</a>](https://docs.pingcap.com/tidb/dev/)に表示されます。 TiDB の次のメジャー バージョンまたはマイナー バージョンがリリースされると、その変更は Web サイトの新しいバージョンのページにも表示されます。

-   欠落または不完全なドキュメント内容の補足など、ドキュメントの強化に関連します。
-   値、説明、例、タイプミスなど、不正確または間違ったドキュメントの内容を修正します。
-   特定のトピック モジュールにドキュメントのリファクタリングが含まれます。

変更が次のいずれかの状況に該当する場合は、**影響を受けるリリース ブランチとマスターを選択してください**。

-   特定のバージョンに関連する機能の動作変更が含まれます。
-   構成項目またはシステム変数のデフォルト値の変更を含む、互換性の変更が含まれます。
-   表示エラーを解決するために形式を修正しました
-   壊れたリンクを修正します

## コンタクト {#contact}

[<a href="https://internals.tidb.io/">TiDB 内部フォーラム</a>](https://internals.tidb.io/)に参加して議論してください。
