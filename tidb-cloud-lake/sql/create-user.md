---
title: CREATE USER
summary: "{{{ .lake }}} に接続するための SQL ユーザーを作成します。ユーザーがデータベースにアクセスして操作を実行するには、適切な権限を付与する必要があります。"
---

# CREATE USER

{{{ .lake }}} に接続するための SQL ユーザーを作成します。ユーザーがデータベースにアクセスして操作を実行するには、適切な権限を付与する必要があります。

関連情報:

- [GRANT](/tidb-cloud-lake/sql/grant.md)
- [ALTER USER](/tidb-cloud-lake/sql/alter-user.md)
- [DROP USER](/tidb-cloud-lake/sql/drop-user.md)

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] USER <name> IDENTIFIED [ WITH <auth_type> ] BY '<password>'
[ WITH MUST_CHANGE_PASSWORD = true | false ]
[ WITH SET PASSWORD POLICY = '<policy_name>' ]
[ WITH SET NETWORK POLICY = '<policy_name>' ]
[ WITH DEFAULT_ROLE = '<role_name>' ]
[ WITH DISABLED = true | false ]
```

**パラメーター:**

- `<name>`: ユーザー名（シングルクォート、ダブルクォート、バックスペース、またはフォームフィード文字を含めることはできません）
- `<auth_type>`: 認証タイプ - `double_sha1_password`（デフォルト）、`sha256_password`、または `no_password`
- `MUST_CHANGE_PASSWORD`: `true` の場合、ユーザーは初回ログイン時にパスワードを変更する必要があります
- `DEFAULT_ROLE`: デフォルトロールを設定します（有効にするには、そのロールを明示的に付与する必要があります）
- `DISABLED`: `true` の場合、ユーザーは無効状態で作成され、ログインできません

## 例 {#examples}

### 例 1: すべてのデータベースに対するフルアクセス {#example-1-full-access-across-all-databases}

すべてのデータベースに対して完全な読み取り/書き込みアクセスを持つユーザーを作成します。

```sql
-- Create a role with global access
CREATE ROLE full_access_role;
GRANT ALL ON *.* TO ROLE full_access_role;

-- Create the user and assign the role
CREATE USER admin_user IDENTIFIED BY 'SecurePass456!' WITH DEFAULT_ROLE = 'full_access_role';
GRANT ROLE full_access_role TO admin_user;
```

### 例 2: すべてのデータベースに対する読み取り専用アクセス {#example-2-read-only-access-across-all-databases}

データのクエリのみを実行できるユーザーを作成します。ダッシュボードや BI ツールに適しています。

```sql
-- Create a read-only role
CREATE ROLE readonly_role;
GRANT SELECT ON *.* TO ROLE readonly_role;

-- Create the user
CREATE USER readonly_user IDENTIFIED BY 'ReadOnly789!' WITH DEFAULT_ROLE = 'readonly_role';
GRANT ROLE readonly_role TO readonly_user;
```

### 例 3: 単一データベースへのアクセス {#example-3-single-database-access}

ロールを作成し、データベース権限を付与して、そのロールをユーザーに割り当てます。

```sql
-- Create a role and grant database privileges
CREATE ROLE data_analyst_role;
GRANT SELECT, INSERT ON default.* TO ROLE data_analyst_role;

-- Create a new user and assign the role
CREATE USER data_analyst IDENTIFIED BY 'secure_password123' WITH DEFAULT_ROLE = 'data_analyst_role';
GRANT ROLE data_analyst_role TO data_analyst;
```

ロールと権限を確認します。

```sql
SHOW GRANTS FOR ROLE data_analyst_role;
+-----------------------------------------------------------------+
| Grants                                                          |
+-----------------------------------------------------------------+
| GRANT SELECT,INSERT ON 'default'.* TO ROLE  'data_analyst_role' |
+-----------------------------------------------------------------+
```

### 例 4: 異なる認証タイプでユーザーを作成する {#example-4-create-users-with-different-authentication-types}

```sql
-- Create user with default authentication
CREATE USER user1 IDENTIFIED BY 'abc123';

-- Create user with SHA256 authentication
CREATE USER user2 IDENTIFIED WITH sha256_password BY 'abc123';
```