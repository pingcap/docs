# TiDBドキュメント寄稿ガイド {#tidb-documentation-contributing-guide}

[TiDB](https://github.com/pingcap/tidb)のドキュメントへようこそ！私たちはあなたが[TiDBコミュニティ](https://github.com/pingcap/community/)に参加する見込みに興奮しています。

## あなたが貢献できること {#what-you-can-contribute}

次の項目のいずれかから開始して、 [PingCAPWebサイトのTiDBドキュメント](https://docs.pingcap.com/tidb/stable)を改善することができます。

-   タイプミスまたはフォーマット（句読点、スペース、インデント、コードブロックなど）を修正します
-   不適切または古い説明を修正または更新する
-   不足しているコンテンツ（文、段落、または新しいドキュメント）を追加します
-   ドキュメントの変更を英語から中国語に翻訳する
-   送信、返信、解決[ドキュメントの問題](https://github.com/pingcap/docs/issues)
-   （詳細）他のユーザーが作成したプルリクエストを確認する

## 貢献する前に {#before-you-contribute}

貢献する前に、TiDBドキュメントのメンテナンスに関する一般的な情報を簡単に確認してください。これは、すぐに寄稿者になるのに役立ちます。

### スタイルに慣れる {#get-familiar-with-style}

-   [メッセージスタイルのコミット](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)
-   [プルリクエストのタイトルスタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)
-   [マークダウンルール](/resources/markdownlint-rules.md)
-   [コードコメントスタイル](https://github.com/pingcap/community/blob/master/contributors/code-comment-style.md)
-   ダイアグラムスタイル： [Figmaクイックスタートガイド](https://github.com/pingcap/community/blob/master/contributors/figma-quick-start-guide.md)

    ダイアグラムのスタイルを一貫させるために、 [フィグマ](https://www.figma.com/)を使用してダイアグラムを描画または設計することをお勧めします。図を描く必要がある場合は、ガイドを参照して、テンプレートで提供されている形状または色を使用してください。

### ドキュメントバージョンについて学ぶ {#learn-about-docs-versions}

現在、次のバージョンのTiDBドキュメントを維持しており、それぞれに個別のブランチがあります。

| ドキュメントブランチ名       | バージョンの説明                 |
| :---------------- | :----------------------- |
| `master`ブランチ      | 最新の開発バージョン               |
| `release 6.1`ブランチ | 6.1 LTS（ロングタームサポート）バージョン |
| `release 6.0`ブランチ | 6.0開発マイルストーンリリース         |
| `release-5.4`ブランチ | 5.4安定バージョン               |
| `release-5.3`ブランチ | 5.3安定バージョン               |
| `release-5.2`ブランチ | 5.2安定バージョン               |
| `release-5.1`ブランチ | 5.1安定バージョン               |
| `release-5.0`ブランチ | 5.0安定バージョン               |
| `release-4.0`ブランチ | 4.0安定バージョン               |
| `release-3.1`ブランチ | 3.1安定バージョン               |
| `release-3.0`ブランチ | 3.0安定バージョン               |
| `release-2.1`ブランチ | 2.1安定バージョン               |

> **ノート：**
>
> 以前は、 `dev` （最新の開発バージョン）、 `v3.0`などのディレクトリを使用して、すべてのバージョンを`master`ブランチに保持していました。各ドキュメントバージョンは非常に頻繁に更新され、あるバージョンへの変更は別のバージョンまたは他のバージョンにも適用されることがよくあります。
>
> 2020年2月21日以降、バージョン間の手動編集と更新作業を減らすために、各バージョンを別々のブランチで維持し始め、sre-bot（現在はti-chi-bot）を導入して、PRを他のバージョンに自動的に提出するようにしました。対応するチェリーピックラベルをPRに追加します。

### チェリーピックラベルを使用する {#use-cherry-pick-labels}

-   変更が1つのドキュメントバージョンにのみ適用される場合は、対応するバージョンブランチにPRを送信するだけです。

-   変更が複数のドキュメントバージョンに適用される場合は、各ブランチにPRを送信する必要はありません。代わりに、PRを送信した後、必要に応じて次のラベルの1つまたは複数を追加して、ti-chi-botをトリガーして他のバージョンのブランチにPRを送信します。現在のPRがマージされると、ti-chi-botが機能し始めます。

    -   `needs-cherry-pick-6.1`ラベル：ti-chi-botはPRを`release-6.1`ブランチに送信します。
    -   `needs-cherry-pick-6.0`ラベル：ti-chi-botはPRを`release-6.0`ブランチに送信します。
    -   `needs-cherry-pick-5.4`ラベル：ti-chi-botはPRを`release-5.4`ブランチに送信します。
    -   `needs-cherry-pick-5.3`ラベル：ti-chi-botはPRを`release-5.3`ブランチに送信します。
    -   `needs-cherry-pick-5.2`ラベル：ti-chi-botはPRを`release-5.2`ブランチに送信します。
    -   `needs-cherry-pick-5.1`ラベル：ti-chi-botはPRを`release-5.1`ブランチに送信します。
    -   `needs-cherry-pick-5.0`ラベル：ti-chi-botはPRを`release-5.0`ブランチに送信します。
    -   `needs-cherry-pick-4.0`ラベル：ti-chi-botはPRを`release-4.0`ブランチに送信します。
    -   `needs-cherry-pick-3.1`ラベル：ti-chi-botはPRを`release-3.1`ブランチに送信します。
    -   `needs-cherry-pick-3.0`ラベル：ti-chi-botはPRを`release-3.0`ブランチに送信します。
    -   `needs-cherry-pick-2.1`ラベル：ti-chi-botはPRを`release-2.1`ブランチに送信します。
    -   `needs-cherry-pick-master`ラベル：ti-chi-botはPRを`master`ブランチに送信します。

    ドキュメントのバージョンを選択する方法については、 [影響を受けるバージョンを選択するためのガイドライン](#guideline-for-choosing-the-affected-versions)を参照してください。

-   ほとんどの変更が複数のドキュメントバージョンに適用されるが、バージョン間にいくつかの違いが存在する場合でも、チェリーピックラベルを使用して、ti-chi-botに他のバージョンへのPRを作成させることができます。別のバージョンへのPRがti-chi-botによって正常に送信された後、そのPRに変更を加えることができます。

## 貢献する方法 {#how-to-contribute}

このリポジトリへのプルリクエストを作成するには、次の手順を実行してください。コマンドを使用したくない場合は、 [GitHubデスクトップ](https://desktop.github.com/)を使用することもできます。これは開始が簡単です。

> **ノート：**
>
> このセクションでは、例として`master`ブランチへのPRの作成について説明します。他のブランチへのPRを作成する手順も同様です。

### ステップ0：CLAに署名する {#step-0-sign-the-cla}

プルリクエストは、 [貢献者ライセンス契約](https://cla-assistant.io/pingcap/docs) （CLA）に署名した後にのみマージできます。続行する前に、必ずCLAに署名してください。

### ステップ1：リポジトリをフォークする {#step-1-fork-the-repository}

1.  プロジェクトにアクセス： [https://github.com/pingcap/docs](https://github.com/pingcap/docs)
2.  右上の[**フォーク**]ボタンをクリックして、完了するまで待ちます。

### ステップ2：フォークされたリポジトリをローカルストレージに複製する {#step-2-clone-the-forked-repository-to-local-storage}

```
cd $working_dir # Comes to the directory that you want put the fork in, for example, "cd ~/Documents/GitHub"
git clone git@github.com:$user/docs.git # Replace "$user" with your GitHub ID

cd $working_dir/docs
git remote add upstream git@github.com:pingcap/docs.git # Adds the upstream repo
git remote -v # Confirms that your remote makes sense
```

### ステップ3：新しいブランチを作成する {#step-3-create-a-new-branch}

1.  アップストリーム/マスターでローカルマスターを最新の状態にします。

    ```
    cd $working_dir/docs
    git fetch upstream
    git checkout master
    git rebase upstream/master
    ```

2.  マスターブランチに基づいて新しいブランチを作成します。

    ```
    git checkout -b new-branch-name
    ```

### ステップ4：何かをする {#step-4-do-something}

`new-branch-name`ブランチのいくつかのファイルを編集し、変更を保存します。 Visual Studio Codeなどのエディターを使用して、 `.md`のファイルを開いて編集できます。

### ステップ5：変更をコミットする {#step-5-commit-your-changes}

```
git status # Checks the local status
git add <file> ... # Adds the file(s) you want to commit. If you want to commit all changes, you can directly use `git add.`
git commit -m "commit-message: update the xx"
```

[メッセージスタイルのコミット](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)を参照してください。

### ステップ6：ブランチをアップストリーム/マスターと同期させます {#step-6-keep-your-branch-in-sync-with-upstream-master}

```
# While on your new branch
git fetch upstream
git rebase upstream/master
```

### ステップ7：変更をリモートにプッシュする {#step-7-push-your-changes-to-the-remote}

```
git push -u origin new-branch-name # "-u" is used to track the remote branch from origin
```

### 手順8：プルリクエストを作成する {#step-8-create-a-pull-request}

1.  [https://github.com/$user/docs](https://github.com/$user/docs)でフォークにアクセスします（ `$user`をGitHub IDに置き換えます）
2.  `new-branch-name`のブランチの横にある`Compare & pull request`のボタンをクリックして、PRを作成します。 [プルリクエストのタイトルスタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)を参照してください。

これで、PRが正常に送信されました。このPRがマージされると、自動的にTiDBドキュメントの寄稿者になります。

## 影響を受けるバージョンを選択するためのガイドライン {#guideline-for-choosing-the-affected-version-s}

プルリクエストを作成するときは、プルリクエストページの説明テンプレートで、ドキュメントの変更が適用されるリリースバージョンを選択する必要があります。

変更が次のいずれかの状況に当てはまる場合は、**マスターブランチのみ**を選択することをお勧めします。 PRがマージされた後、変更はすぐに[PingCAPドキュメントWebサイトの開発ページ](https://docs.pingcap.com/tidb/dev/)に表示されます。 TiDBの次のメジャーバージョンまたはマイナーバージョンがリリースされた後、変更は新しいバージョンのWebサイトページにも表示されます。

-   欠落または不完全なドキュメントコンテンツの補足など、ドキュメントの拡張に関連します。
-   値、説明、例、タイプミスなど、不正確または不正確なドキュメントの内容を修正します。
-   特定のトピックモジュールにドキュメントのリファクタリングが含まれます。

変更が次のいずれかの状況に当てはまる場合は、影響を**受けるリリースブランチとマスター**を選択してください。

-   特定のバージョンに関連する機能の動作の変更が含まれます。
-   構成アイテムまたはシステム変数のデフォルト値の変更を含む、互換性の変更が含まれます。
-   表示エラーを解決するためのフォーマットを修正
-   壊れたリンクを修正

## コンタクト {#contact}

議論のために[TiDB内部フォーラム](https://internals.tidb.io/)に参加してください。
