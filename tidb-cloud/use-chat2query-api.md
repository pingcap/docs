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

## ステップ1. Chat2Queryデータアプリを作成する {#step-1-create-a-chat2query-data-app}

プロジェクトのデータ アプリを作成するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページで、<mdsvgicon name="icon-create-data-app">左ペインで**DataApp を作成します**。データ アプリ作成ダイアログが表示されます。</mdsvgicon>

    > **ヒント：**
    >
    > クラスターの**Chat2Query**ページにいる場合は、右上隅の**...**をクリックし、 **API 経由で Chat2Query にアクセス**を選択して、**新しい Chat2Query データ アプリ**をクリックすることで、データ アプリ作成ダイアログを開くこともできます。

2.  ダイアログで、データ アプリの名前を定義し、データ ソースとして目的のクラスターを選択し、**データ アプリの**種類として**Chat2Query データ アプリ**を選択します。オプションで、アプリの説明を記述することもできます。

3.  **[作成]を**クリックします。

    新しく作成された Chat2Query データ アプリが左側のペインに表示されます。このデータ アプリの下に、Chat2Query エンドポイントのリストが表示されます。

## ステップ2. APIキーを作成する {#step-2-create-an-api-key}

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

4.  **「次へ」**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密鍵をコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密鍵を再度取得できなくなります。

5.  **「完了」を**クリックします。

## ステップ3. Chat2Queryエンドポイントを呼び出す {#step-3-call-chat2query-endpoints}

> **注記：**
>
> 各 Chat2Query データ アプリには、1 日あたり 100 リクエストのレート制限があります。レート制限を超えると、API は`429`エラーを返します。クォータを増やすには、サポート チームに[リクエストを送信する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)お問い合わせください。

各 Chat2Query データ アプリには、次のエンドポイントがあります。

-   Chat2Query v1 エンドポイント: `/v1/chat2data`
-   Chat2Query v2エンドポイント: `/v2/dataSummaries`や`/v2/chat2data`など、名前が`/v2`で始まるエンドポイント

> **ヒント：**
>
> `/v1/chat2data`と比較すると、 `/v2/chat2data`最初に`/v2/dataSummaries`呼び出してデータベースを分析する必要があるため、 `/v2/chat2data`によって返される結果は通常より正確です。

### エンドポイントのコード例を取得する {#get-the-code-example-of-an-endpoint}

TiDB Cloud は、 Chat2Query エンドポイントをすばやく呼び出すのに役立つコード例を提供します。Chat2Query エンドポイントのコード例を取得するには、次の手順を実行します。

1.  [**データサービス**](https://tidbcloud.com/console/data-service)ページの左側のペインで、Chat2Query エンドポイントの名前をクリックします。

    エンドポイント URL、コード例、リクエスト メソッドなど、このエンドポイントを呼び出すための情報が右側に表示されます。

2.  **コード例を表示を**クリックします。

3.  表示されたダイアログ ボックスで、エンドポイントの呼び出しに使用するクラスター、データベース、および認証方法を選択し、コード例をコピーします。

    > **注記：**
    >
    > `/v2/chat2data`と`/v2/jobs/{job_id}`については、認証方法を選択するだけです。

4.  エンドポイントを呼び出すには、アプリケーションに例を貼り付け、例のパラメータを独自のものに置き換えて (プレースホルダー`${PUBLIC_KEY}`と`${PRIVATE_KEY}`を API キーに置き換えるなど)、実行します。

### Chat2Query v2エンドポイントを呼び出す {#call-chat2query-v2-endpoints}

TiDB Cloudデータ サービスは、次の Chat2Query v2 エンドポイントを提供します。

| 方法 | 終点                  | 説明                                                                         |
| -- | ------------------- | -------------------------------------------------------------------------- |
| 役職 | `/v2/dataSummaries` | このエンドポイントは、分析に人工知能を使用して、データベース スキーマ、テーブル スキーマ、列スキーマのデータ サマリーを生成します。        |
| 役職 | `/v2/chat2data`     | このエンドポイントを使用すると、データ サマリー ID と指示を提供することで、人工知能を使用して SQL ステートメントを生成および実行できます。 |
| 得る | `/v2/jobs/{job_id}` | このエンドポイントを使用すると、データ サマリー生成ジョブのステータスを照会できます。                                |

以降のセクションでは、これらのエンドポイントを呼び出す方法を学習します。

#### 1. <code>/v2/dataSummaries</code>を呼び出してデータサマリーを生成する {#1-generate-a-data-summary-by-calling-code-v2-datasummaries-code}

`/v2/chat2data`を呼び出す前に、まず`/v2/dataSummaries`呼び出して AI にデータベースを分析してデータの概要を生成させます。そうすることで、後で`/v2/chat2data` SQL 生成でより良いパフォーマンスを得ることができます。

以下は、 `/v2/chat2data`呼び出して`sp500insight`データベースを分析し、データベースのデータ概要を生成するコード例です。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/dataSummaries'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10939961583884005252",
    "database": "sp500insight"
}'
```

上記の例では、リクエスト本体は次のプロパティを持つ JSON オブジェクトです。

-   `cluster_id` :*文字列*。TiDB クラスターの一意の識別子。
-   `database` :*文字列*。データベースの名前。

応答の例は次のとおりです。

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "data_summary_id": 481235,
    "job_id": "79c2b3d36c074943ab06a29e45dd5887"
  }
}
```

#### 2. <code>/v2/jobs/{job_id}</code>を呼び出して分析ステータスを確認します。 {#2-check-the-analysis-status-by-calling-code-v2-jobs-job-id-code}

`/v2/dataSummaries` API は非同期です。大規模なデータセットを持つデータベースの場合、データベース分析を完了して完全なデータの概要を返すまでに数分かかることがあります。

データベースの分析ステータスを確認するには、次のように`/v2/jobs/{job_id}`エンドポイントを呼び出します。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>`/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

応答の例は次のとおりです。

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1699518950, // A UNIX timestamp indicating when the job is finished
    "job_id": "79c2b3d36c074943ab06a29e45dd5887",  // ID of current job
    "result": DataSummaryObject, // AI exploration information of the given database
    "status": "done" // Status of the current job
  }
}
```

`"status"`が`"done"`の場合、完全なデータ サマリーは準備できており、 `/v2/chat2data`を呼び出してこのデータベースの SQL ステートメントを生成して実行できます。それ以外の場合は、分析が完了するまで待って、後で分析ステータスを確認する必要があります。

レスポンスの`DataSummaryObject` 、指定されたデータベースのAI探索情報を表します。3 `DataSummaryObject`構造は次のとおりです。

```json
{
    "cluster_id": 10939961583884005252, // Your cluster id
    "db_name": "sp500insight", // Database name
    "db_schema": { // Database schema information
        "users": { // A table named "users"
            "columns": { // Columns in table "users"
                "user_id": {
                    "default": null,
                    "description": "The unique identifier for each user.",
                    "name": "user_id",
                    "nullable": true,
                    "type": "int(11)"
                }
            },
            "description": "This table represents the user data and includes the date and time when each user was created.",
            "key_attributes": [ // Key attributes of table "user"
                "user_id",
            ],
            "primary_key": "id",
            "table_name": "users", // Table name in the database
        }
    },
    "entity": { // Entities abstracted by AI
        "users": {
            "attributes": ["user_id"],
            "involved_tables": ["users"],
            "name": "users",
            "summary": "This table represents the user data and includes the date and time when each user was created."
        }
    },
    "org_id": 30061,
    "project_id": 3198952,
    "short_summary": "Comprehensive finance data for analysis and decision-making.",
    "status": "done",
    "summary": "This data source contains information about companies, indexes, and historical stock price data. It is used for financial analysis, investment decision-making, and market research in the finance domain.",
    "summary_keywords": [
        "users"
    ],
    "table_relationship": {}
}
```

#### 3. <code>/v2/chat2data</code>を呼び出してSQL文を生成し実行する {#3-generate-and-execute-sql-statements-by-calling-code-v2-chat2data-code}

データベースのデータ概要が準備できたら、クラスター ID、データベース名、質問を指定して`/v2/chat2data`呼び出して SQL ステートメントを生成し、実行できます。

例えば：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
  "cluster_id": "10939961583884005252",
  "database": "sp500insight",
  "raw_question": "<Your question to generate data>"
}'
```

上記のコードでは、リクエスト本文は次のプロパティを持つ JSON オブジェクトです。

-   `cluster_id` :*文字列*。TiDB クラスターの一意の識別子。
-   `database` :*文字列*。データベースの名前。
-   `raw_question` :*文字列*。必要なクエリを記述する自然言語。

応答の例は次のとおりです。

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "job_id": "3966d5bd95324a6283445e3a02ccd97c"
  }
}
```

次のようにステータス コード`400`の応答を受け取った場合は、データ サマリーが準備されるまでしばらく待つ必要があることを意味します。

```json
{
    "code": 400,
    "msg": "Data summary is not ready, please wait for a while and retry",
    "result": {}
}
```

`/v2/chat2data` API は非同期です。3 エンドポイント`/v2/jobs/{job_id}`呼び出すことでジョブのステータスを確認できます。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

応答の例は次のとおりです。

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1699581661,
    "job_id": "3966d5bd95324a6283445e3a02ccd97c",
    "result": {
      "question_id": "8c4c15cf-a808-45b8-bff7-2ca819a1b6d5",
      "raw_question": "count the users", // The original question you provide
      "task_tree": {
        "0": {
          "clarified_task": "count the users", // Task that AI understands
          "description": "",
          "columns": [ // Columns that are queried in the generated SQL statement
            {
              "col": "user_count"
            }
          ],
          "rows": [ // Query result of generated SQL statement
            [
              "1"
            ]
          ],
          "sequence_no": 0,
          "sql": "SELECT COUNT(`user_id`) AS `user_count` FROM `users`;",
          "task": "count the users",
          "task_id": "0"
        }
      },
      "time_elapsed": 3.854671001434326
    },
    "status": "done"
  }
}
```

### Chat2Data v1エンドポイントを呼び出す {#call-the-chat2data-v1-endpoint}

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
> 各 Chat2Query データ アプリには、1 日あたり 100 リクエストのレート制限があります。レート制限を超えると、API は`429`エラーを返します。クォータを増やすには、サポート チームに[リクエストを送信する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)リクエストしてください。ロール`Chat2Query Data Summary Management Role`の API キーでは、Chat2Data v1 エンドポイントを呼び出すことはできません。

次のコード例は、 `sp500insight.users`テーブル内のユーザー数をカウントするために使用されます。

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
-   [データサービスの応答コードとステータスコード](/tidb-cloud/data-service-response-and-status-code.md)
