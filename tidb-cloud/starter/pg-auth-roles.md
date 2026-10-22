---
title: PostgreSQL の認証とロール
summary: PostgreSQL 互換の TiDB Cloud Starter でデータベースロールと権限を管理する方法を学びます。
---

# PostgreSQL の認証とロール

PostgreSQL 互換の {{{ .starter }}} は、データベースロール、ロール属性、オブジェクト権限、およびセッションロールの切り替えをサポートしています。

このページでは、データベースレベルの認証と認可について説明します。TiDB Cloud の組織、プロジェクト、およびインスタンスへのアクセスは、TiDB Cloud Identity and Access Management によって別途管理されます。

## ロールを作成する {#create-a-role}

データベースに接続できるロールを作成するには、`CREATE ROLE ... LOGIN` を使用します。

```sql
CREATE ROLE app_user
LOGIN
PASSWORD 'SecurePass1';
```

`LOGIN` を持たないロールは、権限管理のためのグループロールとして使用できます。

```sql
CREATE ROLE readonly;
```

ログインロールにグループロールを付与します。

```sql
GRANT readonly TO app_user;
```

## ロールを変更する {#alter-a-role}

ロールのパスワードを変更します。

```sql
ALTER ROLE app_user
PASSWORD 'NewSecurePass1';
```

選択したロール属性を設定または解除します。

```sql
ALTER ROLE app_user CREATEDB;
ALTER ROLE app_user NOCREATEDB;

ALTER ROLE app_user BYPASSRLS;
ALTER ROLE app_user NOBYPASSRLS;
```

以下の一般的なロール属性がサポートされています。

| 属性 | 説明 |
| --- | --- |
| `LOGIN` / `NOLOGIN` | ロールが接続できるかどうかを制御します。 |
| `CREATEDB` / `NOCREATEDB` | ロールがデータベースを作成できるかどうかを制御します。 |
| `BYPASSRLS` / `NOBYPASSRLS` | ロールが行レベルセキュリティポリシーをバイパスするかどうかを制御します。 |

`BYPASSRLS` 属性は、信頼できる管理ロールまたはサービスロールにのみ設定してください。

## テーブル権限を付与する {#grant-table-privileges}

テーブルに対して 1 つ以上の権限を付与します。

```sql
GRANT SELECT, INSERT
ON todos
TO app_user;
```

サポートされているすべてのテーブル権限を付与します。

```sql
GRANT ALL
ON todos
TO app_user;
```

スキーマ内のすべてのテーブルに対する権限を付与します。

```sql
GRANT SELECT
ON ALL TABLES IN SCHEMA public
TO readonly;
```

## テーブル権限を取り消す {#revoke-table-privileges}

以前にロールへ付与した権限を取り消します。

```sql
REVOKE INSERT
ON todos
FROM app_user;
```

テーブルに対するすべての権限を取り消します。

```sql
REVOKE ALL
ON todos
FROM app_user;
```

## スキーマ権限を付与する {#grant-schema-privileges}

ロールがスキーマ内のオブジェクトにアクセスできるようにするには、`USAGE` を使用します。

```sql
GRANT USAGE
ON SCHEMA analytics
TO app_user;
```

スキーマ内にオブジェクトを作成する権限を付与します。

```sql
GRANT CREATE
ON SCHEMA analytics
TO app_user;
```

スキーマに対して `USAGE` を付与しても、そのスキーマ内のテーブルに対する権限は自動的には付与されません。必要なテーブル権限は別途付与してください。

例:

```sql
GRANT USAGE
ON SCHEMA analytics
TO app_user;

GRANT SELECT
ON ALL TABLES IN SCHEMA analytics
TO app_user;
```

## シーケンス権限を付与する {#grant-sequence-privileges}

シーケンス権限は強制されます。

例:

```sql
GRANT USAGE, SELECT
ON SEQUENCE order_seq
TO app_user;
```

関連するシーケンス権限は次のとおりです。

| 権限 | 用途 |
| --- | --- |
| `USAGE` | `nextval()` などの一般的なシーケンス操作を許可します。 |
| `SELECT` | 該当する場合に現在のシーケンス値の読み取りを許可します。 |
| `UPDATE` | `setval()` など、シーケンス値を変更する操作に必要です。 |

たとえば、シーケンスの位置を変更する権限を付与するには、次のようにします。

```sql
GRANT UPDATE
ON SEQUENCE order_seq
TO app_user;
```

> **Note:**
>
> `SERIAL` または `BIGSERIAL` のデフォルト値を使用する非スーパーユーザーロールには、基になるシーケンスに対する `USAGE` または `UPDATE` が必要です。ただし、所有権または継承された権限によってすでにその権限が与えられている場合は除きます。テーブルに対して `INSERT` を付与するだけでは不十分です。

## 将来作成されるオブジェクトに対する権限を付与する {#grant-privileges-on-future-objects}

現在のロールによって後続で作成されるオブジェクトに対する権限を設定するには、`ALTER DEFAULT PRIVILEGES` を使用します。

たとえば、将来作成されるテーブルに対して `SELECT` を付与します。

```sql
ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT SELECT ON TABLES TO readonly;
```

明示的に作成されるシーケンスの場合:

```sql
ALTER DEFAULT PRIVILEGES
IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO app_user;
```

シーケンスに対するデフォルト権限は、`CREATE SEQUENCE` で明示的に作成されたシーケンスに適用されます。`SERIAL` または `BIGSERIAL` によって暗黙的に作成されたシーケンスには、これらのシーケンスのデフォルト権限は継承されません。

`ALTER DEFAULT PRIVILEGES ... ON FUNCTIONS` はサポートされていません。

## ロールメンバーシップを管理する {#manage-role-membership}

あるロールを別のロールに付与します。

```sql
GRANT readonly TO app_user;
```

メンバーシップを取り消します。

```sql
REVOKE readonly FROM app_user;
```

## セッションでロールを切り替える {#switch-roles-in-a-session}

`SET ROLE` を使用して、現在のセッションユーザーに付与されているロールへ切り替えます。

```sql
SET ROLE app_user;
```

元の認証済みロールに戻します。

```sql
RESET ROLE;
```

ロールの切り替えは強制されます。現在のユーザーに付与されていないロールには `SET ROLE` できません。

現在のロールとセッションロールを確認します。

```sql
SELECT CURRENT_USER, SESSION_USER;
```

## ロールと権限を確認する {#inspect-roles-and-privileges}

データベースロールを一覧表示します。

```sql
SELECT
    rolname,
    rolcanlogin,
    rolcreatedb,
    rolbypassrls
FROM pg_roles
ORDER BY rolname;
```

ロールメンバーシップを一覧表示します。

```sql
SELECT
    member_role.rolname AS member,
    granted_role.rolname AS granted_role
FROM pg_auth_members AS m
JOIN pg_roles AS member_role
    ON member_role.oid = m.member
JOIN pg_roles AS granted_role
    ON granted_role.oid = m.roleid
ORDER BY member_role.rolname, granted_role.rolname;
```

テーブル権限を一覧表示します。

```sql
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public'
ORDER BY table_name, grantee, privilege_type;
```

## ロールを削除する {#drop-a-role}

ロールを削除する前に、そのロールが所有するオブジェクトや、そのロールに付与されている権限などの依存関係を解消します。

例:

```sql
REVOKE SELECT ON todos FROM app_user;
REVOKE USAGE ON SCHEMA public FROM app_user;
```

その後、ロールを削除します。

```sql
DROP ROLE app_user;
```

## 行レベルセキュリティ {#row-level-security}

データベースロールは、行レベルセキュリティポリシーから参照できます。

例:

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

CREATE POLICY app_user_todos
ON todos
FOR SELECT
TO app_user
USING (user_id = current_user);
```

RLS の完全な構文と動作については、[PostgreSQL の行レベルセキュリティ](/tidb-cloud/starter/pg-row-level-security.md) を参照してください。