---
title: Start Multi-round Chat2Query
summary: Chat2Query セッション関連 API を使用して、マルチラウンド チャットを開始する方法を学習します。
---

# マルチラウンドChat2Queryを開始する {#start-multi-round-chat2query}

Chat2Query API v3以降では、セッション関連のエンドポイントを呼び出すことで、複数ラウンドのチャットを開始できます`/v3/chat2data`エンドポイントから返される`session_id`使用して、次のラウンドで会話を続行できます。

## 始める前に {#before-you-begin}

マルチラウンド Chat2Query を開始する前に、次のものを用意してください。

-   A [Chat2Queryデータアプリ](/tidb-cloud/use-chat2query-api.md#create-a-chat2query-data-app) 。
-   [Chat2QueryデータアプリのAPIキー](/tidb-cloud/use-chat2query-api.md#create-an-api-key)です。
-   A [ターゲットデータベースのデータサマリー](/tidb-cloud/use-chat2query-api.md#1-generate-a-data-summary-by-calling-v3datasummaries) 。

## ステップ1. セッションを開始する {#step-1-start-a-session}

セッションを開始するには、Chat2Query データ アプリの`/v3/sessions`エンドポイントを呼び出します。

以下は、このエンドポイントを呼び出すための一般的なコード例です。

> **ヒント：**
>
> エンドポイントの具体的なコード例を取得するには、データアプリの左側のペインでエンドポイント名をクリックし、 **「コード例を表示」**をクリックします。詳細については、 [エンドポイントのサンプルコードを取得する](/tidb-cloud/use-chat2query-api.md#get-the-code-example-of-an-endpoint)参照してください。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/sessions'\
    --header 'content-type: application/json'\
    --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "name": "<Your session name>"
}'
```

上記のコードでは、リクエスト本体は次のプロパティを持つ JSON オブジェクトです。

-   `cluster_id` :*文字列*。TiDBクラスタの一意の識別子。
-   `database` :*文字列*。データベースの名前。
-   `name` ：*文字列*。セッションの名前。

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

上記のコードでは、リクエスト本体は次のプロパティを持つ JSON オブジェクトです。

-   `question` :*文字列*。必要なクエリを説明する自然言語での質問。
-   `feedback_answer_id` ：*文字列*。フィードバック回答ID。このフィールドはオプションであり、フィードバックにのみ使用されます。
-   `feedback_task_id` ：*文字列*。フィードバックタスクID。このフィールドはオプションであり、フィードバックにのみ使用されます。
-   `sql_generate_mode` :*文字列*。SQL文を生成するモード。値は`direct`または`auto_breakdown`です。8 `direct`設定すると、APIは指定された`question` SQL文に基づいて直接SQL文を生成します。12 に設定すると、APIは`auto_breakdown` `question` SQL文を複数のタスクに分割し、各タスクごとにSQL文を生成します。

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

レスポンスはエンドポイント`/v3/chat2data`のレスポンスと同様です。エンドポイント`/v2/jobs/{job_id}`呼び出すことでジョブのステータスを確認できます。詳細については、エンド[`/v2/jobs/{job_id}`を呼び出して分析ステータスを確認します。](/tidb-cloud/use-chat2query-api.md#2-check-the-analysis-status-by-calling-v2jobsjob_id)参照してください。
