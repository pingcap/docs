---
title: 安全性与可靠性
summary: "{{{ .lake }}} 提供企业级的安全性与可靠性功能，在数据的整个生命周期内为其保驾护航。从控制谁可以访问您的数据，到防御网络威胁，再到从操作错误中恢复，{{{ .lake }}} 的多层安全方法可帮助您维护数据完整性、合规性和业务可持续性。"
---

# 安全性与可靠性

{{{ .lake }}} 提供**企业级的安全性与可靠性功能**，在数据的整个生命周期内为其保驾护航。从控制谁可以访问您的数据，到防御网络威胁，再到从操作错误中恢复，{{{ .lake }}} 的**多层安全方法**可帮助您维护数据完整性、合规性和业务可持续性。

| 安全功能 | 用途 | 何时使用 |
|-----------------|---------|------------|
| [**访问控制**](/tidb-cloud-lake/guides/access-control.md) | 管理用户权限 | 当您需要通过基于角色的安全机制和对象所有权来控制数据访问时 |
| [**数据保护策略**](/tidb-cloud-lake/guides/data-protection-policies.md) | 在行级和列级保护敏感数据 | 当您需要行级过滤、列级脱敏或同时需要两者时 |
| [**审计追踪**](/tidb-cloud-lake/guides/audit-trail.md) | 跟踪数据库活动 | 当您需要全面的审计跟踪以进行安全监控、合规和性能分析时 |
| [**网络策略**](/tidb-cloud-lake/guides/network-policy.md) | 限制网络访问 | 当您希望即使在凭证有效的情况下，也仅允许来自特定 IP 范围的连接时 |
| [**密码策略**](/tidb-cloud-lake/guides/password-policy.md) | 设置密码要求 | 当您需要强制执行密码复杂度、轮换和账户锁定规则时 |
| [**使用 AWS IAM Role 进行认证**](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md) | 使用 AWS IAM 角色进行身份验证 | 当您希望利用 AWS IAM 安全访问 {{{ .lake }}} 时 |
| [**合规与安全**](/tidb-cloud-lake/guides/compliance-security.md) | 确保监管合规 | 当您需要遵循行业标准和法规时 |
| [**Fail-Safe**](/tidb-cloud-lake/guides/fail-safe.md) | 防止数据丢失 | 当您需要从兼容 S3 的存储中恢复被意外删除的数据时 |
| [**从操作错误中恢复**](/tidb-cloud-lake/guides/recovery-from-operational-errors.md) | 修复操作失误 | 当您需要从已删除的数据库/表或错误的数据修改中恢复时 |