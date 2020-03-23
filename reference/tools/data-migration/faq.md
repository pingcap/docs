---
title: TiDB Data Migration FAQ
summary: Learn about frequently asked questions (FAQs) about TiDB Data Migration (DM).
category: reference
aliases: ['/docs/dev/faq/data-migration/']
---

# TiDB Data Migration FAQ

This document collects the frequently asked questions (FAQs) about TiDB Data Migration (DM).

## Does DM support replicating data from Alibaba RDS or other cloud databases?

Currently, DM only supports decoding the standard version of MySQL or MariaDB binlog. It has not been tested for Alibaba Cloud RDS or other cloud databases. If you are confirmed that its binlog is in standard format, then it is supported.

## Does the regular expression of the black and white list in the task configuration support `non-capturing (?!)`?

Currently, DM does not support it and only supports the regular expressions of the Golang standard library. See regular expressions supported by Golang via [re2-syntax](https://github.com/google/re2/wiki/Syntax).

## If a statement executed upstream contains multiple DDL operations, does DM support such replication?

DM will attempt to split a single statement containing multiple DDL change operations into multiple statements containing only one DDL operation, but might not cover all cases. It is recommended to include only one DDL operation in a statement executed upstream, or verify it in the test environment. If it is not supported, you can file an [issue](https://github.com/pingcap/dm/issues) to the DM repository.

## How to handle incompatible DDL statements?

When you encounter a DDL statement unsupported by TiDB, you need to manually handle it using dmctl (skipping the DDL statement or replacing the DDL statement with a specified DDL statement). For details, see [Skip or replace abnormal SQL statements](/reference/tools/data-migration/skip-replace-sqls.md).

> **Note:**
>
> Currently, TiDB is not compatible with all the DDL statements that MySQL supports. See [MySQL Compatibility](/reference/mysql-compatibility.md#ddl).

## How to reset the data replication task?

You need to reset the entire data replication task in the following cases:

- `RESET MASTER` is accidentally executed in the upstream database.
- The relay log or the upstream binlog is corrupted or lost.

Generally, at this time, the relay unit exits with an error and cannot be automatically restored gracefully. You need to manually restore the data replication and the steps are as follows:

1. Use the `stop-task` command to stop all the replication tasks that are currently running.
2. Use Ansible to [stop the entire DM cluster](/how-to/deploy/data-migration-with-ansible.md#step-10-stop-the-dm-cluster).
3. Manually clean up the relay log directory of the DM-worker corresponding to the MySQL master whose binlog is reset.

    - If the cluster is deployed using DM-Ansible, the relay log is in the `<deploy_dir>/relay_log` directory.
    - If the cluster is manually deployed using the binary, the relay log is in the directory set in the `relay-dir` parameter.

4. Clean up downstream replicated data.
5. Use Ansible to [start the entire DM cluster](/how-to/deploy/data-migration-with-ansible.md#step-9-deploy-the-dm-cluster).
6. Restart data replication with the new task name, or set `remove-meta` to `true` and `task-mode` to `all`.

## How to handle the error returned by the DDL operation related to the gh-ost table, after `online-ddl-scheme: "gh-ost"` is set?

```
[unit=Sync] ["error information"="{\"msg\":\"[code=36046:class=sync-unit:scope=internal:level=high] online ddls on ghost table `xxx`.`_xxxx_gho`\\ngithub.com/pingcap/dm/pkg/terror.(*Error).Generate ......
```

The above error can be caused by the following reason:

- In the last `rename ghost_table to origin table` step, DM reads the DDL information in memory, and restores it to the DDL of the origin table.
- However, the DDL information in memory is obtained in either of the two ways: 
    - DM [processes the gh-ost table during the `alter ghost_table` operation](/reference/tools/data-migration/features/online-ddl-scheme.md#process-online-ddl-scheme-gh-ost) and records the information of the DDL information of ghost_table;
    - When dm-worker is restarted to start the task, DM reads the DDL from `dm_meta.{task_name}_onlineddl`.

Therefore, in the process of incremental replication, if the specified Pos skipped the `alter ghost_table` DDL but the Pos is still in the online-ddl process of gh-ost, the ghost_table is not written into memory or `dm_meta.{task_name}_onlineddl` correctly. In such cases, the above error is returned.

You can avoid this error by the following steps:

1. Remove the `online-ddl-scheme` configuration of the task.

2. Configure `_{table_name}_gho`, `_{table_name}_ghc`, and `_{table_name}_del` in `black-white-list.ignore-tables`.

3. Execute the upstream DDL in the downstream TiDB manually.

4. After the Pos is replicated to the position of the gh-ost process, re-enable the `online-ddl-scheme` and comment out `black-white-list.ignore-tables`.
