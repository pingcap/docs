---
title: SET ROLE
summary: Switches the active role for a session, and the currently active role can be viewed using the SHOW ROLES command, with the is_current field indicating the active role. For more information about the active role and secondary roles, see Active Role & Secondary Roles.
---

# SET ROLE

Switches the active role for a session, and the currently active role can be viewed using the [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) command, with the `is_current` field indicating the active role. For more information about the active role and secondary roles, see [Active Role & Secondary Roles](/tidb-cloud-lake/guides/roles.md#active-role--secondary-roles).

See also: [SET SECONDARY ROLES](/tidb-cloud-lake/sql/set-secondary-roles.md)

## Syntax

```sql
SET ROLE <role_name>
```

## Examples

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
