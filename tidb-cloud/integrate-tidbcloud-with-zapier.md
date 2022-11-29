---
title: Integrate TiDB Cloud with Zapier
summary: Learn how to connect TiDB Cloud to 5000+ Apps with Zapier.
---

# Integrate TiDB Cloud with Zapier

[Zapier](https://zapier.com/app/dashboard) is an automation tool that lets you easily create workflows that involve thousands of apps and services.

Using the [TiDB Cloud app](https://zapier.com/apps/tidb-cloud/integrations) on Zapier enables you to:

- Use TiDB, a MySQl-compatible HTAP database, for free. No need to build locally.
- Make it easier to manage your TiDB Cloud.
- Connect TiDB Cloud to 5000+ apps and automate your workflows.

This guide gives a high-level introduction to the TiDB Cloud app on Zapier and an example of how to use it.

# Quick start with template

In this section, we will use the preset template as an example to try out TiDB Cloud App on Zapier.

## Prerequisites

Before you start, you need:

- A [Zapier account](https://zapier.com/app/login).
- A [GitHub account](https://github.com/login).
- A [TiDB Cloud account](https://tidbcloud.com/signup) and a Serverless Tier cluster on TiDB Cloud, See [TiDB Cloud Quick Start](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster) for more details.

## Step 1: Get the template

Go to [TiDB Cloud App on Zapier](https://zapier.com/apps/tidb-cloud/integrations). Choose a template and click **Try it**. Then you will enter the editor page. 

In this tutorial, we use the **Add new Github global events to TiDB rows** template as an example. In this workflow, every time a new global event is created on GitHub, Zapier adds a new row to your TiDB Cloud cluster.

## Step 2: Set up the trigger

In the editor page, you can see the trigger and action. Click the trigger to set up the trigger.
    
1. Choose app & event

   The template has set the app and the event by default, so you don't need to do anything here. Click **Continue**.

2. Choose account

   Choose a GitHub account that you want to connect with TiDB Cloud. You can either connect a new account or select an existing account. After you set up, click **Continue**.

3. Set up trigger

   The template has set the trigger by default. Click **Continue**.

4. Test trigger

   Click **Test trigger**. It will show the data from GitHub global event if nothing get wrong.

## Step 3: Set up the `Find Table in TiDB Cloud` action

1. Choose app & event

   Keep the default value `Find Table` set by template. Click **Continue** to enter the next step.

2. Choose account

   You will be redirected to a new login page once you click the **Sign in**. Fill in your `Public Key` and `Private Key`. To get API key, follow the [TiDB Cloud API documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management). Click **Continue** after you finish.
    
    ![img.png](/media/tidb-cloud/zapier/tidb_findtable_account.png)

3. Set up action

   In this step, you need to find a table in your TiDB Cloud cluster. And create a new one if it is not exist.

   Choose the project and cluster from drop-down list. Then you will see the connection information of the database.

   ![img.png](/media/tidb-cloud/zapier/tidbcloud_project.png)

   Enter your password and choose the database from drop-down list. 

   ![img.png](/media/tidb-cloud/zapier/tibdcloud_databse.png)

   The template has set the table name and the DDL which will be executed if the table is not exist. You just need to click **Continue** to enter the next step.

   ![img.png](/media/tidb-cloud/zapier/tibdcloud_ddl.png)

4. Test action

   Click **Test action**, and you will create the table in this step. You can also skip the test and create table when this template is running.

## Step 4: Set up the `Create Row in TiDB Cloud` action

1. Choose app & event

   Keep the default value set by template. Click **Continue** to enter the next step.

2. Choose account

   You can select the account you have created before. Click **Continue** to enter the next step.

   ![img.png](/media/tidb-cloud/zapier/tidbcloud_choose_account.png)

3. Set up action

   Fill in the `Project Name`, `Cluster Name`, `TiDB Password`, and `Database Name` just like you did in the previous step. Then choose the **github_global_event** table from drop-down list , and you will find the columns of the table will be shown.

   ![img.png](/media/tidb-cloud/zapier/tidbcloud_columns.png)

   Then click the text area, and you will find that you can choose the data from the trigger. Fill in all the columns with trigger's data. Then click **Continue** to enter the next step.

   ![img.png](/media/tidb-cloud/zapier/tidbcloud_triggers_data.png)

4. Test action

    Click **Test action** to create a new row in the table. If you check the TiDB, you can find the data

   ```
   mysql> select * from test.github_global_event;
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   | id          | type        | actor      | repo_name       | repo_url                                     | public | created_at          |
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   | 25324462424 | CreateEvent | shiyuhang0 | shiyuhang0/docs | https://api.github.com/repos/shiyuhang0/docs | True   | 2022-11-18 08:03:14 |
   +-------------+-------------+------------+-----------------+----------------------------------------------+--------+---------------------+
   1 row in set (0.17 sec)
   ```

## Step 5: Publish your zap

Click **Publish** to publish your zap. Then you can see the zap is running in the [home page](https://zapier.com/app/zaps).

![img.png](/media/tidb-cloud/zapier/tidbcloud_publish.png)

Now, this zap will record all the global events on GitHub into TiDB Cloud automatically.

# Trigger & Action

[Trigger and action](https://zapier.com/how-it-works) are the key concepts in Zapier.

TiDB Cloud App on Zapier provides the following triggers and actions:

Triggers

- New Cluster: Triggers when a new cluster is created.
- New Table: Triggers when a new table is created.
- New Row: Triggers when new rows are created. Only fetch the recently 10000 new rows.
- New Row (Custom Query): Triggers when new rows are returned from a custom query that you provide.

Actions

- Find Cluster: Finds an existing Serverless tier or Dedicated tier.
- Create Cluster: Creates a new cluster. Only support create a free serverless tier now.
- Find Database: Finds an existing Database.
- Create Database: Creates a new database.
- Find Table: Finds an existing Table.
- Create Table: Creates a new table.
- Create Row: Creates a new row.
- Update Row: Updates an existing row.
- Find Row: Finds a row in a table via a lookup column.
- Find Row (Custom Query): Finds a Row in a table via a custom query in your control.

# TiDB Cloud App template

We also provide some templates for you to use directly. Here are some examples, you can find all the templates in the [TiDB Cloud App](https://zapier.com/apps/tidb-cloud/integrations) page.

- [Duplicate new TiDB Cloud rows in Google Sheets](https://zapier.com/apps/google-sheets/integrations/tidb-cloud/1134881/duplicate-new-tidb-cloud-rows-in-google-sheets).
- [Send emails via Gmail from new custom TiDB queries](https://zapier.com/apps/gmail/integrations/tidb-cloud/1134903/send-emails-via-gmail-from-new-custom-tidb-queries).
- [Add rows to TiDB Cloud from newly caught webhooks](https://zapier.com/apps/tidb-cloud/integrations/webhook/1134955/add-rows-to-tidb-cloud-from-newly-caught-webhooks)
- [Store new Salesforce contacts on TiDB rows](https://zapier.com/apps/salesforce/integrations/tidb-cloud/1134923/store-new-salesforce-contacts-on-tidb-rows).
- [Create TiDB rows for new Gmail emails with resumes and send direct Slack notifications](https://zapier.com/apps/gmail/integrations/slack/1135456/create-tidb-rows-for-new-gmail-emails-with-resumes-and-send-direct-slack-notifications)

# FAQ 

## How to set TiDB Cloud account

TiDB Cloud account is not your TiDB Cloud login account. It is your TiDB Cloud API key.

To get your TiDB Cloud API key, follow the [TiDB Cloud API documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).

## How TiDB Cloud triggers de-duplication

Zapier triggers can work with a polling API call to check for new data periodically (depends on Zapier plan).

TiDB Cloud triggers provide the polling API call which will return a lot of results, most of which Zapier has seen before.

Since we don’t want to trigger an action multiple times when an item in your API exists in multiple distinct polls, we will deduplicate the data with the `id` field.

`New Cluster` and `New Table` can simply use the `cluster_id` and `table_id` as `id` field to do the deduplication. You need not do anything for them. Here I will introduce other triggers. 

### New Row Trigger

First, `New Row` trigger limits 10,000 results in every fetch. This will cause the new rows will not be triggered for they may not be included in this 10000 results.

One way to avoid this is to specify `Order By` configuration in the trigger. For example, once you orderby create time, the new rows will always be included in the 10000 results.

Second, `New Row` will use a flexible strategy to generate the `id` filed to do the deduplication. Here are the priority:

1. `id` column if the result contains `id` column.
2. `Dedupe Key` if you specify it in the trigger configuration.
3. primary key if the table has a primary key (use the first column if there are multiple primary keys).
4. unique key if the table has a unique key.
5. the first column of the table.

### New Row (Custom Query) Trigger

`New Row (Custom Query)` trigger limits 1,000,000 results in every fetch. It is a large number, and we only set it to protect the whole system. So, Your query is desired to include order and limit.

As for deduplication, your query results must have a unique id field or you will get the `You must return the results with id field` error.

Note that your custom query must run less than 30 seconds.

## Resources required by TiDB Cloud actions

Most of the TiDB Cloud actions require additional resources you need prepare.

1. Actions need an existing TiDB Cloud serverless tier (TiDB database):

   - Find Database: Finds an existing Database.
   - Create Database: Creates a new database.
   - Find Table: Finds an existing Table.
   - Create Table: Creates a new table.
   - Create Row: Creates a new row.
   - Update Row: Updates an existing row.
   - Find Row: Finds a row in a table via a lookup column.
   - Find Row (Custom Query): Finds a Row in a table via a custom query in your control.

2. Actions need an existing database in TiDB:

   - Find Table: Finds an existing Table.
   - Create Table: Creates a new table.
   - Create Row: Creates a new row.
   - Update Row: Updates an existing row.
   - Find Row: Finds a row in a table via a lookup column.
   - Find Row (Custom Query): Finds a Row in a table via a custom query in your control.

3. Actions need an existing table (including the schema) in TiDB:

   - Create Row: Creates a new row.
   - Update Row: Updates an existing row.
   - Find Row: Finds a row in a table via a lookup column.
   - Find Row (Custom Query): Finds a Row in a table via a custom query in your control.
   
## How to use `find or create` action

`Find or create` action enables you create a resource when it is not exist. Here is an example:

1. Choose `Find Table` action

2. Click `Create TiDB Cloud Table if it doesn’t exist yet?` button to enable `find and create` in `set up action` step

   ![img.png](/media/tidb-cloud/zapier/find-and-create.png)

In this example, we will create a table if it does not exist yet. Note that the table will be created directly if you test your action.