---
title: DROP PASSWORD POLICY
summary: 从 {{{ .lake }}} 中删除现有的密码策略。请注意，在删除密码策略之前，请确保该策略未与任何用户关联。
---

# DROP PASSWORD POLICY

从 {{{ .lake }}} 中删除现有的密码策略。请注意，在删除密码策略之前，请确保该策略未与任何用户关联。

## 语法 {#syntax}

```sql
DROP PASSWORD POLICY [ IF EXISTS ] <policy_name>
```

## 示例 {#examples}

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;

DROP PASSWORD POLICY SecureLogin;
```