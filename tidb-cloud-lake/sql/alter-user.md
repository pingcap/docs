---
title: ALTER USER
summary: ユーザーアカウントを変更します。内容は以下を含みます。
---

# ALTER USER

ユーザーアカウントを変更します。内容は以下を含みます。

- ユーザーのパスワードと認証タイプの変更。
- パスワードポリシーの設定または解除。
- ネットワークポリシーの設定または解除。
- デフォルトロールの設定または変更。明示的に設定されていない場合、{{{ .lake }}} は組み込みロール `public` をデフォルトロールとして使用します。

## 構文 {#syntax}

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

- *auth_type* には `double_sha1_password`（デフォルト）、`sha256_password`、または `no_password` を指定できます。
- `MUST_CHANGE_PASSWORD` を `true` に設定すると、ユーザーは次回ログイン時にパスワードを変更する必要があります。これは、アカウント作成後に一度もパスワードを変更したことがないユーザーに対してのみ有効です。ユーザーが自分で一度でもパスワードを変更したことがある場合は、再度変更する必要はありません。
- [CREATE USER](/tidb-cloud-lake/sql/create-user.md) または ALTER USER を使用してユーザーのデフォルトロールを設定しても、{{{ .lake }}} はそのロールの存在を検証せず、ユーザーにそのロールを自動的に付与もしません。ロールを有効にするには、そのロールをユーザーに明示的に付与する必要があります。
- `DISABLED` を使用すると、ユーザーを有効または無効にできます。無効化されたユーザーは、有効化されるまで {{{ .lake }}} にログインできません。[構文](/tidb-cloud-lake/sql/create-user.md#syntax) を参照してください。

## 例 {#examples}

### 例 1: パスワードと認証タイプの変更 {#example-1-changing-password-authentication-type}

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

### 例 2: ネットワークポリシーの設定と解除 {#example-2-setting-unsetting-network-policy}

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

### 例 3: デフォルトロールの設定 {#example-3-setting-default-role}

1. "user1" という名前のユーザーを作成し、デフォルトロールを "writer" に設定します。

    ```sql title='Connect as user "root":'
    
    CREATE USER user1 IDENTIFIED BY 'abc123';
    
    GRANT ROLE developer TO user1;
    
    GRANT ROLE writer TO user1;
    
    ALTER USER user1 WITH DEFAULT_ROLE = 'writer';
    ```

2. [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) コマンドを使用して、ユーザー "user1" のデフォルトロールを確認します。

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

### 例 2: Workload Group の設定と解除 {#example-2-setting-unsetting-workload-group}

```sql
CREATE USER user1 IDENTIFIED BY 'abc123';

ALTER USER user1 WITH SET WORKLOAD GROUP='wg';

ALTER USER user1 WITH SET WORKLOAD GROUP='wg1';

ALTER USER user1 WITH UNSET WORKLOAD GROUP;
```