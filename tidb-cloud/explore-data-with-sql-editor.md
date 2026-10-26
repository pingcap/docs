---
title: Explore Your Data with SQL Editor
summary: Learn how to use SQL Editor in the TiDB Cloud console to write and run SQL queries, manage SQL files, and view query results.
aliases: ['/tidbcloud/explore-data-with-chat2query', '/tidbcloud/use-chat2query-api', '/tidbcloud/use-chat2query-knowledge', '/tidbcloud/use-chat2query-sessions']
---

# Explore Your Data with SQL Editor

You can use the built-in SQL Editor in the [TiDB Cloud console](https://tidbcloud.com/) to maximize your data value.

In SQL Editor, you can write and run SQL queries against databases without a local SQL client. You can intuitively view the query results in tables or charts and easily check the query logs.

## Use cases

The recommended use cases of SQL Editor are as follows:

- Quickly test the MySQL compatibility of TiDB.
- Easily explore the SQL features in TiDB using your own datasets.

## Limitations

- SQL Editor is available only for [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) instances hosted on AWS. To use SQL Editor on [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters, contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md).

## Access SQL Editor

1. Go to the [**My TiDB**](https://tidbcloud.com/tidbs) page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click the name of your {{{ .starter }}} instance or TiDB Cloud Dedicated cluster, and then click **SQL Editor** in the left navigation pane.

    > **Note:**
    >
    > In the following cases, the **SQL Editor** entry is displayed in gray and not clickable.
    >
    > - Your TiDB Cloud Dedicated cluster is earlier than v6.5.0. To use SQL Editor, you need to contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md) to upgrade your clusters.
    > - Your TiDB Cloud Dedicated cluster is just created and the running environment for SQL Editor is still in preparation. In this case, wait for a few minutes and SQL Editor will be available.
    > - Your TiDB Cloud Dedicated cluster is [paused](/tidb-cloud/pause-or-resume-tidb-cluster.md).

## Write and run SQL queries

In SQL Editor, you can write and run SQL queries using your own dataset.

1. Write SQL queries.

2. Run SQL queries.

    <SimpleTab>
    <div label="macOS">

    For macOS:

    - If you have only one query in the editor, to run it, press **⌘ + Enter** or click <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run**.

    - If you have multiple queries in the editor, to run one or several of them sequentially, select the lines of the target queries with your cursor, and then press **⌘ + Enter** or click **Run**.

    - To run all queries in the editor sequentially, press **⇧ + ⌘ + Enter**, or select the lines of all queries with your cursor and click **Run**.

    </div>

    <div label="Windows/Linux">

    For Windows or Linux:

    - If you have only one query in the editor, to run it, press **Ctrl + Enter** or click <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run**.

    - If you have multiple queries in the editor, to run one or several of them sequentially, select the lines of the target queries with your cursor, and then press **Ctrl + Enter** or click **Run**.

    - To run all queries in the editor sequentially, press **Shift + Ctrl + Enter**, or select the lines of all queries with your cursor and click **Run**.

    </div>
    </SimpleTab>

After running the queries, you can see the query logs and results immediately at the bottom of the page.

> **Note:**
>
> The returned result has a size limit of 8 MiB.

## Manage SQL files

In SQL Editor, you can save your SQL queries in different SQL files and manage SQL files as follows:

- To add a SQL file, click **+** on the **SQL Files** tab.
- To rename a SQL file, move your cursor on the filename, click **...** next to the filename, and then select **Rename**.
- To delete a SQL file, move your cursor on the filename, click **...** next to the filename, and then select **Delete**. Note that when there is only one SQL file on the **SQL Files** tab, you cannot delete it.

## Manage SQL Editor settings

In SQL Editor, you can change the following settings:

- The maximum number of rows in query results
- Whether to show system database schemas on the **Schemas** tab

To change the settings, take the following steps:

1. In the upper-right corner of **SQL Editor**, click **...** and select **Settings**.
2. Change the settings according to your need.
3. Click **Save**.
