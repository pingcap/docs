---
title: system_history.query_history
summary: query_id を使用して特定のクエリの履歴を照会します。
---

# system_history.query_history

**完全な SQL 実行監査証跡** - {{{ .lake }}} で実行されたすべての SQL クエリの包括的な詳細を記録します。各クエリについて 2 つのエントリ（開始と終了）が生成され、次の内容を完全に可視化します。

- **パフォーマンス分析**: クエリ時間、リソース使用量、最適化の機会
- **セキュリティ監査**: 誰が、いつ、どこから、どのクエリを実行したか
- **コンプライアンス追跡**: 規制要件に対応する完全な監査証跡
- **使用状況の監視**: データベースアクティビティのパターンとユーザー行動の分析

## フィールド {#fields}

| フィールド                     | 型             | 説明                                                                                   |
|---------------------------|------------------|-----------------------------------------------------------------------------------------------|
| log_type                  | TINYINT          | クエリのステータス: 1=Start、2=Finish、3=Error、4=Aborted、5=Closed。                                     |
| log_type_name             | VARCHAR          | クエリステータスの文字列名: "Start"、"Finish"、"Error"、"Aborted"、または "Closed"。                                           |
| handler_type              | VARCHAR          | クエリに使用されたプロトコルまたはハンドラー（例: `HTTPQuery`、`MySQL`）。                                 |
| tenant_id                 | VARCHAR          | テナント識別子。                                                                        |
| cluster_id                | VARCHAR          | クラスター識別子。                                                                       |
| node_id                   | VARCHAR          | ノード識別子。                                             |
| sql_user                  | VARCHAR          | クエリを実行したユーザー。                                                              |
| sql_user_quota            | VARCHAR          | ユーザーのクォータ情報。                                                            |
| sql_user_privileges       | VARCHAR          | ユーザーの権限。                                                                   |
| query_id                  | VARCHAR          | クエリの一意識別子。                                                          |
| query_kind                | VARCHAR          | クエリの種類（例: `Query`、`Insert`、`CopyIntoTable` など）。                                                |
| query_text                | VARCHAR          | クエリの SQL テキスト。                                                               |
| query_hash                | VARCHAR          | クエリテキストのハッシュ値。                                                             |
| query_parameterized_hash  | VARCHAR          | 特定の値に関係なくクエリを表すハッシュ値。                                                    |
| event_date                | DATE             | イベントが発生した日付。                                                             |
| event_time                | TIMESTAMP        | イベントが発生したタイムスタンプ。                                                        |
| query_start_time          | TIMESTAMP        | クエリが開始されたタイムスタンプ。                                                         |
| query_duration_ms         | BIGINT           | クエリの合計時間（ミリ秒）。キュー待機時間と実行時間の両方を含みます。                                                    |
| query_queued_duration_ms  | BIGINT           | クエリがキュー内で待機した時間（ミリ秒）。                                        |
| current_database          | VARCHAR          | クエリ実行時に使用されていたデータベース。                                              |
| written_rows              | BIGINT UNSIGNED  | クエリによって書き込まれた行数。                                                      |
| written_bytes             | BIGINT UNSIGNED  | クエリによって書き込まれたバイト数。                                                     |
| join_spilled_rows         | BIGINT UNSIGNED  | join 操作中にスピルされた行数。                                            |
| join_spilled_bytes        | BIGINT UNSIGNED  | join 操作中にスピルされたバイト数。                                           |
| agg_spilled_rows          | BIGINT UNSIGNED  | 集計操作中にスピルされた行数。                                     |
| agg_spilled_bytes         | BIGINT UNSIGNED  | 集計操作中にスピルされたバイト数。                                    |
| group_by_spilled_rows     | BIGINT UNSIGNED  | group by 操作中にスピルされた行数。                                        |
| group_by_spilled_bytes    | BIGINT UNSIGNED  | group by 操作中にスピルされたバイト数。                                       |
| written_io_bytes          | BIGINT UNSIGNED  | IO に書き込まれたバイト数。                                                            |
| written_io_bytes_cost_ms  | BIGINT UNSIGNED  | 書き込みにかかった IO コスト（ミリ秒）。                                                      |
| scan_rows                 | BIGINT UNSIGNED  | クエリによってスキャンされた行数。                                                      |
| scan_bytes                | BIGINT UNSIGNED  | クエリによってスキャンされたバイト数。                                                     |
| scan_io_bytes             | BIGINT UNSIGNED  | スキャン中に読み取られた IO バイト数。                                                  |
| scan_io_bytes_cost_ms     | BIGINT UNSIGNED  | スキャンにかかった IO コスト（ミリ秒）。                                                     |
| scan_partitions           | BIGINT UNSIGNED  | スキャンされたパーティション数。                                                             |
| total_partitions          | BIGINT UNSIGNED  | 関与したパーティションの総数。                                                      |
| result_rows               | BIGINT UNSIGNED  | クエリ結果の行数。                                                       |
| result_bytes              | BIGINT UNSIGNED  | クエリ結果のバイト数。                                                      |
| bytes_from_remote_disk    | BIGINT UNSIGNED  | リモートディスクから読み取られたバイト数。                                                    |
| bytes_from_local_disk     | BIGINT UNSIGNED  | ローカルディスクから読み取られたバイト数。                                                     |
| bytes_from_memory         | BIGINT UNSIGNED  | メモリから読み取られたバイト数。                                                         |
| client_address            | VARCHAR          | クエリを発行したクライアントのアドレス。                                              |
| user_agent                | VARCHAR          | クライアントの user agent 文字列。                                                          |
| exception_code            | INT              | クエリが失敗した場合の例外コード。                                                       |
| exception_text            | VARCHAR          | クエリが失敗した場合の例外メッセージ。                                                    |
| server_version            | VARCHAR          | クエリを処理したサーバーのバージョン。                                           |
| query_tag                 | VARCHAR          | クエリに関連付けられたタグ。                                                            |
| has_profile               | BOOLEAN          | クエリに関連付けられた実行プロファイルがあるかどうか。                                        |
| peek_memory_usage         | VARIANT          | クエリ実行中のピークメモリ使用量（JSON オブジェクトとして）。                              |
| session_id                | VARCHAR          | クエリに関連付けられたセッション識別子。                                             |

## 例 {#examples}

`query_id` を使用して特定のクエリの履歴を照会します

```sql
SELECT * FROM system_history.query_history WHERE query_id = '4e1f50a9-bce2-45cc-86e4-c7a36b9b8d43';

*************************** 1. row ***************************
                log_type: 2
           log_type_name: Finish
            handler_type: HTTPQuery
               tenant_id: test_tenant
              cluster_id: test_cluster
                 node_id: jxSgvulZFAq1sDckR1bu85
                sql_user: root
          sql_user_quota: NULL
     sql_user_privileges: NULL
                query_id: 4e1f50a9-bce2-45cc-86e4-c7a36b9b8d43
              query_kind: Query
              query_text: SELECT * FROM t
              query_hash: cd36a2072e7f9deaa746db7480200944
query_parameterized_hash: cd36a2072e7f9deaa746db7480200944
              event_date: 2025-06-12
              event_time: 2025-06-12 03:31:35.135987
        query_start_time: 2025-06-12 03:31:35.041725
       query_duration_ms: 94
query_queued_duration_ms: 0
        current_database: default
            written_rows: 0
           written_bytes: 0
       join_spilled_rows: 0
      join_spilled_bytes: 0
        agg_spilled_rows: 0
       agg_spilled_bytes: 0
   group_by_spilled_rows: 0
  group_by_spilled_bytes: 0
        written_io_bytes: 0
written_io_bytes_cost_ms: 0
               scan_rows: 1
              scan_bytes: 20
           scan_io_bytes: 605
   scan_io_bytes_cost_ms: 0
         scan_partitions: 1
        total_partitions: 1
             result_rows: 1
            result_bytes: 20
  bytes_from_remote_disk: 74
   bytes_from_local_disk: 0
       bytes_from_memory: 0
          client_address: 127.0.0.1
              user_agent: lakesql/0.26.2-unknown
          exception_code: 0
          exception_text:
          server_version: v1.2.753-nightly-c3d5fabb79(rust-1.88.0-nightly-2025-06-12T01:48:36.733925000Z)
               query_tag:
             has_profile: NULL
       peek_memory_usage: {"jxSgvulZFAq1sDckR1bu85":223840}
              session_id: e3c54c32-f3c0-4ea9-bdd2-65701aa3f2a6
```