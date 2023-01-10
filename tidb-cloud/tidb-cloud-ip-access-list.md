---
title: Configure IP Access List
summary: Learn how to configure IP addresses to connect to your dedicated cluster.
---

# Configure IP Access List

IP access lists are similar to firewall access control lists, the main purpose is to filter internet traffic accessing your Dedicated tier cluster.

In your Dedicated Tier, you have two options where you can set up IP access lists that only allow your clients or applications with specified IP addresses to connect to your Dedicated Tier cluster.

1. You can click **Connect** to enter the **Standard Connection** page to configure your IP access list.

2. You can click **...** at the top of your cluster page, select **Security Settings** to configure your IP access list.

> **Note:**
>
> Only supports configuring the IP access list of the database cluster in the Dedicated Tier, and only set IP access list for your dedicated database Cluster. 

## Configure IP access list in standard connection 

In the TiDB Cloud console, navigate to your Dedicated Tier [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.You can click **Connect** to enter the **Standard Connection** page to configure the IP access list.

## Configure IP access list in security settings（Optional） 

For your Dedicated Tier clusters, you can also click the **...** in the upper-right corner of the page, select **Security Settings**, and configure IP Access List,too.

> **Tip:**
>
> If you have multiple projects, you can switch to the target project in the left navigation pane of the **Clusters** page.

## Add IP access list

1. In the TiDB Cloud console, navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

2. Click **Connect** to move to connection configure page,and then click **Standard Connection**.

3. Click **Add My Current IP Address** to automatically add IP Address of your terminal computer into IP Access List.

4. If you need to add more IP Addresses that are allowed to access your dedicated Cluster, click **Add Item** in the figure, and manually add the IP Address and Description.

5. Click **Update Filter** to save the configuration.

> **Tip:**
>
> If you want to allow any IP Address to access your database cluster, just click **Allow Access From Anywhere** to add it.According to the recommended security best practice, it is not recommended that you add allow access from anywhere to access your Dedicated cluster. This IP access rules is very dangerous, which means that you will completely expose the database to the Internet.

## Modify IP access list

On the **Connect** page of your Dedicated Tier cluster:

1. Select the **Standard Connection** tab, click **Edit** under "Create traffic filter" to open the edit page.

2. On the IP access editing page, click each IP access list to directly modify the IP Address and Description.

3. Click the **Add Item** button to add an IP access list, then click **update Filter** to save the update.

## Delete IP access list

On the IP access edit page of your Dedicated Tier cluster:

1. Click the Remove icon to delete the selected IP access list.

2. Click **Update Filter** to save the configuration.

> **Note:**
>
> In your Dedicated Tier, you can set up to 7 IP access lists per dedicated tier cluster. if the traffic filtering rules of your Dedicated cluster have reached the upper limit. If you need to apply for a quota, please contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).
