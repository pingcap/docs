---
title: TiDB 2.1.7 Release Notes
aliases: ['/docs/dev/releases/release-2.1.7/','/docs/dev/releases/2.1.7/']
---

# TiDB 2.1.7 Release Notes

Release Date: March 28, 2019

TiDB version: 2.1.7

TiDB Ansible version: 2.1.7

## TiDB

- Fix the issue of longer startup time when upgrading the program caused by canceling DDL operations [#9768](https://github.com/pingcap/tidb/pull/9768)
- Fix the issue that the `check-mb4-value-in-utf8` configuration item is in the wrong position in the `config.example.toml` file [#9852](https://github.com/pingcap/tidb/pull/9852)
- Improve the compatibility of the `str_to_date` built-in function with MySQL [#9817](https://github.com/pingcap/tidb/pull/9817)
- Fix the compatibility issue of the `last_day` built-in function [#9750](https://github.com/pingcap/tidb/pull/9750)
- Add the `tidb_table_id` column for `infoschema.tables` to facilitate getting `table_id` by using SQL statements and add the `tidb_indexes` system table to manage the relationship between Table and Index [#9862](https://github.com/pingcap/tidb/pull/9862)
- Add a check about the null definition of Table Partition [#9663](https://github.com/pingcap/tidb/pull/9663)
- Change the privileges required by `Truncate Table` from `Delete` to `Drop` to make it consistent with MySQL [#9876](https://github.com/pingcap/tidb/pull/9876)
- Support using subqueries in the `DO` statement [#9877](https://github.com/pingcap/tidb/pull/9877)
- Fix the issue that the `default_week_format` variable does not take effect in the `week` function [#9753](https://github.com/pingcap/tidb/pull/9753)
- Support the plugin framework [#9880](https://github.com/pingcap/tidb/pull/9880), [#9888](https://github.com/pingcap/tidb/pull/9888)
- Support checking the enabling state of binlog by using the `log_bin` system variable [#9634](https://github.com/pingcap/tidb/pull/9634)
- Support checking the Pump/Drainer status by using SQL statements [#9896](https://github.com/pingcap/tidb/pull/9896)
- Fix the compatibility issue about checking mb4 character on utf8 when upgrading TiDB [#9887](https://github.com/pingcap/tidb/pull/9887)
- Fix the panic issue when the aggregate function calculates JSON data in some cases [#9927](https://github.com/pingcap/tidb/pull/9927)

## PD

- Fix the issue that the transferring leader step cannot be created in the balance-region when the number of replicas is one [#1462](https://github.com/pingcap/pd/pull/1462)

## Tools

- Support replicating generated columns by using binlog

## TiDB Ansible

Change the default retention time of Prometheus monitoring data to 30d
