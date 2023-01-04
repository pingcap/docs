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

## サーバー側のヘルプ システム テーブル {#server-side-help-system-tables}

現在、 `help_topic`は NULL です。

## 統計システム テーブル {#statistics-system-tables}

-   `stats_buckets` : 統計のバケット
-   `stats_histograms` : 統計のヒストグラム
-   `stats_meta` : 行の総数や更新された行など、テーブルのメタ情報
-   `analyze_jobs` : 進行中の統計収集タスクと過去 7 日間の履歴タスク レコード

## GC ワーカー システム テーブル {#gc-worker-system-tables}

-   `gc_delete_range` : 削除するデータを記録する

## キャッシュされたテーブルに関連するシステム テーブル {#system-tables-related-to-cached-tables}

-   `table_cache_meta`は、キャッシュされたテーブルのメタデータを格納します。

## その他のシステム テーブル {#miscellaneous-system-tables}

-   `GLOBAL_VARIABLES` : グローバル システム変数テーブル

<CustomContent platform="tidb">

-   `tidb` : TiDB 実行時のバージョン情報を記録する`bootstrap`

</CustomContent>
