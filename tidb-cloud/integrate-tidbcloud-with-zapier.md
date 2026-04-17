---
title: Integrate TiDB Cloud with Zapier
summary: TiDB CloudをZapierを使って5000以上のアプリに接続する方法を学びましょう。
---

# TiDB CloudとZapierを統合する {#integrate-tidb-cloud-with-zapier}

[ザピアー](https://zapier.com)数千ものアプリやサービスを含むワークフローを簡単に作成できる、ノーコードの自動化ツールです。

Zapier で[TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)使用すると、次のことが可能になります。

-   MySQL互換のHTAPデータベースであるTiDBを使用してください。ローカルでの構築は不要です。
-   TiDB Cloudの管理をより簡単にします。
-   TiDB Cloudを5000以上のアプリに接続して、ワークフローを自動化しましょう。

このガイドでは、Zapier 上のTiDB Cloudアプリの概要と使用例について説明します。

## テンプレートを使ったクイックスタート {#quick-start-with-template}

[Zapテンプレート](https://platform.zapier.com/partners/zap-templates)、公開されているZapier連携機能向けに、アプリとコアフィールドが事前に選択された、すぐに使える連携機能またはZapです。

このセクションでは、 **「新しい GitHub グローバル イベントを TiDB 行に追加する」**テンプレートを例として、ワークフローを作成します。このワークフローでは、GitHub アカウントから新しいグローバル イベント (任意のリポジトリで、あなたからまたはあなたに対して発生する[GitHubイベント](https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types)) が作成されるたびに、Zapier がTiDB Cloudクラスターに新しい行を追加します。

### 前提条件 {#prerequisites}

始める前に必要なもの：

-   [Zapierアカウント](https://zapier.com/app/login)。
-   [GitHubアカウント](https://github.com/login)。
-   [TiDB Cloudアカウント](https://tidbcloud.com/signup)と TiDBTiDB CloudTiDB Cloud Starterインスタンス。詳細については、 [TiDB Cloudクイックスタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-starter-instance)を参照してください。

### ステップ1：テンプレートを入手する {#step-1-get-the-template}

[TiDB CloudアプリをZapierで利用](https://zapier.com/apps/tidb-cloud/integrations)へ。 **[Add new Github global events to TiDB rows]**テンプレートを選択し、 **[Try it]**をクリックします。次に、エディターページに入ります。

### ステップ2：トリガーを設定する {#step-2-set-up-the-trigger}

エディターページでは、トリガーとアクションを確認できます。トリガーをクリックして設定してください。

1.  アプリとイベントを選択

    テンプレートにはアプリとイベントがデフォルトで設定されているため、ここでは何もする必要はありません。 **「続行」**をクリックしてください。

2.  アカウントを選択

    TiDB Cloudに接続するGitHubアカウントを選択してください。新規アカウントを接続することも、既存のアカウントを選択することもできます。設定が完了したら、 **「続行」**をクリックしてください。

3.  トリガーの設定

    テンプレートでは、デフォルトでトリガーが設定されています。 **「続行」**をクリックしてください。

4.  テストトリガー

    **「トリガーをテスト」を**クリックします。トリガーが正常に設定されると、GitHubアカウントから新しいグローバルイベントのデータが表示されます。 **「続行」**をクリックします。

### ステップ3： <code>Find Table in TiDB Cloud</code>アクションを設定する {#step-3-set-up-the-code-find-table-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートで設定されているデフォルト値`Find Table`そのまま使用します。 **[続行]**をクリックします。

2.  アカウントを選択

    1.  「**サインイン」**ボタンをクリックすると、新しいログインページにリダイレクトされます。
    2.  ログイン ページで、公開キーと秘密キーを入力します。 TiDB Cloud API キーを取得するには、 [TiDB Cloud APIドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)ドキュメントの手順に従ってください。
    3.  **「続行」**をクリックしてください。

    ![Account](/media/tidb-cloud/zapier/zapier-tidbcloud-account.png)

3.  アクションを設定する

    この手順では、イベントデータを保存するTiDB Cloud Starterインスタンス内のテーブルを指定する必要があります。テーブルがまだ作成されていない場合は、この手順で作成できます。

    1.  ドロップダウンリストからプロジェクト名とインスタンス名を選択してください。TiDB Cloud Starterインスタンスの接続情報が自動的に表示されます。

        ![Set up project name and instance name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-project-and-cluster.png)

    2.  パスワードを入力してください。

    3.  ドロップダウンリストからデータベースを選択してください。

        ![Set up database name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-databse.png)

        Zapierは、入力されたパスワードを使用してTiDB Cloudからデータベースを検索します。TiDB Cloud Starterインスタンスにデータベースが見つからない場合は、パスワードを再入力してページを更新してください。

    4.  **「検索するテーブル」ボックス**に`github_global_event`と入力します。テーブルが存在しない場合、テンプレートは次の DDL を使用してテーブルを作成します。 **「続行」**をクリックします。

        ![The create table DDL](/media/tidb-cloud/zapier/zapier-tidbcloud-create-table-ddl.png)

4.  テストアクション

    **「テスト」アクション**をクリックすると、Zapierがテーブルを作成します。テストをスキップすることも可能で、その場合はワークフローが初めて実行されるときにテーブルが作成されます。

### ステップ4： <code>Create Row in TiDB Cloud</code>設定する {#step-4-set-up-the-code-create-row-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートで設定されているデフォルト値をそのまま使用します。 **[続行]**をクリックします。

2.  アカウントを選択

    `Find Table in TiDB Cloud`アクションを設定する際に選択したアカウントを選択します。 **[続行]**をクリックします。

    ![Choose account](/media/tidb-cloud/zapier/zapier-tidbcloud-choose-account.png)

3.  アクションを設定する

    1.  前の手順と同様に、**プロジェクト名**、**クラスタ名**、 **TiDBパスワード**、**データベース名**を入力してください。

    2.  「**テーブル名」**で、ドロップダウンリストから「 **github_global_event」**テーブルを選択します。テーブルの列が表示されます。

        ![Table columns](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-columns.png)

    3.  **「列」**ボックスで、トリガーから対応するデータを選択します。すべての列を入力し、 **「続行」**をクリックします。

        ![Fill in Columns](/media/tidb-cloud/zapier/zapier-fill-in-tidbcloud-triggers-data.png)

4.  テストアクション

    **「テスト」アクション**をクリックして、テーブルに新しい行を作成します。TiDB Cloud Starterインスタンスを確認すると、データが正常に書き込まれていることが確認できます。

    ```sql
    mysql> SELECT * FROM test.github_global_event;
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    | id          | type        | actor      | repo_name       | repo_url                                     | public | created_at          |
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    | 25324462424 | CreateEvent | shiyuhang0 | shiyuhang0/docs | https://api.github.com/repos/shiyuhang0/docs | True   | 2022-11-18 08:03:14 |
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    1 row in set (0.17 sec)
    ```

### ステップ5：Zapを公開する {#step-5-publish-your-zap}

**「公開」**をクリックして、作成したZapを公開します。[ホームページ](https://zapier.com/app/zaps)でZapが実行されていることを確認できます。

![Publish the zap](/media/tidb-cloud/zapier/zapier-tidbcloud-publish.png)

これで、このZapによって、GitHubアカウントからのすべてのグローバルイベントがTiDB Cloudに自動的に記録されます。

## トリガーとアクション {#triggers-x26-actions}

[トリガーとアクション](https://zapier.com/how-it-works)は Zapier の重要な概念です。さまざまなトリガーとアクションを組み合わせることで、さまざまな自動化ワークフローを作成できます。

このセクションでは、TiDB Cloud AppがZapier上で提供するトリガーとアクションについて説明します。

### トリガー {#triggers}

以下の表は、TiDB Cloud Appでサポートされているトリガーの一覧です。

| トリガー         | 説明                                        |
| ------------ | ----------------------------------------- |
| 新しいクラスタ      | 新しいクラスターが作成されたときにトリガーされます。                |
| 新しいテーブル      | 新しいテーブルが作成されたときにトリガーされます。                 |
| 新しい行         | 新しい行が作成されたときにトリガーされます。直近の10,000行のみを取得します。 |
| 新規行（カスタムクエリ） | 指定したカスタムクエリから新しい行が返されたときにトリガーされます。        |

### 行動 {#actions}

以下の表は、 TiDB Cloud Appでサポートされているアクションの一覧です。一部のアクションは追加のリソースを必要とするため、アクションを使用する前に必要なリソースを準備する必要があります。

| アクション         | 説明                                                            | リソース                                    |
| ------------- | ------------------------------------------------------------- | --------------------------------------- |
| クラスタの検索       | 既存のTiDB Cloud StarterインスタンスまたはTiDB Cloud Dedicatedクラスタを検索します。 | なし                                      |
| クラスタを作成する     | 新しいクラスターを作成します。TiDB Cloud Starterインスタンスの作成のみをサポートしています。  | なし                                      |
| データベースの検索     | 既存のデータベースを検索します。                                              | TiDB Cloud Starterインスタンス                |
| データベースを作成する   | 新しいデータベースを作成します。                                              | TiDB Cloud Starterインスタンス                |
| テーブルを探す       | 既存のテーブルを検索します。                                                | TiDB Cloud Starterインスタンスとデータベース         |
| テーブルを作成する     | 新しいテーブルを作成します。                                                | TiDB Cloud Starterインスタンスとデータベース         |
| 行を作成する        | 新しい行を作成します。                                                   | TiDB Cloud Starterインスタンス、データベース、およびテーブル |
| 行を更新する        | 既存の行を更新します。                                                   | TiDB Cloud Starterインスタンス、データベース、およびテーブル |
| 行を検索          | 参照列を使用してテーブル内の行を検索します。                                        | TiDB Cloud Starterインスタンス、データベース、およびテーブル |
| 行の検索（カスタムクエリ） | 指定したカスタムクエリを使用して、テーブル内の行を検索します。                               | TiDB Cloud Starterインスタンス、データベース、およびテーブル |

## TiDB Cloudアプリテンプレート {#tidb-cloud-app-templates}

TiDB Cloudには、Zapierで直接使用できるテンプレートがいくつか用意されています。すべてのテンプレートは[TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)ページで確認できます。

以下に例を示します。

-   [GoogleスプレッドシートにTiDB Cloudの新しい行を複製する](https://zapier.com/apps/google-sheets/integrations/tidb-cloud/1134881/duplicate-new-tidb-cloud-rows-in-google-sheets)。
-   [新しいカスタムTiDBクエリからGmail経由でメールを送信する](https://zapier.com/apps/gmail/integrations/tidb-cloud/1134903/send-emails-via-gmail-from-new-custom-tidb-queries)。
-   [新たに捕捉したウェブフックからTiDB Cloudに行を追加する](https://zapier.com/apps/tidb-cloud/integrations/webhook/1134955/add-rows-to-tidb-cloud-from-newly-caught-webhooks)。
-   [新しいSalesforce連絡先をTiDB行に保存します](https://zapier.com/apps/salesforce/integrations/tidb-cloud/1134923/store-new-salesforce-contacts-on-tidb-rows)。
-   [履歴書付きの新しいGmailメール用にTiDB行を作成し、Slackに直接通知を送信する。](https://zapier.com/apps/gmail/integrations/slack/1135456/create-tidb-rows-for-new-gmail-emails-with-resumes-and-send-direct-slack-notifications)

## FAQ {#faq}

### TiDB CloudアカウントをZapierに設定するにはどうすればよいですか？ {#how-can-i-set-up-the-tidb-cloud-account-in-zapier}

Zapierは、 TiDB Cloudアカウントに接続するために**TiDB Cloud APIキー**を必要とします。ZapierはTiDB Cloudのログインアカウントを必要としません。

TiDB Cloud API キーを取得するには、 [TiDB Cloud APIドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)に従ってください。

### TiDB Cloudのトリガーはどのように重複排除を実行するのですか？ {#how-do-tidb-cloud-triggers-perform-de-duplication}

Zapierのトリガーは、ポーリングAPI呼び出しと連携して、定期的に新しいデータをチェックすることができます（間隔はZapierのプランによって異なります）。

TiDB Cloudのトリガーは、多数の結果を返すポーリングAPI呼び出しを提供します。しかし、その結果のほとんどはZapierによって既に確認されているものであり、つまり、ほとんどの結果は重複しています。

API 内のアイテムが複数の異なるポーリングに存在する場合にアクションが複数回トリガーされないようにするため、 TiDB Cloudトリガーは`id`フィールドを使用してデータの重複を排除します。

`New Cluster`および`New Table`トリガーは、 `cluster_id`または`table_id`を`id`フィールドとして使用して重複排除を行います。この 2 つのトリガーについては、何もする必要はありません。

**新しい行のトリガー**

`New Row`トリガーは、フェッチごとに10,000件の結果を制限します。そのため、新しい行が10,000件の結果に含まれていない場合、Zapierはトリガーされません。

これを回避する方法の一つは、トリガーで`Order By`設定を指定することです。例えば、行を生成時刻でソートすると、新しい行は常に 10,000 件の結果に含まれるようになります。

`New Row`トリガーは、重複排除を行う`id`フィールドを生成するために、柔軟な戦略も使用します。トリガーは`id`フィールドを次の順序で生成します。

1.  結果に`id`列が含まれている場合は、 `id`列を使用します。
2.  トリガー構成で`Dedupe Key`を指定する場合は、 `Dedupe Key`を使用してください。
3.  テーブルに主キーがある場合は、その主キーを使用します。主キーが複数ある場合は、最初の列を使用します。
4.  テーブルに一意キーがある場合は、その一意キーを使用してください。
5.  表の最初の列を使用してください。

**新規行（カスタムクエリ）トリガー**

`New Row (Custom Query)`トリガーは、フェッチごとに 1,000,000 件の結果を制限します。1,000,000 は大きな数値であり、システム全体を保護するためにのみ設定されています。クエリには`ORDER BY`と`LIMIT`を含めることをお勧めします。

重複排除を実行するには、クエリ結果に一意のIDフィールドが必要です。そうでない場合、 `You must return the results with id field`エラーが発生します。

カスタムクエリの実行時間が30秒以内であることを確認してください。そうでない場合、タイムアウトエラーが発生します。

### <code>find or create</code>アクションはどのように使用すればよいですか？ {#how-do-i-use-the-code-find-or-create-code-action}

`Find or create`アクションを使用すると、リソースが存在しない場合に作成できます。以下に例を示します。

1.  `Find Table`アクションを選択してください

2.  `set up action`ステップで、 `Create TiDB Cloud Table if it doesn’t exist yet?`ボックスにチェックを入れて、 `find and create`を有効にします。

    ![Find and create](/media/tidb-cloud/zapier/zapier-tidbcloud-find-and-create.png)

このワークフローは、テーブルがまだ存在しない場合に作成します。なお、アクションをテストすると、テーブルは直接作成されます。
