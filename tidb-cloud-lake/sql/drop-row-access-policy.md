---
title: DROP ROW ACCESS POLICY
summary: "Deletes an existing row access policy from {{{ .lake }}}. Before dropping a policy, detach it from all tables that reference it."
---

# DROP ROW ACCESS POLICY

Deletes an existing row access policy from {{{ .lake }}}. Before dropping a policy, detach it from all tables that reference it.

## Syntax

```sql
DROP ROW ACCESS POLICY [ IF EXISTS ] <policy_name>
```

## Access Control Requirements

| Privilege | Description |
|:----------|:------------|
| APPLY ROW ACCESS POLICY | Required to drop a row access policy unless you own that policy. |

You must have the global `APPLY ROW ACCESS POLICY` privilege or APPLY/OWNERSHIP on the target policy. {{{ .lake }}} automatically revokes OWNERSHIP from the creator role after the policy is dropped.

## Examples

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN -> dept = 'Engineering';

CREATE TABLE employees(id INT, department STRING);
ALTER TABLE employees ADD ROW ACCESS POLICY rap_engineering ON (department);

-- Detach the policy before dropping it.
ALTER TABLE employees DROP ROW ACCESS POLICY rap_engineering;

DROP ROW ACCESS POLICY rap_engineering;
```
