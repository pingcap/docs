---
title: DROP PASSWORD POLICY
summary: "{{{ .lake }}} から既存のパスワードポリシーを削除します。パスワードポリシーを削除する前に、このポリシーがどのユーザーにも関連付けられていないことを確認してください。"
---

# DROP PASSWORD POLICY

{{{ .lake }}} から既存のパスワードポリシーを削除します。パスワードポリシーを削除する前に、このポリシーがどのユーザーにも関連付けられていないことを確認してください。

## 構文 {#syntax}

```sql
DROP PASSWORD POLICY [ IF EXISTS ] <policy_name>
```

## 例 {#examples}

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;

DROP PASSWORD POLICY SecureLogin;
```