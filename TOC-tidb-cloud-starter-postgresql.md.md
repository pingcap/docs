<!-- markdownlint-disable MD007 -->
<!-- markdownlint-disable MD041 -->

# Table of Contents

## GET STARTED

- Why TiDB Cloud
  - [Introduction](/tidb-cloud/tidb-cloud-intro.md)
  - [Features](/tidb-cloud/features.md)
  - [PostgreSQL Compatibility](/tidb-cloud/starter/postgresql-compatibility.md)
- Get Started
  - [Try Out TiDB Cloud](/tidb-cloud/starter/pg-quickstart.md)

## GUIDES

- [Select Your Plan](/tidb-cloud/select-cluster-tier.md)
- [Manage TiDB Cloud Resources and Projects](/tidb-cloud/manage-projects-and-resources.md)
- Manage {{{ .starter }}} Instances
  - [Create a {{{ .starter }}} Instance](/tidb-cloud/create-tidb-cluster-serverless.md)
  - [Connect to Your {{{ .starter }}} Instance via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)
  - [Back Up and Restore TiDB Cloud Data](/tidb-cloud/backup-and-restore-serverless.md)
  - Monitor and Alert
    - [Overview](/tidb-cloud/monitor-tidb-cluster.md)
    - [Built-in Metrics](/tidb-cloud/starter/built-in-monitoring-pg.md)
  - [Delete a {{{ .starter }}} Instance](/tidb-cloud/delete-tidb-cluster.md)
- [Migrate from PostgreSQL to TiDB Cloud Starter](/tidb-cloud/starter/Import-with-psql.md)
- Security
  - [Security Overview](/tidb-cloud/security-overview.md)
  - Identity Access Control
    - [Password Authentication](/tidb-cloud/tidb-cloud-password-authentication.md)
    - [Standard SSO Authentication](/tidb-cloud/tidb-cloud-sso-authentication.md)
    - [Organization SSO Authentication](/tidb-cloud/tidb-cloud-org-sso-authentication.md)
    - [Identity Access Management](/tidb-cloud/manage-user-access.md)
    - [OAuth 2.0](/tidb-cloud/oauth2.md)
  - Network Access Control
    - [TLS Connections to TiDB Cloud](/tidb-cloud/secure-connections-to-serverless-clusters.md)
  - Audit Management
    - [Console Audit Logging](/tidb-cloud/tidb-cloud-console-auditing.md)

## REFERENCE

- PostgreSQL Extensions
  - [Overview](/tidb-cloud/starter/pg-extensions-overview.md)
  - [Vector Search](/tidb-cloud/starter/pg-vector-search.md)
  - [Full-Text Search](/tidb-cloud/starter/pg-full-text-search.md)
  - [Import Parquet Data](/tidb-cloud/starter/pg-parquet-import.md)
- SQL Reference
  - [Overview](/tidb-cloud/starter/pg-sql-reference-overview.md)
  - [DDL](/tidb-cloud/starter/pg-ddl.md)
  - [DML and Queries](/tidb-cloud/starter/pg-dml-queries.md)
  - [Data Types](/tidb-cloud/starter/pg-data-types.md)
  - [Built-in Functions](/tidb-cloud/starter/pg-built-in-functions.md)
  - [Advanced SQL](/tidb-cloud/starter/pg-advanced-sql.md)
  - [Authentication and Roles](/tidb-cloud/starter/pg-auth-roles.md)
  - [Transactions and COPY](/tidb-cloud/starter/pg-transactions-copy.md)
  - [Session Parameters](/tidb-cloud/starter/pg-session-parameters.md)
  - [System Catalog](/tidb-cloud/starter/pg-system-catalog.md)
  - [Row-Level Security](/tidb-cloud/starter/pg-row-level-security.md)
  - [Limits and Constraints](/tidb-cloud/starter/pg-limits-constraints.md)
- General Reference
  - TiDB Classic Architecture
    - [Overview](/tidb-architecture.md)
    - [Storage](/tidb-storage.md)
    - [Computing](/tidb-computing.md)
    - [Scheduling](/tidb-scheduling.md)
    - [TSO](/tso.md)
  - [TiDB X Architecture](/tidb-cloud/tidb-x-architecture.md)
  - Storage Engines
    - TiKV
      - [TiKV Overview](/tikv-overview.md)
      - [RocksDB Overview](/storage-engine/rocksdb-overview.md)
    - TiFlash
      - [TiFlash Overview](/tiflash/tiflash-overview.md)
      - [Spill to Disk](/tiflash/tiflash-spill-disk.md)
  - TiDB Cloud Partner Web Console
    - [TiDB Cloud Partners](/tidb-cloud/tidb-cloud-partners.md)
    - [MSP Customer](/tidb-cloud/managed-service-provider-customer.md)
    - [Reseller's Customer](/tidb-cloud/cppo-customer.md)
  - [{{{ .starter }}} and Essential Limitations](/tidb-cloud/serverless-limitations.md)
  - [Limited SQL Features on TiDB X Instances](/tidb-cloud/limited-sql-features-tidb-x.md)
  - [TiDB Limitations](/tidb-limitations.md)
  - [System Variables](/system-variables.md)
  - [Server Status Variables](/status-variables.md)
  - [Table Filter](/table-filter.md)
  - [URI Formats of External Storage Services](/external-storage-uri.md)
  - [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md)
  - [Notifications](/tidb-cloud/notifications.md)
