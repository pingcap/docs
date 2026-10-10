---
title: Table Functions
summary: このページでは、{{{ .lake }}} のテーブル関数に関するリファレンス情報を提供します。テーブル関数は、行の集合（テーブルに類似）を返し、クエリの FROM 句で使用できます。
---

# Table Functions

このページでは、{{{ .lake }}} のテーブル関数に関するリファレンス情報を提供します。テーブル関数は、行の集合（テーブルに類似）を返し、クエリの FROM 句で使用できます。

## データスキーマとファイル検査 {#data-schema-file-inspection}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [INFER_SCHEMA](/tidb-cloud-lake/sql/infer-schema.md) | ファイルメタデータのスキーマを検出し、カラム定義を取得します | `SELECT * FROM INFER_SCHEMA(LOCATION => '@mystage/data/')` |
| [INSPECT_PARQUET](/tidb-cloud-lake/sql/inspect-parquet.md) | Parquet ファイルの構造を検査します | `SELECT * FROM INSPECT_PARQUET(LOCATION => '@mystage/data.parquet')` |

## stage とクエリ管理 {#stage-query-management}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [LIST_STAGE](/tidb-cloud-lake/sql/list-stage.md) | stage 内のファイルを一覧表示します | `SELECT * FROM LIST_STAGE(LOCATION => '@mystage/data/')` |
| [RESULT_SCAN](/tidb-cloud-lake/sql/result-scan.md) | 以前のクエリの結果セットを取得します | `SELECT * FROM RESULT_SCAN(LAST_QUERY_ID())` |

## データ生成 {#data-generation}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [GENERATE_SERIES](/tidb-cloud-lake/sql/generate-series.md) | 値のシーケンスを生成します | `SELECT * FROM GENERATE_SERIES(1, 10, 2)` |

## データ変換と展開 {#data-transformation-expansion}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [FLATTEN](/tidb-cloud-lake/sql/flatten.md) | ネストされた JSON または配列データを表形式に変換します | `SELECT * FROM FLATTEN(INPUT => parse_json('[1,2,3]'))` |

## システム情報と管理 {#system-information-management}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [SHOW_GRANTS](/tidb-cloud-lake/sql/show-grants.md) | 付与された権限を表示します | `SELECT * FROM SHOW_GRANTS()` |
| [SHOW_VARIABLES](/tidb-cloud-lake/sql/show-variables.md) | システム変数を表示します | `SELECT * FROM SHOW_VARIABLES()` |
| [STREAM_STATUS](/tidb-cloud-lake/sql/stream-status.md) | ストリームのステータス情報を表示します | `SELECT * FROM STREAM_STATUS('mystream')` |
| [TASK_HISTROY](/tidb-cloud-lake/sql/task-history.md) | タスク実行履歴を表示します | `SELECT * FROM TASK_HISTROY('mytask')` |
| [POLICY_REFERENCES](/tidb-cloud-lake/sql/policy-references.md) | セキュリティポリシーとテーブル/ビューの関連付けを返します | `SELECT * FROM POLICY_REFERENCES(POLICY_NAME => 'mypolicy')` |
| [TAG_REFERENCES](/tidb-cloud-lake/sql/tag-references.md) | データベースオブジェクトに割り当てられたタグを返します | `SELECT * FROM TAG_REFERENCES('mydb.mytable', 'TABLE')` |
| [GET_LINEAGE](/tidb-cloud-lake/sql/get-lineage.md) | 上流または下流のオブジェクトおよびカラムのリネージを返します | `SELECT * FROM GET_LINEAGE('mydb.mytable', 'TABLE', 'UPSTREAM')` |

## ストレージエンジン関数 {#storage-engine-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [FUSE_VACUUM_TEMPORARY_TABLE](/tidb-cloud-lake/sql/fuse-vacuum-temporary-table.md) | 一時テーブルをクリーンアップします | `SELECT * FROM FUSE_VACUUM_TEMPORARY_TABLE()` |
| [FUSE_AMEND](/tidb-cloud-lake/sql/system-fuse-amend.md) | データ修正を管理します | `SELECT * FROM FUSE_AMEND()` |

## Iceberg 統合 {#iceberg-integration}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [ICEBERG_MANIFEST](/tidb-cloud-lake/sql/iceberg-manifest.md) | Iceberg テーブルの manifest 情報を表示します | `SELECT * FROM ICEBERG_MANIFEST('mytable')` |
| [ICEBERG_SNAPSHOT](/tidb-cloud-lake/sql/iceberg-snapshot.md) | Iceberg テーブルの snapshot 情報を表示します | `SELECT * FROM ICEBERG_SNAPSHOT('mytable')` |

## 匿名化 {#anonymization}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [OBFUSCATE](/tidb-cloud-lake/sql/obfuscate.md) | データセットの匿名化 | `SELECT * FROM OBFUSCATE(users)` |