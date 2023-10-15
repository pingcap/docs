---
title: Connect to TiDB with Visual Studio Code
summary: Learn how to connect to TiDB using Visual Studio Code (VS Code) or Github Codespaces. This tutorial gives visual instructions that work with TiDB using Visual Studio Code or Github Codespaces.
---

# Connect to TiDB with Visual Studio Code

TiDB is a MySQL-compatible database, and [Visual Studio Code](https://code.visualstudio.com/)(or VS Code, VSC) is a lightweight but powerful source code editor. In this tutorial, we will use the [vscode-sqltools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) extension which supports TiDB as an [official driver](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql).

In this tutorial, you will learn how to use to connect to your TiDB cluster using Visual Studio Code.

> **Note:**
>
> This tutorial is compatible with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

> **Note:**
>
> This tutorial also works with Visual Studio Code Remote Development enviorments including [Github Codespaces](https://github.com/features/codespaces), [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers), [Visual Studio Code WSL](https://code.visualstudio.com/docs/remote/wsl), etc.

## Prerequisites

To complete this tutorial, you will need:

- [Visual Studio Code](https://code.visualstudio.com/#alt-downloads) `1.72.0` or higher.
- [SQLTools MySQL/MariaDB/TiDB](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) extension for Visual Studio Code. To install it,
    - Just [click this link to launch VS Code and install it directly](vscode:extension/mtxr.sqltools-driver-mysql). 
    - Or, visit [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql) and click Install. 
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

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Tip:**
    >
    > If your VS Code is running against a remote development enviorment, select the remote OS from the list. For example, if you are using Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution. If you are using Github Codespaces, this doesn't matter.

4. Click **Create password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Go back to VS Code, click **Add New Connection**, and select **TiDB** type.

    ![VS Code sqltools add bew connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

6. Fill in parameters in setting panal.

    - Connection name: Please give a meanful name for this connection.
    - Connection group: (Optional) A meanful name for the group of this connection. And the connections which have the same group name will be gethered together.
    - Connect using: Please select **Server and Port**.
    - Server Address: The parameter `host` from TiDB Cloud connection dialog.
    - Port: The parameter `port` from TiDB Cloud connection dialog.
    - Database: The database that you want to connect.
    - Username: The parameter `user` from TiDB Cloud connection dialog.
    - Password mode: Please select **SQLTools Driver Credentials**.
    - In **MySQL driver specific options** scope:

        - Authentication Protocol: Please select **default**.
        - SSL: Please select **Enabled**. TiDB Serverless requires a secure connection. In **SSL Options (node.TLSSocket)** scope:

            - Certificate Authority (CA) Certificate File: sername: The parameter `ssl_ca` from TiDB Cloud connection dialog.

            > **Note:**
            >
            > If you are running on Windows or Github Codespaces, you can leave this blank. Default is to trust the well-known CAs curated by Mozilla. Learn more about [TiDB Serverless root certificate management](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters#root-certificate-management)

    ![VS Code sqltools serverless connection config](/media/develop/vsc-sqltools-connection-config-serverless.jpg)

7. Click **TEST CONNECTION**, then click **Allow** in the popupwindow.
8. Enter `password` from TiDB Cloud.

    ![VS Code sqltools serverless password](/media/develop/vsc-sqltools-password.jpg)

9. If you can see **Successfully connected!** text appared. Then click **SAVE CONNECTION**.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere**.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Go back to VS Code, click **Add New Connection**, and select **TiDB** type.

    ![VS Code sqltools add bew connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

5. Fill in parameters in setting panal.

    - Connection name: Please give a meanful name for this connection.
    - Connection group: (Optional) A meanful name for the group of this connection. And the connections which have the same group name will be gethered together.
    - Connect using: Please select **Server and Port**.
    - Server Address: The parameter `host` from TiDB Cloud connection dialog.
    - Port: The parameter `port` from TiDB Cloud connection dialog.
    - Database: The database that you want to connect.
    - Username: The parameter `user` from TiDB Cloud connection dialog.
    - Password mode: Please select **SQLTools Driver Credentials**.
    - In **MySQL driver specific options** scope:

        - Authentication Protocol: Please select **default**.
        - SSL: Please select **Disabled**.

    ![VS Code sqltools dedicated connection config](/media/develop/vsc-sqltools-connection-config-dedicated.jpg)

6. Click **TEST CONNECTION**, then click **Allow** in the popupwindow.
7. Enter `password` from TiDB Cloud.

    ![VS Code sqltools dedicated password](/media/develop/vsc-sqltools-password.jpg)

8. If you can see **Successfully connected!** text appared. Then click **SAVE CONNECTION**.

</div>
<div label="TiDB Self-Hosted">

1. Click **Add New Connection**, and select **TiDB** type.

    ![VS Code sqltools add bew connection](/media/develop/vsc-sqltools-add-new-connection.jpg)

2. Fill in parameters in setting panal.

    - Connection name: Please give a meanful name for this connection.
    - Connection group: (Optional) A meanful name for the group of this connection. And the connections which have the same group name will be gethered together.
    - Connect using: Please select **Server and Port**.
    - Server Address: TiDB cluster host.
    - Port: TiDB cluster host.
    - Database: The database that you want to connect.
    - Username: TiDB cluster username.
    - Password mode:

        - If the password is empty, please select **Use empty password**.
        - Otherwise, please select **SQLTools Driver Credentials**.

    - In **MySQL driver specific options** scope:

        - Authentication Protocol: Please select **default**.
        - SSL: Please select **Disabled**.

    ![VS Code sqltools self-hosted connection config](/media/develop/vsc-sqltools-connection-config-self-hosted.jpg)

3. Click **TEST CONNECTION**.
4. (Optional) If the password is not empty, click **Allow** in the popupwindow, then enter the password from TiDB cluster.

    ![VS Code sqltools self-hosted password](/media/develop/vsc-sqltools-password.jpg)

5. If you can see **Successfully connected!** text appared. Then click **SAVE CONNECTION**.

</div>
</SimpleTab>

## Next steps

- Learn more usage of `Visual Studio Code` from [the documentation of Visual Studio Code](https://code.visualstudio.com/docs).
- Learn more usage of `VSCode SQLTools` extension from [the documentation](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) and [GitHub repository](https://github.com/mtxr/vscode-sqltools) of SQLTools.
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](https://support.pingcap.com/).
