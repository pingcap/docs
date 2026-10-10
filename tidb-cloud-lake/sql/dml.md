---
title: DML (Data Manipulation Language) コマンド
summary: このページでは、{{{ .lake }}} における DML (Data Manipulation Language) コマンドのリファレンス情報を提供します。
---

# DML (Data Manipulation Language) コマンド

このページでは、{{{ .lake }}} における DML (Data Manipulation Language) コマンドのリファレンス情報を提供します。

## データ変更 {#data-modification}

| コマンド | 説明 |
|---------|-------------|
| **[INSERT](/tidb-cloud-lake/sql/insert.md)** | テーブルに新しい行を追加します |
| **[INSERT MULTI](/tidb-cloud-lake/sql/insert-multi-table.md)** | 1 つのステートメントで複数のテーブルにデータを挿入します |
| **[UPDATE](/tidb-cloud-lake/sql/update.md)** | テーブル内の既存の行を変更します |
| **[DELETE](/tidb-cloud-lake/sql/delete.md)** | テーブルから行を削除します |
| **[REPLACE](/tidb-cloud-lake/sql/replace.md)** | 新しい行を挿入するか、既存の行を更新します |
| **[MERGE](/tidb-cloud-lake/sql/merge.md)** | 条件に基づいて upsert 操作を実行します |

## データのロード (load) とエクスポート {#data-loading-export}

| コマンド | 説明 |
|---------|-------------|
| **[COPY INTO Table](/tidb-cloud-lake/sql/copy-into-table.md)** | ファイルからテーブルにデータをロードします |
| **[COPY INTO Location](/tidb-cloud-lake/sql/copy-into-location.md)** | テーブルデータをファイルにエクスポートします |