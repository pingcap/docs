---
title: トラブルシューティング
summary: このページでは、TiDB Cloud Lake における一般的な問題のトラブルシューティング方法について説明します。
---

# トラブルシューティング

`system_history` テーブルを使用して、低速クエリ、エラー、リソース使用量、ログインの問題を診断できます。演算子ごとの実行分析（CPU time、I/O、spill、出力行数）には `profile_history` を使用します。すべてのテーブルはテナントごとに分離されています。

## テーブル {#tables}

### system_history.query_history {#system-history-query-history}

完全な SQL 実行監査証跡です。すべてのクエリについて、開始/終了ステータスを持つエントリが生成されます。

| フィールド | 型 | 説明 |
|-------|------|-------------|
| log_type | TINYINT | クエリのステータス: 1=Start, 2=Finish, 3=Error, 4=Aborted, 5=Closed |
| log_type_name | VARCHAR | 文字列名: "Start", "Finish", "Error", "Aborted", "Closed" |
| handler_type | VARCHAR | 使用されたプロトコル（例: `HTTPQuery`, `MySQL`） |
| tenant_id | VARCHAR | テナント識別子 |
| cluster_id | VARCHAR | クラスター識別子 |
| node_id | VARCHAR | ノード識別子 |
| sql_user | VARCHAR | クエリを実行したユーザー |
| sql_user_quota | VARCHAR | ユーザークォータ情報 |
| sql_user_privileges | VARCHAR | ユーザー権限 |
| query_id | VARCHAR | 一意のクエリ識別子 |
| query_kind | VARCHAR | クエリ種別（例: `Query`, `Insert`, `CopyIntoTable`） |
| query_text | VARCHAR | クエリの SQL テキスト |
| query_hash | VARCHAR | クエリテキストのハッシュ |
| query_parameterized_hash | VARCHAR | リテラル値を無視したハッシュ |
| event_date | DATE | イベントの日付 |
| event_time | TIMESTAMP | イベントのタイムスタンプ |
| query_start_time | TIMESTAMP | クエリ開始タイムスタンプ |
| query_duration_ms | BIGINT | 合計所要時間（ms、キュー待機 + 実行） |
| query_queued_duration_ms | BIGINT | キューで待機した時間（ms） |
| current_database | VARCHAR | 使用中のデータベース |
| written_rows | BIGINT UNSIGNED | 書き込まれた行数 |
| written_bytes | BIGINT UNSIGNED | 書き込まれたバイト数 |
| join_spilled_rows | BIGINT UNSIGNED | テーブル結合中に spill した行数 |
| join_spilled_bytes | BIGINT UNSIGNED | テーブル結合中に spill したバイト数 |
| agg_spilled_rows | BIGINT UNSIGNED | 集計中に spill した行数 |
| agg_spilled_bytes | BIGINT UNSIGNED | 集計中に spill したバイト数 |
| group_by_spilled_rows | BIGINT UNSIGNED | group by 中に spill した行数 |
| group_by_spilled_bytes | BIGINT UNSIGNED | group by 中に spill したバイト数 |
| written_io_bytes | BIGINT UNSIGNED | IO に書き込まれたバイト数 |
| written_io_bytes_cost_ms | BIGINT UNSIGNED | IO 書き込みコスト（ms） |
| scan_rows | BIGINT UNSIGNED | スキャンされた行数 |
| scan_bytes | BIGINT UNSIGNED | スキャンされたバイト数 |
| scan_io_bytes | BIGINT UNSIGNED | スキャン中に読み取られた IO バイト数 |
| scan_io_bytes_cost_ms | BIGINT UNSIGNED | IO スキャンコスト（ms） |
| scan_partitions | BIGINT UNSIGNED | スキャンされたパーティション数 |
| total_partitions | BIGINT UNSIGNED | 関与したパーティション総数 |
| result_rows | BIGINT UNSIGNED | 結果の行数 |
| result_bytes | BIGINT UNSIGNED | 結果のバイト数 |
| bytes_from_remote_disk | BIGINT UNSIGNED | リモートディスクから読み取られたバイト数 |
| bytes_from_local_disk | BIGINT UNSIGNED | ローカルディスクから読み取られたバイト数 |
| bytes_from_memory | BIGINT UNSIGNED | メモリから読み取られたバイト数 |
| client_address | VARCHAR | クライアントアドレス |
| user_agent | VARCHAR | クライアントのユーザーエージェント |
| exception_code | INT | 例外コード（0 = 成功） |
| exception_text | VARCHAR | 例外メッセージ |
| server_version | VARCHAR | サーバーバージョン |
| query_tag | VARCHAR | クエリタグ |
| has_profile | BOOLEAN | クエリに実行プロファイルがあるかどうか |
| peek_memory_usage | VARIANT | ピークメモリ使用量（JSON） |
| session_id | VARCHAR | セッション識別子 |
| session_settings | VARCHAR | セッション設定 |

### system_history.profile_history {#system-history-profile-history}

すべてのクエリに対する詳細な実行プロファイルです。演算子ごとの統計情報を抽出するには `jq()` を使用します。

| フィールド | 型 | 説明 |
|-------|------|-------------|
| timestamp | TIMESTAMP | プロファイルが記録された時刻 |
| query_id | VARCHAR | クエリ ID |
| profiles | VARIANT | 演算子の JSON 配列。各要素は `id`, `name`, `statistics[]` を含みます |
| statistics_desc | VARIANT | 統計情報の形式を記述する JSON |

統計配列のインデックス: `[0]`=OutputRows, `[1]`=OutputBytes, `[2]`=InputRows, `[3]`=InputBytes, `[4]`=CpuTime(ns)。

### system_history.log_history {#system-history-log-history}

すべての {{{ .lake }}} ノードおよびコンポーネントからの生ログエントリです。

| フィールド | 型 | 説明 |
|-------|------|-------------|
| timestamp | TIMESTAMP | ログエントリのタイムスタンプ |
| path | VARCHAR | ソースファイルパスと行番号 |
| target | VARCHAR | 対象モジュールまたはコンポーネント |
| log_level | VARCHAR | ログレベル（`INFO`, `ERROR`, `WARN` など） |
| cluster_id | VARCHAR | クラスター識別子 |
| node_id | VARCHAR | ノード識別子 |
| warehouse_id | VARCHAR | Warehouse 識別子 |
| query_id | VARCHAR | 関連するクエリ ID |
| message | VARCHAR | ログメッセージ（プレーンテキスト） |
| fields | VARIANT | 追加フィールド（JSON） |
| batch_number | BIGINT | 内部使用 |

### system_history.access_history {#system-history-access-history}

データリネージおよびアクセス制御の監査です。アクセスまたは変更されたすべてのオブジェクトを追跡します。

| フィールド | 型 | 説明 |
|-------|------|-------------|
| query_id | VARCHAR | クエリ ID |
| query_start | TIMESTAMP | クエリ開始時刻 |
| user_name | VARCHAR | クエリを実行したユーザー |
| base_objects_accessed | VARIANT | アクセスされたオブジェクト（JSON 配列） |
| direct_objects_accessed | VARIANT | 将来の使用のために予約済み |
| objects_modified | VARIANT | DML によって変更されたオブジェクト（JSON 配列） |
| object_modified_by_ddl | VARIANT | DDL によって変更されたオブジェクト（JSON 配列） |

JSON オブジェクトのフィールド: `object_domain` (Database/Table/Stage), `object_name`, `columns[]`, `stage_type`, `operation_type` (Create/Alter/Drop/Undrop), `properties`。

### system_history.login_history {#system-history-login-history}

すべてのログイン試行に対する認証監査証跡です。

| フィールド | 型 | 説明 |
|-------|------|-------------|
| event_time | TIMESTAMP | ログインイベントのタイムスタンプ |
| handler | VARCHAR | プロトコル（例: `HTTP`, `MySQL`） |
| event_type | VARCHAR | `LoginSuccess` または `LoginFailed` |
| connection_uri | VARCHAR | 接続 URI |
| auth_type | VARCHAR | 認証方式（例: Password） |
| user_name | VARCHAR | ログインを試行したユーザー |
| client_ip | VARCHAR | クライアント IP アドレス |
| user_agent | VARCHAR | クライアントのユーザーエージェント |
| session_id | VARCHAR | セッション ID |
| node_id | VARCHAR | ノード ID |
| error_message | VARCHAR | 失敗した場合のエラーメッセージ |

## クイック例 {#quick-examples}

直近 1 時間の低速クエリ（>5s）を見つけます。

```sql
SELECT query_id, sql_user, query_duration_ms, query_text
FROM system_history.query_history
WHERE query_duration_ms > 5000
  AND event_time > now() - INTERVAL 1 HOUR
  AND log_type = 2
ORDER BY query_duration_ms DESC
LIMIT 20;
```

失敗したクエリを見つけます。

```sql
SELECT query_id, sql_user, exception_code, exception_text, query_text
FROM system_history.query_history
WHERE exception_code != 0
  AND event_time > now() - INTERVAL 1 HOUR
ORDER BY event_time DESC;
```

ログイン失敗を確認します。

```sql
SELECT event_time, user_name, client_ip, error_message
FROM system_history.login_history
WHERE event_type = 'LoginFailed'
  AND event_time > now() - INTERVAL 24 HOUR
ORDER BY event_time DESC;
```