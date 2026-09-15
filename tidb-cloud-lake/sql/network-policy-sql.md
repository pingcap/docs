---
title: 网络策略
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的网络策略操作，便于参考。
---

# 网络策略

本页按功能分类，全面概述了 {{{ .lake }}} 中的网络策略操作，便于参考。

## 网络策略管理 {#network-policy-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE NETWORK POLICY](/tidb-cloud-lake/sql/create-network-policy.md) | 创建新的网络策略，以基于 IP 地址控制访问 |
| [ALTER NETWORK POLICY](/tidb-cloud-lake/sql/alter-network-policy.md) | 修改现有网络策略 |
| [DROP NETWORK POLICY](/tidb-cloud-lake/sql/drop-network-policy.md) | 删除网络策略 |

## 网络策略信息 {#network-policy-information}

| 命令 | 描述 |
|---------|-------------|
| [DESCRIBE NETWORK POLICY](/tidb-cloud-lake/sql/desc-network-policy.md) | 显示特定网络策略的详细信息 |
| [SHOW NETWORK POLICIES](/tidb-cloud-lake/sql/show-network-policies.md) | 列出所有网络策略 |

## 相关主题 {#related-topics}

- [网络策略](/tidb-cloud-lake/guides/network-policy.md)

> **注意：**
>
> {{{ .lake }}} 中的网络策略允许你通过指定允许或阻止的 IP 地址及地址范围来控制对数据库的访问。