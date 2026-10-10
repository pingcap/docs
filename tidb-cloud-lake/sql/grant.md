---
title: GRANT
summary: 特定のデータベースオブジェクトに対する権限、ロール、および所有権を付与します。これには以下が含まれます。
---

# GRANT

特定のデータベースオブジェクトに対する権限、ロール、および所有権を付与します。これには以下が含まれます。

- ロールに権限を付与する。
- ユーザーまたは他のロールにロールを割り当てる。
- ロールに所有権を移譲する。

関連情報:

- [REVOKE](/tidb-cloud-lake/sql/revoke.md)
- [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md)

> `GRANT` で権限またはロールを変更した後は、更新内容をすべてのクエリノードに即座に反映するために、[SYSTEM FLUSH PRIVILEGES](/tidb-cloud-lake/guides/privileges.md) を実行してください。

## 構文 {#syntax}

### 権限の付与 {#granting-privileges}

権限とは何か、およびその仕組みについては、[Privileges](/tidb-cloud-lake/guides/privileges.md) を参照してください。

> **Note:**
>
> 所有権オブジェクトを作成する CREATE 系の権限は、ユーザーに直接付与できません。これらの権限はまずロールに付与する必要があり、その後でそのロールをユーザーに割り当てることができます。これには以下が含まれます。
>
> - CREATE
> - CREATE DATABASE
> - CREATE WAREHOUSE
> - CREATE CONNECTION
> - CREATE SEQUENCE
> - CREATE PROCEDURE
> - CREATE MASKING POLICY
> - CREATE ROW ACCESS POLICY
>
> `ALL` にはこれらの CREATE 権限が含まれるため、`GRANT ALL ... TO USER` も失敗します。たとえば、`GRANT ALL ON *.* TO USER u1` や `GRANT CREATE DATABASE ON *.* TO USER u1` は失敗します。代わりに、次を使用してください。
>
> ```sql
> GRANT ALL ON *.* TO ROLE r1;
> GRANT ROLE r1 TO USER u1;
> ```

```sql
GRANT {
        schemaObjectPrivileges | ALL [ PRIVILEGES ] ON <privileges_level>
      }
TO ROLE <role_name>
```

以下のとおりです。

```sql
schemaObjectPrivileges ::=
-- For TABLE
  { SELECT | INSERT }

-- For SCHEMA
  { CREATE | DROP | ALTER }

-- For USER
  { CREATE USER }

-- For ROLE
  { CREATE ROLE}

-- For STAGE
  { READ, WRITE }

-- For UDF
  { USAGE }

-- For MASKING POLICY (account-level privileges)
  { CREATE MASKING POLICY | APPLY MASKING POLICY }

-- For ROW ACCESS POLICY (account-level privileges)
  { CREATE ROW ACCESS POLICY | APPLY ROW ACCESS POLICY }
```

```sql
privileges_level ::=
    *.*
  | db_name.*
  | db_name.tbl_name
  | STAGE <stage_name>
  | UDF <udf_name>
  | MASKING POLICY <policy_name>
  | ROW ACCESS POLICY <policy_name>
```

### マスキングポリシー権限の付与 {#granting-masking-policy-privileges}

個々のマスキングポリシーへのアクセスを管理するには、次の形式を使用します。

```sql
GRANT APPLY ON MASKING POLICY <policy_name> TO ROLE <role_name>
GRANT ALL [ PRIVILEGES ] ON MASKING POLICY <policy_name> TO ROLE <role_name>
GRANT OWNERSHIP ON MASKING POLICY <policy_name> TO ROLE '<role_name>'
```

- `CREATE MASKING POLICY` は、ロールが新しいマスキングポリシーを作成できるようにします。
- `APPLY MASKING POLICY` は、適切な `ALTER TABLE` またはポリシーコマンドと組み合わせることで、被付与者が任意のマスキングポリシーをアタッチ、デタッチ、記述、または削除できるようにします。
- `GRANT APPLY ON MASKING POLICY ...` は、グローバルアクセスを付与せずに、被付与者が特定のマスキングポリシーを管理できるようにします。
- OWNERSHIP はマスキングポリシーに対する完全な制御を提供します。{{{ .lake }}} は新しいポリシーに対する OWNERSHIP を作成者ロールに自動的に付与し、ポリシーが削除されるとそれを取り消します。

### 行アクセスポリシー権限の付与 {#granting-row-access-policy-privileges}

個々の行アクセスポリシーへのアクセスを管理するには、次の形式を使用します。

```sql
GRANT APPLY ON ROW ACCESS POLICY <policy_name> TO ROLE <role_name>
GRANT ALL [ PRIVILEGES ] ON ROW ACCESS POLICY <policy_name> TO ROLE <role_name>
GRANT OWNERSHIP ON ROW ACCESS POLICY <policy_name> TO ROLE '<role_name>'
```

- `CREATE ROW ACCESS POLICY` は、ロールが新しい行アクセスポリシーを作成できるようにします。
- `APPLY ROW ACCESS POLICY` は、任意の行アクセスポリシーをテーブルにアタッチまたはデタッチする権限を付与し、DESCRIBE/DROP コマンドもあわせて許可します。
- `GRANT APPLY ON ROW ACCESS POLICY ...` は、特定の行アクセスポリシーへのアクセスに制限します。
- OWNERSHIP は行アクセスポリシーに対する完全な制御を提供します。作成者ロールは OWNERSHIP を自動的に受け取り、ポリシーが削除されるとそれを失います。

### ロールの付与 {#granting-role}

ロールとは何か、およびその仕組みについては、[ロール](/tidb-cloud-lake/guides/roles.md) を参照してください。

```sql
-- Grant a role to a user
GRANT ROLE <role_name> TO <user_name>

-- Grant a role to a role
GRANT ROLE <role_name> TO ROLE <role_name>
```

> **Note:**
>
> `default_role` はユーザーのプロパティです。これは `CREATE USER` または `ALTER USER` のときに設定され、`GRANT`/`REVOKE` では変更されません。そのため、後で誰かの `default_role` であるロールを取り消しても、その設定自体は残りますが、ロールメンバーシップは失われます。明示的に更新するには、`ALTER USER ... WITH DEFAULT_ROLE` を使用してください。

### 所有権の付与 {#granting-ownership}

所有権とは何か、およびその仕組みについては、[Ownership](/tidb-cloud-lake/guides/ownership.md) を参照してください。

```sql
-- Grant ownership of a specific table within a database to a role
GRANT OWNERSHIP ON <database_name>.<table_name> TO ROLE '<role_name>'

-- Grant ownership of a stage to a role
GRANT OWNERSHIP ON STAGE <stage_name> TO ROLE '<role_name>'

-- Grant ownership of a user-defined function (UDF) to a role
GRANT OWNERSHIP ON UDF <udf_name> TO ROLE '<role_name>'
```

## 例 {#examples}

### 例 1: ロールへの権限の付与 {#example-1-granting-privileges-to-a-role}

ロールを作成します。

```sql
CREATE ROLE user1_role;
```

`default` データベース内の既存のすべてのテーブルに対する `ALL` 権限を、ロール `user1_role` に付与します。

```sql
GRANT ALL ON default.* TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON 'default'.* TO ROLE 'user1_role'    |
+--------------------------------------------------+
```

すべてのデータベースに対する `ALL` 権限を、ロール `user1_role` に付与します。

```sql
GRANT ALL ON *.* TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON 'default'.* TO ROLE 'user1_role'    |
| GRANT ALL ON *.* TO ROLE 'user1_role'            |
+--------------------------------------------------+
```

`s1` という名前の stage に対する `ALL` 権限を、ロール `user1_role` に付与します。

```sql
GRANT ALL ON STAGE s1 TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON STAGE s1 TO ROLE 'user1_role'       |
+--------------------------------------------------+
```

`f1` という名前の UDF に対する `ALL` 権限を、ロール `user1_role` に付与します。

```sql
GRANT ALL ON UDF f1 TO ROLE user1_role;
```

```sql
SHOW GRANTS FOR ROLE user1_role;
+--------------------------------------------------+
| Grants                                           |
+--------------------------------------------------+
| GRANT ALL ON UDF f1 TO ROLE 'user1_role'         |
+--------------------------------------------------+
```

### 例 2: ロールへの特定の権限の付与 {#example-2-granting-specific-privileges-to-a-role}

`mydb` データベース内の既存のすべてのテーブルに対する `SELECT` 権限を、ロール `role1` に付与します。

ロールを作成します。

```sql
CREATE ROLE role1;
```

ロールに権限を付与します。

```sql
GRANT SELECT ON mydb.* TO ROLE role1;
```

ロールに付与されている権限を表示します。

```sql
SHOW GRANTS FOR ROLE role1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT SELECT ON 'mydb'.* TO 'role1' |
+-------------------------------------+
```

### 例 3: ユーザーへのロールの付与 {#example-3-granting-a-role-to-a-user}

ユーザーを作成します。

```sql
CREATE USER user1 IDENTIFIED BY 'abc123' WITH DEFAULT_ROLE = 'role1';
```

ロール `role1` に付与されている権限は次のとおりです。

```sql
SHOW GRANTS FOR ROLE role1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT SELECT ON 'mydb'.* TO 'role1' |
+-------------------------------------+
```

ロール `role1` をユーザー `user1` に付与します。

```sql
 GRANT ROLE role1 TO user1;
```

これで、ユーザー `user1` に付与されている権限は次のとおりです。

```sql
SHOW GRANTS FOR user1;
+-------------------------------------+
| Grants                              |
+-------------------------------------+
| GRANT ROLE role1 TO 'user1'@'%'     |
+-------------------------------------+
```

### 例 4: ロールへの所有権の付与 {#example-4-granting-ownership-to-a-role}

```sql
-- Grant ownership of all tables in the 'finance_data' database to the role 'data_owner'
GRANT OWNERSHIP ON finance_data.* TO ROLE 'data_owner';

-- Grant ownership of the table 'transactions' in the 'finance_data' schema to the role 'data_owner'
GRANT OWNERSHIP ON finance_data.transactions TO ROLE 'data_owner';

-- Grant ownership of the stage 'ingestion_stage' to the role 'data_owner'
GRANT OWNERSHIP ON STAGE ingestion_stage TO ROLE 'data_owner';

-- Grant ownership of the user-defined function 'calculate_profit' to the role 'data_owner'
GRANT OWNERSHIP ON UDF calculate_profit TO ROLE 'data_owner';
```

### 例 5: マスキングポリシー権限の付与 {#example-5-granting-masking-policy-privileges}

```sql
-- Allow the current user to create masking policies
GRANT CREATE MASKING POLICY ON *.* TO ROLE security_admin;

-- Create a masking policy while assuming the security_admin role
CREATE MASKING POLICY email_mask AS (val STRING) RETURNS STRING -> '***';

-- Grant a role the ability to apply the policy when altering tables
GRANT APPLY ON MASKING POLICY email_mask TO ROLE pii_readers;

-- Review the masking policy privileges
SHOW GRANTS ON MASKING POLICY email_mask;
```

### 例 6: 行アクセスポリシー権限の付与 {#example-6-granting-row-access-policy-privileges}

```sql
-- Allow the current role to create row access policies
GRANT CREATE ROW ACCESS POLICY ON *.* TO ROLE row_policy_admin;

-- Define a row access policy while assuming the row_policy_admin role
CREATE ROW ACCESS POLICY rap_region AS (region STRING) RETURNS BOOLEAN -> region = 'APAC';

-- Allow a role to apply the policy when altering tables
GRANT APPLY ON ROW ACCESS POLICY rap_region TO ROLE apac_only;

-- Review the row access policy privileges
SHOW GRANTS ON ROW ACCESS POLICY rap_region;
```