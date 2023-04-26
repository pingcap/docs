---
title: mysql Schema
summary: Learn about the TiDB system tables.
---

# <code>mysql</code>スキーマ {#code-mysql-code-schema}

`mysql`スキーマには、TiDB システム テーブルが含まれています。設計は MySQL の`mysql`スキーマに似ており、 `mysql.user`などのテーブルを直接編集できます。また、MySQL の拡張機能である多数のテーブルも含まれています。

## システム テーブルの付与 {#grant-system-tables}

これらのシステム テーブルには、ユーザー アカウントとその権限に関する付与情報が含まれています。

-   `user` : ユーザー アカウント、グローバル権限、およびその他の権限以外の列
-   `db` : データベース レベルの権限
-   `tables_priv` : テーブルレベルの権限
-   `columns_priv` : 列レベルの権限
-   `password_history` : パスワード変更履歴
-   `default_roles` : ユーザーのデフォルトのロール
-   `global_grants` : 動的権限
-   `global_priv` : 証明書に基づく認証情報
-   `role_edges` : ロール間の関係

## サーバー側のヘルプ システム テーブル {#server-side-help-system-tables}

現在、 `help_topic`は NULL です。

## 統計システム テーブル {#statistics-system-tables}

-   `stats_buckets` : 統計のバケット
-   `stats_histograms` : 統計のヒストグラム
-   `stats_top_n` : 統計の上位 N
-   `stats_meta` : 行の総数や更新された行など、テーブルのメタ情報
-   `stats_extended` : 列間の順序相関などの拡張統計
-   `stats_feedback` : 統計のクエリ フィードバック
-   `stats_fm_sketch` : 統計列のヒストグラムの FMSketch 分布
-   `analyze_options` : 各テーブルのデフォルトの`analyze`オプション
-   `column_stats_usage` : 列統計の使用
-   `schema_index_usage` : インデックスの使用
-   `analyze_jobs` : 進行中の統計収集タスクと過去 7 日間の履歴タスク レコード

## 実行計画関連のシステム テーブル {#execution-plan-related-system-tables}

-   `bind_info` : 実行計画のバインディング情報
-   `capture_plan_baselines_blacklist` : 実行計画の自動バインディングのブロックリスト

## GC ワーカー システム テーブル {#gc-worker-system-tables}

-   `gc_delete_range` : 削除する KV 範囲
-   `gc_delete_range_done` : 削除された KV 範囲

## キャッシュされたテーブルに関連するシステム テーブル {#system-tables-related-to-cached-tables}

-   `table_cache_meta`キャッシュされたテーブルのメタデータを格納します。

## その他のシステム テーブル {#miscellaneous-system-tables}

-   `GLOBAL_VARIABLES` : グローバル システム変数テーブル

<CustomContent platform="tidb">

-   `tidb` : TiDB 実行時のバージョン情報を記録する`bootstrap`
-   `expr_pushdown_blacklist` : 式プッシュダウンのブロックリスト
-   `opt_rule_blacklist` : 論理最適化ルールのブロックリスト
-   `table_cache_meta` : キャッシュされたテーブルのメタデータ

</CustomContent>
