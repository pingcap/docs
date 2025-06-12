---
title: Configure an IP Access List
summary: Learn how to configure IP addresses that are allowed to access your TiDB Cloud Dedicated cluster.
---

# Configure an IP Access List

For each TiDB Cloud Dedicated cluster in TiDB Cloud, you can configure an IP access list to filter internet traffic trying to access the cluster, which works similarly to a firewall access control list. After the configuration, only the clients and applications whose IP addresses are in the IP access list can connect to your TiDB Cloud Dedicated cluster.

> **Note:**
>
> This document applies to [**TiDB Cloud Dedicated**](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated). For instructions on configuring an IP access list for **TiDB Cloud Serverless**, see [Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md).

To configure an IP access list for your TiDB Cloud Dedicated cluster, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. In the left navigation pane, click **Settings** > **Networking**.
3. On the **Networking** page, click **Add IP Address**.
4. In the displayed dialog, choose one of the following options:

    - **Allow access from anywhere**: allows all IP addresses to access TiDB Cloud. This option exposes your cluster to the internet completely and is highly risky.
    - **Use IP addresses** (recommended): you can add a list of IPs and CIDR addresses that are allowed to access TiDB Cloud via a SQL client.

5. If you choose **Use IP addresses**, add IP addresses or CIDR range with an optional description. For each TiDB Cloud Dedicated cluster, you can add up to 100 IP addresses.
6. Click **Confirm** to save your changes.
