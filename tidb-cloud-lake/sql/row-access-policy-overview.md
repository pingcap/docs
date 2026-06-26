---
title: Row Access Policy Overview
summary: "A comprehensive overview of Row Access Policy operations in {{{ .lake }}}, organized by functionality for easy reference."
---

# Row Access Policy Overview

This page provides a comprehensive overview of Row Access Policy operations in {{{ .lake }}}, organized by functionality for easy reference.

## Row Access Policy Management

| Command | Description |
|---------|-------------|
| [CREATE ROW ACCESS POLICY](/tidb-cloud-lake/sql/create-row-access-policy.md) | Creates a row-level filter policy |
| [DESCRIBE ROW ACCESS POLICY](/tidb-cloud-lake/sql/desc-row-access-policy.md) | Shows details of a row access policy |
| [DROP ROW ACCESS POLICY](/tidb-cloud-lake/sql/drop-row-access-policy.md) | Removes a row access policy |

## Related Topics

- [Row Access Policy](/tidb-cloud-lake/guides/row-access-policy.md)
- [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#row-access-policy-operations)
- [POLICY_REFERENCES](/tidb-cloud-lake/sql/policy-references.md)

> **Note:**
>
> Row access policies filter rows at query time. A protected table returns only the rows for which the policy expression evaluates to `TRUE`.
