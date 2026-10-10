---
title: コンテキスト関数
summary: このページでは、{{{ .lake }}} のコンテキスト関連の関数に関するリファレンス情報を提供します。これらの関数は、現在のセッション、データベース、またはシステムコンテキストに関する情報を返します。
---

# コンテキスト関数

このページでは、{{{ .lake }}} のコンテキスト関連の関数に関するリファレンス情報を提供します。これらの関数は、現在のセッション、データベース、またはシステムコンテキストに関する情報を返します。

## セッション情報関数 {#session-information-functions}

| Function | 説明 | 例 |
|----------|-------------|--------|
| [CONNECTION_ID](/tidb-cloud-lake/sql/connection-id.md) | 現在の接続の接続 ID を返します | `CONNECTION_ID()` → `42` |
| [CURRENT_USER](/tidb-cloud-lake/sql/current-user.md) | 現在の接続のユーザー名とホストを返します | `CURRENT_USER()` → `'root'@'%'` |
| [LAST_QUERY_ID](/tidb-cloud-lake/sql/last-query-id.md) | 最後に実行されたクエリのクエリ ID を返します | `LAST_QUERY_ID()` → `'01890a5d-ac96-7cc6-8128-01d71ab8b93e'` |

## データベースコンテキスト関数 {#database-context-functions}

| Function | 説明 | 例 |
|----------|-------------|--------|
| [CURRENT_CATALOG](/tidb-cloud-lake/sql/current-catalog.md) | 現在のカタログ名を返します | `CURRENT_CATALOG()` → `'default'` |
| [DATABASE](/tidb-cloud-lake/sql/database-function.md) | 現在のデータベース名を返します | `DATABASE()` → `'default'` |

## システム情報関数 {#system-information-functions}

| Function | 説明 | 例 |
|----------|-------------|--------|
| [VERSION](/tidb-cloud-lake/sql/version.md) | {{{ .lake }}} の現在のバージョンを返します | `VERSION()` → `'LakeQuery v1.2.252-nightly-193ed56304'` |