---
title: Integrate TiDB Cloud with Zapier
summary: Learn how to connect TiDB Cloud to 5000+ Apps with Zapier.
---

# TiDB Cloudと Zapier を統合する {#integrate-tidb-cloud-with-zapier}

[ザピエル](https://zapier.com)は、コード不要の自動化ツールで、何千ものアプリやサービスが関与するワークフローを簡単に作成できます。

Zapier で[TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)使用すると、次のことが可能になります。

-   MySQL 互換の HTAP データベースである TiDB を使用します。ローカルで構築する必要はありません。
-   TiDB Cloudの管理が簡単になります。
-   TiDB Cloud を5000 以上のアプリに接続し、ワークフローを自動化します。

このガイドでは、Zapier 上のTiDB Cloudアプリの概要とその使用方法の例を示します。

## テンプレートを使ったクイックスタート {#quick-start-with-template}

[ザップテンプレート](https://platform.zapier.com/partners/zap-templates)は、公開されている Zapier 統合用に、事前に選択されたアプリとコア フィールドを備えた既製の統合または Zaps です。

このセクションでは、例として**「新しい Github グローバル イベントを TiDB 行に追加」**テンプレートを使用してワークフローを作成します。このワークフローでは、GitHub アカウントから新しいグローバル イベント (任意のリポジトリ上で、あなたから、またはあなたへの[GitHubイベント](https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types)のイベントが発生する) が作成されるたびに、Zapier は新しい行をTiDB Cloudクラスターに追加します。

### 前提条件 {#prerequisites}

始める前に、次のものが必要です。

-   回答[ザピアアカウント](https://zapier.com/app/login) ．
-   回答[GitHub アカウント](https://github.com/login) ．
-   A [TiDB Cloudアカウント](https://tidbcloud.com/signup)と TiDBTiDB Cloud上の TiDB サーバーレス クラスター。詳細については、 [TiDB Cloudクイック スタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)を参照してください。

### ステップ 1: テンプレートを取得する {#step-1-get-the-template}

[Zapier 上のTiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)に進みます。 **[Add new Github global events to TiDB rows]**テンプレートを選択し、 **[Try it]**をクリックします。次に、エディターページに入ります。

### ステップ 2: トリガーを設定する {#step-2-set-up-the-trigger}

エディター ページでは、トリガーとアクションを確認できます。トリガーをクリックして設定します。

1.  アプリとイベントを選択

    テンプレートにはデフォルトでアプリとイベントが設定されているため、ここでは何もする必要はありません。 **[続行]**をクリックします。

2.  アカウントを選択してください

    TiDB Cloudに接続する GitHub アカウントを選択します。新しいアカウントを接続するか、既存のアカウントを選択できます。設定が完了したら、 **[続行]**をクリックします。

3.  トリガーを設定する

    テンプレートにはデフォルトでトリガーが設定されています。 **[続行]**をクリックします。

4.  テストトリガー

    **[トリガーのテスト]**をクリックします。トリガーが正常に設定されると、GitHub アカウントから新しいグローバル イベントのデータを確認できます。 **[続行]**をクリックします。

### ステップ 3: <code>Find Table in TiDB Cloud</code>アクションを設定する {#step-3-set-up-the-code-find-table-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートで設定されたデフォルト値`Find Table`そのまま使用します。 **[続行]**をクリックします。

2.  アカウントを選択してください

    1.  **「サインイン」**ボタンをクリックすると、新しいログインページにリダイレクトされます。
    2.  ログイン ページで、公開キーと秘密キーを入力します。 TiDB CloudAPI キーを取得するには、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)の手順に従ってください。
    3.  **[続行]**をクリックします。

    ![Account](/media/tidb-cloud/zapier/zapier-tidbcloud-account.png)

3.  アクションを設定する

    このステップでは、イベント データを保存するためにTiDB Cloudクラスター内のテーブルを指定する必要があります。まだテーブルがない場合は、この手順でテーブルを作成できます。

    1.  ドロップダウン リストからプロジェクト名とクラスター名を選択します。クラスターの接続情報が自動的に表示されます。

        ![Set up project name and cluster name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-project-and-cluster.png)

    2.  パスワードを入力してください。

    3.  ドロップダウン リストからデータベースを選択します。

        ![Set up database name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-databse.png)

        Zapier は、入力したパスワードを使用してTiDB Cloudからデータベースにクエリを実行します。クラスター内にデータベースが見つからない場合は、パスワードを再入力してページを更新します。

    4.  **[検索するテーブル] ボックス**に`github_global_event`と入力します。テーブルが存在しない場合、テンプレートは次の DDL を使用してテーブルを作成します。 **[続行]**をクリックします。

        ![The create table DDL](/media/tidb-cloud/zapier/zapier-tidbcloud-create-table-ddl.png)

4.  テストアクション

    **[アクションのテスト]**をクリックすると、Zapier によってテーブルが作成されます。テストをスキップすることもできます。このワークフローが初めて実行されるときにテーブルが作成されます。

### ステップ 4: <code>Create Row in TiDB Cloud</code>アクションを設定する {#step-4-set-up-the-code-create-row-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートで設定されたデフォルト値をそのまま使用します。 **[続行]**をクリックします。

2.  アカウントを選択してください

    `Find Table in TiDB Cloud`アクションを設定するときに選択したアカウントを選択します。 **[続行]**をクリックします。

    ![Choose account](/media/tidb-cloud/zapier/zapier-tidbcloud-choose-account.png)

3.  アクションを設定する

    1.  前のステップと同様に、 **「プロジェクト名」** 、 **「クラスタ名」** 、 **「TiDB パスワード」** 、および**「データベース名」**を入力します。

    2.  **[テーブル名]**で、ドロップダウン リストから**github_global_event**テーブルを選択します。テーブルの列が表示されます。

        ![Table columns](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-columns.png)

    3.  **[列]**ボックスで、トリガーから対応するデータを選択します。すべての列に入力し、 **[続行]**をクリックします。

        ![Fill in Columns](/media/tidb-cloud/zapier/zapier-fill-in-tidbcloud-triggers-data.png)

4.  テストアクション

    **[テスト アクション]**をクリックして、テーブルに新しい行を作成します。 TiDB Cloudクラスターを確認すると、データが正常に書き込まれていることがわかります。

    ```sql
    mysql> SELECT * FROM test.github_global_event;
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    | id          | type        | actor      | repo_name       | repo_url                                     | public | created_at          |
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    | 25324462424 | CreateEvent | shiyuhang0 | shiyuhang0/docs | https://api.github.com/repos/shiyuhang0/docs | True   | 2022-11-18 08:03:14 |
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    1 row in set (0.17 sec)
    ```

### ステップ 5: ザップを公開する {#step-5-publish-your-zap}

**「公開」**をクリックしてザップを公開します。 [ホームページ](https://zapier.com/app/zaps)でザップが実行されていることがわかります。

![Publish the zap](/media/tidb-cloud/zapier/zapier-tidbcloud-publish.png)

このザップにより、すべてのグローバル イベントが GitHub アカウントからTiDB Cloudに自動的に記録されます。

## トリガーとアクション {#triggers-x26-actions}

[トリガーとアクション](https://zapier.com/how-it-works)は Zapier の重要な概念です。さまざまなトリガーとアクションを組み合わせることで、さまざまな自動化ワークフローを作成できます。

このセクションでは、Zapier 上のTiDB Cloud App によって提供されるトリガーとアクションを紹介します。

### トリガー {#triggers}

次の表に、 TiDB Cloud App でサポートされるトリガーを示します。

| 引き金            | 説明                                           |
| -------------- | -------------------------------------------- |
| 新しいクラスタ        | 新しいクラスターが作成されるときにトリガーされます。                   |
| 新しいテーブル        | 新しいテーブルが作成されるときにトリガーされます。                    |
| 新しい行           | 新しい行が作成されたときにトリガーされます。最近の 10000 行のみをフェッチします。 |
| 新しい行 (カスタムクエリ) | 指定したカスタム クエリから新しい行が返されたときにトリガーされます。          |

### 行動 {#actions}

次の表に、 TiDB Cloud App でサポートされるアクションを示します。一部のアクションには追加のリソースが必要なので、アクションを使用する前に対応するリソースを準備する必要があることに注意してください。

| アクション           | 説明                                              | リソース                          |
| --------------- | ----------------------------------------------- | ----------------------------- |
| クラスタの検索         | 既存の TiDB サーバーレス クラスターまたは TiDB 専用クラスターを検索します。    | なし                            |
| クラスタの作成         | 新しいクラスターを作成します。 TiDB サーバーレス クラスターの作成のみをサポートします。 | なし                            |
| データベースの検索       | 既存のデータベースを検索します。                                | TiDB サーバーレスクラスター              |
| データベースの作成       | 新しいデータベースを作成します。                                | TiDB サーバーレスクラスター              |
| テーブルの検索         | 既存のテーブルを検索します。                                  | TiDB サーバーレス クラスターとデータベース      |
| テーブルの作成         | 新しいテーブルを作成します。                                  | TiDB サーバーレス クラスターとデータベース      |
| 行の作成            | 新しい行を作成します。                                     | TiDB サーバーレス クラスター、データベース、テーブル |
| 行を更新            | 既存の行を更新します。                                     | TiDB サーバーレス クラスター、データベース、テーブル |
| 行の検索            | ルックアップ列を介してテーブル内の行を検索します。                       | TiDB サーバーレス クラスター、データベース、テーブル |
| 行の検索 (カスタム クエリ) | 指定したカスタム クエリを介してテーブル内の行を検索します。                  | TiDB サーバーレス クラスター、データベース、テーブル |

## TiDB Cloudアプリ テンプレート {#tidb-cloud-app-templates}

TiDB Cloud には、 Zapier で直接使用できるテンプレートがいくつか用意されています。すべてのテンプレートが[TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)ページで見つかります。

ここではいくつかの例を示します。

-   [Google スプレッドシートで新しいTiDB Cloud行を複製する](https://zapier.com/apps/google-sheets/integrations/tidb-cloud/1134881/duplicate-new-tidb-cloud-rows-in-google-sheets) 。
-   [新しいカスタム TiDB クエリから Gmail 経由で電子メールを送信](https://zapier.com/apps/gmail/integrations/tidb-cloud/1134903/send-emails-via-gmail-from-new-custom-tidb-queries) 。
-   [新しくキャッチした Webhook からTiDB Cloudに行を追加します](https://zapier.com/apps/tidb-cloud/integrations/webhook/1134955/add-rows-to-tidb-cloud-from-newly-caught-webhooks) 。
-   [新しい Salesforce 連絡先を TiDB 行に保存する](https://zapier.com/apps/salesforce/integrations/tidb-cloud/1134923/store-new-salesforce-contacts-on-tidb-rows) 。
-   [履歴書付きの新しい Gmail メール用の TiDB 行を作成し、Slack 通知を直接送信します](https://zapier.com/apps/gmail/integrations/slack/1135456/create-tidb-rows-for-new-gmail-emails-with-resumes-and-send-direct-slack-notifications)

## FAQ {#faq}

### Zapier でTiDB Cloudアカウントを設定するにはどうすればよいですか? {#how-can-i-set-up-the-tidb-cloud-account-in-zapier}

Zapier では、 TiDB Cloudアカウントに接続するために**TiDB CloudAPI キーが**必要です。 Zapier では、 TiDB Cloudのログイン アカウントは必要ありません。

TiDB CloudAPI キーを取得するには、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)に従ってください。

### TiDB Cloudトリガーはどのように重複除外を実行しますか? {#how-do-tidb-cloud-triggers-perform-de-duplication}

Zapier トリガーは、ポーリング API 呼び出しと連携して、新しいデータを定期的にチェックできます (間隔は Zapier プランによって異なります)。

TiDB Cloudトリガーは、多くの結果を返すポーリング API 呼び出しを提供します。ただし、結果のほとんどは以前に Zapier によって確認されたものであり、結果のほとんどが重複しています。

API 内の項目が複数の異なるポーリングに存在する場合、アクションを複数回トリガーしたくないため、 TiDB Cloudトリガーは`id`フィールドでデータの重複を排除します。

`New Cluster`および`New Table`トリガーは、単に`cluster_id`または`table_id` `id`フィールドとして使用して重複排除を実行します。 2 つのトリガーに対しては何もする必要はありません。

**新しい行トリガー**

`New Row`トリガーでは、フェッチごとに 10,000 件の結果が制限されます。したがって、10,000 件の結果に新しい行が含まれていない場合、Zapier をトリガーできません。

これを回避する 1 つの方法は、トリガーで`Order By`構成を指定することです。たとえば、行を作成時間で並べ替えると、新しい行は常に 10,000 件の結果に含まれます。

`New Row`トリガーは、重複排除を行うための`id`フィールドを生成する柔軟な戦略も使用します。トリガーは、次の順序で`id`フィールドを生成します。

1.  結果に`id`列が含まれる場合は、 `id`列を使用します。
2.  トリガー設定で`Dedupe Key`指定する場合は、 `Dedupe Key`使用します。
3.  テーブルに主キーがある場合は、主キーを使用します。複数の主キーがある場合は、最初の列を使用します。
4.  テーブルに一意のキーがある場合は、その一意のキーを使用します。
5.  表の最初の列を使用します。

**新しい行(カスタムクエリ)トリガー**

`New Row (Custom Query)`トリガーは、フェッチごとに 1,000,000 件の結果を制限します。 1,000,000 は大きな数であり、システム全体を保護するためにのみ設定されています。クエリには`ORDER BY`と`LIMIT`を含めることをお勧めします。

重複排除を実行するには、クエリ結果に一意の ID フィールドが必要です。そうしないと、 `You must return the results with id field`エラーが発生します。

カスタム クエリが 30 秒以内に実行されるようにしてください。そうしないと、タイムアウト エラーが発生します。

### <code>find or create</code>アクションを使用するにはどうすればよいですか? {#how-do-i-use-the-code-find-or-create-code-action}

`Find or create`アクションを使用すると、リソースが存在しない場合にリソースを作成できます。以下に例を示します。

1.  アクションを`Find Table`選択してください

2.  `set up action`ステップで、 `Create TiDB Cloud Table if it doesn’t exist yet?`ボックスにチェックを入れて`find and create`を有効にします。

    ![Find and create](/media/tidb-cloud/zapier/zapier-tidbcloud-find-and-create.png)

このワークフローは、テーブルがまだ存在しない場合は作成します。アクションをテストすると、テーブルが直接作成されることに注意してください。
