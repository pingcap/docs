---
title: CREATE PASSWORD POLICY
sidebar_position: 1
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.339"/>

Creates a new password policy in Databend.

## Syntax

```sql
CREATE [ OR REPLACE ] PASSWORD POLICY [ IF NOT EXISTS ] <policy_name>
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
```

### Password Policy Attributes

This table summarizes essential parameters for a password policy, covering aspects like length, character requirements, age restrictions, retry limits, lockout duration, and password history:

| Attribute                     | Min | Max | Default | Description                                                                          |
|-------------------------------|-----|-----|---------|--------------------------------------------------------------------------------------|
| PASSWORD_MIN_LENGTH           | 8   | 256 | 8       | Minimum length of the password                                                       |
| PASSWORD_MAX_LENGTH           | 8   | 256 | 256     | Maximum length of the password                                                       |
| PASSWORD_MIN_UPPER_CASE_CHARS | 0   | 256 | 1       | Minimum number of uppercase characters in the password                               |
| PASSWORD_MIN_LOWER_CASE_CHARS | 0   | 256 | 1       | Minimum number of lowercase characters in the password                               |
| PASSWORD_MIN_NUMERIC_CHARS    | 0   | 256 | 1       | Minimum number of numeric characters in the password                                 |
| PASSWORD_MIN_SPECIAL_CHARS    | 0   | 256 | 0       | Minimum number of special characters in the password                                 |
| PASSWORD_MIN_AGE_DAYS         | 0   | 999 | 0       | Minimum number of days before password can be modified (0 indicates no restriction)  |
| PASSWORD_MAX_AGE_DAYS         | 0   | 999 | 90      | Maximum number of days before password must be modified (0 indicates no restriction) |
| PASSWORD_MAX_RETRIES          | 1   | 10  | 5       | Maximum number of password retries before lockout                                    |
| PASSWORD_LOCKOUT_TIME_MINS    | 1   | 999 | 15      | Duration of lockout in minutes after exceeding retries                               |
| PASSWORD_HISTORY              | 0   | 24  | 0       | Number of recent passwords to check for duplication (0 indicates no restriction)     |

## Examples

This example creates a password policy named 'SecureLogin' with a minimum password length requirement set to 10 characters:

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;
```