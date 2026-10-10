---
title: Table
summary: このページでは、{{{ .lake }}} におけるテーブル操作の包括的な概要を、参照しやすいよう機能別に整理して紹介します。
---

# Table

このページでは、{{{ .lake }}} におけるテーブル操作の包括的な概要を、参照しやすいよう機能別に整理して紹介します。

## テーブルの作成 {#table-creation}

| コマンド | 説明 |
|---------|-------------|
| [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) | 指定したカラムとオプションで新しいテーブルを作成します |
| [CREATE TABLE ... LIKE](/tidb-cloud-lake/sql/create-table.md#create-table--like) | 既存のテーブルと同じカラム定義を持つテーブルを作成します |
| [CREATE TABLE ... AS](/tidb-cloud-lake/sql/create-table.md#create-table--as) | テーブルを作成し、SELECT クエリの結果に基づいてデータを挿入します |
| [CREATE TRANSIENT TABLE](/tidb-cloud-lake/sql/create-transient-table.md) | Time Travel をサポートしないテーブルを作成します |
| [CREATE EXTERNAL TABLE](/tidb-cloud-lake/sql/create-external-table.md) | 指定した外部ロケーションに保存されたデータを持つテーブルを作成します |
| [ATTACH TABLE](/tidb-cloud-lake/sql/attach-table.md) | 既存のテーブルに関連付けることでテーブルを作成します |

## テーブルの変更 {#table-modification}

| コマンド | 説明 |
|---------|-------------|
| [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md) | テーブルのカラム、コメント、Fuse オプション、外部接続を変更するか、別のテーブルとメタデータを入れ替えます |
| [RENAME TABLE](/tidb-cloud-lake/sql/rename-table.md) | テーブル名を変更します |

## テーブル情報 {#table-information}

| コマンド | 説明 |
|---------|-------------|
| [DESCRIBE TABLE](/tidb-cloud-lake/sql/describe-table.md) / [SHOW FIELDS](/tidb-cloud-lake/sql/show-fields.md) | 指定したテーブルのカラムに関する情報を表示します |
| [SHOW FULL COLUMNS](/tidb-cloud-lake/sql/show-columns.md) | 指定したテーブルのカラムに関する詳細情報を取得します |
| [SHOW CREATE TABLE](/tidb-cloud-lake/sql/show-create-table.md) | 指定したテーブルを作成する CREATE TABLE 文を表示します |
| [SHOW TABLES](/tidb-cloud-lake/sql/show-tables.md) | 現在のデータベースまたは指定したデータベース内のテーブルを一覧表示します |
| [SHOW TABLE STATUS](/tidb-cloud-lake/sql/show-table-status.md) | データベース内のテーブルのステータスを表示します |
| [SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md) | 現在のデータベースまたは指定したデータベースで削除されたテーブルを一覧表示します |

## テーブルの削除とリカバリ {#table-deletion-recovery}

| コマンド | 説明 | リカバリオプション |
|---------|-------------|----------------|
| [TRUNCATE TABLE](/tidb-cloud-lake/sql/truncate-table.md) | テーブルのスキーマを保持したまま、テーブル内のすべてのデータを削除します | [FLASHBACK TABLE](/tidb-cloud-lake/sql/flashback-table.md) |
| [DROP TABLE](/tidb-cloud-lake/sql/drop-table.md) | テーブルを削除します | [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md) |
| [VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md) | テーブルの履歴データファイルを完全に削除します（Enterprise Edition） | リカバリ不可 |
| [VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md) | 削除済みテーブルのデータファイルを完全に削除します（Enterprise Edition） | リカバリ不可 |

## テーブルの最適化 {#table-optimization}

| コマンド | 説明 |
|---------|-------------|
| [OPTIMIZE TABLE](/tidb-cloud-lake/sql/optimize-table.md) | ストレージ容量を節約し、クエリ性能を向上させるために、履歴データを圧縮または削除します |
| [SET CLUSTER KEY](/tidb-cloud-lake/sql/set-cluster-key.md) | 大規模テーブルのクエリ性能を向上させるために、クラスターキーを設定します |

> **Note:**
>
> テーブルの最適化は高度な操作です。データ損失の可能性を避けるため、実行する前に必ずドキュメントをよく確認してください。