---
title: TiDB 5.0.4 Release Notes
summary: 互換性の変更には、SHOW VARIABLES` の実行速度低下の修正、`tidb_stmt_summary_max_stmt_count` のデフォルト値の変更、およびアップグレード時の非互換性を引き起こす可能性のあるバグ修正が含まれます。機能強化には、`tidb_enforce_mpp=1` 設定のサポートと動的 TiCDC 構成が含まれます。改善点には、自動分析トリガー、MPP クエリ再試行のサポート、安定した結果モードが含まれます。バグ修正では、TiDB、TiKV、PD、 TiFlash、およびDumplingや TiCDC などのツールにおけるさまざまな問題が修正されています。
---

# TiDB 5.0.4 リリースノート {#tidb-5-0-4-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 5.0.4

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   新規セッションで`SHOW VARIABLES`を実行すると遅くなる問題を修正しました。この修正により、 で行われた変更の一部が元に戻り、互換性の問題が発生する可能性があります[＃24326](https://github.com/pingcap/tidb/issues/24326) [＃19341](https://github.com/pingcap/tidb/pull/19341)
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から`3000`に変更します[＃25873](https://github.com/pingcap/tidb/pull/25873)

    <!---->

    -   次のバグ修正により実行結果が変わり、アップグレードの非互換性が発生する可能性があります。
        -   `UNION`の子に`NULL`値が含まれている場合に TiDB が間違った結果を返す問題を修正しました [＃26559](https://github.com/pingcap/tidb/issues/26559)
        -   `greatest(datetime) union null`空の文字列を返す問題を修正[＃26532](https://github.com/pingcap/tidb/issues/26532)
        -   `last_day`関数の動作が SQL モードで互換性がない問題を修正しました [＃26000](https://github.com/pingcap/tidb/pull/26000)
        -   `having`節が正しく動作しない可能性がある問題を修正[＃26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`前後の照合順序が異なる場合に発生する誤った実行結果を修正[＃27146](https://github.com/pingcap/tidb/issues/27146)
        -   `group_concat`関数の列に非ビン照合順序ある場合に発生する誤った実行結果を修正しました [＃27429](https://github.com/pingcap/tidb/issues/27429)
        -   新しい照合順序が有効になっているときに、複数の列で`count(distinct)`式を使用すると間違った結果が返される問題を修正しました[＃27091](https://github.com/pingcap/tidb/issues/27091)
        -   `extract`関数の引数が負の期間場合に発生する結果の誤りを修正 [＃27236](https://github.com/pingcap/tidb/issues/27236)
        -   `SQL_MODE` 「STRICT_TRANS_TABLES」の場合、無効な日付を挿入してもエラーが報告されない問題を修正しました[＃26762](https://github.com/pingcap/tidb/issues/26762)
        -   `SQL_MODE` 「NO_ZERO_IN_DATE」の場合に無効なデフォルト日付を使用してもエラーが報告されない問題を修正しました[＃26766](https://github.com/pingcap/tidb/issues/26766)
        -   プレフィックスインデックスのクエリ範囲に関するバグを修正 [＃26029](https://github.com/pingcap/tidb/issues/26029)
        -   `LOAD DATA`文が非 UTF8 データを異常にインポートする可能性がある問題を修正[＃25979](https://github.com/pingcap/tidb/issues/25979)
        -   `insert ignore on duplicate update`セカンダリインデックスに主キーと同じ列がある場合に間違ったデータが挿入される可能性がある問題を修正[＃25809](https://github.com/pingcap/tidb/issues/25809)
        -   パーティションテーブルにクラスター化インデックスがある場合に間違ったデータが挿入される可能性が`insert ignore duplicate update`問題を修正しました[＃25846](https://github.com/pingcap/tidb/issues/25846)
        -   PointGetまたはバッチPointGetでキーが`ENUM`型の場合にクエリ結果が間違っている可能性がある問題を修正しました [＃24562](https://github.com/pingcap/tidb/issues/24562)
        -   `BIT`型の値を割ったときに発生する誤った結果を修正しました [＃23479](https://github.com/pingcap/tidb/issues/23479)
        -   `prepared`ステートメントと直接クエリの結果が矛盾する可能性がある問題を修正[＃22949](https://github.com/pingcap/tidb/issues/22949)
        -   `YEAR`型を文字列または整数型と比較するとクエリ結果が間違っている可能性がある問題を修正しました [＃23262](https://github.com/pingcap/tidb/issues/23262)

## 機能強化 {#feature-enhancements}

-   TiDB

    -   最適化の推定を無視し、MPPモードを強制的に使用する設定`tidb_enforce_mpp=1`サポート [＃26382](https://github.com/pingcap/tidb/pull/26382)

-   TiKV

    -   TiCDC 構成の動的な変更をサポート[＃10645](https://github.com/tikv/tikv/issues/10645)

-   PD

    -   TiDB DashboardにOIDCベースのSSOサポートを追加 [＃3884](https://github.com/tikv/pd/pull/3884)

-   TiFlash

    -   DAGリクエストの`HAVING()`機能をサポートする
    -   `DATE()`機能をサポートする
    -   インスタンスごとの書き込みスループットの Grafana パネルを追加する

## 改善点 {#improvements}

-   TiDB

    -   ヒストグラムの行数に基づいて自動分析をトリガーする[＃24237](https://github.com/pingcap/tidb/issues/24237)
    -   ノードが故障して前に再起動した場合、一定期間TiFlashノードへのリクエストの送信を停止します。 [＃26757](https://github.com/pingcap/tidb/pull/26757)
    -   `split region`上限を上げて`split table`と`presplit`をより安定させる[＃26657](https://github.com/pingcap/tidb/pull/26657)
    -   MPPクエリの再試行をサポート[＃26483](https://github.com/pingcap/tidb/pull/26483)
    -   MPPクエリを起動する前にTiFlashの可用性を確認してください [＃1807](https://github.com/pingcap/tics/issues/1807)
    -   クエリ結果をより安定させるために、安定した結果モードをサポートします[＃26084](https://github.com/pingcap/tidb/pull/26084)
    -   MySQLシステム変数`init_connect`とその関連機能サポートする [＃18894](https://github.com/pingcap/tidb/issues/18894)
    -   MPPモードで`COUNT(DISTINCT)`集約機能を徹底的にプッシュダウンする [＃25861](https://github.com/pingcap/tidb/pull/25861)
    -   集計関数を`EXPLAIN`文でプッシュダウンできない場合にログ警告を出力する [＃25736](https://github.com/pingcap/tidb/pull/25736)
    -   Grafanaダッシュボードの`TiFlashQueryTotalCounter`にエラーラベルを追加する [＃25327](https://github.com/pingcap/tidb/pull/25327)
    -   HTTP API によるセカンダリインデックス経由でクラスター化インデックステーブルの MVCC データを取得する機能をサポート [＃24209](https://github.com/pingcap/tidb/issues/24209)
    -   パーサーの`prepared`文のメモリ割り当てを最適化する [＃24371](https://github.com/pingcap/tidb/pull/24371)

-   TiKV

    -   読み取り準備と書き込み準備は別々に処理して読み取りレイテンシーを削減する[＃10475](https://github.com/tikv/tikv/issues/10475)
    -   ネットワーク帯域幅を節約するために、解決されたTSメッセージのサイズを縮小します[＃2448](https://github.com/pingcap/tiflow/issues/2448)
    -   スロガースレッドが過負荷になりキューがいっぱいになったときに、スレッドをブロックする代わりにログをドロップする[＃10841](https://github.com/tikv/tikv/issues/10841)
    -   TiKVコプロセッサのスローログに、リクエスト処理に費やされた時間のみを考慮するようにする [＃10841](https://github.com/tikv/tikv/issues/10841)
    -   未確定エラーの可能性を減らすために、できるだけべき等な事前書き込みを行う[＃10587](https://github.com/tikv/tikv/pull/10587)
    -   書き込みフローが低い場合に「GC が動作できません」という誤った警告を回避する[＃10662](https://github.com/tikv/tikv/pull/10662)
    -   復元するデータベースが、バックアップ時の元のクラスタサイズと常に一致するようにします[＃10643](https://github.com/tikv/tikv/pull/10643)
    -   panic出力がログにフラッシュされていることを確認する [＃9955](https://github.com/tikv/tikv/pull/9955)

-   PD

    -   PD間のリージョン情報の同期パフォーマンスを向上[＃3993](https://github.com/tikv/pd/pull/3993)

-   ツール

    -   Dumpling

        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`構文をサポートしていない MySQL 互換データベースのバックアップをサポート[＃309](https://github.com/pingcap/dumpling/issues/309)

    -   TiCDC

        -   Unified Sorterがメモリを使用してソートする場合のメモリ管理を最適化します[＃2553](https://github.com/pingcap/tiflow/issues/2553)
        -   メジャーバージョンまたはマイナーバージョン間での TiCDC クラスターの操作を禁止[＃2598](https://github.com/pingcap/tiflow/pull/2598)
        -   テーブルのリージョンがすべて TiKV ノードから転送されるときに、goroutine の使用を減らす [＃2284](https://github.com/pingcap/tiflow/issues/2284)
        -   `file sorter` を削除 [＃2326](https://github.com/pingcap/tiflow/pull/2326)
        -   常にTiKVから古い値を引き出し、出力は`enable-old-value` に従って調整されます。 [＃2301](https://github.com/pingcap/tiflow/issues/2301)
        -   PDエンドポイントに証明書がない場合に返されるエラーメッセージを改善しました[＃1973](https://github.com/pingcap/tiflow/issues/1973)
        -   同時実行性が高い場合は、ワーカープールを最適化してゴルーチンの数を減らす[＃2211](https://github.com/pingcap/tiflow/issues/2211)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[＃2533](https://github.com/pingcap/tiflow/pull/2533)

## バグ修正 {#bug-fixes}

-   TiDB

    -   パーティションテーブルをクエリし、パーティションキーに条件`IS NULL`がある場合に TiDB がpanic可能性がある問題を修正しました[＃23802](https://github.com/pingcap/tidb/issues/23802)
    -   `FLOAT64`型のオーバーフローチェックがMySQL と異なる問題を修正 [＃23897](https://github.com/pingcap/tidb/issues/23897)
    -   `case when`式の間違った文字セットと照合順序を修正します [＃26662](https://github.com/pingcap/tidb/issues/26662)
    -   悲観的トランザクションをコミットすると書き込み競合が発生する可能性がある問題を修正[＃25964](https://github.com/pingcap/tidb/issues/25964)
    -   悲観的トランザクションのインデックスキーが繰り返しコミットされる可能性があるバグを修正[＃26359](https://github.com/pingcap/tidb/issues/26359) [＃10600](https://github.com/tikv/tikv/pull/10600)
    -   非同期コミットロックを解決する際に TiDB がpanic可能性がある問題を修正[＃25778](https://github.com/pingcap/tidb/issues/25778)
    -   `INDEX MERGE` 使用時に列が見つからないことがあるバグを修正 [＃25045](https://github.com/pingcap/tidb/issues/25045)
    -   `ALTER USER REQUIRE SSL`ユーザーの`authentication_string` をクリアするバグを修正 [＃25225](https://github.com/pingcap/tidb/issues/25225)
    -   新しいクラスターの`tidb_gc_scan_lock_mode`グローバル変数の値が、実際のデフォルトモード「LEGACY」 ではなく「PHYSICAL」と表示されるバグを修正しました。 [＃25100](https://github.com/pingcap/tidb/issues/25100)
    -   `TIKV_REGION_PEERS`システムテーブルに正しい`DOWN`ステータスが表示されないバグを修正しました [＃24879](https://github.com/pingcap/tidb/issues/24879)
    -   HTTP API使用時に発生するメモリリークの問題を修正[＃24649](https://github.com/pingcap/tidb/pull/24649)
    -   ビューが`DEFINER` をサポートしない問題を修正 [＃24414](https://github.com/pingcap/tidb/issues/24414)
    -   `tidb-server --help`コード`2` で終了する問題を修正 [＃24046](https://github.com/pingcap/tidb/issues/24046)
    -   グローバル変数`dml_batch_size`設定が有効にならない問題を修正[＃24709](https://github.com/pingcap/tidb/issues/24709)
    -   `read_from_storage`とパーティションテーブルを同時に使用するとエラーが発生する問題を修正[＃20372](https://github.com/pingcap/tidb/issues/20372)
    -   射影演算子を実行するときに TiDB がパニックを起こす問題を修正しました [＃24264](https://github.com/pingcap/tidb/issues/24264)
    -   統計情報によりクエリがpanicになる可能性がある問題を修正[＃24061](https://github.com/pingcap/tidb/pull/24061)
    -   `BIT`列で`approx_percentile`関数を使用するとpanic可能性がある問題を修正しました[＃23662](https://github.com/pingcap/tidb/issues/23662)
    -   Grafanaの**コプロセッサー Cache**パネルのメトリックが間違っている問題を修正しました[＃26338](https://github.com/pingcap/tidb/issues/26338)
    -   同じパーティションを同時に切り捨てるとDDL文がスタックする問題を修正しました[＃26229](https://github.com/pingcap/tidb/issues/26229)
    -   セッション変数を`GROUP BY`項目として使用した場合に発生する誤ったクエリ結果の問題を修正しました [＃27106](https://github.com/pingcap/tidb/issues/27106)
    -   テーブルを結合する際の`VARCHAR`とタイムスタンプ間の誤った暗黙的な変換を修正しました [＃25902](https://github.com/pingcap/tidb/issues/25902)
    -   関連するサブクエリステートメントの誤った結果を修正する[＃27233](https://github.com/pingcap/tidb/issues/27233)

-   TiKV

    -   破損したスナップショットファイルによって引き起こされる潜在的なディスクフル問題を修正[＃10813](https://github.com/tikv/tikv/issues/10813)
    -   Titan が有効になっている 5.0 より前のバージョンからアップグレードするときに発生する TiKV panic問題を修正しました[＃10843](https://github.com/tikv/tikv/pull/10843)
    -   新しいバージョンのTiKVをv5.0.xにロールバックできない問題を修正しました[＃10843](https://github.com/tikv/tikv/pull/10843)
    -   5.0より前のバージョンから5.0以降のバージョンにアップグレードする際に発生するTiKV panicの問題を修正しました。アップグレード前にTitanが有効になっているTiKV v3.xからクラスタをアップグレードした場合、このクラスタでこの問題が発生する可能性があります[＃10774](https://github.com/tikv/tikv/issues/10774)
    -   左悲観的ロックによる解析エラーを修正[＃26404](https://github.com/pingcap/tidb/issues/26404)
    -   特定のプラットフォームで期間を計算するときに発生するpanicを修正[＃10571](https://github.com/tikv/tikv/pull/10571)
    -   Load Base Split の`batch_get_command`のキーがエンコードされていない問題を修正[＃10542](https://github.com/tikv/tikv/issues/10542)

-   PD

    -   PDがダウンしたピアを時間内に修復しない問題を修正[＃4077](https://github.com/tikv/pd/issues/4077)
    -   `replication.max-replicas`を更新した後、デフォルトの配置ルールのレプリカ数が一定のままになる問題を修正[＃3886](https://github.com/tikv/pd/issues/3886)
    -   TiKV をスケールアウトするときに PD がpanic可能性があるバグを修正しました [＃3868](https://github.com/tikv/pd/issues/3868)
    -   複数のスケジューラが同時に実行されているときに発生するスケジュール競合の問題を修正[＃3807](https://github.com/tikv/pd/issues/3807)
    -   スケジューラが削除された後でも再び表示されることがある問題を修正[＃2572](https://github.com/tikv/pd/issues/2572)

-   TiFlash

    -   テーブルスキャンタスクの実行時に発生する可能性のあるpanic問題を修正しました
    -   MPPタスク実行時に発生する可能性のあるメモリリークの問題を修正
    -   TiFlashがDAQリクエストを処理する際に`duplicated region`エラーを発生させるバグを修正しました
    -   集計関数`COUNT`または`COUNT DISTINCT`を実行するときに予期しない結果が発生する問題を修正しました
    -   MPPタスク実行時に発生する可能性のあるpanic問題を修正
    -   複数のディスクに展開されたときにTiFlash がデータを復元できない潜在的なバグを修正しました
    -   解体時に発生する可能性のあるpanic問題を修正`SharedQueryBlockInputStream`
    -   解体時に発生する可能性のあるpanic問題を修正`MPPTask`
    -   TiFlash がMPP 接続を確立できなかった場合に予期しない結果が発生する問題を修正しました
    -   ロックを解決する際に発生する可能性のあるpanic問題を修正
    -   書き込みが集中するとメトリクスのストアサイズが不正確になる問題を修正しました
    -   クエリに`CONSTANT` 、 `<` 、 `<=` 、 `>` 、 `>=` 、 `COLUMN`などのフィルターが含まれている場合に誤った結果が発生するバグを修正しました。
    -   TiFlash が長時間実行した後にデルタデータをガベージコレクションできない潜在的な問題を修正しました
    -   メトリックが間違った値を表示する潜在的なバグを修正
    -   TiFlash を複数のディスクに展開した場合に発生する可能性のあるデータの不整合の問題を修正しました。

-   ツール

    -   Dumpling

        -   MySQL 8.0.3以降のバージョンで`show table status`の実行が停止する問題を修正[＃322](https://github.com/pingcap/dumpling/issues/322)

    -   TiCDC

        -   `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar`などのデータ型をJSON にエンコードする際に発生するプロセスpanicの問題を修正 [＃2758](https://github.com/pingcap/tiflow/issues/2758)
        -   このテーブルが再スケジュールされているときに複数のプロセッサが同じテーブルにデータを書き込む可能性があるために発生するデータの不整合の問題を修正しました[＃2417](https://github.com/pingcap/tiflow/pull/2417)
        -   TiCDC があまりにも多くのリージョンをキャプチャしたときに発生する OOM を回避するために、gRPC ウィンドウのサイズを小さくします[＃2724](https://github.com/pingcap/tiflow/pull/2724)
        -   メモリ負荷が高いときにgRPC接続が頻繁に切断されるエラーを修正[＃2202](https://github.com/pingcap/tiflow/issues/2202)
        -   符号なし`TINYINT`型でTiCDCがpanicを起こすバグを修正 [＃2648](https://github.com/pingcap/tiflow/issues/2648)
        -   TiCDCオープンプロトコルがトランザクションを挿入し、アップストリームで同じ行のデータを削除すると空の値を出力する問題を修正しました。 [＃2612](https://github.com/pingcap/tiflow/issues/2612)
        -   スキーマ変更の終了 TS で変更フィードが開始されると DDL 処理が失敗するバグを修正しました。 [＃2603](https://github.com/pingcap/tiflow/issues/2603)
        -   応答しないダウンストリームが、タスクがタイムアウトするまで古い所有者のレプリケーションタスクを中断する問題を修正しました[＃2295](https://github.com/pingcap/tiflow/issues/2295)
        -   メタデータ管理のバグを修正 [＃2558](https://github.com/pingcap/tiflow/pull/2558)
        -   TiCDC 所有者スイッチ後に発生するデータの不整合の問題を修正[＃2230](https://github.com/pingcap/tiflow/issues/2230)
        -   `capture list`コマンドの出力に古いキャプチャが表示される可能性がある問題を修正しました [＃2388](https://github.com/pingcap/tiflow/issues/2388)
        -   統合テストでDDLジョブの重複が発生したときに発生する`ErrSchemaStorageTableMiss`エラーを修正します [＃2422](https://github.com/pingcap/tiflow/issues/2422)
        -   `ErrGCTTLExceeded`エラーが発生した場合に changefeed を削除できないバグを修正[＃2391](https://github.com/pingcap/tiflow/issues/2391)
        -   大きなテーブルをcdclogに複製できないバグを修正[＃1259](https://github.com/pingcap/tiflow/issues/1259) [＃2424](https://github.com/pingcap/tiflow/issues/2424)
        -   CLI の下位互換性の問題を修正[＃2373](https://github.com/pingcap/tiflow/issues/2373)
        -   `SinkManager` のマップへの安全でない同時アクセスの問題を修正 [＃2299](https://github.com/pingcap/tiflow/pull/2299)
        -   DDL ステートメント実行時にオーナーがクラッシュした場合に、潜在的な DDL 損失が発生する問題を修正しました。 [＃1260](https://github.com/pingcap/tiflow/issues/1260)
        -   リージョン初期化直後にロックが解決される問題を修正 [＃2188](https://github.com/pingcap/tiflow/issues/2188)
        -   新しいパーティションテーブルを追加するときに発生する余分なパーティションディスパッチの問題を修正しました。 [＃2263](https://github.com/pingcap/tiflow/pull/2263)
        -   削除された変更フィードについて TiCDC が警告し続ける問題を修正しました [＃2156](https://github.com/pingcap/tiflow/issues/2156)
