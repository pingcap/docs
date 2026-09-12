---
title: CURRENT_USER
summary: 返回服务器用于对当前客户端进行身份验证的账户的用户名和主机名组合。该账户决定了你的访问权限。返回值是 utf8 字符集中的字符串。
---

# CURRENT_USER

返回服务器用于对当前客户端进行身份验证的账户的用户名和主机名组合。该账户决定了你的访问权限。返回值是 utf8 字符集中的字符串。

## 语法 {#syntax}

```sql
CURRENT_USER()
```

## 示例 {#examples}

```sql
SELECT CURRENT_USER();

┌────────────────┐
│ current_user() │
├────────────────┤
│ 'root'@'%'     │
└────────────────┘
```