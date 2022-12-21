---
title: Integrate TiDB Cloud with n8n
summary: Learn the use of TiDB Cloud node in n8n.
---

# Integrate TiDB Cloud with n8n

[n8n](https://n8n.io/) is an extendable workflow automation tool. With a [fair-code](https://faircode.io/) distribution model, n8n will always have visible source code, be available to self-host, and allow you to add your custom functions, logic, and apps. 

This document introduces how to build an auto-workflow: create a TiDB Cloud Serverless Tier cluster, gather Hacker News RSS, store it to TiDB and send a briefing email.

## Prerequisites: Get TiDB Cloud API Key

1. Access your TiDB Cloud dashboard.
2. Click <MDSvgIcon name="icon-top-organization" /> **Organization** >  **Organization Settings** in the upper-right corner.
3. Click the **API Keys** tab.
4. Click the **Create API Key** button to create a new API Key.
5. Save the created API key for later use in n8n.

For more information, see [TiDB Cloud API Overview](/tidb-cloud/api-overview.md).

## Step 1: Install n8n

There are two ways to install your self-hosting n8n, choose whichever works for you.

<SimpleTab>
<div label="npm">

1. Install [node.js](https://nodejs.org/en/download/) on your workspace.
2. Download and start n8n by `npx`.

    ```shell
    npx n8n
    ```

</div>
<div label="Docker">

1. Install [Docker](https://www.docker.com/products/docker-desktop) on your workspace.
2. Download and start n8n by `docker`

    ```shell
    docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
    ```

</div>
</SimpleTab>

After starting n8n, you can visit [localhost:5678](http://localhost:5678) to taste n8n.

## Step 2: Install TiDB Cloud Node in n8n

TiDB Cloud node is named `n8n-nodes-tidb-cloud` in the npm repository. You need to install this node manually to control TiDB Cloud with n8n.

1. In the [localhost:5678](http://localhost:5678) page, create an owner account for self-hosting n8n.
2. Go to **Settings** > **Community nodes**.
3. Click **Install a community node**.
4. Enter `n8n-nodes-tidb-cloud` in **npm Package Name** field.
5. Click **Install**.

Then you can search **TiDB Cloud** node in the search bar and use it by dragging it to a workspace.

## Step 3: Build Your Workflow

In this step, you will create a new workflow to insert some data to TiDB when you click **Execute** button.

This example usage workflow would use the following nodes.

- [Schedule Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
- [RSS Read](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.rssfeedread/)
- [Code](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
- [Gmail](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
- [TiDB Cloud node](https://www.npmjs.com/package/n8n-nodes-tidb-cloud)

The final workflow should look like the following image.

![img](/media/tidb-cloud/integration-n8n-workflow-rss.jpg)

### (Optional) Create a TiDB Cloud Serverless Tier cluster

If you haven't got a TiDB Cloud Serverless Tier cluster, you can use this node to create one. Otherwise, feel free to skip this operation.

1. Navigate to **Workflows** panel, and click **Add workflow**.
2. In new workflow workspace, click **+** in the top right corner and choose **All** field.
3. Search `TiDB Cloud` and drag it to the workspace.
4. Enter credentials, which is the TiDB Cloud API key, for the TiDB Cloud node.
5. Choose your project from the **Project** list.
6. Select `Create Serverless Cluster` from the **Operation** list.
7. Enter a cluster name in the **Cluster Name** field.
8. Select a region from the **Region** list.
9. Enter a password used to log in to your TiDB clusters in the **Password** field.
10. Click on **Execute Node** to run the node.

> **Note:** 
> 
> This step takes seconds to create a new TiDB Serverless cluster.

### Create a workflow

#### Use a manual trigger as the workflow's starter

1. If you don't have a workflow yet, navigate to the **Workflows** panel, and click **Start from scratch**. Otherwise, skip this step.
2. Click **+** in the top right corner and search `schedule trigger`.
3. Drag the manual trigger node to your workspace, and double-click on the node. The **Parameters** dialog is displayed.
4. Configure the rule as follows:
    - **Trigger Interval**: `Days`
    - **Days Between Triggers**: `1`
    - **Trigger at Hour**: `8am`
    - **Trigger at Minute**:`0`

This trigger will execute your workflow every morning at 8 AM. 

#### Create a table used to insert data

1. Click **+** to the right of the manual trigger node.
2. Search `TiDB Cloud` and add it to the workspace.
3. In the **Parameters** dialog, enter the credential for the TiDB Cloud node. The credential is your TiDB Cloud API key.
4. Choose your project from the **Project** list.
5. Select `Execute SQL` from the **Operation** list.
6. Select the cluster. If you have not seen your new cluster in the list, you need to wait a few minutes until the cluster creation is completed.
7. Choose a user in the **User** list. TiDB Cloud always creates a default user, so you don't have to manually create one.
8. Enter `test` in the **Database** field.
9. Enter your database password.
10. Enter the following SQL in the ***SQL*** field:

    ```sql
    CREATE TABLE IF NOT EXISTS hacker_news_briefing (creator VARCHAR (200), title TEXT,  link VARCHAR(200), pubdate VARCHAR(200), comments VARCHAR(200), content TEXT, guid VARCHAR (200), isodate VARCHAR(200));
    ```

11. Click on **Execute node** to create the table.

#### Get the Hacker News RSS

1. Click **+** to the right of the TiDB Cloud node.
2. Search `rss feed read` and add it to the workspace.
3. Enter `https://hnrss.org/frontpage` to the **URL**.

#### Insert data to TiDB

1. Click **+** to the right of the RSS Feed Read node.
2. Search `TiDB Cloud` and add it to the workspace.
3. Select the credentials that you entered in the previous node.
4. Choose your project from the **Project** list.
5. Select `Insert` from the **Operation** list.
6. Enter the value in **Cluster**, **User**, **Database** and **Password** fields.
7. Enter the `hacker_news_briefing` table in the **Table** field.
8. Enter `creator, title, link, pubdate, comments, content, guid, isodate` in the **Columns** field.

#### Build message

1. Click **+** to the right of the RSS Feed Read node.
2. Search `code` and add it to the workspace.
3. Choose `Run Once for All Items` mode.
4. Copy the following code to the **JavaScript** field.

```javascript
let message = "";

// Loop the input items
for (item of items) {
  message += `
       <h3>${item.json.title}</h3>
       <br>
       ${item.json.content}
       <br>
       `
}

let response =
    `
       <!DOCTYPE html> 
       <html> 
       <head> 
       <title>Hacker News Briefing</title> 
    </head> 
    <body>  
        ${message} 
    </body> 
    </html>
    `
// Return our message
return [{json: {response}}];
```

#### Send message by Gmail

1. Click **+** to the right of the code node.
2. Search `gmail` and add it to the workspace.
3. Enter the credential for the Gmail node. For detailed instructions, refer to [n8n documentation](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/).
4. Choose `Message` in the **Resource**. 
5. Choose `Send` in the **Operation**.
6. Enter your email in the **To**.
7. Enter `Hacker News Briefing` in the **Subject**.
8. Choose `HTML` in the **Email Type**.
9. In the **Message** field mode, click `Expression` and enter `{{ $json["response"] }}`.

> **Note:** 
> 
> It is very important to mouse hover the Message field and select the Expression pattern.

## Step 4: Run Your Workflow

After building up the workflow, you can click the **Execute Workflow** button to test run it. 

If the workflow runs as expected, you'll get Hacker News briefing emails. These news contents will be logged to your TiDB Cloud Serverless Tier cluster so you don't have to worry about losing them.

Now you can activate this workflow in the **Workflows** panel. This workflow will help you get the front-page articles on Hacker News every day.

## TiDB Cloud Node Core

### Support Operation

TiDB Cloud Node acts as a [regular node](https://docs.n8n.io/workflows/nodes/#regular-nodes), and only supports the following five operations.

- **Create Serverless Cluster**: Create a TiDB Cloud Serverless Tier cluster.
- **Execute SQL**: Execute an SQL statement in TiDB.
- **Delete**：Delete rows in TiDB.
- **Insert**: Insert rows in TiDB.
- **Update**: Update rows in TiDB.

### Fields Description

Different operations require different fields to be filled in. The following shows the respective field descriptions according to the operation.

<SimpleTab>
<div label="Create Serverless Cluster">

- **Credential for TiDB Cloud API**: Only supports TiDB Cloud API key authentication. Refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: The TiDB Cloud project name. 
- **Operation**: The operation of this node. Refer to [Support Operation](#support-operation).
- **Cluster**: The TiDB Cloud cluster name. Enter one name for your new cluster.
- **Region**: The region name. Choose a region where your cluster will be deployed. Usually, choose the region closest to your application deployment.
- **Password**: The root password. Set a password for your new cluster.

</div>
<div label="Execute SQL">

- **Credential for TiDB Cloud API**: Only supports TiDB Cloud API key authentication. Refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: The TiDB Cloud project name.
- **Operation**: The operation of this node. Refer to [Support Operation](#support-operation).
- **Cluster**: The TiDB Cloud cluster name.
- **Password**: The password of TiDB Cloud cluster.
- **User**: The username of your TiDB Cloud cluster.
- **Database**: The database name.
- **SQL**: The SQL statement to execute.

</div>
<div label="Delete">

- **Credential for TiDB Cloud API**: Only supports TiDB Cloud API key authentication. Refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: The TiDB Cloud project name.
- **Operation**: The operation of this node. Refer to [Support Operation](#support-operation).
- **Cluster**: The TiDB Cloud cluster name. In the Create Serverless Cluster operation, you need to enter one name for your new cluster . While in other operations, you should choose one existing cluster.
- **Password**: The password of TiDB Cloud cluster.
- **User**: The username of your TiDB Cloud cluster.
- **Database**: The database name.
- **Table**: The table name. You can use `From list` mode to choose one or `Name` mode to type table name manually.
- **Delete Key**: The Name of the item's property which decides which rows in the database should be deleted. Item is the data sent from one node to another. A node performs its action on each item of incoming data. For more information about item in n8n, see [n8n documentation](https://docs.n8n.io/workflows/items/).

</div>
<div label="Insert">

- **Credential for TiDB Cloud API**: Only supports TiDB Cloud API key authentication. Refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: The TiDB Cloud project name.
- **Operation**: The operation of this node. Refer to [Support Operation](#support-operation).
- **Cluster**: The TiDB Cloud cluster name. In the Create Serverless Cluster operation, you need to enter one name for your new cluster . While in other operations, you should choose one existing cluster.
- **Password**: The password of TiDB Cloud cluster.
- **User**: The username of your TiDB Cloud cluster.
- **Database**: The database name.
- **Table**: The table name. You can use `From list` mode to choose one or `Name` mode to type table name manually.
- **Columns**: The comma-separated list of the input item's property which should used as columns for the new rows. Item is the data sent from one node to another. A node performs its action on each item of incoming data. For more information about item in n8n, see [n8n documentation](https://docs.n8n.io/workflows/items/).

</div>
<div label="Update">

- **Credential for TiDB Cloud API**: Only supports TiDB Cloud API key authentication. Refer to [Get TiDB Cloud API Key](#prerequisites-get-tidb-cloud-api-key).
- **Project**: The TiDB Cloud project name.
- **Operation**: The operation of this node. Refer to [Support Operation](#support-operation).
- **Cluster**: The TiDB Cloud cluster name. In the Create Serverless Cluster operation, you need to enter one name for your new cluster. While in other operations, you should choose one existing cluster.
- **Password**: The password of TiDB Cloud cluster.
- **User**: The username of your TiDB Cloud cluster.
- **Database**: The database name.
- **Table**: The table name. You can use `From list` mode to choose one or `Name` mode to type table manually.
- **Update Key**: The name of the item's property which decides which rows in the database should be updated. Item is the data sent from one node to another. A node performs its action on each item of incoming data. For more information about item in n8n, see [n8n documentation](https://docs.n8n.io/workflows/items/).
- **Columns**: The comma-separated list of the input item which should used as columns for the rows to update.

</div>
</SimpleTab>

### Limitations 
 
1. Normally only one SQL statement is allowed in the **Execute SQL** operation. If you want to execute more than one statement in a single operation, you need to manually enable [`tidb_multi_statement_mode`](https://docs.pingcap.com/tidb/dev/system-variables#tidb_multi_statement_mode-new-in-v4011).
2. The **Delete** and **Update** operation need to specify one field as a key. For example, the `Delete Key` is set to `id`, which is equivalent to executing `delete from table where id = ${item.id}`. Currently, it only supports specifying one key.
3. The **Insert** and **Update** operation need to specify the comma-separated list in the **Columns** field, and the field name must be the same as the input item's property.
