---
title: TiDB Cloud Release Notes
summary: Learn about the release notes of TiDB Cloud.
aliases: ['/tidbcloud/beta/supported-tidb-versions']
---

# TiDB Cloud Release Notes

This page lists the release notes of [TiDB Cloud](https://en.pingcap.com/tidb-cloud/).

## April 7, 2022

* Upgrade TiDB Cloud to [TiDB v6.0.0](https://docs.pingcap.com/tidb/v6.0/release-6.0.0-dmr) for Developer Tier

## March 31, 2022

TiDB Cloud is now in General Availability. You can [sign up](https://tidbcloud.com/signup) and select one of the following options:

* Get started with Developer Tier for free
* Apply for a 14-day PoC trial for free
* Get full access with the Dedicated Tier

## March 25, 2022

New feature:

* Support [TiDB Cloud built-in alerting](/cloud/monitor-built-in-alerting.md)

    With the TiDB Cloud built-in alerting feature, you can be notified by emails whenever a TiDB Cloud cluster in your project triggers one of TiDB Cloud built-in alert conditions.

## March 15, 2022

General changes:

* No cluster tier with the fixed cluster size any more. You can customize the cluster size of TiDB, TiKV, and TiFlash<sup>beta</sup> easily.
* Support adding TiFlash<sup>beta</sup> nodes for an existing cluster without TiFlash.
* Support specifying the storage size (500 to 2048 GiB) when creating a new cluster. The storage size cannot be changed after the cluster is created.
* Introduce a new public region: `eu-central-1`.
* Deprecate 8 vCPU TiFlash<sup>beta</sup> and provide 16 vCPU TiFlash.
* Separate the price of CPU and storage (both have 30% public preview discount).
* Update the [node cost formula](/cloud/tidb-cloud-billing.md#node-cost) and the [price table](https://en.pingcap.com/tidb-cloud/#pricing).

New features:

* Support [the Prometheus and Grafana integration](/cloud/monitor-prometheus-and-grafana-integration.md)

    With the Prometheus and Grafana integration, you can configure a [Prometheus](https://prometheus.io/) service to read key metrics from the TiDB Cloud endpoint and view the metrics using [Grafana](https://grafana.com/).

* Support assigning a default backup time based on the selected region of your new cluster

    For more information, see [Back up and Restore TiDB Cluster Data](/cloud/backup-and-restore.md).

## March 04, 2022

New feature:

* Support [the Datadog integration](/cloud/monitor-datadog-integration.md)

    With the Datadog integration, you can configure TiDB Cloud to send metric data about your TiDB clusters to [Datadog](https://www.datadoghq.com/). After that, you can view these metrics in your Datadog dashboards directly.

## February 15, 2022

General change:

* Upgrade TiDB Cloud to [TiDB v5.4.0](https://docs.pingcap.com/tidb/stable/release-5.4.0) for Developer Tier

Improvement:

* Support using custom file names when importing [CSV files](/cloud/import-csv-files.md) or [Apache Parquet files](/cloud/import-parquet-files.md) into TiDB Cloud

## January 11, 2022

General change:

* Upgrade TiDB Operator to [v1.2.6](https://docs.pingcap.com/tidb-in-kubernetes/stable/release-1.2.6)

Improvement:

* Add a suggested option `--connect-timeout 15` to the MySQL client on the **Connect** page

Bug fixes:

* Fix the issue that a user cannot create a cluster if the password contains a single quote
* Fix the issue that even an organization only has one owner, the owner can be deleted or changed to another role

## December 28, 2021

New feature:

* Support [importing Apache Parquet files from Amazon S3 or GCS into TiDB Cloud](/cloud/import-parquet-files.md)

Bug fixes:

* Fix the import error that occurs when importing more than 1000 files to TiDB Cloud
* Fix the issue that TiDB Cloud allows to import data to existing tables that already have data

## November 30, 2021

General change:

* Upgrade TiDB Cloud to [TiDB v5.3.0](https://docs.pingcap.com/tidb/stable/release-5.3.0) for Developer Tier

New feature:

* Support [adding VPC CIDR for your TiDB cloud project](\cloud\set-up-vpc-peering-connections.md)

Improvements:

* Improve the monitoring ability for Developer Tier
* Support setting the auto backup time the same as the creation time of a Developer Tier cluster

Bug fixes:

* Fix the TiKV crash issue due to full disk in Developer Tier
* Fix the vulnerability of HTML injection

## November 8, 2021

* Launch [Developer Tier](/cloud/select-cluster-tier.md#developer-tier), which offers you a one-year free trial of TiDB Cloud

    Each Developer Tier cluster is a full-featured TiDB cluster and comes with the following:
    
    * One TiDB shared node
    * One TiKV shared node (with 10 GiB of OLTP storage)
    * One TiFlash<sup>beta</sup> shared node (with 10 GiB of OLAP storage)
  
  Get started [here](/cloud/tidb-cloud-quickstart.md).
  
## October 21, 2021

* Open user registration to personal email accounts
* Support [importing or migrating from Amazon S3 or GCS to TiDB Cloud](/cloud/migrate-from-amazon-s3-or-gcs.md)

## October 11, 2021

* Support [viewing and exporting billing details of TiDB Cloud](\cloud\tidb-cloud-billing.md#billing-details), including the cost of each service and each project
* Fix several issues of TiDB Cloud internal features

## September 16, 2021

* Upgrade the default TiDB version from 5.2.0 to 5.2.1 for newly deployed clusters. See [5.2.1](https://docs.pingcap.com/tidb/stable/release-5.2.1) release notes for detailed changes in 5.2.1.

## September 2, 2021

* Upgrade the default TiDB version from 5.0.2 to 5.2.0 for newly deployed clusters. See [5.2.0](https://docs.pingcap.com/tidb/stable/release-5.2.0) and [5.1.0](https://docs.pingcap.com/tidb/stable/release-5.1.0) release notes for details of TiDB 5.1.0 and 5.2.0 features.
* Fix several issues of TiDB Cloud internal features.

## August 19, 2021

* Fix several issues of TiDB Cloud internal features. This release does not bring any user behavior changes.

## August 5, 2021

* Support organization role management. Organization owners can configure permissions of organization members as needed.
* Support the isolation of multiple projects within an organization. Organization owners can create and manage projects as needed, and the members and instances between projects support network and authority isolation.
* Optimize the bill to show the billing of each item in the current month and previous month.

## July 22, 2021

* Optimize the user experience of adding credit cards
* Strengthen the security management of credit cards
* Fix the issue that the cluster recovered from backup cannot be charged normally

## July 6, 2021

* Upgrade the default TiDB version from 4.0.11 to 5.0.2 for newly deployed clusters. The upgrade brings significant performance and functionality improvements. See [here](https://docs.pingcap.com/tidb/stable/release-5.0.0) for details.

## June 25, 2021

* Fix the **Select Region** not working issue on the [TiDB Cloud Pricing](https://en.pingcap.com/products/tidbcloud/pricing/) page

## June 24, 2021

* Fix the parse errors of the parquet files when importing the Aurora snapshot into a TiDB instance
* Fix the Estimated Hours not being updated issue when PoC users create a cluster and change the cluster configuration

## June 16, 2021

* **China** is added to the **Country/Region** drop-down list when you sign up for an account

## June 14, 2021

* Fix the mounting EBS error when importing the Aurora snapshot into a TiDB instance

## May 10, 2021

General 

* TiDB Cloud is now in Public Preview. You can [sign up](https://tidbcloud.com/signup) and select one of the trial options: 

    * 48-Hour Free Trial
    * 2-Week PoC Free Trial
    * Preview On-Demand

Management Console

* Email verification and anti-robot reCAPTCHA have been added to the sign up process
* [TiDB Cloud Service Agreement](https://pingcap.com/legal/tidb-cloud-services-agreement) and [PingCAP Privacy Policy](https://pingcap.com/legal/privacy-policy/) have been updated
* You can apply for a [PoC](\cloud\tidb-cloud-poc.md) by filling out an application form in the console
* You can import sample data into TiDB Cloud cluster through UI
* Clusters with the same name are not allowed to avoid confusion 
* You can give feedback by clicking **Give Feedback** in the **Support** menu  
* Data backup and restore features are available for PoC and on-demand trial options 
* Points calculator and points usage dashboard have been added for Free Trial and PoC. Data storage and transfer costs are waived for all trial options

## December 30, 2020

* Upgrade the default TiDB version to v4.0.9
* Support upgrading and scaling in TiDB gracefully to achieve zero client failures
* Recover cluster configuration after restoring a new cluster from backup

## December 16, 2020

* Adjust the minimum number of TiDB nodes to one for all cluster tiers
* Prohibit executing system command on the SQL web shell
* Enable redact-log for TiDB clusters by default

## November 24, 2020

* Allow the traffic filter IP list of a TiDB cluster's public endpoint to be empty to disable public access
* Improve the delivery rate of invitation emails sent to customers with Outlook or Hotmail
* Polish the error notification message for sign-up
* New clusters will run on CentOS VM instead of Ubuntu
* Fix the issue that the cluster does not show in the recycle bin when the corresponding backup still exists

## November 4, 2020

* Implement the function of changing the organization name
* Prevent users from accessing TiDB during data restoring
* Update Terms of Service and Privacy location in the Sign Up page
* Add a feedback form entrance widget
* Prevent Members from deleting owner(s) in the Preference tab
* Change TiFlash<sup>beta</sup> and TiKV storage chart metrics
* Upgrade the default TiDB cluster version to 4.0.8

## October 12, 2020

* Change the SQL webshell client from Oracle MySQL client to `usql` client
* Upgrade the default TiDB version to 4.0.7
* Extend the manual backup retention period from 7 days to 30 days

## October 2, 2020

* Fix TiFlash<sup>beta</sup> disk storage configuration

## September 14, 2020

* Fix monitoring metrics by adding the `region` label
* Fix the issue that non-HTAP clusters cannot be scaled

## September 11, 2020

* Customers now can access TiDB using a public endpoint with traffic filters
* Add the time zone indicator at the auto backup settings dialog
* Fix the broken invitation link when registration is not finished

## September 4, 2020

* Fix an incorrect URL in invitation Email

## August 6, 2020

* Change email support to visiting TiDB Cloud Customer Support
* Add the simple 2fa feature for custom email login
* Add the feature of setting up VPC peering
* Add custom email support for signup/login

## July 17, 2020

* Adjust the default retention of automated daily backup to 7 days
* Add reasons at tooltip for clusters in unhealthy status
* Fix the issue that when the initial credit is 0, users can still create a cluster
* Optimize the integration of Dashboard
* Send emails when adding credits for customers
* Add the tenant ID in the tenant preference page
* Optimize the reasonable notice message for user's quota limit
* Fix backup/restore metrics
