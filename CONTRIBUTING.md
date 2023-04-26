# TiDB ドキュメンテーション寄稿ガイド {#tidb-documentation-contributing-guide}

[TiDB](https://github.com/pingcap/tidb)ドキュメントへようこそ! [TiDB コミュニティ](https://github.com/pingcap/community/)への参加をお待ちしております。

## 貢献できること {#what-you-can-contribute}

[PingCAP Web サイトの TiDB ドキュメント](https://docs.pingcap.com/tidb/stable)を改善するために、次の項目のいずれかから開始できます。

-   タイプミスや形式 (句読点、スペース、インデント、コード ブロックなど) を修正します。
-   不適切または古い説明を修正または更新する
-   不足しているコンテンツを追加する (文、段落、または新しいドキュメント)
-   ドキュメントの変更を英語から中国語に翻訳する
-   送信、返信、解決[ドキュメントの問題](https://github.com/pingcap/docs/issues)
-   (高度) 他のユーザーが作成したプル リクエストを確認する

## 貢献する前に {#before-you-contribute}

貢献する前に、TiDB ドキュメントのメンテナンスに関する一般的な情報を簡単に確認してください。これにより、すぐに寄稿者になることができます。

### スタイルに慣れる {#get-familiar-with-style}

-   [コミット メッセージ スタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)
-   [プル リクエストのタイトル スタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)
-   [マークダウンのルール](/resources/markdownlint-rules.md)
-   [コード コメント スタイル](https://github.com/pingcap/community/blob/master/contributors/code-comment-style.md)
-   図のスタイル: [figmaクイックスタートガイド](https://github.com/pingcap/community/blob/master/contributors/figma-quick-start-guide.md)

    図の一貫したスタイルを維持するために、 [フィグマ](https://www.figma.com/)使用して図を描画または設計することをお勧めします。図を描く必要がある場合は、ガイドを参照し、テンプレートで提供されている形や色を使用してください。

### ドキュメントのバージョンについて学ぶ {#learn-about-docs-versions}

現在、私たちは次のバージョンの TiDB ドキュメントを維持しており、それぞれに別のブランチがあります。

| ドキュメントのブランチ名    | バージョンの説明               |
| :-------------- | :--------------------- |
| `master`支店      | 最新の開発バージョン             |
| `release 6.1`支店 | 6.1 LTS (長期サポート) バージョン |
| `release 6.0`支店 | 6.0 開発マイルストーン リリース     |
| `release-5.4`支店 | 5.4 安定版                |
| `release-5.3`支店 | 5.3 安定バージョン            |
| `release-5.2`支店 | 5.2 安定版                |
| `release-5.1`支店 | 5.1 安定バージョン            |
| `release-5.0`支店 | 5.0 安定版                |
| `release-4.0`支店 | 4.0 安定版                |
| `release-3.1`支店 | 3.1 安定版                |
| `release-3.0`支店 | 3.0 安定版                |
| `release-2.1`支店 | 2.1 安定版                |

> **ノート：**
>
> 以前は、 `dev` (最新の開発バージョン)、 `v3.0`などのディレクトリを使用して、すべてのバージョンを`master`ブランチに保持していました。ドキュメントの各バージョンは非常に頻繁に更新され、あるバージョンへの変更が別のバージョンまたは他のバージョンにも適用されることがよくあります。
>
> 2020 年 2 月 21 日以降、バージョン間の手動編集および更新作業を減らすために、各バージョンを別のブランチで維持することを開始し、sre-bot (現在の ti-chi-bot) を導入して、PR を他のバージョンに自動的にファイルするようにしました。対応するチェリー ピック ラベルを PR に追加します。

### チェリーピックラベルを使用する {#use-cherry-pick-labels}

-   変更が 1 つのドキュメント バージョンのみに適用される場合は、対応するバージョン ブランチに PR を送信してください。

-   変更が複数のドキュメント バージョンに適用される場合は、各ブランチに PR を送信する必要はありません。代わりに、PR を送信した後、必要に応じて次のラベルの 1 つまたは複数を追加して、ti-chi-bot をトリガーして他のバージョン ブランチに PR を送信します。現在の PR がマージされると、ti-chi-bot が機能し始めます。

    -   `needs-cherry-pick-6.1`ラベル: ti-chi-bot は`release-6.1`ブランチに PR を送信します。
    -   `needs-cherry-pick-6.0`ラベル: ti-chi-bot は`release-6.0`ブランチに PR を送信します。
    -   `needs-cherry-pick-5.4`ラベル: ti-chi-bot は`release-5.4`ブランチに PR を送信します。
    -   `needs-cherry-pick-5.3`ラベル: ti-chi-bot は`release-5.3`ブランチに PR を送信します。
    -   `needs-cherry-pick-5.2`ラベル: ti-chi-bot は`release-5.2`ブランチに PR を送信します。
    -   `needs-cherry-pick-5.1`ラベル: ti-chi-bot は`release-5.1`ブランチに PR を送信します。
    -   `needs-cherry-pick-5.0`ラベル: ti-chi-bot は`release-5.0`ブランチに PR を送信します。
    -   `needs-cherry-pick-4.0`ラベル: ti-chi-bot は`release-4.0`ブランチに PR を送信します。
    -   `needs-cherry-pick-3.1`ラベル: ti-chi-bot は`release-3.1`ブランチに PR を送信します。
    -   `needs-cherry-pick-3.0`ラベル: ti-chi-bot は`release-3.0`ブランチに PR を送信します。
    -   `needs-cherry-pick-2.1`ラベル: ti-chi-bot は`release-2.1`ブランチに PR を送信します。
    -   `needs-cherry-pick-master`ラベル: ti-chi-bot は`master`ブランチに PR を送信します。

    ドキュメント バージョンの選択方法については、 [影響を受けるバージョンを選択するためのガイドライン](#guideline-for-choosing-the-affected-versions)を参照してください。

-   ほとんどの変更が複数のドキュメント バージョンに適用され、バージョン間にいくつかの違いがある場合でも、cherry-pick ラベルを使用して、ti-chi-bot が他のバージョンへの PR を作成できるようにすることができます。別のバージョンへの PR が ti-chi-bot によって正常に送信された後、その PR を変更できます。

## 貢献する方法 {#how-to-contribute}

このリポジトリへのプル リクエストを作成するには、次の手順を実行してください。コマンドを使いたくない場合は、簡単に開始できる[GitHub デスクトップ](https://desktop.github.com/)使用することもできます。

> **ノート：**
>
> このセクションでは、例として`master`ブランチへの PR を作成します。他のブランチへの PR を作成する手順は似ています。

### ステップ 0: CLA に署名する {#step-0-sign-the-cla}

プル リクエストは、 [寄稿者ライセンス契約](https://cla-assistant.io/pingcap/docs) (CLA) に署名した後にのみマージできます。続行する前に、必ず CLA に署名してください。

### ステップ 1: リポジトリをフォークする {#step-1-fork-the-repository}

1.  プロジェクトにアクセス: [https://github.com/pingcap/docs](https://github.com/pingcap/docs)
2.  右上の**Fork**ボタンをクリックして、完了するまで待ちます。

### ステップ 2: フォークされたリポジトリをローカルstorageに複製する {#step-2-clone-the-forked-repository-to-local-storage}

```
cd $working_dir # Comes to the directory that you want put the fork in, for example, "cd ~/Documents/GitHub"
git clone git@github.com:$user/docs.git # Replace "$user" with your GitHub ID

cd $working_dir/docs
git remote add upstream git@github.com:pingcap/docs.git # Adds the upstream repo
git remote -v # Confirms that your remote makes sense
```

### ステップ 3: 新しいブランチを作成する {#step-3-create-a-new-branch}

1.  アップストリーム/マスターを使用して、ローカル マスターを最新の状態にします。

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

`new-branch-name`ブランチでいくつかのファイルを編集し、変更を保存します。 Visual Studio Code などのエディターを使用して、 `.md`ファイルを開いて編集できます。

### ステップ 5: 変更をコミットする {#step-5-commit-your-changes}

```
git status # Checks the local status
git add <file> ... # Adds the file(s) you want to commit. If you want to commit all changes, you can directly use `git add.`
git commit -m "commit-message: update the xx"
```

[コミット メッセージ スタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)を参照してください。

### ステップ 6: ブランチをアップストリーム/マスターと同期させておく {#step-6-keep-your-branch-in-sync-with-upstream-master}

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

1.  フォークの[https://github.com/$user/docs](https://github.com/$user/docs)にアクセスします ( `$user` GitHub ID に置き換えます)。
2.  `new-branch-name`ブランチの横にある`Compare & pull request`ボタンをクリックして、PR を作成します。 [プル リクエストのタイトル スタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)を参照してください。

これで、PR が正常に送信されました。この PR がマージされた後、あなたは自動的に TiDB ドキュメントへの寄稿者になります。

## 影響を受けるバージョンを選択するためのガイドライン {#guideline-for-choosing-the-affected-version-s}

プル リクエストを作成するときは、プル リクエスト ページの説明テンプレートで、ドキュメントの変更が適用されるリリース バージョンを選択する必要があります。

変更が次のいずれかの状況に当てはまる場合は、**マスター ブランチのみを選択する**ことをお勧めします。 PR がマージされると、すぐに変更が[PingCAP ドキュメント Web サイトの開発ページ](https://docs.pingcap.com/tidb/dev/)に表示されます。 TiDB の次のメジャーまたはマイナー バージョンがリリースされた後、変更は新しいバージョンの Web サイト ページにも表示されます。

-   不足または不完全なドキュメントの内容を補足するなど、ドキュメントの機能強化に関連しています。
-   値、説明、例、タイプミスなど、不正確または不適切なドキュメント コンテンツを修正します。
-   特定のトピック モジュールにドキュメントのリファクタリングが含まれます。

変更が次のいずれかの状況に当てはまる場合は、**影響を受けるリリース ブランチとマスターを選択してください**。

-   特定のバージョンに関連する機能の動作の変更が含まれます。
-   構成項目またはシステム変数のデフォルト値の変更を含む、互換性の変更を伴います。
-   表示エラーを解決するためにフォーマットを修正
-   リンク切れを修正

## コンタクト {#contact}

議論のために[TiDB 内部フォーラム](https://internals.tidb.io/)に参加してください。
