---
title: TiDB Cloud BYOC 联合验证
summary: 本文档概述了 TiDB Cloud BYOC 部署的联合验证流程。
---

# TiDB Cloud BYOC 联合验证

最后阶段旨在确保环境稳定、安全且具备完整的可观测性。TiDB Cloud 团队将与您协作，执行以下检查。

## 验证清单 {#validation-checklist}

| 类别 | 验证项 | 负责人 |
| :---- | :---- | :---- |
| **连接性** | SQL Endpoint：验证能否从您的应用服务器连接到私有和公共 SQL endpoint。 | Customer |
| **连接性** | Secure Tunnel（可选）：通过 Bastion Host 确认 VPN 链路稳定。 | TiDB Cloud |
| **可观测性** | Metrics：验证系统指标是否已在 Grafana 和 Prometheus 中正确填充。 | TiDB Cloud |
| **可观测性** | Logging：确认日志正在被收集。 | TiDB Cloud |
| **安全性** | Audit：验证 AWS CloudTrail 是否正在主动记录对 Bastion Host 的访问尝试。 | Customer |
| **告警** | Test Alerts：触发一次测试告警，以确认通知传递系统运行正常。 | Joint |

当所有验证项都标记为 **Pass** 后：

1. 该部署将被正式视为 **Complete**。
2. 您可以继续进行数据迁移或应用集成。

## 后续操作 {#what-s-next}

在 {{{ .byoc }}} 部署通过验证后，您可以将应用程序连接到该实例、迁移数据，或继续配置监控、备份和安全等运维能力。要进一步减少部署期间授予的权限，请参见[TiDB Cloud BYOC Security Hardening](/tidb-cloud/byoc/security-hardening.md)。