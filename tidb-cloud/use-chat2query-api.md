---
title: Get Started with Chat2Query API
summary: 指示に従って、 TiDB Cloud Chat2Query API を使用して AI で SQL ステートメントを生成および実行する方法を学びます。
---

# Chat2Query APIを使い始める {#get-started-with-chat2query-api}

TiDB Cloud は、指示を与えることで AI を使用して SQL ステートメントを生成および実行できる RESTful インターフェースである Chat2Query API を提供します。その後、API がクエリ結果を返します。

Chat2Query API には HTTPS 経由でのみアクセスでき、ネットワーク経由で送信されるすべてのデータは TLS を使用して暗号化されます。

> **注記：**
>
> Chat2Query API は[TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターで使用できます。3 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスターで Chat2Query API を使用するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## 始める前に {#before-you-begin}

Chat2Query エンドポイントを呼び出す前に、Chat2Query データ アプリを作成し、データ アプリの API キーを作成する必要があります。

### Chat2Queryデータアプリを作成する {#create-a-chat2query-data-app}

プロジェクトのデータ アプリを作成するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページで、<mdsvgicon name="icon-create-data-app">左ペインで**DataApp を作成します**。データ アプリ作成ダイアログが表示されます。</mdsvgicon>

    > **ヒント：**
    >
    > クラスターの**SQL エディター**ページにいる場合は、右上隅の**...**をクリックし、 **API 経由で Chat2Query にアクセス**を選択して、**新しい Chat2Query データ アプリ**をクリックすることで、データ アプリ作成ダイアログを開くこともできます。

2.  ダイアログで、データ アプリの名前を定義し、データ ソースとして目的のクラスターを選択し、**データ アプリの**種類として**Chat2Query データ アプリ**を選択します。オプションで、アプリの説明を記述することもできます。

3.  **[作成]を**クリックします。

    新しく作成された Chat2Query データ アプリが左側のペインに表示されます。このデータ アプリの下に、Chat2Query エンドポイントのリストが表示されます。

### APIキーを作成する {#create-an-api-key}

エンドポイントを呼び出す前に、エンドポイントがTiDB Cloudクラスターのデータにアクセスするために使用する Chat2Query データ アプリの API キーを作成する必要があります。

API キーを作成するには、次の手順を実行します。

1.  [**データサービス**](https://tidbcloud.com/console/data-service)の左側のペインで、Chat2Query データ アプリをクリックすると、右側にその詳細が表示されます。

2.  **認証**領域で、 **「API キーの作成」を**クリックします。

3.  **「API キーの作成」**ダイアログで説明を入力し、API キーの次のいずれかのロールを選択します。

    -   `Chat2Query Admin` : API キーがデータ サマリーを管理し、提供された指示に基づいて SQL ステートメントを生成し、任意の SQL ステートメントを実行できるようにします。

    -   `Chat2Query Data Summary Management Role` : API キーによるデータ サマリーの生成と更新のみを許可します。

        > **ヒント：**
        >
        > Chat2Query API の場合、データ サマリーは、データベースの説明、テーブルの説明、列の説明など、AI によるデータベースの分析結果です。データベースのデータ サマリーを生成することで、指示を与えて SQL 文を生成するときに、より正確な応答を得ることができます。

    -   `Chat2Query SQL ReadOnly` : API キーは提供された指示に基づいて SQL ステートメントを生成し、 `SELECT` SQL ステートメントを実行することのみを許可します。

    -   `Chat2Query SQL ReadWrite` : API キーが提供された指示に基づいて SQL ステートメントを生成し、任意の SQL ステートメントを実行できるようにします。

4.  デフォルトでは、API キーの有効期限はありません。キーの有効期限を設定する場合は、 **[有効期限] を**クリックし、時間単位 ( `Minutes` `Days`または`Months` ) を選択して、時間単位に必要な数値を入力します。

5.  **「次へ」**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密鍵をコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密鍵を再度取得できなくなります。

6.  **「完了」を**クリックします。

## Chat2Queryエンドポイントを呼び出す {#call-chat2query-endpoints}

> **注記：**
>
> 各 Chat2Query データ アプリには、1 日あたり 100 リクエストのレート制限があります。レート制限を超えると、API は`429`エラーを返します。クォータを増やすには、サポート チームに[リクエストを送信する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)お問い合わせください。

各 Chat2Query データ アプリには、次のエンドポイントがあります。

-   Chat2Query v3 エンドポイント: `/v3/dataSummaries`や`/v3/chat2data`など、名前が`/v3`で始まるエンドポイント (推奨)
-   Chat2Query v2エンドポイント: `/v2/dataSummaries`や`/v2/chat2data`など、名前が`/v2`で始まるエンドポイント
-   Chat2Query v1 エンドポイント: `/v1/chat2data` (非推奨)

> **ヒント：**
>
> `/v1/chat2data`と比較すると、 `/v3/chat2data`と`/v2/chat2data`では、最初に`/v3/dataSummaries`または`/v2/dataSummaries`呼び出してデータベースを分析する必要があります。その結果、 `/v3/chat2data`と`/v2/chat2data`によって返される結果は通常より正確になります。

### エンドポイントのコード例を取得する {#get-the-code-example-of-an-endpoint}

TiDB Cloud は、 Chat2Query エンドポイントをすばやく呼び出すのに役立つコード例を提供します。Chat2Query エンドポイントのコード例を取得するには、次の手順を実行します。

1.  [**データサービス**](https://tidbcloud.com/console/data-service)ページの左側のペインで、Chat2Query エンドポイントの名前をクリックします。

    エンドポイント URL、コード例、リクエスト メソッドなど、このエンドポイントを呼び出すための情報が右側に表示されます。

2.  **コード例を表示を**クリックします。

3.  表示されたダイアログ ボックスで、エンドポイントの呼び出しに使用するクラスター、データベース、および認証方法を選択し、コード例をコピーします。

    > **注記：**
    >
    > `/v2/jobs/{job_id}`などの一部のエンドポイントでは、認証方法を選択するだけで済みます。

4.  エンドポイントを呼び出すには、アプリケーションに例を貼り付け、例のパラメータを独自のものに置き換えて (プレースホルダー`${PUBLIC_KEY}`と`${PRIVATE_KEY}`を API キーに置き換えるなど)、実行します。

### Chat2Query v3エンドポイントまたはv2エンドポイントを呼び出す {#call-chat2query-v3-endpoints-or-v2-endpoints}

TiDB Cloudデータ サービスは、次の Chat2Query v3 エンドポイントと v2 エンドポイントを提供します。

| 方法 | 終点                                                                | 説明                                                                                                                                                  |
| -- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 役職 | `/v3/dataSummaries`                                               | このエンドポイントは、分析に人工知能を使用して、データベース スキーマ、テーブル スキーマ、および列スキーマのデータ サマリーを生成します。                                                                              |
| 得る | `/v3/dataSummaries`                                               | このエンドポイントは、データベースのすべてのデータ概要を取得します。                                                                                                                  |
| 得る | `/v3/dataSummaries/{data_summary_id}`                             | このエンドポイントは、特定のデータの概要を取得します。                                                                                                                         |
| 置く | `/v3/dataSummaries/{data_summary_id}`                             | このエンドポイントは、特定のデータ サマリーを更新します。                                                                                                                       |
| 置く | `/v3/dataSummaries/{data_summary_id}/tables/{table_name}`         | このエンドポイントは、特定のデータ サマリー内の特定のテーブルの説明を更新します。                                                                                                           |
| 置く | `/v3/dataSummaries/{data_summary_id}/tables/{table_name}/columns` | このエンドポイントは、特定のデータ サマリー内の特定のテーブルの列の説明を更新します。                                                                                                         |
| 役職 | `/v3/knowledgeBases`                                              | このエンドポイントは新しいナレッジ ベースを作成します。ナレッジ ベース関連のエンドポイントの使用法の詳細については、 [ナレッジベースを使用する](/tidb-cloud/use-chat2query-knowledge.md)を参照してください。                       |
| 得る | `/v3/knowledgeBases`                                              | このエンドポイントはすべてのナレッジ ベースを取得します。                                                                                                                       |
| 得る | `/v3/knowledgeBases/{knowledge_base_id}`                          | このエンドポイントは特定のナレッジ ベースを取得します。                                                                                                                        |
| 置く | `/v3/knowledgeBases/{knowledge_base_id}`                          | このエンドポイントは特定のナレッジ ベースを更新します。                                                                                                                        |
| 役職 | `/v3/knowledgeBases/{knowledge_base_id}/data`                     | このエンドポイントは、特定のナレッジ ベースにデータを追加します。                                                                                                                   |
| 得る | `/v3/knowledgeBases/{knowledge_base_id}/data`                     | このエンドポイントは、特定のナレッジ ベースからデータを取得します。                                                                                                                  |
| 置く | `/v3/knowledgeBases/{knowledge_base_id}/data/{knowledge_data_id}` | このエンドポイントは、ナレッジ ベース内の特定のデータを更新します。                                                                                                                  |
| 削除 | `/v3/knowledgeBases/{knowledge_base_id}/data/{knowledge_data_id}` | このエンドポイントは、ナレッジ ベースから特定のデータを削除します。                                                                                                                  |
| 役職 | `/v3/sessions`                                                    | このエンドポイントは新しいセッションを作成します。セッション関連のエンドポイントの使用法の詳細については、 [マルチラウンドChat2Queryを開始する](/tidb-cloud/use-chat2query-sessions.md)を参照してください。                    |
| 得る | `/v3/sessions`                                                    | このエンドポイントは、すべてのセッションのリストを取得します。                                                                                                                     |
| 得る | `/v3/sessions/{session_id}`                                       | このエンドポイントは、特定のセッションの詳細を取得します。                                                                                                                       |
| 置く | `/v3/sessions/{session_id}`                                       | このエンドポイントは特定のセッションを更新します。                                                                                                                           |
| 置く | `/v3/sessions/{session_id}/reset`                                 | このエンドポイントは特定のセッションをリセットします。                                                                                                                         |
| 役職 | `/v3/sessions/{session_id}/chat2data`                             | このエンドポイントは、人工知能を使用して特定のセッション内で SQL ステートメントを生成し、実行します。詳細については、 [セッションを使用してマルチラウンド Chat2Query を開始する](/tidb-cloud/use-chat2query-sessions.md)参照してください。 |
| 役職 | `/v3/chat2data`                                                   | このエンドポイントを使用すると、データ サマリー ID と指示を提供することで、人工知能を使用して SQL ステートメントを生成および実行できます。                                                                          |
| 役職 | `/v3/refineSql`                                                   | このエンドポイントは、人工知能を使用して既存の SQL クエリを改良します。                                                                                                              |
| 役職 | `/v3/suggestQuestions`                                            | このエンドポイントは、提供されたデータの概要に基づいて質問を提案します。                                                                                                                |
| 役職 | `/v2/dataSummaries`                                               | このエンドポイントは、人工知能を使用して、データベース スキーマ、テーブル スキーマ、列スキーマのデータ サマリーを生成します。                                                                                    |
| 得る | `/v2/dataSummaries`                                               | このエンドポイントはすべてのデータ概要を取得します。                                                                                                                          |
| 役職 | `/v2/chat2data`                                                   | このエンドポイントを使用すると、データ サマリー ID と指示を提供することで、人工知能を使用して SQL ステートメントを生成および実行できます。                                                                          |
| 得る | `/v2/jobs/{job_id}`                                               | このエンドポイントを使用すると、特定のデータ サマリー生成ジョブのステータスを照会できます。                                                                                                      |

`/v3/chat2data`と`/v2/chat2data`を呼び出す手順は同じです。次のセクションでは、 `/v3/chat2data`例にして、その呼び出し方法を説明します。

#### 1. <code>/v3/dataSummaries</code>を呼び出してデータサマリーを生成する {#1-generate-a-data-summary-by-calling-code-v3-datasummaries-code}

`/v3/chat2data`を呼び出す前に、まず`/v3/dataSummaries`呼び出して AI にデータベースを分析してデータの概要を生成させます。そうすることで、後で`/v3/chat2data` SQL 生成でより良いパフォーマンスを得ることができます。

以下は、 `/v3/dataSummaries`呼び出して`sp500insight`データベースを分析し、データベースのデータ概要を生成するコード例です。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/dataSummaries'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "description": "Data summary for SP500 Insight",
    "reuse": false
}'
```

上記の例では、リクエスト本体は次のプロパティを持つ JSON オブジェクトです。

-   `cluster_id` :*文字列*。TiDB クラスターの一意の識別子。
-   `database` :*文字列*。データベースの名前。
-   `description` :*文字列*。データ概要の説明。
-   `reuse` :*ブール値*。既存のデータ サマリーを再利用するかどうかを指定します。 `true`に設定すると、API は既存のデータ サマリーを再利用します。 `false`に設定すると、API は新しいデータ サマリーを生成します。

応答の例は次のとおりです。

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "data_summary_id": 304823,
    "job_id": "fb99ef785da640ab87bf69afed60903d"
  }
}
```

#### 2. <code>/v2/jobs/{job_id}</code>を呼び出して分析ステータスを確認します。 {#2-check-the-analysis-status-by-calling-code-v2-jobs-job-id-code}

`/v3/dataSummaries` API は非同期です。大規模なデータセットを持つデータベースの場合、データベース分析を完了して完全なデータの概要を返すまでに数分かかることがあります。

データベースの分析ステータスを確認するには、次のように`/v2/jobs/{job_id}`エンドポイントを呼び出します。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>`/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

応答の例は次のとおりです。

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1699518950, // A UNIX timestamp indicating when the job is finished
    "job_id": "fb99ef785da640ab87bf69afed60903d", // ID of current job
    "result": DataSummaryObject, // AI exploration information of the given database
    "status": "done" // Status of the current job
  }
}
```

`"status"`が`"done"`の場合、完全なデータ サマリーは準備できており、 `/v3/chat2data`を呼び出してこのデータベースの SQL ステートメントを生成して実行できます。それ以外の場合は、分析が完了するまで待って、後で分析ステータスを確認する必要があります。

レスポンスの`DataSummaryObject` 、指定されたデータベースのAI探索情報を表します。3 `DataSummaryObject`構造は次のとおりです。

```js
{
    "cluster_id": "10140100115280519574", // The cluster ID
    "data_summary_id": 304823, // The data summary ID
    "database": "sp500insight", // The database name
    "default": false, // Whether this data summary is the default one
    "status": "done", // The status of the data summary
    "description": {
        "system": "Data source for financial analysis and decision-making in stock market", // The description of the data summary generated by AI
        "user": "Data summary for SP500 Insight" // The description of the data summary provided by the user
    },
    "keywords": ["User_Stock_Selection", "Index_Composition"], // Keywords of the data summary
    "relationships": {
        "companies": {
            "referencing_table": "...", // The table that references the `companies` table
            "referencing_table_column": "..." // The column that references the `companies` table
            "referenced_table": "...", // The table that the `companies` table references
            "referenced_table_column": "..." // The column that the `companies` table references
        }
    }, // Relationships between tables
    "summary": "Financial data source for stock market analysis", // The summary of the data summary
    "tables": { // Tables in the database
      "companies": {
        "name": "companies" // The table name
        "description": "This table provides comprehensive...", // The description of the table
        "columns": {
          "city": { // Columns in the table
            "name": "city" // The column name
            "description": "The city where the company is headquartered.", // The description of the column
          }
        },
      },
    }
}
```

#### 3. <code>/v3/chat2data</code>を呼び出してSQL文を生成し実行する {#3-generate-and-execute-sql-statements-by-calling-code-v3-chat2data-code}

データベースのデータ概要が準備できたら、クラスター ID、データベース名、質問を指定して`/v3/chat2data`呼び出して SQL ステートメントを生成し、実行できます。

例えば：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "question": "<Your question to generate data>",
    "sql_generate_mode": "direct"
}'
```

リクエスト本体は、次のプロパティを持つ JSON オブジェクトです。

-   `cluster_id` :*文字列*。TiDB クラスターの一意の識別子。
-   `database` :*文字列*。データベースの名前。
-   `data_summary_id` :*整数*。SQL の生成に使用されるデータ サマリーの ID。このプロパティは、 `cluster_id`と`database`が指定されていない場合にのみ有効になります。 `cluster_id`と`database`両方を指定すると、API はデータベースのデフォルトのデータ サマリーを使用します。
-   `question` :*文字列*。必要なクエリを説明する自然言語での質問。
-   `sql_generate_mode` :*文字列*。SQL 文を生成するモード。値は`direct`または`auto_breakdown`です。 `direct`に設定すると、API は指定した`question`に基づいて SQL 文を直接生成します。 `auto_breakdown`に設定すると、API は`question`複数のタスクに分割し、各タスクの SQL 文を生成します。

応答の例は次のとおりです。

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "job_id": "20f7577088154d7889964f1a5b12cb26",
    "session_id": 304832
  }
}
```

次のようにステータス コード`400`の応答を受け取った場合は、データ サマリーが準備されるまでしばらく待つ必要があることを意味します。

```js
{
    "code": 400,
    "msg": "Data summary is not ready, please wait for a while and retry",
    "result": {}
}
```

`/v3/chat2data` API は非同期です。3 エンドポイント`/v2/jobs/{job_id}`呼び出すことでジョブのステータスを確認できます。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

応答の例は次のとおりです。

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1718785006, // A UNIX timestamp indicating when the job is finished
    "job_id": "20f7577088154d7889964f1a5b12cb26",
    "reason": "", // The reason for the job failure if the job fails
    "result": {
      "assumptions": [],
      "chart_options": { // The generated chart options for the result
        "chart_name": "Table",
        "option": {
          "columns": [
            "total_users"
          ]
        },
        "title": "Total Number of Users in the Database"
      },
      "clarified_task": "Count the total number of users in the database.", // The clarified description of the task
      "data": { // The data returned by the SQL statement
        "columns": [
          {
            "col": "total_users"
          }
        ],
        "rows": [
          [
            "1"
          ]
        ]
      },
      "description": "",
      "sql": "SELECT COUNT(`user_id`) AS total_users FROM `users`;", // The generated SQL statement
      "sql_error": null, // The error message of the SQL statement
      "status": "done", // The status of the job
      "task_id": "0",
      "type": "data_retrieval" // The type of the job
    },
    "status": "done"
  }
}
```

### Chat2Data v1エンドポイントを呼び出す（非推奨） {#call-the-chat2data-v1-endpoint-deprecated}

> **注記：**
>
> Chat2Data v1 エンドポイントは非推奨です。代わりに Chat2Data v3 エンドポイントを呼び出すことをお勧めします。

TiDB Cloudデータ サービスは、次の Chat2Query v1 エンドポイントを提供します。

| 方法 | 終点              | 説明                                                                       |
| -- | --------------- | ------------------------------------------------------------------------ |
| 役職 | `/v1/chat2data` | このエンドポイントを使用すると、ターゲット データベース名と指示を指定して、人工知能を使用して SQL ステートメントを生成および実行できます。 |

`/v1/chat2data`エンドポイントを直接呼び出して、SQL ステートメントを生成および実行できます。 `/v2/chat2data`と比較すると、 `/v1/chat2data`応答が速くなりますが、パフォーマンスは低くなります。

TiDB Cloud は、エンドポイントを呼び出すのに役立つコード例を生成します。例を取得してコードを実行するには、 [エンドポイントのコード例を取得する](#get-the-code-example-of-an-endpoint)参照してください。

`/v1/chat2data`呼び出すときは、次のパラメータを置き換える必要があります。

-   プレースホルダー`${PUBLIC_KEY}`と`${PRIVATE_KEY}`を API キーに置き換えます。
-   `<your table name, optional>`プレースホルダーを、クエリするテーブル名に置き換えます。テーブル名を指定しないと、AI はデータベース内のすべてのテーブルをクエリします。
-   `<your instruction>`プレースホルダーを、AI に SQL ステートメントを生成および実行させる命令に置き換えます。

> **注記：**
>
> 各 Chat2Query データ アプリには、1 日あたり 100 リクエストのレート制限があります。レート制限を超えると、API は`429`エラーを返します。クォータを増やすには、サポート チームに[リクエストを送信する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)リクエストしてください。ロール`Chat2Query Data Summary Management Role`の API キーでは、Chat2Data v1 エンドポイントを呼び出すことはできません。次のコード例は、 `sp500insight.users`内のユーザー数をカウントするために使用されます。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10939961583884005252",
    "database": "sp500insight",
    "tables": ["users"],
    "instruction": "count the users"
}'
```

上記の例では、リクエスト本体は次のプロパティを持つ JSON オブジェクトです。

-   `cluster_id` :*文字列*。TiDB クラスターの一意の識別子。
-   `database` :*文字列*。データベースの名前。
-   `tables` :*配列*。(オプション) クエリするテーブル名のリスト。
-   `instruction` :*文字列*。必要なクエリを説明する自然言語の命令。

応答は次のとおりです。

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [
      {
        "col": "COUNT(`user_id`)",
        "data_type": "BIGINT",
        "nullable": false
      }
    ],
    "rows": [
      {
        "COUNT(`user_id`)": "1"
      }
    ],
    "result": {
      "code": 200,
      "message": "Query OK!",
      "start_ms": 1699529488292,
      "end_ms": 1699529491901,
      "latency": "3.609656403s",
      "row_count": 1,
      "row_affect": 0,
      "limit": 1000,
      "sql": "SELECT COUNT(`user_id`) FROM `users`;",
      "ai_latency": "3.054822491s"
    }
  }
}
```

API 呼び出しが成功しなかった場合は、 `200`以外のステータス コードが返されます。以下は、 `500`ステータス コードの例です。

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [],
    "rows": [],
    "result": {
      "code": 500,
      "message": "internal error! defaultPermissionHelper: rpc error: code = DeadlineExceeded desc = context deadline exceeded",
      "start_ms": "",
      "end_ms": "",
      "latency": "",
      "row_count": 0,
      "row_affect": 0,
      "limit": 0
    }
  }
}
```

## もっと詳しく知る {#learn-more}

-   [APIキーを管理する](/tidb-cloud/data-service-api-key.md)
-   [マルチラウンドChat2Queryを開始する](/tidb-cloud/use-chat2query-sessions.md)
-   [ナレッジベースを使用する](/tidb-cloud/use-chat2query-knowledge.md)
-   [データサービスの応答コードとステータスコード](/tidb-cloud/data-service-response-and-status-code.md)
