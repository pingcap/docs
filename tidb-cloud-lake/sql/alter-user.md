---
title: ALTER USER
summary: 修改用户账户，包括。
---

# ALTER USER

修改用户账户，包括：

- 更改用户的密码和认证类型。
- 设置或取消设置密码策略。
- 设置或取消设置网络策略。
- 设置或修改默认角色。如果未显式设置，{{{ .lake }}} 默认使用内置角色 `public` 作为默认角色。

## 语法 {#syntax}

```sql
-- Modify password / authentication type
ALTER USER <name> IDENTIFIED [ WITH auth_type ] BY '<new_password>' [ WITH MUST_CHANGE_PASSWORD = true | false ]

-- Require user to modify password at next login
ALTER USER <name> WITH MUST_CHANGE_PASSWORD = true

-- Modify password for currently logged-in user
ALTER USER USER() IDENTIFIED BY '<new_password>'

-- Set password policy
ALTER USER <name> WITH SET PASSWORD POLICY = '<policy_name>'

-- Unset password policy
ALTER USER <name> WITH UNSET PASSWORD POLICY

-- Set network policy
ALTER USER <name> WITH SET NETWORK POLICY = '<policy_name>'

-- Unset network policy
ALTER USER <name> WITH UNSET NETWORK POLICY

-- Set default role
ALTER USER <name> WITH DEFAULT_ROLE = '<role_name>'

-- Enable or disable user
ALTER USER <name> WITH DISABLED = true | false

-- Set workload group
ALTER USER <name> WITH SET WORKLOAD GROUP = '<workload_group_name>'

-- Unset workload group
ALTER USER <name> WITH UNSET WORKLOAD GROUP
```

- *auth_type* 可以是 `double_sha1_password`（默认）、`sha256_password` 或 `no_password`。
- 当 `MUST_CHANGE_PASSWORD` 设置为 `true` 时，用户必须在下次登录时修改密码。请注意，这仅对自账户创建以来从未修改过密码的用户生效。如果用户曾经自行修改过密码，则无需再次修改。
- 当你使用 [CREATE USER](/tidb-cloud-lake/sql/create-user.md) 或 ALTER USER 为用户设置默认角色时，{{{ .lake }}} 不会验证该角色是否存在，也不会自动将该角色授予用户。你必须显式将该角色授予用户，该角色才会生效。
- `DISABLED` 允许你启用或禁用用户。被禁用的用户在重新启用之前无法登录到 {{{ .lake }}}。参见[语法](/tidb-cloud-lake/sql/create-user.md#syntax)。

## 示例 {#examples}

### 示例 1：更改密码和认证类型 {#example-1-changing-password-authentication-type}

```sql
CREATE USER user1 IDENTIFIED BY 'abc123';

SHOW USERS;
+-----------+----------+----------------------+---------------+
| name      | hostname | auth_type            | is_configured |
+-----------+----------+----------------------+---------------+
| user1     | %        | double_sha1_password | NO            |
+-----------+----------+----------------------+---------------+

ALTER USER user1 IDENTIFIED WITH sha256_password BY '123abc';

SHOW USERS;
+-------+----------+-----------------+---------------+
| name  | hostname | auth_type       | is_configured |
+-------+----------+-----------------+---------------+
| user1 | %        | sha256_password | NO            |
+-------+----------+-----------------+---------------+

ALTER USER 'user1' IDENTIFIED WITH no_password;

show users;
+-------+----------+-------------+---------------+
| name  | hostname | auth_type   | is_configured |
+-------+----------+-------------+---------------+
| user1 | %        | no_password | NO            |
+-------+----------+-------------+---------------+
```

### 示例 2：设置和取消设置网络策略 {#example-2-setting-unsetting-network-policy}

```sql
SHOW NETWORK POLICIES;

Name        |Allowed Ip List          |Blocked Ip List|Comment    |
------------+-------------------------+---------------+-----------+
test_policy |192.168.10.0,192.168.20.0|               |new comment|
test_policy1|192.168.100.0/24         |               |           |

CREATE USER user1 IDENTIFIED BY 'abc123';

ALTER USER user1 WITH SET NETWORK POLICY='test_policy';

ALTER USER user1 WITH SET NETWORK POLICY='test_policy1';

ALTER USER user1 WITH UNSET NETWORK POLICY;
```

### 示例 3：设置默认角色 {#example-3-setting-default-role}

1. 创建一个名为 "user1" 的用户，并将默认角色设置为 "writer"：

    ```sql title='Connect as user "root":'
    
    CREATE USER user1 IDENTIFIED BY 'abc123';
    
    GRANT ROLE developer TO user1;
    
    GRANT ROLE writer TO user1;
    
    ALTER USER user1 WITH DEFAULT_ROLE = 'writer';
    ```

2. 使用 [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) 命令验证用户 "user1" 的默认角色：

```sql title='Connect as user "user1":'
eric@Erics-iMac ~ % lakesql --user user1 --password abc123
show roles;
┌───────────────────────────────────────────────────────┐
│    name   │ inherited_roles │ is_current │ is_default │
│   String  │      UInt64     │   Boolean  │   Boolean  │
├───────────┼─────────────────┼────────────┼────────────┤
│ developer │               0 │ false      │ false      │
│ public    │               0 │ false      │ false      │
│ writer    │               0 │ true       │ true       │
└───────────────────────────────────────────────────────┘
```

### 示例 2：设置和取消设置 Workload Group {#example-2-setting-unsetting-workload-group}

```sql
CREATE USER user1 IDENTIFIED BY 'abc123';

ALTER USER user1 WITH SET WORKLOAD GROUP='wg';

ALTER USER user1 WITH SET WORKLOAD GROUP='wg1';

ALTER USER user1 WITH UNSET WORKLOAD GROUP;
```