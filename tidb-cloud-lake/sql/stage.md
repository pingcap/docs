---
title: Stage
summary: このページでは、{{{ .lake }}} における stage 操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。
---

# Stage

このページでは、{{{ .lake }}} における stage 操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。

## stage の管理 {#stage-management}

| Command | 説明 |
|---------|-------------|
| [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) | ファイルを保存するための新しい stage を作成します |
| [DROP STAGE](/tidb-cloud-lake/sql/drop-stage.md) | stage を削除します |
| [PRESIGN](/tidb-cloud-lake/sql/presign.md) | stage にアクセスするための署名付き URL を生成します |

## stage の操作 {#stage-operations}

| Command | 説明 |
|---------|-------------|
| [LIST STAGE](/tidb-cloud-lake/sql/list-stage-files.md) | stage 内のファイルを一覧表示します |
| [REMOVE STAGE](/tidb-cloud-lake/sql/remove-stage-files.md) | stage からファイルを削除します |

## stage の情報 {#stage-information}

| Command | 説明 |
|---------|-------------|
| [DESC STAGE](/tidb-cloud-lake/sql/desc-stage.md) | stage の詳細情報を表示します |
| [SHOW STAGES](/tidb-cloud-lake/sql/show-stages.md) | 現在または指定したデータベース内のすべての stage を一覧表示します |

## 関連トピック {#related-topics}

- [stage からロード](/tidb-cloud-lake/guides/load-from-stage.md)
- [クエリと変換](/tidb-cloud-lake/guides/query-stage.md)
- [ファイル形式 (DDL)](/tidb-cloud-lake/sql/file-format.md)

> **Note:**
>
> {{{ .lake }}} の stage は、テーブルにロード (load) したり、テーブルからアンロード (unload) したりするデータファイルの一時保存場所として使用されます。