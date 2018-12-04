---
title: TiDB Introduction
summary: An introduction to the TiDB database platform
category: introduction
---

# TiDB Introduction

TiDB (The pronunciation is: /'taɪdiːbi:/ tai-D-B, etymology: titanium) is an open-source distributed scalable Hybrid Transactional and Analytical Processing (HTAP) database. It features horizontal scalability, strong consistency, and high availability. TiDB is MySQL compatible and serves as a one-stop data warehouse for both OLTP (Online Transactional Processing) and OLAP (Online Analytical Processing) workloads.

- __Horizontal scalability__

    TiDB scales horizontally by simply adding new nodes and there's no sharding required.

- __MySQL compatibility__

    Use TiDB without changing a single line of MySQL application code in most cases and still benefit from the MySQL ecosystem.

- __Distributed transactions__

    TiDB guarantees ACID compliance.

- __Cloud Native__

    TiDB is designed to work in the cloud -- public, private, or hybrid -- making deployment, provisioning, and maintenance drop-dead simple.

- __Minimize ETL__

    TiDB's hybrid OLTP/OLAP architecture means you can start performing analytical workloads without creating an ETL (Extract, Transform and Load) process.

- __High availability__

    TiDB is designed for fault tolerance by using a layered architecture and the Raft protocol.

TiDB is designed to support both OLTP and OLAP scenarios. For complex OLAP scenarios, use [TiSpark](tispark/tispark-user-guide.md).

Read the following three articles to understand TiDB techniques:

- [Data Storage](https://pingcap.github.io/blog/2017/07/11/tidbinternal1/)
- [Computing](https://pingcap.github.io/blog/2017/07/11/tidbinternal2/)
- [Scheduling](https://pingcap.github.io/blog/2017/07/20/tidbinternal3/)
