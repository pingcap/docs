---
title: DM-worker Connection Switch Between Upstream MySQL Instances
summary: Learn how to switch DM-worker connection between upstream MySQL instances.
category: reference
---

# DM-worker Connection Switch Between Upstream MySQL Instances

This document introduces how to switch the DM-worker connection from one upstream MySQL instance to another within the same master-slave replication cluster.

> **Note:**
>
> - You can only switch the DM-worker connection to a instance within the same master-slave replication cluster.
> - The MySQL instance to be newly connected to must have the binlog required by DM-worker.
> - DM-worker must operate in the GTID sets mode. That is to say that you must specify `enable_gtid=true` when you deploy DM using DM-Ansible.
> - The connection switch only supports the following two scenarios. Strictly follow the procedures for each scenario. Otherwise, you might have to re-deploy the DM cluster according to the newly connected MySQL instance and perform the data replication task all over again.

For more details on GTID set, refer to [MySQL documentation](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html#replication-gtids-concepts-gtid-sets).

## DM-worker connection switch behind virtual IP

When DM-worker connects the upstream MySQL instance behind virtual IP (VIP) and if you switch the MySQL instance that VIP directs at, you switch the MySQL instance actually connected to DM-worker with the upstream connection address unchanged.

> **Note:**
>
> Make necessary changes on DM in this scenario. Otherwise, when you switch the MySQL instance that VIP actually directs at, DM might connect to the new and old MySQL instances at the same time. In this situation, the binlog replicated to DM is not consistent with other upstream status that DM receives, causing unpredictable anomalies and even data damage.

For this VIP to direct at a new MySQL instance, follow these procedures:

1. Use the `query-status` command to get the GTID sets (`relayBinlogGtid`) corresponding to the binlog that relay log has replicated from the old MySQL instance. Mark this sets as `gtid-W`.
2. Use the `SELECT @@GLOBAL.gtid_purged;` command on the new MySQL instance to get the GTID sets corresponding to the purged binlogs. Mark this sets as `_gtid-P_`.
3. Use the `SELECT @@GLOBAL.gtid_executed;` command on the new MySQL instance to get the GTID sets corresponding to all successfully executed transactions. Mark this sets as `gtid-E_`.
4. Make sure that the following conditions are met. Otherwise, you cannot switch the DM-work connection to the new MySQL instance:
    - `gtid-W` contains `gtid-P`. `gtid-P` might be empty.
    - `gtid-E` contains `gtid-W`.
5. Use `pause-relay` to pause relay.
6. Use `pause-task` to pause all running tasks of data replication.
7. Change the VIP for it to direct at the new MySQL instance.
8. Use `switch-relay-master` to tell relay to execute the master-slave switch.
9. Use `resume-relay` to make relay resume to read binlog from the new MySQL instance.
10. Use `resume-task` to resume the previous replication task.

## Change address of upstream MySQL instance connected to DM-worker

To change the configuration information of DM-worker so that DM-worker connects to a new MySQL instance in the upstream, follow these procedures:

1. Use the `query-status` command to get the GTID sets (`relayBinlogGtid`) corresponding to the binlog that relay log has replicated from the old MySQL instance. Mark this sets as `gtid-W`.
2. Use the `SELECT @@GLOBAL.gtid_purged;` command on the new MySQL instance to get the GTID sets corresponding to the purged binlogs. Mark this sets as `_gtid-P_`.
3. Use the `SELECT @@GLOBAL.gtid_executed;` command on the new MySQL instance to get the GTID sets corresponding to all successfully executed transactions. Mark this sets as `gtid-E_`.
4. Make sure that the following conditions are met. Otherwise, you cannot switch the DM-work connection to the new MySQL instance:
    - `gtid-W` contains `gtid-P`. `gtid-P` might be empty.
    - `gtid-E` contains `gtid-W`.
5. Use `stop-task` to stop all running tasks of data replication.
6. Update the DM-worker configuration in the `inventory.ini` file and use DM-Ansible to perform a rolling upgrade on DM-worker.
7. Use `start-task` to restart the replication task.
