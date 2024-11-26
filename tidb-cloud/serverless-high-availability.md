---
title: High Availability in TiDB Cloud Serverless
summary: Learn about the high availability architecture of TiDB Cloud Serverless. Discover Zonal and Regional High Availability options, automated backups, failover processes, and how TiDB ensures data durability and business continuity.
---

# High Availability in TiDB Cloud Serverless

TiDB Cloud Serverless is designed with robust mechanisms to maintain high availability and data durability by default, preventing single points of failure and ensuring continuous service even in the face of disruptions. As a fully managed service based on the battle-tested TiDB Open Source product, it inherits TiDB's core high availability (HA) features and augments them with additional cloud-native capabilities.

## Overview

TiDB ensures high availability and data durability using the Raft consensus algorithm. This algorithm consistently replicates data changes across multiple nodes, allowing TiDB to handle read and write requests even in the event of node failures or network partitions. This approach provides both high data durability and fault tolerance.

TiDB Cloud Serverless extends these capabilities with two types of high availability to meet different operational requirements:

- **Zonal high availability (default)**: This option places all nodes within a single availability zone, reducing network latency. It ensures high availability without requiring application-level redundancy across zones, making it suitable for applications that prioritize low latency within a single zone. Zonal high availability is available in all regions that support TiDB Cloud Serverless. For more information, see [Zonal high availability architecture](#zonal-high-availability-architecture).

- **Regional high availability (beta)**: This option distributes nodes across multiple availability zones, offering maximum infrastructure isolation and redundancy. It provides the highest level of availability but requires application-level redundancy across zones. It is recommended to choose this option if you need maximum availability protection against infrastructure failures within a zone. Note that it increases latency and might incur cross-zone data transfer fees. This feature is available in selected regions with multi-availability zone support and can only be enabled during cluster creation. For more information, see [Regional high availability architecture](#regional-high-availability-architecture).

## Zonal high availability architecture

> **Note:**
>
> Zonal high availability is the default option and is available in all AWS regions that support TiDB Cloud Serverless.

When you create a cluster with the default zonal high availability, all components, including Gateway, TiDB, TiKV, and TiFlash compute/write nodes, run in the same availability zone. The placement of these components in the data plane offer infrastructure redundancy with virtual machine pools, which minimizes failover time and network latency due to colocation.

![TiDB Cloud Serverless zonal high availability](/media/tidb-cloud/serverless-zonal-high-avaliability-aws.png)

In zonal high availability architecture:

- The Placement Driver (PD) is deployed across multiple availability zones, ensuring high availability by replicating data redundantly across zones.
- Data is replicated across TiKV servers and TiFlash write nodes within the local availability zone.
- TiDB servers and TiFlash compute nodes read from and write to TiKV and TiFlash write nodes, which are safeguarded by storage-level replication.

### Failover process

TiDB Cloud Serverless ensures a transparent failover process for your applications. During a failover:

- A new replica is created to replace the failed one.

- Servers providing storage services recover local caches from persisted data on Amazon S3, restoring the system to a consistent state with the replicas.

In the storage layer, persisted data is regularly pushed to Amazon S3 for high durability. Moreover, immediate updates are not only replicated across multiple TiKV servers but also stored on the EBS of each server, which further replicates the data for additional durability. TiDB automatically resolves issues by backing off and retrying in milliseconds, ensuring the failover process remains seamless for client applications.

The gateway and computing layers are stateless, so failover involves restarting them elsewhere immediately. Applications should implement retry logic for their connections. While the zonal setup provides high availability, it cannot handle an entire zone failure. If the zone becomes unavailable, downtime will occur until the zone and its dependent services are restored.

## Regional high availability architecture

When you create a cluster with regional high availability, critical OLTP (Online Transactional Processing) workload components, such as PD and TiKV, are deployed across multiple availability zones to ensure redundant replication and maximizing availability. During normal operations, components like Gateway, TiDB, and TiFlash compute/write nodes are hosted in the primary availability zone. These components in data plane offer infrastructure redundancy through virtual machine pools, which minimizes failover time and network latency due to colocation.

> **Note:**
>
> - Regional high availability is currently in beta and only available in the AWS Tokyo (`ap-northeast-1`) region.
> - You can enable regional high availability only during cluster creation.

![TiDB Cloud Serverless regional high availability](/media/tidb-cloud/serverless-regional-high-avaliability-aws.png)

In regional high availability architecture:

- The Placement Driver (PD) and TiKV are deployed across multiple availability zones, and data is always replicated redundantly across zones to ensure the highest level of availability.
- Data is replicated across TiFlash write nodes within the primary availability zone.
- TiDB servers and TiFlash compute nodes read from and write to these TiKV and TiFlash write nodes, which are safeguarded by storage-level replication.

### Failover process

In the rare event of a primary zone failure scenario, which could be caused by a natural disaster, configuration change, software issue, or hardware failure, critical OLTP workload components, including Gateway and TiDB, are automatically launched in the standby availability zone. Traffic is automatically redirected to the standby zone to ensure swift recovery and maintain business continuity.

TiDB Cloud Serverless minimizes service disruption and ensures business continuity during a primary zone failure by performing the following actions:

- Automatically create new replicas of Gateway and TiDB in the standby availability zone.
- Use the elastic load balancer to detect active gateway replicas in the standby availability zone and redirect OLTP traffic from the failed primary zone.

In addition to providing high availability through TiKV replication, TiKV instances are deployed and configured to place each data replica in a different availability zone. The system remains available as long as two availability zones are operating normally. For high durability, data persistence is ensured by regularly backing up data to S3. Even if two zones fail, data stored in S3 remains accessible and recoverable.

Applications are unaffected by failures in non-primary zones and remain unaware of such events. During a primary zone failure, Gateway and TiDB are launched in the standby availability zone to handle workloads. Ensure that your applications implement retry logic to redirect new requests to active servers in the standby availability zone.

## Automatic backups and durability

Database backups are essential for business continuity and disaster recovery, helping to protect your data from corruption or accidental deletion. With backups, you can restore your database to a specific point in time within the retention period, minimizing data loss and downtime.

TiDB Cloud Serverless provides robust automated backup mechanisms to ensure continuous data protection:

- **Daily full backups**: A full backup of your database is created once a day, capturing the entire database state.
- **Continuous transaction log backups**: Transaction logs are backed up continuously, approximately every 5 minutes, though the exact frequency depends on database activity.

These automated backups enable you to restore your database either from a full backup or from a specific point in time by combining full backups with continuous transaction logs. This flexibility ensures that you can recover your database to a precise point just before an incident occurs.

> **Note:**
>
> Automatic backups, including snapshot-based and continuous backups for Point-in-Time Recovery (PITR), are performed on Amazon S3, which provides regional-level high durability.

## Impact on sessions during failures

During a failure, ongoing transactions on the failed server might be interrupted. Although failover is transparent to applications, you must implement logic to handle recoverable failures during active transactions. Different failure scenarios are handled as follows:

- **TiDB failures**: If a TiDB instance fails, client connections are unaffected because TiDB Cloud Serverless automatically reroutes traffic through the gateway. While transactions on the failed TiDB instance might be interrupted, the system ensures that committed data is preserved, and new transactions are handled by another available TiDB instance.
- **Gateway failures**: If the Gateway fails, client connections are disrupted. However, TiDB Cloud Serverless gateways are stateless and can restart immediately in a new zone or server. Traffic is automatically redirected to the new gateway, minimizing downtime.

It is recommended to implement retry logic in your application to handle recoverable failures. For implementation details, refer to your driver or ORM documentation (for example, [JDBC](https://dev.mysql.com/doc/connector-j/en/connector-j-config-failover.html)).

## RTO and RPO

When creating your business continuity plan, consider these two key metrics:

- Recovery Time Objective (RTO): The maximum acceptable time it takes for the application to fully recover after a disruptive event.
- Recovery Point Objective (RPO): The maximum acceptable time interval of recent data updates that the application can tolerate losing during recovery from an unplanned disruptive event.

The following table compares the RTO and RPO for each high availability option:

| High availability architecture | RTO (downtime)                | RPO (data loss) |
|--------------------------------|-------------------------------|-----------------|
| Zonal high availability                         | Near 0 seconds                      | 0               |
| Regional high availability                      | Typically less than 600 seconds | 0               |
