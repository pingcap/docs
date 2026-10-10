---
title: TiDB Cloud Lake におけるデータライフサイクル
summary: "{{{ .lake }}} は、使い慣れた Data Definition Language (DDL) および Data Manipulation Language (DML) コマンドをサポートしており、データベースを簡単に管理できます。データの整理、保存、クエリ、変更、削除のいずれを行う場合でも、{{{ .lake }}} は一般的な業界標準に従っています。"
---

# TiDB Cloud Lake におけるデータライフサイクル

{{{ .lake }}} は、使い慣れた Data Definition Language (DDL) および Data Manipulation Language (DML) コマンドをサポートしており、データベースを簡単に管理できます。データの整理、保存、クエリ、変更、削除のいずれを行う場合でも、{{{ .lake }}} は一般的な業界標準に従っています。

## {{{ .lake }}} のオブジェクト {#lake-objects}

{{{ .lake }}} は、以下のオブジェクトの作成および変更をサポートしています。

- データベース
- テーブル
- 外部テーブル
- ストリーム
- ビュー
- インデックス
- Stage
- ファイル形式
- 接続
- ユーザー定義関数 (UDF)
- 外部関数
- ユーザー
- ロール
- 権限付与
- Warehouse
- タスク
- [スナップショットタグ](/tidb-cloud-lake/sql/table-versioning.md#snapshot-tags)

## データの整理 {#organizing-data}

データをデータベースとテーブルに整理します。

主なコマンド:

- [`CREATE DATABASE`](/tidb-cloud-lake/sql/create-database.md): 新しいデータベースを作成します。
- [`ALTER DATABASE`](/tidb-cloud-lake/sql/alter-database.md): 既存のデータベースを変更します。
- [`CREATE TABLE`](/tidb-cloud-lake/sql/create-table.md): 新しいテーブルを作成します。
- [`ALTER TABLE`](/tidb-cloud-lake/sql/alter-table.md): 既存のテーブルを変更します。

## データの保存 {#storing-data}

データをテーブルに直接追加できます。{{{ .lake }}} では、外部ファイルからテーブルにデータをインポートすることもできます。

主なコマンド:

- [`INSERT`](/tidb-cloud-lake/sql/insert.md): テーブルにデータを追加します。
- [`COPY INTO <table>`](/tidb-cloud-lake/sql/copy-into-table.md): 外部ファイルからデータを取り込みます。

## データのクエリ {#querying-data}

データがテーブルに格納されたら、`SELECT` を使用してデータを参照および分析できます。

主なコマンド:

- [`SELECT`](/tidb-cloud-lake/sql/select.md): テーブルからデータを取得します。

## データの操作 {#working-with-data}

データが {{{ .lake }}} に格納された後は、必要に応じて更新、置換、マージ、または削除できます。

主なコマンド:

- [`UPDATE`](/tidb-cloud-lake/sql/update.md): テーブル内のデータを変更します。
- [`REPLACE`](/tidb-cloud-lake/sql/replace.md): 既存のデータを置き換えます。
- [`MERGE`](/tidb-cloud-lake/sql/merge.md): メインテーブルとソーステーブル、またはサブクエリ間のデータを比較しながら、挿入、更新、削除をシームレスに実行します。
- [`DELETE`](/tidb-cloud-lake/sql/delete.md): テーブルからデータを削除します。

## データの削除 {#removing-data}

{{{ .lake }}} では、特定のデータ、テーブル全体、またはデータベース全体を削除できます。

主なコマンド:

- [`TRUNCATE TABLE`](/tidb-cloud-lake/sql/truncate-table.md): テーブル構造を削除せずに内容を消去します。
- [`DROP TABLE`](/tidb-cloud-lake/sql/drop-table.md): テーブルを削除します。
- [`DROP DATABASE`](/tidb-cloud-lake/sql/drop-database.md): データベースを削除します。