---
title: SHOW_GRANTS
summary: ロールに付与された権限、ユーザーへのロール割り当て、または特定のオブジェクトに対する権限を一覧表示します。
---

# SHOW_GRANTS

ロールに付与された権限、ユーザーへのロール割り当て、または特定のオブジェクトに対する権限を一覧表示します。

関連情報: [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md)

## 構文 {#syntax}

```sql
SHOW_GRANTS('role', '<role_name>')
SHOW_GRANTS('user', '<user_name>')
SHOW_GRANTS('stage', '<stage_name>')
SHOW_GRANTS('udf', '<udf_name>')
SHOW_GRANTS('table', '<table_name>', '<catalog_name>', '<db_name>')
SHOW_GRANTS('database', '<db_name>', '<catalog_name>')
```

## `enable_expand_roles` 設定の構成 {#configuring-enable-expand-roles-setting}

`enable_expand_roles` 設定は、SHOW_GRANTS 関数が権限を表示する際にロール継承を展開するかどうかを制御します。

- `enable_expand_roles=1`（デフォルト）:

    - SHOW_GRANTS は継承された権限を再帰的に展開します。つまり、あるロールに別のロールが付与されている場合、継承されたすべての権限が表示されます。
    - ユーザーには、割り当てられたロールを通じて付与されたすべての権限も表示されます。

- `enable_expand_roles=0`:

    - SHOW_GRANTS は、指定したロールまたはユーザーに直接割り当てられた権限のみを表示します。
    - ただし、結果にはロール継承を示すために GRANT ROLE 文が引き続き含まれます。

たとえば、ロール `a` が `t1` に対する `SELECT` 権限を持ち、ロール `b` が `t2` に対する `SELECT` 権限を持っているとします。

```sql
SELECT grants FROM show_grants('role', 'a') ORDER BY object_id;

┌──────────────────────────────────────────────────────┐
│                        grants                        │
├──────────────────────────────────────────────────────┤
│ GRANT SELECT ON 'default'.'default'.'t1' TO ROLE `a` │
└──────────────────────────────────────────────────────┘

SELECT grants FROM show_grants('role', 'b') ORDER BY object_id;

┌──────────────────────────────────────────────────────┐
│                        grants                        │
├──────────────────────────────────────────────────────┤
│ GRANT SELECT ON 'default'.'default'.'t2' TO ROLE `b` │
└──────────────────────────────────────────────────────┘
```

ロール `b` をロール `a` に付与してから、ロール `a` の権限を再度確認すると、`t2` に対する `SELECT` 権限がロール `a` に含まれるようになっていることが分かります。

```sql
GRANT ROLE b TO ROLE a;
```

```sql
SELECT grants FROM show_grants('role', 'a') ORDER BY object_id;

┌──────────────────────────────────────────────────────┐
│                        grants                        │
├──────────────────────────────────────────────────────┤
│ GRANT SELECT ON 'default'.'default'.'t1' TO ROLE `a` │
│ GRANT SELECT ON 'default'.'default'.'t2' TO ROLE `a` │
└──────────────────────────────────────────────────────┘
```

`enable_expand_roles` を `0` に設定してからロール `a` の権限を再度確認すると、結果にはロール `b` から継承された個別の権限の一覧ではなく、`GRANT ROLE` 文が表示されます。

```sql
SET enable_expand_roles=0;
```

```sql
SELECT grants FROM show_grants('role', 'a') ORDER BY object_id;

┌──────────────────────────────────────────────────────┐
│                        grants                        │
├──────────────────────────────────────────────────────┤
│ GRANT SELECT ON 'default'.'default'.'t1' TO ROLE `a` │
│ GRANT ROLE b to ROLE `a`                             │
│ GRANT ROLE public to ROLE `a`                        │
└──────────────────────────────────────────────────────┘
```

## 例 {#examples}

この例では、ユーザーの権限、ロールに付与された権限、および特定のオブジェクトに対する権限を一覧表示する方法を示します。

```sql
-- Create a new user
CREATE USER 'user1' IDENTIFIED BY 'password';

-- Create a new role
CREATE ROLE analyst;

-- Grant the analyst role to the user
GRANT ROLE analyst TO 'user1';

-- Create a stage
CREATE STAGE my_stage;

-- Grant privileges on the stage to the role
GRANT READ ON STAGE my_stage TO ROLE analyst;

-- List grants for the user
SELECT * FROM SHOW_GRANTS('user', 'user1');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ privileges │ object_name │     object_id    │ grant_to │  name  │                    grants                   │
├────────────┼─────────────┼──────────────────┼──────────┼────────┼─────────────────────────────────────────────┤
│ Read       │ my_stage    │             NULL │ USER     │ user1  │ GRANT Read ON STAGE my_stage TO 'user1'@'%' │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- List privileges granted to the role
SELECT * FROM SHOW_GRANTS('role', 'analyst');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ privileges │ object_name │     object_id    │ grant_to │   name  │                     grants                     │
├────────────┼─────────────┼──────────────────┼──────────┼─────────┼────────────────────────────────────────────────┤
│ Read       │ my_stage    │             NULL │ ROLE     │ analyst │ GRANT Read ON STAGE my_stage TO ROLE `analyst` │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- List privileges granted on the stage
SELECT * FROM SHOW_GRANTS('stage', 'my_stage');

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ privileges │ object_name │     object_id    │ grant_to │   name  │      grants      │
├────────────┼─────────────┼──────────────────┼──────────┼─────────┼──────────────────┤
│ Read       │ my_stage    │             NULL │ ROLE     │ analyst │                  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```