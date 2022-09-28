---
title: Data Migration (DM) Best Practices
summary: Learn about best practices when you use TiDB Data Migration (DM) to migrate data.
---

# Data Migration (DM) Best Practices

TiDB Data Migration (DM) is an data migration tool developed by PingCAP. It supports the full data migration and the incremental data replication from MySQL-compatible databases such as MySQL, Percona MySQL, MariaDB, AWS MySQL RDS, AWS Aurora into TiDB.

You can use DM in the following scenarios:

- Perform full and incremental data migration from a single MySQL-compatible database instance to TiDB
- Migrate and merge MySQL shards of small datasets to TiDB
- In the DataHUB scenario, such as the middle platform of business data, and real-time aggregation of business data, use DM as the middleware for data migration

This document introduces how to use DM in an elegant and efficient way, and how to avoid the common mistakes when using DM.

## Performance limitations

| Performance item  | Limitation |
| ----------------- | :--------: |
|  Max Work Nodes              |  1000           |
|  Max Task number             |  600            |
|  Max QPS                     |  30k QPS/worker |
|  Max Binlog throughput       |  20 MB/s/worker |
|  Table number limit per task | Unlimited       |

- DM supports managing 1000 work nodes simultaneously, and the maximum number of tasks is 600. To ensure the high availability of work nodes, you should reserve some work nodes as standby nodes. Reserve 20% to 50% of the number of the work nodes that have run migration task.
- A single work node can theoretically support replication QPS of up to 30K QPS/worker. It varies for different schemas and workloads. The ability to handle upstream binlog is up to 20 MB/s/worker.
- If you use DM as a data replication middleware that will be used for a long time, you need to carefully design the deployment architecture of DM components. For more information, see [Deploy DM-master and DM-woker](#deploy-dm-master-and-dm-woker)

## Before data migration

Before data migration, the design of the overall solution is critical. Especially the design of the scheme before migration is the most important part of the whole scheme. The following sections describe best practices and scenarios from the business side and the implementation side.

### Key points in the business side

To distribute workloads evenly on multiple nodes, the schema design for the distributed database is very different from traditonal databases. It is disgned for both low migration cost and logic correctness after migration. The following sections describe best practices before data migration.

#### Business impact of AUTO_INCREMENT in Schema design

TiDB 的 `AUTO_INCREMENT` 与 MySQL 的 `AUTO_INCREMENT` 整体上看是相互兼容的。但因为 TiDB 作为分布式数据库，一般会有多个计算节点（client 端入口），应用数据写入时会将负载均分开，这就导致在有 `AUTO_INCREMENT` 列的表上，可能出现不连续的自增 ID。详细原理参考 [`AUTO_INCREMENT`](/auto-increment.md#实现原理)。

如果业务对自增 ID 有强依赖，可以考虑使用 [SEQUENCE 函数](/sql-statements/sql-statement-create-sequence.md#sequence-函数)。

In general, `AUTO_INCREMENT` in TiDB is compatible 

### Best practices for deployment

#### Deploy DM-master and DM-woker