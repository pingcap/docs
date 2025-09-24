---
title: Security Overview
summary: 了解 TiDB Cloud 的全面安全框架，包括身份管理、网络隔离、数据保护、访问控制和审计。
---

# Security Overview

TiDB Cloud 提供了全面且灵活的安全框架，覆盖数据生命周期的所有阶段。该平台在身份与访问管理、网络安全与隔离、数据访问控制、数据库访问控制以及审计日志等方面，均提供了全方位的保护。

## 身份与访问管理

TiDB Cloud 支持多种身份验证方式，包括 [邮箱和密码登录](/tidb-cloud/tidb-cloud-password-authentication.md)、[标准 SSO](/tidb-cloud/tidb-cloud-sso-authentication.md) 和 [组织级 SSO](/tidb-cloud/tidb-cloud-org-sso-authentication.md)。

TiDB Cloud 提供分层的角色与权限管理，并且你可以启用多因素认证（MFA）以增强账户安全性。灵活的 [身份与访问控制](/tidb-cloud/manage-user-access.md) 让你能够通过细粒度权限管理项目和资源访问，确保你可以始终遵循最小权限原则。

## 网络安全与隔离

TiDB Cloud 提供私有终端节点、VPC Peering 以及 IP 访问列表，用于实现网络隔离和访问控制。

你可以通过 TLS 加密所有通信，确保数据在传输过程中的机密性和完整性。网络访问控制确保只有授权来源能够访问集群资源，从而提升整体安全性。

## 数据访问控制

对于支持客户自管加密密钥（CMEK）的集群类型，TiDB Cloud 为静态数据和备份数据提供加密保护。

结合强大的密钥管理机制，你可以控制加密密钥的生命周期和使用方式，进一步提升数据安全性和合规性。

更多信息，请参见 [在 AWS 上使用客户自管加密密钥进行静态数据加密](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md) 和 [在 Azure 上使用客户自管加密密钥进行静态数据加密](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md)。

## 数据库访问控制

TiDB Cloud 提供基于用户和角色的访问控制机制，结合静态和动态权限。你可以为用户分配角色，以更细粒度地管理和分发权限。

对于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，你可以 [配置和管理 root 账户密码](/tidb-cloud/configure-security-settings.md)，并通过 [IP 访问列表](/tidb-cloud/configure-ip-access-list.md) 限制访问，以保护敏感账户。

## 审计日志

TiDB Cloud 为控制台和数据库操作都提供了审计日志，以支持活动追踪、合规监控和安全事件调查。

审计日志会记录你的操作、操作时间和来源，为企业安全管理提供可靠的证据。