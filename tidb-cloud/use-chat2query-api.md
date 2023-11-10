---
title: Get Started with Chat2Query API
summary: Learn how to use TiDB Cloud Chat2Query API to generate and execute SQL statements using AI by providing instructions.
---

# Get Started with Chat2Query API

TiDB Cloud provides the Chat2Query API, a RESTful interface that allows you to generate and execute SQL statements using AI by providing instructions. Then, the API returns the query results for you.

Chat2Query API can only be accessed through HTTPS, ensuring that all data transmitted over the network is encrypted using TLS.

> **Note:**
>
> Chat2Query API is available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters. To use the Chat2Query API on [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters, contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md).

## Before you begin

Before using the Chat2Query API, make sure that you have created a TiDB cluster and enabled [AI to generate SQL queries](/tidb-cloud/explore-data-with-chat2query.md). If you do not have a TiDB cluster, follow the steps in [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md) or [Create a TiDB Dedicated cluster](/tidb-cloud/create-tidb-cluster.md) to create one.

## Step 1. Enable the Chat2Query API

To enable the Chat2Query API, perform the following steps:

1. Go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

   > **Tip:**
   >
   > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click your cluster name, and then click **Chat2Query** in the left navigation pane.
3. In the upper-right corner of Chat2Query, click **...** and select **Settings**.
4. Enable **DataAPI** and the Chat2Query Data App is created.

   > **Note:**
   >
   > After DataAPI is enabled for one TiDB cluster, all TiDB clusters in the same project can use the Chat2Query API.

5. Click the **Data Service** link in the message to access the Chat2Query API.

   You can find that the **Chat2Query System** [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) and its **Chat2Data** [endpoint](/tidb-cloud/tidb-cloud-glossary.md#endpoint) are displayed in the left pane.

## Step 2. Create an API key

Before calling an endpoint, you need to create an API key. To create an API key for the Chat2Query Data App, perform the following steps:

1. In the left pane of [**Data Service**](https://tidbcloud.com/console/data-service), click the name of **Chat2Query System** to view its details.
2. In the **Authentication** area, click **Create API Key**.
3. In the **Create API Key** dialog box, enter a description and select a role for your API key.

   - `Chat2Query Admin Role`: allows the API key to management data summary, generate sql from a question, execute any SQL statement
   - `Chat2Query Data Context Management Role`: only allows the API key to generate, update and delete data summary
   - `Chat2Query SQL Generate & Execute (ReadOnly) Role`: can generate sql from a question, but only allows the API key to execute SELECT SQL statement
   - `Chat2Query SQL Generate & Execute (ReadWrite) Role`: can generate sql from a question, but only allows the API key to execute any SQL statement

4. Click **Next**. The public key and private key are displayed.

   Make sure that you have copied and saved the private key in a secure location. After leaving this page, you will not be able to get the full private key again.

5. Click **Done**.

## Step 3. Call the Chat2Query v2 endpoints

### Call generate data summary on your database before start chat2data

**Before you start chat2query, let ai analyze the database first. so the ai can generate get a better performance in sql generation.**

In the left pane of the [**Data Service**](https://tidbcloud.com/console/data-service) page, click **Chat2Query** > **POST /v2/dataSummaries** to view the endpoint details. The **Properties** are displayed:

- **Endpoint Path**: (read-only) the path of the endpoint, which is `/v2/dataSummaries`.

- **Endpoint URL**: (read-only) the URL of the generate data summary endpoint, which is used to call the endpoint. For example, `https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/dataSummaries`.

- **Request Method**: (read-only) the HTTP method of the generate data summary endpoint, which is `POST`.

- **Timeout(ms)**: the timeout for the generate data summaries endpoint, in milliseconds.

TiDB Cloud generates code examples to help you call an endpoint. To get the examples and run the code, perform the following steps:

1.  On the current **generate data summary** page, click **Code Example** to the right of **Endpoint URL**. The **Code Example** dialog box is displayed.
2.  In the dialog box, select the cluster and database that you want to use to call the endpoint, and then copy the code example.
3.  Paste the code example in your application and run it.

        - Replace the `${PUBLIC_KEY}` and `${PRIVATE_KEY}` placeholders with your API key.

    > **Note:**
    >
    > Each Chat2Query Data App has a rate limit of 100 requests per day. If you exceed the rate limit, the API returns a `429` error. For more quota, you can [submit a request](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519) to our support team.

The following code example is used to explore `sp500insight` database:

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

The response is as follows:

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

The api is an async api, we should poll the job results in get job api by each 5 seconds until the job been successed.

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>`/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1699518950, // when the job finished, it's UNIX timestamp
    "job_id": "79c2b3d36c074943ab06a29e45dd5887",  // ID of current job
    "result": DataSummaryObject, // see the definition bellow
    "status": "done" // status of the current job
  }
}
```

`DataSummaryObject` represents AI explored infomation of the given database, here is the structure of `DataSummaryObject`:

```json
{
    "cluster_id": 10939961583884005000, // your cluster id
    "db_name": "sp500insight", // database name
    "db_schema": { // database schema infomation
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
            "status": "done", // generation status
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

**Get data summary result using data summary id in anytime**

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/dataSummaries/{data_summary_id}'\
 --header 'content-type: application/json'
```

The response is as follows:

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

**Update data summary result using data summary id when you have an better result**

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
- `columns`: a Key-Value represent the columns and descriptions you want to update

The response is as follows:

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "job_id": "103d0bf8d8564ec7b2c768d3180d8ab1"
  }
}
```

You can query the job detail by running:

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

when the `status` is `done`, the job had finished and description of table and columns had been updated.

**Next we generate sql using chat2data v2 endpoints**

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
  "data_summary_id": <Your data summary id>,
  "raw_question": "<Your question to generate data>"
}'
```

In the preceding example, the request body is a JSON object with the following properties:

- `data_summary_id`: _string_. A unique identifier generated by create data summary api above.
- `raw_question`: _string_. A natural language describing the query you want.

The response is as follows:

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "job_id": "3966d5bd95324a6283445e3a02ccd97c"
  }
}
```

The api is an async api, we should poll the job results in get job api by each 5 seconds until the job been successed.

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

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

## Step 4. Call the Chat2Data v1 endpoint

You can call chat2data v1 endpoint directly get sql generated result. this api will give a faster response but lower performance.

In the left pane of the [**Data Service**](https://tidbcloud.com/console/data-service) page, click **Chat2Query** > **/chat2data** to view the endpoint details. The **Properties** of Chat2Data are displayed:

- **Endpoint Path**: (read-only) the path of the Chat2Data endpoint, which is `/chat2data`.

- **Endpoint URL**: (read-only) the URL of the Chat2Data endpoint, which is used to call the endpoint. For example, `https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data`.

- **Request Method**: (read-only) the HTTP method of the Chat2Data endpoint, which is `POST`.

- **Timeout(ms)**: the timeout for the Chat2Data endpoint, in milliseconds.

- **Max Rows**: the maximum number of rows that the Chat2Data endpoint returns.

TiDB Cloud generates code examples to help you call an endpoint. To get the examples and run the code, perform the following steps:

1. On the current **Chat2Data** page, click **Code Example** to the right of **Endpoint URL**. The **Code Example** dialog box is displayed.
2. In the dialog box, select the cluster and database that you want to use to call the endpoint, and then copy the code example.
3. Paste the code example in your application and run it.

   - Replace the `${PUBLIC_KEY}` and `${PRIVATE_KEY}` placeholders with your API key.
   - Replace the `<your instruction>` placeholder with the instruction you want AI to generate and execute SQL statements.
   - Replace the `<your table name, optional>` placeholder with the table name you want to query. If you do not specify a table name, AI will query all tables in the database.

> **Note:**
>
> Each Chat2Query Data App has a rate limit of 100 requests per day. If you exceed the rate limit, the API returns a `429` error. For more quota, you can [submit a request](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519) to our support team.
> API Key with the role `Chat2Query Data Context Management Role` cannot call the Chat2Data v1 endpoint.

The following code example is used to count how many users in `sp500insight.users` table:

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
