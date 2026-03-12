---
title: SHOW PASSWORD POLICIES
sidebar_position: 4
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.283"/>

Displays a list of all existing password policies in Databend.

## Syntax

```sql
SHOW PASSWORD POLICIES [ LIKE '<pattern>' ]
```

## Examples

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;

SHOW PASSWORD POLICIES;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     name    │ comment │                                                                                                  options                                                                                                 │
├─────────────┼─────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SecureLogin │         │ MIN_LENGTH=10, MAX_LENGTH=256, MIN_UPPER_CASE_CHARS=1, MIN_LOWER_CASE_CHARS=1, MIN_NUMERIC_CHARS=1, MIN_SPECIAL_CHARS=0, MIN_AGE_DAYS=0, MAX_AGE_DAYS=90, MAX_RETRIES=5, LOCKOUT_TIME_MINS=15, HISTORY=0 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```