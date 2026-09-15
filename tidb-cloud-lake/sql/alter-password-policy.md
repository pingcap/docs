---
title: ALTER PASSWORD POLICY
summary: 修改 {{{ .lake }}} 中现有的密码策略。
---

# ALTER PASSWORD POLICY

修改 {{{ .lake }}} 中现有的密码策略。

## 语法 {#syntax}

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

有关密码策略属性的详细说明，请参见[密码策略属性](/tidb-cloud-lake/sql/create-password-policy.md#password-policy-attributes)。

## 示例 {#examples}

以下示例创建了一个名为 `SecureLogin` 的密码策略，将密码最小长度要求设置为 10 个字符，随后将其修改为允许密码长度在 10 到 16 个字符之间：

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;

ALTER PASSWORD POLICY SecureLogin SET
    PASSWORD_MIN_LENGTH = 10
    PASSWORD_MAX_LENGTH = 16;
```