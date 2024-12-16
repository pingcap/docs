title: Manage TiDB Node Groups
summary: Learn about how to manage TiDB node groups.
---

# Manage TiDB Node Groups

This document describes how to create TiDB node groups and their endpoints to isolate your business workload using the [TiDB Cloud console](https://tidbcloud.com/). It also shows how to view details of a TiDB node group.

> **Note**:
>
> Currently, the TiDB Node Group feature is only available upon request. To request this feature, click ? in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com/) and click Request Support. Then, fill in **Apply for TiDB Node Group feature** in the **Description** field and click **Submit**.

## Prerequisites

- You are using a [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster on AWS. The TiDB Node Group feature is **NOT** available for TiDB Cloud Serverless clusters.
- You are in the **Organization Owner** or **Project Owner** role of your organization. For more information, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

## Terms

- TiDB Node Group: TiDB node group manages the grouping of TiDB nodes and maintains the mapping between endpoints and TiDB nodes.

    - Each TiDB node group has an independent endpoint. 
    - When you delete a TiDB node group, the related network setting (such as private link and IP access list) will be deleted too. 

- Default Group: When a cluster created, a default TiDB node group is created. Therefore, each cluster has a default group. The default group can not be deleted. 

## Create a TiDB node group

> **Note**:
>
> If you create a TiDB node group but still use the endpoint of the default group to connect the cluster, the TiDB nodes in the new node group will not take any workload, which is a waste of the resource. 

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page of your project.
2. Click **...** in the upper-right corner.
3. Click **Modify** in the drop-down menu. The **Modify Cluster** page is displayed.
4. On the **Modify Cluster** page, click + to add a new TiDB node group as follows.

    - TiDB
        - **vCPU + RAM**: choose the [TiDB size](/tidb-cloud/size-your-cluster.md#size-tidb) you need.
        - **Node Groups**: enter the number of TiDB nodes in the Default Groups field. You can also create new node groups by clicking +.
    - TiKV
        - **vCPU + RAM**: choose the [TiKV size](/tidb-cloud/size-your-cluster.md#size-tikv) you need.
        - **Storage X Nodes**: choose the storage size and the number of TiKV nodes.

  ![Create TiDB Node Group](/media/tidb-cloud/tidb-node-group-create.png)

5. New TiDB nodes will be added with the new TiDB node group. The billing of the cluster will change. Review the cluster size in the right pane, and then click **Confirm**.

## Connect to the new TiDB node group

### Connect via Public Endpoint

Public Endpoint for the new TiDB node group is disabled by default. You need to enable it first.

To enable Public Endpoint, do the following:

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. Choose the new TiDB node group and public connection type.
4. Visit the **Networking** page and select the new node group.
5. Enable the Public Endpoint and add the IP access list.
6. Click **Connect** on the up-right of the page and you can get the connection string. 

![Connect to the new TiDB node group via Public Endpoint](/media/tidb-cloud/tidb-node-group-connect-public-endpoint.png)

### Connect via Private Endpoint

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. Choose the new TiDB node group and public connection type.
4. Visit the **Networking** page and select the new node group.
5. Click **Create Private Endpoint Connection** to create a new connection for this node group. For more information, see [Connect to a TiDB Cloud Dedicated Cluster via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections.md).

    > **Note**:
    >
    > If you use Private Link to connect different node groups, you need to create separated Private Endpoint Connection for each node group. 

6. After you create the Private Endpoint Connection, click **Connect** on the up-right of the page to get the connection string. 

### Connect via VPC Peering

Because the cluster is in one VPC and all the TiDB node groups share the same VPC, you only need to create one VPC Peering, then all the groups can use it. 

1. Follow the instrcutions in [Connect to TiDB Cloud Dedicated via VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md) to create a VPC Peering for this cluster. 
2. Click **Connect** on the up-right of the **Networking** page to get the connection string. 

### View the TiDB node groups

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters)  page.
2. Click **Nodes** in the left pane.

    ![TiDB node group window view](/media/tidb-cloud/tidb-node-group-window-view.png)

    **You can also click the button highlighted in the screenshot to switch to table view.**

    ![TiDB node group table view](/media/tidb-cloud/tidb-node-group-table-view.png)

## Modify the TiDB node group

### Change the group name

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) overview page.
2. Click **Nodes** in the left pane.
3. Click the edit icon hilighted in the screenshot to change the name of the TiDB node group.

![Change TiDB node group name](/media/tidb-cloud/tidb-node-group-change-name.png)

### Change the number of TiDB nodes

1. Navigate to the [**Cluster**](https://tidbcloud.com/console/clusters) page.
2. Click **Nodes** in the left pane.
3. Click **Modify**. 
4. On the **Modify Cluster** page, update the number of TiDB nodes, or add new TiDB node groups.

![Change TiDB node group node count](/media/tidb-cloud/tidb-node-group-change-name.png)

### Delete the TiDB node group

> **Warning**:
>
> Deleting the groups (new-group) will also remove the nodes and associated network configurations, including private endpoint connections and the IP list for public access.

1. Navigate to the [Cluster](https://tidbcloud.com/console/clusters) overview page.
2. Click **Nodes** in the left pane.
3. Click **Modify**.
4. On the **Modify Cluster** page, click the delete icon to delete the TiDB node groups.

![Delete the TiDB node group](/media/tidb-cloud/tidb-node-group-delete.png)
