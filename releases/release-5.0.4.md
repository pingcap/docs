---
title: TiDB 5.0.4 Release Notes
---

# TiDB 5.0.4 リリースノート {#tidb-5-0-4-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 5.0.4

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   新しいセッションで`SHOW VARIABLES`を実行すると遅いという問題を修正します。この修正により、 [#19341](https://github.com/pingcap/tidb/pull/19341)で行われた一部の変更が元に戻されるため、互換性の問題が発生する可能性があります。 [#24326](https://github.com/pingcap/tidb/issues/24326)
    -   `tidb_stmt_summary_max_stmt_count`変数のデフォルト値を`200`から`3000`に変更します[#25873](https://github.com/pingcap/tidb/pull/25873)

    <!---->

    -   次のバグ修正により実行結果が変更され、アップグレードの非互換性が発生する可能性があります。
        -   `UNION`の子に`NULL`値[#26559](https://github.com/pingcap/tidb/issues/26559)含まれる場合に TiDB が間違った結果を返す問題を修正
        -   `greatest(datetime) union null`が空の文字列[#26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正
        -   `last_day`関数の動作が SQL モード[#26000](https://github.com/pingcap/tidb/pull/26000)で互換性がない問題を修正
        -   `having`句が正しく動作しない場合がある問題を修正[#26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の前後の照合順序が異なる場合に発生する間違った実行結果を修正します[#27146](https://github.com/pingcap/tidb/issues/27146)
        -   `group_concat`関数の列に非ビン照合順序がある場合に発生する間違った実行結果を修正します[#27429](https://github.com/pingcap/tidb/issues/27429)
        -   新しい照合順序が有効になっている場合に、複数の列で`count(distinct)`式を使用すると間違った結果が返される問題を修正します[#27091](https://github.com/pingcap/tidb/issues/27091)
        -   `extract`関数の引数が負の持続時間の場合に発生する結果が間違っていたのを修正[#27236](https://github.com/pingcap/tidb/issues/27236)
        -   `SQL_MODE`が &#39;STRICT_TRANS_TABLES&#39; [#26762](https://github.com/pingcap/tidb/issues/26762)の場合、無効な日付を挿入してもエラーが報告されない問題を修正します。
        -   `SQL_MODE`が &#39;NO_ZERO_IN_DATE&#39; [#26766](https://github.com/pingcap/tidb/issues/26766)の場合、無効なデフォルト日付を使用してもエラーが報告されない問題を修正します。
        -   プレフィックスインデックス[#26029](https://github.com/pingcap/tidb/issues/26029)のクエリ範囲のバグを修正
        -   `LOAD DATA`ステートメントが非 utf8 データを異常にインポートする可能性がある問題を修正します[#25979](https://github.com/pingcap/tidb/issues/25979)
        -   セカンダリ インデックスに主キー[#25809](https://github.com/pingcap/tidb/issues/25809)と同じ列がある場合、 `insert ignore on duplicate update`で間違ったデータが挿入される可能性がある問題を修正します。
        -   パーティションテーブルにクラスタード インデックスがある場合、 `insert ignore duplicate update`間違ったデータを挿入する可能性がある問題を修正します[#25846](https://github.com/pingcap/tidb/issues/25846)
        -   ポイント取得、バッチポイント取得[#24562](https://github.com/pingcap/tidb/issues/24562)においてキーが`ENUM`型の場合、クエリ結果が不正になる場合がある問題を修正
        -   `BIT`型の値を[#23479](https://github.com/pingcap/tidb/issues/23479)で除算するときに発生する間違った結果を修正
        -   `prepared`ステートメントと直接クエリの結果が一致しない可能性がある問題を修正します[#22949](https://github.com/pingcap/tidb/issues/22949)
        -   `YEAR`型を文字列または整数型[#23262](https://github.com/pingcap/tidb/issues/23262)と比較すると、クエリ結果が間違っている場合がある問題を修正

## 機能強化 {#feature-enhancements}

-   TiDB

    -   オプティマイザの推定を無視し、強制的に MPP モード[#26382](https://github.com/pingcap/tidb/pull/26382)を使用する設定`tidb_enforce_mpp=1`をサポートします。

-   TiKV

    -   TiCDC 構成の動的変更のサポート[#10645](https://github.com/tikv/tikv/issues/10645)

-   PD

    -   TiDB ダッシュボード[#3884](https://github.com/tikv/pd/pull/3884)に OIDC ベースの SSO サポートを追加

-   TiFlash

    -   DAG リクエストで`HAVING()`関数をサポートする
    -   `DATE()`機能をサポート
    -   インスタンスごとの書き込みスループットのために Grafana パネルを追加します

## 改善点 {#improvements}

-   TiDB

    -   ヒストグラムの行数に基づいて自動分析をトリガーする[#24237](https://github.com/pingcap/tidb/issues/24237)
    -   ノードに障害が発生し、 [#26757](https://github.com/pingcap/tidb/pull/26757)より前に再起動した場合は、 TiFlashノードへのリクエストの送信を一定期間停止します。
    -   `split region`の上限を増やして`split table`と`presplit`をより安定させます[#26657](https://github.com/pingcap/tidb/pull/26657)
    -   MPP クエリの再試行をサポート[#26483](https://github.com/pingcap/tidb/pull/26483)
    -   MPP クエリを起動する前にTiFlashが利用可能かどうかを確認する[#1807](https://github.com/pingcap/tics/issues/1807)
    -   安定した結果モードをサポートして、クエリ結果をより安定させます[#26084](https://github.com/pingcap/tidb/pull/26084)
    -   MySQL システム変数`init_connect`とそれに関連する機能[#18894](https://github.com/pingcap/tidb/issues/18894)をサポートします。
    -   `COUNT(DISTINCT)` MPPモードのアグリゲーション機能を徹底的に突き詰める[#25861](https://github.com/pingcap/tidb/pull/25861)
    -   集計関数を`EXPLAIN`ステートメントでプッシュダウンできない場合にログ警告を出力する[#25736](https://github.com/pingcap/tidb/pull/25736)
    -   Grafana ダッシュボード[#25327](https://github.com/pingcap/tidb/pull/25327)に`TiFlashQueryTotalCounter`エラー ラベルを追加します
    -   HTTP API [#24209](https://github.com/pingcap/tidb/issues/24209)によるセカンダリ インデックスを介したクラスター化インデックス テーブルの MVCC データの取得をサポートします。
    -   パーサー[#24371](https://github.com/pingcap/tidb/pull/24371)の`prepared`ステートメントのメモリ割り当てを最適化します。

-   TiKV

    -   読み取りレイテンシー[#10475](https://github.com/tikv/tikv/issues/10475)を短縮するために、読み取り準備完了と書き込み準備完了を個別に処理します。
    -   解決済み TS メッセージのサイズを削減して、ネットワーク帯域幅を節約します[#2448](https://github.com/pingcap/tiflow/issues/2448)
    -   スロガー スレッドが過負荷になってキューがいっぱいになった場合、スレッドをブロックする代わりにログを削除します[#10841](https://github.com/tikv/tikv/issues/10841)
    -   TiKV コプロセッサーの低速ログでは、リクエストの処理に費やした時間のみを考慮するようにします[#10841](https://github.com/tikv/tikv/issues/10841)
    -   未確定エラーの可能性を減らすために、事前書き込みを可能な限り冪等にする[#10587](https://github.com/tikv/tikv/pull/10587)
    -   書き込みフローが低い場合の誤った「GC が機能しません」アラートを回避します[#10662](https://github.com/tikv/tikv/pull/10662)
    -   復元するデータベースは、バックアップ中に常に元のクラスター サイズと一致するようにします。 [#10643](https://github.com/tikv/tikv/pull/10643)
    -   panic出力がログ[#9955](https://github.com/tikv/tikv/pull/9955)にフラッシュされていることを確認します。

-   PD

    -   PD 間のリージョン情報の同期パフォーマンスを向上[#3993](https://github.com/tikv/pd/pull/3993)

-   ツール

    -   Dumpling

        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`または`SHOW CREATE TABLE`構文をサポートしない MySQL 互換データベースのバックアップのサポート[#309](https://github.com/pingcap/dumpling/issues/309)

    -   TiCDC

        -   統合ソーターがソートにメモリを使用している場合のメモリ管理を最適化する[#2553](https://github.com/pingcap/tiflow/issues/2553)
        -   メジャー バージョンまたはマイナー バージョンにまたがる TiCDC クラスターの操作を禁止する[#2598](https://github.com/pingcap/tiflow/pull/2598)
        -   テーブルのリージョンがすべて TiKV ノードから転送される場合の goroutine の使用量を削減します[#2284](https://github.com/pingcap/tiflow/issues/2284)
        -   `file sorter` [#2326](https://github.com/pingcap/tiflow/pull/2326)を削除
        -   常に TiKV から古い値を取得し、出力は`enable-old-value` [#2301](https://github.com/pingcap/tiflow/issues/2301)に従って調整されます。
        -   PD エンドポイントに証明書がない場合に返されるエラー メッセージを改善します[#1973](https://github.com/pingcap/tiflow/issues/1973)
        -   同時実行性が高い場合、ゴルーチンを減らすためにワーカープールを最適化する[#2211](https://github.com/pingcap/tiflow/issues/2211)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[#2533](https://github.com/pingcap/tiflow/pull/2533)

## バグの修正 {#bug-fixes}

-   TiDB

    -   パーティションテーブルにpanicを実行し、パーティション キーに`IS NULL`条件[#23802](https://github.com/pingcap/tidb/issues/23802)あるときに TiDB がパニックになる可能性がある問題を修正します。
    -   `FLOAT64`種のオーバーフローチェックが[#23897](https://github.com/pingcap/tidb/issues/23897)と異なる問題を修正
    -   `case when`式[#26662](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序を修正します。
    -   悲観的トランザクションをコミットすると書き込み競合が発生する可能性がある問題を修正します[#25964](https://github.com/pingcap/tidb/issues/25964)
    -   悲観的トランザクションのインデックスキーが繰り返しコミットされる可能性があるバグを修正[#26359](https://github.com/pingcap/tidb/issues/26359) [#10600](https://github.com/tikv/tikv/pull/10600)
    -   非同期コミット ロックを解決するときに TiDB がpanicになる可能性がある問題を修正します[#25778](https://github.com/pingcap/tidb/issues/25778)
    -   `INDEX MERGE` [#25045](https://github.com/pingcap/tidb/issues/25045)を使用すると列が見つからない場合があるバグを修正
    -   `ALTER USER REQUIRE SSL`がユーザーの`authentication_string` [#25225](https://github.com/pingcap/tidb/issues/25225)をクリアしてしまうバグを修正
    -   新しいクラスター上の`tidb_gc_scan_lock_mode`グローバル変数の値が、実際のデフォルト モード「LEGACY」ではなく「PHYSICAL」と表示されるバグを修正します[#25100](https://github.com/pingcap/tidb/issues/25100)
    -   `TIKV_REGION_PEERS`システムテーブルが正しいステータスを表示しないバグを修正`DOWN` [#24879](https://github.com/pingcap/tidb/issues/24879)
    -   HTTP API使用時に発生するメモリリークの問題を修正[#24649](https://github.com/pingcap/tidb/pull/24649)
    -   ビューが`DEFINER` [#24414](https://github.com/pingcap/tidb/issues/24414)をサポートしていない問題を修正
    -   `tidb-server --help`がコード`2` [#24046](https://github.com/pingcap/tidb/issues/24046)で終了する問題を修正
    -   グローバル変数`dml_batch_size`の設定が反映されない問題を修正[#24709](https://github.com/pingcap/tidb/issues/24709)
    -   `read_from_storage`とパーティションテーブルを同時に使用するとエラー[#20372](https://github.com/pingcap/tidb/issues/20372)が発生する問題を修正
    -   射影演算子[#24264](https://github.com/pingcap/tidb/issues/24264)の実行時に TiDB がパニックになる問題を修正
    -   統計によりクエリがpanicになる可能性がある問題を修正します[#24061](https://github.com/pingcap/tidb/pull/24061)
    -   `BIT`列で`approx_percentile`関数を使用するとpanic[#23662](https://github.com/pingcap/tidb/issues/23662)が発生する可能性がある問題を修正
    -   Grafana の**コプロセッサーキャッシュ**パネルのメトリクスが間違っている問題を修正します[#26338](https://github.com/pingcap/tidb/issues/26338)
    -   同じパーティションを同時に切り詰めると DDL ステートメントがスタックする問題を修正します[#26229](https://github.com/pingcap/tidb/issues/26229)
    -   セッション変数が`GROUP BY`項目[#27106](https://github.com/pingcap/tidb/issues/27106)として使用されている場合に、間違ったクエリ結果が発生する問題を修正します。
    -   テーブル[#25902](https://github.com/pingcap/tidb/issues/25902)を結合するときの`VARCHAR`とタイムスタンプの間の誤った暗黙的な変換を修正しました。
    -   関連するサブクエリ ステートメントの誤った結果を修正します[#27233](https://github.com/pingcap/tidb/issues/27233)

-   TiKV

    -   破損したスナップショット ファイルによって引き起こされる潜在的なディスク フルの問題を修正します[#10813](https://github.com/tikv/tikv/issues/10813)
    -   Titan が有効になっている 5.0 より前のバージョンからアップグレードするときに発生する TiKVpanicの問題を修正します[#10843](https://github.com/tikv/tikv/pull/10843)
    -   新しいバージョンの TiKV を v5.0.x にロールバックできない問題を修正します[#10843](https://github.com/tikv/tikv/pull/10843)
    -   5.0 より前のバージョンから 5.0 以降のバージョンにアップグレードするときに発生する TiKVpanicの問題を修正します。アップグレード前に Titan を有効にしてクラスターを TiKV v3.x からアップグレードした場合、このクラスターで問題が発生する可能性があります。 [#10774](https://github.com/tikv/tikv/issues/10774)
    -   左側の悲観的ロック[#26404](https://github.com/pingcap/tidb/issues/26404)によって引き起こされる解析エラーを修正します。
    -   特定のプラットフォームで期間を計算するときに発生するpanicを修正しました[#10571](https://github.com/tikv/tikv/pull/10571)
    -   Load Base Split の`batch_get_command`のキーがエンコードされていない問題を修正[#10542](https://github.com/tikv/tikv/issues/10542)

-   PD

    -   PD がダウンしたピアを時間内に修復しない問題を修正します[#4077](https://github.com/tikv/pd/issues/4077)
    -   デフォルトの配置ルールのレプリカ数が`replication.max-replicas`が更新された後も一定になる問題を修正[#3886](https://github.com/tikv/pd/issues/3886)
    -   TiKV [#3868](https://github.com/tikv/pd/issues/3868)をスケールアウトするときに PD がpanicになる可能性があるバグを修正
    -   複数のスケジューラが同時に実行されている場合に発生するスケジュールの競合の問題を修正します[#3807](https://github.com/tikv/pd/issues/3807)
    -   スケジューラーを削除しても再度表示される場合がある問題を修正[#2572](https://github.com/tikv/pd/issues/2572)

-   TiFlash

    -   テーブルスキャンタスクの実行時に発生する潜在的なpanicの問題を修正
    -   MPP タスクの実行時に発生する潜在的なメモリリークの問題を修正
    -   DAQ リクエストを処理するときにTiFlashが`duplicated region`エラーを発生させるバグを修正
    -   集計関数`COUNT`または`COUNT DISTINCT`を実行すると予期しない結果が発生する問題を修正
    -   MPP タスクの実行時に発生する潜在的なpanicの問題を修正します。
    -   複数のディスクに展開されている場合にTiFlash がデータを復元できないという潜在的なバグを修正
    -   `SharedQueryBlockInputStream`を分解するときに発生する潜在的なpanicの問題を修正
    -   `MPPTask`を分解するときに発生する潜在的なpanicの問題を修正
    -   TiFlash がMPP 接続の確立に失敗した場合に予期しない結果が発生する問題を修正
    -   ロックを解決するときに発生する潜在的なpanicの問題を修正します。
    -   大量の書き込み時にメトリクスのストア サイズが不正確になる問題を修正
    -   クエリに`CONSTANT` 、 `<` 、 `<=` 、 `>` 、 `>=` 、または`COLUMN`などのフィルターが含まれている場合に発生する誤った結果のバグを修正しました。
    -   TiFlash が長時間実行した後にデルタ データをガベージ コレクションできないという潜在的な問題を修正
    -   メトリクスに間違った値が表示される潜在的なバグを修正
    -   TiFlash が複数のディスクに展開されている場合に発生するデータの不整合の潜在的な問題を修正

-   ツール

    -   Dumpling

        -   MySQL 8.0.3 以降のバージョン[#322](https://github.com/pingcap/dumpling/issues/322)で`show table status`の実行が停止する問題を修正

    -   TiCDC

        -   `mysql.TypeString, mysql.TypeVarString, mysql.TypeVarchar`などのデータ型を JSON [#2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードするときに発生するプロセスpanicの問題を修正
        -   このテーブルが再スケジュールされているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるために発生するデータの不整合の問題を修正します[#2417](https://github.com/pingcap/tiflow/pull/2417)
        -   TiCDC がキャプチャするリージョン[#2724](https://github.com/pingcap/tiflow/pull/2724)が多すぎるときに発生する OOM を回避するには、gRPC ウィンドウ サイズを小さくします。
        -   メモリ負荷が高い場合に gRPC 接続が頻繁に切断されるエラーを修正[#2202](https://github.com/pingcap/tiflow/issues/2202)
        -   TiCDC が unsigned `TINYINT` type [#2648](https://github.com/pingcap/tiflow/issues/2648)でpanicを引き起こすバグを修正しました。
        -   上流[#2612](https://github.com/pingcap/tiflow/issues/2612)でトランザクションを挿入し、同じ行のデータを削除すると、TiCDC オープン プロトコルが空の値を出力する問題を修正します。
        -   スキーマ変更[#2603](https://github.com/pingcap/tiflow/issues/2603)の終了TSでチェンジフィードが開始されるとDDL処理が失敗するバグを修正
        -   応答のないダウンストリームが、タスクがタイムアウトするまで古い所有者のレプリケーション タスクを中断する問題を修正します[#2295](https://github.com/pingcap/tiflow/issues/2295)
        -   メタデータ管理のバグを修正[#2558](https://github.com/pingcap/tiflow/pull/2558)
        -   TiCDC 所有者切り替え後に発生するデータの不整合の問題を修正[#2230](https://github.com/pingcap/tiflow/issues/2230)
        -   `capture list`コマンド[#2388](https://github.com/pingcap/tiflow/issues/2388)の出力に古いキャプチャが表示されることがある問題を修正します。
        -   統合テスト[#2422](https://github.com/pingcap/tiflow/issues/2422)でDDLジョブの重複が発生した場合に発生するエラー`ErrSchemaStorageTableMiss`を修正
        -   `ErrGCTTLExceeded`エラーが発生するとチェンジフィードが削除できないバグを修正[#2391](https://github.com/pingcap/tiflow/issues/2391)
        -   大きなテーブルを cdclog に複製すると失敗するバグを修正[#1259](https://github.com/pingcap/tiflow/issues/1259) [#2424](https://github.com/pingcap/tiflow/issues/2424)
        -   CLI の下位互換性の問題[#2373](https://github.com/pingcap/tiflow/issues/2373)を修正する
        -   `SinkManager` [#2299](https://github.com/pingcap/tiflow/pull/2299)のマップへの安全でない同時アクセスの問題を修正
        -   DDL ステートメントの実行時に所有者がクラッシュした場合に DDL が失われる可能性がある問題を修正します[#1260](https://github.com/pingcap/tiflow/issues/1260)
        -   リージョンが初期化された直後にロックが解決される問題を修正[#2188](https://github.com/pingcap/tiflow/issues/2188)
        -   新しいパーティションテーブルを追加するときに発生する余分なパーティションディスパッチの問題を修正します[#2263](https://github.com/pingcap/tiflow/pull/2263)
        -   削除された変更フィードについて TiCDC が警告を出し続ける問題を修正[#2156](https://github.com/pingcap/tiflow/issues/2156)
