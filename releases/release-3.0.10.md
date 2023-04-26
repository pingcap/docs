---
title: TiDB 3.0.10 Release Notes
---

# TiDB 3.0.10 リリースノート {#tidb-3-0-10-release-notes}

発売日：2020年2月20日

TiDB バージョン: 3.0.10

TiDB アンシブル バージョン: 3.0.10

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## TiDB {#tidb}

-   `IndexLookUpJoin` `OtherCondition`を使用して`InnerRange` [#14599](https://github.com/pingcap/tidb/pull/14599)を構成するときの誤った`Join`結果を修正します
-   `tidb_pprof_sql_cpu`構成アイテムを削除し、 `tidb_pprof_sql_cpu`変数[#14416](https://github.com/pingcap/tidb/pull/14416)を追加します
-   ユーザーがグローバル権限を持っている場合にのみすべてのデータベースを照会できるという問題を修正します[#14386](https://github.com/pingcap/tidb/pull/14386)
-   `PointGet`操作[#14480](https://github.com/pingcap/tidb/pull/14480)の実行時にトランザクション タイムアウトが発生するため、データの可視性が期待どおりにならない問題を修正します。
-   悲観的トランザクションのアクティブ化のタイミングを遅延アクティブ化に変更し、楽観的トランザクション モード[#14474](https://github.com/pingcap/tidb/pull/14474)と一致させます。
-   `unixtimestamp`式がテーブル パーティションのタイム ゾーンを計算するときの間違ったタイム ゾーンの結果を修正します[#14476](https://github.com/pingcap/tidb/pull/14476)
-   デッドロック検出期間を監視する監視項目を`tidb_session_statement_deadlock_detect_duration_seconds`追加[#14484](https://github.com/pingcap/tidb/pull/14484)
-   GC ワーカー[#14439](https://github.com/pingcap/tidb/pull/14439)の論理エラーによって引き起こされるシステムpanicの問題を修正します。
-   `IsTrue`関数の式名を修正[#14516](https://github.com/pingcap/tidb/pull/14516)
-   一部のメモリ使用量が正しくカウントされない問題を修正[#14533](https://github.com/pingcap/tidb/pull/14533)
-   CM-Sketch 統計の初期化中に誤った処理ロジックが原因で発生したシステムpanicの問題を修正します[#14470](https://github.com/pingcap/tidb/pull/14470)
-   パーティション化されたテーブルをクエリするときの不正確なパーティション プルーニングの問題を修正します[#14546](https://github.com/pingcap/tidb/pull/14546)
-   SQL バインディングの SQL ステートメントの既定のデータベース名が正しく設定されていない問題を修正します[#14548](https://github.com/pingcap/tidb/pull/14548)
-   `json_key`が MySQL [#14561](https://github.com/pingcap/tidb/pull/14561)と互換性がない問題を修正
-   分割されたテーブルの統計を自動的に更新する機能を追加します[#14566](https://github.com/pingcap/tidb/pull/14566)
-   `PointGet`操作を実行するとプランIDが変わる問題を修正（プランIDは常に`1`であると予想されます） [#14595](https://github.com/pingcap/tidb/pull/14595)
-   SQL バインディングが[#14263](https://github.com/pingcap/tidb/pull/14263)に一致しない場合に不適切な処理ロジックによって引き起こされるシステムpanicの問題を修正します。
-   悲観的トランザクションのロック失敗後のリトライ回数を監視する監視項目`tidb_session_statement_pessimistic_retry_count`を追加[#14619](https://github.com/pingcap/tidb/pull/14619)
-   `show binding`ステートメント[#14618](https://github.com/pingcap/tidb/pull/14618)の誤った特権チェックを修正します
-   `backoff`ロジックに`killed`タグ[#14614](https://github.com/pingcap/tidb/pull/14614)のチェックが含まれていないため、クエリを強制終了できない問題を修正します。
-   内部ロックを保持する時間を短縮することにより、ステートメントの要約のパフォーマンスを向上させます[#14627](https://github.com/pingcap/tidb/pull/14627)
-   TiDB の文字列の解析結果が MySQL [#14570](https://github.com/pingcap/tidb/pull/14570)と互換性がない問題を修正
-   ユーザーのログイン失敗を監査ログに記録する[#14620](https://github.com/pingcap/tidb/pull/14620)
-   悲観的トランザクションのロックキー数を監視する監視項目を`tidb_session_ statement_lock_keys_count`つ追加[#14634](https://github.com/pingcap/tidb/pull/14634)
-   `&` 、 `<` 、 `>`などの JSON の文字が誤ってエスケープされる問題を修正します[#14637](https://github.com/pingcap/tidb/pull/14637)
-   `HashJoin`オペレーションがハッシュ テーブルを構築しているときに過剰なメモリ使用量が原因で発生するシステムpanicの問題を修正します[#14642](https://github.com/pingcap/tidb/pull/14642)
-   SQL バインドが不正なレコードを処理するときに、不適切な処理ロジックによって引き起こされるpanicの問題を修正します[#14645](https://github.com/pingcap/tidb/pull/14645)
-   ix 10 進数の除算に切り捨てられたエラー検出を追加することによる MySQL の非互換性の問題[#14673](https://github.com/pingcap/tidb/pull/14673)
-   存在しないテーブルに対する権限をユーザーに正常に付与する問題を修正します[#14611](https://github.com/pingcap/tidb/pull/14611)

## TiKV {#tikv}

-   Raftstore
    -   リージョンの失敗によるシステム パニックの問題 #6460 またはデータ損失の問題 #598 を修正します[#6481](https://github.com/tikv/tikv/pull/6481)
    -   スケジューリングの公平性を最適化するためのサポート`yield` 、およびリーダーのスケジューリングの安定性を向上させるためのリーダーの事前転送のサポート[#6563](https://github.com/tikv/tikv/pull/6563)

## PD {#pd}

-   システム トラフィックが変化したときのリージョンキャッシュ情報の自動更新をサポートすることで、無効なキャッシュの問題を修正します[#2103](https://github.com/pingcap/pd/pull/2103)
-   リーダーのリース時間を使用して TSO サービスの有効性を判断する[#2117](https://github.com/pingcap/pd/pull/2117)

## ツール {#tools}

-   TiDBBinlog
    -   Drainer [#893](https://github.com/pingcap/tidb-binlog/pull/893)でリレーログをサポート
-   TiDB Lightning
    -   構成ファイルが見つからない場合に、一部の構成項目がデフォルト値を使用するようにする[#255](https://github.com/pingcap/tidb-lightning/pull/255)
    -   非サーバー モード[#259](https://github.com/pingcap/tidb-lightning/pull/259)で Web インターフェイスを開くことができない問題を修正します。

## TiDB アンシブル {#tidb-ansible}

-   一部のシナリオで PD リーダーの取得に失敗し、コマンドの実行に失敗する問題を修正[#1121](https://github.com/pingcap/tidb-ansible/pull/1121)
-   TiDB ダッシュボードに`Deadlock Detect Duration`監視項目を追加する[#1127](https://github.com/pingcap/tidb-ansible/pull/1127)
-   TiDB ダッシュボードに`Statement Lock Keys Count`監視項目を追加する[#1132](https://github.com/pingcap/tidb-ansible/pull/1132)
-   TiDB ダッシュボードに`Statement Pessimistic Retry Count`監視項目を追加する[#1133](https://github.com/pingcap/tidb-ansible/pull/1133)
