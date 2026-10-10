---
title: ALTER PASSWORD POLICY
summary: {{{ .lake }}} 内の既存のパスワードポリシーを変更します。
---

# ALTER PASSWORD POLICY

{{{ .lake }}} 内の既存のパスワードポリシーを変更します。

## 構文 {#syntax}

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

パスワードポリシー属性の詳細な説明については、[パスワードポリシー属性](/tidb-cloud-lake/sql/create-password-policy.md#password-policy-attributes) を参照してください。

## 例 {#examples}

この例では、最小パスワード長を 10 文字に設定した `SecureLogin` という名前のパスワードポリシーを作成し、その後、10 文字から 16 文字までのパスワードを許可するように更新します。

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;

ALTER PASSWORD POLICY SecureLogin SET
    PASSWORD_MIN_LENGTH = 10
    PASSWORD_MAX_LENGTH = 16;
```