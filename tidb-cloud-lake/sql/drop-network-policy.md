---
title: DROP NETWORK POLICY
summary: 从 {{{ .lake }}} 中删除现有的网络策略。删除网络策略后，该策略会从 {{{ .lake }}} 中移除，其关联的允许和阻止 IP 地址列表规则也将不再生效。请注意，在删除网络策略之前，请确保该策略未与任何用户关联。
---

# DROP NETWORK POLICY

从 {{{ .lake }}} 中删除现有的网络策略。删除网络策略后，该策略会从 {{{ .lake }}} 中移除，其关联的允许和阻止 IP 地址列表规则也将不再生效。请注意，在删除网络策略之前，请确保该策略未与任何用户关联。

## 语法 {#syntax}

```sql
DROP NETWORK POLICY [ IF EXISTS ] <policy_name>
```

## 示例 {#examples}

```sql
DROP NETWORK POLICY test_policy
```