---
title: DESC CONNECTION
sidebar_position: 2
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.208"/>

Describes the details of a specific connection, providing information about its type and configuration.

## Syntax

```sql
DESC CONNECTION <connection_name>
```

## Examples

```sql
DESC CONNECTION toronto;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   name  │ storage_type │                                         storage_params                            │
├─────────┼──────────────┼───────────────────────────────────────────────────────────────────────────────────┤
│ toronto │ s3           │ access_key_id=<your-secret-access-key> secret_access_key=<your-secret-access-key> │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```