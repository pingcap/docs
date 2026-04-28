---
title: Architecture
summary: Learn about architecture concepts for TiDB Cloud.
---

# Architecture

<CustomContent language="en,zh">

TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) that brings the flexibility and power of [TiDB](https://docs.pingcap.com/tidb/stable/overview), an open-source HTAP (Hybrid Transactional and Analytical Processing) database, to Amazon Web Services (AWS), Google Cloud, Microsoft Azure, and Alibaba Cloud.

</CustomContent>

<CustomContent language="ja">

TiDB Cloud is a fully-managed Database-as-a-Service (DBaaS) that brings the flexibility and power of [TiDB](https://docs.pingcap.com/tidb/stable/overview), an open-source HTAP (Hybrid Transactional and Analytical Processing) database, to Amazon Web Services (AWS), Google Cloud, and Microsoft Azure.

</CustomContent>

TiDB is MySQL-compatible, making it easy to migrate and work with existing applications, while offering seamless scalability to handle everything from small workloads to massive, high-performance systems. It supports both transactional (OLTP) and analytical (OLAP) workloads in one system, simplifying operations and enabling real-time insights.

TiDB Cloud makes it easy to scale your database, handle complex management tasks, and stay focused on developing reliable, high-performing applications.

<CustomContent language="en,zh">

- For AWS, TiDB Cloud provides **{{{ .starter }}}** for auto-scaling, cost-efficient workloads, **{{{ .essential }}}** for production-ready workloads with provisioned capacity, and **{{{ .dedicated }}}** for enterprise-grade applications with dedicated resources and advanced capabilities.
- For Google Cloud and Azure, TiDB Cloud provides **{{{ .dedicated }}}** for enterprise-grade applications with dedicated resources and advanced capabilities.
- For Alibaba Cloud, TiDB Cloud provides **{{{ .starter }}}** for auto-scaling, cost-efficient workloads and **{{{ .essential }}}** for production-ready workloads with provisioned capacity.

</CustomContent>

<CustomContent language="ja">

- For AWS, TiDB Cloud provides **{{{ .starter }}}** for auto-scaling, cost-efficient workloads, **{{{ .essential }}}** for production-ready workloads with provisioned capacity, and **{{{ .dedicated }}}** for enterprise-grade applications with dedicated resources and advanced capabilities.
- For Google Cloud and Azure, TiDB Cloud provides **{{{ .dedicated }}}** for enterprise-grade applications with dedicated resources and advanced capabilities.

</CustomContent>

## {{{ .starter }}}

{{{ .starter }}} is a fully managed, multi-tenant TiDB offering. It delivers an instant, autoscaling MySQL-compatible database.

The Starter plan is ideal for those who are getting started with TiDB Cloud. It provides developers and small teams with the following features:

- **No cost**: This plan is completely free, with no credit card required to get started.
- **Storage**: Provides an initial 5 GiB of row-based storage and 5 GiB of columnar storage.
- **Request Units**: Includes 50 million [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) for database operations.

## {{{ .essential }}}

For applications experiencing growing workloads and needing scalability in real time, the Essential plan provides the flexibility and performance to keep pace with your business growth with the following features:

- **Enhanced capabilities**: includes all capabilities of the Starter plan, along with the capacity to handle larger and more complex workloads, as well as advanced security features.
- **Automatic scaling**: automatically adjusts storage and computing resources to efficiently meet changing workload demands.
- **High availability**: built-in fault tolerance and redundancy ensure your applications remain available and resilient, even during infrastructure failures.
- **Predictable pricing**: billed based on storage and Request Capacity Units (RCUs) of the compute resources, offering transparent, usage-based pricing that scales with your needs, so you only pay for what you use without surprises.

{{{ .essential }}} offers two types of high availability to address varying operational requirements.

- Zonal High Availability: places all components within the same availability zone, which results in lower network latency.
- Regional High Availability: distributes nodes across multiple availability zones, providing maximum infrastructure isolation and redundancy.

For more information, see [High Availability in TiDB Cloud](/tidb-cloud/serverless-high-availability.md).

## {{{ .premium }}}

For mission-critical applications that require the highest level of performance, enhanced security within a managed environment, the Premium plan provides robust infrastructure and advanced controls:

- **Unlimited Growth and Auto-scaling**: Provides seamless scaling capabilities to handle evolving workloads，which ensures continuous reliability for business-critical operations.
- **Performance Optimization**: Specifically tuned for high-throughput and low-latency workloads, offering larger resource ceilings and more granular scaling controls.
- **Pay-as-you-go Pricing**:Billed based on actual Request Capacity Unit (RCU) consumption and storage usage, this flexible pay-as-you-go model eliminates the need for manual backend over-provisioning.
- **Advanced Security**: Offers deeper security configurations and compliance capabilities required by large-scale enterprises and regulated industries.

To ensure maximum uptime and resilience for mission-critical workloads, {{{ .premium }}} exclusively provides **Regional High Availability**. By distributing nodes across multiple availability zones, it offers superior redundancy compared to zonal deployments.

## TiDB Cloud Dedicated

TiDB Cloud Dedicated is designed for mission-critical businesses, offering high availability across multiple availability zones, horizontal scaling, and full HTAP capabilities.

Built on isolated cloud resources such as VPCs, VMs, managed Kubernetes services, and cloud storage, it leverages the infrastructure of major cloud providers. TiDB Cloud Dedicated clusters support the complete TiDB feature set, enabling rapid scaling, reliable backups, deployment within specific VPCs, and geographic-level disaster recovery.

![TiDB Cloud Dedicated Architecture](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloud console

The [TiDB Cloud console](https://tidbcloud.com/) is the web-based management interface for TiDB Cloud resources. It provides tools to manage TiDB Cloud resources, import or migrate data, monitor performance metrics, configure backups, set up security controls, and integrate with other cloud services, all from a single, user-friendly platform.

## TiDB Cloud CLI (Beta)

The TiDB Cloud CLI, `ticloud`, allows you to manage {{{ .starter }}} and Essential instances directly from your terminal with simple commands. You can perform tasks such as:

- Creating, deleting, and listing {{{ .starter }}} and Essential instances.
- Importing data into {{{ .starter }}} and Essential instances.
- Exporting data from {{{ .starter }}} and Essential instances.

For more information, see [TiDB Cloud CLI Reference](/tidb-cloud/cli-reference.md).

## TiDB Cloud API (Beta)

The TiDB Cloud API is a REST-based interface that provides programmatic access to manage resources across {{{ .starter }}} and TiDB Cloud Dedicated. It enables automated and efficient handling of tasks such as managing projects, clusters, backups, restores, data imports, billing, and other resources in [TiDB Cloud Data Service](/tidb-cloud/data-service-overview.md).

For more information, see [TiDB Cloud API Overview](https://docs.pingcap.com/api/tidb-cloud-api-overview).

## Nodes

Nodes are the core components of the TiDB architecture. TiDB nodes, TiKV nodes, and TiFlash nodes work together to process SQL queries, store data, and accelerate analytical workloads.

- In a TiDB Cloud Dedicated cluster, you can fully manage the number and size of your dedicated TiDB, TiKV, and TiFlash nodes according to your performance requirements. For more information, see [Scalability](/tidb-cloud/scalability-concepts.md).
- In a {{{ .starter }}} or {{{ .essential }}} or {{{ .premium }}}instance, the number and size of TiDB, TiKV, and TiFlash nodes are automatically managed. This ensures seamless scaling, eliminating the need for users to handle node configuration or management tasks.

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


## Request Capacity Unit In TiDB Cloud Premium

### What is a Request Capacity Unit (RCU)

A Request Capacity Unit (RCU) is a unit of measure used to represent the provisioned compute capacity for your TiDB Cloud Premium instance. One RCU provides a fixed amount of compute resources that can process a certain number of RUs-per-second. The number of RCUs you provision determines your cluster’s baseline performance and throughput capacity.

1 RCU represents sustained RUs-per-second capacity. A baseline of X RCU entitles the tenant to X RU/s averaged over 1-minute windows (or comply with our minimal calculation window).

### TiDB Cloud Premium RCU Autoscale

When configuring your TiDB Cloud Premium instance, you specify the Maximum RCU ($RCU_{max}$) required for your workload. TiDB Cloud automatically scales the available Request Units ($RCU$) within a range where $0.25 \times RCU_{max} \le RCU \le RCU_{max}$.For example, if you set the maximum throughput to 20,000 RCU, the system will dynamically scale between 5,000 and 20,000 RCU based on real-time demand. This scaling process is automatic and instantaneous, ensuring you can consume up to your Max RCU at any time with no manual intervention or latency delays.

### TiDB Cloud Premium RCU Billing

TiDB Cloud Premium follows a usage-based billing model where you are charged based on the actual Request Units consumed by your workload.

#### Per-Minute Calculation

The system calculates your usage every minute. It measures the total amount of Request Units consumed within that 60-second window and averages it to determine the RCU（RUs-per-second capacity） for that minute. This ensures that your billing accurately reflects real-time traffic fluctuations.

#### Minimum Usage Requirement
To ensure high availability and guarantee that resources are always reserved for your cluster, a Minimum Billing RCU is automatically established based on your Maximum RCU setting. This acts as a baseline for the reserved capacity dedicated to your instance.

If your actual consumption during a minute is lower than this threshold, the billing will default to the Minimum Billing RCU. This mechanism ensures that the system can immediately handle sudden traffic spikes up to your specified maximum without any performance degradation or delays.


### Request Unit In TiDB Cloud Premium
A Request Unit (RU) is a unit of measure used to represent the amount of resources consumed by a single request to the database. The amount of RUs consumed by a request depends on various factors, such as the operation type or the amount of data being retrieved or modified.

TiDB Cloud Premium normalizes the cost of all database operations using **Request Units (RUs)** and measures cost based on throughput (**Request Units per second, RU/s**). By providing a unified metric, TiDB Cloud ensures that your throughput costs are **deterministic and predictable**, allowing you to manage your application cost-effectively.

#### Baseline Performance Examples
To help you estimate your workload, here are some baseline performance examples for common operations. 

| Operation Type | Description | Estimated Cost |
| :--- | :--- | :--- |
| **Point Read** | Reading a 1 KB item by its unique ID | **1.5 RU** |
| **OLTP Write** | Standard Sysbench model (1 KB item size) | **2.5 RU** |

> **Note:** > A **Point Read** is the most efficient way to retrieve data by its unique ID. For **Write Operations**, the RU cost accounts for the I/O and indexing effort required to persist the data. RU consumption scales proportionally with data size and operation complexity.

### Request Unit Considerations
The total RU charge for any given operation is determined by the total **"database effort"** required to execute it. TiDB Cloud calculates this consumption based on four key dimensions:

1. Data Access & Size
* **Read/Write Volume**: RUs scale directly with the size of the data payload. Processing a large 100 KB document will naturally consume more RUs than a 1 KB record.
* **Read/Write Rows**: The number of rows involved in an operation is a primary driver of cost. Even with small payloads, querying or updating a large volume of rows increases total RU consumption, as each row requires individual processing, locking, and validation.
* **Indexing Impact**:
    * **Writes**: Every index on a table must be updated during a write operation. Tables with more indexes will incur higher RU costs for `INSERT`, `UPDATE`, and `DELETE` operations.
    * **Reads**: Conversely, well-designed indexes significantly **reduce Query RUs** by allowing the engine to locate rows efficiently and avoiding the heavy resource cost of full-table scans.

2. Query Complexity
* **Scanning Efficiency**: RU consumption is heavily influenced by how many rows the engine must "touch".
    * **Read Metrics (Estimated Rows)**: A point-read using a primary key is the most efficient operation. Conversely, a query requiring a scan of millions of **estimated rows** will consume significantly more RUs than one utilizing an optimized index.
    * **Write Metrics (Affected Rows)**: The RU cost for data modification is tied to the number of **affected rows**. Modifying 10,000 rows in a single statement will result in a much higher charge than modifying a single row.
* **Computational Logic**: Complex SQL operations—including multiple table joins, deep subqueries, and aggregations—require more "optimizer brainpower" and CPU cycles to calculate the execution path and process the data. 


