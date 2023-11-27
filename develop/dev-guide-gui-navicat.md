---
title: Connect to TiDB with Navicat
summary: Learn how to connect to TiDB using Navicat.
---

# Connect to TiDB with Navicat

TiDB is a MySQL-compatible database, and [Navicat](https://www.navicat.com) is a GUI tool set for database users. This tutorial uses the [Navicat for MySQL](https://www.navicat.com/en/products/navicat-for-mysql) tool to connect to TiDB.

> **Warning:**
>
> Navicat doesn't fully support TiDB. Navicat can connect to TiDB, because of TiDB being a MySQL-compatible database. So Navicat will treat TiDB as a MySQL. But there some errors might occur when you are using it. It's a known issue about [Navicat user management compatibility](https://github.com/pingcap/tidb/issues/45154). If you want to know more compatibility issues between Navicat and TiDB, you can use [GitHub issue page](https://github.com/pingcap/tidb/issues?q=is%3Aissue+navicat+is%3Aopen) of TiDB to track it.
>
> It is recommended to use some other free GUI tools that supported TiDB officially:
>
> - [DataGrip](/develop/dev-guide-gui-datagrip.md)
> - [DBeaver](/develop/dev-guide-gui-dbeaver.md)
> - [VS Code SQLTools](/develop/dev-guide-gui-vscode-sqltools.md)

In this tutorial, you can learn how to connect to your TiDB cluster using Navicat.

> **Note:**
>
> This tutorial is compatible with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- [Navicat for MySQL](https://www.navicat.com/en/download/navicat-for-mysql) **16.3.2** or later versions.
- A Navicat for MySQL paid account.
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

5. Launch Navicat and click the **Connection** in the upper-left corner. In the selection panel, click **MySQL**  as the database type.

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

6. In the setting panel, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Host**: enter the `host` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `port` parameter from the TiDB Cloud connection dialog.
    - **Username**: enter the `user` parameter from the TiDB Cloud connection dialog.
    - **Password**: enter the password of the TiDB Serverless cluster.

    ![Navicat: configure connection general panel for TiDB Serverless](/media/develop/navicat-connection-config-serverless-general.png)

7. Click the **SSL** tab, check **Use SSL**, **Use authentication**, **Verify server certificate against CA**, and enter the `ssl_ca` parameter from the TiDB Cloud connection dialog into the **CA Certificate** input box. **Test Connection** to validate the connection to the TiDB Serverless cluster.

    ![Navicat: configure connection SSL panel for TiDB Serverless](/media/develop/navicat-connection-config-serverless-ssl.png)

8. If the connection test is successful, you can see the **Connection Successful** message. Click **Save** to save the connection configuration.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere**.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).
4. Click **Download CA cert** to download it locally, and save location signed as `<ca_cert>`.

5. Launch Navicat and click the **Connection** in the upper-left corner. In the dropdown menu, click **MySQL** as the database type.

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

6. In the setting panel, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Host**: enter the `host` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `port` parameter from the TiDB Cloud connection dialog.
    - **Username**: enter the `user` parameter from the TiDB Cloud connection dialog.
    - **Password**: enter the password of the TiDB Dedicated cluster.

    ![Navicat: configure connection general panel for TiDB Dedicated](/media/develop/navicat-connection-config-dedicated-general.png)

7. Click the **SSL** tab, check **Use SSL**, **Use authentication** and **Verify server certificate against CA**. Then enter the `<ca_cert>` which you downloaded from TiDB Cloud to **CA Certificate**.

    ![Navicat: configure connection SSL panel for TiDB Dedicated](/media/develop/navicat-connection-config-dedicated-ssl.jpg)

8. **Test Connection** to validate the connection to the TiDB Dedicated cluster.

9. If the connection test is successful, you can see the **Connection Successful** message. Click **Save** to save the connection configuration.

</div>
<div label="TiDB Self-Hosted">

1. Launch Navicat and click the **Connection** in the upper-left corner. In the selection panel, click **MySQL**  as the database type.

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

2. In the setting pane, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Host**: enter the IP address or domain name of your TiDB Self-Hosted cluster.
    - **Port**: enter the port number of your TiDB Self-Hosted cluster.
    - **Username**: enter the username to use to connect to your TiDB.
    - **Password**: enter the password to use to connect to your TiDB.

    ![Navicat: configure connection general panel for self-hosted TiDB](/media/develop/navicat-connection-config-self-hosted-general.png)

3. Click **Test Connection** to validate the connection to the self-hosted TiDB.

4. If the connection test is successful, you can see the **Connection Successful** message. Click **Save** to finish the connection configuration.

</div>
</SimpleTab>

## Next steps

- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](/support.md).
