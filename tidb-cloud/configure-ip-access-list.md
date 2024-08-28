---
title: Configure an IP Access List
summary: Learn how to configure IP addresses that are allowed to access your TiDB Dedicated cluster.
---

# Configure an IP Access List

For each TiDB Dedicated cluster in TiDB Cloud, you can configure an IP access list to filter internet traffic trying to access the cluster, which works similarly to a firewall access control list. After the configuration, only the clients and applications whose IP addresses are in the IP access list can connect to your TiDB Dedicated cluster.

> **Note:**
>
> Configuring the IP access list is only available for [TiDB Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-dedicated) clusters.

## Configure an IP access list in Networking page

To configure an IP access list for your TiDB Dedicated cluster in networking page, take the following steps:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target TiDB cluster to go to its overview page.
2. Go to **Network** in the left navigation pane, click **Add IP Address**.
3. In the dialog, choose one of the following options.

    - **Allow access from anywhere** : All IP addresses are allowed to access TiDB Cloud. This would expose your cluster to the internet completely, which is highly risky.
    - **Use IP addresses**: Recommand, you can add a list of IPs and CIDR addresses that are allowed to access TiDB Cloud via a SQL client.

3. Add IP addresses or CIDR range with an optional description. You can add up to 100 addresses.

4. Click **Confirm** to confirm the changes.