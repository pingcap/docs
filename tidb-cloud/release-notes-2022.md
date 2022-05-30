---
title: TiDB Cloud Release Notes in 2022
summary: Learn about the release notes of TiDB Cloud in 2022.
aliases: ['/tidbcloud/beta/supported-tidb-versions','/tidbcloud/release-notes']
---

# TiDB Cloud Release Notes in 2022

This page lists the release notes of [TiDB Cloud](https://en.pingcap.com/tidb-cloud/) in 2022.

## May 24, 2022

* Support customizing TiDB port number when you create or restore a Dedicated Tier cluster

## May 19, 2022

* Add the support of the AWS region `Frankfurt` for Developer Tier cluster creation

## May 18, 2022

* Support [signing up](https://tidbcloud.com/signup) TiDB Cloud with a GitHub account

## May 13, 2022

* Support [signing up](https://tidbcloud.com/signup) TiDB Cloud with a Google account

## May 1, 2022

* Support configuring vCPU size of TiDB, TiKV, and TiFlash<sup>beta</sup> when you create or restore a cluster
* Add the support of the AWS region `Mumbai` for cluster creation
* Update the compute, storage, and data transfer cost for [TiDB Cloud billing](/tidb-cloud/tidb-cloud-billing.md)

## April 7, 2022

* Upgrade TiDB Cloud to [TiDB v6.0.0](https://docs.pingcap.com/tidb/v6.0/release-6.0.0-dmr) for Developer Tier

## March 31, 2022

TiDB Cloud is now in General Availability. You can [sign up](https://tidbcloud.com/signup) and select one of the following options:

* Get started with Developer Tier for free
* Apply for a 14-day PoC trial for free
* Get full access with the Dedicated Tier

## March 25, 2022

New feature:

* Support [TiDB Cloud built-in alerting](/tidb-cloud/monitor-built-in-alerting.md)

    With the TiDB Cloud built-in alerting feature, you can be notified by emails whenever a TiDB Cloud cluster in your project triggers one of TiDB Cloud built-in alert conditions.

## March 15, 2022

General changes:

* No cluster tier with the fixed cluster size any more. You can customize the cluster size of TiDB, TiKV, and TiFlash<sup>beta</sup> easily.
* Support adding TiFlash<sup>beta</sup> nodes for an existing cluster without TiFlash.
* Support specifying the storage size (500 to 2048 GiB) when creating a new cluster. The storage size cannot be changed after the cluster is created.
* Introduce a new public region: `eu-central-1`.
* Deprecate 8 vCPU TiFlash<sup>beta</sup> and provide 16 vCPU TiFlash.
* Separate the price of CPU and storage (both have 30% public preview discount).
* Update the [billing information](/tidb-cloud/tidb-cloud-billing.md) and the [price table](https://en.pingcap.com/tidb-cloud/#pricing).

New features:

* Support [the Prometheus and Grafana integration](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)

    With the Prometheus and Grafana integration, you can configure a [Prometheus](https://prometheus.io/) service to read key metrics from the TiDB Cloud endpoint and view the metrics using [Grafana](https://grafana.com/).

* Support assigning a default backup time based on the selected region of your new cluster

    For more information, see [Back up and Restore TiDB Cluster Data](/tidb-cloud/backup-and-restore.md).

## March 04, 2022

New feature:

* Support [the Datadog integration](/tidb-cloud/monitor-datadog-integration.md)

    With the Datadog integration, you can configure TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/). After that, you can view these metrics in your Datadog dashboards directly.

## February 15, 2022

General change:

* Upgrade TiDB Cloud to [TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0) for Developer Tier

Improvement:

* Support using custom file names when importing [CSV files](/tidb-cloud/import-csv-files.md) or [Apache Parquet files](/tidb-cloud/import-parquet-files.md) into TiDB Cloud

## January 11, 2022

General change:

* Upgrade TiDB Operator to [v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6)

Improvement:

* Add a suggested option `--connect-timeout 15` to the MySQL client on the **Connect** page

Bug fixes:

* Fix the issue that a user cannot create a cluster if the password contains a single quote
* Fix the issue that even an organization only has one owner, the owner can be deleted or changed to another role