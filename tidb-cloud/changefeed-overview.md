---
title: Changefeed
---

# Changefeed

TiDB Cloud changefeed helps you stream data from TiDB Cloud to other data services. Currently, TiDB Cloud supports streaming data to MySQL and Kafka.

> **Note:**
>
> To use the changefeed feature, make sure that your TiDB cluster version is v6.4.0 or later and the TiKV node size is at least 8 vCPU and 16 GiB.
>
> Currently, TiDB Cloud only allows up to 10 changefeeds per cluster.
>
> For [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta), the changefeed feature is unavailable.

Navigate to the **Changefeed** tab of your TiDB cluster, and you can see the changefeed list. In the changefeed list, you can:

- View the information of the created changefeed, including changefeed's id, checkpoint, and status.
- Operate the changefeed, including creating, pausing, resuming, editing, and deleting the changefeed.

## Create Changefeed

To create a changefeed, refer to the tutorials:

- [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) (Beta)
- [Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)

## Delete a Sink

1. Navigate to the **Changefeed** tab of a cluster.
2. Click **Action...** > **Delete** on the corresponding changefeed in the changefeed list.

## Pause or resume a Sink

1. Navigate to the **Changefeed** tab of a cluster.
2. Click **Action...** > **Pause/Resume** on the corresponding changefeed in the changefeed list.

## Edit a sink

> **Note:**
>
> TiDB Cloud currently only allows editing changefeeds in the paused status.

1. Navigate to the **Changefeed** tab of a cluster.
2. Click **Action...** > **Pause** to pause the corresponding changefeed.
3. When the changefeed status changes to `Paused`, click **Action...** > **Edit**  to edit the corresponding changefeed.

    TiDB Cloud populates the changefeed configuration by default. You can modify the following configurations:

    - MySQL sink: **MySQL Connection** and **Table Filter**.
    - Kafka sink: all configurations.

4. After editing the configuration, click **Action...** > **Resume** to resume the corresponding changefeed.

## Query TiCDC RCUs

1. Navigate to the **Changefeed** tab of a cluster.
2. You can see the current TiCDC Replication Capacity Units (RCUs) in the upper-right corner of the page.

To learn the billing for changefeeds in TiDB Cloud, see [Changefeed billing](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md).
