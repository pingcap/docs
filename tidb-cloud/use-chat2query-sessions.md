---
title: Start Multi-round Chat2Query
summary: Chat2Query セッション関連 API を使用して、マルチラウンド チャットを開始する方法を学習します。
---

# マルチラウンドChat2Queryを開始する {#start-multi-round-chat2query}

v3 以降、Chat2Query API では、セッション関連のエンドポイントを呼び出して、複数ラウンドのチャットを開始できます。3 `/v3/chat2data`ポイントによって返される`session_id`使用して、次のラウンドで会話を続行できます。

## 始める前に {#before-you-begin}

マルチラウンド Chat2Query を開始する前に、次のものを用意してください。

-   A [Chat2Query データ アプリ](/tidb-cloud/use-chat2query-api.md#create-a-chat2query-data-app) 。
-   [Chat2Query データ アプリの API キー](/tidb-cloud/use-chat2query-api.md#create-an-api-key) 。
-   A [ターゲットデータベースのデータ概要](/tidb-cloud/use-chat2query-api.md#1-generate-a-data-summary-by-calling-v3datasummaries) 。

## ステップ1.セッションを開始する {#step-1-start-a-session}

セッションを開始するには、Chat2Query データ アプリの`/v3/sessions`エンドポイントを呼び出します。

以下は、このエンドポイントを呼び出すための一般的なコード例です。

> **ヒント：**
>
> エンドポイントの特定のコード例を取得するには、データ アプリの左側のペインでエンドポイント名をクリックし、 **[コード例の表示]**をクリックします。詳細については、 [エンドポイントのサンプルコードを取得する](/tidb-cloud/use-chat2query-api.md#get-the-code-example-of-an-endpoint)参照してください。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/sessions'\
    --header 'content-type: application/json'\
    --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "name": "<Your session name>"
}'
```

上記のコードでは、リクエスト本文は次のプロパティを持つ JSON オブジェクトです。

-   `cluster_id` :*文字列*。TiDB クラスターの一意の識別子。
-   `database` :*文字列*。データベースの名前。
-   `name` :*文字列*。セッションの名前。

応答の例は次のとおりです。

```json
{
    "code": 200,
    "msg": "",
    "result": {
    "messages": [],
    "meta": {
        "created_at": 1718948875, // A UNIX timestamp indicating when the session is created
        "creator": "<Your email>", // The creator of the session
        "name": "<Your session name>", // The name of the session
        "org_id": "1", // The organization ID
        "updated_at": 1718948875 // A UNIX timestamp indicating when the session is updated
    },
    "session_id": 305685 // The session ID
    }
}
```

## ステップ2. セッションでChat2Dataエンドポイントを呼び出す {#step-2-call-chat2data-endpoints-with-the-session}

セッションを開始した後、 `/v3/sessions/{session_id}/chat2data`電話して次のラウンドで会話を続けることができます。

以下は一般的なコード例です。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://eu-central-1.data.tidbcloud.com/api/v1beta/app/chat2query-YqAvnlRj/endpoint/v3/sessions/{session_id}/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "question": "<Your question to generate data>",
    "feedback_answer_id": "",
    "feedback_task_id": "",
    "sql_generate_mode": "direct"
}'
```

上記のコードでは、リクエスト本文は次のプロパティを持つ JSON オブジェクトです。

-   `question` :*文字列*。必要なクエリを説明する自然言語での質問。
-   `feedback_answer_id` :*文字列*。フィードバック回答 ID。このフィールドはオプションであり、フィードバックにのみ使用されます。
-   `feedback_task_id` :*文字列*。フィードバック タスク ID。このフィールドはオプションであり、フィードバックにのみ使用されます。
-   `sql_generate_mode` :*文字列*。SQL 文を生成するモード。値は`direct`または`auto_breakdown`です。 `direct`に設定すると、API は指定した`question`に基づいて SQL 文を直接生成します。 `auto_breakdown`に設定すると、API は`question`複数のタスクに分割し、各タスクの SQL 文を生成します。

応答の例は次のとおりです。

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "job_id": "d96b6fd23c5f445787eb5fd067c14c0b",
    "session_id": 305685
  }
}
```

応答は`/v3/chat2data`エンドポイントの応答と同様です。 `/v2/jobs/{job_id}`エンドポイントを呼び出すことでジョブのステータスを確認できます。詳細については[`/v2/jobs/{job_id}`を呼び出して分析ステータスを確認します。](/tidb-cloud/use-chat2query-api.md#2-check-the-analysis-status-by-calling-v2jobsjob_id)参照してください。
