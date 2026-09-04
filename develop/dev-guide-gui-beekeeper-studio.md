---
title: Connect to TiDB with Beekeeper Studio
summary: Learn how to connect to TiDB using Beekeeper Studio.
aliases: ['/tidb/stable/dev-guide-gui-beekeeper-studio/','/tidb/dev/dev-guide-gui-beekeeper-studio/','/tidbcloud/dev-guide-gui-beekeeper-studio/']
---

# Connect to TiDB with Beekeeper Studio

TiDB is a MySQL-compatible database, and [Beekeeper Studio](https://www.beekeeperstudio.io/) is a free, open-source SQL editor and database manager with a modern, easy-to-use interface for Windows, macOS, and Linux. Beekeeper Studio has a built-in, native **TiDB** connection type.

In this tutorial, you can learn how to connect to TiDB using Beekeeper Studio Community Edition.

> **Note:**
>
> This tutorial is compatible with {{{ .starter }}}, {{{ .essential }}}, {{{ .premium }}}, TiDB Cloud Dedicated, and TiDB Self-Managed.

## Prerequisites

To complete this tutorial, you need:

- [Beekeeper Studio Community Edition **4.3.0** or later](https://www.beekeeperstudio.io/get). Beekeeper Studio Community Edition is free and open source, so no paid account is required.
- A TiDB cluster.

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) [Create a {{{ .starter }}} instance](/develop/dev-guide-build-cluster-in-cloud.md).
- [Deploy a local test TiDB Self-Managed cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB Self-Managed cluster](/production-deployment-using-tiup.md).

## Connect to TiDB

Connect to TiDB depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="{{{ .starter }}} or Essential">

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .starter }}} or Essential instance to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Connection Type** is set to `Public`.
    - **Branch** is set to `main`.
    - **Connect With** is set to `Beekeeper Studio` (or the closest match, such as `General`, if Beekeeper Studio is not in the list).
    - **Operating System** matches your environment.

4. Click **Generate Password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.

5. Launch Beekeeper Studio. On the connections screen, click **New Connection**, select **TiDB** from the **Connection Type** list, and fill in the connection form: copy the **Host** and **Port** from the TiDB Cloud connection dialog, and enter the **User** and **Password** from steps 3 and 4.

    ![Beekeeper Studio: configure a TiDB connection](/media/develop/beekeeper-studio-connection-settings.png)

6. Turn on the **Enable SSL** toggle, since {{{ .starter }}} and Essential require an encrypted connection.

    Unlike some GUI clients, Beekeeper Studio does not require you to manually download or select a CA certificate here — by default it trusts the server's certificate, so enabling SSL is enough.

7. Click **Test** to validate the connection to your target {{{ .starter }}} or Essential instance.

8. If the connection test succeeds, click **Connect** to save the connection and start using it.

</div>
<div label="{{{ .premium }}}">

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .premium }}} instance to go to its overview page.

2. In the left navigation pane, click **Settings** > **Networking**.

3. On the **Networking** page, click **Enable** for **Public Endpoint**, and then click **Add IP Address**.

    Ensure that your client IP address is added to the access list.

4. In the left navigation pane, click **Overview** to return to the instance overview page.

5. Click **Connect** in the upper-right corner. A connection dialog is displayed.

6. In the connection dialog, select **Public** from the **Connection Type** drop-down list.

    - If a message indicates that the public endpoint is still being enabled, wait until the process completes.
    - If you have not set a password yet, click **Set Root Password** in the dialog.
    - In addition to the **Public** connection type, {{{ .premium }}} supports **Private Endpoint** connections. For more information, see [Connect to {{{ .premium }}} via AWS PrivateLink](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md).

7. Launch Beekeeper Studio. On the connections screen, click **New Connection**, select **TiDB** from the **Connection Type** list, and fill in the connection form: copy and paste the **Host**, **Port**, and **Username** from the connection dialog, and enter the password of the {{{ .premium }}} instance.

    Leave **Enable SSL** off.

8. Click **Test** to validate the connection to the {{{ .premium }}} instance.

9. If the connection test succeeds, click **Connect** to save the connection and start using it.

</div>
<div label="TiDB Cloud Dedicated">

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target TiDB Cloud Dedicated cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the connection dialog, select **Public** from the **Connection Type** drop-down list.

    If you have not configured the IP access list, click **Configure IP Access List** or follow the steps in [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) to configure it before your first connection.

    In addition to the **Public** connection type, TiDB Cloud Dedicated supports **Private Endpoint** and **VPC Peering** connection types. For more information, see [Connect to Your TiDB Cloud Dedicated Cluster](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster).

4. Launch Beekeeper Studio. On the connections screen, click **New Connection**, select **TiDB** from the **Connection Type** list, and fill in the connection form: copy and paste the **Host**, **Port**, and **Username** from the TiDB Cloud connection dialog, and enter the password of the TiDB Cloud Dedicated cluster.

    ![Beekeeper Studio: configure a TiDB connection](/media/develop/beekeeper-studio-connection-settings.png)

5. Turn on the **Enable SSL** toggle. Beekeeper Studio trusts the server's certificate by default, so providing a CA certificate is optional — if you want to verify against the CA certificate for your cluster, click **CA cert** in the TiDB Cloud connection dialog to download it, and select the downloaded file in the **CA Cert (optional)** field.

6. Click **Test** to validate the connection to the TiDB Cloud Dedicated cluster.

7. If the connection test succeeds, click **Connect** to save the connection and start using it.

</div>
<div label="TiDB Self-Managed" value="tidb">

1. Launch Beekeeper Studio. On the connections screen, click **New Connection**, select **TiDB** from the **Connection Type** list, and configure the following connection parameters:

    - **Host**: the IP address or domain name of your TiDB Self-Managed cluster.
    - **Port**: the port number of your TiDB Self-Managed cluster.
    - **User**: the username to use to connect to your TiDB Self-Managed cluster.
    - **Password**: the password of the username.

    ![Beekeeper Studio: configure connection settings for TiDB Self-Managed](/media/develop/beekeeper-studio-connection-settings-self-hosted.png)

2. Click **Test** to validate the connection to the TiDB Self-Managed cluster.

3. If the connection test succeeds, click **Connect** to save the connection and start using it.

</div>
</SimpleTab>

## Next steps

- Learn more usage of Beekeeper Studio from [the Beekeeper Studio documentation](https://docs.beekeeperstudio.io/).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](https://docs.pingcap.com/developer/), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Submit a support ticket for TiDB Self-Managed](/support.md)
