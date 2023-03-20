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

Before using the Chat2Query API, make sure that you have created a [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) cluster. If you do not have one, follow the steps in [Create a cluster](/tidb-cloud/create-tidb-cluster.md) to create one.

## 1. Enable the Chat2Query API

To enable the Chat2Query API, perform the following steps:

1. Go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can view the project list and switch to another project from the ☰ hover menu in the upper-left corner.

2. Click your cluster name, and then click **Chat2Query** in the left navigation pane.
3. In the upper-right corner of Chat2Query, click **...** and select **Settings**.
4. Enable **DataAPI** and the **you can view and manage Chat2Query API in Data Service** message is displayed.
5. Click **Data Service** to access the Chat2Query APi. The **Chat2Query System** [Data App](tidb-cloud/tidb-cloud-glossary.md#data-app) and its **Chat2Data** [endpoint](tidb-cloud/tidb-cloud-glossary.md#endpoint) will be displayed in the left pane.

## 2. Create an API key

Before calling an endpoint, you need to create an API key. To create an API key for the Chat2Query Data App, perform the following steps:

1. In the left pane of [**Data Service**](https://tidbcloud.com/console/dataservice), click the name of **Chat2Query System** to view its details.
3. In the **API Key** area, click **Create API Key**.
4. In the **Create API Key** dialog box, enter a description for your API key, and then click **Next**. The private key and public key are displayed.

    Make sure that you have copied and saved the private key in a secure location. After leaving this page, you will not be able to get the full private key again.

5. Click **Done**.

## 3. Call the Chat2Data endpoint

In the left pane of the [**Data Service**](https://tidbcloud.com/console/dataservice) page, click **Chat2Query** > **Chat2Data** to view the endpoint details. The **Properties** of Chat2Data are displayed:

- **Endpoint URL**: (read-only) the URL of the Chat2Data endpoint, which is used to call the endpoint. For example, `https://data.tidbcloud.com/api/v1beta/apps/chat2query-{ID}}/v1/chat2data`.

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

TiDB Cloud generates code examples to help you call an endpoint. To get the code example, perform the following steps:

1. In the Chat2Data details page, click **Code Example** to the right of **Endpoint URL**. The **Code Example** dialog box is displayed.
2. In the dialog box, select the cluster, database, and language that you want to use to call the endpoint, and then copy the code example.
3. Paste the code example in your application and run it.

    - Replace the `<Public Key>` and `<Private Key>` placeholders with your API key.
    - Replace the `<your instruction>` placeholder with the instruction you want AI to generate and execute SQL statements.

An example of the curl code example is as follows:

```bash
curl --digest --user '<Public Key>:<Private Key>' \
  --request POST 'https://data.tidbcloud.com/api/v1beta/apps/chat2query-ABCDEFGH/v1/chat2data' \
  --header 'content-type: application/json' \
  --data-raw '{
      "cluster_id": "12345678912345678960",
      "database": "sample_data",
      "instruction": "Find the most popular repo from GitHub events"
      }'
```

The response is as follows:

```json
{
"type":"chat2data_endpoint",
"data": {
        "columns":[
        {
                    "col": "id",
                    "data_type": "INT",
                    "nullable": false
                },
                {
                    "col": "name",
                    "data_type": "VARCHAR",
                    "nullable": true
                }
        ],
        "rows":[
            {"id":"1","name":"Wolf"}
        ]
        "result":{
            "code": 200,
            "message": "ok",
            "start_ms": 1678965476709,
            "end_ms": 1678965476839,
            "latency": "130ms",
            "row_count": 1,
            "row_affect": 0,
            "limit": 500,
            "query": "Query OK!",
            "sql": "select id,name from sample_data.github_events limit 1;",
            "ai_latency": "30ms"
        }
    }
}
```

If your API call is not successful, you will receive a status code other than `200`. The following is an example of the `401` status code:

```json
{
        "type": "chat2data_endpoint",
        "data": {
                "columns": [],
                "rows": [],
                "result": {
                        "code": 401,
                        "message": "auth failed",
                        "start_ms": 0,
                        "end_ms": 0,
                        "latency": "",
                        "row_count": 0,
                        "row_affect": 0,
                        "limit": 0,
                        "query": "",
                        "sql": "",
                        "ai_latency": ""
                }
        }
}
```

## Learn more

- [Manage an API key](/tidb-cloud/data-service-api-key.md)
- [Response and Error Codes of Data Service](/tidb-cloud/data-service-response-and-error-code.md)
