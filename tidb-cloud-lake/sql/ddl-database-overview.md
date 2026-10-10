---
title: データベース
summary: このページでは、{{{ .lake }}} におけるデータベース操作の包括的な概要を、参照しやすいよう機能別に整理して紹介します。
---

# データベース

このページでは、{{{ .lake }}} におけるデータベース操作の包括的な概要を、参照しやすいよう機能別に整理して紹介します。

## データベースの作成と管理 {#database-creation-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE DATABASE](/tidb-cloud-lake/sql/create-database.md) | 新しいデータベースを作成します |
| [ALTER DATABASE](/tidb-cloud-lake/sql/alter-database.md) | データベースを変更します |
| [DROP DATABASE](/tidb-cloud-lake/sql/drop-database.md) | データベースを削除します |
| [USE DATABASE](/tidb-cloud-lake/sql/use-database.md) | 現在の作業用データベースを設定します |
| [UNDROP DATABASE](/tidb-cloud-lake/sql/undrop-database.md) | 削除されたデータベースを復元します |

## データベース情報 {#database-information}

| コマンド | 説明 |
|---------|-------------|
| [SHOW DATABASES](/tidb-cloud-lake/sql/show-databases.md) | すべてのデータベースを一覧表示します |
| [SHOW CREATE DATABASE](/tidb-cloud-lake/sql/show-create-database.md) | データベースの CREATE DATABASE 文を表示します |
| [SHOW DROP DATABASES](/tidb-cloud-lake/sql/show-drop-databases.md) | 復元可能な削除済みデータベースを一覧表示します |

> **Note:**
>
> データベース操作は、{{{ .lake }}} でデータを整理するための基盤となります。これらのコマンドを実行する前に、適切な権限があることを確認してください。