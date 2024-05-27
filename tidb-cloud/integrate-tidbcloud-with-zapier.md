---
title: Integrate TiDB Cloud with Zapier
summary: Zapier を使用してTiDB Cloudを 5000 以上のアプリに接続する方法を学びます。
---

# TiDB Cloudを Zapier と統合する {#integrate-tidb-cloud-with-zapier}

[ザピエール](https://zapier.com)は、何千ものアプリやサービスが関与するワークフローを簡単に作成できるコード不要の自動化ツールです。

Zapier の[TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)を使用すると、次のことが可能になります。

-   MySQL 互換の HTAP データベースである TiDB を使用します。ローカルで構築する必要はありません。
-   TiDB Cloudの管理が簡単になります。
-   TiDB Cloud を5000 以上のアプリに接続し、ワークフローを自動化します。

このガイドでは、Zapier 上のTiDB Cloudアプリの概要と、その使用方法の例を示します。

## テンプレートを使ったクイックスタート {#quick-start-with-template}

[Zap テンプレート](https://platform.zapier.com/partners/zap-templates) 、公開されている Zapier 統合用に、アプリとコア フィールドが事前に選択された、すぐに使用できる統合または Zap です。

このセクションでは、ワークフローを作成する例として**、「新しい Github グローバル イベントを TiDB 行に追加する」**テンプレートを使用します。このワークフローでは、GitHub アカウントから新しいグローバル イベント (任意のリポジトリで、自分からまたは自分に対して[GitHub イベント](https://docs.github.com/en/developers/webhooks-and-events/events/github-event-types)発生するイベント) が作成されるたびに、Zapier によってTiDB Cloudクラスターに新しい行が追加されます。

### 前提条件 {#prerequisites}

始める前に、次のものが必要です。

-   A [Zapierアカウント](https://zapier.com/app/login) 。
-   A [GitHub アカウント](https://github.com/login) 。
-   [TiDB Cloudアカウント](https://tidbcloud.com/signup)およびTiDB Cloud上の TiDB Serverless クラスター。詳細については、 [TiDB Cloudクイック スタート](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster)を参照してください。

### ステップ1: テンプレートを取得する {#step-1-get-the-template}

[Zapier のTiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)に進みます。 **「新しい Github グローバル イベントを TiDB 行に追加する」**テンプレートを選択し、 **「試してみる」**をクリックします。すると、エディター ページが表示されます。

### ステップ2: トリガーを設定する {#step-2-set-up-the-trigger}

エディターページでトリガーとアクションを確認できます。トリガーをクリックして設定します。

1.  アプリとイベントを選択

    テンプレートではアプリとイベントがデフォルトで設定されているため、ここでは何もする必要はありません。 **[続行]**をクリックします。

2.  アカウントを選択

    TiDB Cloudに接続する GitHub アカウントを選択します。新しいアカウントを接続するか、既存のアカウントを選択できます。設定したら、 **「続行」**をクリックします。

3.  トリガーを設定する

    テンプレートではデフォルトでトリガーが設定されています。 **[続行]**をクリックします。

4.  テストトリガー

    **「トリガーのテスト」**をクリックします。トリガーが正常に設定されていれば、GitHub アカウントからの新しいグローバル イベントのデータを確認できます。 **「続行」**をクリックします。

### ステップ3: <code>Find Table in TiDB Cloud</code>を設定する {#step-3-set-up-the-code-find-table-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートで設定されたデフォルト値`Find Table`をそのままにし、 **[続行] を**クリックします。

2.  アカウントを選択

    1.  **「サインイン」**ボタンをクリックすると、新しいログインページにリダイレクトされます。
    2.  ログインページで、公開鍵と秘密鍵を入力します。TiDB TiDB Cloud API キーを取得するには、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)手順に従ってください。
    3.  **「続行」を**クリックします。

    ![Account](/media/tidb-cloud/zapier/zapier-tidbcloud-account.png)

3.  アクションの設定

    この手順では、イベント データを保存するために、 TiDB Cloudクラスター内のテーブルを指定する必要があります。テーブルがまだない場合は、この手順で作成できます。

    1.  ドロップダウンリストからプロジェクト名とクラスター名を選択します。クラスターの接続情報が自動的に表示されます。

        ![Set up project name and cluster name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-project-and-cluster.png)

    2.  パスワードを入力してください。

    3.  ドロップダウンリストからデータベースを選択します。

        ![Set up database name](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-databse.png)

        Zapier は、入力したパスワードを使用してTiDB Cloudからデータベースを照会します。クラスター内にデータベースが見つからない場合は、パスワードを再入力してページを更新してください。

    4.  **検索するテーブルボックス**に`github_global_event`を入力します。テーブルが存在しない場合は、テンプレートは次の DDL を使用してテーブルを作成します。 **[続行]**をクリックします。

        ![The create table DDL](/media/tidb-cloud/zapier/zapier-tidbcloud-create-table-ddl.png)

4.  テストアクション

    **「テストアクション」**をクリックすると、Zapier がテーブルを作成します。テストをスキップして、このワークフローが初めて実行されるときにテーブルを作成することもできます。

### ステップ4: <code>Create Row in TiDB Cloud</code>アクションを設定する {#step-4-set-up-the-code-create-row-in-tidb-cloud-code-action}

1.  アプリとイベントを選択

    テンプレートによって設定されたデフォルト値をそのままにし、 **「続行」**をクリックします。

2.  アカウントを選択

    `Find Table in TiDB Cloud`アクションの設定時に選択したアカウントを選択します。 **[続行]**をクリックします。

    ![Choose account](/media/tidb-cloud/zapier/zapier-tidbcloud-choose-account.png)

3.  アクションの設定

    1.  前の手順と同様に**、プロジェクト名**、**クラスタ名**、 **TiDB パスワード**、**データベース名**を入力します。

    2.  **テーブル名**で、ドロップダウン リストから**github_global_event**テーブルを選択します。テーブルの列が表示されます。

        ![Table columns](/media/tidb-cloud/zapier/zapier-set-up-tidbcloud-columns.png)

    3.  **「列」**ボックスで、トリガーから対応するデータを選択します。すべての列に入力し、 **「続行」**をクリックします。

        ![Fill in Columns](/media/tidb-cloud/zapier/zapier-fill-in-tidbcloud-triggers-data.png)

4.  テストアクション

    **「テストアクション」**をクリックして、テーブルに新しい行を作成します。TiDB TiDB Cloudクラスターを確認すると、データが正常に書き込まれていることがわかります。

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

**「公開」**をクリックして、zap を公開します。3 [ホームページ](https://zapier.com/app/zaps) zap が実行されているのがわかります。

![Publish the zap](/media/tidb-cloud/zapier/zapier-tidbcloud-publish.png)

これで、この zap は GitHub アカウントからのすべてのグローバル イベントをTiDB Cloudに自動的に記録します。

## トリガーとアクション {#triggers-x26-actions}

[トリガーとアクション](https://zapier.com/how-it-works)は Zapier の重要な概念です。さまざまなトリガーとアクションを組み合わせることで、さまざまな自動化ワークフローを作成できます。

このセクションでは、Zapier 上のTiDB Cloud App によって提供されるトリガーとアクションについて説明します。

### トリガー {#triggers}

次の表は、TiDB Cloud App でサポートされているトリガーを示しています。

| 引き金             | 説明                                         |
| --------------- | ------------------------------------------ |
| 新しいクラスタ         | 新しいクラスターが作成された場合にトリガーされます。                 |
| 新しいテーブル         | 新しいテーブルが作成された時にトリガーされます。                   |
| 新しい行            | 新しい行が作成された場合にトリガーされます。最近の 10000 行のみを取得します。 |
| 新しい行 (カスタム クエリ) | 指定したカスタム クエリから新しい行が返されたときにトリガーされます。        |

### 行動 {#actions}

次の表は、TiDB Cloud App でサポートされているアクションの一覧です。一部のアクションには追加のリソースが必要なため、アクションを使用する前に対応するリソースを準備する必要があることに注意してください。

| アクション           | 説明                                                  | リソース                          |
| --------------- | --------------------------------------------------- | ----------------------------- |
| クラスタを見つける       | 既存の TiDB Serverless または TiDB Dedicated クラスターを検索します。 | なし                            |
| クラスタの作成         | 新しいクラスターを作成します。TiDB Serverless クラスターの作成のみをサポートします。  | なし                            |
| データベースを検索       | 既存のデータベースを検索します。                                    | TiDB サーバーレス クラスター             |
| データベースの作成       | 新しいデータベースを作成します。                                    | TiDB サーバーレス クラスター             |
| テーブルを探す         | 既存のテーブルを検索します。                                      | TiDB サーバーレス クラスターとデータベース      |
| テーブルを作成         | 新しいテーブルを作成します。                                      | TiDB サーバーレス クラスターとデータベース      |
| 行を作成            | 新しい行を作成します。                                         | TiDB サーバーレス クラスター、データベース、テーブル |
| 行を更新            | 既存の行を更新します。                                         | TiDB サーバーレス クラスター、データベース、テーブル |
| 行を検索            | ルックアップ列を使用してテーブル内の行を検索します。                          | TiDB サーバーレス クラスター、データベース、テーブル |
| 行の検索 (カスタム クエリ) | 指定したカスタム クエリを使用してテーブル内の行を検索します。                     | TiDB サーバーレス クラスター、データベース、テーブル |

## TiDB Cloudアプリ テンプレート {#tidb-cloud-app-templates}

TiDB Cloud は、 Zapier で直接使用できるテンプレートをいくつか提供しています。すべてのテンプレートは[TiDB Cloudアプリ](https://zapier.com/apps/tidb-cloud/integrations)ページで見つかります。

ここではいくつかの例を示します。

-   [Google スプレッドシートで新しいTiDB Cloud行を複製する](https://zapier.com/apps/google-sheets/integrations/tidb-cloud/1134881/duplicate-new-tidb-cloud-rows-in-google-sheets) 。
-   [新しいカスタム TiDB クエリから Gmail 経由でメールを送信する](https://zapier.com/apps/gmail/integrations/tidb-cloud/1134903/send-emails-via-gmail-from-new-custom-tidb-queries) 。
-   [新しくキャッチしたウェブフックからTiDB Cloudに行を追加する](https://zapier.com/apps/tidb-cloud/integrations/webhook/1134955/add-rows-to-tidb-cloud-from-newly-caught-webhooks) 。
-   [新しい Salesforce 連絡先を TiDB 行に保存する](https://zapier.com/apps/salesforce/integrations/tidb-cloud/1134923/store-new-salesforce-contacts-on-tidb-rows) 。
-   [履歴書付きの新しい Gmail メールの TiDB 行を作成し、Slack 通知を直接送信する](https://zapier.com/apps/gmail/integrations/slack/1135456/create-tidb-rows-for-new-gmail-emails-with-resumes-and-send-direct-slack-notifications)

## FAQ {#faq}

### Zapier でTiDB Cloudアカウントを設定するにはどうすればよいですか? {#how-can-i-set-up-the-tidb-cloud-account-in-zapier}

Zapier では、TiDB Cloudアカウントに接続するために**TiDB Cloud API キーが**必要です。Zapier では、TiDB Cloudのログイン アカウントは必要ありません。

TiDB Cloud API キーを取得するには、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)に従ってください。

### TiDB Cloudトリガーは重複排除をどのように実行しますか? {#how-do-tidb-cloud-triggers-perform-de-duplication}

Zapier トリガーはポーリング API 呼び出しと連携して、定期的に新しいデータをチェックできます (間隔は Zapier プランによって異なります)。

TiDB Cloudトリガーは、多くの結果を返すポーリング API 呼び出しを提供します。ただし、結果のほとんどは Zapier で以前に確認されたものであり、つまり、結果のほとんどは重複しています。

API 内の項目が複数の異なるポーリングに存在する場合にアクションを複数回トリガーしたくないため、 TiDB Cloud は`id`フィールドを使用してデータの重複を排除します。

`New Cluster`および`New Table`トリガーは、重複排除を実行するために、単に`cluster_id`または`table_id` `id`フィールドとして使用します。2 つのトリガーに対しては何もする必要はありません。

**新しい行トリガー**

`New Row`トリガーは、フェッチごとに 10,000 件の結果を制限します。したがって、10,000 件の結果に含まれていない新しい行がある場合、Zapier をトリガーできません。

これを回避する 1 つの方法は、トリガーで`Order By`構成を指定することです。たとえば、行を作成時刻で並べ替えると、新しい行は常に 10,000 件の結果に含まれます。

`New Row`トリガーは、重複排除を行うために`id`フィールドを生成するためにも柔軟な戦略を使用します。トリガーは、次の順序で`id`フィールドを生成します。

1.  結果に`id`列目が含まれる場合は、 `id`列目を使用します。
2.  トリガー構成で`Dedupe Key`指定する場合は、 `Dedupe Key`使用します。
3.  テーブルに主キーがある場合は、主キーを使用します。主キーが複数ある場合は、最初の列を使用します。
4.  テーブルに一意のキーがある場合は、その一意のキーを使用します。
5.  表の最初の列を使用します。

**新しい行（カスタムクエリ）トリガー**

`New Row (Custom Query)`トリガーは、フェッチごとに 1,000,000 件の結果を制限します。1,000,000 は大きな数であり、システム全体を保護するためにのみ設定されます。クエリには`ORDER BY`と`LIMIT`含めることをお勧めします。

重複排除を実行するには、クエリ結果に一意の ID フィールドが必要です。そうでない場合は、エラー`You must return the results with id field`が発生します。

カスタム クエリが 30 秒以内に実行されることを確認してください。そうでない場合、タイムアウト エラーが発生します。

### <code>find or create</code>アクションを使用するにはどうすればよいですか? {#how-do-i-use-the-code-find-or-create-code-action}

`Find or create`アクションを使用すると、リソースが存在しない場合にリソースを作成できます。次に例を示します。

1.  `Find Table`アクションを選択

2.  `set up action`ステップで、 `Create TiDB Cloud Table if it doesn’t exist yet?`ボックスにチェックを入れて`find and create`を有効にします。

    ![Find and create](/media/tidb-cloud/zapier/zapier-tidbcloud-find-and-create.png)

このワークフローは、テーブルがまだ存在しない場合にテーブルを作成します。アクションをテストすると、テーブルが直接作成されることに注意してください。
