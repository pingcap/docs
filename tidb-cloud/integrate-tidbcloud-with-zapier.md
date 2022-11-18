---
title: Integrate TiDB Cloud with Zapier
summary: Learn how to connect TiDB Cloud to 5000+ Apps with zapier.
---


- [Integrate TiDB Cloud with zapier](#integrate-tidb-cloud-with-zapier)
- [Before your start](#before-your-start)
- [Quick start with our template](#quick-start-with-our-template)
- [Trigger & Action](#trigger---action)
- [How to set TiDB Cloud account](#how-to-set-tidb-cloud-account)
- [How TiDB Cloud triggers de-duplication](#how-tidb-cloud-triggers-de-duplication)
    + [New Row Trigger](#new-row-trigger)
    + [New Row (Custom Query) Trigger](#new-row--custom-query--trigger)

# Integrate TiDB Cloud with zapier

[Zapier](https://zapier.com/app/dashboard) is an automation tool that lets you easily create workflows that involve common apps and services.

Use TiDB Cloud App on zapier enable you connect TiDB Cloud to 5000+ Apps.

This guide describes how to use TiDB Cloud App on zapier.

# Before you start

Make sure you have met the following requires

1. A TiDB Cloud account
2. A zapier account

# Quick start with our template

1. Go to [TiDB Cloud App on zapier](https://zapier.com/apps/tidb-cloud/integrations)

2. Choose a template you want to use. Here we use 

# Trigger & Action

[Trigger and action](https://help.zapier.com/hc/en-us/articles/8496181725453-Learn-key-concepts-in-Zapier) are the key concepts in zapier.

TiDB Cloud App on zapier provides the following triggers and actions

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

# How to set TiDB Cloud account

TiDB Cloud account is not your TiDB Cloud login account. It is your TiDB Cloud API key.

To get your TiDB Cloud API key, follow the [TiDB Cloud API documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).


# How TiDB Cloud triggers de-duplication

Zapier triggers can work with a polling API call to check for new data periodically (depends on zapier plan).

TiDB Cloud triggers provide the polling API call which will return many results, most of which Zapier has seen before.

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




