---
title: 密码策略
summary: 本页按功能分类，全面介绍 {{{ .lake }}} 中 Password Policy 的相关操作，便于快速查阅。
---

# 密码策略

本页按功能分类，全面介绍 {{{ .lake }}} 中 Password Policy 的相关操作，便于快速查阅。

## 密码策略管理 {#password-policy-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE PASSWORD POLICY](/tidb-cloud-lake/sql/create-password-policy.md) | 创建具有特定要求的新密码策略 |
| [ALTER PASSWORD POLICY](/tidb-cloud-lake/sql/alter-password-policy.md) | 修改现有密码策略 |
| [DROP PASSWORD POLICY](/tidb-cloud-lake/sql/drop-password-policy.md) | 删除密码策略 |

## 密码策略信息 {#password-policy-information}

| 命令 | 描述 |
|---------|-------------|
| [DESCRIBE PASSWORD POLICY](/tidb-cloud-lake/sql/desc-password-policy.md) | 显示特定密码策略的详细信息 |
| [SHOW PASSWORD POLICIES](/tidb-cloud-lake/sql/show-password-policies.md) | 列出所有密码策略 |

## 相关主题 {#related-topics}

- [密码策略](/tidb-cloud-lake/guides/password-policy.md)

> **注意：**
>
> {{{ .lake }}} 中的密码策略可用于对用户密码强制执行安全要求，例如最小长度、复杂度和过期规则。