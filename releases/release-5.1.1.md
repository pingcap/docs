---
title: TiDB 5.1.1 Release Notes
summary: TiDB 5.1.1は2021年7月30日にリリースされました。このリリースには、互換性の変更、機能強化、改善、バグ修正、そしてTiDB Dashboard、 TiFlash、TiKV、そして各種ツールのアップデートが含まれています。主な変更点としては、変数のデフォルト値の変更、TiDB DashboardでのOIDC SSOのサポート、そしてデータ損失とpanicに関するバグ修正などが挙げられます。
---

# TiDB 5.1.1 リリースノート {#tidb-5-1-1-release-notes}

リリース日：2021年7月30日

TiDB バージョン: 5.1.1

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   TiDBクラスタをv4.0からv5.1にアップグレードする場合、デフォルト値は`tidb_multi_statement_mode`ではなく`OFF`です。代わりに、クライアントライブラリのマルチステートメント機能を使用することをお勧めします。詳細は[`tidb_multi_statement_mode`に関するドキュメント](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)参照してください[＃25751](https://github.com/pingcap/tidb/pull/25751)
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から`3000`に変更します[＃25874](https://github.com/pingcap/tidb/pull/25874)
    -   `table_storage_stats`テーブルアクセスするには`SUPER`権限が必要です [＃26352](https://github.com/pingcap/tidb/pull/26352)
    -   他のユーザーの権限表示するには、 `information_schema.user_privileges`テーブルにアクセスするために`mysql.user`の`SELECT`権限が必要です。 [＃26311](https://github.com/pingcap/tidb/pull/26311)
    -   `information_schema.cluster_hardware`テーブルアクセスするには`CONFIG`権限が必要です [＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_info`テーブルアクセスするには`PROCESS`権限が必要です [＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_load`テーブルアクセスするには`PROCESS`権限が必要です [＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_systeminfo`テーブルアクセスするには`PROCESS`権限が必要です [＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_log`テーブルアクセスするには`PROCESS`権限が必要です [＃26297](https://github.com/pingcap/tidb/pull/26297)
    -   `information_schema.cluster_config`テーブルアクセスするには`CONFIG`権限が必要です [＃26150](https://github.com/pingcap/tidb/pull/26150)

## 機能強化 {#feature-enhancements}

-   TiDB Dashboard

    -   OIDC SSOをサポートします。OIDC対応のSSOサービス（OktaやAuth0など）を設定することで、ユーザーはSQLパスワードを入力せずにTiDB Dashboardにログインできます[＃3883](https://github.com/tikv/pd/pull/3883)

-   TiFlash

    -   DAGリクエストの`HAVING()`機能をサポートする

## 改善点 {#improvements}

-   TiDB

    -   ステイル読み取り機能の一般提供 (GA) を発表
    -   データ挿入を高速化するために`paramMarker`割り当てを避ける[＃26076](https://github.com/pingcap/tidb/pull/26076)
    -   クエリ結果をより安定させるために、安定した結果モードをサポートします[＃25995](https://github.com/pingcap/tidb/pull/25995)
    -   組み込み関数`json_unquote()`をTiKV にプッシュダウンする機能をサポート [＃26265](https://github.com/pingcap/tidb/pull/26265)
    -   MPPクエリの再試行をサポート[＃26480](https://github.com/pingcap/tidb/pull/26480)
    -   `UPDATE`読み取りで`point get`または`batch point get`使用して、インデックスキーの`LOCK`レコードを`PUT`レコードに変更します[＃26225](https://github.com/pingcap/tidb/pull/26225)
    -   古いクエリからのビューの作成を禁止する[＃26200](https://github.com/pingcap/tidb/pull/26200)
    -   MPPモードで`COUNT(DISTINCT)`集約機能を徹底的にプッシュダウンする [＃26194](https://github.com/pingcap/tidb/pull/26194)
    -   MPPクエリを起動する前にTiFlashの可用性を確認してください [＃26192](https://github.com/pingcap/tidb/pull/26192)
    -   読み取りタイムスタンプを将来の時刻に設定することを許可しない[＃25763](https://github.com/pingcap/tidb/pull/25763)
    -   集計関数を`EXPLAIN`文にプッシュダウンできない場合にログ警告を出力する [＃25737](https://github.com/pingcap/tidb/pull/25737)
    -   クラスターの立ち退きカウント情報を記録するためのテーブル`statements_summary_evicted`を追加します。 [＃25587](https://github.com/pingcap/tidb/pull/25587)
    -   フォーマット指定子`%b/%M/%r/%T` の組み込み関数`str_to_date`の MySQL 互換性を改善しました [＃25768](https://github.com/pingcap/tidb/pull/25768)

-   TiKV

    -   未確定エラーの可能性を減らすために、事前書き込みリクエストを可能な限りべき等にしてください[＃10586](https://github.com/tikv/tikv/pull/10586)
    -   多数の期限切れコマンドを処理する際のスタックオーバーフローのリスクを防ぐ[＃10502](https://github.com/tikv/tikv/pull/10502)
    -   `max_ts` を更新するためにステイル読み取り要求の`start_ts`使用しないことで、コミット要求の再試行を過度に回避します。 [＃10451](https://github.com/tikv/tikv/pull/10451)
    -   読み取り準備と書き込み準備は別々に処理して読み取りレイテンシーを削減する[＃10592](https://github.com/tikv/tikv/pull/10592)
    -   I/Oレート制限が有効になっている場合のデータインポート速度への影響を軽減します[＃10390](https://github.com/tikv/tikv/pull/10390)
    -   Raft gRPC接続間の負荷分散を改善する[＃10495](https://github.com/tikv/tikv/pull/10495)

-   ツール

    -   TiCDC

        -   `file sorter` を削除 [＃2327](https://github.com/pingcap/tiflow/pull/2327)
        -   PDエンドポイントに証明書がない場合に返されるエラーメッセージを改善しました[＃1973](https://github.com/pingcap/tiflow/issues/1973)

    -   TiDB Lightning

        -   スキーマを復元するための再試行メカニズムを追加する [＃1294](https://github.com/pingcap/br/pull/1294)

    -   Dumpling

        -   アップストリームが TiDB v3.x クラスタの場合は、常に`_tidb_rowid`を使用してテーブルを分割します。これにより、TiDB のメモリ使用量が削減されます[＃295](https://github.com/pingcap/dumpling/issues/295)
        -   データベースメタデータへのアクセス頻度を減らして、Dumplingのパフォーマンスと安定性を向上させます[＃315](https://github.com/pingcap/dumpling/pull/315)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `tidb_enable_amend_pessimistic_txn=on` で列タイプを変更するときに発生する可能性のあるデータ損失の問題を修正しました [＃26203](https://github.com/pingcap/tidb/issues/26203)
    -   `last_day`関数の動作がSQLモードで互換性がない問題を修正 [＃26001](https://github.com/pingcap/tidb/pull/26001)
    -   `LIMIT`ウィンドウ関数上にある場合に発生する可能性のpanic問題を修正しました [＃25344](https://github.com/pingcap/tidb/issues/25344)
    -   悲観的トランザクションをコミットすると書き込み競合が発生する可能性がある問題を修正[＃25964](https://github.com/pingcap/tidb/issues/25964)
    -   相関サブクエリのインデックス結合の結果が間違っている問題を修正[＃25799](https://github.com/pingcap/tidb/issues/25799)
    -   正常にコミットされた楽観的トランザクションがコミットエラーを報告する可能性があるバグを修正[＃10468](https://github.com/tikv/tikv/issues/10468)
    -   `SET`型列でマージ結合を使用すると誤った結果が返される問題を修正しました [＃25669](https://github.com/pingcap/tidb/issues/25669)
    -   悲観的トランザクションのインデックスキーが繰り返しコミットされる可能性があるバグを修正[＃26359](https://github.com/pingcap/tidb/issues/26359)
    -   オプティマイザがパーティション検索する際の整数オーバーフローのリスクを修正 [＃26227](https://github.com/pingcap/tidb/issues/26227)
    -   `DATE`タイムスタンプにキャストするときに無効な値が書き込まれる可能性がある問題を修正しました [＃26292](https://github.com/pingcap/tidb/issues/26292)
    -   Grafana でコプロセッサーキャッシュ メトリックが表示されない問題を修正しました [＃26338](https://github.com/pingcap/tidb/issues/26338)
    -   テレメトリ による迷惑なログの問題を修正 [＃25785](https://github.com/pingcap/tidb/issues/25785) [＃25760](https://github.com/pingcap/tidb/issues/25760)
    -   プレフィックスインデックスのクエリ範囲に関するバグを修正 [＃26029](https://github.com/pingcap/tidb/issues/26029)
    -   同じパーティションを同時に切り捨てるとDDL実行がハングする問題を修正[＃26229](https://github.com/pingcap/tidb/issues/26229)
    -   重複した`ENUM`項目の問題を修正 [＃25955](https://github.com/pingcap/tidb/issues/25955)
    -   CTEイテレータが正しく閉じられていないバグを修正[＃26112](https://github.com/pingcap/tidb/issues/26112)
    -   `LOAD DATA`文が非 UTF8 データを異常にインポートする可能性がある問題を修正[＃25979](https://github.com/pingcap/tidb/issues/25979)
    -   符号なし整数列でウィンドウ関数を使用する際に発生する可能性のあるpanic問題を修正しました [＃25956](https://github.com/pingcap/tidb/issues/25956)
    -   非同期コミットロックを解決する際に TiDB がpanic可能性がある問題を修正[＃25778](https://github.com/pingcap/tidb/issues/25778)
    -   ステイル読み取りが`PREPARE`文と完全に互換性がない問題を修正 [＃25800](https://github.com/pingcap/tidb/pull/25800)
    -   ODBCスタイルの定数（たとえば、 `{d '2020-01-01'}` ）を式として使用できない問題を修正しました。 [＃25531](https://github.com/pingcap/tidb/issues/25531)
    -   TiDBを単独で実行したときに発生するエラーを修正[＃25555](https://github.com/pingcap/tidb/pull/25555)

-   TiKV

    -   特定のプラットフォームで期間計算がpanicになる可能性がある問題を修正[＃10569](https://github.com/tikv/tikv/pull/10569)
    -   Load Base Splitが誤って`batch_get_command` のエンコードされていないキーを使用する問題を修正しました [＃10542](https://github.com/tikv/tikv/issues/10542)
    -   `resolved-ts.advance-ts-interval`構成を動的に変更してもすぐには反映されない問題を修正[＃10426](https://github.com/tikv/tikv/issues/10426)
    -   レプリカが 4 つ以上ある場合に稀に発生するフォロワー メタデータ破損の問題を修正[＃10225](https://github.com/tikv/tikv/issues/10225)
    -   暗号化が有効になっている場合にスナップショットを2回構築すると発生するpanic問題を修正[＃9786](https://github.com/tikv/tikv/issues/9786) [＃10407](https://github.com/tikv/tikv/issues/10407)
    -   間違った`tikv_raftstore_hibernated_peer_state`指標を修正する[＃10330](https://github.com/tikv/tikv/issues/10330)
    -   コプロセッサの関数`json_unquote()`の間違った引数の型を修正 [＃10176](https://github.com/tikv/tikv/issues/10176)
    -   悲観的トランザクションのインデックスキーが繰り返しコミットされる可能性があるバグを修正[＃10468](https://github.com/tikv/tikv/issues/10468#issuecomment-869491061)
    -   リーダーが移行された直後に`ReadIndex`リクエストが古い結果を返す問題を修正しました[＃9351](https://github.com/tikv/tikv/issues/9351)

-   PD

    -   複数のスケジューラが同時に実行されているために競合が発生した場合に、期待どおりのスケジュールを生成できない問題を修正[＃3807](https://github.com/tikv/pd/issues/3807) [＃3778](https://github.com/tikv/pd/issues/3778)
    -   スケジューラがすでに削除されているにもかかわらず、スケジューラが再び表示されることがある問題を修正しました[＃2572](https://github.com/tikv/pd/issues/2572)

-   TiFlash

    -   テーブルスキャンタスクの実行時に発生する可能性のあるpanic問題を修正しました
    -   TiFlashがDAQリクエストを処理する際に約`duplicated region`エラーを発生させるバグを修正しました
    -   読み取り負荷が大きい場合に発生するpanic問題を修正しました
    -   `DateFormat`関数の実行時に発生する可能性のあるpanic問題を修正
    -   MPPタスク実行時に発生する可能性のあるメモリリークの問題を修正
    -   集計関数`COUNT`または`COUNT DISTINCT`実行するときに予期しない結果が発生する問題を修正しました
    -   複数のディスクに展開されたときにTiFlash がデータを復元できない潜在的なバグを修正しました
    -   TiDB DashboardがTiFlashのディスク情報を正しく表示できない問題を修正
    -   解体時に発生する可能性のあるpanic問題を修正`SharedQueryBlockInputStream`
    -   解体時に発生する可能性のあるpanic問題を修正`MPPTask`
    -   スナップショット経由でデータを同期した後に発生する可能性のあるデータの不整合の問題を修正

-   ツール

    -   TiCDC

        -   新しい照合順序機能のサポートを修正[＃2301](https://github.com/pingcap/tiflow/issues/2301)
        -   実行時に共有マップへの非同期アクセスによりpanicが発生する可能性がある問題を修正[＃2300](https://github.com/pingcap/tiflow/pull/2300)
        -   DDL ステートメント実行中にオーナーがクラッシュした場合に発生する可能性のある DDL 損失の問題を修正しました。 [＃2290](https://github.com/pingcap/tiflow/pull/2290)
        -   TiDB のロックを早期に解決しようとする問題を修正[＃2188](https://github.com/pingcap/tiflow/issues/2188)
        -   テーブル移行直後に TiCDC ノードが強制終了した場合にデータ損失が発生する可能性があるバグを修正[＃2033](https://github.com/pingcap/tiflow/pull/2033)
        -   `changefeed update` on `--sort-dir`と`--start-ts` の処理ロジックを修正 [＃1921](https://github.com/pingcap/tiflow/pull/1921)

    -   Backup & Restore (BR)

        -   復元するデータのサイズが正しく計算されない問題を修正[＃1270](https://github.com/pingcap/br/issues/1270)
        -   cdclog から復元するときに発生する DDL イベントの欠落の問題を修正しました [＃870](https://github.com/pingcap/br/issues/870)

    -   TiDB Lightning

        -   TiDBがParquetファイル内の`DECIMAL`種類のデータを解析できない問題を修正 [＃1275](https://github.com/pingcap/br/pull/1275)
        -   キー間隔を計算する際の整数オーバーフローの問題を修正[＃1291](https://github.com/pingcap/br/issues/1291) [＃1290](https://github.com/pingcap/br/issues/1290)
