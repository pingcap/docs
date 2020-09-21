---
title: TiDB  Roadmap
category: Roadmap
aliases: ['/docs/ROADMAP/','/docs/roadmap/']
---

<!-- markdownlint-disable MD001 -->

# TiDB Roadmap

## Improve System Stability

- [ ] [Create binding for `update`/`delete`/`insert` queries](https://github.com/pingcap/tidb/issues/15827).
- [ ] [Optimize transaction commits to avoid them failed caused by DDL execution](https://github.com/pingcap/tidb/issues/18098).
- [ ] [Reduce latency jitter](https://github.com/pingcap/tidb/issues/18005).

## Improve System Performance and Reduce Latency

- [ ] [Optimize the performance and efficiency of bulk deletion](https://github.com/pingcap/tidb/issues/18028).
- [ ] [Improve Memory Management](https://github.com/pingcap/tidb/issues/17479).
- [ ] [Improve the Accuracy and Robustness of Index Selection](https://github.com/pingcap/tidb/issues/18065).
- [ ] [Improve partition pruning and data access performance on the partition table](https://github.com/pingcap/tidb/issues/18016).
- [ ] [Async Commit means the writing statement can return to the client ASAP the prewrite stage finished,Reduces system latency](https://github.com/tikv/tikv/issues/8316).
- [ ] [Clustered Index](https://github.com/pingcap/tidb/issues/4841).
- [ ] [Support Cross-Region Deployment & Geo-Partition](https://github.com/pingcap/tidb/issues/18273).

## Improve System Security

### Authentication

- [ ] [Transport Layer Security(TLS) for TiFlash](https://github.com/pingcap/tidb/issues/18080).
- [ ] [TLS in the internal communication of TiDB cluster](https://github.com/pingcap/tiup/issues/529).
- [ ] [SSH LDAP extension for TiUP](https://github.com/pingcap/tiup/issues/528).

### Transparent Data Encryption(TDE)

- [ ] [Transparent Data Encryption(TDE) for TiFlash](https://github.com/pingcap/tidb/issues/18082).
- [ ] [Transparent Data Encryption(TDE) for PD](https://github.com/pingcap/tidb/issues/18262).

### Mask

- [ ] [De-Sensitization TiDB General Log](https://github.com/pingcap/tidb/issues/18034).

## Cost-Effective

- [ ] [Optimize the performance and stability of TiDB running on AWS i3.xlarge/i3.2xlarge](https://github.com/pingcap/tidb/issues/18025).
- [ ] [Optimize the performance and stability of TiDB running on No-NVME SSD or Cloud disk (like AWS EBS gp2)].
- [ ] [Easier discover performance issues and diagnose causes](https://github.com/pingcap/tidb/issues/18867).

## New Feature

- [ ] [Point-in-Time Recovery](https://github.com/pingcap/br/issues/325).
- [ ] [Changing Column Types](https://github.com/pingcap/tidb/issues/17526).
- [ ] [Support collation `utf8mb4_unicode_ci` and `utf8_unicode_ci`](https://github.com/pingcap/tidb/issues/17596).
- [ ] [Make TiCDC a complete alternative to TiDB-Binlog.
    - [ ] Support distinguish update and insert in a row changed event](https://github.com/pingcap/ticdc/issues/690).
    - [ ] Support to provide old values in the row changed event, including old values in delete or update SQL.
- [ ] [snapshot level consistent replication in disasters](https://github.com/pingcap/ticdc/issues/691)
    - [ ] Support MySQL sink can replicate to a snapshot level consistent state when upstream meets a disaster.
- [ ] [Management TiCDC by API](https://github.com/pingcap/ticdc/issues/736).
- [ ] [SQL based import command](https://github.com/pingcap/tidb/issues/18089).
- [ ] [Support Avro sink and make TiCDC compatible with Kafka connect](https://github.com/pingcap/ticdc/issues/660).
- [ ] [Support Spark-3.0](https://github.com/pingcap/tispark/issues/1173).
- [ ] [Support `EXCEPT`/`INTERSECT` Operators](https://github.com/pingcap/tidb/issues/18031).
- [ ] [TiUP/Operator deployment and management DM 2.0](https://github.com/pingcap/tidb-operator/issues/2868).
- [ ] [TiDB Operator supports heterogeneous design](https://github.com/pingcap/tidb-operator/issues/2240).
- [ ] [Support the migration of RDS (for example: MySQL/Aurora) on the cloud to TiDB](https://github.com/pingcap/tidb/issues/18629).
