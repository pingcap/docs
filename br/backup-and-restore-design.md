---
title: Overview of TiDB Backup and Restore Architecture
summary: Learn about the architecture design of TiDB backup and restore features.
---

# Overview of TiDB Backup and Restore Architecture

As described in [TiDB Backup and Restore Overview](/br/backup-and-restore-overview.md), TiDB supports backing up and restoring multiple types of cluster data. You can use Backup & Restore (BR) and TiDB Operator to access these features, and create tasks to back up data from TiKV nodes or restore data to TiKV nodes.

For details about the architecture of each backup and restore feature, see the following documents:

- Full data backup and restore

    - [Back up snapshot data](/br/br-snapshot-architecture.md#backup-process)
    - [Restore snapshot backup data](/br/br-snapshot-architecture.md#restore-process)

- Data change log backup

    - [Log backup: backup of KV data change](/br/br-log-architecture.md#log-backup)

- Point-in-time recovery (PITR)

    - [PITR](/br/br-log-architecture.md#pitr)
