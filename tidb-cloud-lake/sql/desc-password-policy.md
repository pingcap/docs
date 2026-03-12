---
title: DESC PASSWORD POLICY
sidebar_position: 2
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.283"/>

Displays detailed information about a specific password policy in Databend. For detailed descriptions of the password policy attributes, see [Password Policy Attributes](create-password-policy.md#password-policy-attributes).

## Syntax

```sql
DESC PASSWORD POLICY <policy_name>
```

## Examples

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;

DESC PASSWORD POLICY SecureLogin;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│            Property           │    Value    │      Default     │                                                                 Description                                                                │
├───────────────────────────────┼─────────────┼──────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ NAME                          │ SecureLogin │ NULL             │ Name of password policy.                                                                                                                   │
│ COMMENT                       │             │ NULL             │ Comment of password policy.                                                                                                                │
│ PASSWORD_MIN_LENGTH           │ 10          │ 8                │ Minimum length of new password.                                                                                                            │
│ PASSWORD_MAX_LENGTH           │ 256         │ 256              │ Maximum length of new password.                                                                                                            │
│ PASSWORD_MIN_UPPER_CASE_CHARS │ 1           │ 1                │ Minimum number of uppercase characters in new password.                                                                                    │
│ PASSWORD_MIN_LOWER_CASE_CHARS │ 1           │ 1                │ Minimum number of lowercase characters in new password.                                                                                    │
│ PASSWORD_MIN_NUMERIC_CHARS    │ 1           │ 1                │ Minimum number of numeric characters in new password.                                                                                      │
│ PASSWORD_MIN_SPECIAL_CHARS    │ 0           │ 0                │ Minimum number of special characters in new password.                                                                                      │
│ PASSWORD_MIN_AGE_DAYS         │ 0           │ 0                │ Period after a password is changed during which a password cannot be changed again, in days.                                               │
│ PASSWORD_MAX_AGE_DAYS         │ 90          │ 90               │ Period after which password must be changed, in days.                                                                                      │
│ PASSWORD_MAX_RETRIES          │ 5           │ 5                │ Number of attempts users have to enter the correct password before their account is locked.                                                │
│ PASSWORD_LOCKOUT_TIME_MINS    │ 15          │ 15               │ Period of time for which users will be locked after entering their password incorrectly many times (specified by MAX_RETRIES), in minutes. │
│ PASSWORD_HISTORY              │ 0           │ 0                │ Number of most recent passwords that may not be repeated by the user.                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```