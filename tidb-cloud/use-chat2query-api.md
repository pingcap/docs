---
title: Get Started with Chat2Query API
summary: Learn how to use TiDB Cloud Chat2Query API to generate and execute SQL statements using AI by providing instructions.
---

# Get Started with Chat2Query API

TiDB Cloud provides the Chat2Query API, a RESTful interface that enables you to generate and execute SQL statements using AI by providing instructions. Then, the API returns the query results for you.

Chat2Query API can only be accessed through HTTPS, ensuring that all data transmitted over the network is encrypted using TLS.

> **Note:**
>
> Chat2Query API is available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters. To use the Chat2Query API on [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters, contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md).

## Step 1. Create a Chat2Query Data App

To create a Data App for your project, perform the following steps:

1. On the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project, click <MDSvgIcon name="icon-create-data-app" /> **Create DataApp** in the left pane. The data app creation dialog is displayed.

    > **Tip:**
    >
    > If you are on the **Chat2Query** page of your cluster, you can also open the data app creation dialog by clicking ... in the upper-right corner, choosing **Access Chat2Query via API**, and clicking **New Chat2Query Data App**.

2. In the dialog, define a name for your Data App, choose the desired clusters as the data source, and select **Chat2Query Data App** as the Data App type. Optionally, you can also write a description for the App.

3. Click **Create**.

   The newly created Chat2Query Data App is displayed in the left pane. Under this Data App, you can find a list of Chat2Query endpoints.

## Step 2. Create an API key

Before calling an endpoint, you need to create an API key for the Chat2Query Data App, which is used by the endpoint to access data in your TiDB Cloud clusters.

To create an API key, perform the following steps:

1. In the left pane of [**Data Service**](https://tidbcloud.com/console/data-service), click your Chat2Query Data App to view its details on the right side.
2. In the **Authentication** area, click **Create API Key**.
3. In the **Create API Key** dialog, enter a description, and then select one of the following roles for your API key:

   - `Chat2Query Admin Role`: allows the API key to manage data summaries, generate SQL statements based on provided instructions, and execute any SQL statements.
   - `Chat2Query Data Summary Management Role`: only allows the API key to generate and update data summaries.

        > **Tip:**
        >
        > For Chat2Query API, a data summary is an analysis result of your database by AI, including your database descritions, table descriptions, and column descriptions. By generating a data summary of your database, you can get a more accurate response when generating SQL statements by providing instructions.

   - `Chat2Query SQL Generate & Execute (ReadOnly) Role`: only allows the API key to generate SQL statements based on provided instructions and execute `SELECT` SQL statements.
   - `Chat2Query SQL Generate & Execute (ReadWrite) Role`: allows the API key to generate SQL statements based on provided instructions and execute any SQL statements.

4. Click **Next**. The public key and private key are displayed.

    Make sure that you have copied and saved the private key in a secure location. After leaving this page, you will not be able to get the full private key again.

5. Click **Done**.

## Step 3. Call Chat2Query endpoints

> **Note:**
>
> Each Chat2Query Data App has a rate limit of 100 requests per day. If you exceed the rate limit, the API returns a `429` error. For more quota, you can [submit a request](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519) to our support team.

In each Chat2Query Data App, you can find the following endpoints:

- Chat2Query v1 endpoint: `/chat2data`
- Chat2Query v2 endpoints: the endpoints whose names starting with `/v2`, such as `/v2/dataSummaries` and `/v2/chat2data`

> **Tip:**
>
> Compared with the Chat2Query v1 endpoint `/chat2data`, the Chat2Query v2 endpoint `/v2/chat2data` requires you to analyze your database first by calling `/v2/dataSummaries`, so the results returned by `/v2/chat2data` are generally more accurate.

### Get the code example of an endpoint

TiDB Cloud provides code examples to help you quickly call Chat2Query endpoints. To get the code example of a Chat2Query endpoint, perform the following steps:

1. In the left pane of the [**Data Service**](https://tidbcloud.com/console/data-service) page, click the name of a Chat2Query endpoint.

    The information for calling this endpoint is displayed on the right side, such as endpoint URL, code example, and request method.

2. Click **Code Example**.
3. In the displayed dialog box, select the cluster and database that you want to use to call the endpoint, and then copy the code example.
4. To call the endpoint, you can paste the example in your application, replace the parameters in the example with your own (such as replacing the `${PUBLIC_KEY}` and `${PRIVATE_KEY}` placeholders with your API key), and then run it.

### Call Chat2Query v2 endpoints

TiDB Cloud Data Service provides the following Chat2Query v2 endpoints:

|  Method | Endpoint| Description |
|  ----  | ----  |----  |
|  POST  | `/v2/dataSummaries`  | This endpoint generates a data summary for your database schema, table schema, and column schema by using artificial intelligence for analysis. |
|  GET  | `/v2/dataSummaries/{data_summary_id}`  | This endpoint enables you to retrieve a specific generated data summary. |
|  PUT  | `/v2/dataSummaries/{data_summary_id}`  | This endpoint enables you to update the table description and column description of a specific data summary |
|  POST  | `/v2/chat2data`  | This endpoint enables you to generate and execute SQL statements using artificial intelligence by providing the data summary ID and instructions. |
|  GET  | `/v2/jobs/{job_id}` | This endpoint enables you to query the status of the data summary generation job. |

In the subsquent sections, you will learn how to call these endpoints.

#### 1. Generate a data summary by calling `/v2/dataSummaries`

Before calling `/v2/chat2data`, let AI analyze the database and generate a data summary first by calling `/v2/dataSummaries`, so `/v2/chat2data` can get a better performance in SQL generation later.

The following is a code example of calling `/v2/chat2data` to analyze the `sp500insight` database and generate a data summary for the database:

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/dataSummaries'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10939961583884005252",
    "database": "sp500insight"
}'
```

In the preceding example, the request body is a JSON object with the following properties:

- `cluster_id`: _string_. A unique identifier of the TiDB cluster.
- `database`: _string_. The name of the database.

An example response is as follows:

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

#### 2. Check the analysis status by calling `/v2/jobs/{job_id}`

The `/v2/dataSummaries` API is asynchronous. For a database with a large dataset, it might take a few minutes to complete the database analysis and return the full data summary.

To check the analysis status of your database, you can call the `/v2/jobs/{job_id}` endpoint as follows:

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>`/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

An example response is as follows:

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1699518950, // when the job finished, it's UNIX timestamp
    "job_id": "79c2b3d36c074943ab06a29e45dd5887",  // ID of current job
    "result": DataSummaryObject, // see the definition below
    "status": "done" // status of the current job
  }
}
```

If `"status"` is `"done"`, the full data summary is ready and you can now generate and execute SQL statements for this database by calling `/v2/chat2data`. Otherwise, you need to wait and check the analysis status later until it is done.

In the response, `DataSummaryObject` represents AI exploration information of the given database. The structure of `DataSummaryObject` is as follows:

```json
{
    "cluster_id": 10939961583884005000, // your cluster id
    "db_name": "sp500insight", // database name
    "db_schema": { // database schema information
        "users": { // a table named "users"
            "columns": { // columns in table "users"
                "user_id": {
                    "default": null,
                    "description": "The unique identifier for each user.",
                    "name": "user_id",
                    "nullable": true,
                    "type": "int(11)"
                }
            },
            "description": "This table represents the user data and includes the date and time when each user was created.",
            "key_attributes": [ // key attributes of table "user"
                "user_id",
            ],
            "primary_key": "id",
            "status": "done",
            "table_name": "users", // table name in database
        }
    },
    "entity": { // entities abstract by AI
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

#### 3. Generate and execute SQL statements by calling `/v2/chat2data`

When the data summary of an database is ready, you can call `/v2/chat2data` to generate and execute SQL statements by providing the data summary ID and your instructions as follows:

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
  "data_summary_id": <Your data summary id>,
  "raw_question": "<Your question to generate data>"
}'
```

In the preceding code, the request body is a JSON object with the following properties:

- `data_summary_id`: _string_. A unique identifier generated for the data summary when you call `/v2/dataSummaries`.
- `raw_question`: _string_. A natural language describing the query you want.

An example response is as follows:

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "job_id": "3966d5bd95324a6283445e3a02ccd97c"
  }
}
```

The `/v2/chat2data` API is asynchronous. You can check the job status by calling the `/v2/jobs/{job_id}` endpoint:

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

An example response is as follows:

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1699581661,
    "job_id": "3966d5bd95324a6283445e3a02ccd97c",
    "result": {
      "question_id": "8c4c15cf-a808-45b8-bff7-2ca819a1b6d5",
      "raw_question": "count the users", // the original question you gave
      "task_tree": {
        "0": {
          "clarified_task": "count the users", // task that AI understands
          "description": "",
          "columns": [ // query result columns of generated SQL
            {
              "col": "user_count"
            }
          ],
          "rows": [ // query result of generated SQL
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

#### (Optional) 4. Update a data summary for better results of `/v2/chat2data`

If you want to improve the results of `/v2/chat2data` for a database, you can check and update the data summary of this database.

1. To get the data summary of a database, call the `v2/dataSummaries/{data_summary_id}` endpoint in the GET method.

    ```bash
    curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/dataSummaries/{data_summary_id}'\
     --header 'content-type: application/json'
    ```

    An example response is as follows:

    ```json
    {
      "code": 200,
      "msg": "",
      "result": {
        "created_at": 1699518862,
        "creator": "",
        "data": DataSummaryObject, // see the definition of DataSummaryObject
        "id": 481235,
        "name": "data-context",
        "org_id": 30061,
        "type": "data", // type of data summary, it's `data` for data summary
        "updated_at": 1699518950
      }
    }
    ```

2. To update the data summary of a database, call the `v2/dataSummaries/{data_summary_id}` endpoint in the PUT method. Currently, you can update the table descriptions and column descriptions in the summary.


    ```bash
    curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request PUT 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/dataSummaries/{data_summary_id}'\
     --header 'content-type: application/json'\
     --data-raw '{
      "tables": {
            "<table_name>": {
                "description": "<New table description you want to set>",
                "columns": {
                    "<column name>": "<New column description you want to set>"
                }
            }
      }
    }'
    ```

    In the preceding example, the request body is a JSON object with the following properties:

    - `<tables_name>`: _string_. The table you want to update
    - `tables_name.description`: _string_. The new description you want to set for the given table
    - `columns`: a key-value pair to specify the target column and the column description you want to update

    An example response is as follows:

    ```json
    {
      "code": 200,
      "msg": "",
      "result": {
        "job_id": "103d0bf8d8564ec7b2c768d3180d8ab1"
      }
    }
    ```

3. The `v2/dataSummaries/{data_summary_id}` is asynchronous. You can check the status of the summary updating job by calling the `/v2/jobs/{job_id}` endpoint.

    ```bash
    curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/jobs/{job_id}'\
     --header 'content-type: application/json'
    ```

    An example response is as follows:

    ```bash
    {
      "code": 200,
      "msg": "",
      "result": {
        "ended_at": 1699523242,
        "job_id": "103d0bf8d8564ec7b2c768d3180d8ab1",
        "result": null,
        "status": "done"
      }
    }
    ```

    When the `status` is `done`, the job is finished, and the descriptions of tables and columns are updated.

### Call the Chat2Data v1 endpoint

TiDB Cloud Data Service provides the following Chat2Query v1 endpoint:

|  Method | Endpoint| Description |
|  ----  | ----  |----  |
|  POST | `/chat2data`  | This endpoint allows you to generate and execute SQL statements using artificial intelligence by providing the target database name and instructions.  |

You can call the `/chat2data` endpoint directly to generate and execute SQL statements. Compared with `/v2/chat2data`, `/chat2data` provides a faster response but lower performance.

TiDB Cloud generates code examples to help you call an endpoint. To get the examples and run the code, see [Get the code example of an endpoint](#get-the-code-example-of-an-endpoint).

When calling `/chat2data`, you need to replace the following parameters:

- Replace the `${PUBLIC_KEY}` and `${PRIVATE_KEY}` placeholders with your API key.
- Replace the `<your instruction>` placeholder with the instruction you want AI to generate and execute SQL statements.
- Replace the `<your table name, optional>` placeholder with the table name you want to query. If you do not specify a table name, AI will query all tables in the database.

> **Note:**
>
> Each Chat2Query Data App has a rate limit of 100 requests per day. If you exceed the rate limit, the API returns a `429` error. For more quota, you can [submit a request](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519) to our support team.
> API Key with the role `Chat2Query Data Context Management Role` cannot call the Chat2Data v1 endpoint.

The following code example is used to count how many users are in `sp500insight.users` table:

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
- `instruction`: _string_. A natural language instruction describing the query you want.

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
- [Response and Status Codes of Data Service](/tidb-cloud/data-service-response-and-status-code.md)
