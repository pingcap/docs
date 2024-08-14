---
title: Use Witness Replicas to Speed Up Failover
summary: Learn how to use a Witness replica to speed up failover.
---

# Use Witness Replicas to Speed Up Failover

This document describes how to use Witness replicas to improve durability when a TiKV node is down. If you need to use Witness replicas to save costs in a high-reliability storage environment, refer to [Use Witness replicas to save costs](/use-witness-to-save-costs.md).

## Feature description

The Witness feature can be used to quickly recover from any failure (failover) to improve system availability and data durability. For example, in a Raft group of three replicas, if one replica fails, the system is fragile although it meets the majority requirement. It takes a long time to recover a new member (the process requires copying the snapshot first and then applying the latest logs), especially when the Region snapshot is large. In addition, the process of copying replicas might cause more pressure on unhealthy Group members. Therefore, adding a Witness replica can quickly remove the unhealthy node, reduce the risk of the Raft group being unavailable due to another node failure when recovering a new member (the Learner replica cannot participate in the election and submission), and ensure the security of logs during recovery.

> **Warning:**
>
> The Withness replica is introduced in v6.6.0 and is not compatible with previous versions. It is not supported to downgrade.

## User scenarios

In a scenario where you want to quickly recover from any failure to improve durability, you can enable Witness without configuring a Witness replica.

## Usage

To enable Witness, use PD Control to run the `config set enable-witness true` command:

```bash
pd-ctl config set enable-witness true
```

If the command returns `Success`, the Witness replica feature is enabled. If you have not configured Witness replicas according to [Use Witness replicas to save costs](/use-witness-to-save-costs.md), no Witness replicas will be created by default. Only when a TiKV node is down, a Witness replica will be added immediately and will be promoted to a normal Voter later.
