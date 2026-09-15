---
title: Configure an IP Access List
summary: Learn how to configure IP addresses that are allowed to access your TiDB Cloud Dedicated cluster.
---

# Configure an IP Access List

For each TiDB Cloud Dedicated cluster in TiDB Cloud, you can configure an IP access list to filter internet traffic trying to access the cluster, which works similarly to a firewall access control list. After the configuration, only the clients and applications whose IP addresses are in the IP access list can connect to your TiDB Cloud Dedicated cluster.

> **Note:**
>
> This document applies to [**TiDB Cloud Dedicated**](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated). For instructions on configuring an IP access list for **{{{ .starter }}}** or **{{{ .essential }}}**, see [Configure {{{ .starter }}} or Essential Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md).

## Add an IP address

To add an IP address to the IP access list for your TiDB Cloud Dedicated cluster, take the following steps:

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target TiDB Cloud Dedicated cluster to go to its overview page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the left navigation pane, click **Settings** > **Networking**.
3. On the **Networking** page, click **Add IP Address**.
4. In the **Add IP Address** dialog, add IP addresses with an optional description. For each TiDB Cloud Dedicated cluster, you can add up to 100 IP addresses.

    - To add a custom IP address, click the **+** icon, enter the IP address in CIDR notation (for example, `192.168.1.1/32`), and add a description.
    - To add the current IP address of your computer, click **Add Current IP**.
    - To allow any IP address to access your cluster, click **Allow access from anywhere**. This adds the `0.0.0.0/0` CIDR entry. This is highly risky and NOT recommended for production environments.

5. Click **Save**.

## Edit an IP address

To edit an existing IP address in the IP access list, take the following steps:

1. On the **Networking** page, locate the IP address you want to edit in the **IP Access List**.
2. Click **...** in the row of the IP address, and then click **Edit**.
3. In the **Edit IP Address** dialog, modify the IP address or description as needed.
4. Click **Submit**.

## Delete an IP address

To delete an existing IP address from the IP access list, take the following steps:

1. On the **Networking** page, locate the IP address you want to delete in the **IP Access List**.
2. Click **...** in the row of the IP address, and then click **Delete**.
3. In the confirmation dialog, click **Delete**.
