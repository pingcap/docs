---
title: Connect to TiDB with LibreDB Studio
summary: Learn how to connect to TiDB using LibreDB Studio.
aliases: ['/tidb/stable/dev-guide-gui-libredb-studio/','/tidb/dev/dev-guide-gui-libredb-studio/','/tidbcloud/dev-guide-gui-libredb-studio/']
---

# Connect to TiDB with LibreDB Studio

TiDB is a MySQL-compatible database, and [LibreDB Studio](https://libredb.org) is an open-source, web-based SQL IDE that connects to PostgreSQL, MySQL-compatible databases, and a number of other engines from a single workspace. It ships as a Docker image and as an `npx` package, so it runs next to the database instead of requiring a desktop install.

In this tutorial, you can learn how to connect to TiDB using LibreDB Studio.

> **Note:**
>
> This tutorial covers TiDB Self-Managed only. It was not tested against TiDB Cloud, so it does not include TiDB Cloud connection steps.

## Prerequisites

To complete this tutorial, you need:

- LibreDB Studio, started with `npx @libredb/studio` or the Docker image (see the [Quick Start](https://github.com/libredb/libredb-studio#quick-start) instructions).
- A TiDB Self-Managed cluster.

**If you don't have a TiDB cluster, you can deploy one as follows:**

- [Deploy a local test TiDB Self-Managed cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB Self-Managed cluster](/production-deployment-using-tiup.md).

## Connect to TiDB

1. Open LibreDB Studio in your browser and sign in.

2. Click the **+** button next to the LibreDB Studio logo in the top-left corner. This opens the **New Connection** dialog.

    ![LibreDB Studio: the New Connection dialog](/media/develop/libredb-studio-new-connection.png)

3. Select **MySQL** as the database type. TiDB does not have its own entry in this list because LibreDB Studio talks to it over the same driver it uses for MySQL; once MySQL is selected, a note under the type grid lists the wire-compatible engines that driver has been verified against, including the exact TiDB build LibreDB Studio was tested with.

    ![LibreDB Studio: the MySQL driver's compatibility note lists TiDB](/media/develop/libredb-studio-mysql-compatibility-note.png)

4. Configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name, such as `TiDB`.
    - **Host & Instance**: enter the host and port of your TiDB cluster. The default TiDB port is `4000`.
    - **Username**: enter the username to connect to your TiDB cluster.
    - **Password**: enter the password for that username, if one is set.
    - **Database Name**: enter the name of an existing database on the cluster, such as `test`.

    The following figure shows an example of the connection parameters:

    ![LibreDB Studio: connection settings for a TiDB Self-Managed cluster](/media/develop/libredb-studio-connection-settings.png)

5. Click **Test Connection** to validate the connection to your TiDB cluster.

6. Click **Establish Connection** to save the connection and open it.

7. In the query editor, run a statement to confirm the connection works end to end, for example:

    ```sql
    CREATE TABLE demo_users (id INT PRIMARY KEY, name VARCHAR(50));
    INSERT INTO demo_users VALUES (1, 'Ada'), (2, 'Grace');
    SELECT * FROM demo_users;
    ```

    Click **RUN** (or press **Ctrl+Enter**) to execute it.

    ![LibreDB Studio: connected to TiDB and running a query](/media/develop/libredb-studio-connected-query.png)

> **Note:**
>
> Right after you create a table and insert rows, the row count and size shown next to the table in the sidebar can briefly read `0` until TiDB's background statistics collection catches up. This is TiDB's own behavior, not something LibreDB Studio gets wrong, and the numbers correct themselves shortly afterward with no action needed.

## Next steps

- Learn more usage of LibreDB Studio from its [documentation](https://github.com/libredb/libredb-studio/tree/main/docs).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](https://docs.pingcap.com/developer/), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Submit a support ticket for TiDB Self-Managed](/support.md)
