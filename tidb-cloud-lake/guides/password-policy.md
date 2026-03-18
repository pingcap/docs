---
title: Password Policy
---

Password policies define how strong a Databend password must be (length, characters, history, retry limits, and more) and how often it can change. They add predictable guardrails around every `CREATE USER` and password change. For the full list of attributes, see [Password Policy Attributes](/tidb-cloud-lake/sql/create-password-policy.md#password-policy-attributes).

## How It Works

- SQL users start with no password policy. Assign one either when creating the user (`CREATE USER ... WITH SET PASSWORD POLICY`) or later via [ALTER USER](/tidb-cloud-lake/sql/alter-user.md). Policies do **not** apply to admin accounts declared in [`databend-query.toml`](https://github.com/databendlabs/databend/blob/main/scripts/distribution/configs/databend-query.toml).
- Whenever a managed user sets or changes a password, Databend validates the complexity rules (length and character mix) and, for password changes, enforces minimum age and password history.
- On login, Databend also tracks failed attempts and lockouts based on `PASSWORD_MAX_RETRIES`/`PASSWORD_LOCKOUT_TIME_MINS`, and it flags expired passwords after `PASSWORD_MAX_AGE_DAYS`. Expired users can log in only to change their password.

> **Note:**
>
> Users normally cannot change their own password unless they have the built-in `account-admin` role. An `account-admin` can run `ALTER USER ... IDENTIFIED BY ...` to rotate passwords for anyone.

## End-to-End Example

This walkthrough creates dedicated policies for administrators and analysts, binds them to users, and shows how to revise or remove them later.

### 1. Create Policies and Inspect Them

```sql
CREATE PASSWORD POLICY dba_policy
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_MAX_LENGTH = 18
    PASSWORD_MIN_UPPER_CASE_CHARS = 2
    PASSWORD_MIN_LOWER_CASE_CHARS = 2
    PASSWORD_MIN_NUMERIC_CHARS = 2
    PASSWORD_MIN_SPECIAL_CHARS = 1
    PASSWORD_MIN_AGE_DAYS = 1
    PASSWORD_MAX_AGE_DAYS = 45
    PASSWORD_MAX_RETRIES = 3
    PASSWORD_LOCKOUT_TIME_MINS = 30
    PASSWORD_HISTORY = 5
    COMMENT='Strict controls for DBAs';

CREATE PASSWORD POLICY analyst_policy
    COMMENT='Defaults for analysts';

SHOW PASSWORD POLICIES;

┌─────────────────┬───────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ name            │ comment                       │ options                                                                                                                             │
├─────────────────┼───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ analyst_policy  │ Defaults for analysts         │ MIN_LENGTH=8, MAX_LENGTH=256, MIN_UPPER_CASE_CHARS=1, MIN_LOWER_CASE_CHARS=1, MIN_NUMERIC_CHARS=1, MIN_SPECIAL_CHARS=0, ... HISTORY=0        │
│ dba_policy      │ Strict controls for DBAs      │ MIN_LENGTH=12, MAX_LENGTH=18, MIN_UPPER_CASE_CHARS=2, MIN_LOWER_CASE_CHARS=2, MIN_NUMERIC_CHARS=2, MIN_SPECIAL_CHARS=1, ... HISTORY=5       │
└─────────────────┴───────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2. Attach the Policy to Users

```sql
CREATE USER dba_jane IDENTIFIED BY 'Str0ngPass123!' WITH SET PASSWORD POLICY='dba_policy';

CREATE USER analyst_mike IDENTIFIED BY 'Abc12345'
    WITH SET PASSWORD POLICY='analyst_policy';

CREATE USER analyst_zoe IDENTIFIED BY 'Byt3Crush!';
ALTER USER analyst_zoe WITH SET PASSWORD POLICY='analyst_policy';
```

### 3. Verify the Assignments

```sql
DESC USER dba_jane;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name   │ hostname │       auth_type      │ default_role │ roles │ disabled │ network_policy │ password_policy │ must_change_password │
├─────────┼──────────┼──────────────────────┼──────────────┼───────┼──────────┼────────────────┼─────────────────┼──────────────────────┤
│ dba_jane│ %        │ double_sha1_password │              │       │ false    │                │ dba_policy      │ NULL                 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

DESC PASSWORD POLICY dba_policy;

Name       |Comment                     |Options
-----------+----------------------------+---------------------------------------------------------------------------------------------------------------------------------+
dba_policy |Strict controls for DBAs    |MIN_LENGTH=12,MAX_LENGTH=18,MIN_UPPER_CASE_CHARS=2,MIN_LOWER_CASE_CHARS=2,MIN_NUMERIC_CHARS=2,MIN_SPECIAL_CHARS=1,...,HISTORY=5   |
```

### 4. Update a Policy Centrally

Use [ALTER PASSWORD POLICY](/tidb-cloud-lake/sql/alter-password-policy.md) to tighten rules without touching each user:

```sql
ALTER PASSWORD POLICY analyst_policy SET
    PASSWORD_MIN_SPECIAL_CHARS = 1
    PASSWORD_MAX_AGE_DAYS = 60
    COMMENT='Analysts need specials now';

DESC PASSWORD POLICY analyst_policy;

Name           |Comment                      |Options
---------------+-----------------------------+------------------------------------------------------------------------------------------------------------------------+
analyst_policy |Analysts need specials now   |MIN_LENGTH=8,MAX_LENGTH=256,MIN_UPPER_CASE_CHARS=1,MIN_LOWER_CASE_CHARS=1,MIN_NUMERIC_CHARS=1,MIN_SPECIAL_CHARS=1,...    |
```

Every user referencing `analyst_policy` now inherits the stricter password mix and expiry window automatically.

### 5. Detach and Clean Up

```sql
ALTER USER analyst_zoe WITH UNSET PASSWORD POLICY;
DROP PASSWORD POLICY analyst_policy;
```

Databend prevents you from dropping a policy that is still in use; unset it from all users before running `DROP PASSWORD POLICY`.

---

For full syntax, see the [Password Policy SQL reference](/tidb-cloud-lake/sql/password-policy-sql.md), which covers `CREATE`, `ALTER`, `SHOW`, `DESC`, and `DROP`.
