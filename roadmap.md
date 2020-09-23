---
title: TiDB Roadmap
aliases: ['/docs/ROADMAP/','/docs/roadmap/']
---

<!-- markdownlint-disable MD001 -->

# TiDB Roadmap

## Improve system stability

- [ ] [Create bindings for `UPDATE`/`DELETE`/`INSERT` queries](https://github.com/pingcap/tidb/issues/15827).
- [ ] [Optimize transaction commits to avoid commit failures caused by DDL execution](https://github.com/pingcap/tidb/issues/18098).
- [ ] [Reduce latency jitter](https://github.com/pingcap/tidb/issues/18005).

## Improve system performance and reduce latency

- [ ] [Optimize the performance and efficiency of bulk deletion](https://github.com/pingcap/tidb/issues/18028).
- [ ] [Improve memory management](https://github.com/pingcap/tidb/issues/17479).
- [ ] [Improve the accuracy and robustness of index selection](https://github.com/pingcap/tidb/issues/18065).
- [ ] [Improve the performance of partition pruning and data access on the partitioned table](https://github.com/pingcap/tidb/issues/18016).
- [ ] [Async Commit](https://github.com/tikv/tikv/issues/8316). This feature means that the statement being written can return to the client as soon as possible after the prewrite stage finishes, which reduces system latency.
- [ ] [Clustered index](https://github.com/pingcap/tidb/issues/4841).
- [ ] [Support cross-region deployment and geo-partition](https://github.com/pingcap/tidb/issues/18273).

## Improve system security

### Authentication

- [ ] [Transport Layer Security (TLS) for TiFlash](https://github.com/pingcap/tidb/issues/18080).
- [ ] [TLS for internal communication in the TiDB cluster](https://github.com/pingcap/tiup/issues/529).
- [ ] [SSH LDAP extension for TiUP](https://github.com/pingcap/tiup/issues/528).

### Transparent Data Encryption (TDE)

- [ ] [Transparent Data Encryption (TDE) for TiFlash](https://github.com/pingcap/tidb/issues/18082).
- [ ] [TDE for PD](https://github.com/pingcap/tidb/issues/18262).

### Mask

- [ ] [Desensitize the TiDB general log](https://github.com/pingcap/tidb/issues/18034).

## Cost-effectiveness

- [ ] [Optimize the performance and stability of TiDB running on AWS i3.xlarge/i3.2xlarge](https://github.com/pingcap/tidb/issues/18025).
- [ ] [Optimize the performance and stability of TiDB running on non-NVMe SSD or on cloud disk (such as AWS EBS gp2)](https://github.com/pingcap/tidb/issues/18024).

## New features

- [ ] [Point-in-time recovery](https://github.com/pingcap/br/issues/325).
- [ ] [Change column types](https://github.com/pingcap/tidb/issues/17526).
- [ ] [Easier to discover performance issues and diagnose the causes](https://github.com/pingcap/tidb/issues/18867).
- [ ] [Support the collations of `utf8mb4_unicode_ci` and `utf8_unicode_ci`](https://github.com/pingcap/tidb/issues/17596).
- [ ] [Make TiCDC a complete alternative to TiDB Binlog](https://github.com/pingcap/ticdc/issues/690)
    - [ ] Support distinguishing `UPDATE` and `INSERT` in a row changed event.
    - [ ] Support providing old values in the row changed event, including old values before the `DELETE` or `UPDATE` execution.
- [ ] [Support snapshot-level consistent replication for disaster recovery](https://github.com/pingcap/ticdc/issues/691)
    - [ ] Support MySQL sink in replicating the upstream to a snapshot-level consistent state when the upstream meets a disaster.
- [ ] [Manage TiCDC using API](https://github.com/pingcap/ticdc/issues/736).
- [ ] [Support the SQL-based `import` command](https://github.com/pingcap/tidb/issues/18089).
- [ ] [Support Avro sink and make TiCDC compatible with Kafka connect](https://github.com/pingcap/ticdc/issues/660).
- [ ] [Support Spark 3.0](https://github.com/pingcap/tispark/issues/1173).
- [ ] [Support `EXCEPT`/`INTERSECT` operators](https://github.com/pingcap/tidb/issues/18031).
- [ ] [Deploy and manage DM 2.0 using TiUP/TiDB Operator](https://github.com/pingcap/tidb-operator/issues/2868).
- [ ] [TiDB Operator supports heterogeneous design](https://github.com/pingcap/tidb-operator/issues/2240).
- [ ] [Support migrating the RDS (such as MySQL/Aurora) on cloud to TiDB](https://github.com/pingcap/tidb/issues/18629).
