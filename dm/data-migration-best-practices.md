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

- DM 支持同时管理 1000 个同步节点（Work Node），最大同步任务数量为 600 个。为了保证同步节点的高可用，应预留一部分 Work Node 节点作为备用节点，保证数据同步的高可用。预留已开启同步任务 Work Node 数量的 20% ~ 50%。
- 单机部署 Work Node 数量。在服务器配置较好情况下，要保证每个 Work Node 至少有 2 核 CPU 加 4G 内存的可用工作资源，并且应为主机预留 10% ~ 20% 的系统资源。
- 单个同步节点（Work Node），理论最大同步 QPS 在 30K QPS/worker（不同 Schema 和 workload 会有所差异），处理上游 Binlog 的能力最高为 20 MB/s/worker。
- 如果将 DM 作为需要长期使用的数据同步中间件，需要注意 DM 组件的部署架构。请参见 [Master 与 Woker 部署实践](#master-与-woker-部署实践)。
