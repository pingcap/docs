---
title: Ownership
summary: Ownership は、{{{ .lake }}} 内の特定のデータオブジェクト（現在は database、table、UDF、stage を含む）に対して、あるロールが持つ排他的な権利と責任を示す特別な権限です。
---

# Ownership

Ownership は、{{{ .lake }}} 内の特定のデータオブジェクト（現在は database、table、UDF、stage を含む）に対して、あるロールが持つ排他的な権利と責任を示す特別な権限です。

## Ownership の付与 {#granting-ownership}

オブジェクトの Ownership は、そのオブジェクトを作成したユーザーのロールに自動的に付与され、[GRANT](/tidb-cloud-lake/sql/grant.md) コマンドを使用してロール間で移譲できます。

- オブジェクトの Ownership を新しいロールに付与すると、完全な Ownership が新しいロールに移譲され、以前のロールからは削除されます。たとえば、最初に Role A があるテーブルを所有していて、その Ownership を Role B に付与した場合、Role B が新しい所有者となり、Role A はそのテーブルに対する Ownership を失います。
- セキュリティ上の理由から、組み込みロール `public` に Ownership を付与することは推奨されません。ユーザーが `public` ロールに属した状態でオブジェクトを作成すると、すべてのユーザーがそのオブジェクトの Ownership を持つことになります。これは、各ユーザーがデフォルトで `public` ロールを持っているためです。{{{ .lake }}} では、Ownership を明確に管理するために、`public` ロールを使用する代わりにカスタムロールを作成してユーザーに割り当てることを推奨しています。組み込みロールの詳細については、[組み込みロール](/tidb-cloud-lake/guides/roles.md) を参照してください。
- `default` database 内のテーブルについては、組み込みロール `account_admin` が所有しているため、Ownership を付与できません。

## Ownership の取り消しは不可 {#revoking-ownership-not-allowed}

すべてのオブジェクトには所有者が必要なため、Ownership の取り消しは*サポートされていません*。

- オブジェクトが削除されると、元のロールによる Ownership は保持されません。オブジェクトが復元された場合（可能であれば）も、Ownership は自動的には再割り当てされず、`account_admin` が手動でロールに Ownership を再割り当てする必要があります。
- オブジェクトを所有しているロールが削除された場合、`account_admin` はそのオブジェクトの Ownership を別のロールに移譲できます。

## 例 {#examples}

ロールに Ownership を付与するには、[GRANT](/tidb-cloud-lake/sql/grant.md) コマンドを使用します。以下の例では、異なる database オブジェクトの Ownership をロール 'data_owner' に付与する方法を示します。

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

次の例は、{{{ .lake }}} におけるロールベースの Ownership の確立を示しています。管理者はロール 'role1' を作成し、それをユーザー 'u1' に割り当てます。'db' schema 内でテーブルを作成する権限は 'role1' に付与されます。その結果、'u1' がログインすると 'role1' の権限を持つため、'db' 配下でテーブルを作成して所有できます。一方で、'role1' が所有していないテーブルへのアクセスは制限されており、'db.t_old_exists' に対するクエリが失敗することからもそれが分かります。

```sql
-- Admin creates roles and assigns roles to corresponding users
CREATE ROLE role1;
CREATE USER u1 IDENTIFIED BY '123' WITH DEFAULT ROLE 'role1';
GRANT CREATE ON db.* TO ROLE role1;
GRANT ROLE role1 TO u1;

-- After u1 logs into {{{ .lake }}}, role1 has been granted to u1, so u1 can create and own tables under db:
u1> CREATE TABLE db.t(id INT);
u1> INSERT INTO db.t VALUES(1);
u1> SELECT * FROM db.t;
u1> SELECT * FROM db.t_old_exists; -- Failed because the owner of this table is not role1
```

次の例は、ユーザーが自分のロールのみに所有される database を作成できるようにし、明示的にアクセス権が付与されない限り他のユーザーがそれを参照できないようにする方法を示しています。

```sql
CREATE ROLE part1_role;
GRANT CREATE DATABASE ON *.* TO ROLE part1_role;
CREATE USER user1 IDENTIFIED BY 'abc123' WITH DEFAULT ROLE 'part1_role';
GRANT ROLE part1_role TO user1;

-- When user1 creates a database, ownership is assigned to part1_role.
-- Other users will not be able to see or access that database unless
-- privileges or ownership are granted to their roles.
```