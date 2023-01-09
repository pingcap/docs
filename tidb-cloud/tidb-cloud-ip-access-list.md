---
title: Configure IP Access List
summary: Learn how to configure the root password and allowed IP addresses to connect to your dedicated cluster.
---

# Setting IP Access List

If you are viewing the overview page of your dedicated cluster, you can click the **Connect** go to **Standard Connection** page to set IP Access List, and also click the **...** in the upper-right corner of the page, select **Security Settings**, and configure IP Access List.

> **Note:**
>
>Only supports configuring the IP Access List of the database cluster in the Dedicated Tier, and only set IP Access List from the Cluster level. When you click "Add My Current IP Address", you can quickly add your client IP Address; click "Allow Access from Anywhere" to quickly add and allow any IP address to access Your database cluster, allow any IP address to access your Dedicated database cluster.

# Configure Cluster Security Settings

For Dedicated Tier clusters, you can also configure the root password at the security setting page of your cluster, you can click the **...** in the upper-right corner of the page, select **Security Settings**, and configure these settings, too.

## Add IP Access List

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

2. Click "Connect" to move to connection configure page,and then click"Standard Connection".

3. Click "Add My Current IP Address" to automatically add IP Address of your terminal computer into IP Access List.

4. If you need to add more IP Addresses that are allowed to access your dedicated Cluster, click "Add Item" in the figure, and manually add the IP Address and Description.

5. Click "Update Filter" to save the configuration.

> **Tip:**
>
> If you want to allow any IP Address to access your database cluster, just click "Allow Access From Anywhere" to add it.According to the recommended security best practice, it is not recommended that you add allow access from anywhere to access your Dedicated database cluster. This IP Access Rules is very dangerous, which means that you will completely expose the database to the Internet.

## Modify IP Access List

On the **Connect**"** page of your Dedicated Cluster:

1. Select the Standard Connection tab, click "Edit" under "Create traffic filter" to open the edit page.

2. On the IP Access editing page, click each IP Access List to directly modify the IP Address and Description.

3. Click the "Add Item" button to add an IP Access List, then click "update Filter" to save the update.

## Delete IP Access List

On the IP Access edit page of your Dedicated Cluster:

1. Click the Remove icon to delete the selected IP Access List.

2. Click “Update Filter” to save the configuration.

> **Note:**
>
>In your Dedicated Tier, each Dedicated cluster supports 20 IP Access Lists by default, if the traffic filtering rules of your Dedicated cluster have reached the upper limit. If you need to apply for a quota, please contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).