---
title: CURRENT_CATALOG
summary: Returns the name of the catalog currently in use for the session.
---

# CURRENT_CATALOG

import FunctionDescription from '@site/src/components/FunctionDescription';

## CURRENT_CATALOG

<FunctionDescription description="Introduced or updated: v1.2.668"/>

Returns the name of the catalog currently in use for the session.

## Syntax

```sql
CURRENT_CATALOG()
```

## Examples

```sql
SELECT CURRENT_CATALOG();

┌───────────────────┐
│ current_catalog() │
├───────────────────┤
│ default           │
└───────────────────┘
```
