---
title: Stored Procedure
summary: このページでは、{{{ .lake }}} における Stored Procedure の操作について、参照しやすいように機能別に整理して包括的に説明します。
---

# Stored Procedure

このページでは、{{{ .lake }}} における Stored Procedure の操作について、参照しやすいように機能別に整理して包括的に説明します。

## Procedure の管理 {#procedure-management}

| Command | 説明 |
|---------|-------------|
| [CREATE PROCEDURE](/tidb-cloud-lake/sql/create-procedure.md) | 新しいストアドプロシージャを作成します |
| [DROP PROCEDURE](/tidb-cloud-lake/sql/drop-procedure.md) | ストアドプロシージャを削除します |
| [CALL](/tidb-cloud-lake/sql/call-procedure.md) | ストアドプロシージャを実行します |

## Procedure の情報 {#procedure-information}

| Command | 説明 |
|---------|-------------|
| [DESCRIBE PROCEDURE](/tidb-cloud-lake/sql/desc-procedure.md) | 特定のストアドプロシージャの詳細を表示します |
| [SHOW PROCEDURES](/tidb-cloud-lake/sql/show-procedures.md) | 現在のデータベース内のすべてのストアドプロシージャを一覧表示します |

> **Note:**
>
> {{{ .lake }}} のストアドプロシージャでは、一連の SQL 文を再利用可能な単位としてカプセル化し、単一のコマンドとして実行できます。これにより、コードの構成と保守性が向上します。

## 参考資料 {#further-reading}

変数処理、制御フロー、カーソル、プロシージャ内での動的 SQL の使用方法を含む完全な言語リファレンスについては、[Stored Procedure & SQL Scripting](/tidb-cloud-lake/sql/stored-procedure-scripting.md) を参照してください。