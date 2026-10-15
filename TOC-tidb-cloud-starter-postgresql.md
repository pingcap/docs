<!-- markdownlint-disable MD007 -->
<!-- markdownlint-disable MD041 -->

# 目录

## 快速开始 {#get-started}

- 为什么选择 TiDB Cloud
  - [简介](/tidb-cloud/tidb-cloud-intro.md)
  - [功能特性](/tidb-cloud/features.md)
  - [PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)
- 快速开始
  - [试用 TiDB Cloud Starter](/tidb-cloud/starter/pg-quickstart.md)

## 指南 {#guides}

- [选择方案](/tidb-cloud/select-cluster-tier.md)
- [管理 TiDB Cloud 资源和项目](/tidb-cloud/manage-projects-and-resources.md)
- 管理 {{{ .starter }}} 实例
  - [创建 {{{ .starter }}} 实例](/tidb-cloud/create-tidb-cluster-serverless.md)
  - [通过公共端点连接到你的 {{{ .starter }}} 实例](/tidb-cloud/connect-via-standard-connection-serverless.md)
  - [备份和恢复 TiDB Cloud 数据](/tidb-cloud/backup-and-restore-serverless.md)
  - 监控和告警
    - [概览](/tidb-cloud/monitor-tidb-cluster.md)
    - [内置指标](/tidb-cloud/starter/built-in-monitoring-pg.md)
    - [Events](/tidb-cloud/tidb-cloud-events.md)
  - [删除 {{{ .starter }}} 实例](/tidb-cloud/delete-tidb-cluster.md)
- [从 PostgreSQL 迁移到 TiDB Cloud Starter](/tidb-cloud/starter/import-with-psql.md)
- 安全
  - [Security Overview](/tidb-cloud/security-overview.md)
  - 身份访问控制
    - [密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)
    - [标准 SSO 认证](/tidb-cloud/tidb-cloud-sso-authentication.md)
    - [组织 SSO 认证](/tidb-cloud/tidb-cloud-org-sso-authentication.md)
    - [身份访问管理](/tidb-cloud/manage-user-access.md)
    - [OAuth 2.0](/tidb-cloud/oauth2.md)
  - 网络访问控制
    - [到 TiDB Cloud 的 TLS 连接](/tidb-cloud/secure-connections-to-serverless-clusters.md)
  - 审计管理
    - [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)

## 参考 {#reference}

- PostgreSQL 扩展
  - [PostgreSQL 扩展](/tidb-cloud/starter/pg-extensions-overview.md)
  - [向量搜索](/tidb-cloud/starter/pg-vector-search.md)
  - [全文搜索](/tidb-cloud/starter/pg-full-text-search.md)
  - [导入 Parquet 数据](/tidb-cloud/starter/pg-parquet-import.md)
- SQL 参考
  - [概览](/tidb-cloud/starter/pg-sql-reference-overview.md)
  - [DDL](/tidb-cloud/starter/pg-ddl.md)
  - [DML 和查询](/tidb-cloud/starter/pg-dml-queries.md)
  - [数据类型](/tidb-cloud/starter/pg-data-types.md)
  - [内置函数](/tidb-cloud/starter/pg-built-in-functions.md)
  - [高级 SQL](/tidb-cloud/starter/pg-advanced-sql.md)
  - [PostgreSQL 身份验证和角色](/tidb-cloud/starter/pg-auth-roles.md)
  - [事务和 COPY](/tidb-cloud/starter/pg-transactions-copy.md)
  - [会话参数](/tidb-cloud/starter/pg-session-parameters.md)
  - [系统目录](/tidb-cloud/starter/pg-system-catalog.md)
  - [PostgreSQL 行级安全](/tidb-cloud/starter/pg-row-level-security.md)
  - [PostgreSQL 限制与约束](/tidb-cloud/starter/pg-limits-constraints.md)
- 通用参考
  - TiDB 经典架构
    - [概览](/tidb-architecture.md)
    - [存储](/tidb-storage.md)
    - [计算](/tidb-computing.md)
    - [调度](/tidb-scheduling.md)
    - [TSO](/tso.md)
  - [TiDB X 架构](/tidb-cloud/tidb-x-architecture.md)
  - 存储引擎
    - TiKV
      - [TiKV 概述](/tikv-overview.md)
      - [RocksDB 概述](/storage-engine/rocksdb-overview.md)
    - TiFlash
      - [TiFlash 概述](/tiflash/tiflash-overview.md)
      - [落盘](/tiflash/tiflash-spill-disk.md)
  - TiDB Cloud 合作伙伴 Web 控制台
    - [TiDB Cloud 合作伙伴](/tidb-cloud/tidb-cloud-partners.md)
    - [MSP 客户](/tidb-cloud/managed-service-provider-customer.md)
    - [代理商的客户](/tidb-cloud/cppo-customer.md)
  - [{{{ .starter }}} 和 Essential 的限制](/tidb-cloud/serverless-limitations.md)
  - [TiDB X 实例上的受限 SQL 功能](/tidb-cloud/limited-sql-features-tidb-x.md)
  - [TiDB 限制](/tidb-limitations.md)
  - [系统变量](/system-variables.md)
  - [Server Status Variables](/status-variables.md)
  - [Table Filter](/table-filter.md)
  - [外部存储服务的 URI 格式](/external-storage-uri.md)
  - [排查数据与索引不一致问题](/troubleshoot-data-inconsistency-errors.md)
  - [通知](/tidb-cloud/notifications.md)
- 支持计划
  - [Connected Care 概览](/tidb-cloud/connected-care-overview.md)
  - [Connected Care 详情](/tidb-cloud/connected-care-detail.md)
  - Connected Care 支持服务功能
    - [Connected: IM 中的 AI Chat](/tidb-cloud/connected-ai-chat-in-im.md)
    - Connected: TiDB Cloud Alerts 的 IM 订阅
      - [通过 Slack 订阅](/tidb-cloud/monitor-alert-slack.md)
      - [通过 Zoom 订阅](/tidb-cloud/monitor-alert-zoom.md)
      - [通过 Flashduty 订阅](/tidb-cloud/monitor-alert-flashduty.md)
      - [通过 PagerDuty 订阅](/tidb-cloud/monitor-alert-pagerduty.md)
      - [通过 Webhook 订阅](/tidb-cloud/monitor-alert-webhook.md)
      - [通过 Lark 订阅](/tidb-cloud/monitor-alert-lark.md)
    - Connected: 工单创建与修改订阅的 IM 集成
      - [通过 Slack 创建工单并订阅工单更新](/tidb-cloud/connected-slack-ticket-creation.md)
      - [通过 Lark 创建工单并订阅工单更新](/tidb-cloud/connected-lark-ticket-creation.md)
    - Connected: 支持工单的 IM 交互
      - [通过 Slack 与支持工单交互](/tidb-cloud/connected-slack-ticket-interaction.md)
      - [通过 Lark 交互支持工单](/tidb-cloud/connected-lark-ticket-interaction.md)
  - [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)
- 常见问题
  - [TiDB Cloud 常见问题](/tidb-cloud/tidb-cloud-faq.md)
  - [PostgreSQL 兼容的 TiDB Cloud Starter 常见问题](/tidb-cloud/starter/pg-faq.md)
- [术语表](/tidb-cloud/tidb-cloud-glossary.md)