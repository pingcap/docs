---
title: Integrate TiDB Cloud with Zapier
summary: Zapier を使用してTiDB Cloud を5000 以上のアプリに接続する方法を学びます。
---

# TiDB CloudとZapierを統合する {#integrate-tidb-cloud-with-zapier}

[ザピエール](https://zapier.com) 、何千ものアプリやサービスが関与するワークフローを簡単に作成できるコード不要の自動化ツールです。

Zapier の[TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)使用すると、次のことが可能になります。

-   MySQL互換のHTAPデータベースであるTiDBを使用します。ローカルで構築する必要はありません。
-   TiDB Cloudの管理が簡単になります。
-   TiDB Cloud を5000 以上のアプリに接続し、ワークフローを自動化します。

このガイドでは、Zapier 上のTiDB Cloudアプリの概要と使用方法の例を示します。

## テンプレートを使ったクイックスタート {#quick-start-with-template}

[Zapテンプレート](https://platform.zapier.com/partners/zap-templates)は、公開されている Zapier 統合用に、アプリとコア フィールドが事前に選択された、すぐに使用できる統合または Zap です。

このセクションでは、「**新しい Github グローバルイベントを TiDB 行に追加する」**テンプレートを例としてワークフローを作成します。このワークフローでは、GitHub アカウントで新しいグローバルイベント（任意の[GitHubイベント](https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types)で、あなたまたはあなた宛てのイベント）が作成されるたびに、Zapier がTiDB Cloudクラスターに新しい行を追加します。

### 前提条件 {#prerequisites}

始める前に、次のものが必要です。

-   A [Zapierアカウント](https://zapier.com/app/login) 。
-   A [GitHubアカウント](https://github.com/login) 。
-   [TiDB Cloudアカウント](https://tidbcloud.com/signup)とTiDB Cloud Serverless クラスター（TiDB Cloud上）です。詳細については[TiDB Cloudクイックスタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)ご覧ください。

### ステップ1: テンプレートを入手する {#step-1-get-the-template}

[Zapier のTiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)に進みます。「**新しいGithubグローバルイベントをTiDB行に追加」**テンプレートを選択し、 **「試してみる」**をクリックします。すると、エディターページが表示されます。

### ステップ2: トリガーを設定する {#step-2-set-up-the-trigger}

エディターページでトリガーとアクションを確認できます。トリガーをクリックして設定します。

1.  アプリとイベントを選択

    テンプレートではアプリとイベントがデフォルトで設定されているため、ここでは何もする必要はありません。 **「続行」**をクリックしてください。

2.  アカウントを選択

    TiDB Cloudに接続する GitHub アカウントを選択してください。新しいアカウントを接続することも、既存のアカウントを選択することもできます。設定が完了したら、 **「続行」**をクリックしてください。

3.  トリガーを設定する

    テンプレートではデフォルトでトリガーが設定されています。 **「続行」**をクリックしてください。

4.  テストトリガー

    **「テストトリガー」**をクリックします。トリガーが正常に設定されていれば、GitHubアカウントから新しいグローバルイベントのデータを確認できます。 **「続行」**をクリックします。

### ステップ3: <code>Find Table in TiDB Cloud</code>アクションを設定する {#step-3-set-up-the-code-find-table-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートで設定されたデフォルト値`Find Table`ままにし、 **「続行」**をクリックします。

2.  アカウントを選択

    1.  **「サインイン」**ボタンをクリックすると、新しいログインページにリダイレクトされます。
    2.  ログインページで、公開鍵と秘密鍵を入力してください。TiDB TiDB Cloud APIキーを取得するには、 [TiDB Cloud API ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)の手順に従ってください。
    3.  **［続行］**をクリックします。

    ![Account](/media/tidb-cloud/zapier/zapier-tidbcloud-account.png)

3.  アクションの設定

    このステップでは、イベントデータを保存するTiDB Cloudクラスター内のテーブルを指定する必要があります。まだテーブルがない場合は、このステップで作成できます。

    1.  ドロップダウンリストからプロジェクト名とクラスター名を選択します。クラスターの接続情報が自動的に表示されます。

        ![Set up project name and cluster name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-project-and-cluster.png)

    2.  パスワードを入力してください。

    3.  ドロップダウンリストからデータベースを選択します。

        ![Set up database name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-databse.png)

        Zapierは、入力したパスワードを使用してTiDB Cloudのデータベースにクエリを実行します。クラスター内にデータベースが見つからない場合は、パスワードを再入力してページを更新してください。

    4.  **「検索するテーブル」**ボックスに`github_global_event`と入力します。テーブルが存在しない場合は、テンプレートは次のDDLを使用してテーブルを作成します。 **「続行」**をクリックします。

        ![The create table DDL](/media/tidb-cloud/zapier/zapier-tidbcloud-create-table-ddl.png)

4.  テストアクション

    **「テストアクション」**をクリックすると、Zapierがテーブルを作成します。テストをスキップして、このワークフローが初めて実行されるときにテーブルを作成することもできます。

### ステップ4: <code>Create Row in TiDB Cloud</code>を設定する {#step-4-set-up-the-code-create-row-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートで設定されたデフォルト値をそのままにし、 **「続行」**をクリックします。

2.  アカウントを選択

    `Find Table in TiDB Cloud`アクションの設定時に選択したアカウントを選択します。 **「続行」**をクリックします。

    ![Choose account](/media/tidb-cloud/zapier/zapier-tidbcloud-choose-account.png)

3.  アクションの設定

    1.  前の手順と同様に、**プロジェクト名**、**クラスタ名**、 **TiDB パスワード**、**データベース名**を入力します。

    2.  **テーブル名**で、ドロップダウンリストから**github_global_event**テーブルを選択します。テーブルの列が表示されます。

        ![Table columns](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-columns.png)

    3.  **「列」**ボックスで、トリガーから対応するデータを選択します。すべての列に入力し、 **「続行」**をクリックします。

        ![Fill in Columns](/media/tidb-cloud/zapier/zapier-fill-in-tidbcloud-triggers-data.png)

4.  テストアクション

    **「テストアクション」**をクリックすると、テーブルに新しい行が作成されます。TiDB TiDB Cloudクラスターを確認すると、データが正常に書き込まれていることが確認できます。

    ```sql
    mysql> SELECT * FROM test.github_global_event;
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    | id          | type        | actor      | repo_name       | repo_url                                     | public | created_at          |
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    | 25324462424 | CreateEvent | shiyuhang0 | shiyuhang0/docs | https://api.github.com/repos/shiyuhang0/docs | True   | 2022-11-18 08:03:14 |
    +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
    1 row in set (0.17 sec)
    ```

### ステップ5: Zapを公開する {#step-5-publish-your-zap}

**「公開」**をクリックしてZapを公開します。3でZapが実行中であることがわかります[ホームページ](https://zapier.com/app/zaps)

![Publish the zap](/media/tidb-cloud/zapier/zapier-tidbcloud-publish.png)

これで、この zap は GitHub アカウントからのすべてのグローバル イベントをTiDB Cloudに自動的に記録します。

## トリガーとアクション {#triggers-x26-actions}

[トリガーとアクション](https://zapier.com/how-it-works)はZapierの主要概念です。さまざまなトリガーとアクションを組み合わせることで、多様な自動化ワークフローを作成できます。

このセクションでは、Zapier 上のTiDB Cloud App が提供するトリガーとアクションについて説明します。

### トリガー {#triggers}

次の表は、TiDB Cloud App でサポートされているトリガーを示しています。

| トリガー          | 説明                                       |
| ------------- | ---------------------------------------- |
| 新しいクラスタ       | 新しいクラスターが作成された場合にトリガーされます。               |
| 新しいテーブル       | 新しいテーブルが作成された場合にトリガーされます。                |
| 新しい行          | 新しい行が作成された際にトリガーされます。最新の10,000行のみを取得します。 |
| 新しい行（カスタムクエリ） | 指定したカスタム クエリから新しい行が返されたときにトリガーされます。      |

### アクション {#actions}

以下の表は、 TiDB Cloud Appでサポートされているアクションの一覧です。一部のアクションには追加のリソースが必要となるため、アクションを使用する前に適切なリソースを準備する必要があります。

| アクション         | 説明                                                            | リソース                                    |
| ------------- | ------------------------------------------------------------- | --------------------------------------- |
| クラスタを見つける     | 既存のTiDB Cloud Serverless またはTiDB Cloud Dedicated クラスターを検索します。 | なし                                      |
| クラスタの作成       | 新しいクラスターを作成します。TiDB TiDB Cloud Serverless クラスターの作成のみをサポートします。 | なし                                      |
| データベースを探す     | 既存のデータベースを検索します。                                              | TiDB Cloudサーバーレスクラスター                   |
| データベースの作成     | 新しいデータベースを作成します。                                              | TiDB Cloudサーバーレスクラスター                   |
| テーブルを探す       | 既存のテーブルを検索します。                                                | TiDB Cloud Serverlessクラスタとデータベース        |
| テーブルを作成       | 新しいテーブルを作成します。                                                | TiDB Cloud Serverlessクラスタとデータベース        |
| 行を作成          | 新しい行を作成します。                                                   | TiDB Cloud Serverless クラスター、データベース、テーブル |
| 行を更新          | 既存の行を更新します。                                                   | TiDB Cloud Serverless クラスター、データベース、テーブル |
| 行を検索          | ルックアップ列を使用してテーブル内の行を検索します。                                    | TiDB Cloud Serverless クラスター、データベース、テーブル |
| 行の検索（カスタムクエリ） | 指定したカスタム クエリを使用してテーブル内の行を検索します。                               | TiDB Cloud Serverless クラスター、データベース、テーブル |

## TiDB Cloudアプリ テンプレート {#tidb-cloud-app-templates}

TiDB Cloudは、 Zapierで直接使用できるテンプレートをいくつか提供しています。すべてのテンプレートは[TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)ページ目にあります。

以下に例をいくつか挙げます。

-   [Google スプレッドシートで新しいTiDB Cloud行を複製する](https://zapier.com/apps/google-sheets/integrations/tidb-cloud/1134881/duplicate-new-tidb-cloud-rows-in-google-sheets) 。
-   [新しいカスタム TiDB クエリから Gmail 経由でメールを送信する](https://zapier.com/apps/gmail/integrations/tidb-cloud/1134903/send-emails-via-gmail-from-new-custom-tidb-queries) 。
-   [新しくキャッチしたウェブフックからTiDB Cloudに行を追加する](https://zapier.com/apps/tidb-cloud/integrations/webhook/1134955/add-rows-to-tidb-cloud-from-newly-caught-webhooks) 。
-   [新しい Salesforce 連絡先を TiDB 行に保存する](https://zapier.com/apps/salesforce/integrations/tidb-cloud/1134923/store-new-salesforce-contacts-on-tidb-rows) 。
-   [履歴書付きの新しい Gmail メールの TiDB 行を作成し、Slack 通知を直接送信します](https://zapier.com/apps/gmail/integrations/slack/1135456/create-tidb-rows-for-new-gmail-emails-with-resumes-and-send-direct-slack-notifications)

## FAQ {#faq}

### Zapier でTiDB Cloudアカウントを設定するにはどうすればよいですか? {#how-can-i-set-up-the-tidb-cloud-account-in-zapier}

Zapier はTiDB Cloudアカウントに接続するために**TiDB Cloud API キー**を必要とします。Zapier はTiDB Cloudのログインアカウントを必要としません。

TiDB Cloud API キーを取得するには、 [TiDB Cloud API ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)従ってください。

### TiDB Cloudトリガーは重複排除をどのように実行しますか? {#how-do-tidb-cloud-triggers-perform-de-duplication}

Zapier トリガーはポーリング API 呼び出しと連携して、定期的に新しいデータをチェックします (間隔は Zapier プランによって異なります)。

TiDB Cloudトリガーは、大量の結果を返すポーリングAPI呼び出しを提供します。しかし、その結果のほとんどはZapierが以前に確認したものであり、つまり重複しています。

API 内のアイテムが複数の異なるポーリングに存在する場合、アクションを複数回トリガーしたくないため、 TiDB Cloud は`id`フィールドでデータの重複を排除します。

トリガー`New Cluster`と`New Table`は、重複排除を行うために、単に`cluster_id`または`table_id` `id`フィールドとして使用します。2つのトリガーについては何もする必要はありません。

**新しい行トリガー**

トリガー`New Row`は、1回のフェッチで10,000件の結果に制限されます。そのため、10,000件の結果に含まれない新しい行がある場合、Zapierをトリガーできません。

これを回避する方法の一つは、トリガーに`Order By`設定を指定することです。例えば、行を作成時刻で並べ替えると、新しい行は常に10,000件の結果に含まれるようになります。

`New Row`トリガーは、重複排除を行うための`id`番目のフィールドを生成するためにも柔軟な戦略を採用しています。トリガーは、以下の順序で`id`フィールドを生成します。

1.  結果に`id`列目が含まれる場合は、 `id`列目を使用します。
2.  トリガー構成で`Dedupe Key`指定する場合は、 `Dedupe Key`使用します。
3.  テーブルに主キーがある場合は、その主キーを使用します。複数の主キーがある場合は、最初の列を使用します。
4.  テーブルに一意のキーがある場合は、その一意のキーを使用します。
5.  表の最初の列を使用します。

**新しい行（カスタムクエリ）トリガー**

トリガー`New Row (Custom Query)`は、毎回のフェッチで 1,000,000 件の結果を制限します。1,000,000 という数値は大きすぎるため、システム全体を保護するためにのみ設定されています。クエリには`ORDER BY`と`LIMIT`含めることをお勧めします。

重複排除を実行するには、クエリ結果に一意のIDフィールドが必要です。そうでない場合、エラー`You must return the results with id field`が発生します。

カスタムクエリが30秒以内に実行されることを確認してください。30秒未満で実行されると、タイムアウトエラーが発生します。

### <code>find or create</code>アクションを使用するにはどうすればよいですか? {#how-do-i-use-the-code-find-or-create-code-action}

`Find or create`アクションを使用すると、リソースが存在しない場合に作成できます。以下に例を示します。

1.  `Find Table`アクションを選択

2.  `set up action`ステップで、 `Create TiDB Cloud Table if it doesn’t exist yet?`ボックスにチェックを入れて`find and create`有効にします。

    ![Find and create](/media/tidb-cloud/zapier/zapier-tidbcloud-find-and-create.png)

このワークフローは、テーブルがまだ存在しない場合は作成します。アクションをテストすると、テーブルが直接作成されることに注意してください。
