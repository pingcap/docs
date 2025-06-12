---
title: Connect to TiDB with Navicat
summary: Learn how to connect to TiDB using Navicat.
---

# Connect to TiDB with Navicat

TiDB is a MySQL-compatible database, and [Navicat](https://www.navicat.com) is a GUI tool set for database users. This tutorial uses the [Navicat Premium](https://www.navicat.com/en/products/navicat-premium) tool to connect to TiDB.

In this tutorial, you can learn how to connect to your TiDB cluster using Navicat.

> **Note:**
>
> This tutorial is compatible with TiDB Cloud Serverless, TiDB Cloud Dedicated, and TiDB Self-Managed.

## Prerequisites

To complete this tutorial, you need:

- [Navicat Premium](https://www.navicat.com) **17.1.6** or later versions.
- A paid account for Navicat Premium.
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
    - **Connect With** is set to `Navicat`.
    - **Operating System** matches your environment.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.

5. Launch Navicat Premium, click **Connection** in the upper-left corner, select **PingCAP** from the **Vendor Filter** list, and double-click **TiDB** in the right panel.

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6. In the **New Connection (TiDB)** dialog, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Host**: enter the `HOST` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `PORT` parameter from the TiDB Cloud connection dialog.
    - **User Name**: enter the `USERNAME` parameter from the TiDB Cloud connection dialog.
    - **Password**: enter the password of the TiDB Cloud Serverless cluster.

    ![Navicat: configure connection general panel for TiDB Cloud Serverless](/media/develop/navicat-premium-connection-config-serverless-general.png)

7. Click the **SSL** tab and select **Use SSL**, **Use authentication**, and **Verify server certificate against CA** checkboxes. Then, select the `CA` file from the TiDB Cloud connection dialog into the **CA Certificate** field.

    ![Navicat: configure connection SSL panel for TiDB Cloud Serverless](/media/develop/navicat-premium-connection-config-serverless-ssl.png)

8. Click **Test Connection** to validate the connection to the TiDB Cloud Serverless cluster.

9. If the connection test is successful, you can see the **Connection Successful** message. Click **OK** to finish the connection configuration.

</div>
<div label="TiDB Cloud Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the connection dialog, select **Public** from the **Connection Type** drop-down list.

    If you have not configured the IP access list, click **Configure IP Access List** or follow the steps in [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) to configure it before your first connection.

    In addition to the **Public** connection type, TiDB Cloud Dedicated supports **Private Endpoint** and **VPC Peering** connection types. For more information, see [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster).

4. Click **CA cert** to download the CA certificate.

5. Launch Navicat Premium, click **Connection** in the upper-left corner, select **PingCAP** from the **Vendor Filter** list, and double-click **TiDB** in the right panel.

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6. In the **New Connection (TiDB)** dialog, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Host**: enter the `HOST` parameter from the TiDB Cloud connection dialog.
    - **Port**: enter the `PORT` parameter from the TiDB Cloud connection dialog.
    - **User Name**: enter the `USERNAME` parameter from the TiDB Cloud connection dialog.
    - **Password**: enter the password of the TiDB Cloud Dedicated cluster.

    ![Navicat: configure connection general panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-general.png)

7. Click the **SSL** tab and select **Use SSL**, **Use authentication**, and **Verify server certificate against CA** checkboxes. Then, select the CA file downloaded in step 4 into the **CA Certificate** field.

    ![Navicat: configure connection SSL panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-ssl.png)

8. **Test Connection** to validate the connection to the TiDB Cloud Dedicated cluster.

9. If the connection test is successful, you can see the **Connection Successful** message. Click **OK** to finish the connection configuration.

</div>
<div label="TiDB Self-Managed">

1. Launch Navicat Premium, click **Connection** in the upper-left corner, select **PingCAP** from the **Vendor Filter** list, and double-click **TiDB** in the right panel.

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

2. In the **New Connection (TiDB)** dialog, configure the following connection parameters:

    - **Connection Name**: give this connection a meaningful name.
    - **Host**: enter the IP address or domain name of your TiDB Self-Managed cluster.
    - **Port**: enter the port number of your TiDB Self-Managed cluster.
    - **User Name**: enter the username to use to connect to your TiDB.
    - **Password**: enter the password to use to connect to your TiDB.

    ![Navicat: configure connection general panel for self-hosted TiDB](/media/develop/navicat-premium-connection-config-self-hosted-general.png)

3. Click **Test Connection** to validate the connection to the TiDB Self-Managed cluster.

4. If the connection test is successful, you can see the **Connection Successful** message. Click **OK** to finish the connection configuration.

</div>
</SimpleTab>

## Next steps

- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](https://tidb.support.pingcap.com/).

</CustomContent>
