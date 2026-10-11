---
title: Connect to TiDB with VisuaLeaf
summary: Learn how to connect to TiDB using VisuaLeaf.
aliases: ['/tidb/stable/dev-guide-gui-visualeaf/','/tidb/dev/dev-guide-gui-visualeaf/','/tidbcloud/dev-guide-gui-visualeaf/']
---

# Connect to TiDB with VisuaLeaf

TiDB is a MySQL-compatible database, and [VisuaLeaf](https://visualeaf.com/database/tidb/) is a cross-platform desktop database client for Windows, macOS, and Linux. It provides a SQL editor, a results grid, a visual query builder, ER diagrams, and charts built from query results. VisuaLeaf offers a free Community Edition and paid editions.

In this tutorial, you can learn how to connect to TiDB using VisuaLeaf.

> **Note:**
>
> This tutorial covers TiDB Self-Managed only. It was not tested against TiDB Cloud, so it does not include TiDB Cloud connection steps.
>
> It was also tested against a cluster that does not enforce TLS.

## Prerequisites

To complete this tutorial, you need:

- [VisuaLeaf](https://visualeaf.com/download), installed on Windows, macOS, or Linux.
- A TiDB Self-Managed cluster, and a TiDB user with `CREATE`, `INSERT`, and `SELECT` privileges on the database used in this tutorial.

**If you don't have a TiDB cluster, you can deploy one as follows:**

- [Deploy a local test TiDB Self-Managed cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB Self-Managed cluster](/production-deployment-using-tiup.md).

## Connect to TiDB

1. Launch VisuaLeaf.

2. Click **New Connection**. This opens the **New Connection** dialog.

    ![VisuaLeaf: the New Connection dialog](/media/develop/visualeaf-new-connection.png)

3. In the search box, enter `tidb`, and then select **TiDB**. VisuaLeaf has a dedicated TiDB connection type, listed under **MySQL / MariaDB-compatible**.

    ![VisuaLeaf: searching for TiDB in the New Connection dialog](/media/develop/visualeaf-select-tidb.png)

4. Configure the following connection parameters:

    - **Host**: enter the host of your TiDB cluster.
    - **Port**: enter the port of your TiDB cluster. The default TiDB port is `4000`.
    - **Database**: enter the name of an existing database on the cluster, such as `test`.
    - **Username**: enter the username to connect to your TiDB cluster.
    - **Password**: enter the password for that username, if one is set.

    Optionally, change the connection name in the field at the top of the dialog.

    The following figure shows an example of the connection parameters:

    ![VisuaLeaf: connection settings for a TiDB Self-Managed cluster](/media/develop/visualeaf-connection-settings.png)

5. Click **Test Connection** to validate the connection to your TiDB cluster. If the connection succeeds, a **Connection successful** message is displayed.

6. Click **Save & Connect** to save the connection and open it.

7. In the **Connections** sidebar, expand the new connection to see the databases on the cluster. Right-click the database, and then select **New SQL Editor**.

8. In the SQL editor, run statements to confirm the connection works end to end, for example:

    ```sql
    CREATE TABLE demo_users (id INT PRIMARY KEY, name VARCHAR(50));
    INSERT INTO demo_users VALUES (1, 'Ada'), (2, 'Grace');
    SELECT * FROM demo_users;
    ```

    Click **Run All** (or press **F5**) to execute all statements in the editor. To execute only the current statement, click **Run** (or press **F9**). The results are displayed in the results grid below the editor.

    ![VisuaLeaf: connected to TiDB and running a query](/media/develop/visualeaf-connected-query.png)

## Next steps

- Learn more usage of VisuaLeaf from its [TiDB page](https://visualeaf.com/database/tidb/).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](https://docs.pingcap.com/developer/), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Submit a support ticket for TiDB Self-Managed](/support.md)
