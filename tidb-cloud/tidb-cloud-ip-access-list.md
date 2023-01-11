---
title: Configure IP Access List
summary: Learn how to configure IP addresses that are allowed to access your Dedicated Tier cluster.
---

# Configure IP Access List

For each Dedicated Tier cluster in TiDB Cloud, you can configure an IP access list to filter internet traffic trying to access the cluster, which works similarly to a firewall access control list. After the configuration, only the clients or applications whose IP addresses are in the IP access list can connect to your Dedicated Tier cluster.

> **Note:**
>
> Configuring the IP access list is only available for [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier) clusters.

For a Dedicated Tier cluster, you can configure its IP access list in either of the following ways:

- [Configure IP access list in standard connection](#configure-ip-access-list-in-standard-connection)

- [Configure IP access list in security settings](#configure-ip-access-list-in-security-settings)

## Configure IP access list in standard connection

To configure the IP access list for your Dedicated cluster in standard connection, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of your Dedicated Tier cluster, click **...** and select **Connect**. A dialog is displayed.
3. In the dialog, locate ***Step 1: Create traffic filter** on the **Standard Connection** tab and configure the IP access list.

    - If the IP access list of your cluster has not been set, you can click **Add My Current IP Address** to add your current IP address to the IP access list, and then click **Add Item** to add more IP addresses if necessary. Next, click **Update Filter** to save the configuration.

        > **Note:**
        >
        > For each Dedicated Tier cluster, you can add up to 7 IP addresses to the IP access list. To apply for a quota to add more IP addresses, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

    - If the IP access list of your cluster has been set, click **Edit** to add, edit, or remove IP addresses, and then click **Update Filter** to save the configuration.

    - To allow any IP address to access your cluster (not recommended), click **Allow Access From Anywhere**, and then click **Update Filter**. According to security best practices, it is NOT recommended that you allow any IP address to access your cluster, as this would expose your cluster to the internet completely and is highly dangerous.

## Configure IP access list in security settings

To configure the IP access list for your Dedicated cluster in security settings, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. In the row of your Dedicated Tier cluster, click **...** and select **Security Settings**. A security setting dialog is displayed.
3. In the dialog, configure the IP access list as follows:

    - To add your current IP address to the IP access list, click **Add My Current IP Address**.

    - To add an IP address to the IP access list, enter the IP address and description, and click **Add to IP List**.

        > **Note:**
        >
        > For each Dedicated Tier cluster, you can add up to 7 IP addresses to the IP access list. To apply for a quota to add more IP addresses, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

    - To allow any IP address to access your cluster (not recommended), click **Allow Access From Anywhere**, and then click **Update Filter**. According to security best practices, it is NOT recommended that you allow any IP address to access your cluster, as this would expose your cluster to the internet completely and is highly dangerous.

    - To remove an IP address from the access list, click **Remove** in the line of the IP address.