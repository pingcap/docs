---
title: ALTER PASSWORD POLICY
sidebar_position: 3
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.283"/>

Modifies an existing password policy in Databend.

## Syntax

```sql
-- Modify existing password policy attributes
ALTER PASSWORD POLICY [ IF EXISTS ] <name> SET
    [ PASSWORD_MIN_LENGTH = <number> ]
    [ PASSWORD_MAX_LENGTH = <number> ]
    [ PASSWORD_MIN_UPPER_CASE_CHARS = <number> ]
    [ PASSWORD_MIN_LOWER_CASE_CHARS = <number> ]
    [ PASSWORD_MIN_NUMERIC_CHARS = <number> ]
    [ PASSWORD_MIN_SPECIAL_CHARS = <number> ]
    [ PASSWORD_MIN_AGE_DAYS = <number> ]
    [ PASSWORD_MAX_AGE_DAYS = <number> ]
    [ PASSWORD_MAX_RETRIES = <number> ]
    [ PASSWORD_LOCKOUT_TIME_MINS = <number> ]
    [ PASSWORD_HISTORY = <number> ]
    [ COMMENT = '<comment>' ]

-- Remove specific password policy attributes
ALTER PASSWORD POLICY [ IF EXISTS ] <name> UNSET
    [ PASSWORD_MIN_LENGTH ]
    [ PASSWORD_MAX_LENGTH ]
    [ PASSWORD_MIN_UPPER_CASE_CHARS ]
    [ PASSWORD_MIN_LOWER_CASE_CHARS ]
    [ PASSWORD_MIN_NUMERIC_CHARS ]
    [ PASSWORD_MIN_SPECIAL_CHARS ]
    [ PASSWORD_MIN_AGE_DAYS ]
    [ PASSWORD_MAX_AGE_DAYS ]
    [ PASSWORD_MAX_RETRIES ]
    [ PASSWORD_LOCKOUT_TIME_MINS ]
    [ PASSWORD_HISTORY ]
    [ COMMENT ]
```

For detailed descriptions of the password policy attributes, see [Password Policy Attributes](create-password-policy.md#password-policy-attributes).

## Examples

This example creates a password policy named 'SecureLogin' with a minimum password length requirement set to 10 characters, later updated to allow passwords between 10 and 16 characters:

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;


ALTER PASSWORD POLICY SecureLogin SET
    PASSWORD_MIN_LENGTH = 10
    PASSWORD_MAX_LENGTH = 16;
```