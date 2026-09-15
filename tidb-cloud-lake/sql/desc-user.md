---
title: DESC USER
summary: 显示特定 SQL 用户的详细信息，包括认证类型、角色、网络策略、密码策略以及其他与用户相关的设置。
---

# DESC USER

显示特定 SQL 用户的详细信息，包括认证类型、角色、网络策略、密码策略以及其他与用户相关的设置。

## 语法 {#syntax}

```sql
DESC[RIBE] USER <username>
```

## 示例 {#examples}

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

DESC USER eric;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │ hostname │       auth_type      │ default_role │  roles │ disabled │   network_policy  │   password_policy  │ must_change_password │
├────────┼──────────┼──────────────────────┼──────────────┼────────┼──────────┼───────────────────┼────────────────────┼──────────────────────┤
│ eric   │ %        │ double_sha1_password │              │        │ false    │ my_network_policy │ my_password_policy │ NULL                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```