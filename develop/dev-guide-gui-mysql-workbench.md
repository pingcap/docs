---
title: Connect to TiDB with MySQL Workbench
summary: Learn how to connect to TiDB using MySQL Workbench.
aliases: ['/tidb/stable/dev-guide-gui-mysql-workbench/','/tidb/dev/dev-guide-gui-mysql-workbench/','/tidbcloud/dev-guide-gui-mysql-workbench/']
---

# Connect to TiDB with MySQL Workbench

TiDB is a MySQL-compatible database, and [MySQL Workbench](https://www.mysql.com/products/workbench/) is a GUI tool set for MySQL database users.

> **Warning:**
>
> - Although you can use MySQL Workbench to connect to TiDB due to its MySQL compatibility, MySQL Workbench does not fully support TiDB. You might encounter some issues during usage as it treats TiDB as MySQL.
> - It is recommended to use other GUI tools that officially support TiDB, such as [DataGrip](/develop/dev-guide-gui-datagrip.md), [DBeaver](/develop/dev-guide-gui-dbeaver.md), and [VS Code SQLTools](/develop/dev-guide-gui-vscode-sqltools.md). For a complete list of GUI tools that fully supported by TiDB, see [Third-party tools supported by TiDB](/develop/dev-guide-third-party-support.md#gui).

In this tutorial, you can learn how to connect to TiDB using MySQL Workbench.

> **Note:**
>
> This tutorial is compatible with {{{ .starter }}}, {{{ .essential }}}, {{{ .premium }}}, TiDB Cloud Dedicated, and TiDB Self-Managed.

## Prerequisites

To complete this tutorial, you need:

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) **8.0.31** or later versions.
- A TiDB cluster.

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) [Create a {{{ .starter }}} instance](/develop/dev-guide-build-cluster-in-cloud.md).
- [Deploy a local test TiDB Self-Managed cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB Self-Managed cluster](/production-deployment-using-tiup.md).

## Connect to TiDB

Connect to TiDB depending on the TiDB deployment option you have selected.

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .starter }}} or Essential instance to go to its overview page.

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
    - **Password**: click **Store in Keychain ...** or **Store in Vault**, enter the password you created in step 4, and then click **OK** to store the password.

        ![MySQL Workbench: store the password of {{{ .starter }}} in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    The following figure shows an example of the connection parameters:

    ![MySQL Workbench: configure connection settings for {{{ .starter }}}](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7. Click **Test Connection** to validate the connection to your target {{{ .starter }}} or Essential instance.

8. If the connection test is successful, you can see the **Successfully made the MySQL connection** message. Click **OK** to save the connection configuration.

</div>
<div label="{{{ .premium }}}">

1. Navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page, and then click the name of your target instance to go to its overview page.

2. In the left navigation pane, click **Settings** > **Networking**.

3. On the **Networking** page, click **Enable** for **Public Endpoint**, and then click **Add IP Address**.

    Ensure that your client IP address is added to the access list.

4. In the left navigation pane, click **Overview** to return to the instance overview page.

5. Click **Connect** in the upper-right corner. A connection dialog is displayed.

6. In the connection dialog, select **Public** from the **Connection Type** drop-down list.

    - If a message indicates that the public endpoint is still being enabled, wait until the process completes.
    - If you have not set a password yet, click **Set Root Password** in the dialog.
    - If you need to verify the server certificate or if the connection fails and requires a CA certificate, click **CA cert** to download it.
    - In addition to the **Public** connection type, {{{ .premium }}} supports **Private Endpoint** connections. For more information, see [Connect to {{{ .premium }}} via AWS PrivateLink](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md).

7. Launch MySQL Workbench and click **+** near the **MySQL Connections** title.

8. In the **Setup New Connection** dialog, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Hostname**: enter the `HOST` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `PORT` parameter from the TiDB Cloud connection dialog.
    - **Username**: enter the `USERNAME` parameter from the TiDB Cloud connection dialog.
    - **Password**: click **Store in Keychain ...** or **Store in Vault**, enter the password of the {{{ .premium }}} instance, and then click **OK** to store the password.

9. Click **Test Connection** to validate the connection to the {{{ .premium }}} instance.

10. If the connection test is successful, you can see the **Successfully made the MySQL connection** message. Click **OK** to save the connection configuration.

</div>
<div label="TiDB Cloud Dedicated">

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target TiDB Cloud Dedicated cluster to go to its overview page.

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
<div label="TiDB Self-Managed" value="tidb">

1. Launch MySQL Workbench and click **+** near the **MySQL Connections** title.

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

2. In the **Setup New Connection** dialog, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Hostname**: enter the IP address or domain name of your TiDB Self-Managed cluster.
    - **Port**: enter the port number of your TiDB Self-Managed cluster.
    - **Username**: enter the username to use to connect to your TiDB.
    - **Password**: click **Store in Keychain ...**, enter the password to use to connect to your TiDB Self-Managed cluster, and then click **OK** to store the password.

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
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](https://docs.pingcap.com/developer/), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Submit a support ticket for TiDB Self-Managed](/support.md)
