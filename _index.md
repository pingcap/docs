---
title: TiDB Introduction
<<<<<<< HEAD
summary: Learn about the NewSQL database TiDB that supports HTAP workloads.
aliases: ['/tidb/v5.0/adopters']
=======
aliases: ["/docs/dev/", "/docs/dev/adopters/", "/tidb/dev/adopters"]
hide_sidebar: true
hide_commit: true
>>>>>>> a90153a8f (tidb: add the latest content for tidb learning path (#9838))
---

<LearningPathContainer platform="tidb" title="TiDB" subTitle="TiDB is an open-source NewSQL database that supports Hybrid Transactional and Analytical Processing (HTAP) workloads. Find the guide, samples, and references you need to use TiDB.">

<LearningPath label="Learn" icon="cloud1">

<<<<<<< HEAD
Designed for the cloud, TiDB provides flexible scalability, reliability and security on the cloud platform. Users can elastically scale TiDB to meet the requirements of their changing workloads. [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/v1.1/tidb-operator-overview) helps manage TiDB on Kubernetes and automates operating tasks, which makes TiDB easier to deploy on any cloud that provides managed Kubernetes. [TiDB Cloud](https://pingcap.com/tidb-cloud/), the fully-managed TiDB service, is the easiest, most economical, and most resilient way to unlock the full power of [TiDB in the cloud](https://docs.pingcap.com/tidbcloud/), allowing you to deploy and run TiDB clusters with just a few clicks.
=======
[What is TiDB](https://docs.pingcap.com/tidb/dev/overview)
>>>>>>> a90153a8f (tidb: add the latest content for tidb learning path (#9838))

[Features](https://docs.pingcap.com/tidb/dev/basic-features)

<<<<<<< HEAD
- [TiDB Introduction](/overview.md)
- [Basic Features](/basic-features.md)
- [What's New in TiDB 5.0](/releases/release-5.0.0.md)
- [Compatibility with MySQL](/mysql-compatibility.md)
- [Usage Limitations](/tidb-limitations.md)
=======
[TiFlash](https://docs.pingcap.com/tidb/dev/tiflash-overview)
>>>>>>> a90153a8f (tidb: add the latest content for tidb learning path (#9838))

</LearningPath>

<LearningPath label="Try" icon="cloud5">

<<<<<<< HEAD
- [Quick Start Guide](/quick-start-with-tidb.md)
- [Explore SQL with TiDB](/basic-sql-operations.md)
=======
[Try Out TiDB](https://docs.pingcap.com/tidb/dev/quick-start-with-tidb)
>>>>>>> a90153a8f (tidb: add the latest content for tidb learning path (#9838))

[Try Out HTAP](https://docs.pingcap.com/tidb/dev/quick-start-with-htap)

[Import Example Database](https://docs.pingcap.com/tidb/dev/import-example-data)

</LearningPath>

<LearningPath label="Develop" icon="doc8">

[Developer Guide Overview](https://docs.pingcap.com/tidb/dev/dev-guide-overview)

<<<<<<< HEAD
- [Migration Overview](/migration-overview.md)
- [Migrate full data from Aurora](/migrate-from-aurora-using-lightning.md)
- [Migrate continuously from Aurora/MySQL Database](/migrate-from-aurora-mysql-database.md)
- [Migrate from CSV Files](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md)
- [Migrate from MySQL SQL Files](/migrate-from-mysql-dumpling-files.md)
=======
[Quick Start](https://docs.pingcap.com/tidb/dev/dev-guide-build-cluster-in-cloud)
>>>>>>> a90153a8f (tidb: add the latest content for tidb learning path (#9838))

[Example Application](https://docs.pingcap.com/tidb/dev/dev-guide-sample-application-spring-boot)

</LearningPath>

<<<<<<< HEAD
- [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md)
- [Scale TiDB Using TiUP](/scale-tidb-using-tiup.md)
- [Back up and Restore Data](/br/backup-and-restore-tool.md)
- [Deploy and Manage TiCDC](/ticdc/manage-ticdc.md)
- [Maintain TiDB Using TiUP](/maintain-tidb-using-tiup.md)
- [Maintain TiFlash](/tiflash/maintain-tiflash.md)
=======
<LearningPath label="Deploy" icon="deploy">
>>>>>>> a90153a8f (tidb: add the latest content for tidb learning path (#9838))

[Software and Hardware Requirements](https://docs.pingcap.com/tidb/dev/hardware-and-software-requirements)

[Deploy a TiDB Cluster Using TiUP (Recommended)](https://docs.pingcap.com/tidb/dev/production-deployment-using-tiup)

[Deploy a TiDB Cluster in Kubernetes](https://docs.pingcap.com/tidb/dev/tidb-in-kubernetes)

</LearningPath>

<LearningPath label="Migrate" icon="cloud3">

[Migration Overview](https://docs.pingcap.com/tidb/dev/migration-overview)

[Migration Tools](https://docs.pingcap.com/tidb/dev/migration-tools)

[Typical Scenarios](https://docs.pingcap.com/tidb/dev/migrate-aurora-to-tidb)

</LearningPath>

<LearningPath label="Maintain" icon="maintain">

[Upgrade a Cluster](https://docs.pingcap.com/tidb/dev/upgrade-tidb-using-tiup)

[Scale a Cluster](https://docs.pingcap.com/tidb/dev/scale-tidb-using-tiup)

[Back Up Cluster Data](https://docs.pingcap.com/tidb/dev/br-usage-backup)

[Restore Cluster Data](https://docs.pingcap.com/tidb/dev/br-usage-restore)

[Daily Check](https://docs.pingcap.com/tidb/dev/daily-check)

[Maintain TiDB Using TiUP](https://docs.pingcap.com/tidb/dev/maintain-tidb-using-tiup)

</LearningPath>

<LearningPath label="Monitor" icon="cloud6">

[Use Prometheus and Grafana](https://docs.pingcap.com/tidb/dev/tidb-monitoring-framework)

[Monitoring API](https://docs.pingcap.com/tidb/dev/tidb-monitoring-api)

[Alert Rules](https://docs.pingcap.com/tidb/dev/alert-rules)

</LearningPath>

<LearningPath label="Tune" icon="tidb-cloud-tune">

[Tuning Overview](https://docs.pingcap.com/tidb/dev/performance-tuning-overview)

[Tuning Methods](https://docs.pingcap.com/tidb/dev/performance-tuning-methods)

[Tune OLTP Performance](https://docs.pingcap.com/tidb/dev/performance-tuning-practices)

[Tune Operating System](https://docs.pingcap.com/tidb/dev/tune-operating-system)

[Tune Configurations](https://docs.pingcap.com/tidb/dev/configure-memory-usage)

[Tune SQL Performance](https://docs.pingcap.com/tidb/dev/sql-tuning-overview)

</LearningPath>

<LearningPath label="Tools" icon="doc7">

[TiUP](https://docs.pingcap.com/tidb/dev/tiup-overview)

[Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview)

[TiDB Lightning](https://docs.pingcap.com/tidb/dev/tidb-lightning-overview)

[Data Migration](https://docs.pingcap.com/tidb/dev/dm-overview)

[Backup & Restore (BR)](https://docs.pingcap.com/tidb/dev/backup-and-restore-overview)

[TiCDC](https://docs.pingcap.com/tidb/dev/ticdc-overview)

[PingCAP Clinic](https://docs.pingcap.com/tidb/dev/clinic-introduction)

[TiDB Operator](https://docs.pingcap.com/tidb/dev/tidb-operator-overview)

[TiSpark](https://docs.pingcap.com/tidb/dev/tispark-overview) 

</LearningPath>

</LearningPathContainer>
