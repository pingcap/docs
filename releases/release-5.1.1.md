---
title: TiDB 5.1.1 Release Notes
---

# TiDB 5.1.1 リリースノート {#tidb-5-1-1-release-notes}

リリース日：2021年7月30日

TiDB バージョン: 5.1.1

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   TiDB クラスターを v4.0 から v5.1 にアップグレードする場合、デフォルト値の`tidb_multi_statement_mode`は`OFF`です。代わりに、クライアント ライブラリのマルチステートメント機能を使用することをお勧めします。詳細は[`tidb_multi_statement_mode`に関するドキュメント](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)を参照してください。 [#25751](https://github.com/pingcap/tidb/pull/25751)
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から`3000` [#25874](https://github.com/pingcap/tidb/pull/25874)に変更します。
    -   `table_storage_stats`表[#26352](https://github.com/pingcap/tidb/pull/26352)にアクセスするには`SUPER`特権が必要です
    -   `information_schema.user_privileges`テーブルにアクセスして他のユーザーの権限を表示するには、 `mysql.user`に対する`SELECT`権限が必要です[#26311](https://github.com/pingcap/tidb/pull/26311)
    -   `information_schema.cluster_hardware`表[#26297](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`CONFIG`特権が必要です
    -   `information_schema.cluster_info`表[#26297](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`PROCESS`特権が必要です
    -   `information_schema.cluster_load`表[#26297](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`PROCESS`特権が必要です
    -   `information_schema.cluster_systeminfo`表[#26297](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`PROCESS`特権が必要です
    -   `information_schema.cluster_log`表[#26297](https://github.com/pingcap/tidb/pull/26297)にアクセスするには`PROCESS`特権が必要です
    -   `information_schema.cluster_config`表[#26150](https://github.com/pingcap/tidb/pull/26150)にアクセスするには`CONFIG`特権が必要です

## 機能強化 {#feature-enhancements}

-   TiDB ダッシュボード

    -   OIDC SSO をサポートします。 OIDC 互換の SSO サービス (Okta や Auth0 など) を設定することで、ユーザーは SQL パスワードを入力せずに TiDB ダッシュボードにログインできます。 [#3883](https://github.com/tikv/pd/pull/3883)

-   TiFlash

    -   DAG リクエストで`HAVING()`機能をサポート

## 改良点 {#improvements}

-   TiDB

    -   ステイル読み取り機能の一般提供 (GA) を発表
    -   データ挿入を高速化するために`paramMarker`割り当てを避ける[#26076](https://github.com/pingcap/tidb/pull/26076)
    -   安定した結果モードをサポートして、クエリ結果をより安定させます[#25995](https://github.com/pingcap/tidb/pull/25995)
    -   組み込み関数`json_unquote()`を TiKV [#26265](https://github.com/pingcap/tidb/pull/26265)にプッシュ ダウンするサポート
    -   MPP クエリの再試行をサポート[#26480](https://github.com/pingcap/tidb/pull/26480)
    -   `UPDATE`回の読み取り[#26225](https://github.com/pingcap/tidb/pull/26225)に対して`point get`または`batch point get`を使用して、インデックス キーの`LOCK`レコードを`PUT`レコードに変更します。
    -   古いクエリからのビューの作成を禁止する[#26200](https://github.com/pingcap/tidb/pull/26200)
    -   `COUNT(DISTINCT)` MPPモードの集計機能を徹底的に押し下げる[#26194](https://github.com/pingcap/tidb/pull/26194)
    -   MPP クエリを起動する前に、 TiFlashの可用性を確認してください[#26192](https://github.com/pingcap/tidb/pull/26192)
    -   読み取りタイムスタンプを将来の時刻に設定することを許可しない[#25763](https://github.com/pingcap/tidb/pull/25763)
    -   集計関数を`EXPLAIN`ステートメントでプッシュダウンできない場合にログ警告を出力する[#25737](https://github.com/pingcap/tidb/pull/25737)
    -   `statements_summary_evicted`テーブルを追加して、クラスターの削除されたカウント情報を記録します[#25587](https://github.com/pingcap/tidb/pull/25587)
    -   フォーマット指定子の組み込み関数`str_to_date`の MySQL 互換性を向上させる`%b/%M/%r/%T` [#25768](https://github.com/pingcap/tidb/pull/25768)

-   TiKV

    -   事前書き込み要求を可能な限り冪等にして、未確定エラーの可能性を減らします[#10586](https://github.com/tikv/tikv/pull/10586)
    -   期限切れのコマンドを多数処理する際のスタック オーバーフローのリスクを回避する[#10502](https://github.com/tikv/tikv/pull/10502)
    -   ステイル読み取りリクエストの`start_ts`から update `max_ts` [#10451](https://github.com/tikv/tikv/pull/10451)を使用しないことで、過剰な commit リクエストの再試行を回避します。
    -   読み取りレイテンシーを短縮するために、読み取り準備完了と書き込み準備完了を別々に処理する[#10592](https://github.com/tikv/tikv/pull/10592)
    -   I/O レート制限が有効になっている場合のデータ インポート速度への影響を軽減します[#10390](https://github.com/tikv/tikv/pull/10390)
    -   Raft gRPC 接続間の負荷バランスを改善する[#10495](https://github.com/tikv/tikv/pull/10495)

-   ツール

    -   TiCDC

        -   削除`file sorter` [#2327](https://github.com/pingcap/tiflow/pull/2327)
        -   PD エンドポイントで証明書が見つからない場合に返されるエラー メッセージを改善します[#1973](https://github.com/pingcap/tiflow/issues/1973)

    -   TiDB Lightning

        -   スキーマを復元するための再試行メカニズムを追加する[#1294](https://github.com/pingcap/br/pull/1294)

    -   Dumpling

        -   アップストリームが TiDB v3.x クラスターである場合は、常に`_tidb_rowid`使用してテーブルを分割します。これにより、TiDB のメモリ使用量を削減できます[#295](https://github.com/pingcap/dumpling/issues/295)
        -   Dumpling のパフォーマンスと安定性を向上させるために、データベースのメタデータにアクセスする頻度を減らします[#315](https://github.com/pingcap/dumpling/pull/315)

## バグの修正 {#bug-fixes}

-   TiDB

    -   列タイプを`tidb_enable_amend_pessimistic_txn=on` [#26203](https://github.com/pingcap/tidb/issues/26203)に変更したときに発生する可能性があるデータ損失の問題を修正します。
    -   `last_day`関数の動作が SQL モード[#26001](https://github.com/pingcap/tidb/pull/26001)で互換性がない問題を修正
    -   `LIMIT`ウィンドウ関数の上にあるときに発生する可能性があるpanicの問題を修正します[#25344](https://github.com/pingcap/tidb/issues/25344)
    -   悲観的トランザクションをコミットすると書き込み競合が発生する可能性がある問題を修正します[#25964](https://github.com/pingcap/tidb/issues/25964)
    -   相関サブクエリのインデックス結合の結果が間違っている問題を修正[#25799](https://github.com/pingcap/tidb/issues/25799)
    -   正常にコミットされた楽観的トランザクションがコミット エラーを報告する可能性があるバグを修正します[#10468](https://github.com/tikv/tikv/issues/10468)
    -   `SET`型の列[#25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると、誤った結果が返される問題を修正します。
    -   悲観的トランザクションのインデックス キーが繰り返しコミットされる可能性があるバグを修正します[#26359](https://github.com/pingcap/tidb/issues/26359)
    -   オプティマイザがパーティションを検索するときの整数オーバーフローのリスクを修正します[#26227](https://github.com/pingcap/tidb/issues/26227)
    -   タイムスタンプ[#26292](https://github.com/pingcap/tidb/issues/26292)に`DATE`をキャストすると、無効な値が書き込まれる可能性がある問題を修正します。
    -   コプロセッサー Cache メトリックが Grafana [#26338](https://github.com/pingcap/tidb/issues/26338)で表示されない問題を修正します。
    -   テレメトリによって発生する迷惑なログの問題を修正する[#25760](https://github.com/pingcap/tidb/issues/25760) [#25785](https://github.com/pingcap/tidb/issues/25785)
    -   プレフィックス インデックス[#26029](https://github.com/pingcap/tidb/issues/26029)のクエリ範囲のバグを修正
    -   同じパーティションを同時に切り捨てると DDL の実行がハングする問題を修正します[#26229](https://github.com/pingcap/tidb/issues/26229)
    -   重複の問題を修正`ENUM`アイテム[#25955](https://github.com/pingcap/tidb/issues/25955)
    -   CTE イテレータが正しく閉じられないバグを修正[#26112](https://github.com/pingcap/tidb/issues/26112)
    -   `LOAD DATA`ステートメントが utf8 以外のデータを異常にインポートする可能性がある問題を修正します[#25979](https://github.com/pingcap/tidb/issues/25979)
    -   符号なし整数列でウィンドウ関数を使用するときに発生する可能性があるpanicの問題を修正します[#25956](https://github.com/pingcap/tidb/issues/25956)
    -   非同期コミット ロックを解決するときに TiDB がpanicになる可能性がある問題を修正します[#25778](https://github.com/pingcap/tidb/issues/25778)
    -   ステイル読み取り が`PREPARE`ステートメントと完全に互換性がないという問題を修正します[#25800](https://github.com/pingcap/tidb/pull/25800)
    -   ODBC スタイルの定数 (たとえば、 `{d '2020-01-01'}` ) を式[#25531](https://github.com/pingcap/tidb/issues/25531)として使用できないという問題を修正します。
    -   TiDB単体で実行した際に発生するエラーを修正[#25555](https://github.com/pingcap/tidb/pull/25555)

-   TiKV

    -   特定のプラットフォームで継続時間の計算がpanicになる問題を修正[#10569](https://github.com/tikv/tikv/pull/10569)
    -   Load Base Split が`batch_get_command` [#10542](https://github.com/tikv/tikv/issues/10542)のエンコードされていないキーを誤って使用する問題を修正します。
    -   `resolved-ts.advance-ts-interval`構成を動的に変更してもすぐに有効にならないという問題を修正します[#10426](https://github.com/tikv/tikv/issues/10426)
    -   レプリカが[#10225](https://github.com/tikv/tikv/issues/10225)つを超えると、まれにフォロワーのメタデータが破損する問題を修正します。
    -   暗号化が有効になっている場合にスナップショットを 2 回作成すると発生するpanicの問題を修正します[#9786](https://github.com/tikv/tikv/issues/9786) [#10407](https://github.com/tikv/tikv/issues/10407)
    -   間違った`tikv_raftstore_hibernated_peer_state`メトリクスを修正する[#10330](https://github.com/tikv/tikv/issues/10330)
    -   コプロセッサ[#10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数タイプを修正します。
    -   悲観的トランザクションのインデックス キーが繰り返しコミットされる可能性があるバグを修正します[#10468](https://github.com/tikv/tikv/issues/10468#issuecomment-869491061)
    -   リーダーが転送された直後に`ReadIndex`リクエストが古い結果を返す問題を修正[#9351](https://github.com/tikv/tikv/issues/9351)

-   PD

    -   複数のスケジューラが同時に実行されているために競合が発生した場合に、期待されるスケジューリングが生成されない問題を修正します[#3807](https://github.com/tikv/pd/issues/3807) [#3778](https://github.com/tikv/pd/issues/3778)
    -   スケジューラーを削除しても再度スケジューラーが表示されることがある問題を修正[#2572](https://github.com/tikv/pd/issues/2572)

-   TiFlash

    -   テーブル スキャン タスクの実行時に発生する潜在的なpanicの問題を修正します。
    -   TiFlashが DAQ リクエストの処理時に`duplicated region`のエラーを発生させるバグを修正
    -   読み取り負荷が高い場合に発生するpanicの問題を修正
    -   `DateFormat`関数の実行時に発生する潜在的なpanicの問題を修正します。
    -   MPP タスクの実行時に発生する潜在的なメモリリークの問題を修正します。
    -   集計関数`COUNT`または`COUNT DISTINCT`を実行したときに予期しない結果が生じる問題を修正
    -   複数のディスクに展開されたときにTiFlash がデータを復元できないという潜在的なバグを修正します
    -   TiDB ダッシュボードでTiFlashのディスク情報が正しく表示されない問題を修正
    -   分解時に発生する潜在的なpanicの問題を修正します`SharedQueryBlockInputStream`
    -   分解時に発生する潜在的なpanicの問題を修正します`MPPTask`
    -   スナップショットを介してデータを同期した後にデータの不整合が発生する可能性がある問題を修正

-   ツール

    -   TiCDC

        -   新しい照合順序機能のサポートを修正します[#2301](https://github.com/pingcap/tiflow/issues/2301)
        -   実行時に共有マップへの非同期アクセスが原因でpanic[#2300](https://github.com/pingcap/tiflow/pull/2300)が発生する可能性がある問題を修正します。
        -   DDL ステートメントの実行中に所有者がクラッシュしたときに発生する潜在的な DDL 損失の問題を修正します[#2290](https://github.com/pingcap/tiflow/pull/2290)
        -   TiDB のロックを時期尚早に解決しようとする問題を修正します[#2188](https://github.com/pingcap/tiflow/issues/2188)
        -   テーブルの移行直後に TiCDC ノードが強制終了された場合にデータが失われる可能性があるバグを修正します[#2033](https://github.com/pingcap/tiflow/pull/2033)
        -   `changefeed update` on `--sort-dir`と`--start-ts` [#1921](https://github.com/pingcap/tiflow/pull/1921)の処理ロジックを修正

    -   バックアップと復元 (BR)

        -   復元するデータのサイズが正しく計算されない問題を修正します[#1270](https://github.com/pingcap/br/issues/1270)
        -   cdclog [#870](https://github.com/pingcap/br/issues/870)から復元するときに発生する DDL イベントの欠落の問題を修正します。

    -   TiDB Lightning

        -   TiDB が Parquet ファイルの`DECIMAL`型データの解析に失敗する問題を修正[#1275](https://github.com/pingcap/br/pull/1275)
        -   キー間隔を計算するときの整数オーバーフローの問題を修正します[#1291](https://github.com/pingcap/br/issues/1291) [#1290](https://github.com/pingcap/br/issues/1290)
