---
title: SET ROLE
summary: 切换会话的活动角色。你可以使用 [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) 命令查看当前活动角色，其中 `is_current` 字段表示活动角色。有关活动角色和次要角色的更多信息，请参阅 [活动角色和次要角色](/tidb-cloud-lake/guides/roles.md#active-role--secondary-roles)。
---

# SET ROLE

切换会话的活动角色。你可以使用 [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) 命令查看当前活动角色，其中 `is_current` 字段表示活动角色。有关活动角色和次要角色的更多信息，请参阅 [活动角色和次要角色](/tidb-cloud-lake/guides/roles.md#active-role--secondary-roles)。

另请参阅：[SET SECONDARY ROLES](/tidb-cloud-lake/sql/set-secondary-roles.md)

## 语法 {#syntax}

```sql
SET ROLE <role_name>
```

## 示例 {#examples}

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