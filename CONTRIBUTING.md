# TiDB ドキュメント貢献ガイド {#tidb-documentation-contributing-guide}

[TiDB](https://github.com/pingcap/tidb)ドキュメントへようこそ! [TiDBコミュニティ](https://github.com/pingcap/community/)ご参加いただけることを心よりお待ちしております。

## あなたが貢献できること {#what-you-can-contribute}

[PingCAP ウェブサイトの TiDB ドキュメント](https://docs.pingcap.com/tidb/stable)改善するには、次のいずれかの項目から始めることができます。

-   タイプミスやフォーマット（句読点、スペース、インデント、コードブロックなど）を修正します
-   不適切または古い説明を修正または更新する
-   不足しているコンテンツ（文、段落、または新しいドキュメント）を追加します
-   ドキュメントの変更を英語から中国語に翻訳する
-   提出、返信、解決[ドキュメントの問題](https://github.com/pingcap/docs/issues)
-   (上級) 他の人が作成したプルリクエストを確認する

## 貢献する前に {#before-you-contribute}

貢献する前に、TiDB ドキュメントのメンテナンスに関する一般的な情報をざっとお読みください。これにより、すぐに貢献者になれるでしょう。

### スタイルに慣れる {#get-familiar-with-style}

-   [コミットメッセージのスタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)
-   [プルリクエストのタイトルスタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)
-   [マークダウンルール](/resources/markdownlint-rules.md)
-   [コードコメントスタイル](https://github.com/pingcap/community/blob/master/contributors/code-comment-style.md)
-   図表スタイル: [Figma クイックスタートガイド](https://github.com/pingcap/community/blob/master/contributors/figma-quick-start-guide.md)

    図のスタイルを統一するために、図の描画やデザインには[フィグマ](https://www.figma.com/)使用することをお勧めします。図を描く必要がある場合は、ガイドを参照し、テンプレートで提供されている図形や色を使用してください。

### ドキュメントテンプレートを選択する {#pick-a-doc-template}

TiDB 用の新しいドキュメントを作成する場合は、当社のスタイルに合わせて使用できる[いくつかのドキュメントテンプレート](/resources/doc-templates)ドキュメントを提供します。

プル リクエストを送信する前に、次のテンプレートを確認してください。

-   [コンセプト](/resources/doc-templates/template-concept.md)
-   [タスク](/resources/doc-templates/template-task.md)
-   [参照](/resources/doc-templates/template-reference.md)
-   [新機能](/resources/doc-templates/template-new-feature.md)
-   [トラブルシューティング](/resources/doc-templates/template-troubleshooting.md)

### ドキュメントのバージョンについて学ぶ {#learn-about-docs-versions}

異なるバージョンの TiDB ドキュメントを管理するために、個別のブランチを使用します。

-   [開発中のドキュメント](https://docs.pingcap.com/tidb/dev) `master`ブランチで維持されます。
-   [公開された文書](https://docs.pingcap.com/tidb/stable/)対応する`release-<version>`ブランチでメンテナンスされています。例えば、TiDB v8.1 のドキュメントは`release-8.1`ブランチでメンテナンスされています。
-   [アーカイブされた文書](https://docs-archive.pingcap.com/)メンテナンスされなくなり、今後更新されることはありません。

### チェリーピックラベルを使用する {#use-cherry-pick-labels}

あるドキュメント バージョンへの変更は他のドキュメント バージョンにも適用されることが多いため、チェリー ピック ラベルに基づいて PR チェリー ピック プロセスを自動化する[チチボット](https://github.com/ti-chi-bot)導入します。

-   変更が特定のドキュメントバージョンにのみ適用される場合は、そのドキュメントバージョンのブランチに基づいてPRを作成してください。チェリーピックラベルを追加する必要はありません。

-   変更が複数のドキュメントバージョンに適用される場合は、複数のPRを作成する代わりに、最新の適用可能なブランチ（例： `master` ）に基づいて1つのPRを作成し、適用可能なドキュメントバージョンに応じて1つまたは複数の`needs-cherry-pick-release-<version>`ラベルをPRに追加します。PRがマージされると、ti-chi-botは指定されたバージョンのブランチに基づいて、対応するチェリーピックPRを自動的に作成します。

-   変更の大部分が複数のドキュメントバージョンに適用されるものの、バージョン間で差異が存在する場合は、対象バージョンすべてにチェリーピックラベルを付与するだけでなく、PRレビュアーへのリマインダーとして「 `requires-version-specific-change`ラベルも付与する必要があります。PRがマージされ、ti-chi-botが対応するチェリーピックPRを作成した後でも、これらのチェリーピックPRに変更を加えることができます。

## 貢献方法 {#how-to-contribute}

このリポジトリへのプルリクエストを作成するには、以下の手順を実行してください。コマンドを使いたくない場合は、 [GitHubデスクトップ](https://desktop.github.com/)使用することもできます。こちらの方が簡単です。

> **注記：**
>
> このセクションでは、ブランチ`master`への PR の作成を例に説明します。他のブランチへの PR の作成手順も同様です。

### ステップ0: CLAに署名する {#step-0-sign-the-cla}

プルリクエストをマージするには、 [貢献者ライセンス契約](https://cla.pingcap.net/pingcap/docs) (CLA) に署名する必要があります。続行する前に必ず署名してください。

### ステップ1: リポジトリをフォークする {#step-1-fork-the-repository}

1.  プロジェクトを訪問: [https://github.com/pingcap/docs](https://github.com/pingcap/docs)
2.  右上の**フォーク**ボタンをクリックし、完了するまで待ちます。

### ステップ2: フォークしたリポジトリをローカルstorageにクローンする {#step-2-clone-the-forked-repository-to-local-storage}

    cd $working_dir # Comes to the directory that you want put the fork in, for example, "cd ~/Documents/GitHub"
    git clone git@github.com:$user/docs.git # Replace "$user" with your GitHub ID

    cd $working_dir/docs
    git remote add upstream git@github.com:pingcap/docs.git # Adds the upstream repo
    git remote -v # Confirms that your remote makes sense

### ステップ3: 新しいブランチを作成する {#step-3-create-a-new-branch}

1.  ローカル マスターを、upstream/master で最新の状態にします。

        cd $working_dir/docs
        git fetch upstream
        git checkout master
        git rebase upstream/master

2.  マスター ブランチに基づいて新しいブランチを作成します。

        git checkout -b new-branch-name

### ステップ4：何か行動を起こす {#step-4-do-something}

`new-branch-name`ブランチのファイルをいくつか編集し、変更を保存します。Visual Studio Code などのエディタを使用して`.md`ファイルを開いて編集できます。

### ステップ5: 変更をコミットする {#step-5-commit-your-changes}

    git status # Checks the local status
    git add <file> ... # Adds the file(s) you want to commit. If you want to commit all changes, you can directly use `git add.`
    git commit -m "commit-message: update the xx"

[コミットメッセージのスタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#how-to-write-a-good-commit-message)参照。

### ステップ6: ブランチをアップストリーム/マスターと同期させる {#step-6-keep-your-branch-in-sync-with-upstream-master}

    # While on your new branch
    git fetch upstream
    git rebase upstream/master

### ステップ7: 変更をリモートにプッシュする {#step-7-push-your-changes-to-the-remote}

    git push -u origin new-branch-name # "-u" is used to track the remote branch from origin

### ステップ8: プルリクエストを作成する {#step-8-create-a-pull-request}

1.  [https://github.com/$user/docs](https://github.com/$user/docs)でフォークにアクセスします ( `$user` GitHub ID に置き換えます)
2.  `new-branch-name`ブランチの横にある`Compare & pull request`ボタンをクリックして PR を作成します。5 [プルリクエストのタイトルスタイル](https://github.com/pingcap/community/blob/master/contributors/commit-message-pr-style.md#pull-request-title-style)参照してください。

これで、PR が正常に送信されました。この PR がマージされると、自動的に TiDB ドキュメントの貢献者になります。

## 影響を受けるバージョンを選択するためのガイドライン {#guideline-for-choosing-the-affected-version-s}

プル リクエストを作成するときは、プル リクエスト ページの説明テンプレートで、ドキュメントの変更を適用するリリース バージョンを選択する必要があります。

変更が以下のいずれかの状況に該当する場合は、 **「マスターブランチのみを選択」すること**をお勧めします。PRがマージされると、変更はすぐに[PingCAP ドキュメント ウェブサイトの開発ページ](https://docs.pingcap.com/tidb/dev/)に表示されます。TiDBの次のメジャーバージョンまたはマイナーバージョンがリリースされると、変更は新しいバージョンのウェブサイトページにも表示されます。

-   欠落または不完全なドキュメントの内容を補足するなど、ドキュメントの拡張に関連します。
-   値、説明、例、タイプミスなど、不正確または間違ったドキュメントの内容を修正します。
-   特定のトピック モジュールでのドキュメントのリファクタリングが含まれます。

変更が以下のいずれかの状況に当てはまる場合は、**影響を受けるリリース ブランチとマスターを選択してください**。

-   特定のバージョンに関連する機能の動作の変更が含まれます。
-   構成項目またはシステム変数のデフォルト値の変更など、互換性の変更が含まれます。
-   表示エラーを解決するためにフォーマットを修正します
-   壊れたリンクを修正

## TiDB Cloudドキュメントへの貢献に関するガイドライン {#guideline-for-contributing-to-tidb-cloud-documentation}

現在、 [TiDB Cloudドキュメント](https://docs.pingcap.com/tidbcloud/)英語版のみで提供されており、SQLドキュメントとTiDB v8.1の開発ドキュメントを再利用するために、このリポジトリの[リリース8.1](https://github.com/pingcap/docs/tree/release-8.1/tidb-cloud)ブランチに保存されています。したがって、 TiDB Cloudドキュメントのプルリクエストを作成する場合は、プルリクエストが[リリース8.1](https://github.com/pingcap/docs/tree/release-8.1)ブランチに基づいていることを確認してください。

> **ヒント：**
>
> TiDB Cloudによって再利用される TiDB ドキュメントを確認するには、 [TiDB Cloudドキュメントの TOC ファイル](https://github.com/pingcap/docs/blob/release-8.1/TOC-tidb-cloud.md?plain=1)確認してください。
>
> -   このファイル内のドキュメントのパスが`/tidb-cloud/`で始まる場合、このドキュメントはTiDB Cloud専用であることを意味します。
> -   このファイル内のドキュメントのパスが`/tidb-cloud/`で始まっていない場合は、この TiDB ドキュメントがTiDB Cloudによって再利用されることを意味します。

TiDB Cloudで再利用される一部の TiDB ドキュメントには、 `CustomContent`タグが含まれている場合があります。これらの`CustomContent`タグは、TiDB またはTiDB Cloudの専用コンテンツを示すために使用されます。

例えば：

```Markdown
## Restrictions

<CustomContent platform="tidb">

* The TiDB memory limit on the `INSERT INTO SELECT` statement can be adjusted using the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query). Starting from v6.5.0, it is not recommended to use [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) to control transaction memory size.

    For more information, see [TiDB memory control](/configure-memory-usage.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

* The TiDB memory limit on the `INSERT INTO SELECT` statement can be adjusted using the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query). Starting from v6.5.0, it is not recommended to use [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) to control transaction memory size.

    For more information, see [TiDB memory control](https://docs.pingcap.com/tidb/stable/configure-memory-usage).

</CustomContent>

* TiDB has no hard limit on the concurrency of the `INSERT INTO SELECT` statement, but it is recommended to consider the following practices:

    * When a "write transaction" is large, such as close to 1 GiB, it is recommended to control concurrency to no more than 10.
    * When a "write transaction" is small, such as less than 100 MiB, it is recommended to control concurrency to no more than 30.
    * Determine the concurrency based on testing results and specific circumstances.
```

この例では、

-   `<CustomContent platform="tidb">`タグ内のコンテンツは TiDB にのみ適用され、 [TiDB Cloudドキュメント](https://docs.pingcap.com/tidbcloud/) Web サイトには表示されません。
-   `<CustomContent platform="tidb-cloud">`タグ内のコンテンツはTiDB Cloudにのみ適用され、 [TiDBドキュメント](https://docs.pingcap.com/tidb/stable) Web サイトには表示されません。
-   `<CustomContent>`タグで囲まれていないコンテンツは、TiDB とTiDB Cloud の両方に適用され、両方のドキュメント Web サイトに表示されます。

## EBNF図のプレビューのガイドライン {#guideline-for-previewing-ebnf-diagrams}

[TiDBドキュメント](https://docs.pingcap.com/tidb/stable) 、SQL構文の理解を助けるために、多くのSQL概要図を提供しています。例えば、 `ALTER INDEX`文[ここ](https://docs.pingcap.com/tidb/stable/sql-statement-alter-index#synopsis)の概要図があります。

これら概要図のソースは[拡張バッカスナウア記法（EBNF）](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form)使用して記述されています。SQL文のEBNFコードを準備する際には、コードを[https://kennytm.github.io/website-docs/dist/](https://kennytm.github.io/website-docs/dist/)にコピーして**「レンダリング」**をクリックすることで、EBNF図を簡単にプレビューできます。

## 接触 {#contact}

ディスカッションには[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)参加してください。
