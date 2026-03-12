---
title: Databend Cloud Architecture
sidebar_label: Architecture
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

![Alt text](@site/static/img/documents/overview/2.png)

<Tabs groupId="databendlay">
<TabItem value="Meta-Service Layer" label="Meta-Service Layer">

The metadata service is a multi-tenant service that stores the metadata of each tenant in Databend Cloud in a highly available Raft cluster. This metadata includes:

- Table schema: including the field structure and storage location information of each table, providing optimization information for query planning and providing transaction atomicity guarantee for the storage layer write;
- Cluster management: When the cluster of each tenant starts, multiple instances within the cluster will be registered as metadata and provide health checks for the instances to ensure the overall health of the cluster;
- Security management: saves user, role, and permission-granting information to ensure the security and reliability of data access authentication and authorization processes.

</TabItem>
<TabItem value="Compute Layer" label="Compute Layer">

The architecture of complete separation of storage and compute gives Databend Cloud a unique computational elasticity.

Each tenant in Databend Cloud can have multiple compute clusters (Warehouse), each with exclusive computing resources, and can automatically release them when inactive for more than 1 minute to reduce usage costs.

In the compute cluster, queries are executed through the high-performance Databend engine. Each query will go through multiple different submodules:

- Planner: After parsing the SQL statement, it will combine different operators (such as Projection, Filter, Limit, etc.) into a query plan based on different query types.
- Optimizer: The Databend engine provides a rule-based and cost-based optimizer framework, which implements a series of optimization mechanisms such as predicate pushdown, join reorder, and scan pruning, greatly accelerating queries.
- Processors: Databend implements a push-pull combination of pipeline execution engines. It composes the physical execution of queries into a series of pipelines in the Processor and can dynamically adapt the pipeline configuration based on the runtime information of the query task, combining the vectorized expression calculation framework to maximize the computing power of the CPU.

In addition, Databend Cloud can dynamically increase or decrease nodes in the cluster with the change of query workload, making computing faster and more cost-effective.

</TabItem>
<TabItem value="Storage Layer" label="Storage Layer">

The storage layer of Databend Cloud is based on FuseEngine, which is designed and optimized for inexpensive object storage. FuseEngine efficiently organizes data based on the properties of object storage, allowing for high-throughput data ingestion and retrieval.

FuseEngine compresses data in a columnar format and stores it in object storage, which significantly reduces the data volume and storage costs.

In addition to storing data files, FuseEngine also generates index information, including MinMax index, Bloomfilter index, and others. These indexes reduce IO and CPU consumption during query execution, greatly improving query performance.

</TabItem>
</Tabs>
