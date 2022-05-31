---
title: Learning Path
hide_title: true
hide_sidebar: true
---
<!--

Note the parameters in the frontmatter:
    - `hide_title: true` Hide the document title.
    - `hide_sidebar: true` Hides the right sidbar.

Each `LearningPath` specifies one category. Each content tab is labeled with `LearningPathContent`. Note that you must define the id and label. The label is the name displayed on the tab. In our case, it's the target user name, such as DBA, Dev.

The whole content is enclosed by `LearningPathContainer`.
-->

<LearningPathContainer>
<!--
<LearningPathContent id="dba" label="DBA">
-->

<LearningPath>

![Introduction](/media/tidb-cloud/tidb-cloud-intro.png)

<h4>Introduction</h4>

- [What is TiDB Cloud](/tidb-cloud/tidb-cloud-intro.md)
- [Architecture](/tidb-cloud/tidb-cloud-intro.md#architecture)
- [High Availability](/tidb-cloud/high-availability-with-multi-az.md)
- [FAQs](/tidb-cloud/tidb-cloud-faq.md)

</LearningPath>

<LearningPath>

![Pricing](/media/tidb-cloud/tidb-cloud-pricing.png)

<h4>Pricing</h4>

- [Billing](/tidb-cloud/tidb-cloud-billing.md)
- [Pricing](https://en.pingcap.com/tidb-cloud-pricing)

</LearningPath>

<LearningPath>

![Try](/media/tidb-cloud/tidb-cloud-try.png)

<h4>Try</h4>

- [Quick Start](/tidb-cloud/tidb-cloud-quickstart.md)
- [Perform a PoC](/tidb-cloud/tidb-cloud-poc.md)
- [Cluster Tier](/tidb-cloud/select-cluster-tier.md)

</LearningPath>

<LearningPath>

![Deploy](/media/tidb-cloud/tidb-cloud-deploy.png)

<h4>Deploy</h4>

- [Determine TiDB Size](/tidb-cloud/size-your-cluster.md)
- [Create TiDB Cluster](/tidb-cloud/create-tidb-cluster.md)
- [Connect to Cluster](/tidb-cloud/connect-to-tidb-cluster.md)
- [Set Up VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md)
- [Manage User Access](/tidb-cloud/manage-user-access.md)

</LearningPath>

<LearningPath>

![Migrate](/media/tidb-cloud/tidb-cloud-migrate.png)

<h4>Migrate</h4>

- [From MySQL-Compatible Databases](/tidb-cloud/migrate-data-into-tidb.md)
- [From Aurora](/tidb-cloud/migrate-from-aurora-bulk-import.md)
- [From S3 or GCS](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md)
- [Import CSV Files](/tidb-cloud/import-csv-files.md)
- [Import Apache Parquet Files](/tidb-cloud/import-parquet-files.md)

</LearningPath>

<LearningPath>

![Monitor](/media/tidb-cloud/tidb-cloud-monitor.png)

<h4>Monitor</h4>

- [Overview](/tidb-cloud/monitor-tidb-cluster.md)
- [Built-in Alerting](/tidb-cloud/monitor-built-in-alerting.md)
- [Datadog](/tidb-cloud/monitor-datadog-integration.md)
- [Prometheus and Grafana](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)

</LearningPath>

<LearningPath>

![Tune Performance](/media/tidb-cloud/tidb-cloud-tune.png)

<h4>Tune Performance</h4>

- [Analyze and Tune Performance](/tidb-cloud/tune-performance.md)
- [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer)

</LearningPath>
<!--
</LearningPathContent>
-->

</LearningPathContainer>
