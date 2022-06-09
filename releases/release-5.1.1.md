---
title: TiDB 5.1.1 Release Notes
---

# TiDB5.1.1リリースノート {#tidb-5-1-1-release-notes}

発売日：2021年7月30日

TiDBバージョン：5.1.1

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   TiDBクラスターをv4.0からv5.1にアップグレードする場合、デフォルト値の`tidb_multi_statement_mode`は`OFF`です。代わりに、クライアントライブラリのマルチステートメント機能を使用することをお勧めします。詳細については、 [`tidb_multi_statement_mode`に関するドキュメント](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)を参照してください。 [＃25751](https://github.com/pingcap/tidb/pull/25751)
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から[＃25874](https://github.com/pingcap/tidb/pull/25874)に変更し`3000`
    -   `table_storage_stats`のテーブルにアクセスするには`SUPER`の特権が必要です[＃26352](https://github.com/pingcap/tidb/pull/26352)
    -   他のユーザーの特権を表示するために`information_schema.user_privileges`テーブルにアクセスするには、 `mysql.user`の`SELECT`特権が必要です[＃26311](https://github.com/pingcap/tidb/pull/26311)
    -   `information_schema.cluster_hardware`のテーブルにアクセスするには`CONFIG`の特権が必要です[＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_info`のテーブルにアクセスするには`PROCESS`の特権が必要です[＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_load`のテーブルにアクセスするには`PROCESS`の特権が必要です[＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_systeminfo`のテーブルにアクセスするには`PROCESS`の特権が必要です[＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_log`のテーブルにアクセスするには`PROCESS`の特権が必要です[＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_config`のテーブルにアクセスするには`CONFIG`の特権が必要です[＃26150](https://github.com/pingcap/tidb/pull/26150)

## 機能拡張 {#feature-enhancements}

-   TiDBダッシュボード

    -   OIDCSSOをサポートします。 OIDC互換のSSOサービス（OktaやAuth0など）を設定することにより、ユーザーはSQLパスワードを入力せずにTiDBダッシュボードにログインできます。 [＃3883](https://github.com/tikv/pd/pull/3883)

-   TiFlash

    -   DAGリクエストで`HAVING()`の機能をサポートする

## 改善 {#improvements}

-   TiDB

    -   Stale Read機能の一般提供（GA）を発表する
    -   データ挿入を高速化するために`paramMarker`の割り当てを避けてください[＃26076](https://github.com/pingcap/tidb/pull/26076)
    -   安定した結果モードをサポートして、クエリ結果をより安定させます[＃25995](https://github.com/pingcap/tidb/pull/25995)
    -   内蔵機能`json_unquote()`から[＃26265](https://github.com/pingcap/tidb/pull/26265)へのプッシュダウンをサポート
    -   MPPクエリの再試行のサポート[＃26480](https://github.com/pingcap/tidb/pull/26480)
    -   `UPDATE`の読み取りに`point get`または`batch point get`を使用して、インデックスキーの`LOCK`レコードを`PUT`レコードに変更します[＃26225](https://github.com/pingcap/tidb/pull/26225)
    -   古いクエリからのビューの作成を禁止する[＃26200](https://github.com/pingcap/tidb/pull/26200)
    -   MPPモード[＃26194](https://github.com/pingcap/tidb/pull/26194)で`COUNT(DISTINCT)`集約機能を徹底的に押し下げます。
    -   MPPクエリを起動する前にTiFlashの可用性を確認してください[＃26192](https://github.com/pingcap/tidb/pull/26192)
    -   読み取りタイムスタンプを将来の時刻に設定することを許可しない[＃25763](https://github.com/pingcap/tidb/pull/25763)
    -   `EXPLAIN`のステートメントで集計関数をプッシュダウンできない場合のログ警告の出力[＃25737](https://github.com/pingcap/tidb/pull/25737)
    -   `statements_summary_evicted`のテーブルを追加して、クラスタ[＃25587](https://github.com/pingcap/tidb/pull/25587)の削除されたカウント情報を記録します。
    -   フォーマット指定子[＃25768](https://github.com/pingcap/tidb/pull/25768)の組み込み関数`str_to_date`のMySQL互換性を改善し`%b/%M/%r/%T`

-   TiKV

    -   未確定のエラーの可能性を減らすために、事前書き込み要求を可能な限りべき等にします[＃10586](https://github.com/tikv/tikv/pull/10586)
    -   多くの期限切れのコマンドを処理するときにスタックオーバーフローのリスクを防ぐ[＃10502](https://github.com/tikv/tikv/pull/10502)
    -   [＃10451](https://github.com/tikv/tikv/pull/10451)リクエストの`start_ts`を使用して更新35を使用しないことにより、過度のコミットリクエストの再試行を回避し`max_ts` 。
    -   読み取りの待ち時間を短縮するために、読み取り準備と書き込み準備を別々に処理します[＃10592](https://github.com/tikv/tikv/pull/10592)
    -   I/Oレート制限が有効になっている場合のデータインポート速度への影響を減らす[＃10390](https://github.com/tikv/tikv/pull/10390)
    -   RaftgRPC接続間の負荷分散を改善する[＃10495](https://github.com/tikv/tikv/pull/10495)

-   ツール

    -   TiCDC

        -   [＃2327](https://github.com/pingcap/tiflow/pull/2327)を削除し`file sorter`
        -   PDエンドポイントが証明書を見逃したときに返されるエラーメッセージを改善する[＃1973](https://github.com/pingcap/tiflow/issues/1973)

    -   TiDB Lightning

        -   スキーマを復元するための再試行メカニズムを追加する[＃1294](https://github.com/pingcap/br/pull/1294)

    -   Dumpling

        -   アップストリームがTiDBv3.xクラスタの場合は、常に`_tidb_rowid`を使用してテーブルを分割します。これにより、TiDBのメモリ使用量を削減できます[＃295](https://github.com/pingcap/dumpling/issues/295)
        -   データベースメタデータにアクセスする頻度を減らして、Dumplingのパフォーマンスと安定性を向上させます[＃315](https://github.com/pingcap/dumpling/pull/315)

## バグの修正 {#bug-fixes}

-   TiDB

    -   列タイプを`tidb_enable_amend_pessimistic_txn=on`で変更するときに発生する可能性のあるデータ損失の問題を修正し[＃26203](https://github.com/pingcap/tidb/issues/26203)
    -   `last_day`関数の動作がSQLモード[＃26001](https://github.com/pingcap/tidb/pull/26001)で互換性がないという問題を修正します
    -   `LIMIT`がウィンドウ関数[＃25344](https://github.com/pingcap/tidb/issues/25344)の上にあるときに発生する可能性のあるパニックの問題を修正します
    -   悲観的なトランザクションをコミットすると書き込みの競合が発生する可能性があるという問題を修正します[＃25964](https://github.com/pingcap/tidb/issues/25964)
    -   相関サブクエリでのインデックス結合の結果が間違っている問題を修正します[＃25799](https://github.com/pingcap/tidb/issues/25799)
    -   正常にコミットされたオプティミスティックトランザクションがコミットエラーを報告する可能性があるバグを修正します[＃10468](https://github.com/tikv/tikv/issues/10468)
    -   `SET`型列[＃25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると誤った結果が返される問題を修正します。
    -   悲観的なトランザクションのインデックスキーが繰り返しコミットされる可能性があるバグを修正します[＃26359](https://github.com/pingcap/tidb/issues/26359)
    -   オプティマイザがパーティション[＃26227](https://github.com/pingcap/tidb/issues/26227)を見つけているときに整数オーバーフローのリスクを修正します
    -   `DATE`をタイムスタンプ[＃26292](https://github.com/pingcap/tidb/issues/26292)にキャストするときに無効な値が書き込まれる可能性がある問題を修正します
    -   コプロセッサーキャッシュメトリックがGrafana1に表示されない問題を修正し[＃26338](https://github.com/pingcap/tidb/issues/26338)
    -   [＃25785](https://github.com/pingcap/tidb/issues/25785)によって引き起こされる迷惑なログの問題を修正する[＃25760](https://github.com/pingcap/tidb/issues/25760)
    -   プレフィックスインデックス[＃26029](https://github.com/pingcap/tidb/issues/26029)のクエリ範囲のバグを修正
    -   同じパーティションを同時に切り捨てると、DDL実行がハングする問題を修正します[＃26229](https://github.com/pingcap/tidb/issues/26229)
    -   重複`ENUM`アイテムの問題を修正します[＃25955](https://github.com/pingcap/tidb/issues/25955)
    -   CTEイテレータが正しく閉じられないバグを修正します[＃26112](https://github.com/pingcap/tidb/issues/26112)
    -   `LOAD DATA`ステートメントがutf8以外のデータを異常にインポートする可能性がある問題を修正します[＃25979](https://github.com/pingcap/tidb/issues/25979)
    -   符号なし整数列でウィンドウ関数を使用するときに発生する可能性のあるパニックの問題を修正します[＃25956](https://github.com/pingcap/tidb/issues/25956)
    -   非同期コミットロックを解決するときにTiDBがパニックになる可能性がある問題を修正します[＃25778](https://github.com/pingcap/tidb/issues/25778)
    -   StaleReadが`PREPARE`ステートメントと完全に互換性がないという問題を修正します[＃25800](https://github.com/pingcap/tidb/pull/25800)
    -   ODBCスタイルの定数（たとえば、 `{d '2020-01-01'}` ）を式[＃25531](https://github.com/pingcap/tidb/issues/25531)として使用できない問題を修正します。
    -   TiDBを単独で実行しているときに発生するエラーを修正します[＃25555](https://github.com/pingcap/tidb/pull/25555)

-   TiKV

    -   特定のプラットフォームで期間の計算がパニックになる可能性がある問題を修正します[＃10569](https://github.com/tikv/tikv/pull/10569)
    -   LoadBaseSplitが`batch_get_command`のエンコードされていないキーを誤って使用する問題を修正し[＃10542](https://github.com/tikv/tikv/issues/10542)
    -   `resolved-ts.advance-ts-interval`構成をオンラインで変更してもすぐには有効にならないという問題を修正します[＃10426](https://github.com/tikv/tikv/issues/10426)
    -   4つを超えるレプリカがあるまれなケースでのフォロワーメタデータの破損の問題を修正します[＃10225](https://github.com/tikv/tikv/issues/10225)
    -   暗号化が有効になっている場合にスナップショットを2回作成するときに発生するパニックの問題を修正し[＃10407](https://github.com/tikv/tikv/issues/10407) [＃9786](https://github.com/tikv/tikv/issues/9786)
    -   間違った`tikv_raftstore_hibernated_peer_state`メトリック[＃10330](https://github.com/tikv/tikv/issues/10330)を修正
    -   コプロセッサー[＃10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数タイプを修正してください
    -   悲観的なトランザクションのインデックスキーが繰り返しコミットされる可能性があるバグを修正します[＃10468](https://github.com/tikv/tikv/issues/10468#issuecomment-869491061)
    -   リーダーが転送された直後に`ReadIndex`のリクエストが古い結果を返す問題を修正します[＃9351](https://github.com/tikv/tikv/issues/9351)

-   PD

    -   複数のスケジューラーが同時に実行されているために競合が発生した場合に、期待されるスケジューリングを生成できない問題を修正します[＃3807](https://github.com/tikv/pd/issues/3807) [＃3778](https://github.com/tikv/pd/issues/3778)
    -   スケジューラーが既に削除されている場合でも、スケジューラーが再び表示される可能性がある問題を修正します[＃2572](https://github.com/tikv/pd/issues/2572)

-   TiFlash

    -   テーブルスキャンタスクの実行時に発生する可能性のあるパニックの問題を修正します
    -   DAQリクエストを処理するときにTiFlashが約`duplicated region`のエラーを発生させるバグを修正します
    -   読み取り負荷が大きいときに発生するパニックの問題を修正します
    -   `DateFormat`関数の実行時に発生する可能性のあるパニックの問題を修正します
    -   MPPタスクの実行時に発生する可能性のあるメモリリークの問題を修正します
    -   集計関数`COUNT`または`COUNT DISTINCT`を実行するときに予期しない結果が発生する問題を修正します
    -   複数のディスクにデプロイしたときにTiFlashがデータを復元できない潜在的なバグを修正します
    -   TiDBダッシュボードがTiFlashのディスク情報を正しく表示できない問題を修正します
    -   `SharedQueryBlockInputStream`を解体するときに発生する可能性のあるパニックの問題を修正します
    -   `MPPTask`を解体するときに発生する可能性のあるパニックの問題を修正します
    -   スナップショットを介してデータを同期した後のデータの不整合の潜在的な問題を修正します

-   ツール

    -   TiCDC

        -   新しい照合順序機能のサポートを修正する[＃2301](https://github.com/pingcap/tiflow/issues/2301)
        -   実行時に共有マップへの非同期アクセスがパニックを引き起こす可能性がある問題を修正します[＃2300](https://github.com/pingcap/tiflow/pull/2300)
        -   DDLステートメントの実行中に所有者がクラッシュしたときに発生する可能性のあるDDL損失の問題を修正します[＃2290](https://github.com/pingcap/tiflow/pull/2290)
        -   TiDBのロックを時期尚早に解決しようとする問題を修正します[＃2188](https://github.com/pingcap/tiflow/issues/2188)
        -   テーブルの移行直後にTiCDCノードが強制終了された場合にデータが失われる可能性があるバグを修正します[＃2033](https://github.com/pingcap/tiflow/pull/2033)
        -   `changefeed update`および`--start-ts`の処理[＃1921](https://github.com/pingcap/tiflow/pull/1921)を修正し`--sort-dir` 。

    -   バックアップと復元（BR）

        -   復元するデータのサイズが正しく計算されない問題を修正します[＃1270](https://github.com/pingcap/br/issues/1270)
        -   cdclog1からの復元時に発生するDDLイベントの欠落の問題を修正し[＃870](https://github.com/pingcap/br/issues/870)

    -   TiDB Lightning

        -   TiDBがParquetファイル[＃1275](https://github.com/pingcap/br/pull/1275)の`DECIMAL`タイプのデータの解析に失敗する問題を修正します
        -   キー間隔を計算するときの整数オーバーフローの問題を修正し[＃1290](https://github.com/pingcap/br/issues/1290) [＃1291](https://github.com/pingcap/br/issues/1291)
