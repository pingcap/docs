---
title: mysql Schema
summary: TiDBのmysqlスキーマには、ユーザーアカウントと権限に関する情報を含むシステムテーブルが含まれています。また、クラスタステータス、サーバー側のヘルプ、統計、実行計画、GCワーカー、キャッシュされたテーブル、TTL関連、暴走クエリ、メタデータロック、DDLステートメント、TiDB Distributed eXecution Framework (DXF)、リソース制御に関連するシステムテーブルがあります。また、その他のシステムテーブルも含まれています。
---

# <code>mysql</code>スキーマ {#code-mysql-code-schema}

`mysql`スキーマには TiDB システム テーブルが含まれています。この設計は MySQL の`mysql`スキーマに似ており、 `mysql.user`などのテーブルを直接編集できます。また、MySQL の拡張機能である多数のテーブルも含まれています。

## 付与システムテーブル {#grant-system-tables}

これらのシステム テーブルには、ユーザー アカウントとその権限に関する付与情報が含まれています。

-   `user` : ユーザー アカウント、グローバル権限、およびその他の非権限列
-   `db` : データベースレベルの権限
-   `tables_priv` : テーブルレベルの権限
-   `columns_priv` : 列レベルの権限
-   `password_history` : パスワード変更履歴
-   `default_roles` : ユーザーのデフォルトの役割
-   `global_grants` : 動的権限
-   `global_priv` : 証明書に基づく認証情報
-   `role_edges` : 役割間の関係

## クラスタステータスシステムテーブル {#cluster-status-system-tables}

-   `tidb`表には、TiDB に関するいくつかのグローバル情報が含まれています。

    -   `bootstrapped` : TiDB クラスターが初期化されているかどうか。この値は読み取り専用であり、変更できないことに注意してください。
    -   `tidb_server_version` : TiDB 初期化時のバージョン情報。この値は読み取り専用であり、変更できないことに注意してください。
    -   `system_tz` : TiDB のシステム タイム ゾーン。
    -   `new_collation_enabled` : TiDB が[照合順序の新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)有効にしているかどうか。この値は読み取り専用であり、変更できないことに注意してください。

## サーバー側のヘルプ システム テーブル {#server-side-help-system-tables}

現在、 `help_topic`は NULL です。

## 統計システムテーブル {#statistics-system-tables}

-   `stats_buckets` : 統計のバケット
-   `stats_histograms` : 統計のヒストグラム
-   `stats_top_n` : 統計のトップN
-   `stats_meta` : テーブルのメタ情報 (総行数や更新された行など)
-   `stats_extended` : 拡張統計 (列間の順序相関など)
-   `stats_feedback` : 統計のクエリフィードバック
-   `stats_fm_sketch` : 統計列のヒストグラムの FMSketch 分布
-   `analyze_options` : 各テーブルのデフォルトの`analyze`オプション
-   `column_stats_usage` : 列統計の使用法
-   `schema_index_usage` : インデックスの使用
-   `analyze_jobs` : 進行中の統計収集タスクと過去 7 日間の履歴タスク レコード

## 実行計画関連のシステムテーブル {#execution-plan-related-system-tables}

-   `bind_info` : 実行計画のバインディング情報
-   `capture_plan_baselines_blacklist` : 実行計画の自動バインドのブロックリスト

## GC ワーカー システム テーブル {#gc-worker-system-tables}

> **注記：**
>
> GC ワーカー システム テーブルは、TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

-   `gc_delete_range` : 削除するKV範囲
-   `gc_delete_range_done` : 削除された KV 範囲

## キャッシュされたテーブルに関連するシステム テーブル {#system-tables-related-to-cached-tables}

-   `table_cache_meta`キャッシュされたテーブルのメタデータを保存します。

## TTL関連のシステムテーブル {#ttl-related-system-tables}

> **注記：**

> TTL 関連のシステム テーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

-   `tidb_ttl_table_status` : すべての TTL テーブルに対して以前に実行された TTL ジョブと進行中の TTL ジョブ
-   `tidb_ttl_task` : 現在進行中の TTL サブタスク
-   `tidb_ttl_job_history` : 過去 90 日間の TTL タスクの実行履歴

## 暴走クエリに関連するシステム テーブル {#system-tables-related-to-runaway-queries}

-   `tidb_runaway_queries` : 過去 7 日間に特定されたすべての暴走クエリの履歴レコード
-   `tidb_runaway_watch` : 暴走クエリの監視リスト
-   `tidb_runaway_watch_done` : 削除または期限切れの暴走クエリの監視リスト

## メタデータ ロックに関連するシステム テーブル {#system-tables-related-to-metadata-locks}

-   `tidb_mdl_view` : メタデータ ロックのビュー。これを使用して、現在ブロックされている DDL ステートメントに関する情報を表示できます。
-   `tidb_mdl_info` : ノード間でメタデータ ロックを同期するために TiDB によって内部的に使用されます。

## DDL ステートメントに関連するシステム テーブル {#system-tables-related-to-ddl-statements}

-   `tidb_ddl_history` : DDL ステートメントの履歴レコード
-   `tidb_ddl_jobs` : TiDB によって現在実行されている DDL ステートメントのメタデータ
-   `tidb_ddl_reorg` : TiDB によって現在実行されている物理 DDL ステートメント (インデックスの追加など) のメタデータ

## TiDB Distributed eXecution Framework (DXF) に関連するシステム テーブル {#system-tables-related-to-tidb-distributed-execution-framework-dxf}

-   `dist_framework_meta` : Distributed eXecution Framework (DXF) タスク スケジューラのメタデータ
-   `tidb_global_task` : 現在の DXF タスクのメタデータ
-   `tidb_global_task_history` : 成功したタスクと失敗したタスクの両方を含む、履歴 DXF タスクのメタデータ
-   `tidb_background_subtask` : 現在の DXF サブタスクのメタデータ
-   `tidb_background_subtask_history` : 過去の DXF サブタスクのメタデータ

## リソース制御に関連するシステムテーブル {#system-tables-related-to-resource-control}

-   `request_unit_by_group` : すべてのリソース グループの消費されたリソース ユニット (RU) の履歴レコード

## その他のシステムテーブル {#miscellaneous-system-tables}

<CustomContent platform="tidb">

> **注記：**
>
> `tidb` 、 `expr_pushdown_blacklist` 、 `opt_rule_blacklist` 、 `table_cache_meta` 、 `tidb_import_jobs` 、および`tidb_timers`システム テーブルは TiDB セルフホストにのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

-   `GLOBAL_VARIABLES` : グローバル システム変数テーブル
-   `expr_pushdown_blacklist` : 式プッシュダウンのブロックリスト
-   `opt_rule_blacklist` : 論理最適化ルールのブロックリスト
-   `tidb_import_jobs` : [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)のジョブ情報
-   `tidb_timers` : 内部タイマーのメタデータ

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `GLOBAL_VARIABLES` : グローバル システム変数テーブル

</CustomContent>
