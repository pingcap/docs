---
title: Integrate TiDB Cloud with n8n
summary: Learn the use TiDB Cloud node in n8n.
---

# Integrate TiDB Cloud with n8n

[n8n](https://n8n.io/) is an extendable workflow automation tool. With a [fair-code](https://faircode.io/) distribution model, n8n will always have visible source code, be available to self-host, and allow you to add your custom functions, logic ,and apps. 

This document introduces how to build an auto-workflow, create a TiDB Serverless cluster and write some data into TiDB.

## Prerequisites: Get TiDB Cloud API Key

1. Access your TiDB Cloud dashboard.
2. Click on the **account** tab in the top right.
3. Click **Organization Settings**.
4. Click **API Keys** tab.
5. Click on the **Create API Key** button to create a new API Key.
6. Use these **API Keys** with your TiDB Cloud node credentials in n8n.

For more information, see [TiDB Cloud API Overview](https://docs.pingcap.com/tidbcloud/api-overview/).

## Step 1: Install n8n

There are two ways to install your self-hosting n8n, choose whichever works for you.

- **Install by npm**
  1. Install [node.js](https://nodejs.org/en/download/) on your workspace.
  2. Download and start n8n by `npx`.
     ```shell
     npx n8n
     ```
     
- **Install by docker**
  1. Install [Docker](https://www.docker.com/products/docker-desktop) on your workspace.
  2. Download and start n8n by `docker`
     ```shell
     docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
     ```

After starting n8n, you can visit [localhost:5678](http://localhost:5678) to taste n8n.

## Step 2: Install TiDB Cloud Node in n8n

TiDB Cloud node names `n8n-nodes-tidb-cloud` in npm repository. You need to install this node manually to control TiDB Cloud with n8n.

1. Sign up [self-hosting n8n](http://localhost:5678).
2. Go to **Settings** > **Community Nodes**.
3. Select **Install a community node**.
4. Enter `n8n-nodes-tidb-cloud` in **npm Package Name** field.
5. Click **Install**.

Then you can search **TiDB Cloud** node in the search bar and use it by dragging it to a workspace.

## Step 3: Build Your Workflow

In this step, you will create a new workflow to insert some data to TiDB when you click **Execute** button.

This example usage workflow would use the following nodes.

- [Manual Trigger node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.manualworkflowtrigger/)
- [Set node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.set/)
- [TiDB Cloud node](https://www.npmjs.com/package/n8n-nodes-tidb-cloud)

The final workflow should look like the following image.

![img](/media/tidb-cloud/integration-n8n-workflow.jpg)

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

> Note: The step takes some 1 minute to create a new TiDB Serverless cluster.

### Create an insert operation workflow

#### Use a manual trigger as the workflow's starter

1. If you don't have a workflow. Please navigate to **Workflows** panel, and click **Add workflow**. Otherwise, skip this point.
2. Click **+** in the top right corner and search `manual trigger`.
3. Drag the manual trigger node to your workspace.

#### Create a table used to insert data

1. Click **+** to the right of the manual trigger node.
2. Search `TiDB Cloud` and add it to the workspace.
3. Enter credentials, which is the TiDB Cloud API key, for the TiDB Cloud node.
4. Choose your project from the **Project** list.
5. Select `Execute SQL` from the **Operation** list.
6. Select the cluster. If you have not seen your new cluster, you need to wait a few minutes until the creating cluster mission is completed.
7. Choose a user in the **User** list. You needn't worry about creating users as TiDB always creates a default user for you.
8. Enter `test` in the **Database** field.
9. Enter your database password.
10. Enter the following SQL in the ***SQL*** field:`CREATE TABLE IF NOT EXISTS execute_workflow (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(200), update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)`.

#### Build data to insert

1. Click **+** to the right of the TiDB Cloud node.
2. Click the **Add Value** button and select `String` from the dropdown list.
3. Enter `name` in the **Name** field.
4. Enter a name string in the **Value** field. For example, `n8n-tidb-workflow`.

#### Insert data to TiDB

1. Click **+** to the right of the set node.
2. Search `TiDB Cloud` and add it to the workspace.
3. Select the credentials that you entered in the previous node.
4. Choose your project from the **Project** list.
5. Select `Insert` from the **Operation** list.
6. Enter the value in **Cluster**, **User**, **Database** and **Password** fields.
7. Choose the `execute_workflow` table in the **Table** list.
8. Enter `name` in the **Columns** field.

## Step 4: Run Your Workflow

After building up the workflow, you can click the **Execute Workflow** button to run it. This workflow will help you to create a new TiDB Cloud Serverless Tier cluster and record the execution times of the workflow.

## Support Operations of TiDB Cloud Node

- Create TiDB Serverless clusters
- Execute SQL in TiDB Cloud
- Delete rows in TiDB Cloud
- Insert rows in TiDB Cloud
- Update rows in TiDB Cloud