---
title: Configure an IP Access List
summary: Learn how to configure IP addresses that are allowed to access your TiDB Dedicated cluster.
---

# Configure an IP Access List

For each TiDB Dedicated cluster in TiDB Cloud, you can configure an IP access list to filter internet traffic trying to access the cluster, which works similarly to a firewall access control list. After the configuration, only the clients and applications whose IP addresses are in the IP access list can connect to your TiDB Dedicated cluster.

> **Note:**
>
> Configuring the IP access list is only available for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

To configure an IP access list, take the following steps in the [TiDB Cloud console](https://tidbcloud.com/console/clusters):

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Networking**, and then click **Add IP Address**.
3. In the dialog, choose one of the following options:

    - **Allow access from anywhere**: allows all IP addresses to access TiDB Cloud. This option exposes your cluster to the internet completely and is highly risky.
    - **Use IP addresses** (recommended): you can add a list of IPs and CIDR addresses that are allowed to access TiDB Cloud via a SQL client.

4. If you choose **Use IP addresses**, add IP addresses or CIDR range with an optional description. For each TiDB Dedicated cluster, you can add up to 100 IP addresses.
5. Click **Confirm** to save your changes.
