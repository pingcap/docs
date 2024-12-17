---
title: Manage TiDB Node Groups
summary: Learn about how to manage TiDB node groups.
---

# Manage TiDB Node Groups

This document describes how to manage TiDB node groups and their endpoints to isolate your business workload using the [TiDB Cloud console](https://tidbcloud.com/). 

Currently, the TiDB Node Group feature is in private beta and only available upon request. To request this feature:

1. Click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com/).
2. Click **Request Support**. 
3. Fill in **Apply for TiDB Node Group feature** in the **Subject** field.
4. Click **Submit**.

## Terms

- TiDB Node Group: A TiDB node group manages the grouping of TiDB nodes and maintains the mapping between endpoints and TiDB nodes.

    - Each TiDB node group has an independent endpoint. 
    - When you delete a TiDB node group, the related network setting (such as private link and IP access list) will be deleted too. 

- Default Group: When a cluster created, a default TiDB node group is created. Therefore, each cluster has a default group. The default group can not be deleted. 

## Prerequisites

- You have a [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster on AWS.
- You are in the **Organization Owner** or **Project Owner** role of your organization. For more information, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

## Create a TiDB node group

> **Note**:
>
> If you create a TiDB node group but still use the endpoint of the default group to connect to the cluster, the TiDB nodes in the TiDB node group will not take any workload, which is a waste of the resource. 

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page of your project.
2. Click **Nodes** in the left navigation pane.
3. Click **Modify** in the upper-right corner. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, click **+** to add a new TiDB node group as follows.

    - TiDB
        - **vCPU + RAM**: choose the [TiDB size](/tidb-cloud/size-your-cluster.md#size-tidb) you need. Only TiDB nodes with 8 vCPU and 16 GiB memory or higher specifications are supported.
        - **Node Groups**: enter the number of TiDB nodes in the Default Groups field. You can also create new node groups by clicking **+**. 
    
    - TiKV
        - **vCPU + RAM**: choose the [TiKV size](/tidb-cloud/size-your-cluster.md#size-tikv) you need.
        - **Storage X Nodes**: choose the storage size and the number of TiKV nodes.
    
    - TiFlash (Optional)
        - **vCPU + RAM**: choose the [TiFlash size](/tidb-cloud/size-your-cluster.md#size-tiflash) you need.
        - **Storage X Nodes**: choose the storage size and the number of TiFlash nodes.

    ![Create TiDB Node Group](/media/tidb-cloud/tidb-node-group-create.png)

5. New TiDB nodes will be added together with the new TiDB node group. The billing of the cluster will change. Review the cluster size in the right pane, and then click **Confirm**.

By default, you can create up to five TiDB node groups for a TiDB Cloud Dedicated cluster. If you need more groups, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md). 

## Connect to a TiDB node group

### Connect via public connection

Public connection for the new TiDB node group is disabled by default. You need to enable it first.

To enable public connection, do the following:

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. Choose the new TiDB node group and the **Public** connection type.
4. Click **Configure the IP Access** List.
4. On the **Networking** page, select the TiDB node group in the upper-right corner.
5. Enable the public endpoint and add the IP access list.
6. Click **Connect** on the up-right of the page and you can get the connection string. 

![Connect to the new TiDB node group via Public Endpoint](/media/tidb-cloud/tidb-node-group-connect-public-endpoint.png)

For more information, see [Connect to TiDB Cloud Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md).

### Connect via private endpoint

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. Choose the new TiDB node group and **Private Endpoint** connection type.
4. Click **Networking** in the left navigation pane. On the **Networking** page, select the TiDB node group.
5. Click **Create Private Endpoint Connection** to create a new connection for this node group. For more information, see [Connect to a TiDB Cloud Dedicated Cluster via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections.md).

    > **Note**:
    >
    > If you use Private Link to connect different node groups, you need to create separated private endpoint connection for each node group. 

6. After you create the private endpoint connection, click **Connect** on the up-right of the page to get the connection string. 

### Connect via VPC peering

Because the cluster is in one VPC and all the TiDB node groups share the same VPC, you only need to create one VPC peering, then all the groups can use it. 

1. Follow the instrcutions in [Connect to TiDB Cloud Dedicated via VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) to create a VPC peering for this cluster. 
2. Click **Networking** in the left navigation pane. 
3. On the **Networking** page, click **Connect** on the up-right to get the connection string. 

## View TiDB node groups

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page.
2. Click **Nodes** in the left pane to view the list of TiDB node groups.

![TiDB node group window view](/media/tidb-cloud/tidb-node-group-window-view.png)

You can also click the button highlighted in the following creenshot to switch to the table view.

![TiDB node group table view](/media/tidb-cloud/tidb-node-group-table-view.png)

## Modify a TiDB node group

You can change the group name and the number of TiDB nodes in the group.

### Change the group name

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page.
2. Click **Nodes** in the left navigation pane.
3. Click the edit icon highlighted in the screenshot to change the name of the TiDB node group.

![Change TiDB node group name](/media/tidb-cloud/tidb-node-group-change-name.png)

### Change the number of TiDB nodes

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page.
2. Click **Nodes** in the left navigation pane.
3. Click **Modify** in the upper-right corner. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, update the number of TiDB nodes, or add new node groups. On this page, you can also change the size and Storage X Nodes of the TiKV and TiFlash nodes.

![Change TiDB node group node count](/media/tidb-cloud/tidb-node-group-change-node-count.png)

## Delete a TiDB node group

> **Note**:
>
> Deleting a TiDB node group will also remove the nodes and associated network configurations, including private endpoint connections and the IP list for public access.

1. Navigate to the [Cluster](https://tidbcloud.com/console/clusters) page.
2. Click **Nodes** in the left navigation pane.
3. Click **Modify** in the upper-right corner. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, click the delete icon to delete the TiDB node group. 

![Delete the TiDB node group](/media/tidb-cloud/tidb-node-group-delete.png)
