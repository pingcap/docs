---
title: 管理コマンド
summary: このページでは、{{{ .lake }}} のシステム管理コマンドに関するリファレンス情報を提供します。
---

# 管理コマンド

このページでは、{{{ .lake }}} のシステム管理コマンドに関するリファレンス情報を提供します。

## システム監視 {#system-monitoring}

| コマンド | 説明 |
|---------|-------------|
| **[SHOW PROCESSLIST](/tidb-cloud-lake/sql/show-processlist.md)** | アクティブなクエリと接続を表示します |
| **[SHOW METRICS](/tidb-cloud-lake/sql/show-metrics.md)** | システムパフォーマンスメトリクスを表示します |
| **[KILL](/tidb-cloud-lake/sql/kill.md)** | 実行中のクエリまたは接続を終了します |
| **[RUST BACKTRACE](/tidb-cloud-lake/sql/system-enable-disable-exception-backtrace.md)** | Rust のスタックトレースをデバッグします |

## アクセス制御 {#access-control}

| コマンド | 説明 |
|---------|-------------|
| **[FLUSH PRIVILEGES](/tidb-cloud-lake/guides/privileges.md)** | すべてのクエリノードに対して、ロールおよび権限メタデータの再ロードを強制します |

## 設定管理 {#configuration-management}

| コマンド | 説明 |
|---------|-------------|
| **[SET](/tidb-cloud-lake/sql/set.md)** | グローバル設定パラメータを設定します |
| **[UNSET](/tidb-cloud-lake/sql/unset.md)** | 設定を削除します |
| **[SET VARIABLE](/tidb-cloud-lake/sql/set-var.md)** | ユーザー定義変数を管理します |
| **[SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md)** | 現在のシステム設定を表示します |

## 関数管理 {#function-management}

| コマンド | 説明 |
|---------|-------------|
| **[SHOW FUNCTIONS](/tidb-cloud-lake/sql/show-functions.md)** | 組み込み関数を一覧表示します |
| **[SHOW USER FUNCTIONS](/tidb-cloud-lake/sql/show-user-functions.md)** | ユーザー定義関数を一覧表示します |
| **[SHOW TABLE FUNCTIONS](/tidb-cloud-lake/sql/show-table-functions.md)** | テーブル値関数を一覧表示します |

## ストレージメンテナンス {#storage-maintenance}

| コマンド | 説明 |
|---------|-------------|
| **[VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md)** | テーブルからストレージ領域を回収します |
| **[VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md)** | 削除されたテーブルデータをクリーンアップします |
| **[VACUUM TEMP FILES](/tidb-cloud-lake/sql/vacuum-temporary-files.md)** | 一時ファイルを削除します |
| **[VACUUM VIRTUAL COLUMN](/tidb-cloud-lake/sql/vacuum-virtual-column.md)** | 古くなった仮想カラムファイルを削除します |
| **[SHOW INDEXES](/tidb-cloud-lake/sql/show-indexes.md)** | テーブルのインデックスを表示します |

## 動的実行 {#dynamic-execution}

| コマンド | 説明 |
|---------|-------------|
| **[EXECUTE IMMEDIATE](/tidb-cloud-lake/sql/execute-immediate.md)** | 動的に構築された SQL 文を実行します |