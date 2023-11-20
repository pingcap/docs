---
title: Connect to TiDB with MySQL Workbench
summary: Learn how to connect to TiDB using MySQL Workbench.
---

# Connect to TiDB with MySQL Workbench

TiDB is a MySQL-compatible database, and [MySQL Workbench](https://www.mysql.com/products/workbench/) is a GUI tool set for MySQL database users.

> **Warning:**
>
> MySQL Workbench does not fully support TiDB. MySQL Workbench can connect to TiDB, because of TiDB is a MySQL-compatible database. So the MySQL Workbench will treat TiDB as a MySQL. But some errors might  occur when you are using it. It is recommended that you use other free GUI tools like the ones below, as they supported TiDB officially:
>
> - [DataGrip](/develop/dev-guide-gui-datagrip.md)
> - [DBeaver](/develop/dev-guide-gui-dbeaver.md)
> - [VS Code SQLTools](/develop/dev-guide-gui-vscode-sqltools.md)

In this tutorial, you can learn how to connect to your TiDB cluster using MySQL Workbench.

> **Note:**
>
> This tutorial is compatible with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) **8.0.31** or later versions.
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Connect to TiDB

Connect to your TiDB cluster depending on the TiDB deployment option you have selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`.
    - **Connect With** is set to `General`.
    - **Operating System** matches your environment.

4. Click **Create password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Launch MySQL Workbench and click the **+** in the right side of **MySQL Connections**.

    ![MySQL Workbench: add new connection](/media/develop/navicat-add-new-connection.png)

6. In the setup panel, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Hostname**: enter the `host` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `port` parameter from the TiDB Cloud connection dialog.
    - **Username**: enter the `user` parameter from the TiDB Cloud connection dialog.
    - **Password**: click **Store in Keychain ...**, enter the password of the TiDB Serverless cluster, then click **OK** to store the password.

        ![MySQL Workbench: store password in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    ![MySQL Workbench: configure connection parameters panel for TiDB Dedicated](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7. Click **Test Connection**, if the connection test is successful, you can see the **Successfully made the MySQL connection** message. Click **OK** to save the connection configuration.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere**.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Launch MySQL Workbench and click the **+** in the right side of **MySQL Connections**.

    ![MySQL Workbench: add new connection](/media/develop/navicat-add-new-connection.png)

5. In the setup panel, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Hostname**: enter the `host` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `port` parameter from the TiDB Cloud connection dialog.
    - **Username**: enter the `user` parameter from the TiDB Cloud connection dialog.
    - **Password**: click **Store in Keychain ...**, enter the password of the TiDB Dedicated cluster, then click **OK** to store the password.

        ![MySQL Workbench: store Dedicated Tier password in keychain](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    ![MySQL Workbench: configure connection parameters panel for TiDB Dedicated](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6. Click **Test Connection**, if the connection test is successful, you can see the **Successfully made the MySQL connection** message. Click **OK** to save the connection configuration.

</div>
<div label="TiDB Self-Hosted">

1. Launch MySQL Workbench and click the **+** in the right side of **MySQL Connections**.

    ![MySQL Workbench: add new connection](/media/develop/navicat-add-new-connection.png)

2. In the setup panel, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Hostname**: enter the IP address or domain name of your TiDB Self-Hosted cluster.
    - **Port**: enter the port number of your TiDB Self-Hosted cluster.
    - **Username**: enter the username to use to connect to your TiDB.
    - **Password**: click **Store in Keychain ...**, enter the password to use to connect to your TiDB, then click **OK** to store the password.

        ![MySQL Workbench: store self-hosted password in keychain](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    ![MySQL Workbench: configure connection parameters panel for self-hosted TiDB](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3. **Test Connection** to validate the connection to the self-hosted TiDB.

4. If the connection test is successful, you can see the **Connection Successful** message. Click **Save** to save the connection configuration.

</div>
</SimpleTab>

## Next steps

- Learn more usage of MySQL Workbench from [the documentation of MySQL Workbench](https://dev.mysql.com/doc/workbench/en/).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap) or [create a support ticket](https://support.pingcap.com/).
