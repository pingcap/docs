---
title: Use Witness Replicas to Save Costs
summary: Learn how to use Witness replicas to save costs in a highly reliable storage environment.
---

# Use Witness Replicas to Save Costs

This document describes how to use Witness replicas to save costs in a highly reliable storage environment. If you need to use Witness replicas to improve the durability when a TiKV node is down, refer to [Use Witness replicas to speed up failover](/use-witness-to-speed-up-failover.md).

## Feature description

In cloud environments, it is recommended to use Amazon Elastic Block Store (EBS) with 99.8%~99.9% durability or Persistent Disk of Google Cloud Platform (GCP) with 99.99%~99.999% durability as the storage of each TiKV node. In this case, using three Raft replicas with TiKV is possible but not necessary. To reduce costs, TiKV introduces the Witness replica, which is the "2 Replicas With 1 Log Only" mechanism. The 1 Log Only replica only stores Raft logs and does not apply data, and still ensures data consistency through the Raft protocol. Compared with the standard three replica architecture, the Witness replica can save storage resources and CPU usage.

> **Warning:**
>
> The Withness replica is introduced in v6.6.0 and is not compatible with previous versions. It is not supported to downgrade.

## User scenarios

In a highly reliable storage environment (99.8%~99.9%), such as Amazon EBS and Persistent Disk of GCP, you can enable and configure Witness replicas to save costs.

## Usage

### Step 1: Enable Witness

To enable Witness, use PD Control to run the `config set enable-witness true` command:

```bash
pd-ctl config set enable-witness true
```

If the command returns `Success`, the Witness replica feature is enabled. If you have not configured Witness replicas using Placement Rules, no Witness replicas will be created by default. Only when a TiKV node is down, a Witness replica will be added immediately and will be promoted to a normal Voter later.

### Step 2: Configure Witness replicas

Assume that three replicas are present. Modify `rule.json` to the configuration in [Scenario 6: Configure Witness replicas in a highly reliable storage environment](/configure-placement-rules.md#scenario-6-configure-witness-replicas-in-a-highly-reliable-storage-environment).

After editing the file, use the following command to save the configuration to the PD server:

```bash
pd-ctl config placement-rules save --in=rule.json
```

## Notes

- It is recommended to configure Witness replicas only in a highly reliable storage environment, such as Amazon EBS with 99.8%~99.9% durability and Persistent Disk of GCP with 99.99%~99.999% durability to store TiKV nodes.
- Since a Witness replica does not apply Raft logs, it cannot provide read and write services. When the Leader is down and the remaining Voters do not have the latest Raft logs, Raft elects the Witness replica as a Leader. After the Witness replica is elected, it sends Raft logs to Voters and transfers the leader to a Voter. If the Witness replica cannot transfer the leader in time, the application might receive an `IsWitness` error after the Backoff timeout.
- When there is a pending Voter in the system, to prevent the Witness replica from accumulating too many Raft logs and occupying the entire disk space, the system will promote the Witness replica to a normal Voter.
