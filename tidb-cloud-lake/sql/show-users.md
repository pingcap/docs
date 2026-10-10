---
title: SHOW USERS
summary: システム内のすべての SQL ユーザーを一覧表示します。{{{ .lake }}} を使用している場合、このコマンドは {{{ .lake }}} へのログインに使用される組織内のユーザーアカウント（メールアドレス）も表示します。
---

# SHOW USERS

システム内のすべての SQL ユーザーを一覧表示します。{{{ .lake }}} を使用している場合、このコマンドは {{{ .lake }}} へのログインに使用される組織内のユーザーアカウント（メールアドレス）も表示します。

## 構文 {#syntax}

```sql
SHOW USERS
```

## 例 {#examples}

```sql
CREATE NETWORK POLICY my_network_policy ALLOWED_IP_LIST=('192.168.100.0/24');

CREATE PASSWORD POLICY my_password_policy
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_MAX_LENGTH = 24
    PASSWORD_MIN_UPPER_CASE_CHARS = 2
    PASSWORD_MIN_LOWER_CASE_CHARS = 2
    PASSWORD_MIN_NUMERIC_CHARS = 2
    PASSWORD_MIN_SPECIAL_CHARS = 2
    PASSWORD_MIN_AGE_DAYS = 1
    PASSWORD_MAX_AGE_DAYS = 30
    PASSWORD_MAX_RETRIES = 3
    PASSWORD_LOCKOUT_TIME_MINS = 30
    PASSWORD_HISTORY = 5
    COMMENT = 'test comment';

CREATE USER eric IDENTIFIED BY '123ABCabc$$123' WITH SET PASSWORD POLICY='my_password_policy', SET NETWORK POLICY='my_network_policy';

SHOW USERS;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │ hostname │       auth_type      │ is_configured │  default_role │     roles     │ disabled │   network_policy  │   password_policy  │ must_change_password │
├────────┼──────────┼──────────────────────┼───────────────┼───────────────┼───────────────┼──────────┼───────────────────┼────────────────────┼──────────────────────┤
│ eric   │ %        │ double_sha1_password │ NO            │               │               │ false    │ my_network_policy │ my_password_policy │ NULL                 │
│ root   │ %        │ no_password          │ YES           │ account_admin │ account_admin │ false    │ NULL              │ NULL               │ NULL                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```