---
title: Integrate TiDB Cloud with Zapier
summary: Learn how to connect TiDB Cloud to 5000+ Apps with Zapier.
---

# TiDB Cloudと Zapier を統合する {#integrate-tidb-cloud-with-zapier}

[ザピア](https://zapier.com)は、何千ものアプリやサービスを含むワークフローを簡単に作成できる、コード不要の自動化ツールです。

Zapier で[TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)使用すると、次のことが可能になります。

-   MySQL 互換の HTAP データベースである TiDB を使用します。ローカルでビルドする必要はありません。
-   TiDB Cloud の管理を容易にします。
-   TiDB Cloud を5000 以上のアプリに接続し、ワークフローを自動化します。

このガイドでは、Zapier のTiDB Cloudアプリの概要と使用方法の例を紹介します。

## テンプレートを使用したクイック スタート {#quick-start-with-template}

[Zap テンプレート](https://platform.zapier.com/partners/zap-templates)は、公開されている Zapier 統合用に、アプリとコア フィールドが事前に選択された既製の統合または Zap です。

このセクションでは、ワークフローを作成する例として**、新しい Github グローバル イベントを TiDB 行に追加する**テンプレートを使用します。このワークフローでは、GitHub アカウントから新しいグローバル イベント (任意のレポで、任意の[GitHub イベント](https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types)が発生します) が作成されるたびに、Zapier がTiDB Cloudクラスターに新しい行を追加します。

### 前提条件 {#prerequisites}

開始する前に、次のものが必要です。

-   [ザピアアカウント](https://zapier.com/app/login) .
-   [GitHub アカウント](https://github.com/login) .
-   TiDB Cloud上の[TiDB Cloudアカウント](https://tidbcloud.com/signup)およびServerless Tierクラスター。詳細については、 [TiDB Cloudクイック スタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)を参照してください。

### ステップ 1: テンプレートを取得する {#step-1-get-the-template}

[Zapier 上のTiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)に進みます。 **Add new Github global events to TiDB rows**テンプレートを選択し、 <strong>Try it を</strong>クリックします。次に、エディターページに入ります。

### ステップ 2: トリガーを設定する {#step-2-set-up-the-trigger}

エディター ページでは、トリガーとアクションを確認できます。トリガーをクリックして設定します。

1.  アプリとイベントを選択

    テンプレートにはデフォルトでアプリとイベントが設定されているため、ここでは何もする必要はありません。 **[続行]**をクリックします。

2.  アカウントを選択

    TiDB Cloudに接続する GitHub アカウントを選択します。新しいアカウントを接続するか、既存のアカウントを選択できます。設定したら、 **[続行]**をクリックします。

3.  トリガーを設定する

    テンプレートには、デフォルトでトリガーが設定されています。 **[続行]**をクリックします。

4.  テストトリガー

    **[トリガーのテスト]**をクリックします。トリガーが正常にセットアップされると、GitHub アカウントから新しいグローバル イベントのデータを確認できます。 <strong>[続行]</strong>をクリックします。

### ステップ 3: <code>Find Table in TiDB Cloud</code>設定する {#step-3-set-up-the-code-find-table-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートによって設定されたデフォルト値`Find Table`保持します。 **[続行]**をクリックします。

2.  アカウントを選択

    1.  **[サインイン]**ボタンをクリックすると、新しいログイン ページにリダイレクトされます。
    2.  ログイン ページで、公開鍵と秘密鍵を入力します。 TiDB Cloud API キーを取得するには、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)の手順に従います。
    3.  **[続行]**をクリックします。

    ![Account](/media/tidb-cloud/zapier/zapier-tidbcloud-account.png)

3.  アクションを設定する

    このステップでは、イベント データを格納するために、 TiDB Cloudクラスター内のテーブルを指定する必要があります。まだテーブルがない場合は、この手順で作成できます。

    1.  ドロップダウン リストから、プロジェクト名とクラスター名を選択します。クラスターの接続情報が自動的に表示されます。

        ![Set up project name and cluster name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-project-and-cluster.png)

    2.  パスワードを入力してください。

    3.  ドロップダウン リストから、データベースを選択します。

        ![Set up database name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-databse.png)

        Zapier は、入力したパスワードを使用してTiDB Cloudからデータベースにクエリを実行します。クラスター内にデータベースが見つからない場合は、パスワードを再入力してページを更新してください。

    4.  **[検索するテーブル] ボックス**に`github_global_event`と入力します。テーブルが存在しない場合、テンプレートは次の DDL を使用してテーブルを作成します。 <strong>[続行]</strong>をクリックします。

        ![The create table DDL](/media/tidb-cloud/zapier/zapier-tidbcloud-create-table-ddl.png)

4.  テスト アクション

    **Test action**をクリックすると、Zapier がテーブルを作成します。テストをスキップすることもできます。このワークフローが初めて実行されるときにテーブルが作成されます。

### ステップ 4: <code>Create Row in TiDB Cloud</code>アクションを設定する {#step-4-set-up-the-code-create-row-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートによって設定されたデフォルト値を保持します。 **[続行]**をクリックします。

2.  アカウントを選択

    `Find Table in TiDB Cloud`アクションの設定時に選択したアカウントを選択します。 **[続行]**をクリックします。

    ![Choose account](/media/tidb-cloud/zapier/zapier-tidbcloud-choose-account.png)

3.  アクションを設定する

    1.  前の手順と同様に、 **Project Name** 、 <strong>クラスタ Name</strong> 、 <strong>TiDB Password</strong> 、および<strong>Database Name</strong>を入力します。

    2.  **[テーブル名]**で、ドロップダウン リストから<strong>github_global_event</strong>テーブルを選択します。テーブルの列が表示されます。

        ![Table columns](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-columns.png)

    3.  **[列]**ボックスで、トリガーから対応するデータを選択します。すべての列に入力し、 <strong>[続行]</strong>をクリックします。

        ![Fill in Columns](/media/tidb-cloud/zapier/zapier-fill-in-tidbcloud-triggers-data.png)

4.  テスト アクション

    **[アクションのテスト]**をクリックして、テーブルに新しい行を作成します。 TiDB Cloudクラスターを確認すると、データが正常に書き込まれていることがわかります。

    ```sql
    mysql> SELECT * FROM test.github_global_event;
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    | id          | type        | actor      | repo_name       | repo_url                                     | public | created_at          |
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    | 25324462424 | CreateEvent | shiyuhang0 | shiyuhang0/docs | https://api.github.com/repos/shiyuhang0/docs | True   | 2022-11-18 08:03:14 |
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    1 row in set (0.17 sec)
    ```

### ステップ 5: Zap を公開する {#step-5-publish-your-zap}

**[公開]**をクリックして Zap を公開します。 [ホームページ](https://zapier.com/app/zaps)で zap が実行されていることがわかります。

![Publish the zap](/media/tidb-cloud/zapier/zapier-tidbcloud-publish.png)

これで、この zap は、GitHub アカウントからTiDB Cloudにすべてのグローバル イベントを自動的に記録します。

## トリガーとアクション {#triggers-x26-actions}

[トリガーとアクション](https://zapier.com/how-it-works)は Zapier の重要な概念です。さまざまなトリガーとアクションを組み合わせることで、さまざまな自動化ワークフローを作成できます。

このセクションでは、 TiDB Cloud App on Zapier が提供するトリガーとアクションを紹介します。

### トリガー {#triggers}

次の表に、 TiDB Cloud App でサポートされているトリガーを示します。

| 引き金             | 説明                                                |
| --------------- | ------------------------------------------------- |
| 新しいクラスタ         | 新しいクラスターが作成されたときにトリガーされます。                        |
| 新しいテーブル         | 新しいテーブルが作成されたときにトリガーされます。                         |
| 新しい行            | 新しい行が作成されたときにトリガーされます。最近の 10000 行の新しい行のみをフェッチします。 |
| 新しい行 (カスタム クエリ) | 指定したカスタム クエリから新しい行が返されたときにトリガーされます。               |

### 行動 {#actions}

次の表に、 TiDB Cloud App でサポートされているアクションを示します。一部のアクションには追加のリソースが必要であり、アクションを使用する前に対応するリソースを準備する必要があることに注意してください。

| アクション           | 説明                                                 | リソース                                |
| --------------- | -------------------------------------------------- | ----------------------------------- |
| クラスタを検索         | 既存のサーバーレス層または専用層を検索します。                            | なし                                  |
| クラスタの作成         | 新しいクラスターを作成します。 Serverless Tierクラスターの作成のみをサポートします。 | なし                                  |
| データベースを探す       | 既存のデータベースを検索します。                                   | Serverless Tierクラスター                |
| データベースの作成       | 新しいデータベースを作成します。                                   | Serverless Tierクラスター                |
| テーブルを検索         | 既存のテーブルを検索します。                                     | Serverless Tierクラスターとデータベース         |
| テーブルの作成         | 新しいテーブルを作成します。                                     | Serverless Tierクラスターとデータベース         |
| 行を作成            | 新しい行を作成します。                                        | Serverless Tierクラスター、データベース、およびテーブル |
| 行の更新            | 既存の行を更新します。                                        | Serverless Tierクラスター、データベース、およびテーブル |
| 行を検索            | ルックアップ列を介してテーブル内の行を検索します。                          | Serverless Tierクラスター、データベース、およびテーブル |
| 行の検索 (カスタム クエリ) | 指定したカスタム クエリを使用して、テーブル内の行を検索します。                   | Serverless Tierクラスター、データベース、およびテーブル |

## TiDB Cloudアプリ テンプレート {#tidb-cloud-app-templates}

TiDB Cloud には、 Zapier で直接使用できるいくつかのテンプレートが用意されています。 [TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)ページですべてのテンプレートを見つけることができます。

ここではいくつかの例を示します。

-   [Google スプレッドシートで新しいTiDB Cloud行を複製する](https://zapier.com/apps/google-sheets/integrations/tidb-cloud/1134881/duplicate-new-tidb-cloud-rows-in-google-sheets) .
-   [新しいカスタム TiDB クエリから Gmail 経由でメールを送信する](https://zapier.com/apps/gmail/integrations/tidb-cloud/1134903/send-emails-via-gmail-from-new-custom-tidb-queries) .
-   [新しくキャッチされた Webhook からTiDB Cloudに行を追加する](https://zapier.com/apps/tidb-cloud/integrations/webhook/1134955/add-rows-to-tidb-cloud-from-newly-caught-webhooks) .
-   [新しい Salesforce 連絡先を TiDB 行に保存する](https://zapier.com/apps/salesforce/integrations/tidb-cloud/1134923/store-new-salesforce-contacts-on-tidb-rows) .
-   [履歴書付きの新しい Gmail メールの TiDB 行を作成し、直接 Slack 通知を送信する](https://zapier.com/apps/gmail/integrations/slack/1135456/create-tidb-rows-for-new-gmail-emails-with-resumes-and-send-direct-slack-notifications)

## FAQ {#faq}

### Zapier でTiDB Cloudアカウントを設定するにはどうすればよいですか? {#how-can-i-set-up-the-tidb-cloud-account-in-zapier}

Zapier が TiDB TiDB Cloudアカウントに接続するには、 **TiDB Cloud API キー**が必要です。 Zapier はTiDB Cloudのログイン アカウントを必要としません。

TiDB Cloud API キーを取得するには、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)に従ってください。

### TiDB Cloudトリガーはどのように重複除外を実行しますか? {#how-do-tidb-cloud-triggers-perform-de-duplication}

Zapier トリガーは、ポーリング API 呼び出しと連携して、新しいデータを定期的に確認できます (間隔は Zapier プランによって異なります)。

TiDB Cloudトリガーは、多くの結果を返すポーリング API 呼び出しを提供します。ただし、ほとんどの結果は以前に Zapier で確認されたものです。つまり、ほとんどの結果は重複しています。

API 内のアイテムが複数の異なるポーリングに存在する場合、アクションを複数回トリガーしたくないため、 TiDB Cloudトリガーは`id`フィールドでデータを重複排除します。

`New Cluster`および`New Table`トリガーは、単純に`cluster_id`または`table_id` `id`フィールドとして使用して重複排除を行います。 2 つのトリガーに対して何もする必要はありません。

**新しい行トリガー**

`New Row`トリガーは、フェッチごとに 10,000 件の結果を制限します。したがって、10,000 件の結果に新しい行が含まれていない場合、Zapier をトリガーすることはできません。

これを回避する 1 つの方法は、トリガーで`Order By`構成を指定することです。たとえば、作成時間で行を並べ替えると、新しい行は常に 10,000 件の結果に含まれます。

`New Row`トリガーも柔軟な戦略を使用して、重複排除を行うための`id`フィールドを生成します。トリガーは、次の順序で`id`フィールドを生成します。

1.  結果に`id`列が含まれる場合は、 `id`列を使用します。
2.  トリガー構成で`Dedupe Key`指定する場合は、 `Dedupe Key`を使用します。
3.  テーブルに主キーがある場合は、主キーを使用します。複数の主キーがある場合は、最初の列を使用します。
4.  テーブルに一意のキーがある場合は、一意のキーを使用します。
5.  表の最初の列を使用します。

**新しい行 (カスタム クエリ) トリガー**

`New Row (Custom Query)`トリガーは、すべてのフェッチで 1,000,000 の結果を制限します。 1,000,000 は大きな数であり、システム全体を保護するためにのみ設定されます。クエリに`ORDER BY`と`LIMIT`を含めることをお勧めします。

重複排除を実行するには、クエリ結果に一意の id フィールドが必要です。そうしないと、 `You must return the results with id field`エラーが発生します。

カスタム クエリが 30 秒以内に実行されることを確認してください。そうしないと、タイムアウト エラーが発生します。

### <code>find or create</code>アクションを使用するにはどうすればよいですか? {#how-do-i-use-the-code-find-or-create-code-action}

`Find or create`アクションを使用すると、リソースが存在しない場合にリソースを作成できます。次に例を示します。

1.  `Find Table`アクションを選択してください

2.  ステップ`set up action`で、ボックス`Create TiDB Cloud Table if it doesn’t exist yet?`にチェックを入れて`find and create`を有効にします。

    ![Find and create](/media/tidb-cloud/zapier/zapier-tidbcloud-find-and-create.png)

このワークフローは、テーブルがまだ存在しない場合に作成します。アクションをテストすると、テーブルが直接作成されることに注意してください。
