---
title: TiDB 5.0.4 Release Notes
---

# TiDB5.0.4リリースノート {#tidb-5-0-4-release-notes}

リリース日：2021年9月27日

TiDBバージョン：5.0.4

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   新しいセッションで`SHOW VARIABLES`を実行すると時間がかかる問題を修正します。この修正により、 [＃19341](https://github.com/pingcap/tidb/pull/19341)で行われたいくつかの変更が元に戻され、互換性の問題が発生する可能性があります。 [＃24326](https://github.com/pingcap/tidb/issues/24326)
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から[＃25873](https://github.com/pingcap/tidb/pull/25873)に変更し`3000`

    <!---->

    -   次のバグ修正により、実行結果が変更され、アップグレードの非互換性が発生する可能性があります。
        -   `UNION`の子に`NULL`の値[＃26559](https://github.com/pingcap/tidb/issues/26559)が含まれている場合にTiDBが誤った結果を返す問題を修正します
        -   `greatest(datetime) union null`が空の文字列[＃26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正します
        -   `last_day`関数の動作がSQLモード[＃26000](https://github.com/pingcap/tidb/pull/26000)で互換性がないという問題を修正します
        -   `having`句が正しく機能しない可能性がある問題を修正します[＃26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の周りの照合が異なる場合に発生する誤った実行結果を修正します[＃27146](https://github.com/pingcap/tidb/issues/27146)
        -   `group_concat`関数の列に非ビン照合順序が含まれている場合に発生する誤った実行結果を修正します[＃27429](https://github.com/pingcap/tidb/issues/27429)
        -   複数の列で`count(distinct)`式を使用すると、新しい照合順序が有効になっているときに誤った結果が返される問題を修正します[＃27091](https://github.com/pingcap/tidb/issues/27091)
        -   `extract`関数の引数が負の期間[＃27236](https://github.com/pingcap/tidb/issues/27236)である場合に発生する誤った結果を修正します
        -   `SQL_MODE`が&#39; [＃26762](https://github.com/pingcap/tidb/issues/26762)の場合、無効な日付を挿入してもエラーが報告されない問題を修正します。
        -   `SQL_MODE`が「NO_ZERO_IN_DATE」の場合に無効なデフォルトの日付を使用してもエラーが報告されない問題を修正します[＃26766](https://github.com/pingcap/tidb/issues/26766)
        -   プレフィックスインデックス[＃26029](https://github.com/pingcap/tidb/issues/26029)のクエリ範囲のバグを修正
        -   `LOAD DATA`ステートメントがutf8以外のデータを異常にインポートする可能性がある問題を修正します[＃25979](https://github.com/pingcap/tidb/issues/25979)
        -   二次インデックスが主キー[＃25809](https://github.com/pingcap/tidb/issues/25809)と同じ列を持っている場合、 `insert ignore on duplicate update`が間違ったデータを挿入する可能性がある問題を修正します。
        -   パーティションテーブルにクラスター化インデックス[＃25846](https://github.com/pingcap/tidb/issues/25846)がある場合、 `insert ignore duplicate update`が間違ったデータを挿入する可能性がある問題を修正します。
        -   キーが`ENUM`タイプのポイント取得またはバッチポイント取得[＃24562](https://github.com/pingcap/tidb/issues/24562)の場合、クエリ結果が間違っている可能性がある問題を修正します。
        -   `BIT`タイプの値を除算するときに発生する間違った結果を修正します[＃23479](https://github.com/pingcap/tidb/issues/23479)
        -   `prepared`ステートメントと直接クエリの結果に一貫性がない可能性があるという問題を修正します[＃22949](https://github.com/pingcap/tidb/issues/22949)
        -   `YEAR`型を文字列または整数型[＃23262](https://github.com/pingcap/tidb/issues/23262)と比較すると、クエリ結果が間違っている可能性がある問題を修正します。

## 機能拡張 {#feature-enhancements}

-   TiDB

    -   オプティマイザ推定を無視し、MPPモード[＃26382](https://github.com/pingcap/tidb/pull/26382)を強制的に使用するには、設定`tidb_enforce_mpp=1`をサポートします。

-   TiKV

    -   TiCDC構成の動的な変更をサポート[＃10645](https://github.com/tikv/tikv/issues/10645)

-   PD

    -   TiDBダッシュボード[＃3884](https://github.com/tikv/pd/pull/3884)のOIDCベースのSSOサポートを追加します

-   TiFlash

    -   DAGリクエストで`HAVING()`の機能をサポートする
    -   `DATE()`機能をサポート
    -   インスタンスごとの書き込みスループットのためにGrafanaパネルを追加します

## 改善 {#improvements}

-   TiDB

    -   ヒストグラムの行数に基づいて自動分析をトリガーする[＃24237](https://github.com/pingcap/tidb/issues/24237)
    -   ノードに障害が発生し、 [＃26757](https://github.com/pingcap/tidb/pull/26757)より前に再起動した場合は、TiFlashノードへの要求の送信を一定期間停止します。
    -   `split region`の上限を増やして、 `split table`と`presplit`をより安定させます[＃26657](https://github.com/pingcap/tidb/pull/26657)
    -   MPPクエリの再試行をサポート[＃26483](https://github.com/pingcap/tidb/pull/26483)
    -   MPPクエリを起動する前にTiFlashの可用性を確認してください[＃1807](https://github.com/pingcap/tics/issues/1807)
    -   安定した結果モードをサポートして、クエリ結果をより安定させます[＃26084](https://github.com/pingcap/tidb/pull/26084)
    -   MySQLシステム変数`init_connect`とそれに関連する機能をサポートする[＃18894](https://github.com/pingcap/tidb/issues/18894)
    -   MPPモード[＃25861](https://github.com/pingcap/tidb/pull/25861)で`COUNT(DISTINCT)`集約機能を徹底的に押し下げます。
    -   `EXPLAIN`のステートメントで集計関数をプッシュダウンできない場合のログ警告の出力[＃25736](https://github.com/pingcap/tidb/pull/25736)
    -   Grafanaダッシュボード[＃25327](https://github.com/pingcap/tidb/pull/25327)に`TiFlashQueryTotalCounter`のエラーラベルを追加します
    -   [＃24209](https://github.com/pingcap/tidb/issues/24209)によるセカンダリインデックスを介したクラスター化インデックステーブルのMVCCデータの取得をサポート
    -   パーサー[＃24371](https://github.com/pingcap/tidb/pull/24371)の`prepared`のステートメントのメモリ割り当てを最適化します

-   TiKV

    -   読み取りの待ち時間を短縮するために、読み取り準備と書き込み準備を別々に処理します[＃10475](https://github.com/tikv/tikv/issues/10475)
    -   解決されたTSメッセージのサイズを減らして、ネットワーク帯域幅を節約します[＃2448](https://github.com/pingcap/tiflow/issues/2448)
    -   sloggerスレッドが過負荷になり、キューがいっぱいになったときにスレッドをブロックする代わりにログをドロップする[＃10841](https://github.com/tikv/tikv/issues/10841)
    -   TiKVコプロセッサーの遅いログに、要求の処理に費やされた時間のみを考慮させる[＃10841](https://github.com/tikv/tikv/issues/10841)
    -   未確定のエラーの可能性を減らすために、可能な限りべき等の事前書き込みを行います[＃10587](https://github.com/tikv/tikv/pull/10587)
    -   書き込みフローが少ない場合の誤った「GCが機能しない」アラートを回避する[＃10662](https://github.com/tikv/tikv/pull/10662)
    -   復元するデータベースを、バックアップ中に常に元のクラスタサイズと一致させるようにします。 [＃10643](https://github.com/tikv/tikv/pull/10643)
    -   panic出力がログ[＃9955](https://github.com/tikv/tikv/pull/9955)にフラッシュされることを確認します

-   PD

    -   PD間でリージョン情報を同期するパフォーマンスを向上させる[＃3993](https://github.com/tikv/pd/pull/3993)

-   ツール

    -   Dumpling

        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`構文をサポートしないMySQL互換データベースのバックアップをサポートする[＃309](https://github.com/pingcap/dumpling/issues/309)

    -   TiCDC

        -   UnifiedSorterがメモリを使用して[＃2553](https://github.com/pingcap/tiflow/issues/2553)をソートするときにメモリ管理を最適化する
        -   メジャーバージョンまたはマイナーバージョン間でのTiCDCクラスターの運用を禁止する[＃2598](https://github.com/pingcap/tiflow/pull/2598)
        -   テーブルのリージョンがすべてTiKVノードから転送される場合のゴルーチンの使用量を減らします[＃2284](https://github.com/pingcap/tiflow/issues/2284)
        -   [＃2326](https://github.com/pingcap/tiflow/pull/2326)を削除し`file sorter`
        -   常にTiKVから古い値を取得し、出力は`enable-old-value`に従って調整され[＃2301](https://github.com/pingcap/tiflow/issues/2301) 。
        -   PDエンドポイントが証明書を見逃したときに返されるエラーメッセージを改善する[＃1973](https://github.com/pingcap/tiflow/issues/1973)
        -   同時実行性が高い場合に、ワーカープールを最適化してゴルーチンを減らします[＃2211](https://github.com/pingcap/tiflow/issues/2211)
        -   グローバルgRPC接続プールを追加し、KVクライアント間でgRPC接続を共有します[＃2533](https://github.com/pingcap/tiflow/pull/2533)

## バグの修正 {#bug-fixes}

-   TiDB

    -   パーティション化されたテーブルをクエリするときにTiDBがpanicになり、パーティションキーの条件が`IS NULL`になる問題を修正し[＃23802](https://github.com/pingcap/tidb/issues/23802) 。
    -   `FLOAT64`タイプのオーバーフローチェックがMySQL3のオーバーフローチェックと異なる問題を修正し[＃23897](https://github.com/pingcap/tidb/issues/23897)
    -   `case when`式[＃26662](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序を修正します
    -   悲観的なトランザクションをコミットすると書き込みの競合が発生する可能性があるという問題を修正します[＃25964](https://github.com/pingcap/tidb/issues/25964)
    -   悲観的なトランザクションのインデックスキーが繰り返しコミットされる可能性があるバグを修正し[＃10600](https://github.com/tikv/tikv/pull/10600) [＃26359](https://github.com/pingcap/tidb/issues/26359)
    -   非同期コミットロックを解決するときにTiDBがpanicになる可能性がある問題を修正します[＃25778](https://github.com/pingcap/tidb/issues/25778)
    -   [＃25045](https://github.com/pingcap/tidb/issues/25045)を使用すると列が見つからない可能性があるバグを修正し`INDEX MERGE`
    -   `ALTER USER REQUIRE SSL`がユーザーの[＃25225](https://github.com/pingcap/tidb/issues/25225)をクリアするバグを修正し`authentication_string`
    -   新しいクラスタの`tidb_gc_scan_lock_mode`のグローバル変数の値が実際のデフォルトモード「LEGACY」ではなく「PHYSICAL」と表示されるバグを修正します[＃25100](https://github.com/pingcap/tidb/issues/25100)
    -   `TIKV_REGION_PEERS`システムテーブルに正しい`DOWN`ステータスが表示されないバグを修正します[＃24879](https://github.com/pingcap/tidb/issues/24879)
    -   HTTPAPIの使用時に発生するメモリリークの問題を修正します[＃24649](https://github.com/pingcap/tidb/pull/24649)
    -   ビューが[＃24414](https://github.com/pingcap/tidb/issues/24414)をサポートしない問題を修正し`DEFINER`
    -   `tidb-server --help`がコード[＃24046](https://github.com/pingcap/tidb/issues/24046)で終了する問題を修正し`2`
    -   グローバル変数`dml_batch_size`の設定が有効にならない問題を修正します[＃24709](https://github.com/pingcap/tidb/issues/24709)
    -   `read_from_storage`とパーティションテーブルを同時に使用するとエラー[＃20372](https://github.com/pingcap/tidb/issues/20372)が発生する問題を修正します
    -   射影演算子[＃24264](https://github.com/pingcap/tidb/issues/24264)を実行するときにTiDBがパニックになる問題を修正します
    -   統計によってクエリがpanicになる可能性がある問題を修正します[＃24061](https://github.com/pingcap/tidb/pull/24061)
    -   `BIT`列で`approx_percentile`関数を使用するとpanicになる可能性がある問題を修正します[＃23662](https://github.com/pingcap/tidb/issues/23662)
    -   Grafanaの**コプロセッサーキャッシュ**パネルのメトリックが間違っている問題を修正します[＃26338](https://github.com/pingcap/tidb/issues/26338)
    -   同じパーティションを同時に切り捨てると、DDLステートメントがスタックする問題を修正します[＃26229](https://github.com/pingcap/tidb/issues/26229)
    -   セッション変数が`GROUP BY`項目として使用されたときに発生する誤ったクエリ結果の問題を修正します[＃27106](https://github.com/pingcap/tidb/issues/27106)
    -   テーブル[＃25902](https://github.com/pingcap/tidb/issues/25902)を結合するときの`VARCHAR`とタイムスタンプの間の誤った暗黙の変換を修正しました
    -   関連するサブクエリステートメントの間違った結果を修正する[＃27233](https://github.com/pingcap/tidb/issues/27233)

-   TiKV

    -   破損したスナップショットファイルによって引き起こされる潜在的なディスクフルの問題を修正する[＃10813](https://github.com/tikv/tikv/issues/10813)
    -   Titanが有効になっている5.0より前のバージョンからアップグレードするときに発生するTiKVpanicの問題を修正します[＃10843](https://github.com/tikv/tikv/pull/10843)
    -   新しいバージョンのTiKVをv5.0.xにロールバックできない問題を修正します[＃10843](https://github.com/tikv/tikv/pull/10843)
    -   5.0より前のバージョンから5.0以降のバージョンにアップグレードするときに発生するTiKVpanicの問題を修正します。アップグレード前にTitanを有効にしてクラスタをTiKVv3.xからアップグレードした場合、このクラスタで問題が発生する可能性があります。 [＃10774](https://github.com/tikv/tikv/issues/10774)
    -   左の悲観的なロックによって引き起こされた解析の失敗を修正します[＃26404](https://github.com/pingcap/tidb/issues/26404)
    -   特定のプラットフォームで期間を計算するときに発生するpanicを修正する[＃10571](https://github.com/tikv/tikv/pull/10571)
    -   LoadBaseSplitの`batch_get_command`のキーがエンコードされていない[＃10542](https://github.com/tikv/tikv/issues/10542)の問題を修正します

-   PD

    -   PDが時間内にダウンピアを修正しないという問題を修正します[＃4077](https://github.com/tikv/pd/issues/4077)
    -   `replication.max-replicas`が更新された後、デフォルトの配置ルールのレプリカ数が一定のままになる問題を修正します[＃3886](https://github.com/tikv/pd/issues/3886)
    -   TiKV1をスケールアウトするときにPDがpanicになる可能性があるバグを修正し[＃3868](https://github.com/tikv/pd/issues/3868)
    -   複数のスケジューラーが同時に実行されている場合に発生するスケジュールの競合の問題を修正します[＃3807](https://github.com/tikv/pd/issues/3807)
    -   スケジューラーが削除された場合でもスケジューラーが再び表示される可能性がある問題を修正します[＃2572](https://github.com/tikv/pd/issues/2572)

-   TiFlash

    -   テーブルスキャンタスクの実行時に発生する可能性のあるpanicの問題を修正します
    -   MPPタスクの実行時に発生する可能性のあるメモリリークの問題を修正します
    -   DAQリクエストを処理するときにTiFlashが`duplicated region`エラーを発生させるバグを修正します
    -   集計関数`COUNT`または`COUNT DISTINCT`を実行するときに予期しない結果が発生する問題を修正します
    -   MPPタスクの実行時に発生する可能性のあるpanicの問題を修正します
    -   複数のディスクにデプロイしたときにTiFlashがデータを復元できない潜在的なバグを修正します
    -   `SharedQueryBlockInputStream`を解体するときに発生する可能性のあるpanicの問題を修正します
    -   `MPPTask`を解体するときに発生する可能性のあるpanicの問題を修正します
    -   TiFlashがMPP接続の確立に失敗した場合の予期しない結果の問題を修正します
    -   ロックを解決するときに発生する可能性のあるpanicの問題を修正します
    -   大量の書き込みの下でメトリックのストアサイズが不正確になる問題を修正します
    -   `<=`に`CONSTANT`などの`>`が含まれている場合に発生する`COLUMN`た結果の`>=`を修正し`<`
    -   TiFlashが長時間実行した後にデルタデータをガベージコレクションできないという潜在的な問題を修正します
    -   メトリックが間違った値を表示する潜在的なバグを修正します
    -   TiFlashが複数のディスクに展開されているときに発生するデータの不整合の潜在的な問題を修正します

-   ツール

    -   Dumpling

        -   MySQL8.0.3以降のバージョン[＃322](https://github.com/pingcap/dumpling/issues/322)で`show table status`の実行がスタックする問題を修正します

    -   TiCDC

        -   `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar`などのデータ型をJSON3にエンコードするときに発生するプロセスpanicの問題を修正し[＃2758](https://github.com/pingcap/tiflow/issues/2758)
        -   このテーブルが再スケジュールされているときに複数のプロセッサが同じテーブルにデータを書き込む可能性があるために発生するデータの不整合の問題を修正します[＃2417](https://github.com/pingcap/tiflow/pull/2417)
        -   TiCDCがあまりにも多くのリージョンをキャプチャするときに発生するOOMを回避するために、gRPCウィンドウサイズを小さくします[＃2724](https://github.com/pingcap/tiflow/pull/2724)
        -   メモリプレッシャーが高いときにgRPC接続が頻繁に切断されるというエラーを修正します[＃2202](https://github.com/pingcap/tiflow/issues/2202)
        -   符号なし`TINYINT`タイプ[＃2648](https://github.com/pingcap/tiflow/issues/2648)でTiCDCがpanicになるバグを修正します
        -   トランザクションを挿入し、アップストリーム[＃2612](https://github.com/pingcap/tiflow/issues/2612)の同じ行のデータを削除すると、TiCDCOpenProtocolが空の値を出力する問題を修正します。
        -   スキーマ変更の終了TSで変更フィードが開始されたときにDDL処理が失敗するバグを修正します[＃2603](https://github.com/pingcap/tiflow/issues/2603)
        -   タスクがタイムアウトするまで、応答しないダウンストリームが古い所有者のレプリケーションタスクを中断する問題を修正します[＃2295](https://github.com/pingcap/tiflow/issues/2295)
        -   メタデータ管理のバグを修正する[＃2558](https://github.com/pingcap/tiflow/pull/2558)
        -   TiCDC所有者の切り替え後に発生するデータの不整合の問題を修正します[＃2230](https://github.com/pingcap/tiflow/issues/2230)
        -   `capture list`コマンドの出力に古いキャプチャが表示される可能性がある問題を修正します[＃2388](https://github.com/pingcap/tiflow/issues/2388)
        -   統合テスト[＃2422](https://github.com/pingcap/tiflow/issues/2422)でDDLジョブの重複が発生したときに発生する`ErrSchemaStorageTableMiss`のエラーを修正します。
        -   `ErrGCTTLExceeded`エラーが発生した場合にチェンジフィードを削除できないというバグを修正します[＃2391](https://github.com/pingcap/tiflow/issues/2391)
        -   大きなテーブルを[＃2424](https://github.com/pingcap/tiflow/issues/2424)に複製できないバグを修正します[＃1259](https://github.com/pingcap/tiflow/issues/1259)
        -   CLIの下位互換性の問題を修正する[＃2373](https://github.com/pingcap/tiflow/issues/2373)
        -   [＃2299](https://github.com/pingcap/tiflow/pull/2299)のマップへの安全でない同時アクセスの問題を修正し`SinkManager`
        -   DDLステートメントの実行時に所有者がクラッシュした場合の潜在的なDDL損失の問題を修正します[＃1260](https://github.com/pingcap/tiflow/issues/1260)
        -   リージョンが初期化された直後にロックが解決される問題を修正します[＃2188](https://github.com/pingcap/tiflow/issues/2188)
        -   新しいパーティションテーブルを追加するときに発生する余分なパーティションディスパッチの問題を修正します[＃2263](https://github.com/pingcap/tiflow/pull/2263)
        -   TiCDCが削除されたチェンジフィードで警告を表示し続ける問題を修正します[＃2156](https://github.com/pingcap/tiflow/issues/2156)
