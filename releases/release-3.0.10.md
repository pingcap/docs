---
title: TiDB 3.0.10 Release Notes
---

# TiDB 3.0.10 リリースノート {#tidb-3-0-10-release-notes}

発売日：2020年2月20日

TiDB バージョン: 3.0.10

TiDB Ansible バージョン: 3.0.10

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかり、これらの問題は新しいバージョンで修正されています。最新の 3.0.x バージョンを使用することをお勧めします。

## TiDB {#tidb}

-   `IndexLookUpJoin` `OtherCondition`を使用して`InnerRange` [<a href="https://github.com/pingcap/tidb/pull/14599">#14599</a>](https://github.com/pingcap/tidb/pull/14599)を構築したときの間違った`Join`結果を修正
-   `tidb_pprof_sql_cpu`設定項目を削除し、 `tidb_pprof_sql_cpu`変数[<a href="https://github.com/pingcap/tidb/pull/14416">#14416</a>](https://github.com/pingcap/tidb/pull/14416)を追加します
-   ユーザーがグローバル権限[<a href="https://github.com/pingcap/tidb/pull/14386">#14386</a>](https://github.com/pingcap/tidb/pull/14386)を持っている場合にのみすべてのデータベースをクエリできるという問題を修正します。
-   `PointGet`オペレーション[<a href="https://github.com/pingcap/tidb/pull/14480">#14480</a>](https://github.com/pingcap/tidb/pull/14480)の実行時にトランザクション タイムアウトが発生し、データの可視性が期待どおりにならない問題を修正
-   悲観的トランザクション モード[<a href="https://github.com/pingcap/tidb/pull/14474">#14474</a>](https://github.com/pingcap/tidb/pull/14474)と一致して、楽観的トランザクションのアクティブ化のタイミングを遅延アクティブ化に変更します。
-   `unixtimestamp`式がテーブル パーティション[<a href="https://github.com/pingcap/tidb/pull/14476">#14476</a>](https://github.com/pingcap/tidb/pull/14476)のタイム ゾーンを計算するときの誤ったタイム ゾーン結果を修正します。
-   デッドロック検出期間[<a href="https://github.com/pingcap/tidb/pull/14484">#14484</a>](https://github.com/pingcap/tidb/pull/14484)を監視する監視項目`tidb_session_statement_deadlock_detect_duration_seconds`を追加
-   GC ワーカー[<a href="https://github.com/pingcap/tidb/pull/14439">#14439</a>](https://github.com/pingcap/tidb/pull/14439)の一部のロジック エラーによって引き起こされるシステムpanicの問題を修正します。
-   `IsTrue`関数[<a href="https://github.com/pingcap/tidb/pull/14516">#14516</a>](https://github.com/pingcap/tidb/pull/14516)の式名を修正します。
-   一部のメモリ使用量が不正確にカウントされる問題を修正[<a href="https://github.com/pingcap/tidb/pull/14533">#14533</a>](https://github.com/pingcap/tidb/pull/14533)
-   CM-Sketch 統計の初期化中に不適切な処理ロジックが原因で発生するシステムpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/14470">#14470</a>](https://github.com/pingcap/tidb/pull/14470)
-   パーティション テーブルのクエリを実行するときに不正確なパーティション プルーニングの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/14546">#14546</a>](https://github.com/pingcap/tidb/pull/14546)
-   SQL バインディング内の SQL ステートメントのデフォルトのデータベース名が正しく設定されない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/14548">#14548</a>](https://github.com/pingcap/tidb/pull/14548)
-   `json_key`がMySQL [<a href="https://github.com/pingcap/tidb/pull/14561">#14561</a>](https://github.com/pingcap/tidb/pull/14561)と互換性がない問題を修正
-   パーティションテーブルの統計を自動更新する機能を追加[<a href="https://github.com/pingcap/tidb/pull/14566">#14566</a>](https://github.com/pingcap/tidb/pull/14566)
-   `PointGet`操作を実行するとプラン ID が変更される問題を修正 (プラン ID は常に`1`であることが期待されます) [<a href="https://github.com/pingcap/tidb/pull/14595">#14595</a>](https://github.com/pingcap/tidb/pull/14595)
-   SQL バインディングが正確に一致しない場合に不正な処理ロジックが原因で発生するシステムpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/14263">#14263</a>](https://github.com/pingcap/tidb/pull/14263)
-   悲観的トランザクションロック失敗後のリトライ回数を監視する監視項目`tidb_session_statement_pessimistic_retry_count`を追加[<a href="https://github.com/pingcap/tidb/pull/14619">#14619</a>](https://github.com/pingcap/tidb/pull/14619)
-   `show binding`ステートメントの誤った権限チェックを修正[<a href="https://github.com/pingcap/tidb/pull/14618">#14618</a>](https://github.com/pingcap/tidb/pull/14618)
-   `backoff`ロジックに`killed`タグのチェックが含まれていないため、クエリを強制終了できない問題を修正します。 [<a href="https://github.com/pingcap/tidb/pull/14614">#14614</a>](https://github.com/pingcap/tidb/pull/14614)
-   内部ロックを保持する時間を短縮することで、ステートメント サマリーのパフォーマンスを向上させます[<a href="https://github.com/pingcap/tidb/pull/14627">#14627</a>](https://github.com/pingcap/tidb/pull/14627)
-   TiDB の文字列解析結果が MySQL [<a href="https://github.com/pingcap/tidb/pull/14570">#14570</a>](https://github.com/pingcap/tidb/pull/14570)と互換性がない問題を修正
-   ユーザーのログイン失敗を監査ログに記録します[<a href="https://github.com/pingcap/tidb/pull/14620">#14620</a>](https://github.com/pingcap/tidb/pull/14620)
-   悲観的トランザクションのロックキー数を監視する監視項目`tidb_session_ statement_lock_keys_count`を追加[<a href="https://github.com/pingcap/tidb/pull/14634">#14634</a>](https://github.com/pingcap/tidb/pull/14634)
-   JSON 内の`&` 、 `<` 、 `>`などの文字が誤ってエスケープされる問題を修正[<a href="https://github.com/pingcap/tidb/pull/14637">#14637</a>](https://github.com/pingcap/tidb/pull/14637)
-   `HashJoin`オペレーションがハッシュ テーブル[<a href="https://github.com/pingcap/tidb/pull/14642">#14642</a>](https://github.com/pingcap/tidb/pull/14642)を構築しているときに過剰なメモリ使用量が原因で発生するシステムpanicの問題を修正します。
-   SQL バインディングが不正なレコードを処理するときに、不正な処理ロジックによって引き起こされるpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/14645">#14645</a>](https://github.com/pingcap/tidb/pull/14645)
-   小数点以下の除算計算[<a href="https://github.com/pingcap/tidb/pull/14673">#14673</a>](https://github.com/pingcap/tidb/pull/14673)に切り捨てエラー検出を追加することで、MySQL の非互換性の問題を解決しました。
-   存在しないテーブルに対するユーザー権限が正常に付与される問題を修正します[<a href="https://github.com/pingcap/tidb/pull/14611">#14611</a>](https://github.com/pingcap/tidb/pull/14611)

## TiKV {#tikv}

-   Raftstore
    -   リージョンリージョンの失敗によるシステム パニックの問題 #6460 またはデータ損失の問題 #598 を修正します[<a href="https://github.com/tikv/tikv/pull/6481">#6481</a>](https://github.com/tikv/tikv/pull/6481)
    -   スケジューリングの公平性を最適化するためのサポート`yield` 、およびリーダーのスケジューリングの安定性を向上させるためのリーダーの事前転送のサポート[<a href="https://github.com/tikv/tikv/pull/6563">#6563</a>](https://github.com/tikv/tikv/pull/6563)

## PD {#pd}

-   システム トラフィックが変化したときのリージョンキャッシュ情報の自動更新をサポートすることで、無効なキャッシュの問題を修正しました[<a href="https://github.com/pingcap/pd/pull/2103">#2103</a>](https://github.com/pingcap/pd/pull/2103)
-   リーダーのリース時間を使用して TSO サービスの有効性を判断します[<a href="https://github.com/pingcap/pd/pull/2117">#2117</a>](https://github.com/pingcap/pd/pull/2117)

## ツール {#tools}

-   TiDBBinlog
    -   Drainer[<a href="https://github.com/pingcap/tidb-binlog/pull/893">#893</a>](https://github.com/pingcap/tidb-binlog/pull/893)のサポートリレーログ
-   TiDB Lightning
    -   構成ファイルが見つからない場合に一部の構成項目にデフォルト値を使用させる[<a href="https://github.com/pingcap/tidb-lightning/pull/255">#255</a>](https://github.com/pingcap/tidb-lightning/pull/255)
    -   非サーバーモード[<a href="https://github.com/pingcap/tidb-lightning/pull/259">#259</a>](https://github.com/pingcap/tidb-lightning/pull/259)でWebインターフェースを開けない問題を修正

## TiDB Ansible {#tidb-ansible}

-   一部のシナリオでPDリーダーの取得に失敗し、コマンドの実行が失敗する問題を修正[<a href="https://github.com/pingcap/tidb-ansible/pull/1121">#1121</a>](https://github.com/pingcap/tidb-ansible/pull/1121)
-   TiDB ダッシュボードに`Deadlock Detect Duration`監視項目を追加します[<a href="https://github.com/pingcap/tidb-ansible/pull/1127">#1127</a>](https://github.com/pingcap/tidb-ansible/pull/1127)
-   TiDB ダッシュボードに`Statement Lock Keys Count`監視項目を追加します[<a href="https://github.com/pingcap/tidb-ansible/pull/1132">#1132</a>](https://github.com/pingcap/tidb-ansible/pull/1132)
-   TiDB ダッシュボードに`Statement Pessimistic Retry Count`監視項目を追加します[<a href="https://github.com/pingcap/tidb-ansible/pull/1133">#1133</a>](https://github.com/pingcap/tidb-ansible/pull/1133)
