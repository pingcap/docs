---
title: TiDB Cloud Release Notes in 2026
summary: Learn about the release notes of TiDB Cloud in 2026.
aliases: ['/tidbcloud/supported-tidb-versions','/tidbcloud/release-notes','/ai/vector-search-changelogs/']
---

# TiDB Cloud Release Notes in 2026

This page lists the release notes of [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) in 2026.

## September 1, 2026

**General changes**

- **TiDB Cloud Essential**

    - TiDB Cloud Essential now lets you temporarily authorize TiDB Cloud Support to access Plan Replayer files for SQL performance troubleshooting.

        You can choose the access duration, extend it if needed, or revoke access at any time. Access is automatically revoked when the authorization expires.

        Plan Replayer files contain SQL text, table schemas, and optimizer statistics, but no actual table row data.

        For more information, see [Use Plan Replayer to Troubleshoot SQL Performance](https://docs.pingcap.com/tidbcloud/plan-replayer/?plan=essential).

- **TiDB Cloud Premium**

    - The **Events** page is now available for TiDB Cloud Premium instances.

        You can view historical events that record changes to your Premium instance on this page, along with information such as the event type, status, message, trigger time, and trigger user. Event data is retained for 7 days.

        For more information, see [Events](/tidb-cloud/tidb-cloud-events.md).

    - TiDB Cloud Premium now lets you configure filter rules for database audit logging.

        You can filter audit events by SQL user, event class, table, and execution status to control which database activities are logged, helping you focus on relevant events for security auditing and compliance.

        For more information, see [Specify audit filter rules](https://docs.pingcap.com/tidbcloud/tidb-cloud-auditing-premium/?plan=premium#specify-audit-filter-rules).

    - TiDB Cloud Premium now lets you temporarily authorize TiDB Cloud Support to access Plan Replayer files for SQL performance troubleshooting.

        You can choose the access duration, extend it if needed, or revoke access at any time. Access is automatically revoked when the authorization expires.

        Plan Replayer files contain SQL text, table schemas, and optimizer statistics, but no actual table row data.

        For more information, see [Use Plan Replayer to Troubleshoot SQL Performance](https://docs.pingcap.com/tidbcloud/plan-replayer/?plan=premium).

**Billing adjustments**

- **TiDB Cloud Essential**

    - Starting September 1, 2026, billing for backup usage and network egress on [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) instances gradually takes effect.

        Network egress is billed as a separate line item instead of being included in RCU charges.

        For more information, see [TiDB Cloud Essential Pricing Details](https://www.pingcap.com/tidb-cloud-essential-pricing-details/).

## August 28, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.5.7](https://docs.pingcap.com/tidb/stable/release-8.5.7/) to [v8.5.8](https://docs.pingcap.com/tidb/stable/release-8.5.8/).

## August 25, 2026

**General changes**

- **TiDB Cloud Premium**

    - TiDB Cloud Premium now supports streaming changefeed data directly to Amazon S3 and Alibaba Cloud Object Storage Service (OSS).

        This feature enables you to archive change data to cloud storage for downstream analytics and long-term retention, while reducing costs by eliminating the need for intermediate message queues.

        For more information, see [Sink to Cloud Storage](https://docs.pingcap.com/tidbcloud/changefeed-sink-to-cloud-storage/?plan=premium).

## August 18, 2026

**General changes**

- **TiDB Cloud Premium**

    - Introduce **Statement Insight** (PREVIEW) for TiDB Cloud Premium instances.

        This feature provides an actionable view into SQL resource consumption in your TiDB Cloud Premium instances.

        Now you can analyze RU consumption, latency, and execution counts of SQL statements in multiple dimensions, such as DB User, SQL type, DB, table, or SQL digest. In addition, you can see top contributors at a glance, making it easier to identify the sources of high resource consumption or slowdowns.

        Currently, this feature is in public preview and available only for a limited number of TiDB Cloud Premium instances created on or after August 19.

        For more information, see [Statement Insight (PREVIEW)](https://docs.pingcap.com/tidbcloud/statement-insight/?plan=premium).

- **TiDB Cloud Lake**

    - [TiDB Cloud Lake](https://docs.pingcap.com/tidbcloudlake/) is now available on Alibaba Cloud in Japan (Tokyo) (`ap-northeast-1`). 

        For more supported regions, see [Platforms & Regions](https://docs.pingcap.com/tidbcloudlake/platforms-regions/).

    - Expand Python extensibility and analytics engineering workflows for TiDB Cloud Lake with the new external Python UDF SDK and dbt adapter.

        - With the new external Python UDF SDK, you can implement custom scalar and table functions in Python, deploy them on a UDF server, register the endpoint in TiDB Cloud Lake, and call the functions directly from SQL. The SDK supports common and complex data types, NULL handling, I/O parallelism, and per-function concurrency controls.
        - With the new dbt adapter, you can connect dbt to TiDB Cloud Lake to build, test, and document data transformation workflows. The adapter supports table, view, and incremental materializations, as well as seeds, sources, custom data tests, documentation generation, snapshots, and connection retries.

      For more information, see the following documentation:

        - [External Function](https://docs.pingcap.com/tidbcloudlake/external-function/)
        - [Choose a User-Defined Function Type](https://docs.pingcap.com/tidbcloudlake/choose-a-udf-type/)
        - [Load Data with dbt](https://docs.pingcap.com/tidbcloudlake/load-with-dbt/)

## August 11, 2026

**General changes**

- **TiDB Cloud Essential, Premium, and Dedicated**

    - Support subscribing to alert notifications from TiDB Cloud via [Lark](https://www.larksuite.com/).

        If the [support plan](/tidb-cloud/connected-care-overview.md#connected-care) of your organization is **Enterprise** or **Premium**, you can now receive alert notifications via Lark.

        For more information, see the following documentation:

        - TiDB Cloud Essential: [Subscribe via Lark](https://docs.pingcap.com/tidbcloud/monitor-alert-lark/?plan=essential)
        - TiDB Cloud Premium: [Subscribe via Lark](https://docs.pingcap.com/tidbcloud/monitor-alert-lark/?plan=premium)
        - TiDB Cloud Dedicated: [Subscribe via Lark](https://docs.pingcap.com/tidbcloud/monitor-alert-lark/)

- **TiDB Cloud Lake**

    - Expand AI, Python, and BI integrations for [TiDB Cloud Lake](https://docs.pingcap.com/tidbcloudlake/) with the new MCP server and SQLAlchemy dialect.

        - With the new MCP server, you can now connect MCP-compatible AI tools to explore database objects, inspect table schemas, and run SQL using natural-language instructions. Built-in session sandbox protection is enabled by default, keeping production objects read-only while restricting writes to session-specific sandbox objects.
        - With the new SQLAlchemy dialect, you can connect Python applications and SQLAlchemy-compatible tools to TiDB Cloud Lake through the dialect. You can use tools such as Jupyter Notebook for querying and visualizing data, and Apache Superset for building charts and dashboards.

      For more information, see the following documentation:

        - [TiDB Cloud Lake MCP Server](https://docs.pingcap.com/tidbcloudlake/mcp-server)
        - [Connect AI Tools to TiDB Cloud Lake Using MCP](https://docs.pingcap.com/tidbcloudlake/mcp-client-integration)
        - [Connect to TiDB Cloud Lake with Jupyter Notebook](https://docs.pingcap.com/tidbcloudlake/jupyter-notebook)
        - [Connect to TiDB Cloud Lake with Apache Superset](https://docs.pingcap.com/tidbcloudlake/superset)

**Console changes**

- Improve the networking experience across TiDB Cloud plans with the following updates in the [TiDB Cloud console](https://tidbcloud.com/):

    - The **Networking** page now uses more consistent naming for endpoint configurations across TiDB Cloud plans.
    - For endpoint types with no configured endpoints, the **Networking** page now displays only the corresponding action button instead of an empty table.
    - For TiDB Cloud Starter and Essential instances, you can now click **Connect** in the upper-right corner of the **Networking** page to connect to your instance after configuring network access.
    - For TiDB Cloud Essential, Premium, and Dedicated, managing allowed IP addresses for public endpoints is now more intuitive. You can click **Add IP Address** to add an IP address, or click **...** for an existing IP address to edit or delete it.

## August 5, 2026

**General changes**

- **TiDB Cloud Premium**

    - Introduce **Custom Retention Mode** for automatic backups on TiDB Cloud Premium instances.

        TiDB Cloud Premium now offers two automatic backup modes:

        - **Custom Retention Mode:** lets you specify the retention period from 3 to 33 days and choose when daily snapshots are created.
        - **Standard Bundle Mode:** preserves the previous default automatic backup settings for PITR, hourly snapshots, and daily snapshots.

      For more information, see [Automatic backup modes](/tidb-cloud/premium/backup-and-restore-premium.md#automatic-backup-modes).

## August 4, 2026

**General changes**

- **TiDB Cloud Essential**

    - Support subscribing to alert notifications from TiDB Cloud Essential via generic webhooks.

        If the [support plan](/tidb-cloud/connected-care-overview.md#connected-care) of your organization is **Enterprise** or **Premium**, you can now receive alert notifications via a generic webhook. For services that require custom payload formats, such as Telegram or Microsoft Teams, use a lightweight relay to transform and forward the notifications.

        For more information, see [Subscribe via Webhook](https://docs.pingcap.com/tidbcloud/monitor-alert-webhook/?plan=essential).

- **TiDB Cloud Premium**

    - Support [Amazon MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html) clusters as changefeed sinks for TiDB Cloud Premium instances.

        For TiDB Cloud Premium instances hosted on AWS, you can now stream row change events to Amazon MSK Provisioned clusters over AWS PrivateLink.

        For more information, see [Set Up Private Endpoint for Changefeeds](/tidb-cloud/premium/set-up-sink-private-endpoint-premium.md) and [Set Up an Amazon MSK Provisioned Cluster via AWS PrivateLink](/tidb-cloud/setup-aws-msk-provisioned-private-link-service.md).

    - Support subscribing to alert notifications from TiDB Cloud Premium via generic webhooks.

        If the [support plan](/tidb-cloud/connected-care-overview.md#connected-care) of your organization is **Enterprise** or **Premium**, you can now receive alert notifications via a generic webhook. For services that require custom payload formats, such as Telegram or Microsoft Teams, use a lightweight relay to transform and forward the notifications.

        For more information, see [Subscribe via Webhook](https://docs.pingcap.com/tidbcloud/monitor-alert-webhook/?plan=premium).

- **TiDB Cloud Dedicated**

    - Update pause requirements for TiDB Cloud Dedicated clusters.

        Before [pausing a TiDB Cloud Dedicated cluster](/tidb-cloud/pause-or-resume-tidb-cluster.md), you must turn off [Point-in-Time Restore (PITR)](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore) and ensure that no Data Migration (DM) job is running. If either condition is not met, TiDB Cloud rejects the pause request and displays an error message.

    - Support subscribing to alert notifications from TiDB Cloud Dedicated via generic webhooks.

        If the [support plan](/tidb-cloud/connected-care-overview.md#connected-care) of your organization is **Enterprise** or **Premium**, you can now receive alert notifications via a generic webhook. For services that require custom payload formats, such as Telegram or Microsoft Teams, use a lightweight relay to transform and forward the notifications.

        For more information, see [Subscribe via Webhook](https://docs.pingcap.com/tidbcloud/monitor-alert-webhook/).

## July 28, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Database audit logging is now available in public preview for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters running TiDB v7.5.6 or later, or v8.5.2 or later.

        This feature records user access activities, including executed SQL statements, supports writing audit logs to Amazon S3, Google Cloud Storage (GCS), or Azure Blob Storage, and lets you configure filter rules to control which events are captured for specific SQL users.

        For more information, see [TiDB Cloud Dedicated Database Audit Logging (Preview)](/tidb-cloud/tidb-cloud-auditing.md).

## July 21, 2026

**General changes**

- **TiDB Cloud Essential**

    - [Top RU](/tidb-cloud/top-ru.md) (public preview) for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) now supports the following additional region:

        - Alibaba Cloud: `Jakarta (ap-southeast-5)`

      This feature displays minute-level top RU-consuming SQLs, helping you quickly identify the most resource-intensive queries to reduce costs.

## July 14, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Enhance cross-region restore for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated).

        When the target restore region has no pre-allocated CIDR block, you can now create a CIDR block directly on the **Restore** page, eliminating the need to manually create a cluster in that region before starting the restore.

## July 9, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.5.6](https://docs.pingcap.com/tidb/stable/release-8.5.6/) to [v8.5.7](https://docs.pingcap.com/tidb/stable/release-8.5.7/).

## July 7, 2026

**General changes**

- **TiDB Cloud Essential**

    - Support the Datadog integration (public preview).

        You can now configure TiDB Cloud to send key metrics from your [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) instances to [Datadog](https://www.datadoghq.com/) for centralized monitoring and alerting.

        For more information, see [Integrate TiDB Cloud with Datadog](https://docs.pingcap.com/tidbcloud/monitor-datadog-integration-for-tidb-x/?plan=essential).

- **TiDB Cloud Premium**

    - Support the Datadog integration (public preview).

        You can now configure TiDB Cloud to send key metrics from your [TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) instances to [Datadog](https://www.datadoghq.com/) for centralized monitoring and alerting.

        For more information, see [Integrate TiDB Cloud with Datadog](https://docs.pingcap.com/tidbcloud/monitor-datadog-integration-for-tidb-x/?plan=premium).

**Console changes**

- Standardize the label used in the [TiDB Cloud console](https://tidbcloud.com/) for public preview features as `PREVIEW`, replacing the previous mixed use of `BETA` and `PREVIEW`.

**API changes**

- **TiDB Cloud Dedicated**

    - Introduce the changefeed API endpoints for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated), providing programmatic management of change data capture (CDC) changefeeds.

        You can use these endpoints to create, list, get, delete, pause, resume, and scale changefeeds for real-time data replication to downstream systems, including Apache Kafka, MySQL, Amazon S3, Google Cloud Storage (GCS), and Azure Blob Storage.

        For more information, see [Changefeed API v1beta1 Reference](https://docs.pingcap.com/tidbcloud/api/v1beta1/dedicated/#tag/Changefeed).

## June 30, 2026

**General changes**

- **TiDB Cloud Essential**

    - Enhance the stability, security, and operational experience of [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential). The following enhancements and changes are rolling out gradually to newly created TiDB Cloud Essential instances.

        - **Improve the connection experience**: support standalone endpoints for newly created TiDB Cloud Essential instances, so you no longer need to include the mandatory [account prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix) when connecting to these instances.
        - **Support changing the root password**: you can change the root password directly from the TiDB Cloud console.
        - **Enhance the data import experience**: after entering the source destination fields on the import data page, you can click **Test Bucket Access** to verify access to the specified object storage bucket before importing data. In addition, the import page now displays the size of files to be imported to improve visibility and management of import operations.
        - **Update the availability of the Branch feature**: starting from **July 14, 2026**, newly created TiDB Cloud Essential instances no longer support the [Branch](/tidb-cloud/branch-overview.md) feature. Existing TiDB Cloud Essential instances created before this date are not affected. The Branch feature remains available in [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter).
        - **Update import and export capabilities**: to enhance security, importing data from local files and exporting data to local files are no longer supported.
        - **Update DB audit log storage requirements**: for security and compliance reasons, you must specify an external storage location for audit log retention.
        - [Changefeed](/tidb-cloud/essential-changefeed-overview.md) will be available as a billable feature starting from **July 1, 2026**.

      These features are rolling out in phases. Contact [support@pingcap.com](mailto:support@pingcap.com) for early access.

    - [Top RU](/tidb-cloud/top-ru.md) is now available in public preview for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) in the following regions:

        - Alibaba Cloud: `Singapore (ap-southeast-1)` and `Tokyo (ap-northeast-1)`

      This feature displays minute-level top RU-consuming SQL statements, helping you quickly identify the most resource-intensive queries to reduce costs.

      This feature is rolling out in phases. Contact [support@pingcap.com](mailto:support@pingcap.com) for early access.

- **TiDB Cloud Dedicated**

    - Refine the backup and restore flow for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

        - The **Restore** page for TiDB Cloud Dedicated no longer includes the **Restore From Region** option. Because TiDB Cloud Dedicated implicitly stores backup data in the same region as the cluster, you no longer need to select the region to restore from.
        - The **Restore to Region** option is renamed to **Cloud Provider & Region**.

      For more information, see [Restore data to a new cluster](/tidb-cloud/backup-and-restore.md).

- **TiDB Cloud Lake**

    - TiDB Cloud Lake is now in public preview.

        TiDB Cloud Lake is a cloud-native analytics warehouse in TiDB Cloud for modern analytics and AI-oriented data workflows. It provides elastic warehouses, ANSI SQL analytics, object storage, full-text search, vector search, and geospatial analysis in one managed service, helping teams analyze structured and semi-structured data without managing separate analytics infrastructure.

        With this public preview, you can run SQL analytics with elastic warehouses and use built-in search capabilities for BI, log analytics, semantic retrieval, and other modern analytics and AI use cases.

        To try TiDB Cloud Lake, log in to the [TiDB Cloud console](https://tidbcloud.com/), click **My Lake** in the left navigation pane, and then click **Try TiDB Cloud Lake** in the upper-right corner.

        For more information, see [TiDB Cloud Lake documentation](https://docs.pingcap.com/tidbcloudlake/).

**Upcoming billing adjustments**

- The following billing adjustments will take effect for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential):

    - **Minimum RCU billing updates**: starting from **August 1, 2026**, the minimum RCU value is automatically determined based on your configured maximum RCU value (Minimum RCU = 0.1 × configured maximum RCU, with a lower bound of 2,000 RCUs). If your actual usage remains below the minimum RCU threshold, TiDB Cloud calculates charges based on the minimum RCU value. For **existing instances created before July 1, 2026**, the implementation of this minimum RCU billing policy is postponed, and the exact effective date will be announced later.
    - **Additional billable features**: charges for backup usage and network egress will take effect on **September 1, 2026**. For more information, see [TiDB Cloud Essential pricing](https://www.pingcap.com/tidb-cloud-essential-pricing-details/).

## June 16, 2026

**General changes**

- Add domain verification for [Cloud Organization SSO](/tidb-cloud/tidb-cloud-org-sso-authentication.md).

    In the following scenarios, the **Allowed Email Domains** field is required. To improve security, you must verify domains before entering them in this field:

    - Enabling auto-provisioning for the OIDC or SAML authentication method
    - Enabling SCIM provisioning for the SAML authentication method

  For more information, see [Add and verify domains for OIDC and SAML](/tidb-cloud/tidb-cloud-org-sso-authentication.md#add-and-verify-domains-for-oidc-and-saml).

## June 9, 2026

**General changes**

- **TiDB Cloud Starter**

    - Add a new AWS region for [full-text search](https://docs.pingcap.com/ai/vector-search-full-text-search-python/) (public preview) on [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter): `N. Virginia (us-east-1)`. The feature is now available in the following AWS regions:

        - `Tokyo (ap-northeast-1)`
        - `Oregon (us-west-2)`
        - `N. Virginia (us-east-1)`
        - `Frankfurt (eu-central-1)`
        - `Singapore (ap-southeast-1)`

<CustomContent language="en,zh">

**High availability changes**

- **TiDB Cloud Essential**

    - Starting from June 9, 2026, newly created [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) instances are deployed in a single Availability Zone and do not support regional high availability.

        If you need regional high availability and cross-AZ failover, consider choosing [TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium).

        This change does not affect TiDB Cloud Essential instances created before June 9, 2026.
        
</CustomContent>

**API changes**

- **TiDB Cloud Premium**

    - Introduce the following backup API endpoints for [TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium), enabling unified management for both active and deleted instances within your organization.

        - [List backups](https://docs.pingcap.com/tidbcloud/api/v1beta2/premium/#tag/Backup/operation/BackupService_ListBackups): lists backups for both active and deleted TiDB Cloud Premium instances (in the recycle bin) within your organization.
        - [Delete a backup](https://docs.pingcap.com/tidbcloud/api/v1beta2/premium/#tag/Backup/operation/BackupService_DeleteBackup): deletes a specific backup within your organization by `backupId`.

## June 2, 2026

**General changes**

- **TiDB Cloud Starter**

    - Introduce the [Instance Capacity Plan](https://www.pingcap.com/programs/agentic-ai-instance-capacity) for organizations that require a large number of [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) instances and branches.

        By default, for each paid organization in TiDB Cloud, you can create up to 100 TiDB Cloud Starter instances and branches in total, with each branch counted as a separate instance. To exceed this limit, apply for the [Instance Capacity Plan](https://www.pingcap.com/programs/agentic-ai-instance-capacity).

- **TiDB Cloud Essential**

    - Top RU is now available in public preview for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) in the following regions:

        - AWS: `N. Virginia (us-east-1)`, `Tokyo (ap-northeast-1)`

      This feature displays minute-level top RU-consuming SQL statements, helping you quickly identify the most resource-intensive queries to reduce costs.

        This feature is rolling out in phases. Contact [support@pingcap.com](mailto:support@pingcap.com) for early access.

- **TiDB Cloud Premium**

    - Support Dual-Layer Data Encryption on Alibaba Cloud for [TiDB Cloud Premium](/tidb-cloud/select-cluster-tier.md#premium) instances.

        You can use your own keys in Alibaba Cloud Key Management Service (KMS) to encrypt data at rest, giving you greater control over data security and compliance.

        This feature is now available upon request. For more information, see [Dual-Layer Data Encryption](/tidb-cloud/premium/dual-layer-data-encryption-premium.md).

    - Provide two new TTL monitoring metrics on the **Metrics** page (**Instance Overview** tab) for TiDB Cloud Premium instances.

        - Table Count by TTL Schedule Delay
        - TTL Insert/Delete Rows by Day

      These metrics help you observe TTL job health and detect data retention issues. For more information, see [{{{ .premium }}} Built-in Metrics](/tidb-cloud/premium/built-in-monitoring-premium.md).

**API changes**

- **TiDB Cloud Starter**

    - For a paid organization not enrolled in the [Instance Capacity Plan](https://www.pingcap.com/programs/agentic-ai-instance-capacity), TiDB Cloud API now enforces a limit of 100 TiDB Cloud Starter instances and branches in total, with each branch counted as a separate instance.

        - When the limit is reached, API requests to create new TiDB Cloud Starter instances or branches are rejected.
        - To exceed this limit, apply for the [Instance Capacity Plan](https://www.pingcap.com/programs/agentic-ai-instance-capacity).

## May 26, 2026

**General changes**

- **TiDB Cloud Starter**

    - Add two new AWS regions for [full-text search](https://docs.pingcap.com/ai/vector-search-full-text-search-python/) (public preview) on [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter): `Tokyo (ap-northeast-1)` and `Oregon (us-west-2)`. The feature is now available in the following AWS regions:

        - `Tokyo (ap-northeast-1)`
        - `Oregon (us-west-2)`
        - `Frankfurt (eu-central-1)`
        - `Singapore (ap-southeast-1)`

- **TiDB Cloud Essential**

    - Top RU is now available in public preview for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) in the following regions:

        - AWS: `Oregon (us-west-2)`, `Frankfurt (eu-central-1)`, `Singapore (ap-southeast-1)`

      This feature shows the top RU-consuming SQL statements at minute-level granularity, helping you quickly identify resource-intensive queries to reduce costs.

      The feature is rolling out in phases. To request early access, contact [support@pingcap.com](mailto:support@pingcap.com).

**API changes**

- TiDB Cloud IAM API (v1beta1) supports managing organization members programmatically.

    The new `/members` endpoints let you manage organization membership and role assignments. You can use these endpoints to automate user lifecycle management tasks, such as onboarding new members with specific roles, adjusting permissions as responsibilities change, and removing members who leave the organization.

    For more information, see [TiDB Cloud IAM API](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam/#tag/Member).

## May 19, 2026

**General changes**

- **TiDB Cloud Essential**

    - Recycle Bin is now available for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential). It stores data of deleted TiDB Cloud resources that have valid backups.

        When a TiDB Cloud Essential instance with existing backups is deleted, its backup files are moved to the Recycle Bin. Backup files created by automatic backups are retained in the Recycle Bin for a specified period. To avoid data loss, restore the data to a new TiDB Cloud Essential instance before the retention period expires. Note that if a TiDB Cloud Essential instance **has no backup**, the deleted instance is not displayed in the Recycle Bin.

        For more information, see [Backup and Restore](/tidb-cloud/backup-and-restore-serverless.md#restore-from-recycle-bin).

    - Top RU is now available in public preview for [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) in the following region:

        - Alibaba Cloud: `Mexico (na-south-1)`

      This feature shows the top RU-consuming SQL statements at minute-level granularity, helping you quickly identify resource-intensive queries to reduce costs.

        The feature is rolling out in phases. To request early access, contact [support@pingcap.com](mailto:support@pingcap.com).

## May 12, 2026

**General changes**

- **TiDB Cloud Premium**

    - Add the `AVG RU/s` metric to the [TiDB Cloud Premium](https://docs.pingcap.com/tidbcloud/premium/?plan=premium) **Metrics** page.
    
        `AVG RU/s` displays the average number of RUs consumed per second over the selected time range, helping you better understand resource consumption.

- **TiDB Cloud Dedicated**

    - [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) is now generally available (GA) on Microsoft Azure in **Japan East** and **East US 2**.

        It delivers three-AZ high availability with a 99.99% uptime SLA, full HTAP powered by TiFlash, independent compute and storage scaling, fully managed operations by PingCAP SRE, seamless data import and migration, continuous backup with PITR, enterprise-grade security, and integrated observability. It also supports bulk data import, migration from MySQL and other sources, and real-time replication to downstream systems. If you use [Azure Marketplace](https://azuremarketplace.microsoft.com/), you can also subscribe to TiDB Cloud Dedicated through Azure Marketplace.

        For more information, see [From Preview to Production: TiDB Cloud Dedicated on Microsoft Azure is Now Generally Available](https://www.pingcap.com/blog/tidb-cloud-dedicated-ga-microsoft-azure/).

## April 28, 2026

**General changes**

- **TiDB Cloud Premium**

    - [TiDB Cloud Premium](https://docs.pingcap.com/tidbcloud/premium/?plan=premium) is now in public preview on AWS<CustomContent language="en,zh"> and Alibaba Cloud</CustomContent>.

        Powered by the [TiDB X](/tidb-cloud/tidb-x-architecture.md) kernel, TiDB Cloud Premium is specifically designed for mission-critical enterprise workloads that require hyperscale, uncompromising performance, and the cost efficiency of a cloud-native consumption model.

        TiDB Cloud Premium bridges the gap between [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated).

        - Compared with TiDB Cloud Essential, TiDB Cloud Premium delivers significantly stronger isolation across the compute, storage, and network layers, ensuring predictable performance for critical workloads. At the same time, it retains an elastic, on-demand scaling model, allowing compute capacity to scale independently without operational overhead.
        - Compared with TiDB Cloud Dedicated, TiDB Cloud Premium improves cost efficiency by eliminating idle headroom, so you only pay for the performance you actually use.

      For more information about TiDB Cloud Premium, see [TiDB Cloud Premium: Public Preview for Mission-Critical SQL](https://www.pingcap.com/blog/tidb-cloud-premium-public-preview/).

      To try TiDB Cloud Premium, go to the [TiDB Cloud console](https://tidbcloud.com/), click **Create Resource**, and select **Premium** as your plan. For more information, see [Create a TiDB Cloud Premium instance](/tidb-cloud/premium/create-tidb-instance-premium.md).

- **TiDB Cloud Dedicated**

    - TiProxy is now generally available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters on AWS. It provides enhanced connection management and load balancing to improve database reliability and performance.

        Key features of TiProxy:

        - Maintains persistent client connections during scaling operations and rolling upgrades.
        - Distributes traffic evenly across TiDB nodes for better resource utilization.

      For implementation details, see [Overview of TiProxy](/tidb-cloud/tiproxy-overview-for-cloud.md).

**Console changes**

- Improve the firewall rule management experience for public endpoints of TiDB Cloud Starter and Essential.

    The TiDB Cloud console now provides a streamlined dialog for managing firewall rules for public endpoints in TiDB Cloud Starter and Essential. You can add your current IP address, allow access from all AWS IP addresses for AWS-hosted instances, or manually specify an IP address or IP address range in one place.

    For more information, see [Create and manage a firewall rule](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md#create-and-manage-a-firewall-rule).

**API changes**

- Introduce TiDB Cloud Premium API (v1beta2) for managing the following resources automatically and efficiently:

    - **TiDB Cloud Premium Instance**: manage the lifecycle and configuration of TiDB Cloud Premium instances, including passwords, CA certificates, and cloud provider information.
    - **Backup**: manage backups for TiDB Cloud Premium instances, including backup-based restore.
    - **Region**: retrieve available regions for creating TiDB Cloud Premium instances.

  For more information, see [TiDB Cloud Premium API](https://docs.pingcap.com/tidbcloud/api/v1beta2/premium/).

## April 14, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.5.5](https://docs.pingcap.com/tidb/stable/release-8.5.5/) to [v8.5.6](https://docs.pingcap.com/tidb/stable/release-8.5.6/).

    - The Top SQL page in [TiDB Cloud Clinic](/tidb-cloud/tidb-cloud-clinic.md) now supports collecting and displaying TiKV network traffic and logical I/O metrics for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters hosted on AWS.

**Console changes**

- Unify the [TiDB Cloud console](https://tidbcloud.com) experience across all TiDB Cloud plans (such as {{{ .starter }}}, Essential, and Dedicated). The following capabilities are now available:

    - **[My TiDB](https://tidbcloud.com/tidbs) homepage**: A new org-level homepage with both the resource view and project view.
 
        - The resource view lists all TiDB Cloud resources across plans in one place.
        - The project view organizes TiDB Cloud resources by project and lets you manage projects in your organization.

    - **Unified resource creation workflow**: A single creation flow applies to all TiDB Cloud resource types, including {{{ .starter }}}, Essential, and Dedicated.
    - **TiDB X project support**: TiDB X instances (a service-oriented TiDB Cloud offering built on the [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md), such as {{{ .starter }}} and Essential) can now be optionally assigned to projects and moved between projects after creation.
    - **Instance-level roles**: Role assignments can now be scoped to individual TiDB X instances, enabling fine-grained access control within a project.
    - **Terminology update**: {{{ .starter }}} and Essential **clusters** are renamed to {{{ .starter }}} and Essential **instances** across the console.
    - **Breaking change tour guide**: A guided walkthrough is shown to existing users to explain structural changes, reducing disruption during the transition.

  For more information, see [Manage TiDB Cloud Resources and Projects](/tidb-cloud/manage-projects-and-resources.md) and [Project Migration FAQ for TiDB X Instances](/tidb-cloud/tidbx-instance-move-faq.md).

**API changes**

- `project_id` values for TiDB Cloud Starter and Essential instances **can change** because these instances can be moved between projects in the TiDB Cloud console. Do not hardcode `project_id` values.

- Add a `type` field to the [List all accessible projects](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Project/operation/ListProjects) endpoint.

    - If your application only reads the `id` and `name` fields from project responses, no changes are required.
    - If you need to distinguish between [project types](/tidb-cloud/tidbx-instance-move-faq.md#what-project-types-are-available-in-tidb-cloud) (for example, to filter dedicated projects, TiDB X projects, or the TiDB X virtual project), start reading the `type` field.

For more information, see [Project API Migration Guide for {{{ .starter }}} and Essential](/tidb-cloud/tidbx-starter-essential-project-api-migration-guide.md).

## April 8, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Enhance the cloud storage data import experience for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters.

        The import process is now streamlined into a 3-step wizard (Connection, Destination Mapping, and Pre-check) with a unified **Import data from Cloud Storage** entry point for Amazon S3, Google Cloud Storage, and Azure Blob Storage. The new flow supports single-file URIs and manual file mapping via wildcard patterns, and the pre-check step scans the source files and previews the mapping before the import runs, helping you catch configuration issues early and reduce import failures.

        For more information, see the following documents:

        - [Import CSV Files from Cloud Storage into TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md)
        - [Import Apache Parquet Files from Cloud Storage into TiDB Cloud Dedicated](/tidb-cloud/import-parquet-files.md)

## March 31, 2026

**General changes**

- **TiDB Cloud Essential**

    - Support configuring a private endpoint allowlist.

        You can now secure and manage private endpoint access more easily by configuring an allowlist in the [TiDB Cloud console](https://tidbcloud.com). In the allowlist, you can specify the AWS VPC Endpoint IDs and Alibaba Cloud endpoint IDs that are allowed to connect.

        For more information, see the following documents:

        - [Connect via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) 
        - [Connect via Private Endpoint with Alibaba Cloud](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

    - Enable Prometheus metrics integration (PREVIEW).

        [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) manages Prometheus integrations at the cluster level. This feature lets you seamlessly ship metrics from your TiDB Cloud Essential cluster to Prometheus, enabling advanced alerting on a unified platform. 

        For integration steps, see [Integrate TiDB Cloud with Prometheus and Grafana](/tidb-cloud/prometheus-grafana-integration.md).

## March 24, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Add a **Public Endpoint** status to [Console Audit Logging](/tidb-cloud/tidb-cloud-console-auditing.md) in TiDB Cloud to improve security tracking.

**Console changes**

- Support a logarithmic Y-axis to improve visualization for metrics with large value disparities. High-range and low-range fluctuations are clearly visible, making anomalies easier to identify.

## March 10, 2026

**General changes**

- **TiDB Cloud Essential**

    - Support Amazon MSK Provisioned in private link connections for dataflow scenarios.

        [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) now supports creating private link connections to an [Amazon MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html) cluster. This feature enables private network connectivity for changefeeds to Amazon MSK Provisioned clusters, without exposing traffic to the public internet.

        For more information, see [Connect to Amazon MSK Provisioned via a Private Link Connection](/tidb-cloud/serverless-private-link-connection-to-amazon-msk.md).

## March 3, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Changefeeds for Amazon S3 sinks support using AWS Role ARN for authentication.

        You can now configure changefeeds for Amazon S3 sinks using an IAM Role ARN on [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters, in addition to the existing AK/SK authentication method. This feature enhances security by enabling short-lived credentials and automatic rotation, simplifies secret management, and supports least-privileged practices.

        For more information, see [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md).

    - Refine storage usage calculation for TiKV and TiFlash.

        The calculation of TiKV and TiFlash storage usage for metrics and alerting systems now incorporates WAL files and temporary files, providing more accurate capacity and usage monitoring.

        For more information, see [TiDB Cloud Built-in Metrics](/tidb-cloud/built-in-monitoring.md).

## February 10, 2026

**General changes**

- **TiDB Cloud Starter**

    - Upgrade the default TiDB version of new [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) clusters from [v7.5.6](https://docs.pingcap.com/tidb/stable/release-7.5.6) to [v8.5.3](https://docs.pingcap.com/tidb/stable/release-8.5.3).

- **TiDB Cloud Essential**

    - Support built-in alerting.

        Built-in alerting enables you to subscribe to receive instant alerts through email, Slack, Zoom, Flashduty, and PagerDuty. You can also customize alerts by defining specific thresholds for each alert type.

        For more information, see [TiDB Cloud Built-in Alerting](https://docs.pingcap.com/tidbcloud/monitor-built-in-alerting/?plan=essential).

- **TiDB Cloud Dedicated**

    - Support Private Link connectivity for data imports from Azure Blob Storage.
  
        When importing data from Azure Blob Storage into a [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) cluster, you can now select Private Link as the connectivity method to connect via an Azure private endpoint instead of the public internet. This feature enables secure, network-isolated data imports for storage accounts that restrict public access.

        For more information, see [Import Sample Data (SQL Files) from Cloud Storage](/tidb-cloud/import-sample-data.md), [Import CSV Files from Cloud Storage](/tidb-cloud/import-csv-files.md), and [Import Apache Parquet Files from Cloud Storage](/tidb-cloud/import-parquet-files.md).

    - Add "Enable/Disable Public Endpoint" events to the Console Audit Logging in TiDB Cloud for better security tracking.

## February 3, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Support sinking changefeed data to Azure Blob Storage.

        [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) now supports sinking changefeed data directly to Azure Blob Storage. This feature enables Azure-based users to archive change data efficiently for downstream analytics and long-term retention. It also reduces costs by eliminating the need for intermediate message queues and maintains format compatibility with existing Amazon S3 and Google Cloud Storage (GCS) sinks.

        For more information, see [Sink to Cloud Storage](/tidb-cloud/changefeed-sink-to-cloud-storage.md).

## January 27, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Support Flashduty and PagerDuty as alert subscription channels.
  
        These integrations are designed to streamline your incident management process and improve operational reliability.
  
        For more information, see [Subscribe via Flashduty](/tidb-cloud/monitor-alert-flashduty.md) and [Subscribe via PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md).

## January 20, 2026

**General changes**

- **TiDB Cloud Starter**

    - Display real client IP addresses in the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) view and the [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) table (beta).

        TiDB Cloud now supports client IP pass-through, enabling the Slow Query view and the `INFORMATION_SCHEMA.PROCESSLIST` table, to display the real client IP address instead of the Load Balancer (LB) IP. This feature helps accurately identify the true source of database requests for better troubleshooting and analysis. 

        Currently, this feature is in beta and is available only in the AWS region `Frankfurt (eu-central-1)`.

- **TiDB Cloud Essential**

    - Support data migration (beta).

        Now you can use the Data Migration feature in the [TiDB Cloud console](https://tidbcloud.com) to seamlessly migrate data from any MySQL-compatible database to your [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) clusters.

        - Supported source databases include various MySQL-compatible systems, such as self-hosted MySQL, Amazon RDS, Alibaba Cloud RDS, and PolarDB.
        - Supported connection methods for data migration include public connection and PrivateLink to ensure both ease of use and enterprise-grade security:

            - **Public connection**: quickly connects to your source database over the internet using secure and encrypted channels.
            - **PrivateLink**: establishes a secure and private connection between your source VPC and TiDB Cloud, bypassing the public internet to ensure maximum data privacy and reduced network latency.

      Currently, the Data Migration feature only supports logical mode.
  
        For more information, see [Migrate Existing and Incremental Data Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md) and [Migrate Incremental Data Using Data Migration](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md).

    - Display real client IP addresses in the [Slow Query](/tidb-cloud/tune-performance.md#slow-query) view, [DB audit logs](/tidb-cloud/essential-database-audit-logging.md), and the [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) table (beta)

        TiDB Cloud now supports client IP pass-through, enabling the Slow Query view, DB audit logs, and the `INFORMATION_SCHEMA.PROCESSLIST` table, to display the real client IP address instead of the Load Balancer (LB) IP. This feature helps accurately identify the true source of database requests for better troubleshooting and analysis. 

        Currently, this feature is in beta and is available only in the AWS region `Frankfurt (eu-central-1)`.

**Console changes**

- Improve the support experience with plan-aware support options.

    The [TiDB Cloud console](https://tidbcloud.com/) now offers plan-aware support options to enhance the support experience across all subscription plans. These updates include:

    - **Plan-aware support redirection**: on the cluster overview page, selecting **Get Support** in the **Actions** column directs you to the most relevant resource based on your subscription plan. Users on the Basic plan are guided to the **Support Plan** panel, and users on paid plans are directed to the **Support Portal**.
    - **Refined Help Center menu**: rename help menu items to **Support Options** and **Support Tickets** to better reflect available services. Add tooltips to clarify that technical support tickets are available only for paid plans.
    - **Clear community support access**: within the **Support Plan** options, Slack and Discord are clearly identified as the primary technical support channels for Basic plan users. The following documentation is streamlined to clarify support channel policies and community access: [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md), [Connected Care Overview](/tidb-cloud/connected-care-overview.md), and [Connected Care Details](/tidb-cloud/connected-care-detail.md).
    - **Action-oriented Support Plan UI**: redesign the **Support Plan** window to prioritize the support options available for your current subscription, rather than generic plan comparisons. This change helps you quickly identify how to get support based on your active plan.

  For more information, see [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## January 15, 2026

**General changes**

- **TiDB Cloud Dedicated**

    - Upgrade the default TiDB version of new [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters from [v8.5.4](https://docs.pingcap.com/tidb/stable/release-8.5.4/) to [v8.5.5](https://docs.pingcap.com/tidb/stable/release-8.5.5/).
