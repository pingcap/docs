---
title: DESC NETWORK POLICY
summary: 显示 {{{ .lake }}} 中特定网络策略的详细信息。它会提供与该策略关联的允许和阻止 IP 地址列表，以及用于描述该策略用途或函数的注释（如果有）。
---

# DESC NETWORK POLICY

显示 {{{ .lake }}} 中特定网络策略的详细信息。它会提供与该策略关联的允许和阻止 IP 地址列表，以及用于描述该策略用途或函数的注释（如果有）。

## 语法 {#syntax}

```sql
DESC NETWORK POLICY <policy_name>
```

## 示例 {#examples}

```sql
DESC NETWORK POLICY test_policy;

Name       |Allowed Ip List          |Blocked Ip List|Comment    |
-----------+-------------------------+---------------+-----------+
test_policy|192.168.10.0,192.168.20.0|               |new comment|
```