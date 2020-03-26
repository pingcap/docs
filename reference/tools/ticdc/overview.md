---
title: TiCDC Overview
category: reference
---

# TiCDC Overview

[TiCDC](https://github.com/pingcap/ticdc) is a tool for replicating the incremental data of TiDB. This tool is implemented by pulling TiKV change logs. It can restore data to a consistent state with any upstream TSO, and provides Open Data Protocol to support other systems to subscribe to data changes.

## TiCDC Architecture

When TiCDC is running, it is a stateless node made highly available through etcd in PD. The TiCDC cluster supports creating multiple replication tasks to replicate data to multiple different downstreams. The architecture of TiCDC is shown in the following figure:

![TiCDC architecture](/media/cdc-architecture.png)

### System roles

- TiKV CDC component: Only outputs key-value (KV) change logs.

    - Internal logic assembles KV change logs.
    - Provides the KV change log interface. The data sent includes real-time change logs and incremental scan change logs.

- `capture`: The operating process of TiCDC. Multiple `capture`s form a TiCDC cluster that replicates KV change logs.

    - Each `capture` pulls a part of KV change logs.
    - Sorts the pulled the KV change log(s).
    - Restores the transaction downstream or outputs the log based on the TiCDC open protocol.

## Replication features

This section introduces the replication features of TiCDC.

### Sink support

Currently, the TiCDC sink component supports replicating data to the following downstream databases:

- Databases compatible with MySQL protocol. The sink component provides the final consistency support.
- Kafka based on the TiCDC open protocol. The sink component ensures the row-level orderliness, final consistency or strict transactional consistency.

### Black and white table lists

You can write blacklist and whitelist filtering rules to filter all changed data in certain databases or tables or to only replicate changed data in certain databases or tables. This filtering rules are similar to those of MySQL.

## Restrictions

To replicate data to TiDB or MySQL, meet the following requirements to guarantee the correctness of replication:

- The table to be replicated has the primary key or a unique index.
- If the table to be replicated only has unique indexes, each column of at least one unique index is explicitly defined in the table schema as `NOT NULL`.
