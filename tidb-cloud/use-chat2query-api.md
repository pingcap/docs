---
title: Get Started with Chat2Query API
summary: Learn how to use TiDB Cloud Chat2Query API to generate and execute SQL statements using AI by providing instructions.
---

# Get Started with Chat2Query API

TiDB Cloud provides the Chat2Query API, a RESTful interface that allows you to generate and execute SQL statements using AI by providing instructions. Then, the API returns the query results for you.

Chat2Query API can only be accessed through HTTPS, ensuring that all data transmitted over the network is encrypted using TLS.

> **Note:**
>
> Chat2Query API is only available for [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) clusters.

## Before you begin

Before using the Chat2Query API, make sure that you have created a [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) cluster and enabled [AI to generate SQL queries](/tidb-cloud/explore-data-with-chat2query.md). If you do not have a Serverless Tier cluster, follow the steps in [Create a cluster](/tidb-cloud/create-tidb-cluster.md) to create one.

## Step 1. Enable the Chat2Query API

To enable the Chat2Query API, perform the following steps:

1. Go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can view the project list and switch to another project from the ☰ hover menu in the upper-left corner.

2. Click your cluster name, and then click **Chat2Query** in the left navigation pane.
3. In the upper-right corner of Chat2Query, click **...** and select **Settings**.
4. Enable **DataAPI** and the Chat2Query Data App is created.

    > **Note:**
    >
    > After DataAPI is enabled for one Serverless Tier cluster, all Serverless Tier clusters in the same project can use the Chat2Query API.

5. Click **Data Service** in the message to access the Chat2Query API.

    You can find that the **Chat2Query System** [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) and its **Chat2Data** [endpoint](/tidb-cloud/tidb-cloud-glossary.md#endpoint) are displayed in the left pane.

## Step 2. Create an API key

Before calling an endpoint, you need to create an API key. To create an API key for the Chat2Query Data App, perform the following steps:

1. In the left pane of [**Data Service**](https://tidbcloud.com/console/dataservice), click the name of **Chat2Query System** to view its details.
2. In the **API Key** area, click **Create API Key**.
3. In the **Create API Key** dialog box, enter a description for your API key, and then click **Next**. The private key and public key are displayed.

    Make sure that you have copied and saved the private key in a secure location. After leaving this page, you will not be able to get the full private key again.

4. Click **Done**.

## Step 3. Call the Chat2Data endpoint

In the left pane of the [**Data Service**](https://tidbcloud.com/console/dataservice) page, click **Chat2Query** > **/chat2data** to view the endpoint details. The **Properties** of Chat2Data are displayed:

- **Endpoint Path**: (read-only) the path of the Chat2Data endpoint, which is `/chat2data`.

- **Endpoint URL**: (read-only) the URL of the Chat2Data endpoint, which is used to call the endpoint. For example, `https://data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data`.

- **Request Method**: (read-only) the HTTP method of the Chat2Data endpoint, which is `POST`.

- **Timeout(ms)**: the timeout for the Chat2Data endpoint.

    - Default value: `30000`
    - Maximum value: `30000`
    - Minimum value: `1`
    - Unit: millisecond

- **Max Rows**: the maximum number of rows that the Chat2Data endpoint returns.

    - Default value: `50`
    - Maximum value: `2000`
    - Minimum value: `1`

TiDB Cloud generates code examples to help you call an endpoint. To get the examples and run the code, perform the following steps:

1. On the current **Chat2Data** page, click **Code Example** to the right of **Endpoint URL**. The **Code Example** dialog box is displayed.
2. In the dialog box, select the cluster and database that you want to use to call the endpoint, and then copy the code example.
3. Paste the code example in your application and run it.

    - Replace the `<Public Key>` and `<Private Key>` placeholders with your API key.
    - Replace the `<your instruction>` placeholder with the instruction you want AI to generate and execute SQL statements.
    - Replace the `<your table name, optional>` placeholder with the table name you want to query. If you do not specify a table name, AI will query all tables in the database.

The following code example is used to find the most popular GitHub repository from `sample_data.github_events` table:

```bash
curl --digest --user '<Public Key>:<Private Key>' \
  --request POST 'https://data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data' \
  --header 'content-type: application/json' \
  --data-raw '{
      "cluster_id": "12345678912345678960",
      "database": "sample_data",
      "tables": ["github_events"],
      "instruction": "Find the most popular repo from GitHub events"
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
                "col": "repo_name",
                "data_type": "VARCHAR",
                "nullable": false
            },
            {
                "col": "count",
                "data_type": "BIGINT",
                "nullable": false
            }
        ],
        "rows": [
            {
                "count": "2390",
                "repo_name": "pytorch/pytorch"
            }
        ],
        "result": {
            "code": 200,
            "message": "ok",
            "start_ms": 1678965476709,
            "end_ms": 1678965476839,
            "latency": "130ms",
            "row_count": 1,
            "row_affect": 0,
            "limit": 50,
            "query": "Query OK!",
            "sql": "SELECT sample_data.github_events.`repo_name`, COUNT(*) AS count FROM sample_data.github_events GROUP BY sample_data.github_events.`repo_name` ORDER BY count DESC LIMIT 1;",
            "ai_latency": "30ms"
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
            "limit": 0,
            "query": ""
        }
    }
}
```

## Learn more

- [Manage an API key](/tidb-cloud/data-service-api-key.md)
- [Response and Error Codes of Data Service](/tidb-cloud/data-service-response-and-error-code.md)
