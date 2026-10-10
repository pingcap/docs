---
title: DROP ROLE
summary: 指定したロールをシステムから削除します。
---

# DROP ROLE

指定したロールをシステムから削除します。

## 構文 {#syntax}

```sql
DROP ROLE [ IF EXISTS ] <role_name>
```

## 使用上の注意 {#usage-notes}

* ロールがユーザーに付与されている場合、{{{ .lake }}} はそのロールから付与を自動的に削除できません。

## 例 {#examples}

```sql
DROP ROLE role1;
```