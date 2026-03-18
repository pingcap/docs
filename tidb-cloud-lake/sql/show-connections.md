---
title: SHOW CONNECTIONS
summary: Displays a list of all available connections.
---

> **Note:**
>
> Introduced or updated in v1.2.208.

Displays a list of all available connections.

## Syntax

```sql
SHOW CONNECTIONS
```

## Examples

```sql
SHOW CONNECTIONS;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name  │ storage_type │                                         storage_params                            │
├─────────┼──────────────┼───────────────────────────────────────────────────────────────────────────────────┤
│ toronto │ s3           │ access_key_id=<your-secret-access-key> secret_access_key=<your-secret-access-key> │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```