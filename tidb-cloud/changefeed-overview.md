---
title: Changefeed
summary: TiDB Cloud changefeed helps you stream data from TiDB Cloud to other data services.
---

# Changefeed

TiDB Cloud changefeed helps you stream data from TiDB Cloud to other data services. Currently, TiDB Cloud supports streaming data to Apache Kafka, MySQL, TiDB Cloud and cloud storage.

> **Note:**
>
> - Currently, TiDB Cloud only allows up to 100 changefeeds per <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>.
> - Currently, TiDB Cloud only allows up to 100 table filter rules per changefeed.
> - For [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) and [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) clusters, the changefeed feature is unavailable.

## View the Changefeed page

To access the changefeed feature, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), <CustomContent plan="dedicated">navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.</CustomContent><CustomContent plan="premium">navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page.</CustomContent>

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent> to go to its overview page, and then click **Data** > **Changefeed** in the left navigation pane. The changefeed page is displayed.

On the **Changefeed** page, you can create a changefeed, view a list of existing changefeeds, and operate the existing changefeeds (such as scaling, pausing, resuming, editing, and deleting a changefeed).

## Create a changefeed

To create a changefeed, refer to the tutorials:

- [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md)
- [Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)
- [Sink to TiDB Cloud](/tidb-cloud/changefeed-sink-to-tidb-cloud.md)
- [Sink to cloud storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md)

## Query changefeed capacity

<CustomContent plan="dedicated">

For TiDB Cloud Dedicated, you can query the TiCDC Replication Capacity Units (RCUs) of a changefeed.

1. Navigate to the [**Changefeed**](#view-the-changefeed-page) page of your target TiDB cluster.
2. Locate the corresponding changefeed you want to query, and click **...** > **View** in the **Action** column.
3. You can see the current TiCDC Replication Capacity Units (RCUs) in the **Specification** area of the page.

</CustomContent>
<CustomContent plan="premium">

For TiDB Cloud Premium, you can query the TiCDC Changefeed Capacity Units (CCUs) of a changefeed.

1. Navigate to the [**Changefeed**](#view-the-changefeed-page) page of your target TiDB instance.
2. Locate the corresponding changefeed you want to query, and click **...** > **View** in the **Action** column.
3. You can see the current TiCDC Changefeed Capacity Units (CCUs) in the **Specification** area of the page.

</CustomContent>

## Scale a changefeed

<CustomContent plan="dedicated">

You can change the TiCDC Replication Capacity Units (RCUs) of a changefeed by scaling up or down the changfeed.

> **Note:**
>
> - To scale a changefeed for a cluster, make sure that all changefeeds for this cluster are created after March 28, 2023.
> - If a cluster has changefeeds created before March 28, 2023, neither the existing changefeeds nor newly created changefeeds for this cluster support scaling up or down.

</CustomContent>
<CustomContent plan="premium">

You can change the TiCDC Changefeed Capacity Units (CCUs) of a changefeed by scaling up or down the changfeed.

</CustomContent>

1. Navigate to the [**Changefeed**](#view-the-changefeed-page) page of your target TiDB <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>.
2. Locate the corresponding changefeed you want to scale, and click **...** > **Scale Up/Down** in the **Action** column.
3. Select a new specification.
4. Click **Submit**.

It takes about 10 minutes to complete the scaling process (during which the changfeed works normally) and a few seconds to switch to the new specification (during which the changefeed will be paused and resumed automatically).

## Pause or resume a changefeed

1. Navigate to the [**Changefeed**](#view-the-changefeed-page) page of your target TiDB <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>.
2. Locate the corresponding changefeed you want to pause or resume, and click **...** > **Pause/Resume** in the **Action** column.

## Edit a changefeed

> **Note:**
>
> TiDB Cloud currently only allows editing changefeeds in the paused status.

1. Navigate to the [**Changefeed**](#view-the-changefeed-page) page of your target TiDB <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>.
2. Locate the changefeed you want to pause, and click **...** > **Pause** in the **Action** column.
3. When the changefeed status changes to `Paused`, click **...** > **Edit** to edit the corresponding changefeed.

    TiDB Cloud populates the changefeed configuration by default. You can modify the following configurations:

    - Apache Kafka sink: all configurations.
    - MySQL sink: **MySQL Connection**, **Table Filter**, and **Event Filter**.
    - TiDB Cloud sink: **TiDB Cloud Connection**, **Table Filter**, and **Event Filter**.
    - Cloud storage sink: **Storage Endpoint**, **Table Filter**, and **Event Filter**.

4. After editing the configuration, click **...** > **Resume** to resume the corresponding changefeed.

## Delete a changefeed

1. Navigate to the [**Changefeed**](#view-the-changefeed-page) page of your target TiDB <CustomContent plan="dedicated">cluster</CustomContent><CustomContent plan="premium">instance</CustomContent>.
2. Locate the corresponding changefeed you want to delete, and click **...** > **Delete** in the **Action** column.

## Changefeed billing

To learn the billing for changefeeds in TiDB Cloud, see [Changefeed billing](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md).

## Changefeed states

The state of a replication task represents the running state of the replication task. During the running process, replication tasks might fail with errors, or be manually paused or resumed. These behaviors can lead to changes of the replication task state.

The states are described as follows:

- `CREATING`: the replication task is being created.
- `RUNNING`: the replication task runs normally and the checkpoint-ts proceeds normally.
- `EDITING`: the replication task is being edited.
- `PAUSING`: the replication task is being paused.
- `PAUSED`: the replication task is paused.
- `RESUMING`: the replication task is being resumed.
- `DELETING`: the replication task is being deleted.
- `DELETED`: the replication task is deleted.
- `WARNING`: the replication task returns a warning. The replication cannot continue due to some recoverable errors. The changefeed in this state keeps trying to resume until the state transfers to `RUNNING`. The changefeed in this state blocks [GC operations](https://docs.pingcap.com/tidb/stable/garbage-collection-overview).
- `FAILED`: the replication task fails. Due to some errors, the replication task cannot resume and cannot be recovered automatically. If the issues are resolved before the garbage collection (GC) of the incremental data, you can manually resume the failed changefeed. The default Time-To-Live (TTL) duration for incremental data is 24 hours, which means that the GC mechanism does not delete any data within 24 hours after the changefeed is interrupted.
