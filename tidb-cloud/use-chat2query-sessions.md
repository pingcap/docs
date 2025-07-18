---
title: Start Multi-round Chat2Query
summary: Learn how to start multi-round chat by using Chat2Query session-related APIs.
---

# Start Multi-round Chat2Query

Starting from v3, the Chat2Query API enables you to start multi-round chats by calling session related endpoints. You can use the `session_id` returned by the `/v3/chat2data` endpoint to continue your conversation in the next round.

## Before you begin

Before starting multi-round Chat2Query, make sure that you have the following:

- A [Chat2Query Data App](/tidb-cloud/use-chat2query-api.md#create-a-chat2query-data-app).
- An [API key for the Chat2Query Data App](/tidb-cloud/use-chat2query-api.md#create-an-api-key).
- A [data summary for your target database](/tidb-cloud/use-chat2query-api.md#1-generate-a-data-summary-by-calling-v3datasummaries).

## Step 1. Start a session

To start a session, you can call the `/v3/sessions` endpoint of your Chat2Query Data App.

The following is a general code example for calling this endpoint.

> **Tip:**
>
> To get a specific code example for your endpoint, click the endpoint name in the left pane of your Data App, and then click **Show Code Example**. For more information, see [Get the example code of an endpoint](/tidb-cloud/use-chat2query-api.md#get-the-code-example-of-an-endpoint).

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/sessions'\
    --header 'content-type: application/json'\
    --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "name": "<Your session name>"
}'
```

In the preceding code, the request body is a JSON object with the following properties:

- `cluster_id`: _string_. A unique identifier of the TiDB cluster.
- `database`: _string_. The name of the database.
- `name`: _string_. The name of the session.

An example response is as follows:

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

## Step 2. Call Chat2Data endpoints with the session

After starting a session, you can call `/v3/sessions/{session_id}/chat2data` to continue your conversation in the next round.

The following is a general code example:

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

In the preceding code, the request body is a JSON object with the following properties:

- `question`: _string_. A question in natural language describing the query you want.
- `feedback_answer_id`: _string_. The feedback answer ID. This field is optional and is only used for feedback.
- `feedback_task_id`: _string_. The feedback task ID. This field is optional and is only used for feedback.
- `sql_generate_mode`: _string_. The mode to generate SQL statements. The value can be `direct` or `auto_breakdown`. If you set it to `direct`, the API will generate SQL statements directly based on the `question` you provided. If you set it to `auto_breakdown`, the API will break down the `question` into multiple tasks and generate SQL statements for each task.

An example response is as follows:

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

The response is similar to the response of the `/v3/chat2data` endpoint. You can check the job status by calling the `/v2/jobs/{job_id}` endpoint. For more information, see [Check the analysis status by calling `/v2/jobs/{job_id}`](/tidb-cloud/use-chat2query-api.md#2-check-the-analysis-status-by-calling-v2jobsjob_id).