---
title: Connect to TiDB with JetBrains DataGrip
summary: Learn how to connect to TiDB using JetBrains DataGrip. This tutorial gives visual instructions that work with TiDB using JetBrains DataGrip.
---

# Connect to TiDB with JetBrains DataGrip

TiDB is a MySQL-compatible database, and [JetBrains DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html) is a powerful cross-platform IDE for working with SQL and NoSQL databases. You can use DataGrip in two distinct ways:

- Standalone edition: [Download](https://www.jetbrains.com/datagrip/download) and use **DataGrip** in a standalone IDE.
- Plugin edition: Use [JetBrains database tools and SQL plugin](https://www.jetbrains.com/help/idea/relational-databases.html) in JetBrains IDEs.

> **Note:**
>
> As per the documentation for the **JetBrains database tools and SQL plugin**, it offers support for all the features available in [DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html), the standalone database management environment for developers.
>
> We will primarily focus on the standalone edition, although the procedures in both editions are quite similar. Therefore, if you are using the plugin edition, you can also refer to this document for sufficient instructions.

In this tutorial, you will learn how to use TiDB and DataGrip to establish a connection to your TiDB cluster using DataGrip.

> **Note:**
>
> This tutorial is compatible with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you will need:

- [DataGrip **2023.2.1** or higher](https://www.jetbrains.com/datagrip/download/).
- A non-community edition [JetBrains](https://www.jetbrains.com/) IDE.

Additionally, ensure you have the following:

- A TiDB cluster.
- A paid account that allows the use of DataGrip.

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

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Connect With** is set to `JDBC`
    - **Operating System** matches your environment.

4. Click **Create password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Create a project to manage your connections.

    ![DataGrip create a project](/media/develop/datagrip-create-project.jpg)

6. Click **+** in the upper-left corner of the **Database Explorer** panel, and select **Data Source** > **Other** > **TiDB**.

    ![DataGrip select data source](/media/develop/datagrip-data-source-select.jpg)

7. Copy the JDBC string from the TiDB Cloud connection dialog and replace the `<your_password>` placeholder with your actual password. Then, paste it into `URL`, and the remaining parameters will be auto-filled. The example result is as follows:

    ![DataGrip URL paste](/media/develop/datagrip-url-paste.jpg)

8. Click **Download** missing driver files. If you have used DataGrip before, you can skip this step.

9. Click **Test Connection** to establish a connection to TiDB Serverless Tier cluster.

    ![DataGrip test connection](/media/develop/datagrip-test-connection.jpg)

10. Click **OK** to save it.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere** and then click **Download TiDB cluster CA** to download the CA certificate.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Create a project to manage your connections.

    ![DataGrip create a project](/media/develop/datagrip-create-project.jpg)

5. Click **+** in the upper-left corner of the **Database Explorer** panel, and select **Data Source** > **Other** > **TiDB**.

    ![DataGrip select data source](/media/develop/datagrip-data-source-select.jpg)

6. Copy and paste the corresponding connection string into the DataGrip connection panel. The correspoding relations are:

    - Host: {host}
    - Port: {port}
    - User: {user}
    - Password: {password}

    The example result is as follows:

    ![DataGrip dedicated tier connect](/media/develop/datagrip-dedicated-connect.jpg)

7. Navigate to **SSH/SSL**, check the **Use SSL** option, and input the CA certificate path into **CA file**.

    ![DataGrip dedicated tier connect](/media/develop/datagrip-dedicated-ssl.jpg)

8. Click **Download** missing driver files. If you have used DataGrip before, you can skip this step.

9. Navigate to **Advanced**, scroll down to the **enabledTLSProtocols** parameter, and set the value to `TLSv1.2,TLSv1.3`.

    ![DataGrip dedicated tier advanced](/media/develop/datagrip-dedicated-advanced.jpg)

10. Click **Test Connection** to establish a connection to TiDB Dedicated Tier cluster.

    ![DataGrip dedicated test connection](/media/develop/datagrip-dedicated-test-connection.jpg)

11. Click **OK** to save it.

</div>
<div label="TiDB Self-Hosted">

1. Create a project to manage your connections.

    ![DataGrip create a project](/media/develop/datagrip-create-project.jpg)

2. Click **+** in the upper-left corner of the **Database Explorer** panel, and select **Data Source** > **Other** > **TiDB**.

    ![DataGrip select data source](/media/develop/datagrip-data-source-select.jpg)

3. Copy and paste the corresponding connection string into the DataGrip connection panel. The correspoding relations are:

    - Host: {host}
    - Port: {port}
    - User: {user}
    - Password: {password}

    The example result is as follows:

    ![DataGrip self-hosted connect](/media/develop/datagrip-self-hosted-connect.jpg)

4. Click **Download** missing driver files. If you have used DataGrip before, you can skip this step.

5. Click **Test Connection** to establish a connection to TiDB Self-hosted cluster.

    ![DataGrip self-hosted test connection](/media/develop/datagrip-self-hosted-test-connection.jpg)

6. Click **OK** to save it.

</div>
</SimpleTab>

## Next steps

- Learn more usage of `DataGrip` from [the documentation of DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](https://support.pingcap.com/).
