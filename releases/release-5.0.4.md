---
title: TiDB 5.0.4 Release Notes
---

# TiDB 5.0.4 リリースノート {#tidb-5-0-4-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 5.0.4

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   新しいセッションで`SHOW VARIABLES`を実行すると遅い問題を修正します。この修正により、 [#19341](https://github.com/pingcap/tidb/pull/19341)で行われた一部の変更が元に戻り、互換性の問題が発生する可能性があります。 [#24326](https://github.com/pingcap/tidb/issues/24326)
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から`3000` [#25873](https://github.com/pingcap/tidb/pull/25873)に変更します。

    <!---->

    -   次のバグ修正により実行結果が変更され、アップグレードの非互換性が生じる可能性があります。
        -   `UNION`の子に`NULL`値[#26559](https://github.com/pingcap/tidb/issues/26559)が含まれている場合、TiDB が間違った結果を返す問題を修正します。
        -   `greatest(datetime) union null`が空の文字列[#26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正
        -   `last_day`関数の動作が SQL モード[#26000](https://github.com/pingcap/tidb/pull/26000)で互換性がない問題を修正
        -   `having`節が正しく動作しない場合がある問題を修正[#26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の前後の照合が異なる場合に発生する誤った実行結果を修正します[#27146](https://github.com/pingcap/tidb/issues/27146)
        -   `group_concat`関数の列に非ビン照合順序がある場合に発生する誤った実行結果を修正します[#27429](https://github.com/pingcap/tidb/issues/27429)
        -   新しい照合順序が有効になっている場合、複数の列で`count(distinct)`式を使用すると間違った結果が返される問題を修正します[#27091](https://github.com/pingcap/tidb/issues/27091)
        -   `extract`関数の引数が負の期間[#27236](https://github.com/pingcap/tidb/issues/27236)の場合に発生する結果の誤りを修正します。
        -   `SQL_MODE`が &#39;STRICT_TRANS_TABLES&#39; [#26762](https://github.com/pingcap/tidb/issues/26762)の場合、無効な日付を挿入してもエラーが報告されない問題を修正します。
        -   `SQL_MODE`が &#39;NO_ZERO_IN_DATE&#39; [#26766](https://github.com/pingcap/tidb/issues/26766)の場合、無効なデフォルト日付を使用してもエラーが報告されない問題を修正します。
        -   プレフィックス インデックス[#26029](https://github.com/pingcap/tidb/issues/26029)のクエリ範囲のバグを修正
        -   `LOAD DATA`ステートメントが utf8 以外のデータを異常にインポートする可能性がある問題を修正します[#25979](https://github.com/pingcap/tidb/issues/25979)
        -   副次索引に主キーと同じ列がある場合、 `insert ignore on duplicate update`誤ったデータを挿入する可能性がある問題を修正します[#25809](https://github.com/pingcap/tidb/issues/25809)
        -   パーティションテーブルにクラスター化されたインデックスがある場合に間違ったデータが挿入される可能性が`insert ignore duplicate update`問題を修正します[#25846](https://github.com/pingcap/tidb/issues/25846)
        -   ポイントgetやバッチポイント[#24562](https://github.com/pingcap/tidb/issues/24562)でキーが`ENUM`型の場合、クエリ結果がおかしくなることがある問題を修正
        -   `BIT`型の値[#23479](https://github.com/pingcap/tidb/issues/23479)を除算するときに発生する誤った結果を修正します。
        -   `prepared`ステートメントと直接クエリの結果が一致しない可能性がある問題を修正します[#22949](https://github.com/pingcap/tidb/issues/22949)
        -   `YEAR`型を文字列または整数型と比較すると、クエリの結果が正しくない場合がある問題を修正[#23262](https://github.com/pingcap/tidb/issues/23262)

## 機能強化 {#feature-enhancements}

-   TiDB

    -   オプティマイザの推定を無視して強制的に MPP モード[#26382](https://github.com/pingcap/tidb/pull/26382)を使用する設定`tidb_enforce_mpp=1`をサポート

-   TiKV

    -   TiCDC 構成の動的変更をサポート[#10645](https://github.com/tikv/tikv/issues/10645)

-   PD

    -   TiDB ダッシュボード[#3884](https://github.com/tikv/pd/pull/3884)に OIDC ベースの SSO サポートを追加

-   TiFlash

    -   DAG リクエストで`HAVING()`機能をサポート
    -   `DATE()`機能をサポート
    -   インスタンスごとの書き込みスループット用に Grafana パネルを追加する

## 改良点 {#improvements}

-   TiDB

    -   ヒストグラムの行数に基づいて自動分析をトリガーする[#24237](https://github.com/pingcap/tidb/issues/24237)
    -   ノードに障害が発生して[#26757](https://github.com/pingcap/tidb/pull/26757)前に再起動した場合、 TiFlashノードへのリクエストの送信を一定期間停止します。
    -   `split region`の上限を増やして`split table`と`presplit`をより安定させる[#26657](https://github.com/pingcap/tidb/pull/26657)
    -   MPP クエリの再試行のサポート[#26483](https://github.com/pingcap/tidb/pull/26483)
    -   MPP クエリを起動する前に、 TiFlashの可用性を確認してください[#1807](https://github.com/pingcap/tics/issues/1807)
    -   安定した結果モードをサポートして、クエリ結果をより安定させます[#26084](https://github.com/pingcap/tidb/pull/26084)
    -   MySQL システム変数`init_connect`とそれに関連する機能[#18894](https://github.com/pingcap/tidb/issues/18894)サポート
    -   `COUNT(DISTINCT)` MPPモードの集計機能を徹底的に押し下げる[#25861](https://github.com/pingcap/tidb/pull/25861)
    -   集計関数を`EXPLAIN`ステートメントでプッシュダウンできない場合にログ警告を出力する[#25736](https://github.com/pingcap/tidb/pull/25736)
    -   Grafana ダッシュボード[#25327](https://github.com/pingcap/tidb/pull/25327)に`TiFlashQueryTotalCounter`エラー ラベルを追加する
    -   HTTP API [#24209](https://github.com/pingcap/tidb/issues/24209)によるセカンダリ インデックスを介したクラスター化インデックス テーブルの MVCC データの取得のサポート
    -   パーサー[#24371](https://github.com/pingcap/tidb/pull/24371)で`prepared`ステートメントのメモリ割り当てを最適化する

-   TiKV

    -   読み取りレイテンシーを短縮するために、読み取り準備完了と書き込み準備完了を別々に処理する[#10475](https://github.com/tikv/tikv/issues/10475)
    -   解決済み TS メッセージのサイズを縮小してネットワーク帯域幅を節約する[#2448](https://github.com/pingcap/tiflow/issues/2448)
    -   slogger スレッドが過負荷になり、キューがいっぱいになったときに、スレッドをブロックする代わりにログを削除します[#10841](https://github.com/tikv/tikv/issues/10841)
    -   TiKV コプロセッサーのスローログを、リクエストの処理に費やされた時間のみを考慮するようにします[#10841](https://github.com/tikv/tikv/issues/10841)
    -   事前書き込みを可能な限り冪等にして、未確定エラーの可能性を減らします[#10587](https://github.com/tikv/tikv/pull/10587)
    -   低い書き込みフロー[#10662](https://github.com/tikv/tikv/pull/10662)で誤った「GC can not work」アラートを回避する
    -   復元するデータベースは、バックアップ中に常に元のクラスター サイズと一致するようにします。 [#10643](https://github.com/tikv/tikv/pull/10643)
    -   panic出力がログ[#9955](https://github.com/tikv/tikv/pull/9955)にフラッシュされることを確認します。

-   PD

    -   PD 間のリージョン情報の同期のパフォーマンスを向上させます[#3993](https://github.com/tikv/pd/pull/3993)

-   ツール

    -   Dumpling

        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`構文をサポートしていない MySQL 互換データベースのバックアップのサポート[#309](https://github.com/pingcap/dumpling/issues/309)

    -   TiCDC

        -   ユニファイド ソーターが並べ替えにメモリを使用している場合のメモリ管理を最適化します[#2553](https://github.com/pingcap/tiflow/issues/2553)
        -   メジャーまたはマイナー バージョン間での TiCDC クラスターの動作を禁止する[#2598](https://github.com/pingcap/tiflow/pull/2598)
        -   テーブルのリージョンがすべて TiKV ノードから転送されるときのゴルーチンの使用量を減らします[#2284](https://github.com/pingcap/tiflow/issues/2284)
        -   削除`file sorter` [#2326](https://github.com/pingcap/tiflow/pull/2326)
        -   常に TiKV から古い値を引き出し、出力は`enable-old-value` [#2301](https://github.com/pingcap/tiflow/issues/2301)に従って調整されます
        -   PD エンドポイントで証明書が見つからない場合に返されるエラー メッセージを改善します[#1973](https://github.com/pingcap/tiflow/issues/1973)
        -   同時実行性が高い場合、より少ないゴルーチンのためにワーカープールを最適化します[#2211](https://github.com/pingcap/tiflow/issues/2211)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[#2533](https://github.com/pingcap/tiflow/pull/2533)

## バグの修正 {#bug-fixes}

-   TiDB

    -   パーティションテーブルにpanicを実行し、パーティション キーの条件が`IS NULL` [#23802](https://github.com/pingcap/tidb/issues/23802)の場合に TiDB がパニックになる可能性がある問題を修正します。
    -   `FLOAT64`型のオーバーフローチェックがMySQL [#23897](https://github.com/pingcap/tidb/issues/23897)と異なる問題を修正
    -   `case when`式[#26662](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序を修正します
    -   悲観的トランザクションをコミットすると書き込み競合が発生する可能性があるという問題を修正します[#25964](https://github.com/pingcap/tidb/issues/25964)
    -   悲観的トランザクションのインデックス キーが繰り返しコミットされる可能性があるバグを修正[#26359](https://github.com/pingcap/tidb/issues/26359) [#10600](https://github.com/tikv/tikv/pull/10600)
    -   非同期コミット ロックを解決するときに TiDB がpanicになる可能性がある問題を修正します[#25778](https://github.com/pingcap/tidb/issues/25778)
    -   `INDEX MERGE` [#25045](https://github.com/pingcap/tidb/issues/25045)使用時に列が見つからないことがあるバグを修正
    -   ユーザーの`authentication_string` [#25225](https://github.com/pingcap/tidb/issues/25225)を`ALTER USER REQUIRE SSL`クリアしてしまう不具合を修正
    -   新しいクラスタの`tidb_gc_scan_lock_mode`グローバル変数の値が、実際のデフォルト モード「LEGACY」ではなく「PHYSICAL」を示すバグを修正します[#25100](https://github.com/pingcap/tidb/issues/25100)
    -   `TIKV_REGION_PEERS`システムテーブルが正しい`DOWN`ステータスを表示しないバグを修正[#24879](https://github.com/pingcap/tidb/issues/24879)
    -   HTTP API 使用時にメモリリークが発生する問題を修正[#24649](https://github.com/pingcap/tidb/pull/24649)
    -   ビューが`DEFINER` [#24414](https://github.com/pingcap/tidb/issues/24414)をサポートしていない問題を修正
    -   `tidb-server --help`がコード`2` [#24046](https://github.com/pingcap/tidb/issues/24046)で終了する問題を修正
    -   グローバル変数`dml_batch_size`の設定が反映されない問題を修正[#24709](https://github.com/pingcap/tidb/issues/24709)
    -   `read_from_storage`とパーティションテーブルを同時に使用するとエラー[#20372](https://github.com/pingcap/tidb/issues/20372)が発生する問題を修正
    -   射影演算子[#24264](https://github.com/pingcap/tidb/issues/24264)を実行すると TiDB がパニックになる問題を修正
    -   統計がpanicのパニックを引き起こす可能性がある問題を修正します[#24061](https://github.com/pingcap/tidb/pull/24061)
    -   `BIT`列で`approx_percentile`関数を使用するとpanic[#23662](https://github.com/pingcap/tidb/issues/23662)が発生する可能性がある問題を修正します。
    -   Grafana の**コプロセッサー Cache**パネルのメトリックが間違っている問題を修正します[#26338](https://github.com/pingcap/tidb/issues/26338)
    -   同じパーティションを同時に切り捨てると DDL ステートメントがスタックする問題を修正します[#26229](https://github.com/pingcap/tidb/issues/26229)
    -   `GROUP BY`項目[#27106](https://github.com/pingcap/tidb/issues/27106)にセッション変数を使用した場合に発生する、誤ったクエリ結果の問題を修正します。
    -   テーブルを結合するときの`VARCHAR`とタイムスタンプの間の間違った暗黙的な変換を修正します[#25902](https://github.com/pingcap/tidb/issues/25902)
    -   関連付けられたサブクエリ ステートメントの間違った結果を修正する[#27233](https://github.com/pingcap/tidb/issues/27233)

-   TiKV

    -   破損したスナップショット ファイルが原因で発生する可能性のあるディスクがいっぱいになる問題を修正します[#10813](https://github.com/tikv/tikv/issues/10813)
    -   Titan を有効にして 5.0 より前のバージョンからアップグレードするときに発生する TiKVpanicの問題を修正します[#10843](https://github.com/tikv/tikv/pull/10843)
    -   新しいバージョンの TiKV が v5.0.x にロールバックできない問題を修正[#10843](https://github.com/tikv/tikv/pull/10843)
    -   5.0 より前のバージョンから 5.0 以降のバージョンにアップグレードするときに発生する TiKVpanicの問題を修正します。アップグレード前に Titan を有効にしてクラスターを TiKV v3.x からアップグレードした場合、このクラスターで問題が発生する可能性があります。 [#10774](https://github.com/tikv/tikv/issues/10774)
    -   左悲観的ロックによる解析エラーを修正[#26404](https://github.com/pingcap/tidb/issues/26404)
    -   特定のプラットフォームで期間を計算するときに発生するpanicを修正します[#10571](https://github.com/tikv/tikv/pull/10571)
    -   Load Base Split の`batch_get_command`のキーがエンコードされていない問題を修正[#10542](https://github.com/tikv/tikv/issues/10542)

-   PD

    -   PD が時間[#4077](https://github.com/tikv/pd/issues/4077)でダウンしたピアを修正しない問題を修正します。
    -   `replication.max-replicas`が更新された後、デフォルトの配置ルールのレプリカ数が一定のままになる問題を修正します[#3886](https://github.com/tikv/pd/issues/3886)
    -   TiKV [#3868](https://github.com/tikv/pd/issues/3868)をスケールアウトすると PD がpanicになることがあるバグを修正
    -   複数のスケジューラが同時に実行されている場合に発生するスケジュールの競合の問題を修正します[#3807](https://github.com/tikv/pd/issues/3807)
    -   スケジューラーを削除しても再度表示されることがある問題を修正[#2572](https://github.com/tikv/pd/issues/2572)

-   TiFlash

    -   テーブル スキャン タスクの実行時に発生する潜在的なpanicの問題を修正します。
    -   MPP タスクの実行時に発生する潜在的なメモリリークの問題を修正します。
    -   DAQ リクエストの処理時にTiFlashが`duplicated region`エラーを発生させるバグを修正
    -   集計関数`COUNT`または`COUNT DISTINCT`を実行したときに予期しない結果が生じる問題を修正
    -   MPP タスクの実行時に発生する潜在的なpanicの問題を修正します
    -   複数のディスクに展開されたときにTiFlash がデータを復元できないという潜在的なバグを修正します
    -   分解時に発生する潜在的なpanicの問題を修正します`SharedQueryBlockInputStream`
    -   分解時に発生する潜在的なpanicの問題を修正します`MPPTask`
    -   TiFlash がMPP 接続の確立に失敗したときの予期しない結果の問題を修正
    -   ロックを解決するときに発生する潜在的なpanicの問題を修正します
    -   負荷の高い書き込みでメトリクスのストア サイズが不正確になる問題を修正
    -   クエリに`CONSTANT` 、 `<` 、 `<=` 、 `>` 、 `>=` 、または`COLUMN`などのフィルターが含まれている場合に発生する誤った結果のバグを修正します
    -   長時間実行した後、 TiFlash がデルタ データをガベージ コレクションできないという潜在的な問題を修正します。
    -   メトリクスが間違った値を表示する潜在的なバグを修正
    -   TiFlash が複数のディスクに展開されている場合に発生する可能性のあるデータの不整合の問題を修正します。

-   ツール

    -   Dumpling

        -   MySQL 8.0.3 以降で`show table status`の実行がスタックする問題を修正[#322](https://github.com/pingcap/dumpling/issues/322)

    -   TiCDC

        -   `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar`などのデータ型を JSON にエンコードする際にプロセスpanicが発生する問題を修正[#2758](https://github.com/pingcap/tiflow/issues/2758)
        -   このテーブルが再スケジュールされているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるために発生するデータの不整合の問題を修正します[#2417](https://github.com/pingcap/tiflow/pull/2417)
        -   TiCDC がキャプチャするリージョンが多すぎる場合に発生する OOM を回避するために、gRPC ウィンドウ サイズを小さくします[#2724](https://github.com/pingcap/tiflow/pull/2724)
        -   メモリプレッシャが高い場合に gRPC 接続が頻繁に切断されるエラーを修正します[#2202](https://github.com/pingcap/tiflow/issues/2202)
        -   unsigned `TINYINT` type [#2648](https://github.com/pingcap/tiflow/issues/2648)で TiCDC がpanicになるバグを修正
        -   アップストリーム[#2612](https://github.com/pingcap/tiflow/issues/2612)でトランザクションを挿入し、同じ行のデータを削除すると、TiCDC Open Protocol が空の値を出力する問題を修正します。
        -   スキーマ変更[#2603](https://github.com/pingcap/tiflow/issues/2603)の終了 TS で変更フィードが開始されると、DDL 処理が失敗するバグを修正します。
        -   タスクがタイムアウトするまで、無応答のダウンストリームが古い所有者のレプリケーション タスクを中断する問題を修正します[#2295](https://github.com/pingcap/tiflow/issues/2295)
        -   メタデータ管理のバグを修正[#2558](https://github.com/pingcap/tiflow/pull/2558)
        -   TiCDC 所有者の切り替え後に発生するデータの不整合の問題を修正します[#2230](https://github.com/pingcap/tiflow/issues/2230)
        -   `capture list`コマンド[#2388](https://github.com/pingcap/tiflow/issues/2388)の出力に古いキャプチャが表示されることがある問題を修正します。
        -   統合テスト[#2422](https://github.com/pingcap/tiflow/issues/2422)で DDL ジョブの重複が発生した場合に発生する`ErrSchemaStorageTableMiss`エラーを修正します。
        -   `ErrGCTTLExceeded`エラーが発生するとチェンジフィードを削除できない不具合を修正[#2391](https://github.com/pingcap/tiflow/issues/2391)
        -   cdclog への大きなテーブルの複製が失敗するバグを修正[#1259](https://github.com/pingcap/tiflow/issues/1259) [#2424](https://github.com/pingcap/tiflow/issues/2424)
        -   CLI の下位互換性の問題を修正します[#2373](https://github.com/pingcap/tiflow/issues/2373)
        -   `SinkManager` [#2299](https://github.com/pingcap/tiflow/pull/2299)でマップへの安全でない同時アクセスの問題を修正
        -   DDL ステートメントの実行時に所有者がクラッシュすると、DDL が失われる可能性がある問題を修正します[#1260](https://github.com/pingcap/tiflow/issues/1260)
        -   リージョンが初期化された直後にロックが解除される問題を修正[#2188](https://github.com/pingcap/tiflow/issues/2188)
        -   新しいパーティションテーブルを追加するときに発生する余分なパーティション ディスパッチの問題を修正します[#2263](https://github.com/pingcap/tiflow/pull/2263)
        -   TiCDC が変更フィードを削除しても警告を発し続ける問題を修正[#2156](https://github.com/pingcap/tiflow/issues/2156)
