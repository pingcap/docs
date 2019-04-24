---
title: TiDB-Binlog Cluster upgrade
summary: Learn how to deploy, operate, and monitor the cluster version of TiDB-Binlog.
category: tools
---

# TiDB-Binlog upgrade

The new TiDB versions (v2.0.8-binlog, v2.1.0-rc.5 or later) are not compatible with the [Kafka version](../tools/tidb-binlog-kafka.md) or [local version](../tools/tidb-binlog.md) of TiDB-Binlog. If TiDB is upgraded to one of the new versions, it is required to use the cluster version of TiDB-Binlog. If the Kafka or local version of TiDB-Binlog is used before upgrading, you need to upgrade your TiDB-Binlog to the cluster version.

The corresponding relationship between TiDB-Binlog versions and TiDB versions is shown in the following table:

| TiDB-Binlog version | TiDB version | Note |
|:---|:---|:---|
| Local | TiDB 1.0 or earlier ||
| Kafka | TiDB 1.0 ~ TiDB 2.1 RC5 | TiDB 1.0 supports both the local and Kafka versions of TiDB-Binlog. |
| Cluster | TiDB v2.0.8-binlog, TiDB 2.1 RC5 or later | TiDB v2.0.8-binlog is a special 2.0 version supporting the cluster version of TiDB-Binlog. |

## Upgrade process

- If importing the full data is acceptable, you can abandon the old version and deploy TiDB-Binlog following this document.
- If you want to resume synchronization from the original checkpoint, perform the following steps to upgrade TiDB-Binlog:

    1. Deploy the new version of Pump.
    2. Stop the TiDB cluster service.
    3. Upgrade TiDB and the configuration, and write the binlog data to the new Pump cluster.
    4. Reconnect the TiDB cluster to the service.
    5. Make sure that the old version of Drainer has synchronized the data in the old version of Pump to the downstream completely.
    6. Start the new version of Drainer.
    7. Close the Pump and Drainer of the old versions and the dependent Kafka and Zookeeper.
