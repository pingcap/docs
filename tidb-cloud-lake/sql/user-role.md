---
title: User & Role
summary: このページでは、{{{ .lake }}} におけるユーザーおよびロールの操作について、参照しやすいように機能別に整理して包括的に説明します。
---

# User & Role

このページでは、{{{ .lake }}} におけるユーザーおよびロールの操作について、参照しやすいように機能別に整理して包括的に説明します。

## ユーザー管理 {#user-management}

| Command | 説明 |
|---------|-------------|
| [CREATE USER](/tidb-cloud-lake/sql/create-user.md) | 新しいユーザーアカウントを作成します |
| [ALTER USER](/tidb-cloud-lake/sql/alter-user.md) | 既存のユーザーアカウントを変更します |
| [DROP USER](/tidb-cloud-lake/sql/drop-user.md) | ユーザーアカウントを削除します |
| [DESC USER](/tidb-cloud-lake/sql/desc-user.md) | ユーザーの詳細情報を表示します |
| [SHOW USERS](/tidb-cloud-lake/sql/show-users.md) | システム内のすべてのユーザーを一覧表示します |

## ロール管理 {#role-management}

| Command | 説明 |
|---------|-------------|
| [CREATE ROLE](/tidb-cloud-lake/sql/create-role.md) | 新しいロールを作成します |
| [DROP ROLE](/tidb-cloud-lake/sql/drop-role.md) | ロールを削除します |
| [SET ROLE](/tidb-cloud-lake/sql/set-role.md) | セッションの現在のアクティブロールを設定します |
| [SET SECONDARY ROLES](/tidb-cloud-lake/sql/set-secondary-roles.md) | セッションのセカンダリロールを設定します |
| [SHOW ROLES](/tidb-cloud-lake/sql/show-roles.md) | システム内のすべてのロールを一覧表示します |

## 権限管理 {#privilege-management}

| Command | 説明 |
|---------|-------------|
| [GRANT](/tidb-cloud-lake/sql/grant.md) | ロールに権限を付与します |
| [REVOKE](/tidb-cloud-lake/sql/revoke.md) | ロールから権限を削除します |
| [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md) | ロールへの権限付与とロールの割り当てを表示します |

> **Note:**
>
> 適切なユーザーおよびロール管理は、データベースセキュリティに不可欠です。権限を付与する際は、常に最小権限の原則に従ってください。