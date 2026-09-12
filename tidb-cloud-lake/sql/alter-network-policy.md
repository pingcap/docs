---
title: ALTER NETWORK POLICY
summary: 修改 {{{ .lake }}} 中现有的网络策略。
---

# ALTER NETWORK POLICY

修改 {{{ .lake }}} 中现有的网络策略。

## 语法 {#syntax}

```sql
ALTER NETWORK POLICY [ IF EXISTS ] <policy_name>
    SET [ ALLOWED_IP_LIST = ('allowed_ip1', 'allowed_ip2', ...) ]
    [ BLOCKED_IP_LIST = ('blocked_ip1', 'blocked_ip2', ...) ]
    [ COMMENT = 'comment' ]
```

| 参数 | 描述 |
|----------------- |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| policy_name      | 指定要修改的网络策略名称。                                                                                                                                                                                                               |
| ALLOWED_IP_LIST  | 指定要为该策略修改的、以逗号分隔的允许 IP 地址范围列表。这会用新提供的列表覆盖现有的允许 IP 地址列表。                                                                                                |
| BLOCKED_IP_LIST  | 指定要为该策略修改的、以逗号分隔的阻止 IP 地址范围列表。这会用新提供的列表覆盖现有的阻止 IP 地址列表。如果将此参数设置为空列表 `()`，则会移除所有阻止 IP 地址限制。  |
| COMMENT          | 可选参数，用于修改与网络策略关联的描述或注释。                                                                                                                                                                    |

> **注意：**
>
> 此命令支持灵活地仅修改允许 IP 列表或阻止 IP 列表中的任意一个，同时保持另一个列表不变。`ALLOWED_IP_LIST` 和 `BLOCKED_IP_LIST` 都是可选参数。

## 示例 {#examples}

```sql
-- Modify the network policy test_policy to change the blocked IP address list from ('192.168.1.99') to ('192.168.1.10'):
ALTER NETWORK POLICY test_policy SET BLOCKED_IP_LIST=('192.168.1.10')

-- Update the network policy test_policy to allow IP address ranges ('192.168.10.0', '192.168.20.0') and remove any blocked IP address restrictions. Also, change the comment to 'new comment':

ALTER NETWORK POLICY test_policy SET ALLOWED_IP_LIST=('192.168.10.0', '192.168.20.0') BLOCKED_IP_LIST=() COMMENT='new comment'
```