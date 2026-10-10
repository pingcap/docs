---
title: SET ROLE
summary: セッションのアクティブなロールを切り替えます。現在アクティブなロールは [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) コマンドで確認でき、`is_current` フィールドがアクティブなロールを示します。アクティブロールおよびセカンダリロールの詳細については、[Active Role & Secondary Roles](/tidb-cloud-lake/guides/roles.md#active-role--secondary-roles) を参照してください。
---

# SET ROLE

セッションのアクティブなロールを切り替えます。現在アクティブなロールは [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) コマンドで確認でき、`is_current` フィールドがアクティブなロールを示します。アクティブロールおよびセカンダリロールの詳細については、[Active Role & Secondary Roles](/tidb-cloud-lake/guides/roles.md#active-role--secondary-roles) を参照してください。

関連項目: [SET SECONDARY ROLES](/tidb-cloud-lake/sql/set-secondary-roles.md)

## 構文 {#syntax}

```sql
SET ROLE <role_name>
```

## 例 {#examples}

```sql
SHOW ROLES;

┌───────────────────────────────────────────────────────┐
│    name   │ inherited_roles │ is_current │ is_default │
├───────────┼─────────────────┼────────────┼────────────┤
│ developer │               0 │ false      │ false      │
│ public    │               0 │ false      │ false      │
│ writer    │               0 │ true       │ true       │
└───────────────────────────────────────────────────────┘

SET ROLE developer;

SHOW ROLES;

┌───────────────────────────────────────────────────────┐
│    name   │ inherited_roles │ is_current │ is_default │
├───────────┼─────────────────┼────────────┼────────────┤
│ developer │               0 │ true       │ false      │
│ public    │               0 │ false      │ false      │
│ writer    │               0 │ false      │ true       │
└───────────────────────────────────────────────────────┘
```