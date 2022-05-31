---
title: TiDB Cloud Replication
summary: Learn how to create a replica to stream data from a primary TiDB cluster to a secondary TiDB cluster.
---

# TiDB Cloud Replication

TiDB Cloud Replication is a feature that allows you to create a continuously replicated readable secondary TiDB cluster for a primary TiDB cluster in TiDB Cloud. This readable secondary cluster (also known as cross-region replication, secondary replication, or geo-replication) can be in the same region as the primary TiDB cluster, or more commonly, in a different region.

With TiDB Cloud Replication, you can perform quick disaster recovery of a database in the event of a regional disaster or large-scale failure, which helps achieve business continuity. Once a secondary cluster is set up, you can manually initiate geographic failover to the secondary cluster in a different region.

> **Warning:**
>
> Currently, the **TiDB Cloud Replication** feature is in **Public Preview** with the following limitations:
>
> * One primary cluster can only have one replication.
> * You cannot use a secondary cluster as a source of **TiDB Cloud Replication** to another cluster.
> * **TiDB Cloud Replication** contradicts **Sink to Apache Kafka**](/tidb-cloud/changefeed-sink-to-apache-kafka.md) and [**Sink to MySQL**](/tidb-cloud/changefeed-sink-to-mysql.md). When **TiDB Cloud Replication** is enabled, neither the primary nor the secondary cluster can use **Sink to Apache Kafka** or **Sink to MySQL** changefeed and vice versa.
> * Because TiDB Cloud uses TiCDC to establish replication, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions).

To support application replication, you must deploy your applications in both primary and secondary regions, and ensure that each application is connected to the TiDB cluster in the same region. The applications in the secondary region are on standby. When the primary region fails, you can initiate a "Detach" operation to make the TiDB cluster in the secondary region active, and then transfer all data traffic to the applications in the secondary region.

The following diagram illustrates a typical deployment of a geo-redundant cloud application using TiDB Cloud Replication:

<!-- https://www.figma.com/file/DaevXzW4aq35QodwZEkcTS/DBaaS-Architecture-Chart-(high-level)-(Copy)?node-id=0%3A1 -->
![TiDB Cloud Replication](/media/tidb-cloud/changefeed-replication-deployment.png)

Creating a secondary TiDB cluster is only a part of the business continuity solution. To recover an application (or service) end-to-end after a catastrophic failure, you also need to ensure that all components and dependent services of the application can be restored.

- Check whether each component of the application is resilient to the same failures and become available within recovery time objective (RTO) of your application. The typical components of an application include client software (such as browsers with custom JavaScript), web front ends, storage, and DNS.
- Identify all dependent services, check the guarantees and capabilities of these services, and ensure that your application is operational during a failover of these services.

## Terminology and capabilities of TiDB Cloud Replication

### Automatic asynchronous replication

Only one secondary cluster can be created for each Primary TiDB cluster. TiDB Cloud makes a full Backup for the primary TiDB cluster, then restore to the newly created secondary cluster which means all existing data is included in the secondary cluster. After the secondary cluster is created, all data changes on the primary cluster will be replicated asynchronously to the secondary cluster.

### Readable secondary cluster

The secondary cluster is opened in read-only mode, you can distribute your read-only workload with low real-time data requirements to the secondary cluster.

To satisfy read-intensive scenarios in the same region, you can use **TiDB Cloud Replication** to create a readable secondary cluster in the same region as the primary cluster. However, because a secondary cluster in the same region does not provide additional resiliency for large-scale outages or catastrophic failures, do not use it as a failover target for regional disaster recovery purposes.

### Planned Detach

**Planned Detach** can be trigged by you manually. It is used for planned maintenance in most cases, such as disaster recovery drills. **Planned detach** makes sure all data changes are replicated to the secondary cluster and no data loss (RPO=0). For RTO, it depends on the replication lag between primary and secondary clusters. In most cases, the RTO is minutes level.

**Planned Detach** detaches the secondary cluster from the primary cluster into an individual cluster. When **Planned Detach** is triggered, it performs the following steps:

1. Sets the primary cluster as read-only, to prevent any new transaction from being committed to the primary cluster.
2. Waits until the secondary cluster is fully synced with the primary cluster.
3. Stops the replication from the primary to the secondary cluster.
4. Sets the original secondary cluster as writable, which makes it available to serve your business.

After **Planned Detach** is finished, the original primary cluster is set as read-only. If you still need to write to the original primary cluster, you can do one of the following to set the cluster as writable explicitly:

- Go to the cluster details page, click **Settings**, and then click the **Make Writable** drop-down button.
- Connect to the SQL port of the original primary cluster and execute the following statement:

{{< copyable "sql" >}}

```sql
set global tidb_super_read_only=OFF;
```

### Force Detach

To recover from an unplanned outage, use **Force Detach**. In the event of a catastrophic failure in the region where the primary cluster is located, you should use **Force Detach** so that the secondary cluster can serve the business as quickly as possible, ensuring business continuity. Because this operation makes the secondary cluster serve as an individual cluster immediately and does not wait for any unreplicated data, the RPO depends on the Primary-Secondary replication lag, while the RTO depends on how quickly **Force Detach** is triggered by you.

**Force Detach** detaches the secondary cluster from the primary cluster into an individual cluster. When **Force Detach** is triggered, it performs the following steps：

1. Stops data replication from the primary to the secondary cluster immediately.
2. Sets the original secondary cluster as writable so that it can start to serve your workload.
3. If the old primary cluster is still reachable, or when the original primary cluster recovers, TiDB Cloud sets it as read-only to avoid any new transaction from being committed to it.

If the original primary cluster is recovered from the outage, you still have the opportunity to review transactions that would have been executed in the original primary cluster but not in the original secondary cluster by comparing the data in the two clusters, and decide whether to manually replicate these unsynchronized transactions to the original secondary cluster based on your business situation.

The data replication topology between primary and secondary clusters does not exist anymore after you detached the secondary cluster. The original primary cluster is set to read-only mode and the original secondary cluster becomes writable. You need to disable read-only mode manually on the original primary cluster if any DML/DDL is planned to run on it. If you want to disable the read-only mode on the original primary, do one of the following:

- Go to the cluster details page, click **Settings**, and then click the **Make Writable** drop-down button.
- Connect to the SQL port of the original primary cluster and execute the following statement:

{{< copyable "sql" >}}

```sql
set global tidb_super_read_only=OFF;
```

## Configure TiDB Cloud Replication

To configure TiDB Cloud Replication, do the following:

1. Navigate to the **Changefeed** tab of your TiDB cluster.
2. Click **Create a replica of your TiDB Cluster**.
3. Fill in the username and password of your database.
4. Choose the region of the secondary cluster.
5. Click **Create**. After a while, the sink will begin its work, and the status of the sink will be changed to "**Producing**".

To trigger a **Planned Detach** or **Force Detach**, do the following:

1. Navigate to the **Changefeed** tab of your TiDB cluster.
2. Click **Create a replica of your TiDB Cluster**.
3. Click **Planned Detach** or **Force Detach**.

## Scale the primary cluster

You can scale out or scale in the primary cluster without disconnecting the secondary cluster. When the primary cluster is scaled, the secondary cluster follows the same scaling automatically.

## Monitor the primary-secondary lag

To monitor lag concerning the RPO, do the following:

1. Navigate to the **Changefeed** tab of your TiDB cluster.
2. Click **Create a replica of your TiDB Cluster**.
3. You can see the lag of the primary-secondary cluster.
