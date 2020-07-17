---
title: Backup & Restore FAQ
summary: Learn about Frequently Asked Questions (FAQ) and the solutions of BR.
aliases: ['/docs/dev/br/backup-and-restore-faq/']
---

# Backup & Restore FAQ

This document lists the frequently asked questions (FAQs) and the solutions about Backup & Restore (BR).

## What should I do if the error message `could not read local://...:download sst failed` is returned during data restoration?

When you restore data, each node must have access to **all** backup files (SST files). By default, if `local` storage is used, you cannot restore data because the backup files are scattered among different nodes. Therefore, you have to copy the backup file of each TiKV node to the other TiKV nodes.

It is recommended to mount an NFS disk as a backup disk during backup. For details, see [Back up a single table to a network disk](/br/backup-and-restore-use-cases.md#back-up-a-single-table-to-a-network-disk-recommended).

## How much does it affect the cluster during backup using BR?

When you use the `oltp_read_only` scenario of `sysbench` to back up to a disk (make sure the backup disk and the service disk are different) at full rate, the cluster QPS is decreased by 15%-25%. The impact on the cluster depends on the table schema.

To reduce the impact on the cluster, you can use the `--ratelimit` parameter to limit the backup rate.

## Does BR back up system tables? During data restoration, do they raise conflict?

The system libraries (`information_schema`, `performance_schema`, `mysql`) are filtered out during full backup. For more details, refer to the [Backup Principle](/br/backup-and-restore-tool.md#implementation-principles).

Because these system libraries do not exist in the backup files, no conflict occurs among system tables during data restoration.

## What should I do to resolve the `Permission denied` error, even if I have tried to run BR using root in vain?

You need to confirm whether TiKV has access to the backup directory. To back up data, confirm whether TiKV has the write permission. To restore data, confirm whether it has the read permission.

Running BR with the root access might fail due to the disk permission, because the backup files (SST files) are saved by TiKV.

> **Note:**
>
> You might encounter the same problem during data restoration. When the SST files are read for the first time, the read permission is verified. The execution duration of DDL suggests that there might be a long interval between checking the permission and running BR. You might receive the error message `Permission denied` after waiting for a long time.
>
> Therefore, It is recommended to check the permission before data restoration.

## What should I do to resolve the `Io(Os...)` error?

Almost all of these problems are system call errors that occur when TiKV writes data to the disk. You can check the mounting method and the file system of the backup directory, and try to back up data to another folder or another hard disk.
 
For example, you might encounter the `Code: 22(invalid argument)` error when backing up data to the network disk built by `samba`.

## Where are the backed up files stored when I use `local` storage?
 
When you use `local` storage, `backupmeta` is generated on the node where BR is running, and backup files are generated on the Leader nodes of each Region.

## How about the size of the backup data? Are there replicas of the backup?

During data backup, backup files are generated on the Leader nodes of each Region. The size of the backup is equal to the data size, with no redundant replicas. Therefore, the total data size is approximately the total number of TiKV data divided by the number of replicas.

However, if you want to restore data from local storage, the number of replicas is equal to that of the TiKV nodes, because each TiKV must have access to all backup files.
