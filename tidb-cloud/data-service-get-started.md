---
title: Get Started with Data Service
summary: Learn how to use TiDB Cloud Data Service to access your data with HTTPS requests.
---

# Get Started with Data Service

Data Service (beta) enables you to access TiDB Cloud data via an HTTPS request using a custom API endpoint and allows you to seamlessly integrate with any application or service that is compatible with HTTPS.

> **Tip:**
>
> TiDB Cloud provides a Chat2Query API for TiDB Serverless clusters. After it is enabled, TiDB Cloud will automatically create a system Data App called **Chat2Query** and a Chat2Data endpoint in Data Service. You can call this endpoint to let AI generate and execute SQL statements by providing instructions.
>
> For more information, see [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md).

This document introduces how to quickly get started with TiDB Cloud Data Service (beta) by creating a Data App, developing, testing, deploying, and calling an endpoint.

## Before you begin

Before creating a Data App, make sure that you have created a [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta) cluster. If you do not have one, follow the steps in [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md) to create one.

## Step 1. Create a Data App

A Data App is a group of endpoints that you can use to access data for a specific application. To create a Data App, perform the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).

2. In the left navigation pane, click <MDSvgIcon name="icon-left-data-service" /> **Data Service**.

3. On the **Get started by creating your first data application** page, enter a name and select clusters that you want the Data App to access.

4. (Optional) To automatically deploy endpoints of the Data App to your preferred GitHub repository and branch, enable **Connect to GitHub**, and then do the following:

    1. Click **Install on GitHub**, and then follow the on-screen instructions to install **TiDB Cloud Data Service** as an application on your target repository.
    2. Click **Authorize** to authorize access to the application on GitHub.
    3. Specify the target repository, branch, and directory where you want to save the configuration files of your Data App.

    > **Note:**
    >
    > - The directory must start with a slash (`/`). For example, `/mydata`. If the directory you specified does not exist in the target repository and branch, it will be created automatically.
    > - The combination of repository, branch, and directory identifies the path of the configuration files, which must be unique among Data Apps. If your specified path is already used by another Data App, you need to specify a new path instead. Otherwise, the endpoints configured in the TiDB Cloud console for the current Data App will overwrite the files in your specified path.

5. Click **Create Data App**. The [**Data Service**](https://tidbcloud.com/console/data-service) details page is displayed.

6. If you have configured to connect your Data App to GitHub, check your specified GitHub directory. You will find that the [Data App configuration files](/tidb-cloud/data-service-app-config-files.md) have been committed to the directory by `tidb-cloud-data-service`, which means that your Data App is connected to GitHub successfully.

    For your new Data App, **Auto Sync & Deployment** and **Review Draft** are enabled by default so you can easily synchronize Data App changes between TiDB Cloud console and GitHub and review changes before the deployment. For more information about the GitHub integration, see [Deploy your Data App changes with GitHub automatically](/tidb-cloud/data-service-manage-github-connection.md).

## Step 2. Develop an endpoint

An endpoint is a web API that you can customize to execute SQL statements.

After creating a Data App, a default `untitled endpoint` is created for you automatically. You can use the default endpoint to access your TiDB Cloud cluster.

If you want to create a new endpoint, locate the newly created Data App and click **+** **Create Endpoint** to the right of the App name.

### Configure properties

On the right pane, click the **Properties** tab and set properties for the endpoint, such as:

- **Endpoint Path**: the unique path of the endpoint that users use to access it.

    - The path must be unique within a Data App.
    - Only letters, numbers, underscores (`_`), and slashes (`/`) are allowed in the path, which must start with a slash (`/`) and end with a letter, number, or underscore (`_`). For example, `/my_endpoint/get_id`.
    - The length of the path must be less than 64 characters.

- **Endpoint URL**: (read-only) the URL is automatically generated based on the region where the corresponding cluster is located, the service URL of the Data App, and the path of the endpoint. For example, if the path of the endpoint is `/my_endpoint/get_id`, the endpoint URL is `https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id`.

- **Request Method**: the HTTP method of the endpoint. The following methods are supported:

    - `GET`: use this method to query data, such as a `SELECT` statement.
    - `POST`: use this method to insert data, such as an `INSERT` statement.

- **Timeout(ms)**: the timeout for the endpoint. It ranges from `1` to `30000`. The default value is `5000` milliseconds. For more details, see [Configure properties](/tidb-cloud/data-service-manage-endpoint.md#configure-properties).

- **Max Rows**: the maximum number of rows that the endpoint returns. It ranges from `1` to `2000`. The default value is `50` rows. For more details, see [Configure properties](/tidb-cloud/data-service-manage-endpoint.md#configure-properties).

### Write SQL statements

You can customize SQL statements for the endpoint in the SQL editor, which is the middle pane on the **Data Service** page.

1. Select a cluster.

    > **Note:**
    >
    > Only clusters that are linked to the Data App are displayed in the drop-down list. To manage the linked clusters, see [Manage linked clusters](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources).

    On the upper part of the SQL editor, select a cluster on which you want to execute SQL statements from the drop-down list. Then, you can view all databases of this cluster in the **Schema** tab on the right pane.

2. Write SQL statements.

    Before querying or modifying data, you need to first specify the database in the SQL statements. For example, `USE database_name;`.

    In the SQL editor, you can write statements such as table join queries, complex queries, and aggregate functions. You can also simply type `--` followed by your instructions to let AI generate SQL statements automatically.

    To define a parameter, you can insert it as a variable placeholder like `${ID}` in the SQL statement. For example, `SELECT * FROM table_name WHERE id = ${ID}`. Then, you can click the **Params** tab on the right pane to change the parameter definition and test values.

    > **Note:**
    >
    > - The parameter name is case-sensitive.
    > - The parameter cannot be used as a table name or column name.

    - In the **Definition** section, you can specify whether the parameter is required when a client calls the endpoint, the data type (`STRING`, `NUMBER`, or `BOOLEAN`), and the default value of the parameter. When using a `STRING` type parameter, you do not need to add quotation marks (`'` or `"`). For example, `foo` is valid for the `STRING` type and is processed as `"foo"`, whereas `"foo"` is processed as `"\"foo\""`.
    - In the **Test Values** section, you can set the test value for a parameter. The test values are used when you run the SQL statements or test the endpoint. If you do not set the test values, the default values are used.
    - For more information, see [Configure parameters](/tidb-cloud/data-service-manage-endpoint.md#configure-parameters).

3. Run SQL statements.

    If you have inserted parameters in the SQL statements, make sure that you have set test values or default values for the parameters in the **Params** tab on the right pane. Otherwise, an error is returned.

    To run a SQL statement, select the line of the SQL with your cursor and click **Run** > **Run at cursor**.

    To run all SQL statements in the SQL editor, click **Run**. In this case, only the last SQL results are returned.

    After running the statements, you can see the query results immediately in the **Result** tab at the bottom of the page.

## Step 3. Test the endpoint (optional)

After configuring an endpoint, you can test the endpoint to verify whether it works as expected before deploying.

To test the endpoint, click **Test** in the upper-right corner or press **F5**.

Then, you can see the response in the **HTTP Response** tab at the bottom of the page. For more information about the response, see [Response of an endpoint](/tidb-cloud/data-service-manage-endpoint.md#response).

## Step 4. Deploy the endpoint

To deploy the endpoint, perform the following steps:

1. On the endpoint details page, click **Deploy** in the upper-right corner.

2. Click **Deploy** to confirm the deployment. You will get the **Endpoint has been deployed** prompt if the endpoint is successfully deployed.

    On the right pane of the endpoint details page, you can click the **Deployments** tab to view the deployed history.

## Step 5. Call the endpoint

You can call the endpoint by sending an HTTPS request. Before calling an endpoint, you need to first obtain an API key for the Data App.

### 1. Create an API key

1. In the left pane of the [**Data Service**](https://tidbcloud.com/console/data-service) page, click the name of your Data App to view its details.
2. In the **API Key** area, click **Create API Key**.
3. In the **Create API Key** dialog box, enter a description and select a role for your API key.

    The role is used to control whether the API key can read or write data to the clusters linked to the Data App. You can select the `ReadOnly` or `ReadAndWrite` role:

    - `ReadOnly`: only allows the API key to read data, such as `SELECT`, `SHOW`, `USE`, `DESC`, and `EXPLAIN` statements.
    - `ReadAndWrite`: allows the API key to read and write data. You can use this API key to execute all SQL statements, such as DML and DDL statements.

4. Click **Next**. The public key and private key are displayed.

    Make sure that you have copied and saved the private key in a secure location. After leaving this page, you will not be able to get the full private key again.

5. Click **Done**.

### 2. Get the code example

TiDB Cloud generates code examples to help you call an endpoint. To get the code example, perform the following steps:

1. In the left pane of the [**Data Service**](https://tidbcloud.com/console/data-service) page, click the name of your endpoint, and then click **...** > **Code Example** in the upper-right corner. The **Code Example** dialog box is displayed.

2. In the dialog box, select the cluster and database that you want to use to call the endpoint, and then copy the code example.

    An example of the curl code example is as follows:

    <SimpleTab>
    <div label="Test Environment">

    To call a draft version of the endpoint, you need to add the `endpoint-type: draft` header:

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>' \
      --header 'endpoint-type: draft'
    ```

    </div>

    <div label="Online Environment">

    You must deploy your endpoint first before checking the code example in the online environment.

    To call the current online version of the endpoint, use the following command:

    ```bash
    curl --digest --user '<Public Key>:<Private Key>' \
      --request GET 'https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/<Endpoint Path>'
    ```

    </div>
    </SimpleTab>

    > **Note:**
    >
    > - By requesting the regional domain `<region>.data.tidbcloud.com`, you can directly access the endpoint in the region where the TiDB cluster is located.
    > - Alternatively, you can also request the global domain `data.tidbcloud.com` without specifying a region. In this way, TiDB Cloud will internally redirect the request to the target region, but this might result in additional latency. If you choose this way, make sure to add the `--location-trusted` option to your curl command when calling an endpoint.

### 3. Use the code example

Paste the code example in your application and run it. Then, you can get the response of the endpoint.

- You need to replace the `<Public Key>` and `<Private Key>` placeholders with your API key.
- If the endpoint contains parameters, specify the parameter values when calling the endpoint.

After calling an endpoint, you can see the response in JSON format. The following is an example:

```json
{
  "type": "sql_endpoint",
  "data": {
    "columns": [
      {
        "col": "id",
        "data_type": "BIGINT",
        "nullable": false
      },
      {
        "col": "type",
        "data_type": "VARCHAR",
        "nullable": false
      }
    ],
    "rows": [
      {
        "id": "20008295419",
        "type": "CreateEvent"
      }
    ],
    "result": {
      "code": 200,
      "message": "Query OK!",
      "start_ms": 1678965476709,
      "end_ms": 1678965476839,
      "latency": "130ms",
      "row_count": 1,
      "row_affect": 0,
      "limit": 50
    }
  }
}
```

For more information about the response, see [Response of an endpoint](/tidb-cloud/data-service-manage-endpoint.md#response).

## Learn more

- [Data Service Overview](/tidb-cloud/data-service-overview.md)
- [Get Started with Chat2Query API](/tidb-cloud/use-chat2query-api.md)
- [Manage a Data App](/tidb-cloud/data-service-manage-data-app.md)
- [Manage an Endpoint](/tidb-cloud/data-service-manage-endpoint.md)
