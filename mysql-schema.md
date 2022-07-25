---
title: mysql Schema
summary: Learn about the TiDB system tables.
---

# <code>mysql</code>スキーマ {#code-mysql-code-schema}

`mysql`スキーマには、TiDBシステムテーブルが含まれています。設計はMySQLの`mysql`スキーマに似ており、 `mysql.user`などのテーブルを直接編集できます。また、MySQLの拡張機能であるいくつかのテーブルも含まれています。

## システムテーブルを付与する {#grant-system-tables}

これらのシステムテーブルには、ユーザーアカウントとその特権に関する付与情報が含まれています。

-   `user` ：ユーザーアカウント、グローバル特権、およびその他の非特権列
-   `db` ：データベースレベルの権限
-   `tables_priv` ：テーブルレベルの権限
-   `columns_priv` ：列レベルの特権

## サーバー側のヘルプシステムテーブル {#server-side-help-system-tables}

現在、 `help_topic`はNULLです。

## 統計システムテーブル {#statistics-system-tables}

-   `stats_buckets` ：統計のバケット
-   `stats_histograms` ：統計のヒストグラム
-   `stats_meta` ：行の総数や更新された行など、テーブルのメタ情報
-   `analyze_jobs` ：過去7日以内に進行中の統計収集タスクと履歴タスクレコード

## GCワーカーシステムテーブル {#gc-worker-system-tables}

-   `gc_delete_range` ：削除するデータを記録します

## その他のシステムテーブル {#miscellaneous-system-tables}

-   `GLOBAL_VARIABLES` ：グローバルシステム変数テーブル

<CustomContent platform="tidb">

-   `tidb` ：TiDB実行時のバージョン情報を記録します`bootstrap`

</CustomContent>
