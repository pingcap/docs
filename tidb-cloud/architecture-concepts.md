---
title: Architecture
summary: Learn about architecture concepts for TiDB Cloud.
---

# Architecture

TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) that brings the flexibility and power of [TiDB](https://docs.pingcap.com/tidb/stable/overview), an open-source HTAP (Hybrid Transactional and Analytical Processing) database, to Google Cloud and AWS.

TiDB is MySQL-compatible, making it easy to migrate and work with existing applications, while offering seamless scalability to handle everything from small workloads to massive, high-performance clusters. It supports both transactional (OLTP) and analytical (OLAP) workloads in one system, simplifying operations and enabling real-time insights.

TiDB Cloud provides two deployment options: **TiDB Cloud** **Serverless**, for auto-scaling, cost-efficient workloads, and **TiDB Cloud Dedicated**, for enterprise-grade applications with dedicated resources and advanced capabilities. TiDB Cloud makes it easy to scale your database, handle complex management tasks, and stay focused on developing reliable, high-performing applications.

## TiDB Cloud Serverless

TiDB Cloud Serverless is a fully managed serverless solution that provides HTAP capabilities similar to traditional TiDB, while offering auto-scaling to alleviate users' burdens related to capacity planning and management complexities. It includes a free tier for basic usage, with consumption-based billing for any usage that exceeds the free limits. TiDB Cloud Serverless offers two types of high availability to address varying operational requirements.

By default, clusters utilizing the Zonal High Availability option have all components located within the same availability zone, which results in lower network latency.

![TiDB Cloud Serverless zonal high availability](/media/tidb-cloud/serverless-zonal-high-avaliability-aws.png)

For applications that require maximum infrastructure isolation and redundancy, the Regional High Availability option distributes nodes across multiple availability zones.

![TiDB Cloud Serverless regional high availability](/media/tidb-cloud/serverless-regional-high-avaliability-aws.png)

## TiDB Cloud Dedicated

TiDB Cloud Dedicated is designed for mission-critical businesses, offering high availability across multiple availability zones, horizontal scaling, and full HTAP capabilities.

Built on isolated cloud resources such as VPCs, VMs, managed Kubernetes services, and cloud storage, it leverages the infrastructure of major cloud providers. TiDB Cloud Dedicated clusters support the complete TiDB feature set, enabling rapid scaling, reliable backups, deployment within specific VPCs, and geographic-level disaster recovery.

![TiDB Cloud Dedicated Architecture](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloud console

The [TiDB Cloud console](https://tidbcloud.com/) is the web-based management interface for both TiDB Cloud Serverless and TiDB Cloud Dedicated. It provides tools to manage clusters, import or migrate data, monitor performance metrics, configure backups, set up security controls, and integrate with other cloud services, all from a single, user-friendly platform.

## TiDB Cloud CLI

The TiDB Cloud CLI, `ticloud`, allows you to manage TiDB Cloud Serverless and TiDB Cloud Dedicated directly from your terminal with simple commands. You can perform tasks such as:

- Creating, deleting, and listing clusters.
- Importing data into clusters.
- Exporting data from clusters.

For more information, see [TiDB Cloud CLI Reference](/tidb-cloud/cli-reference.md).

## TiDB Cloud API

The TiDB Cloud API is a REST-based interface that provides programmatic access to manage resources across TiDB Cloud Serverless and TiDB Cloud Dedicated. It enables automated and efficient handling of tasks such as managing projects, clusters, backups, restores, data imports, billing, and other resources in [TiDB Cloud Data Service](/tidb-cloud/data-service-overview.md).

For more information, see [TiDB Cloud API Overview](/tidb-cloud/api-overview.md).

## Nodes

In TiDB Cloud, each cluster consists of TiDB, TiKV, and TiFlash nodes.

- In a TiDB Cloud Dedicated cluster, you can fully manage the number and size of your dedicated TiDB, TiKV, and TiFlash nodes according to your performance requirements. For more information, see [Scalability](/tidb-cloud/scalability-concepts.md).
- In a TiDB Cloud Serverless cluster, the number and size of TiDB, TiKV, and TiFlash nodes are automatically managed. This ensures seamless scaling, eliminating the need for users to handle node configuration or management tasks.

### TiDB node

A [TiDB node](/tidb-computing.md) is a stateless SQL layer that connects to applications using a MySQL-compatible endpoint. It handles tasks like parsing, optimizing, and creating distributed execution plans for SQL queries.

You can deploy multiple TiDB nodes to scale horizontally and manage higher workloads. These nodes work with load balancers, such as TiProxy or HAProxy, to provide a seamless interface. TiDB nodes do not store data themselves---they forward data requests to TiKV nodes for row-based storage or TiFlash nodes for columnar storage.

### TiKV node

A [TiKV node](/tikv-overview.md) is the backbone of data storage in the TiDB architecture, serving as a distributed transactional key-value storage engine that delivers reliability, scalability, and high availability.

**Key features:**

- **Region-based data storage**

    - Data is divided into [Regions](https://docs.pingcap.com/tidb/dev/glossary#regionpeerraft-group), each covering a specific Key Range (left-closed, right-open interval: `StartKey` to `EndKey`).
    - Multiple Regions coexist within each TiKV node to ensure efficient data distribution.

- **Transactional support**

    - TiKV nodes provide native distributed transaction support at the key-value level, ensuring Snapshot Isolation as the default isolation level.
    - The TiDB node translates SQL execution plans into calls to the TiKV node API, enabling seamless SQL-level transaction support.

- **High availability**

    - All data in TiKV nodes is replicated (default: three replicas) for durability.
    - TiKV ensures native high availability and supports automatic failover, safeguarding against node failures.

- **Scalability and reliability**

    - TiKV nodes are designed to handle expanding datasets while maintaining distributed consistency and fault tolerance.

### TiFlash node

A [TiFlash node](/tiflash/tiflash-overview.md) is a specialized type of storage node within the TiDB architecture. Unlike ordinary TiKV nodes, TiFlash is designed for analytical acceleration with a columnar storage model.

**Key features:**

- **Columnar storage**

    TiFlash nodes store data in a columnar format, making them optimized for analytical queries and significantly improving performance for read-intensive workloads.

- **Vector search index support**

    The vector search index feature uses TiFlash replicas for tables, enabling advanced search capabilities and improving efficiency in complex analytical scenarios.