---
title: SHOW NETWORK POLICIES
summary: 显示 {{{ .lake }}} 中所有现有网络策略的列表。它会提供可用网络策略的信息，包括其名称，以及是否配置了允许或阻止的 IP 地址列表。
---

# SHOW NETWORK POLICIES

显示 {{{ .lake }}} 中所有现有网络策略的列表。它会提供可用网络策略的信息，包括其名称，以及是否配置了允许或阻止的 IP 地址列表。

## 语法 {#syntax}

```sql
SHOW NETWORK POLICIES
```

## 示例 {#examples}

```sql
SHOW NETWORK POLICIES;

Name        |Allowed Ip List |Blocked Ip List|Comment     |
------------+----------------+---------------+------------+
test_policy |192.168.1.0/24  |192.168.1.99   |test comment|
test_policy1|192.168.100.0/24|               |            |
```