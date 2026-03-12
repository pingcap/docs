---
title: SHOW ROLES
sidebar_position: 6
---

Lists all the roles assigned to the current user.

## Syntax

```sql
SHOW ROLES
```

## Output

The command returns the results in a table with these columns:

| Column          | Description                                                 |
|-----------------|-------------------------------------------------------------|
| name            | The role name.                                              |
| inherited_roles | Number of roles inherited by the current role.              |
| is_current      | Indicates whether the role is currently active.             |
| is_default      | Indicates whether the role is the default role of the user. |

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
```