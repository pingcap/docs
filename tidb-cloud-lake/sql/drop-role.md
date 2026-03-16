---
title: DROP ROLE
sidebar_position: 8
---

Removes the specified role from the system.

## Syntax

```sql
DROP ROLE [ IF EXISTS ] <role_name>
```

## Usage Notes
* If a role is a grant to users, Databend can't drop the grants from the role automatically.

## Examples

```sql
DROP ROLE role1;
```