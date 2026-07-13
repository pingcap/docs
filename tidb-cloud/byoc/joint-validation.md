---
title: TiDB Cloud BYOC Joint Validation
summary: This document outlines the joint validation process for TiDB Cloud BYOC deployments.
---

# TiDB Cloud BYOC Joint Validation

The final phase ensures that the environment is stable, secure, and fully observable. The TiDB Cloud team will collaborate with you to perform the following checks.

## Validation Checklist

| Category | Validation Item | Owner |
| :---- | :---- | :---- |
| **Connectivity** | SQL Endpoint: verify connectivity to both private and public SQL endpoints from your application servers. | Customer |
| | Secure Tunnel（Optional）: Confirm stable VPN links via the Bastion Host. | TiDB Cloud |
| **Observability** | Metrics: verify that system metrics are populating correctly in Grafana/Prometheus. | TiDB Cloud |
| | Logging: Confirm that logs are being collected. | TiDB Cloud |
| **Security** | Audit: verify that AWS CloudTrail is actively logging access attempts to the Bastion Host. | Customer |
| **Alerting** | Test Alerts: Trigger a test alert to confirm the notification delivery system is functioning. | Joint |

Once all validation items are marked as **Pass**:

1. The deployment is officially considered **Complete**.
2. You may proceed with data migration or application integration.
