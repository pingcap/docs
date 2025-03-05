---
title: mysql Schema
summary: TiDB システム テーブルについて学習します。
---

# <code>mysql</code>スキーマ {#code-mysql-code-schema}

`mysql`スキーマには、TiDB システム テーブルが含まれています。設計は MySQL の`mysql`スキーマに似ており、 `mysql.user`などのテーブルを直接編集できます。また、MySQL の拡張機能であるテーブルもいくつか含まれています。

> **注記：**
>
> ほとんどのシナリオでは、 `INSERT` 、 `UPDATE` 、または`DELETE`を使用してシステム テーブルの内容を直接変更することは推奨されません。代わりに、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 、 [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 、 [`DROP USER`](/sql-statements/sql-statement-drop-user.md) 、 [`GRANT`](/sql-statements/sql-statement-grant-privileges.md) 、 [`REVOKE`](/sql-statements/sql-statement-revoke-privileges.md) 、および[`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md)などのステートメントを使用して、ユーザーと権限を管理します。システム テーブルを直接変更する必要がある場合は、 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)使用して変更を有効にします。

## システムテーブルの付与 {#grant-system-tables}

これらのシステム テーブルには、ユーザー アカウントとその権限に関する付与情報が含まれています。

-   [`user`](/mysql-schema/mysql-schema-user.md) : ユーザーアカウント、グローバル権限、およびその他の非権限列
-   `db` : データベースレベルの権限
-   `tables_priv` : テーブルレベルの権限
-   `columns_priv` : 列レベルの権限
-   `password_history` : パスワード変更履歴
-   `default_roles` : ユーザーのデフォルトロール
-   `global_grants` : 動的権限
-   `global_priv` : 証明書に基づく認証情報
-   `role_edges` : 役割間の関係

## クラスタステータスシステムテーブル {#cluster-status-system-tables}

-   `tidb`テーブルには、TiDB に関するいくつかのグローバル情報が含まれています。

    -   `bootstrapped` : TiDB クラスターが初期化されているかどうか。この値は読み取り専用であり、変更できないことに注意してください。
    -   `tidb_server_version` : TiDB が初期化されたときのバージョン情報。この値は読み取り専用であり、変更できないことに注意してください。
    -   `system_tz` : TiDB のシステムタイムゾーン。
    -   `new_collation_enabled` : TiDB が[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)有効にしているかどうか。この値は読み取り専用であり、変更できないことに注意してください。

## サーバー側ヘルプシステムテーブル {#server-side-help-system-tables}

現在、 `help_topic`は NULL です。

## 統計システムテーブル {#statistics-system-tables}

-   `stats_buckets` : 統計の塊
-   `stats_histograms` : 統計のヒストグラム
-   `stats_top_n` : 統計のトップN
-   `stats_meta` : テーブルのメタ情報（行の総数や更新された行数など）
-   `stats_extended` : 列間の順序相関などの拡張統計
-   `stats_feedback` : 統計のクエリフィードバック
-   `stats_fm_sketch` : 統計列のヒストグラムのFMSketch分布
-   `stats_table_locked` : ロックされた統計に関する情報
-   `stats_meta_history` : 履歴統計のメタ情報
-   `stats_history` : 履歴統計のその他の情報
-   `analyze_options` : 各テーブルのデフォルトの`analyze`オプション
-   `column_stats_usage` : 列統計の使用
-   `analyze_jobs` : 進行中の統計収集タスクと過去 7 日間の履歴タスク レコード

## 実行計画関連のシステムテーブル {#execution-plan-related-system-tables}

-   `bind_info` : 実行計画のバインディング情報
-   `capture_plan_baselines_blacklist` : 実行プランの自動バインディングのブロックリスト

## PLAN REPLAYER に関連するシステム テーブル {#system-tables-related-to-plan-replayer}

-   `plan_replayer_status` : ユーザーが登録した[`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture)タスク
-   `plan_replayer_task` : [`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture)タスクの結果

## GC ワーカー システム テーブル {#gc-worker-system-tables}

> **注記：**
>
> GC ワーカー システム テーブルは TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

-   `gc_delete_range` : 削除するKV範囲
-   `gc_delete_range_done` : 削除されたKV範囲

## キャッシュされたテーブルに関連するシステムテーブル {#system-tables-related-to-cached-tables}

-   `table_cache_meta`キャッシュされたテーブルのメタデータを格納します。

## TTL関連のシステムテーブル {#ttl-related-system-tables}

-   `tidb_ttl_table_status` : 以前に実行されたTTLジョブと、すべてのTTLテーブルに対して実行中のTTLジョブ
-   `tidb_ttl_task` : 現在進行中のTTLサブタスク
-   `tidb_ttl_job_history` : 過去90日間のTTLタスクの実行履歴

## ランナウェイクエリに関連するシステムテーブル {#system-tables-related-to-runaway-queries}

-   `tidb_runaway_queries` : 過去 7 日間に特定されたすべてのランナウェイ クエリの履歴レコード
-   `tidb_runaway_watch` : 暴走クエリの監視リスト
-   `tidb_runaway_watch_done` : 削除または期限切れのランナウェイクエリの監視リスト

## メタデータ ロックに関連するシステム テーブル {#system-tables-related-to-metadata-locks}

-   `tidb_mdl_view` : メタデータロックのビュー。現在ブロックされているDDLステートメントに関する情報を表示するために使用できます。
-   `tidb_mdl_info` : TiDBがノード間でメタデータロックを同期するために内部的に使用する

## DDL ステートメントに関連するシステム テーブル {#system-tables-related-to-ddl-statements}

-   `tidb_ddl_history` : DDL文の履歴レコード
-   `tidb_ddl_job` : 現在 TiDB によって実行されている DDL ステートメントのメタデータ
-   `tidb_ddl_reorg` : 現在 TiDB によって実行されている物理 DDL ステートメント (インデックスの追加など) のメタデータ

## TiDB 分散実行フレームワーク (DXF) に関連するシステム テーブル {#system-tables-related-to-tidb-distributed-execution-framework-dxf}

-   `dist_framework_meta` : 分散実行フレームワーク (DXF) タスク スケジューラのメタデータ
-   `tidb_global_task` : 現在のDXFタスクのメタデータ
-   `tidb_global_task_history` : 成功したタスクと失敗したタスクの両方を含む、履歴 DXF タスクのメタデータ
-   `tidb_background_subtask` : 現在のDXFサブタスクのメタデータ
-   `tidb_background_subtask_history` : 履歴DXFサブタスクのメタデータ

## リソース制御に関連するシステムテーブル {#system-tables-related-to-resource-control}

-   `request_unit_by_group` : すべてのリソース グループの消費されたリソース ユニット (RU) の履歴レコード

## その他のシステムテーブル {#miscellaneous-system-tables}

<CustomContent platform="tidb">

> **注記：**
>
> `tidb` 、 `expr_pushdown_blacklist` 、 `opt_rule_blacklist` 、 `table_cache_meta` 、 `tidb_import_jobs` 、および`tidb_timers`システム テーブルは TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

-   `GLOBAL_VARIABLES` : グローバルシステム変数テーブル
-   `expr_pushdown_blacklist` : 式プッシュダウンのブロックリスト
-   `opt_rule_blacklist` : 論理最適化ルールのブロックリスト
-   `tidb_import_jobs` : [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)の求人情報
-   `tidb_timers` : 内部タイマーのメタデータ
-   `advisory_locks` : [ロック関数](/functions-and-operators/locking-functions.md)に関連する情報

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `GLOBAL_VARIABLES` : グローバルシステム変数テーブル

</CustomContent>
