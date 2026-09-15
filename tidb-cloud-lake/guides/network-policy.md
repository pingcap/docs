---
title: 网络策略
summary: 网络策略根据客户端 IP 控制谁可以登录 {{{ .lake }}}。即使凭据正确，如果连接请求的 IP 不满足策略，也会被拒绝，从而在用户名和密码之外为你提供额外的一层安全保护。
---

# 网络策略

网络策略根据客户端 IP 控制谁可以登录 {{{ .lake }}}。即使凭据正确，如果连接请求的 IP 不满足策略，也会被拒绝，从而在用户名和密码之外为你提供额外的一层安全保护。

## 工作原理 {#how-it-works}

- `ALLOWED_IP_LIST` 接受单个 IPv4 地址或 CIDR 网段（例如 `10.0.0.0/24`）。只有列表中的地址才允许登录。
- `BLOCKED_IP_LIST`（可选）允许你从已允许的范围中进一步明确指定拒绝规则。{{{ .lake }}} 会先检查阻止列表，因此同时存在于两个列表中的 IP 仍会被拒绝。
- 一个用户在同一时间最多只能引用一个网络策略，但同一个策略可以被多个用户共享，以便于管理。
- 如果服务器无法确定客户端 IP，或者该 IP 与允许列表不匹配，{{{ .lake }}} 会立即返回 `AuthenticateFailure`。

## 端到端示例 {#end-to-end-example}

以下演练涵盖了典型的生命周期：创建策略、将其绑定到用户、确认其状态、集中修改策略，最后解绑并删除策略。

### 1. 创建并查看策略 {#1-create-and-inspect-a-policy}

```sql
CREATE NETWORK POLICY corp_vpn_policy
    ALLOWED_IP_LIST=('10.1.0.0/16', '172.16.8.12/32')
    BLOCKED_IP_LIST=('10.1.10.25')
    COMMENT='Only VPN ranges';

SHOW NETWORK POLICIES;

Name            |Allowed Ip List           |Blocked Ip List|Comment          |
----------------+--------------------------+---------------+-----------------+
corp_vpn_policy |10.1.0.0/16,172.16.8.12/32|10.1.10.25     |Only VPN ranges  |
```

### 2. 将策略绑定到用户 {#2-attach-the-policy-to-users}

```sql
CREATE USER alice IDENTIFIED BY 'Str0ngPass!' WITH SET NETWORK POLICY='corp_vpn_policy';
CREATE USER bob IDENTIFIED BY 'An0therPass!';

-- Apply the policy to an existing user
ALTER USER bob WITH SET NETWORK POLICY='corp_vpn_policy';
```

### 3. 验证策略是否生效 {#3-verify-enforcement}

```sql
DESC USER alice;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │ hostname │       auth_type      │ default_role │ roles │ disabled │   network_policy  │ password_policy │ must_change_password │
├────────┼──────────┼──────────────────────┼──────────────┼───────┼──────────┼───────────────────┼─────────────────┼──────────────────────┤
│ alice  │ %        │ double_sha1_password │              │       │ false    │ corp_vpn_policy   │                 │ NULL                 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

DESC NETWORK POLICY corp_vpn_policy;

Name            |Allowed Ip List           |Blocked Ip List|Comment         |
----------------+--------------------------+---------------+----------------+
corp_vpn_policy |10.1.0.0/16,172.16.8.12/32|10.1.10.25     |Only VPN ranges |
```

### 4. 修改并复用策略 {#4-update-and-reuse-the-policy}

使用 [ALTER NETWORK POLICY](/tidb-cloud-lake/sql/network-policy-sql.md) 可以调整允许或阻止的 IP，而无需逐个修改用户：

```sql
ALTER NETWORK POLICY corp_vpn_policy
    SET ALLOWED_IP_LIST=('10.1.0.0/16', '10.2.0.0/16')
        BLOCKED_IP_LIST=('10.1.10.25', '10.2.5.5')
        COMMENT='VPN + DR site';

DESC NETWORK POLICY corp_vpn_policy;

Name            |Allowed Ip List             |Blocked Ip List          |Comment          |
----------------+----------------------------+-------------------------+-----------------+
corp_vpn_policy |10.1.0.0/16,10.2.0.0/16     |10.1.10.25,10.2.5.5      |VPN + DR site    |
```

所有引用该策略的用户都会自动获取新的 IP 范围。

### 5. 解绑并清理 {#5-detach-and-clean-up}

```sql
ALTER USER bob WITH UNSET NETWORK POLICY;
DROP NETWORK POLICY corp_vpn_policy;
```

删除策略前，请确认没有用户依赖该策略；否则，这些用户将无法登录。

---

有关完整的语法详情，请参见 [网络策略 SQL 参考](/tidb-cloud-lake/sql/network-policy-sql.md)，其中涵盖了 `CREATE`、`ALTER`、`SHOW`、`DESC` 和 `DROP`。