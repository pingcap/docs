---
title: TiDB 5.0.3 Release Notes
---

# TiDB5.0.3リリースノート {#tidb-5-0-3-release-notes}

発売日：2021年7月2日

TiDBバージョン：5.0.3

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   v4.0クラスタがv5.0以降のバージョン（devまたはv5.1）にアップグレードされると、 `tidb_multi_statement_mode`変数のデフォルト値が`WARN`から`OFF`に変更されます。
    -   TiDBは、MySQL5.7のnoop変数`innodb_default_row_format`と互換性があります。この変数を設定しても効果はありません。 [＃23541](https://github.com/pingcap/tidb/issues/23541)

## 機能の強化 {#feature-enhancements}

-   ツール

    -   TiCDC

        -   HTTP APIを追加して、ノード[＃1955](https://github.com/pingcap/tiflow/pull/1955)のチェンジフィード情報とヘルス情報を取得します。
        -   kafkaシンク[＃1942](https://github.com/pingcap/tiflow/pull/1942)のSASL/SCRAMサポートを追加します
        -   サーバーレベル[＃2070](https://github.com/pingcap/tiflow/pull/2070)でTiCDCサポート`--data-dir`を作成します

## 改善 {#improvements}

-   TiDB

    -   `TopN`人のオペレーターを[＃25162](https://github.com/pingcap/tidb/pull/25162)にプッシュダウンすることをサポート
    -   内蔵機能`json_unquote()`から[＃24415](https://github.com/pingcap/tidb/issues/24415)へのプッシュダウンをサポート
    -   デュアルテーブルからのユニオンブランチの削除をサポート[＃25614](https://github.com/pingcap/tidb/pull/25614)
    -   内蔵機能`replace()`から[＃25565](https://github.com/pingcap/tidb/pull/25565)へのプッシュダウンをサポート
    -   `datediff()` `datesub()` `unix_timestamp()` 、および`day()`を`concat()`に[＃25564](https://github.com/pingcap/tidb/pull/25564)ダウンすることを`concat_ws()`し`year()`
    -   骨材オペレーターのコストファクターを最適化する[＃25241](https://github.com/pingcap/tidb/pull/25241)
    -   `Limit`人のオペレーターを[＃25159](https://github.com/pingcap/tidb/pull/25159)にプッシュダウンすることをサポート
    -   内蔵機能`str_to_date`から[＃25148](https://github.com/pingcap/tidb/pull/25148)へのプッシュダウンをサポート
    -   MPP外部結合が、テーブルの行数[＃25142](https://github.com/pingcap/tidb/pull/25142)に基づいてビルドテーブルを選択できるようにします。
    -   組み込み関数`left()` 、および`right()`の`abs()`へのプッシュダウンを[＃25133](https://github.com/pingcap/tidb/pull/25133)
    -   ブロードキャストデカルト参加を[＃25106](https://github.com/pingcap/tidb/pull/25106)にプッシュダウンすることをサポート
    -   `Union All`人のオペレーターを[＃25051](https://github.com/pingcap/tidb/pull/25051)にプッシュダウンすることをサポート
    -   リージョン[＃24724](https://github.com/pingcap/tidb/pull/24724)に基づく異なるTiFlashノード間でのMPPクエリワークロードのバランス調整をサポート
    -   MPPクエリの実行後にキャッシュ内の古いリージョンを無効にすることをサポートします[＃24432](https://github.com/pingcap/tidb/pull/24432)
    -   フォーマット指定子[＃25767](https://github.com/pingcap/tidb/pull/25767)の組み込み関数`str_to_date`のMySQL互換性を改善し`%b/%M/%r/%T`

-   TiKV

    -   TiCDCシンクのメモリ消費を制限する[＃10305](https://github.com/tikv/tikv/pull/10305)
    -   TiCDCの古い値キャッシュのメモリ制限上限を追加します[＃10313](https://github.com/tikv/tikv/pull/10313)

-   PD

    -   TiDBダッシュボードをv2021.06.15.1に更新します[＃3798](https://github.com/pingcap/pd/pull/3798)

-   TiFlash

    -   `STRING`タイプから`DOUBLE`タイプへのキャストをサポート
    -   `STR_TO_DATE()`機能をサポート
    -   複数のスレッドを使用して、右外部結合で結合されていないデータを最適化します
    -   デカルト参加をサポートする
    -   `LEFT()`と`RIGHT()`の機能をサポート
    -   MPPクエリで古いリージョンを自動的に無効にすることをサポート
    -   `ABS()`機能をサポート

-   ツール

    -   TiCDC

        -   gRPCの再接続ロジックを改良し、KVクライアントのスループットを向上させます[＃1586](https://github.com/pingcap/tiflow/issues/1586) [＃1501](https://github.com/pingcap/tiflow/issues/1501#issuecomment-820027078) [＃1682](https://github.com/pingcap/tiflow/pull/1682) [＃1393](https://github.com/pingcap/tiflow/issues/1393) [＃1847](https://github.com/pingcap/tiflow/pull/1847) [＃1905](https://github.com/pingcap/tiflow/issues/1905) [＃1904](https://github.com/pingcap/tiflow/issues/1904)
        -   ソーターI/Oエラーをよりユーザーフレンドリーにします

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SET`型列[＃25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると誤った結果が返される問題を修正します。
    -   `IN`式の引数[＃25591](https://github.com/pingcap/tidb/issues/25591)のデータ破損の問題を修正します
    -   GCのセッションがグローバル変数の影響を受けないようにする[＃24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリ[＃25344](https://github.com/pingcap/tidb/issues/25344)で`limit`を使用するときに発生するパニックの問題を修正します
    -   `Limit`を使用してパーティションテーブルをクエリするときに返される誤った値を修正し[＃24636](https://github.com/pingcap/tidb/issues/24636)
    -   `IFNULL`が`ENUM`または`SET`タイプの列[＃24944](https://github.com/pingcap/tidb/issues/24944)で正しく有効にならない問題を修正します
    -   結合サブクエリの`count`を[＃24865](https://github.com/pingcap/tidb/issues/24865)に変更することによって引き起こされる間違った結果を修正し`first_row`
    -   `TopN`演算子[＃24930](https://github.com/pingcap/tidb/issues/24930)で`ParallelApply`を使用した場合に発生するクエリハングの問題を修正します。
    -   複数列のプレフィックスインデックスを使用してSQLステートメントを実行すると、予想よりも多くの結果が返される問題を修正します[＃24356](https://github.com/pingcap/tidb/issues/24356)
    -   `<=>`オペレーターが正しく有効にできない問題を修正します[＃24477](https://github.com/pingcap/tidb/issues/24477)
    -   パラレル`Apply`オペレーター[＃23280](https://github.com/pingcap/tidb/issues/23280)のデータ競合の問題を修正します
    -   PartitionUnionオペレーター[＃23919](https://github.com/pingcap/tidb/issues/23919)のIndexMerge結果をソートするときに`index out of range`エラーが報告される問題を修正します。
    -   `tidb_snapshot`変数を予想外に大きな値に設定すると、トランザクション分離が損なわれる可能性があるという問題を修正します[＃25680](https://github.com/pingcap/tidb/issues/25680)
    -   ODBCスタイルの定数（たとえば、 `{d '2020-01-01'}` ）を式[＃25531](https://github.com/pingcap/tidb/issues/25531)として使用できない問題を修正します。
    -   `SELECT DISTINCT`を`Batch Get`に変換すると誤った結果が発生する問題を修正します[＃25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashからTiKVへのクエリのバックオフをトリガーできない問題を修正し[＃24421](https://github.com/pingcap/tidb/issues/24421) [＃23665](https://github.com/pingcap/tidb/issues/23665)
    -   `only_full_group_by`をチェックするときに発生する`index-out-of-range`のエラーを修正します[＃23839](https://github.com/pingcap/tidb/issues/23839) ）
    -   相関サブクエリでのインデックス結合の結果が間違っている問題を修正します[＃25799](https://github.com/pingcap/tidb/issues/25799)

-   TiKV

    -   間違った`tikv_raftstore_hibernated_peer_state`メトリック[＃10330](https://github.com/tikv/tikv/issues/10330)を修正
    -   コプロセッサー[＃10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数タイプを修正してください
    -   場合によってはACIDの破損を回避するために、正常なシャットダウン中にコールバックのクリアをスキップします[＃10353](https://github.com/tikv/tikv/issues/10353) [＃10307](https://github.com/tikv/tikv/issues/10307)
    -   リーダー[＃10347](https://github.com/tikv/tikv/issues/10347)のレプリカ読み取りで読み取りインデックスが共有されるバグを修正します
    -   `DOUBLE`から[＃25200](https://github.com/pingcap/tidb/issues/25200)をキャストする間違った関数を修正し`DOUBLE`

-   PD

    -   スケジューラーの開始後にTTL構成をロードするときに発生するデータ競合の問題を修正します[＃3771](https://github.com/tikv/pd/issues/3771)
    -   [＃24293](https://github.com/pingcap/tidb/issues/24293)の`TIKV_REGION_PEERS`テーブルの`is_learner`フィールドが正しくないバグを修正し[＃3372](https://github.com/tikv/pd/issues/3372) 57
    -   ゾーン内のすべてのTiKVノードがオフラインまたはダウンしている場合、PDが他のゾーンへのレプリカをスケジュールしないという問題を修正します[＃3705](https://github.com/tikv/pd/issues/3705)
    -   スキャッターリージョンスケジューラが追加された後、PDがパニックになる可能性がある問題を修正します[＃3762](https://github.com/tikv/pd/pull/3762)

-   TiFlash

    -   分割の失敗が原因でTiFlashが再起動し続ける問題を修正します
    -   TiFlashがデルタデータを削除できないという潜在的な問題を修正します
    -   TiFlashが`CAST`関数の非バイナリ文字に間違ったパディングを追加するバグを修正します
    -   複雑な`GROUP BY`列の集計クエリを処理するときの誤った結果の問題を修正します
    -   書き込み圧力が高い場合に発生するTiFlashパニックの問題を修正します
    -   右のjonキーがnullalbeでなく、左のjoinキーがnull許容である場合に発生するパニックを修正します
    -   `read-index`のリクエストに時間がかかる可能性のある問題を修正します
    -   読み取り負荷が大きいときに発生するパニックの問題を修正します
    -   `Date_Format`の関数が`STRING`の型の引数と`NULL`の値で呼び出されたときに発生する可能性のあるパニックの問題を修正します

-   ツール

    -   TiCDC

        -   チェックポイント[＃1902](https://github.com/pingcap/tiflow/issues/1902)を更新するときにTiCDC所有者が終了する問題を修正します
        -   MySQLシンクがエラーに遭遇して一時停止した後に一部のMySQL接続がリークする可能性があるバグを修正します[＃1946](https://github.com/pingcap/tiflow/pull/1946)
        -   [＃2024](https://github.com/pingcap/tiflow/pull/2024)が13の読み取りに失敗したときに発生するパニックの問題を修正し`/proc/meminfo`
        -   [＃1958](https://github.com/pingcap/tiflow/pull/1958)のランタイムメモリ消費を削減する[＃2012](https://github.com/pingcap/tiflow/pull/2012)
        -   解決されたts1の計算が遅れたために、 [＃1576](https://github.com/pingcap/tiflow/issues/1576)サーバーがパニックになる可能性があるバグを修正します。
        -   プロセッサ[＃2142](https://github.com/pingcap/tiflow/pull/2142)の潜在的なデッドロックの問題を修正します

    -   バックアップと復元（BR）

        -   復元中にすべてのシステムテーブルがフィルタリングされるバグを修正し[＃1201](https://github.com/pingcap/br/issues/1201) [＃1197](https://github.com/pingcap/br/issues/1197)
        -   復元中にTDEが有効になっている場合に、バックアップと復元で「ファイルは既に存在します」というエラーが報告される問題を修正します[＃1179](https://github.com/pingcap/br/issues/1179)

    -   TiDB Lightning

        -   いくつかの特別なデータのTiDBLightningパニックの問題を修正します[＃1213](https://github.com/pingcap/br/issues/1213)
        -   TiDBLightningがインポートされた大きなCSVファイルを分割するときに報告されるEOFエラーを修正します[＃1133](https://github.com/pingcap/br/issues/1133)
        -   TiDB Lightningが`FLOAT`または`DOUBLE`タイプ[＃1186](https://github.com/pingcap/br/pull/1186)の`auto_increment`列のテーブルをインポートすると、非常に大きなベース値が生成されるバグを修正します。
        -   TiDBがParquetファイル[＃1277](https://github.com/pingcap/br/pull/1277)の`DECIMAL`タイプのデータの解析に失敗する問題を修正します
