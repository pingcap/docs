---
title: DROP PASSWORD POLICY
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.283"/>

Deletes an existing password policy from Databend. Please note that, before dropping a password policy, ensure that this policy is not associated with any users.

## Syntax

```sql
DROP PASSWORD POLICY [ IF EXISTS ] <policy_name>
```

## Examples

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;

DROP PASSWORD POLICY SecureLogin;
```