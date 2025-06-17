---
title: Connect to TiDB with JetBrains DataGrip
summary: Learn how to connect to TiDB using JetBrains DataGrip. This tutorial also applies to the Database Tools and SQL plugin available in other JetBrains IDEs, such as IntelliJ, PhpStorm, and PyCharm.
---

# Connect to TiDB with JetBrains DataGrip

TiDB is a MySQL-compatible database, and [JetBrains DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html) is a powerful integrated development environment (IDE) for database and SQL. This tutorial walks you through the process of connecting to your TiDB cluster using DataGrip.

You can use DataGrip in two ways:

- As the [DataGrip IDE](https://www.jetbrains.com/datagrip/download) standalone tool.
- As the [Database Tools and SQL plugin](https://www.jetbrains.com/help/idea/relational-databases.html) in JetBrains IDEs, such as IntelliJ, PhpStorm, and PyCharm.

This tutorial mainly focuses on the standalone DataGrip IDE. The steps of connecting to TiDB using the JetBrains Database Tools and SQL plugin in JetBrains IDEs are similar. You can also follow the steps in this document for reference when connecting to TiDB from any JetBrains IDE.

## Prerequisites

To complete this tutorial, you need:

- [DataGrip **2023.2.1** or later](https://www.jetbrains.com/datagrip/download/) or a non-community edition [JetBrains](https://www.jetbrains.com/) IDE.
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Cloud Starter cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Cloud Starter cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Connect to TiDB

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

1. Navigate to the [**Clusters**](https://console.tidb.io/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Connection Type** is set to `Public`
    - **Branch** is set to `main`
    - **Connect With** is set to `DataGrip`
    - **Operating System** matches your environment.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.

5. Launch DataGrip and create a project to manage your connections.

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

6. In the newly created project, click **+** in the upper-left corner of the **Database Explorer** panel, and select **Data Source** > **Other** > **TiDB**.

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

7. Copy the connection string from the TiDB Cloud connection dialog. Then, paste it into the **URL** field, and the remaining parameters will be auto-populated. An example result is as follows:

    ![Configure the URL field for TiDB Cloud Starter](/media/develop/datagrip-url-paste.jpg)

    If a **Download missing driver files** warning displays, click **Download** to acquire the driver files.

8. Click **Test Connection** to validate the connection to the TiDB Cloud Starter cluster.

    ![Test the connection to a TiDB Cloud Starter clustser](/media/develop/datagrip-test-connection.jpg)

9. Click **OK** to save the connection configuration.

## Next steps

- Learn more usage of DataGrip from [the documentation of DataGrip](https://www.jetbrains.com/help/datagrip/getting-started.html).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

<CustomContent platform="tidb">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs), or [submit a support ticket](https://tidb.support.pingcap.com/).

</CustomContent>
