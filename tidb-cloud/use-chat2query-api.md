---
title: Get Started with Chat2Query API
summary: Learn how to use TiDB Cloud Chat2Query API to generate and execute SQL statements using AI by providing instructions.
---

# Get Started with Chat2Query API

TiDB Cloud provides the Chat2Query API, a RESTful interface that enables you to generate and execute SQL statements using AI by providing instructions. Then, the API returns the query results for you.

Chat2Query API can only be accessed through HTTPS, ensuring that all data transmitted over the network is encrypted using TLS.

> **Note:**
>
> Chat2Query API is available for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters. To use the Chat2Query API on [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters, contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md).

## Before you begin

Before calling Chat2Query endpoints, you need to create a Chat2Query Data App and create an API key for the Data App.

### Create a Chat2Query Data App

To create a Data App for your project, perform the following steps:

1. On the [**Data Service**](https://tidbcloud.com/project/data-service) page of your project, click <MDSvgIcon name="icon-create-data-app" /> **Create DataApp** in the left pane. The data app creation dialog is displayed.

    > **Tip:**
    >
    > If you are on the **SQL Editor** page of your cluster, you can also open the data app creation dialog by clicking **...** in the upper-right corner, choosing **Access Chat2Query via API**, and clicking **New Chat2Query Data App**.

2. In the dialog, define a name for your Data App, choose the desired clusters as the data sources, and select **Chat2Query Data App** as the **Data App** type. Optionally, you can also write a description for the App.

3. Click **Create**.

   The newly created Chat2Query Data App is displayed in the left pane. Under this Data App, you can find a list of Chat2Query endpoints.

### Create an API key

Before calling an endpoint, you need to create an API key for the Chat2Query Data App, which is used by the endpoint to access data in your TiDB Cloud clusters.

To create an API key, perform the following steps:

1. In the left pane of [**Data Service**](https://tidbcloud.com/project/data-service), click your Chat2Query Data App to view its details on the right side.
2. In the **Authentication** area, click **Create API Key**.
3. In the **Create API Key** dialog, enter a description, and then select one of the following roles for your API key:

   - `Chat2Query Admin`: allows the API key to manage data summaries, generate SQL statements based on provided instructions, and execute any SQL statements.
   - `Chat2Query Data Summary Management Role`: only allows the API key to generate and update data summaries.

        > **Tip:**
        >
        > For Chat2Query API, a data summary is an analysis result of your database by AI, including your database descriptions, table descriptions, and column descriptions. By generating a data summary of your database, you can get a more accurate response when generating SQL statements by providing instructions.

   - `Chat2Query SQL ReadOnly`: only allows the API key to generate SQL statements based on provided instructions and execute `SELECT` SQL statements.
   - `Chat2Query SQL ReadWrite`: allows the API key to generate SQL statements based on provided instructions and execute any SQL statements.

4. By default, an API key never expires. If you prefer to set an expiration time for the key, click **Expires in**, select a time unit (`Minutes`, `Days`, or `Months`), and then fill in a desired number for the time unit.

5. Click **Next**. The public key and private key are displayed.

    Make sure that you have copied and saved the private key in a secure location. After leaving this page, you will not be able to get the full private key again.

6. Click **Done**.

## Call Chat2Query endpoints

> **Note:**
>
> Each Chat2Query Data App has a rate limit of 100 requests per day. If you exceed the rate limit, the API returns a `429` error. For more quota, you can [submit a request](https://tidb.support.pingcap.com/) to our support team.

In each Chat2Query Data App, you can find the following endpoints:

- Chat2Query v3 endpoints: the endpoints whose names starting with `/v3`, such as `/v3/dataSummaries` and `/v3/chat2data`(recommended)
- Chat2Query v2 endpoints: the endpoints whose names starting with `/v2`, such as `/v2/dataSummaries` and `/v2/chat2data`
- Chat2Query v1 endpoint: `/v1/chat2data`(deprecated)

> **Tip:**
>
> Compared with `/v1/chat2data`, `/v3/chat2data` and `/v2/chat2data` requires you to analyze your database first by calling `/v3/dataSummaries` or `/v2/dataSummaries`. Consequently, the results returned by `/v3/chat2data` and `/v2/chat2data` are generally more accurate.

### Get the code example of an endpoint

TiDB Cloud provides code examples to help you quickly call Chat2Query endpoints. To get the code example of a Chat2Query endpoint, perform the following steps:

1. In the left pane of the [**Data Service**](https://tidbcloud.com/project/data-service) page, click the name of a Chat2Query endpoint.

    The information for calling this endpoint is displayed on the right side, such as endpoint URL, code example, and request method.

2. Click **Show Code Example**.

3. In the displayed dialog box, select the cluster, database, and authentication method that you want to use to call the endpoint, and then copy the code example.

    > **Note:**
    >
    > For some of the endpoints such as `/v2/jobs/{job_id}`, you only need to select the authentication method.

4. To call the endpoint, you can paste the example in your application, replace the parameters in the example with your own (such as replacing the `${PUBLIC_KEY}` and `${PRIVATE_KEY}` placeholders with your API key), and then run it.

### Call Chat2Query v3 endpoints or v2 endpoints

TiDB Cloud Data Service provides the following Chat2Query v3 endpoints and v2 endpoints:

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST   | `/v3/dataSummaries` | This endpoint generates a data summary for your database schema, table schema, and column schema by using artificial intelligence for analysis. |
| GET    | `/v3/dataSummaries` | This endpoint retrieves all data summaries of your database. |
| GET    | `/v3/dataSummaries/{data_summary_id}` | This endpoint retrieves a specific data summary. |
| PUT    | `/v3/dataSummaries/{data_summary_id}` | This endpoint updates a specific data summary. |
| PUT    | `/v3/dataSummaries/{data_summary_id}/tables/{table_name}` | This endpoint updates the description of a specific table in a specific data summary. |
| PUT    | `/v3/dataSummaries/{data_summary_id}/tables/{table_name}/columns` | This endpoint updates the description of columns for a specific table in a specific data summary. |
| POST   | `/v3/knowledgeBases` | This endpoint creates a new knowledge base. For more information about the usage of knowledge base related endpoints, see [Use knowledge bases](/tidb-cloud/use-chat2query-knowledge.md).  |
| GET    | `/v3/knowledgeBases` | This endpoint retrieves all knowledge bases. |
| GET    | `/v3/knowledgeBases/{knowledge_base_id}` | This endpoint retrieves a specific knowledge base. |
| PUT    | `/v3/knowledgeBases/{knowledge_base_id}` | This endpoint updates a specific knowledge base. |
| POST   | `/v3/knowledgeBases/{knowledge_base_id}/data` | This endpoint adds data to a specific knowledge base. |
| GET    | `/v3/knowledgeBases/{knowledge_base_id}/data` | This endpoint retrieves data from a specific knowledge base. |
| PUT    | `/v3/knowledgeBases/{knowledge_base_id}/data/{knowledge_data_id}` | This endpoint updates specific data in a knowledge base. |
| DEL    | `/v3/knowledgeBases/{knowledge_base_id}/data/{knowledge_data_id}` | This endpoint deletes specific data from a knowledge base. |
| POST   | `/v3/sessions` | This endpoint creates a new session. For more information about the usage of session-related endpoints, see [Start multi-round Chat2Query](/tidb-cloud/use-chat2query-sessions.md). |
| GET    | `/v3/sessions` | This endpoint retrieves a list of all sessions. |
| GET    | `/v3/sessions/{session_id}` | This endpoint retrieves the details of a specific session. |
| PUT    | `/v3/sessions/{session_id}` | This endpoint updates a specific session. |
| PUT    | `/v3/sessions/{session_id}/reset` | This endpoint resets a specific session. |
| POST   | `/v3/sessions/{session_id}/chat2data` | This endpoint generates and executes SQL statements within a specific session using artificial intelligence. For more information, see [Start multi-round Chat2Query by using sessions](/tidb-cloud/use-chat2query-sessions.md). |
| POST   | `/v3/chat2data` | This endpoint enables you to generate and execute SQL statements using artificial intelligence by providing the data summary ID and instructions. |
| POST   | `/v3/refineSql` | This endpoint refines existing SQL queries using artificial intelligence. |
| POST   | `/v3/suggestQuestions` | This endpoint suggests questions based on the provided data summary. |
| POST   | `/v2/dataSummaries` | This endpoint generates a data summary for your database schema, table schema, and column schema using artificial intelligence. |
| GET    | `/v2/dataSummaries` | This endpoint retrieves all data summaries. |
| POST   | `/v2/chat2data` | This endpoint enables you to generate and execute SQL statements using artificial intelligence by providing the data summary ID and instructions. |
| GET    | `/v2/jobs/{job_id}` | This endpoint enables you to query the status of a specific data summary generation job. |

The steps to call `/v3/chat2data` and `/v2/chat2data` are the same. The following sections take `/v3/chat2data` as an example to show how to call it.

#### 1. Generate a data summary by calling `/v3/dataSummaries`

Before calling `/v3/chat2data`, let AI analyze the database and generate a data summary first by calling `/v3/dataSummaries`, so `/v3/chat2data` can get a better performance in SQL generation later.

The following is a code example of calling `/v3/dataSummaries` to analyze the `sp500insight` database and generate a data summary for the database:

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

In the preceding example, the request body is a JSON object with the following properties:

- `cluster_id`: _string_. A unique identifier of the TiDB cluster.
- `database`: _string_. The name of the database.
- `description`: _string_. A description of the data summary.
- `reuse`: _boolean_. Specifies whether to reuse an existing data summary. If you set it to `true`, the API will reuse an existing data summary. If you set it to `false`, the API will generate a new data summary.

An example response is as follows:

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

#### 2. Check the analysis status by calling `/v2/jobs/{job_id}`

The `/v3/dataSummaries` API is asynchronous. For a database with a large dataset, it might take a few minutes to complete the database analysis and return the full data summary.

To check the analysis status of your database, you can call the `/v2/jobs/{job_id}` endpoint as follows:

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>`/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

An example response is as follows:

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

If `"status"` is `"done"`, the full data summary is ready and you can now generate and execute SQL statements for this database by calling `/v3/chat2data`. Otherwise, you need to wait and check the analysis status later until it is done.

In the response, `DataSummaryObject` represents AI exploration information of the given database. The structure of `DataSummaryObject` is as follows:

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

#### 3. Generate and execute SQL statements by calling `/v3/chat2data`

When the data summary of a database is ready, you can call `/v3/chat2data` to generate and execute SQL statements by providing the cluster ID, database name, and your question.

For example:

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

The request body is a JSON object with the following properties:

- `cluster_id`: _string_. A unique identifier of the TiDB cluster.
- `database`: _string_. The name of the database.
- `data_summary_id`: _integer_. The ID of the data summary used to generate SQL. This property only takes effect if `cluster_id` and `database` are not provided. If you specify both `cluster_id` and `database`, the API uses the default data summary of the database.
- `question`: _string_. A question in natural language describing the query you want.
- `sql_generate_mode`: _string_. The mode to generate SQL statements. The value can be `direct` or `auto_breakdown`. If you set it to `direct`, the API will generate SQL statements directly based on the `question` you provided. If you set it to `auto_breakdown`, the API will break down the `question` into multiple tasks and generate SQL statements for each task.

An example response is as follows:

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

If you receive a response with the status code `400` as follows, it means that you need to wait a moment for the data summary to be ready.

```js
{
    "code": 400,
    "msg": "Data summary is not ready, please wait for a while and retry",
    "result": {}
}
```

The `/v3/chat2data` API is asynchronous. You can check the job status by calling the `/v2/jobs/{job_id}` endpoint:

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

An example response is as follows:

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

### Call the Chat2Data v1 endpoint (deprecated)

> **Note:**
>
> The Chat2Data v1 endpoint is deprecated. It is recommended that you call Chat2Data v3 endpoints instead.

TiDB Cloud Data Service provides the following Chat2Query v1 endpoint:

|  Method | Endpoint| Description |
|  ----  | ----  |----  |
|  POST | `/v1/chat2data`  | This endpoint allows you to generate and execute SQL statements using artificial intelligence by providing the target database name and instructions.  |

You can call the `/v1/chat2data` endpoint directly to generate and execute SQL statements. Compared with `/v2/chat2data`, `/v1/chat2data` provides a faster response but lower performance.

TiDB Cloud generates code examples to help you call an endpoint. To get the examples and run the code, see [Get the code example of an endpoint](#get-the-code-example-of-an-endpoint).

When calling `/v1/chat2data`, you need to replace the following parameters:

- Replace the `${PUBLIC_KEY}` and `${PRIVATE_KEY}` placeholders with your API key.
- Replace the `<your table name, optional>` placeholder with the table name you want to query. If you do not specify a table name, AI will query all tables in the database.
- Replace the `<your instruction>` placeholder with the instruction you want AI to generate and execute SQL statements.

> **Note:**
>
> - Each Chat2Query Data App has a rate limit of 100 requests per day. If you exceed the rate limit, the API returns a `429` error. For more quota, you can [submit a request](https://tidb.support.pingcap.com/) to our support team.
> - An API Key with the role `Chat2Query Data Summary Management Role` cannot call the Chat2Data v1 endpoint.
The following code example is used to count how many users are in the `sp500insight.users` table:

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

In the preceding example, the request body is a JSON object with the following properties:

- `cluster_id`: _string_. A unique identifier of the TiDB cluster.
- `database`: _string_. The name of the database.
- `tables`: _array_. (optional) A list of table names to be queried.
- `instruction`: _string_. An instruction in natural language describing the query you want.

The response is as follows:

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

If your API call is not successful, you will receive a status code other than `200`. The following is an example of the `500` status code:

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

## Learn more

- [Manage an API key](/tidb-cloud/data-service-api-key.md)
- [Start Multi-round Chat2Query](/tidb-cloud/use-chat2query-sessions.md)
- [Use Knowledge Bases](/tidb-cloud/use-chat2query-knowledge.md)
- [Response and Status Codes of Data Service](/tidb-cloud/data-service-response-and-status-code.md)
