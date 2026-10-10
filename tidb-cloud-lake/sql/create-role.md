---
title: CREATE ROLE
summary: アクセス制御のための新しいロールを作成します。ロールは権限をグループ化するために使用され、ユーザーまたは他のロールに割り当てることができるため、{{{ .lake }}} で権限を柔軟に管理できます。
---

# CREATE ROLE

アクセス制御のための新しいロールを作成します。ロールは権限をグループ化するために使用され、ユーザーまたは他のロールに割り当てることができるため、{{{ .lake }}} で権限を柔軟に管理できます。

## 構文 {#syntax}

```sql
CREATE ROLE [ IF NOT EXISTS ] <name>
```

**Parameters:**

- `IF NOT EXISTS`: ロールが存在しない場合にのみ作成します（エラーを避けるため推奨）
- `<name>`: ロール名（シングルクォート、ダブルクォート、バックスペース、またはフォームフィード文字を含めることはできません）

## 例 {#examples}

```sql
-- Create a basic role
CREATE ROLE analyst;

-- Create role only if it doesn't exist (recommended)
CREATE ROLE IF NOT EXISTS data_viewer;
```

## 一般的な使用パターン {#common-usage-patterns}

### 読み取り専用アナリストロール {#read-only-analyst-role}

売上データへの読み取りアクセスが必要なデータアナリスト向けのロールを作成します。

```sql
-- Create the analyst role
CREATE ROLE sales_analyst;

-- Grant read permissions
GRANT SELECT ON sales_db.* TO ROLE sales_analyst;

-- Assign to users
GRANT ROLE sales_analyst TO 'alice';
GRANT ROLE sales_analyst TO 'bob';
```

### データベース管理者ロール {#database-administrator-role}

完全な制御が必要な管理者向けのロールを作成します。

```sql
-- Create the admin role
CREATE ROLE sales_admin;

-- Grant full permissions on the database
GRANT ALL ON sales_db.* TO ROLE sales_admin;

-- Grant user management permissions
GRANT CREATE USER, CREATE ROLE ON *.* TO ROLE sales_admin;

-- Assign to admin users
GRANT ROLE sales_admin TO 'admin_user';
```

### 検証 {#verification}

```sql
-- Check what each role can do
SHOW GRANTS FOR ROLE sales_analyst;
SHOW GRANTS FOR ROLE sales_admin;

-- Check user permissions
SHOW GRANTS FOR 'alice';
SHOW GRANTS FOR 'admin_user';
```

## 関連項目 {#see-also}

- [GRANT](/tidb-cloud-lake/sql/grant.md) - 権限とロールを付与します
- [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md) - 付与された権限を表示します
- [DROP ROLE](/tidb-cloud-lake/sql/drop-role.md) - ロールを削除します