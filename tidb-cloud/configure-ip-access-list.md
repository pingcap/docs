---
title: Configure an IP Access List
summary: Learn how to configure IP addresses that are allowed to access your TiDB Cloud Dedicated cluster.
---

# Configure an IP Access List

For each TiDB Cloud Dedicated cluster in TiDB Cloud, you can configure an IP access list to filter internet traffic trying to access the cluster, which works similarly to a firewall access control list. After the configuration, only the clients and applications whose IP addresses are in the IP access list can connect to your TiDB Cloud Dedicated cluster.

> **Note:**
>
> Configuring the IP access list is only available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

For a TiDB Dedicated cluster, you can configure its IP access list in either of the following ways:

- [Configure an IP access list in standard connection](#configure-an-ip-access-list-in-standard-connection)

- [Configure an IP access list in security settings](#configure-an-ip-access-list-in-security-settings)

4. If you choose **Use IP addresses**, add IP addresses or CIDR range with an optional description. For each TiDB Cloud Dedicated cluster, you can add up to 100 IP addresses.
5. Click **Confirm** to save your changes.
