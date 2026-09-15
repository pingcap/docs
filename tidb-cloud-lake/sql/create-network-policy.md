---
title: CREATE NETWORK POLICY
summary: 在 {{{ .lake }}} 中创建新的网络策略。
---

# CREATE NETWORK POLICY

在 {{{ .lake }}} 中创建新的网络策略。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] NETWORK POLICY [ IF NOT EXISTS ] <policy_name>
    ALLOWED_IP_LIST = ( 'allowed_ip1', 'allowed_ip2', ... )
    [ BLOCKED_IP_LIST = ( 'blocked_ip1', 'blocked_ip2', ...) ]
    [ COMMENT = 'comment' ]
```

| 参数            | 描述                                                                                                                                                                                       |
|----------------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| policy_name      | 指定要创建的网络策略名称。                                                                                                                                           |
| ALLOWED_IP_LIST  | 指定策略允许的 IP 地址范围列表，多个地址范围之间以逗号分隔。与此策略关联的用户可以使用指定的 IP 范围访问网络。                     |
| BLOCKED_IP_LIST  | 指定策略阻止的 IP 地址范围列表，多个地址范围之间以逗号分隔。与此策略关联的用户仍然可以从 ALLOWED_IP_LIST 中的 IP 范围访问网络，但 BLOCKED_IP_LIST 中指定的 IP 将被限制访问。  |
| COMMENT          | 可选参数，用于为网络策略添加描述或注释。                                                                                                                |

## 示例 {#examples}

以下示例演示了如何创建一个包含指定允许和阻止 IP 地址的网络策略，然后将该策略与用户关联以控制网络访问。该网络策略允许从 192.168.1.0 到 192.168.1.255 的所有 IP 地址，但特定 IP 地址 192.168.1.99 除外。

```sql
-- Create a network policy
CREATE NETWORK POLICY sample_policy
    ALLOWED_IP_LIST=('192.168.1.0/24')
    BLOCKED_IP_LIST=('192.168.1.99')
    COMMENT='Sample';

SHOW NETWORK POLICIES;

Name         |Allowed Ip List          |Blocked Ip List|Comment    |
-------------+-------------------------+---------------+-----------+
sample_policy|192.168.1.0/24           |192.168.1.99   |Sample     |

-- Create a user
CREATE USER sample_user IDENTIFIED BY 'datalake';

-- Associate the network policy with the user
ALTER USER sample_user WITH SET NETWORK POLICY='sample_policy';
```