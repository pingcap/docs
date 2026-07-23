---
title: TiDB Cloud BYOC Joint Validation
summary: This document outlines the joint validation process for TiDB Cloud BYOC deployments.
---

# TiDB Cloud BYOC Joint Validation

The final phase ensures that the environment is stable, secure, and fully observable. The TiDB Cloud team will collaborate with you to perform the following checks.

## Validation checklist

| Category | Validation Item | Owner |
| :---- | :---- | :---- |
| **Connectivity** | SQL Endpoint: verify connectivity to both private and public SQL endpoints from your application servers. | Customer |
| **Connectivity** | Secure Tunnel (optional): confirm stable VPN links via the Bastion Host. | TiDB Cloud |
| **Observability** | Metrics: verify that system metrics are populating correctly in Grafana and Prometheus. | TiDB Cloud |
| **Observability** | Logging: Confirm that logs are being collected. | TiDB Cloud |
| **Security** | Audit: verify that AWS CloudTrail is actively logging access attempts to the Bastion Host. | Customer |
| **Alerting** | Test Alerts: trigger a test alert to confirm the notification delivery system is functioning. | Joint |

Once all validation items are marked as **Pass**:

1. The deployment is officially considered **Complete**.
2. You can proceed with data migration or application integration.

## What's next

After the {{{ .byoc }}} deployment is validated, you can connect your applications to the instance, migrate data, or continue configuring operational capabilities such as monitoring, backup, and security. To further reduce the permissions granted during deployment, see [TiDB Cloud BYOC Security Hardening](/tidb-cloud/byoc/security-hardening.md).
