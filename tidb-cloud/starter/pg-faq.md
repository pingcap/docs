---
title: PostgreSQL-Compatible TiDB Cloud Starter FAQs
summary: Find answers to frequently asked questions about PostgreSQL-compatible TiDB Cloud Starter during the public preview period.
---

# PostgreSQL-Compatible TiDB Cloud Starter FAQs

This document answers frequently asked questions about PostgreSQL-compatible {{{ .starter }}} during public preview.

PostgreSQL-compatible {{{ .starter }}} enables developers to create and manage PostgreSQL-compatible database instances directly from the TiDB Cloud console. It supports the core instance lifecycle, including connections, monitoring, backup, and restore, as well as PostgreSQL ecosystem capabilities such as pgvector-compatible vector search and selected PostgreSQL extensions.

During public preview, PostgreSQL-compatible {{{ .starter }}} is available free of charge, subject to usage quotas. Billing is not enabled during the preview period.

## General FAQs

### How can I create a PostgreSQL-compatible Starter instance?

PostgreSQL-compatible {{{ .starter }}} is available in public preview.

To create an instance, select **Starter** in the TiDB Cloud console, choose the **PostgreSQL Compatible** option, review your configuration, and create the instance.

During public preview, PostgreSQL compatibility is available only with {{{ .starter }}}. {{{ .essential }}} and {{{ .premium }}} do not currently support this option.

### Which regions currently support PostgreSQL-compatible Starter?

During public preview, PostgreSQL-compatible {{{ .starter }}} is available in the following region:

- AWS US East (N. Virginia): `us-east-1`

Additional regions might become available as the preview expands. New region availability will be announced when ready.

### Can I use both MySQL-compatible and PostgreSQL-compatible Starter instances in the same TiDB Cloud organization?

Yes. You can use both MySQL-compatible and PostgreSQL-compatible {{{ .starter }}} instances in the same organization, project, and region.

TiDB Cloud displays the database type in the resource list and instance overview so you can distinguish between the two types of instances.

### How many Starter instances can I create?

A paid organization can create up to **100 {{{ .starter }}} instances** in total by default, including both MySQL-compatible and PostgreSQL-compatible instances. For MySQL-compatible instances, each branch is also counted as an instance.

The free-instance allowance covers:

- The first **5 MySQL-compatible** {{{ .starter }}} instances.
- The first **10 PostgreSQL-compatible** {{{ .starter }}} instances.

### Can I use PostgreSQL-compatible Starter in production?

During public preview, you can evaluate PostgreSQL-compatible {{{ .starter }}} with development, testing, and production-like workloads. **No service-level agreement (SLA) commitment is provided during public preview.**

Because the service is still in preview and some capabilities might continue to evolve, we recommend waiting until General Availability (GA) before using PostgreSQL-compatible {{{ .starter }}} for production workloads.

## Features and operations FAQs

### What features are currently available in PostgreSQL-compatible Starter?

PostgreSQL-compatible {{{ .starter }}} includes the following capabilities:

- **Instance management:** Create, list, monitor, and delete PostgreSQL-compatible {{{ .starter }}} instances in the TiDB Cloud console.
- **Connectivity:** Connect through a public endpoint using PostgreSQL-compatible clients and drivers.
- **Data import:** Import data using familiar PostgreSQL workflows, such as `psql` and `COPY`.
- **Backup and restore:** Use daily automatic backups and restore a snapshot to a new PostgreSQL-compatible {{{ .starter }}} instance.
- **Observability:** View built-in metrics for storage usage, queries per second (QPS), connections, and query duration.
- **AI and vector search:** Use pgvector-compatible vector search, full-text search, server-side embedding capabilities, and selected PostgreSQL extensions.

Additional capabilities are planned as PostgreSQL-compatible {{{ .starter }}} continues to evolve during public preview.

### How do I connect to a PostgreSQL-compatible Starter instance?

In the TiDB Cloud console, open the connection information for your PostgreSQL-compatible {{{ .starter }}} instance to find its public endpoint, port, username, and connection examples.

Private endpoints are not currently supported for PostgreSQL-compatible {{{ .starter }}}.

### Can a PostgreSQL-compatible backup be restored into a MySQL-compatible instance?

No. Cross-protocol restore is not supported. A PostgreSQL-compatible backup can be restored only into a PostgreSQL-compatible {{{ .starter }}} instance.

### What are the `tidbcloud_com_cell_*` tables?

PostgreSQL-compatible {{{ .starter }}} uses system-managed tables in the `public` schema to manage database users and safely process changes. These tables store service metadata, not application data.

- **`tidbcloud_com_cell_principals`:** Tracks database users managed by TiDB Cloud.
- **`tidbcloud_com_cell_sql_versions`:** Tracks changes to managed database resources and helps prevent conflicting updates.
- **`tidbcloud_com_cell_sql_receipts`:** Records operation results so retries can be handled safely. This table does not store passwords.

TiDB Cloud automatically maintains these tables. **Do not modify or drop them, or use them to store application data.** Doing so might interfere with managed database user operations.

## Billing and metering FAQs

### How is my usage measured?

PostgreSQL-compatible {{{ .starter }}} follows the TiDB Cloud Starter usage model, which measures:

- **Request Units (RUs)**
- **Row-based storage**

During public preview, RU usage is not yet displayed, and no billing charges are generated.

### Is PostgreSQL-compatible Starter free during public preview?

Yes. PostgreSQL-compatible {{{ .starter }}} is free of charge during public preview, subject to usage quotas. Billing is not enabled during this period.

For the first **10 PostgreSQL-compatible {{{ .starter }}} instances** in each organization, the free quota for each instance is:

- **Row-based storage:** 50 GiB
- **Request Units (RUs):** 500 million per month

If resource usage exceeds the free quota, TiDB Cloud might restrict further usage or suspend service.

If you anticipate exceeding these allowances or need additional resources, please contact <a href="mailto:support@pingcap.com">support@pingcap.com</a> to discuss your requirements.
