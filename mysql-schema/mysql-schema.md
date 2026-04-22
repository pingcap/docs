---
title: mysql Schema
summary: TiDBのシステムテーブルについて学びましょう。
---

# <code>mysql</code>スキーマ {#code-mysql-code-schema}

`mysql`スキーマには、TiDBシステムテーブルが含まれています。この設計は、MySQLの`mysql`スキーマに似ており、 `mysql.user`などのテーブルを直接編集できます。また、MySQLの拡張機能となるテーブルも多数含まれています。

> **注記：**
>
> ほとんどのシナリオでは、 `INSERT` 、 `UPDATE` 、または`DELETE`を使用してシステムテーブルの内容を直接変更することは推奨されません。代わりに、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md) 、[`ALTER USER`](/sql-statements/sql-statement-alter-user.md) 、 [`DROP USER`](/sql-statements/sql-statement-drop-user.md) 、 [`GRANT`](/sql-statements/sql-statement-grant-privileges.md) 、 [`REVOKE`](/sql-statements/sql-statement-revoke-privileges.md) 、および[`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md)などのステートメントを使用して、ユーザーと権限を管理してください。システムテーブルの直接変更が避けられない場合は、 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md)を使用して変更を有効にしてください。

## 助成金システムテーブル {#grant-system-tables}

これらのシステムテーブルには、ユーザーアカウントとその権限に関する許可情報が含まれています。

-   [`user`](/mysql-schema/mysql-schema-user.md) ：ユーザーアカウント、グローバル権限、およびその他の権限以外の列
-   `db` : データベースレベルの権限
-   `tables_priv` : テーブルレベルの権限
-   `columns_priv` : 列レベルの権限
-   `password_history` : パスワード変更履歴
-   `default_roles` : ユーザーのデフォルトロール
-   `global_grants` : 動的権限
-   `global_priv` : 証明書に基づく認証情報
-   `role_edges` : 役割間の関係

## クラスタステータスシステムテーブル {#cluster-status-system-tables}

-   `tidb`テーブルには、TiDB に関するグローバル情報が含まれています。

    -   `bootstrapped` : TiDBクラスタが初期化されているかどうか。この値は読み取り専用であり、変更できません。
    -   `tidb_server_version` : TiDB の初期化時のバージョン情報。この値は読み取り専用であり、変更できません。
    -   `system_tz` : TiDB のシステム タイム ゾーン。
    -   `new_collation_enabled` : TiDB が[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)を有効にしたかどうか。この値は読み取り専用であり、変更できないことに注意してください。
    -   `cluster_id` （v8.5.6で追加）：TiDBクラスタの一意の識別子。この値は読み取り専用であり、変更できません。

## サーバー側のヘルプシステムテーブル {#server-side-help-system-tables}

現在、 `help_topic`は NULL です。

## 統計システム表 {#statistics-system-tables}

-   `stats_buckets` : 統計のバケット
-   `stats_histograms` : 統計のヒストグラム
-   `stats_top_n` : 統計のトップN
-   `stats_meta` : テーブルのメタ情報（行の総数や更新された行数など）
-   `stats_extended` : 列間の順序相関などの拡張統計
-   `stats_feedback` : 統計情報のクエリフィードバック
-   `stats_fm_sketch` : 統計列のヒストグラムの FMSketch 分布
-   `stats_table_locked` : ロックされた統計情報に関する情報
-   `stats_meta_history` : 履歴統計のメタ情報
-   `stats_history` : 履歴統計のその他の情報
-   `analyze_options` : 各テーブルのデフォルトの`analyze`オプション
-   `column_stats_usage` : 列統計の使用方法
-   `analyze_jobs` : 進行中の統計収集タスクと過去 7 日間の履歴タスク記録

## 実行計画関連のシステムテーブル {#execution-plan-related-system-tables}

-   `bind_info` : 実行計画のバインディング情報
-   `capture_plan_baselines_blacklist` : 実行プランの自動バインド用のブロックリスト

## PLAN REPLAYERに関連するシステムテーブル {#system-tables-related-to-plan-replayer}

-   `plan_replayer_status` : ユーザーが登録した[`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture)タスク
-   `plan_replayer_task` : [`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture)タスクの結果

## GCワーカーシステムテーブル {#gc-worker-system-tables}

> **注記：**
>
> GCワーカーシステムテーブルは、TiDBセルフマネージドでのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

-   `gc_delete_range` : 削除する KV 範囲
-   `gc_delete_range_done` : 削除された KV 範囲

## キャッシュされたテーブルに関連するシステムテーブル {#system-tables-related-to-cached-tables}

-   `table_cache_meta`キャッシュされたテーブルのメタデータを保存します。

## TTL関連のシステムテーブル {#ttl-related-system-tables}

-   `tidb_ttl_table_status` : すべてのTTLテーブルに対して、以前に実行されたTTLジョブと進行中のTTLジョブ
-   `tidb_ttl_task` : 現在進行中のTTLサブタスク
-   `tidb_ttl_job_history` : 過去 90 日間の TTL タスクの実行履歴

## 暴走クエリに関連するシステムテーブル {#system-tables-related-to-runaway-queries}

-   `tidb_runaway_queries` : 過去 7 日間に検出されたすべての暴走クエリの履歴記録
-   `tidb_runaway_watch` : 暴走クエリの監視リスト
-   `tidb_runaway_watch_done` : 削除または期限切れの暴走クエリの監視リスト

## メタデータロックに関連するシステムテーブル {#system-tables-related-to-metadata-locks}

-   [`tidb_mdl_view`](/mysql-schema/mysql-schema-tidb-mdl-view.md) : メタデータ ロックのビュー。これを使用して、現在ブロックされている DDL ステートメントに関する情報を表示できます。[メタデータロック](/metadata-lock.md)も参照してください。
-   `tidb_mdl_info` : TiDB が内部的に使用して、ノード間でメタデータ ロックを同期します。

## DDLステートメントに関連するシステムテーブル {#system-tables-related-to-ddl-statements}

-   `tidb_ddl_history` : DDLステートメントの履歴レコード
-   `tidb_ddl_job` : TiDBによって現在実行されているDDLステートメントのメタデータ
-   `tidb_ddl_reorg` : TiDBによって現在実行されている物理DDLステートメント（インデックスの追加など）のメタデータ

## TiDB分散実行フレームワーク（DXF）に関連するシステムテーブル {#system-tables-related-to-tidb-distributed-execution-framework-dxf}

-   `dist_framework_meta` : 分散実行フレームワーク (DXF) タスクスケジューラのメタデータ
-   `tidb_global_task` : 現在の DXF タスクのメタデータ
-   `tidb_global_task_history` : 成功したタスクと失敗したタスクの両方を含む、過去の DXF タスクのメタデータ
-   `tidb_background_subtask` : 現在の DXF サブタスクのメタデータ
-   `tidb_background_subtask_history` : 過去の DXF サブタスクのメタデータ

## リソース制御に関連するシステムテーブル {#system-tables-related-to-resource-control}

-   `request_unit_by_group` : すべてのリソースグループの消費リソースユニット (RU) の履歴記録

## バックアップと復元に関連するシステムテーブル {#system-tables-related-to-backup-and-restore}

-   `tidb_pitr_id_map` : ポイントインタイムリカバリ(PITR) 操作の ID マッピング情報

## その他のシステムテーブル {#miscellaneous-system-tables}

<CustomContent platform="tidb">

> **注記：**
>
> `tidb` 、 `expr_pushdown_blacklist` 、 `opt_rule_blacklist` 、 `table_cache_meta` 、 `tidb_import_jobs` 、および`tidb_timers`システムテーブルは、TiDB Self-Managedにのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

-   `GLOBAL_VARIABLES` : グローバルシステム変数テーブル
-   `expr_pushdown_blacklist` : 式プッシュダウンのブロックリスト
-   `opt_rule_blacklist` : 論理最適化ルールのブロックリスト
-   `tidb_import_jobs` : [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)のジョブ情報
-   `tidb_timers` : 内部タイマーのメタデータ
-   `advisory_locks` : [ロック関数](/functions-and-operators/locking-functions.md)に関する情報

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `GLOBAL_VARIABLES` : グローバルシステム変数テーブル

</CustomContent>
