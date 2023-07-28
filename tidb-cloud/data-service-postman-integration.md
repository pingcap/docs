---
title: Run Data App in Postman
summary: Learn how to run your Data App in Postman.
---

# Run Data App in Postman

[Postman](https://www.postman.com/) is an API platform for building and using APIs, which simplifies each step of the API lifecycle and streamlines collaboration so you can create better APIs—faster.

In TiDB Cloud [Data Service](https://tidbcloud.com/console/data-service), you can easily import your Data App to Postman and leverage Postman's extensive tools to enhance your API development experience.

This document describes how to import your Data App to Postman and how to run your Data App in Postman.

## Before you begin

Before importing a Data App to Postman, make sure that you have the following:

- A [Postman](https://www.postman.com/) account.
- A [Postman Desktop app](https://www.postman.com/downloads/) (Optional. You can use the Postman webpage version without downloading the app.)
- A [Data App](/tidb-cloud/data-service-manage-data-app.md) with at least one [endpoint](/tidb-cloud/data-service-manage-endpoint.md). Only endpoints that meet the following requirements can be imported to Postman:

    - The target cluster is selected.
    - The endpoint path and request method are configured.
    - The SQL statements are written.

- An [API key](/tidb-cloud/data-service-api-key.md#create-an-api-key) for the Data App.

## Step 1. Import your Data App to Postman

To import your Data App to Postman, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the upper-right corner of the page, click **Run in Postman**. A dialog for import instructions is displayed.

    > **Note:**
    >
    > - If a Data App does not have any endpoint with the target cluster, path, request method, and SQL statements configured, **Run in Postman** is unclickable for the Data App.
    > - For `Chat2Query` Data App, **Run in Postman** is unavailable.

4. Follow the steps provided in the dialog for the Data App import:

    1. Depending on the Postman version you want to use, click **Run in Postman for Web** or **Run in Postman Desktop** to open your Postman workspaces, and then click your target workspace in Postman.

        - If you have not logged into Postman, follow the on-screen instructions log into Postman first.
        - If you clicked **Run in Postman Desktop**, follow the on-screen instructions to open the Postman client.

    2. On the page of your target workspace in Postman, click **Import** in the left navigation menu.
    3. Copy the Data App URL in the TiDB Cloud dialog, and then past the URL to Postman for the import.

5. After you paste the URL, Postman imports the Data App automatically as a new [collection](https://learning.postman.com/docs/collections/collections-overview/). The name of the collection is in the `TiDB Data Service - <Your App Name>` format.

    In the collection, the deployed endpoints are grouped in the **Deployed** folder and the undeployed endpoints are grouped in the **Draft** folder.

## Step 2. Configure your Data App API key in Postman

Before running the imported Data App in Postman, you need to configure the API key for the Data App in Postman as follows:

1. In the left navigation pane of Postman, click `TiDB Data Service - <Your App Name>` to open a tab for it on the right side.
2. Under the `TiDB Data Service - <Your App Name>` tab, click the **Variables** tab.
3. In the variable table, paste your public key and private key for your Data App to the **Current value** column.
4. In the upper-right corner of the `TiDB Data Service - <Your App Name>` tab, click **Save**.

## Step 3. Run Data App in Postman

To run your Data App in Postman, take the following steps:

1. In the left navigation pane of Postman, expand the **Deployed** or **Draft** folder, and then click your endpoint name to open a tab for it on the right side.
2. Under the `<Your Endpoint Name>` tab, you can call your endpoint as follows:

    - For an endpoint without parameters, you can click **Send** to call it directly.
    - For an endpoint with parameters, you need to fill in the values of the parameters first, and then click **Send**.

        - For a `GET` or `DELETE` request, fill in values of the parameters in the **Query Params** table.
        - For a `POST` or `PUT` request, click the **Body** tab, and then fill in values of the parameters as an JSON object. If **Batch Operation** is enabled for the endpoint in TiDB Cloud Data Service, fill in values of the parameters as an array of JSON objects.

3. Check the response in the lower pane.

4. If you want to call the endpoint again with different parameter values, you can edit the parameter values accordingly, and then click **Send** again.

To learn more about the Postman usage, see [Postman documentation](https://learning.postman.com/docs).

## Deal with new changes in Data App

After a Data App is imported to Postman, TiDB Cloud Data Service will not synchronize the following new changes of the Data App to Postman.

- The creation of new endpoints
- The renaming or deletion of existing endpoints
- The parameter modification of existing endpoints

If you want to have these changes in Postman, you need to [import the latest Data App](/tidb-cloud/data-service-postman-integration.md#step-1-import-your-data-app-to-postman) to Postman again. Because the collection name is unique in a Postman workspace, you can either use the latest Data App to replace the previously imported one or import the latest Data App as a new collection.

After the import, you need to configure the API key for the newly imported App in Postman again.