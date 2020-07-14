---
title: High Availability FAQ
summary: Introduce the FAQs relating to high availability.
---

# High Availability FAQ

This document introduces the FAQS relating to high availability.

## How is TiDB strongly consistent?

Data is redundantly copied between TiKV nodes using the [Raft consensus algorithm](https://raft.github.io/) to ensure recoverability should a node failure occur.

At the bottom layer, TiKV uses a model of replication log + State Machine to replicate data. For the write requests, the data is written to a Leader and the Leader then replicates the command to its Followers in the form of log. When the majority of nodes in the cluster receive this log, this log is committed and can be applied into the State Machine.

## Besides the TiDB documentation, are there any other ways to acquire TiDB knowledge?

Currently [TiDB documentation](/overview.md#tidb-introduction) is the most important and timely way to get TiDB related knowledge. In addition, we also have some technical communication groups, if you need to learn more, send an email to [info@pingcap.com](mailto:info@pingcap.com).
