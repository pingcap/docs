---
title: Connect to TiDB with MySQL Workbench
summary: Learn how to connect to TiDB using MySQL Workbench.
---

# Connect to TiDB with MySQL Workbench

TiDB is a MySQL-compatible database, and [MySQL Workbench](https://www.mysql.com/products/workbench/) is a GUI tool set for MySQL database users.

> **Warning:**
>
> - Although you can use MySQL Workbench to connect to TiDB due to its MySQL compatibility, MySQL Workbench does not fully support TiDB. You might encounter some issues during usage as it treats TiDB as MySQL.
> - It is recommended to use other GUI tools that officially support TiDB, such as [DataGrip](/develop/dev-guide-gui-datagrip.md), [DBeaver](/develop/dev-guide-gui-dbeaver.md), and [VS Code SQLTools](/develop/dev-guide-gui-vscode-sqltools.md). For a complete list of GUI tools that fully supported by TiDB, see [Third-party tools supported by TiDB](/develop/dev-guide-third-party-support.md#gui).

In this tutorial, you can learn how to connect to your TiDB cluster using MySQL Workbench.

> **Note:**
>
> This tutorial is compatible with TiDB Cloud Serverless, TiDB Cloud Dedicated, and TiDB Self-Managed.

## Prerequisites

To complete this tutorial, you need:

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) **8.0.31** or later versions.
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Cloud Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Connect to TiDB

Connect to your TiDB cluster depending on the TiDB deployment option you have selected.

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Connection Type** is set to `Public`.
    - **Branch** is set to `main`.
    - **Connect With** is set to `MySQL Workbench`.
    - **Operating System** matches your environment.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.

5. Launch MySQL Workbench and click **+** near the **MySQL Connections** title.

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

6. In the **Setup New Connection** dialog, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Hostname**: enter the `HOST` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `PORT` parameter from the TiDB Cloud connection dialog.
    - **Username**: enter the `USERNAME` parameter from the TiDB Cloud connection dialog.
    - **Password**: click **Store in Keychain ...** or **Store in Vault**, enter the password of the TiDB Cloud Serverless cluster, and then click **OK** to store the password.

        ![MySQL Workbench: store the password of TiDB Cloud Serverless in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    The following figure shows an example of the connection parameters:

    ![MySQL Workbench: configure connection settings for TiDB Cloud Serverless](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7. Click **Test Connection** to validate the connection to the TiDB Cloud Serverless cluster.

8. If the connection test is successful, you can see the **Successfully made the MySQL connection** message. Click **OK** to save the connection configuration.

</div>
<div label="TiDB Cloud Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the connection dialog, select **Public** from the **Connection Type** drop-down list, and then click **CA cert** to download the CA certificate.

    If you have not configured the IP access list, click **Configure IP Access List** or follow the steps in [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) to configure it before your first connection.

    In addition to the **Public** connection type, TiDB Cloud Dedicated supports **Private Endpoint** and **VPC Peering** connection types. For more information, see [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster).

4. Launch MySQL Workbench and click **+** near the **MySQL Connections** title.

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

5. In the **Setup New Connection** dialog, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Hostname**: enter the `HOST` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `PORT` parameter from the TiDB Cloud connection dialog.
    - **Username**: enter the `USERNAME` parameter from the TiDB Cloud connection dialog.
    - **Password**: click **Store in Keychain ...**, enter the password of the TiDB Cloud Dedicated cluster, and then click **OK** to store the password.

        ![MySQL Workbench: store the password of TiDB Cloud Dedicated in keychain](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    The following figure shows an example of the connection parameters:

    ![MySQL Workbench: configure connection settings for TiDB Cloud Dedicated](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6. Click **Test Connection** to validate the connection to the TiDB Cloud Dedicated cluster.

7. If the connection test is successful, you can see the **Successfully made the MySQL connection** message. Click **OK** to save the connection configuration.

</div>
<div label="TiDB Self-Managed">

1. Launch MySQL Workbench and click **+** near the **MySQL Connections** title.

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

2. In the **Setup New Connection** dialog, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Hostname**: enter the IP address or domain name of your TiDB Self-Managed cluster.
    - **Port**: enter the port number of your TiDB Self-Managed cluster.
    - **Username**: enter the username to use to connect to your TiDB.
    - **Password**: click **Store in Keychain ...**, enter the password to use to connect to your TiDB cluster, and then click **OK** to store the password.

        ![MySQL Workbench: store the password of TiDB Self-Managed in keychain](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    The following figure shows an example of the connection parameters:

    ![MySQL Workbench: configure connection settings for TiDB Self-Managed](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3. Click **Test Connection** to validate the connection to the TiDB Self-Managed cluster.

4. If the connection test is successful, you can see the **Successfully made the MySQL connection** message. Click **OK** to save the connection configuration.

</div>
</SimpleTab>

## FAQs

### How to handle the connection timeout error "Error Code: 2013. Lost connection to MySQL server during query"?

This error indicates that the query execution time exceeds the timeout limit. To resolve this issue, you can adjust the timeout settings by the following steps:

1. Launch MySQL Workbench and navigate to the **Workbench Preferences** page.
2. In the **SQL Editor** > **MySQL Session** section, configure the **DBMS connection read timeout interval (in seconds)** option. This sets the maximum amount of time (in seconds) that a query can take before MySQL Workbench disconnects from the server.

    ![MySQL Workbench: adjust timeout option in SQL Editor settings](/media/develop/mysql-workbench-adjust-sqleditor-read-timeout.jpg)

For more information, see [MySQL Workbench frequently asked questions](https://dev.mysql.com/doc/workbench/en/workbench-faq.html).

## Next steps

- Learn more usage of MySQL Workbench from [the documentation of MySQL Workbench](https://dev.mysql.com/doc/workbench/en/).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](https://tidb.support.pingcap.com/).

</CustomContent>
