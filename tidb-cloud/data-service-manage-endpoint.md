---
title: Manage an Endpoint
summary: Learn how to create, develop, test, deploy, and delete an endpoint in a Data App in the TiDB Cloud console.
---

# Manage an Endpoint

An endpoint in Data Service (beta) is a web API that you can customize to execute SQL statements. You can specify parameters for the SQL statements, such as the value used in the `WHERE` clause. When a client calls an endpoint and provides values for the parameters in a request URL, the endpoint executes the SQL statement with the provided parameters and returns the results as part of the HTTP response.

This document describes how to manage your endpoints in a Data App in the TiDB Cloud console.

## Before you begin

Before you manage an endpoint, make sure that you have created a cluster and a Data App. For more information, see [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md) and [Create a Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app).

Before you call an endpoint, make sure that you have created an API key in the Data App. For more information, see [Create an API key](/tidb-cloud/data-service-api-key.md#create-an-api-key).

## Create an endpoint

To create an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App and click **...** > **Create Endpoint**. You can update the default name if necessary.

    > **Tip:**
    >
    > Alternatively, you can also locate the Data App and click **+** **Create Endpoint** at the top of the left pane.

3. The newly created endpoint is added to the top of the endpoint list.

You can also create an endpoint from a SQL file in Chat2Query (beta). For more details, see [Generate an endpoint from a SQL file](/tidb-cloud/explore-data-with-chat2query.md#generate-an-endpoint-from-a-sql-file)

## Develop an endpoint

For each endpoint, you can write SQL statements to execute on a TiDB cluster, define parameters for the SQL statements, or manage the name and version.

### Configure properties

On the right pane of the endpoint details page, you can click the **Properties** tab to view and manage the following properties of the endpoint:

- **Endpoint Path**: the unique path of the endpoint that users use to access it.

    - The path must be unique within a Data App.
    - Only letters, numbers, underscores (`_`), and slashes (`/`) are allowed in the path, which must start with a slash (`/`). For example, `/my_endpoint/get_id`.
    - The length of the path must be less than 64 characters.

- **Endpoint URL**: (read-only) the URL is automatically generated based on the region where the corresponding cluster is hosted, the service URL of the Data App, and the path of the endpoint. For example, if the path of the endpoint is `/my_endpoint/get_id`, the endpoint URL is `https://<region>.data.tidbcloud.com/api/v1beta/app/<App ID>/endpoint/my_endpoint/get_id`.

- **Request Method**: the HTTP method of the endpoint. The following methods are supported:

    - `GET`: use this method to query data, such as a `SELECT` statement.
    - `POST`: use this method to insert data, such as an `INSERT` statement.

- **Timeout(ms)**: the timeout for the endpoint.

    - Default value: `5000`
    - Maximum value: `30000`
    - Minimum value: `1`
    - Unit: millisecond

- **Max Rows**: the maximum number of rows that the endpoint returns.

    - Default value: `50`
    - Maximum value: `2000`
    - Minimum value: `1`

- **Description** (Optional): the description of the endpoint.

### Write SQL statements

On the SQL editor of the endpoint details page, you can write and run the SQL statements for an endpoint. You can also simply type `--` followed by your instructions to let AI generate SQL statements automatically.

1. Select a cluster.

    > **Note:**
    >
    > Only clusters that are linked to the Data App are displayed in the drop-down list. To manage the linked clusters, see [Manage linked clusters](/tidb-cloud/data-service-manage-data-app.md#manage-linked-clusters).

    On the upper part of the SQL editor, select a cluster on which you want to execute SQL statements from the drop-down list. Then, you can view all databases of this cluster in the **Schema** tab on the right pane.

2. Write SQL statements.

    Before querying or modifying data, you need to first specify the database in the SQL statements. For example, `USE database_name;`.

    In the SQL editor, you can write statements such as table join queries, complex queries, and aggregate functions. You can also simply type `--` followed by your instructions to let AI generate SQL statements automatically.

    To define a parameter, you can insert it as a variable placeholder like `${ID}` in the SQL statement. For example, `SELECT * FROM table_name WHERE id = ${ID}`. Then, you can click the **Params** tab on the right pane to change the parameter definition and test values. For more information, see [Parameters](#configure-parameters).

    > **Note:**
    >
    > - The parameter name is case-sensitive.
    > - The parameter cannot be used as a table name or column name.

3. Run SQL statements.

    If you have inserted parameters in the SQL statements, make sure that you have set test values or default values for the parameters in the **Params** tab on the right pane. Otherwise, an error is returned.

    To run a SQL statement, select the line of the SQL with your cursor and click **Run** > **Run at cursor**.

    To run all SQL statements in the SQL editor, click **Run**. In this case, only the last SQL results are returned.

    After running the statements, you can see the query results immediately in the **Result** tab at the bottom of the page.

### Configure parameters

On the right pane of the endpoint details page, you can click the **Params** tab to view and manage the parameters used in the endpoint.

In the **Definition** section, you can view and manage the following properties for a parameter:

- The parameter name: the name can only include letters, digits, and underscores (`_`) and must start with a letter or an underscore (`_`).
- **Required**: specifies whether the parameter is required in the request. The default configuration is set to not required.
- **Type**: specifies the data type of the parameter. Supported values are `STRING`, `NUMBER`, and `BOOLEAN`.  When using a `STRING` type parameter, you do not need to add quotation marks (`'` or `"`). For example, `foo` is valid for the `STRING` type and is processed as `"foo"`, whereas `"foo"` is processed as `"\"foo\""`.
- **Default Value**: specifies the default value of the parameter.

    - Make sure that the value can be converted to the type of parameter. Otherwise, the endpoint returns an error.
    - If you do not set a test value for a parameter, the default value is used when testing the endpoint.

In the **Test Values** section, you can view and set test parameters. These values are used as the parameter values when you test the endpoint. Make sure that the value can be converted to the type of parameter. Otherwise, the endpoint returns an error.

### Manage versions

On the right pane of the endpoint details page, you can click the **Deployments** tab to view and manage the deployed versions of the endpoint.

In the **Deployments** tab, you can deploy a draft version and undeploy the online version.

### Rename

To rename an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Locate the endpoint you want to rename, click **...** > **Rename**., and enter a new name for the endpoint.

## Test an endpoint

To test an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Click the name of the endpoint you want to test to view its details.
4. (Optional) If the endpoint contains parameters, you need to set test values before testing.

    1. On the right pane of the endpoint details page, click the **Params** tab.
    2. Expand the **Test Values** section and set test values for the parameters.

        If you do not set a test value for a parameter, the default value is used.

5. Click **Test** in the upper-right corner.

    > **Tip:**
    >
    > Alternatively, you can also press <kbd>F5</kbd> to test the endpoint.

After testing the endpoint, you can see the response as JSON at the bottom of the page. For more information about the JSON response, refer to [Response of an endpoint](#response).

## Deploy an endpoint

To deploy an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Locate the endpoint you want to deploy, click the endpoint name to view its details, and then click **Deploy** in the upper-right corner.

4. Click **Deploy** to confirm the deployment. You will get the **Endpoint has been deployed** prompt if the endpoint is successfully deployed.

    On the right pane of the endpoint details page, you can click the **Deployments** tab to view the deployed history.

## Call an endpoint

To call an endpoint, you can send an HTTPS request to either an undeployed draft version or a deployed online version of the endpoint.

### Prerequisites

Before calling an endpoint, you need to create an API key. For more information, refer to [Create an API key](/tidb-cloud/data-service-api-key.md#create-an-api-key).

### Request

TiDB Cloud generates code examples to help you call an endpoint. To get the code example, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Locate the endpoint you want to call and click **...** > **Code Example**. The **Code Example** dialog box is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the endpoint name to view its details and click **...** > **Code Example** in the upper-right corner.

4. In the dialog box, select the cluster and database that you want to use to call the endpoint, and then copy the code example.

    > **Note:**
    >
    > - The code examples are generated based on the properties and parameters of the endpoint.
    > - The online environment is available only after you deploy the endpoint.
    > - Currently, TiDB Cloud only provides the curl code example.

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
    > - By requesting the regional domain `<region>.data.tidbcloud.com`, you can directly access the data API in the region where the TiDB cluster is located.
    > - Alternatively, you can also request the global domain `data.tidbcloud.com` without specifying the region information. In this way, TiDB Cloud will internally redirect the request to the target region, but this might result in additional latency. If you choose this way, make sure to add the `--location-trusted` option to your curl code when calling an endpoint.

5. Paste the code example in your application and run it.

    - You need to replace the `<Public Key>` and `<Private Key>` placeholders with your API key. For more information, refer to [Manage an API key](/tidb-cloud/data-service-api-key.md).
    - If the endpoint contains parameters, specify the parameter values when calling the endpoint.

### Response

After calling an endpoint, you can see the response in JSON format. For more information, see [Response and Status Codes of Data Service](/tidb-cloud/data-service-response-and-status-code.md).

## Undeploy an endpoint

To undeploy an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Click the name of the endpoint you want to undeploy to view its details.
4. On the right pane of the endpoint details page, click the **Deployments** tab. The deployed version page is displayed.
5. Locate the current online version and click **Undeploy**. The version status will be changed to **Offline**.

## Delete an endpoint

> **Note:**
>
> Before you delete an endpoint, make sure that the endpoint is not online. Otherwise, the endpoint cannot be deleted. To undeploy an endpoint, refer to [Undeploy an endpoint](#undeploy-an-endpoint).

To delete an endpoint, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its endpoints.
3. Locate the endpoint you want to delete and click **...** > **Delete**. The **Confirm deletion of endpoint** dialog box is displayed.

    > **Tip:**
    >
    > Alternatively, you can also click the endpoint name to view its details and click **...** > **Delete** in the upper-right corner.

4. Click **Delete** to confirm the deletion.
