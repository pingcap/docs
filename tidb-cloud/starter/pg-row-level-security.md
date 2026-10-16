---
title: PostgreSQL Row-Level Security
summary: PostgreSQL-compatible TiDB Cloud Starter で PostgreSQL 互換の行レベルセキュリティポリシーを使用する方法を学びます。
---

# PostgreSQL Row-Level Security

PostgreSQL-compatible {{{ .starter }}} は、PostgreSQL 互換の Row-Level Security (RLS) をサポートしています。RLS は、ロールのテーブル権限に加えて、データベースロールがどの行を表示、挿入、更新、または削除できるかをさらに制限します。

RLS ポリシーは、該当する各クエリに対してデータベースによって評価されます。このため、RLS はマルチテナントアプリケーションや、行単位のアクセス制御を必要とするその他のワークロードに役立ちます。

## 行レベルセキュリティを有効にする {#enable-row-level-security}

`ALTER TABLE ... ENABLE ROW LEVEL SECURITY` を使用します。

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;
```

RLS が有効で、かつ適用可能なポリシーが存在しない場合、RLS をバイパスしないロールに対しては、デフォルトでアクセスが拒否されます。

RLS を無効にするには、次を使用します。

```sql
ALTER TABLE todos DISABLE ROW LEVEL SECURITY;
```

## テーブル所有者に対して RLS を強制する {#force-rls-for-the-table-owner}

デフォルトでは、テーブル所有者は RLS ポリシーをバイパスします。

`FORCE ROW LEVEL SECURITY` を使用すると、テーブル所有者にもポリシーを適用できます。

```sql
ALTER TABLE todos FORCE ROW LEVEL SECURITY;
```

所有者のデフォルト動作に戻すには、次を使用します。

```sql
ALTER TABLE todos NO FORCE ROW LEVEL SECURITY;
```

スーパーユーザーおよび `BYPASSRLS` 属性を持つロールは、`FORCE ROW LEVEL SECURITY` が有効な場合でも RLS をバイパスします。`FORCE ROW LEVEL SECURITY` は、所有者がスーパーユーザーではなく、かつ `BYPASSRLS` を持っていない場合にのみ、テーブル所有者にポリシーを適用します。

## ポリシーを作成する {#create-a-policy}

RLS ポリシーを定義するには `CREATE POLICY` を使用します。

一般的な構文は次のとおりです。

```sql
CREATE POLICY policy_name ON table_name
    [AS { PERMISSIVE | RESTRICTIVE }]
    [FOR { ALL | SELECT | INSERT | UPDATE | DELETE }]
    [TO role_name [, ...]]
    [USING (expression)]
    [WITH CHECK (expression)];
```

`AS` を省略した場合、ポリシーは `PERMISSIVE` になります。

`FOR` を省略した場合、ポリシーはサポートされているすべてのコマンドに適用されます。

`TO` を省略した場合、ポリシーは `PUBLIC` に適用されます。

## `USING` と `WITH CHECK` {#using-and-with-check}

`USING` と `WITH CHECK` は目的が異なります。

| 句 | 目的 | 適用対象 |
| --- | --- | --- |
| `USING` | どの既存行を表示できるか、または対象にできるかを決定します。 | `SELECT`, `UPDATE`, `DELETE` |
| `WITH CHECK` | 新しい行または変更された行の値を検証します。 | `INSERT`, `UPDATE` |

各操作で使用される句は次のとおりです。

| 操作 | `USING` | `WITH CHECK` |
| --- | --- | --- |
| `SELECT` | 使用される | 使用されない |
| `INSERT` | 使用されない | 使用される |
| `UPDATE` | 使用される | 使用される |
| `DELETE` | 使用される | 使用されない |

`UPDATE` ポリシーでは、`WITH CHECK` を省略すると、更新後の行の検証にも `USING` 式が使用されます。

## 例: ユーザーごとに行を制限する {#example-restrict-rows-by-user}

次の例では、各ロールが `user_id` が `current_user` と一致する行にのみアクセスできるようにします。

テーブルを作成します。

```sql
CREATE TABLE todos (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    task TEXT NOT NULL,
    done BOOLEAN DEFAULT false
);
```

RLS を有効にします。

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;
```

ユーザーが自分の行を読み取れるようにします。

```sql
CREATE POLICY user_select
ON todos
FOR SELECT
USING (user_id = current_user);
```

ユーザーが自分自身のための行を挿入できるようにします。

```sql
CREATE POLICY user_insert
ON todos
FOR INSERT
WITH CHECK (user_id = current_user);
```

ユーザーが自分の行を更新できるようにします。

```sql
CREATE POLICY user_update
ON todos
FOR UPDATE
USING (user_id = current_user)
WITH CHECK (user_id = current_user);
```

ユーザーが自分の行を削除できるようにします。

```sql
CREATE POLICY user_delete
ON todos
FOR DELETE
USING (user_id = current_user);
```

## 例: 公開行と非公開行 {#example-public-and-private-rows}

次の例では、テーブルに対する SELECT 権限を持つロールが公開済みの投稿を参照でき、作成者は自分の未公開投稿を参照できるようにします。

テーブルを作成し、RLS を有効にします。

```sql
CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    author TEXT,
    published BOOLEAN DEFAULT false,
    content TEXT
);

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

公開済み投稿用のポリシーを作成します。

```sql
CREATE POLICY see_published
ON posts
FOR SELECT
USING (published = true);
```

ユーザー自身の投稿用に別のポリシーを作成します。

```sql
CREATE POLICY see_own
ON posts
FOR SELECT
USING (author = current_user);
```

両方のポリシーはデフォルトで permissive であるため、SELECT 権限を持つロールは、適用可能ないずれかのポリシーで許可されていれば、その行を参照できます。

## permissive ポリシーと restrictive ポリシー {#permissive-and-restrictive-policies}

### permissive ポリシー {#permissive-policies}

同じコマンドに対する複数の `PERMISSIVE` ポリシーは、`OR` で結合されます。

例:

```text
permissive_policy_1 OR permissive_policy_2 OR ...
```

少なくとも 1 つの適用可能な permissive ポリシーが、その行を許可する必要があります。

### 制限的ポリシー {#restrictive-policies}

一致するすべての制限的ポリシーが通過する必要がある場合は、`AS RESTRICTIVE` を使用します。

```sql
CREATE POLICY must_be_published
ON posts
AS RESTRICTIVE
FOR SELECT
USING (published = true);
```

制限的ポリシーは `AND` で結合され、許可的ポリシーの結果に加えて適用されます。

```text
(permissive_policy_1 OR permissive_policy_2 OR ...)
AND restrictive_policy_1
AND restrictive_policy_2
AND ...
```

制限的ポリシー自体ではアクセスは許可されません。少なくとも 1 つの適用可能な許可的ポリシーでも、その行が許可されている必要があります。

## 特定のロールにポリシーを適用する {#apply-policies-to-specific-roles}

`TO` を使用して、ポリシーを 1 つ以上のロールに限定します。

例:

```sql
CREATE POLICY support_read
ON tickets
FOR SELECT
TO support_agent
USING (status <> 'private');
```

明示的な `TO` 句がないポリシーは `PUBLIC` に適用されます。

## ポリシーを変更する {#alter-a-policy}

`ALTER POLICY` を使用して、ロールまたはポリシー式を変更します。

```sql
ALTER POLICY see_own
ON posts
USING (author = current_user OR published = true);
```

## ポリシーを削除する {#drop-a-policy}

`DROP POLICY` を使用します。

```sql
DROP POLICY see_own ON posts;
```

ポリシーが存在しない場合のエラーを回避するには、次を使用します。

```sql
DROP POLICY IF EXISTS see_own ON posts;
```

## RLS をバイパスする {#bypass-rls}

### `BYPASSRLS` ロール属性 {#bypassrls-role-attribute}

`BYPASSRLS` を持つロールは RLS ポリシーをバイパスします。

この属性を持つログインロールを作成します。

```sql
CREATE ROLE service_admin
LOGIN
PASSWORD 'SecurePass1'
BYPASSRLS;
```

後からこの属性を付与または取り消すこともできます。

```sql
ALTER ROLE service_admin BYPASSRLS;
ALTER ROLE service_admin NOBYPASSRLS;
```

`BYPASSRLS` は、信頼できる管理ロールまたはサービスロールにのみ付与してください。

### テーブル所有者 {#table-owners}

テーブル所有者は、デフォルトで RLS をバイパスします。所有者もポリシーの対象にする必要がある場合は、`FORCE ROW LEVEL SECURITY` を使用します。

### `SECURITY DEFINER` 関数 {#security-definer-functions}

`SECURITY DEFINER` 関数は、その所有者の権限で実行されます。

例:

```sql
CREATE FUNCTION list_all_posts()
RETURNS SETOF posts
LANGUAGE SQL
SECURITY DEFINER
AS $$
    SELECT * FROM posts
$$;
```

関数の所有者が RLS をバイパスできる場合、関数内で実行されるクエリも RLS をバイパスできる可能性があります。

> **Warning:**
>
> `SECURITY DEFINER` 関数は慎重に使用してください。関数がアクセス可能な操作や行を厳密に制御していない限り、RLS をバイパスできる関数を信頼できないロールに公開しないでください。

## RLS ポリシーを確認する {#inspect-rls-policies}

テーブル上のポリシーを一覧表示するには、`pg_policies` を使用します。

```sql
SELECT
    policyname,
    cmd,
    permissive,
    roles,
    qual,
    with_check
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename = 'todos'
ORDER BY policyname;
```

RLS が有効か、または強制されているかを確認します。

```sql
SELECT
    relname,
    relrowsecurity,
    relforcerowsecurity
FROM pg_class
WHERE oid = 'public.todos'::regclass;
```

ロールが RLS をバイパスできるかどうかを確認します。

```sql
SELECT
    rolname,
    rolbypassrls
FROM pg_roles
WHERE rolname = 'app_user';
```

## セキュリティに関する考慮事項 {#security-considerations}

RLS を使用する場合:

- 通常のアプリケーショントラフィックには、管理ロールではなく専用のアプリケーションロールを使用します。
- 保護対象テーブルへのアクセスをアプリケーションロールに付与する前に、RLS を有効にします。
- アプリケーションが必要とするすべての操作に対してポリシーを作成します。
- `UPDATE` ポリシーでは、`USING` 条件と `WITH CHECK` 条件の両方を確認します。
- `BYPASSRLS` は信頼できるロールにのみ付与します。
- `SECURITY DEFINER` 関数は関数所有者の権限で実行されるため、慎重に確認します。
- アプリケーションが使用するものと同じロールを使って RLS の動作をテストします。