---
title: システムテーブル
summary: "{{{ .lake }}} は、{{{ .lake }}} のデプロイ、データベース、テーブル、クエリ、およびシステムパフォーマンスに関するメタデータを含む一連のシステムテーブルを提供します。これらのテーブルは読み取り専用であり、システムによって自動的に更新されます。"
---

# システムテーブル

{{{ .lake }}} は、{{{ .lake }}} のデプロイ、データベース、テーブル、クエリ、およびシステムパフォーマンスに関するメタデータを含む一連のシステムテーブルを提供します。これらのテーブルは読み取り専用であり、システムによって自動的に更新されます。

システムテーブルは `system` スキーマに整理されており、標準 SQL を使用してクエリできます。これらのテーブルは、{{{ .lake }}} 環境の監視、トラブルシューティング、および理解に役立つ重要な情報を提供します。

## 利用可能なシステムテーブル {#available-system-tables}

### データベースとテーブルのメタデータ {#database-table-metadata}

| テーブル                                                             | 説明                                                                                       |
|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [system.tables](/tidb-cloud-lake/sql/system-tables.md)                                 | プロパティ、作成時刻、サイズなどを含む、すべてのテーブルのメタデータ情報を提供します。 |
| [system.tables_with_history](/tidb-cloud-lake/sql/system-tables-with-history.md)       | 削除されたテーブルを含む、テーブルの履歴メタデータ情報を提供します。                    |
| [system.databases](/tidb-cloud-lake/sql/system-databases.md)                           | システム内のすべてのデータベースに関する情報を含みます。                                           |
| [system.views](/tidb-cloud-lake/sql/system-views.md)                                   | システム内のすべてのビューに関する情報を含みます。                                               |
| [system.databases_with_history](/tidb-cloud-lake/sql/system-databases-with-history.md) | 削除されたデータベースを含む、データベースの履歴情報を含みます。                     |
| [system.columns](/tidb-cloud-lake/sql/system-columns.md)                               | すべてのテーブルのカラムに関する情報を提供します。                                                 |
| [system.indexes](/tidb-cloud-lake/sql/system-indexes.md)                               | テーブルインデックスに関する情報を含みます。                                                         |
| [system.virtual_columns](/tidb-cloud-lake/sql/system-virtual-columns.md)               | システムで利用可能な仮想カラムを一覧表示します。                                                    |

### クエリとパフォーマンス {#query-performance}

| テーブル | 説明 |
|-------|-------------|
| [system.query_log](/tidb-cloud-lake/sql/system-query-log.md) | パフォーマンスメトリクスを含む、実行されたクエリに関する情報を含みます。 |
| [system.metrics](/tidb-cloud-lake/sql/system-metrics.md) | システムメトリクスイベントに関する情報を含みます。 |
| [system.query_cache](/tidb-cloud-lake/sql/system-query-cache.md) | クエリキャッシュに関する情報を提供します。 |
| [system.locks](/tidb-cloud-lake/sql/system-locks.md) | システム内で取得されたロックに関する情報を含みます。 |

### 関数と設定 {#functions-settings}

| テーブル | 説明 |
|-------|-------------|
| [system.functions](/tidb-cloud-lake/sql/system-functions.md) | 利用可能なすべての組み込み関数を一覧表示します。 |
| [system.table_functions](/tidb-cloud-lake/sql/system-table-functions.md) | 利用可能なすべてのテーブル関数を一覧表示します。 |
| [system.user_functions](/tidb-cloud-lake/sql/system-user-functions.md) | ユーザー定義関数に関する情報を含みます。 |
| [system.settings](/tidb-cloud-lake/sql/system-settings.md) | システム設定に関する情報を含みます。 |

### システム情報 {#system-information}

| テーブル | 説明 |
|-------|-------------|
| [system.build_options](/tidb-cloud-lake/sql/system-build-options.md) | {{{ .lake }}} のコンパイルに使用されたビルドオプションに関する情報を含みます。 |
| [system.clusters](/tidb-cloud-lake/sql/system-clusters.md) | システム内のクラスターに関する情報を含みます。 |
| [system.contributors](/tidb-cloud-lake/sql/system-contributors.md) | {{{ .lake }}} プロジェクトへの貢献者を一覧表示します。 |
| [system.credits](/tidb-cloud-lake/sql/system-credits.md) | {{{ .lake }}} で使用されているサードパーティライブラリに関する情報を含みます。 |
| [system.caches](/tidb-cloud-lake/sql/system-caches.md) | システムキャッシュに関する情報を提供します。 |

### ユーティリティテーブル {#utility-tables}

| テーブル | 説明 |
|-------|-------------|
| [system.numbers](/tidb-cloud-lake/sql/system-numbers.md) | 0 から始まる整数を含む単一カラムのテーブルで、テストデータの生成に役立ちます。 |
| [system.streams](/tidb-cloud-lake/sql/system-streams.md) | システム内のストリームに関する情報を含みます。 |
| [system.temp_tables](/tidb-cloud-lake/sql/system-temporary-tables.md) | 一時テーブルに関する情報を含みます。 |
| [system.temp_files](/tidb-cloud-lake/sql/system-temp-files.md) | 一時ファイルに関する情報を含みます。 |