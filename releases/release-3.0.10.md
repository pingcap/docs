---
title: TiDB 3.0.10 Release Notes
summary: TiDB 3.0.10は2020年2月20日にリリースされました。TiDB、TiKV、PD、TiDB Ansibleの様々なバグ修正と改善が含まれています。主な修正としては、Join結果の誤り、データ可視性の問題、システムpanicの問題などが挙げられます。また、TiDB Ansibleではダッシュボードに新しい監視項目が追加されました。このリリースには既知の問題があるため、リリースノートでは最新の3.0.xバージョンの使用を推奨しています。
---

# TiDB 3.0.10 リリースノート {#tidb-3-0-10-release-notes}

発売日：2020年2月20日

TiDBバージョン: 3.0.10

TiDB Ansible バージョン: 3.0.10

> **警告：**
>
> このバージョンにはいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の3.0.xバージョンをご利用いただくことをお勧めします。

## TiDB {#tidb}

-   `IndexLookUpJoin` `OtherCondition`を使用して`InnerRange` を構築したときに間違った`Join`結果を修正します [＃14599](https://github.com/pingcap/tidb/pull/14599)
-   `tidb_pprof_sql_cpu`設定項目を削除し、 `tidb_pprof_sql_cpu`変数を追加します。 [＃14416](https://github.com/pingcap/tidb/pull/14416)
-   ユーザーがグローバル権限を持っている場合にのみすべてのデータベースをクエリできる問題を修正[＃14386](https://github.com/pingcap/tidb/pull/14386)
-   `PointGet`操作を実行するときにトランザクション タイムアウトによりデータの可視性が期待どおりに機能しない問題を修正しました [＃14480](https://github.com/pingcap/tidb/pull/14480)
-   楽観的トランザクションモードと一致するように、悲観的トランザクションのアクティブ化のタイミングを遅延アクティブ化に変更します。 [＃14474](https://github.com/pingcap/tidb/pull/14474)
-   `unixtimestamp`式がテーブルパーティションのタイムゾーンを計算するときに誤ったタイムゾーン結果が返される問題を修正しました。 [＃14476](https://github.com/pingcap/tidb/pull/14476)
-   デッドロック検出期間を監視するための監視項目を`tidb_session_statement_deadlock_detect_duration_seconds`追加します[＃14484](https://github.com/pingcap/tidb/pull/14484)
-   GCワーカーのいくつかのロジックエラーによって引き起こされるシステムpanicの問題を修正しました [＃14439](https://github.com/pingcap/tidb/pull/14439)
-   `IsTrue`関数の式名を修正します [＃14516](https://github.com/pingcap/tidb/pull/14516)
-   一部のメモリ使用量が不正確にカウントされる問題を修正[＃14533](https://github.com/pingcap/tidb/pull/14533)
-   CM-Sketch統計初期化中の誤った処理ロジックによって引き起こされるシステムpanicの問題を修正[＃14470](https://github.com/pingcap/tidb/pull/14470)
-   パーティションテーブルをクエリする際の不正確なパーティションプルーニングの問題を修正[＃14546](https://github.com/pingcap/tidb/pull/14546)
-   SQLバインディング内のSQL文のデフォルトのデータベース名が正しく設定されていない問題を修正しました[＃14548](https://github.com/pingcap/tidb/pull/14548)
-   `json_key` MySQL と互換性がない問題を修正 [＃14561](https://github.com/pingcap/tidb/pull/14561)
-   パーティションテーブルの統計情報を自動更新する機能を追加[＃14566](https://github.com/pingcap/tidb/pull/14566)
-   `PointGet`操作が実行されるとプラン ID が変わる問題を修正 (プラン ID は常に`1`になることが期待されます) [＃14595](https://github.com/pingcap/tidb/pull/14595)
-   SQLバインディングが正確に一致しない場合に誤った処理ロジックによって発生するシステムpanicの問題を修正しました[＃14263](https://github.com/pingcap/tidb/pull/14263)
-   悲観的トランザクションロック失敗後の再試行回数を監視するための監視項目`tidb_session_statement_pessimistic_retry_count`を追加します。 [＃14619](https://github.com/pingcap/tidb/pull/14619)
-   `show binding`文の不正な権限チェックを修正 [＃14618](https://github.com/pingcap/tidb/pull/14618)
-   `backoff`ロジックに`killed`タグのチェックが含まれていないため、クエリを強制終了できない問題を修正しました。 [＃14614](https://github.com/pingcap/tidb/pull/14614)
-   内部ロックの保持時間を短縮することで、ステートメントサマリーのパフォーマンスを向上します[＃14627](https://github.com/pingcap/tidb/pull/14627)
-   TiDBの文字列を時間に変換する結果がMySQL と互換性がない問題を修正 [＃14570](https://github.com/pingcap/tidb/pull/14570)
-   監査ログにユーザーのログイン失敗を記録する [＃14620](https://github.com/pingcap/tidb/pull/14620)
-   悲観的トランザクションのロックキーの数を監視するための`tidb_session_ statement_lock_keys_count`監視項目を追加します。 [＃14634](https://github.com/pingcap/tidb/pull/14634)
-   JSON内の`&`、`<`、`>`などの文字が誤ってエスケープされる問題を修正しました [＃14637](https://github.com/pingcap/tidb/pull/14637)
-   `HashJoin`操作でハッシュテーブルを構築する際に過剰なメモリ使用によって発生するシステムpanicの問題を修正しました [＃14642](https://github.com/pingcap/tidb/pull/14642)
-   SQLバインディングが無効なレコードを処理するときに、誤った処理ロジックによって発生するpanicの問題を修正しました[＃14645](https://github.com/pingcap/tidb/pull/14645)
-   ix MySQLの非互換性の問題を修正するために、小数点割り算の計算に切り捨てエラー検出を追加しました[＃14673](https://github.com/pingcap/tidb/pull/14673)
-   存在しないテーブルに対する権限をユーザーに付与してしまう問題を修正[＃14611](https://github.com/pingcap/tidb/pull/14611)

## TiKV {#tikv}

-   Raftstore
    -   リージョンマージの失敗によって発生するシステムpanicの問題＃6460またはデータ損失の問題＃598を修正しました [＃6481](https://github.com/tikv/tikv/pull/6481)
    -   スケジューリングの公平性を最適化するためのサポート`yield`と、リーダーのスケジューリングの安定性を向上させるためのリーダーの事前転送のサポート[＃6563](https://github.com/tikv/tikv/pull/6563)

## PD {#pd}

-   システムトラフィックの変化に応じてリージョンキャッシュ情報を自動的に更新できるようにすることで、無効なキャッシュの問題を修正しました[＃2103](https://github.com/pingcap/pd/pull/2103)
-   リーダーリース時間を使用してTSOサービスの有効性を決定する[＃2117](https://github.com/pingcap/pd/pull/2117)

## ツール {#tools}

-   TiDB Binlog
    -   Drainerのサポートリレーログ [＃893](https://github.com/pingcap/tidb-binlog/pull/893)
-   TiDB Lightning
    -   設定ファイルが見つからない場合に、一部の設定項目でデフォルト値を使用するようにする[＃255](https://github.com/pingcap/tidb-lightning/pull/255)
    -   非サーバーモードでWebインターフェースを開けない問題を修正[＃259](https://github.com/pingcap/tidb-lightning/pull/259)

## TiDB Ansible {#tidb-ansible}

-   一部のシナリオでPDリーダーの取得に失敗したためにコマンド実行が失敗する問題を修正[＃1121](https://github.com/pingcap/tidb-ansible/pull/1121)
-   TiDB Dashboardに`Deadlock Detect Duration`監視項目を追加する [＃1127](https://github.com/pingcap/tidb-ansible/pull/1127)
-   TiDB Dashboardに`Statement Lock Keys Count`監視項目を追加する [＃1132](https://github.com/pingcap/tidb-ansible/pull/1132)
-   TiDB Dashboardに`Statement Pessimistic Retry Count`監視項目を追加する [＃1133](https://github.com/pingcap/tidb-ansible/pull/1133)
