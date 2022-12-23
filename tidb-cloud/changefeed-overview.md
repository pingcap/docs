---
title: Changefeed
---

# Changefeed

TiDB Cloud Changefeed help you stream data from TiDB Cloud to your MySQL/Kafka.

> **Note:**
>
> To use the Changefeed feature, make sure that your TiDB cluster version is v6.4.0 or later and the TiKV node size is at least 8 vCPU and 16 GiB.
>
> Currently, TiDB Cloud only allows up to 10 changefeeds per cluster.
>
> For [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta), the changefeed feature is unavailable.

Navigate to the **Changefeed** tab of your TiDB cluster and you can see the changefeed list. In the changefeed list, you can:

- View the information of the created changefeed, including changefeed's id, checkpoint, status.
- Operate the changefeed, including creating, pausing, resuming, editing, and deleting the changefeed.

## Create Changefeed

To create a changefeed, please refer to the tutorial:

- [Sink to Apache Kafka](/tidb-cloud/changefeed-sink-to-apache-kafka.md) (Beta)
- [Sink to MySQL](/tidb-cloud/changefeed-sink-to-mysql.md)

## Delete a Sink

1. Navigate to the **Changefeed** tab of a cluster.
2. Click the **Action... > Delete** of the corresponding Changefeed in Changefeed list.

## Pause or resume a Sink

1. Navigate to the **Changefeed** tab of a cluster.
2. Click the **Action... > Pause/Resume** of the corresponding Changefeed in Changefeed list.

## Edit a sink

> **Note:**
>
> TiDB Cloud currently only allows editing of changefeeds in the paused status

1. Navigate to the **Changefeed** tab of a cluster.
2. Click the **Action... > Pause**  to pause the corresponding Changefeed.
3. When the changefeed status changes to paused, click the **Action... > edit**  to edit the corresponding Changefeed.

    TiDB Cloud populates the changefeed configuration by default, the configurations that can be modified include

    - **MySQL Connection** and **Table Filter** configurations for MySQL sink.
    - all configurations for Kafka sink.

4. After editing, click the **Action... > Resume**  to resume the corresponding Changefeed.

## Query TiCDC RCUs

1. Navigate to the **Changefeed** tab of a cluster.
2. You can see the current TiCDC Replication Capacity Units (RCUs) in the upper-right corner of the page.

To learn the billing for changefeeds in TiDB Cloud, see [Changefeed billing](/tidb-cloud/tidb-cloud-billing-ticdc-rcu.md).
