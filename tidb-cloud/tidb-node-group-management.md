---
title: Manage TiDB Node Groups
summary: Learn about how to manage TiDB node groups and their endpoints to isolate your business workload.
---

# Manage TiDB Node Groups

This document describes how to manage TiDB node groups and their endpoints to isolate your business workload using the [TiDB Cloud console](https://tidbcloud.com/).

> **Note**:
>
> The TiDB Node Group feature is **NOT** available for TiDB Cloud Serverless clusters.

## Terms

- TiDB Node Group: A TiDB node group manages the grouping of TiDB nodes and maintains the mapping between endpoints and TiDB nodes.

    - Each TiDB node group has a unique endpoint. 
    - When you delete a TiDB node group, the related network setting (such as private link and IP access list) will be deleted too. 

- Default Group: When a cluster is created, a default TiDB node group is created. Therefore, each cluster has a default group. The default group cannot be deleted. 

## Prerequisites

- You have a [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster deployed on AWS or Google Cloud.
- You are in the **Organization Owner** or **Project Owner** role of your organization. For more information, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

> **Note**:
>
> The TiDB node groups cannot be created during cluster creation. You need to add the groups after the cluster is created and in the **Available** state. 

## Create a TiDB node group

To create a TiDB node group, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Nodes**.
3. Click **Modify** in the upper-right corner. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, click **+** to add a new TiDB node group as follows. You can also use the default group directly.

    - TiDB
        - **vCPU + RAM**: choose the [TiDB size](/tidb-cloud/size-your-cluster.md#size-tidb) you need. Only TiDB nodes with 8 vCPU and 16 GiB memory or higher specifications are supported.
        - **Node Groups**: click **+** to create a new TiDB node group. You can also use the default group and enter the number of TiDB nodes in the **DefaultGroup** field.
    
    - TiKV
        - **vCPU + RAM**: choose the [TiKV size](/tidb-cloud/size-your-cluster.md#size-tikv) you need.
        - **Storage x Nodes**: choose the storage size and the number of TiKV nodes.
    
    - TiFlash (optional)
        - **vCPU + RAM**: choose the [TiFlash size](/tidb-cloud/size-your-cluster.md#size-tiflash) you need.
        - **Storage x Nodes**: choose the storage size and the number of TiFlash nodes.

    ![Create TiDB Node Group](/media/tidb-cloud/tidb-node-group-create.png)

5. New TiDB nodes are added along with the new TiDB node group, which affects the cluster's billing. Review the cluster size in the right pane, then click **Confirm**.

By default, you can create up to five TiDB node groups for a TiDB Cloud Dedicated cluster. If you need more groups, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md). 

If you create a TiDB node group but still use the endpoint of the default group to connect to the cluster, the TiDB nodes in the TiDB node group will not take any workload, which is a waste of the resource. You need to create new connection to the TiDB nodes in the new TiDB node group. See [Connect to a TiDB node group](#connect-to-a-tidb-node-group).

## Connect to a TiDB node group

### Connect via public connection

Public connection for the new TiDB node group is disabled by default. You need to enable it first.

To enable public connection, do the following:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.
2. In the upper-right corner, click **Connect**. A connection dialog is displayed.
3. Select your TiDB node group from the **TiDB Node Group** list and **Public** from the **Connection Type** list.

    If you have not configured the IP access list, click **Configure IP Access List** or follow the steps in [Configure an IP Access List](https://docs.pingcap.com/tidbcloud/configure-ip-access-list) to configure it before your first connection.

4. In the left navigation pane, click **Settings** > **Networking**.
5. On the **Networking** page, select your TiDB node group from the **TiDB Node Group** list in the upper-right corner.
6. Click **Enable** in the **Public Endpoint** section, then click **Add IP Address** in the **IP Access List** section.
7. In the upper-right corner of the **Networking** page, click **Connect** to get the connection string.

![Connect to the new TiDB node group via Public Endpoint](/media/tidb-cloud/tidb-node-group-connect-public-endpoint.png)

For more information, see [Connect to TiDB Cloud Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md).

### Connect via private endpoint

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.
2. In the upper-right corner, click **Connect**. A connection dialog is displayed.
3. Select your TiDB node group from the **TiDB Node Group** list and **Private Endpoint** from the **Connection Type** list.
4. In the left navigation pane, click **Settings** > **Networking**.
5. On the **Networking** page, select your TiDB node group from the **TiDB Node Group** list in the upper-right corner.
6. Click **Create Private Endpoint Connection** to create a new connection for this node group.

     - For clusters deployed on AWS, refer to [Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md). 
     - For clusters deployed on Google Cloud, refer to [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md).

    > **Note**:
    >
    > If you use Private Link to connect different node groups, you need to create separated private endpoint connection for each node group. 

7. After creating the private endpoint connection, click **Connect** in the upper-right corner of the page to get the connection string.

### Connect via VPC peering

Because all TiDB node groups share the same VPC as the cluster, you only need to create one VPC peering connection to enable access for all groups.

1. Follow the instructions in [Connect to TiDB Cloud Dedicated via VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) to create a VPC peering for this cluster.
2. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.
3. In the left navigation pane, click **Settings** > **Networking**.
4. In the upper-right corner of the **Networking** page, click **Connect** to get the connection string.

## View TiDB node groups

To view the details of TiDB node groups, perform the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Nodes** to view the list of TiDB node groups.

    To switch to the table view, click <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 -4 24 24" stroke-width="1.5"><path d="M3 9.5H21M3 14.5H21M7.8 4.5H16.2C17.8802 4.5 18.7202 4.5 19.362 4.82698C19.9265 5.1146 20.3854 5.57354 20.673 6.13803C21 6.77976 21 6.61984 21 8.3V15.7C21 17.3802 21 17.2202 20.673 17.862C20.3854 18.4265 19.9265 18.8854 19.362 19.173C18.7202 19.5 17.8802 19.5 16.2 19.5H7.8C6.11984 19.5 5.27976 19.5 4.63803 19.173C4.07354 18.8854 3.6146 18.4265 3.32698 17.862C3 17.2202 3 17.3802 3 15.7V8.3C3 6.61984 3 6.77976 3.32698 6.13803C3.6146 5.57354 4.07354 5.1146 4.63803 4.82698C5.27976 4.5 6.11984 4.5 7.8 4.5Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"></path></svg>.

## Modify a TiDB node group

You can modify the group name and node configurations in the group.

### Change the group name

To change the group name, perform the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Nodes**.
3. Click <svg width="16" height="16" viewBox="0 -2 24 24" stroke-width="1.5" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"/></svg> and enter a new name for the TiDB node group.

### Update the node configuration

To update TiDB, TiKV, or TiFlash node configurations in the group, perform the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Nodes**.
3. On the **Node Map** page, click **Modify** in the upper-right corner. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, you can:

    - Change the number of TiDB nodes.
    - Add new node groups.
    - Update the size and **Storage x Nodes** configuration for TiKV and TiFlash nodes.

![Change TiDB node group node count](/media/tidb-cloud/tidb-node-group-change-node-count.png)

## Delete a TiDB node group

> **Note**:
>
> When you delete a TiDB node group, its nodes and network configurations are also removed, including private endpoint connections and the IP list for public access.

To delete a TiDB node group, perform the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.
2. In the left navigation pane, click **Nodes**.
3. On the **Node Map** page, click **Modify** in the upper-right corner. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, click <svg width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16 6V5.2C16 4.0799 16 3.51984 15.782 3.09202C15.5903 2.71569 15.2843 2.40973 14.908 2.21799C14.4802 2 13.9201 2 12.8 2H11.2C10.0799 2 9.51984 2 9.09202 2.21799C8.71569 2.40973 8.40973 2.71569 8.21799 3.09202C8 3.51984 8 4.0799 8 5.2V6M10 11.5V16.5M14 11.5V16.5M3 6H21M19 6V17.2C19 18.8802 19 19.7202 18.673 20.362C18.3854 20.9265 17.9265 21.3854 17.362 21.673C16.7202 22 15.8802 22 14.2 22H9.8C8.11984 22 7.27976 22 6.63803 21.673C6.07354 21.3854 5.6146 20.9265 5.32698 20.362C5 19.7202 5 18.8802 5 17.2V6" stroke="currentColor" stroke-width="inherit" stroke-linecap="round" stroke-linejoin="round"/></svg> to delete the TiDB node group.

![Delete the TiDB node group](/media/tidb-cloud/tidb-node-group-delete.png)
