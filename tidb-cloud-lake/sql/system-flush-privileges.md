---
title: SYSTEM FLUSH PRIVILEGES
---

`SYSTEM FLUSH PRIVILEGES` broadcasts a refresh request to every query node so each node immediately reloads privilege and role metadata from the Meta service. Run the command after `GRANT` or `REVOKE` statements when you need the changes to take effect across the cluster without waiting for the default 15-second role-cache interval.

See also:

- [GRANT](../00-ddl/02-user/10-grant.md)
- [REVOKE](../00-ddl/02-user/11-revoke.md)

## Syntax

```sql
SYSTEM FLUSH PRIVILEGES
```

## Usage Notes

- Requires a role that is allowed to execute system administration commands, such as `ACCOUNT ADMIN`.
- Refreshes cached privilege metadata only; it does not alter roles or grants by itself.
- Statements that are already running keep using the privileges that were resolved when they started. Re-run the statement after the flush to pick up the changes.

## Example

The following sequence grants a role access to a database and immediately flushes the caches so the new privilege is visible from every query node:

```sql
GRANT SELECT ON DATABASE marketing TO ROLE analyst;

SYSTEM FLUSH PRIVILEGES;
```

After the flush completes, any new query that runs under the `analyst` role receives the updated privilege set without waiting for the cache to expire.
