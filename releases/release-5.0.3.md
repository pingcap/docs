---
title: TiDB 5.0.3 Release Notes
summary: TiDB 5.0.3 は 2021 年 7 月 2 日にリリースされました。このリリースには、TiDB、TiKV、PD、 TiFlashや、TiCDC、Backup & Restore (BR)、 TiDB Lightningなどのツールの互換性の変更、機能強化、改善、バグ修正、更新が含まれています。注目すべき変更点としては、演算子と関数をTiFlashにプッシュダウンするためのサポート、TiCDC のメモリ消費制限、TiDB、TiKV、PD、 TiFlashのさまざまな問題に対するバグ修正などがあります。
---

# TiDB 5.0.3 リリースノート {#tidb-5-0-3-release-notes}

発売日: 2021年7月2日

TiDB バージョン: 5.0.3

## 互換性の変更 {#compatibility-changes}

-   ティビ

    -   v4.0 クラスターを v5.0 以降のバージョン (dev または v5.1) にアップグレードすると、 `tidb_multi_statement_mode`変数のデフォルト値が`WARN`から`OFF`に変更されます。
    -   TiDB はMySQL 5.7の noop 変数`innodb_default_row_format`と互換性を持つようになりました。この変数を設定しても効果はありません[＃23541](https://github.com/pingcap/tidb/issues/23541)

## 機能強化 {#feature-enhancements}

-   ツール

    -   ティCDC

        -   ノード[＃1955](https://github.com/pingcap/tiflow/pull/1955)の変更フィード情報とヘルス情報を取得するための HTTP API を追加します。
        -   kafka シンク[＃1942](https://github.com/pingcap/tiflow/pull/1942)に SASL/SCRAM サポートを追加する
        -   TiCDCをサーバーレベル[＃2070](https://github.com/pingcap/tiflow/pull/2070)でサポート`--data-dir`にする

## 改善点 {#improvements}

-   ティビ

    -   `TopN`演算子をTiFlash [＃25162](https://github.com/pingcap/tidb/pull/25162)にプッシュダウンするサポート
    -   組み込み関数`json_unquote()`をTiKV [＃24415](https://github.com/pingcap/tidb/issues/24415)にプッシュダウンするサポート
    -   デュアルテーブル[＃25614](https://github.com/pingcap/tidb/pull/25614)からユニオンブランチを削除するサポート
    -   内蔵機能`replace()`をTiFlash [＃25565](https://github.com/pingcap/tidb/pull/25565)にプッシュダウンするサポート
    -   `concat()`関数`unix_timestamp()` `year()` `datediff()` `day()` `datesub()`プッシュダウンするTiFlash`concat_ws()` [＃25564](https://github.com/pingcap/tidb/pull/25564)
    -   集計オペレータのコスト要因[＃25241](https://github.com/pingcap/tidb/pull/25241)を最適化する
    -   `Limit`演算子をTiFlash [＃25159](https://github.com/pingcap/tidb/pull/25159)にプッシュダウンするサポート
    -   内蔵機能`str_to_date`をTiFlash [＃25148](https://github.com/pingcap/tidb/pull/25148)にプッシュダウンするサポート
    -   MPP外部結合がテーブル行数[＃25142](https://github.com/pingcap/tidb/pull/25142)に基づいてビルドテーブルを選択できるようにします。
    -   組み込み関数`left()` `right()` TiFlash `abs()` [＃25133](https://github.com/pingcap/tidb/pull/25133)プッシュダウンするサポート
    -   ブロードキャスト デカルト ジョインをTiFlash [＃25106](https://github.com/pingcap/tidb/pull/25106)にプッシュダウンするサポート
    -   `Union All`演算子をTiFlash [＃25051](https://github.com/pingcap/tidb/pull/25051)にプッシュダウンするサポート
    -   リージョン[＃24724](https://github.com/pingcap/tidb/pull/24724)に基づいて、異なるTiFlashノード間でMPPクエリワークロードのバランスをとることをサポート
    -   MPPクエリの実行後にキャッシュ内の古い領域を無効にする機能をサポート[＃24432](https://github.com/pingcap/tidb/pull/24432)
    -   フォーマット指定子`%b/%M/%r/%T` [＃25767](https://github.com/pingcap/tidb/pull/25767)の組み込み関数`str_to_date`の MySQL 互換性を向上

-   ティクヴ

    -   TiCDCシンクのメモリ消費を制限する[＃10305](https://github.com/tikv/tikv/pull/10305)
    -   TiCDC の古い値キャッシュ[＃10313](https://github.com/tikv/tikv/pull/10313)のメモリ制限上限を追加します。

-   PD

    -   TiDBダッシュボードをv2021.06.15.1 [＃3798](https://github.com/pingcap/pd/pull/3798)に更新

-   TiFlash

    -   `STRING`型から`DOUBLE`型へのキャストをサポート
    -   `STR_TO_DATE()`機能をサポートする
    -   複数のスレッドを使用して右外部結合の非結合データを最適化する
    -   デカルト結合をサポートする
    -   `LEFT()`と`RIGHT()`関数をサポート
    -   MPP クエリで古いリージョンを自動的に無効化する機能をサポート
    -   `ABS()`機能をサポートする

-   ツール

    -   ティCDC

        -   gRPCの再接続ロジックを改良し、KVクライアントのスループットを向上させる[＃1586](https://github.com/pingcap/tiflow/issues/1586) [＃1501](https://github.com/pingcap/tiflow/issues/1501#issuecomment-820027078) [＃1682](https://github.com/pingcap/tiflow/pull/1682) [＃1393](https://github.com/pingcap/tiflow/issues/1393) [＃1847](https://github.com/pingcap/tiflow/pull/1847) [＃1905](https://github.com/pingcap/tiflow/issues/1905) [＃1904](https://github.com/pingcap/tiflow/issues/1904)
        -   ソーターのI/Oエラーをよりユーザーフレンドリーにする

## バグ修正 {#bug-fixes}

-   ティビ

    -   `SET`型列[＃25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると誤った結果が返される問題を修正
    -   `IN`式の引数[＃25591](https://github.com/pingcap/tidb/issues/25591)データ破損の問題を修正
    -   GCのセッションがグローバル変数の影響を受けないようにする[＃24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリ[＃25344](https://github.com/pingcap/tidb/issues/25344)で`limit`使用した場合に発生するpanic問題を修正
    -   `Limit` [＃24636](https://github.com/pingcap/tidb/issues/24636)を使用してパーティションテーブルをクエリしたときに返される誤った値を修正しました。
    -   `IFNULL` `ENUM`または`SET`タイプの列[＃24944](https://github.com/pingcap/tidb/issues/24944)に正しく反映されない問題を修正
    -   結合サブクエリの`count` `first_row` [＃24865](https://github.com/pingcap/tidb/issues/24865)に変更することで発生する誤った結果を修正
    -   `ParallelApply`が`TopN`演算子[＃24930](https://github.com/pingcap/tidb/issues/24930)の下で使用された場合に発生するクエリ ハングの問題を修正しました
    -   複数列プレフィックスインデックスを使用してSQL文を実行すると、予想よりも多くの結果が返される問題を修正[＃24356](https://github.com/pingcap/tidb/issues/24356)
    -   `<=>`演算子が正しく機能しない問題を修正[＃24477](https://github.com/pingcap/tidb/issues/24477)
    -   並列`Apply`演算子[＃23280](https://github.com/pingcap/tidb/issues/23280)のデータ競合問題を修正
    -   PartitionUnion演算子[＃23919](https://github.com/pingcap/tidb/issues/23919)のIndexMerge結果をソートするときに`index out of range`エラーが報告される問題を修正
    -   `tidb_snapshot`変数を予想外に大きな値に設定するとトランザクション分離[＃25680](https://github.com/pingcap/tidb/issues/25680)が損なわれる可能性がある問題を修正しました。
    -   ODBCスタイルの定数（たとえば、 `{d '2020-01-01'}` ）を式[＃25531](https://github.com/pingcap/tidb/issues/25531)として使用できない問題を修正しました。
    -   `SELECT DISTINCT` `Batch Get`に変換すると誤った結果になる問題を修正[＃25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashからTiKVへのバックオフクエリがトリガーされない問題を修正[＃23665](https://github.com/pingcap/tidb/issues/23665) [＃24421](https://github.com/pingcap/tidb/issues/24421)
    -   `only_full_group_by` [＃23839](https://github.com/pingcap/tidb/issues/23839)をチェックするときに発生する`index-out-of-range`エラーを修正します)
    -   相関サブクエリのインデックス結合の結果が間違っている問題を修正[＃25799](https://github.com/pingcap/tidb/issues/25799)

-   ティクヴ

    -   間違った`tikv_raftstore_hibernated_peer_state`の指標[＃10330](https://github.com/tikv/tikv/issues/10330)修正する
    -   コプロセッサ[＃10176](https://github.com/tikv/tikv/issues/10176)の関数`json_unquote()`の間違った引数の型を修正
    -   場合によってはACIDの破壊を避けるために、正常なシャットダウン中にコールバックのクリアをスキップする[＃10353](https://github.com/tikv/tikv/issues/10353) [＃10307](https://github.com/tikv/tikv/issues/10307)
    -   Leader[＃10347](https://github.com/tikv/tikv/issues/10347)のレプリカ読み取りで読み取りインデックスが共有されるバグを修正しました。
    -   `DOUBLE` `DOUBLE` [＃25200](https://github.com/pingcap/tidb/issues/25200)に変換する間違った関数を修正

-   PD

    -   スケジューラの起動後にTTL設定をロードするときに発生するデータ競合の問題を修正[＃3771](https://github.com/tikv/pd/issues/3771)
    -   TiDBの`TIKV_REGION_PEERS`のテーブルの`is_learner`のフィールドが正しくないバグを修正[＃3372](https://github.com/tikv/pd/issues/3372) [＃24293](https://github.com/pingcap/tidb/issues/24293)
    -   ゾーン内のすべての TiKV ノードがオフラインまたはダウンしている場合、PD が他のゾーンへのレプリカをスケジュールしない問題を修正[＃3705](https://github.com/tikv/pd/issues/3705)
    -   スキャッタリージョンスケジューラを追加した後にPDがpanicになる可能性がある問題を修正[＃3762](https://github.com/tikv/pd/pull/3762)

-   TiFlash

    -   分割失敗によりTiFlash が再起動し続ける問題を修正
    -   TiFlashがデルタデータを削除できない潜在的な問題を修正
    -   TiFlash が`CAST`関数で非バイナリ文字に間違ったパディングを追加するバグを修正しました
    -   複雑な`GROUP BY`列の集計クエリを処理するときに誤った結果が返される問題を修正しました。
    -   書き込み圧力が高い場合に発生するTiFlashpanic問題を修正
    -   右の結合キーが null 可能でなく、左の結合キーが null 可能な場合に発生するpanicを修正しました。
    -   `read-index`のリクエストに長い時間がかかる潜在的な問題を修正
    -   読み取り負荷が大きい場合に発生するpanic問題を修正
    -   `Date_Format`関数が`STRING`の型引数と`NULL`値で呼び出されたときに発生する可能性のあるpanic問題を修正しました。

-   ツール

    -   ティCDC

        -   チェックポイント[＃1902](https://github.com/pingcap/tiflow/issues/1902)を更新するときに TiCDC 所有者が終了する問題を修正しました
        -   MySQLシンクがエラーに遭遇して一時停止した後に、一部のMySQL接続がリークする可能性があるバグを修正[＃1946](https://github.com/pingcap/tiflow/pull/1946)
        -   TiCDCが`/proc/meminfo` [＃2024](https://github.com/pingcap/tiflow/pull/2024)読み取りに失敗した場合に発生するpanic問題を修正
        -   TiCDC のランタイムメモリ消費を削減する[#2012](https://github.com/pingcap/tiflow/pull/2012) [＃1958](https://github.com/pingcap/tiflow/pull/1958)
        -   解決された ts [＃1576](https://github.com/pingcap/tiflow/issues/1576)の計算が遅れて TiCDCサーバーがpanicになる可能性があるバグを修正しました。
        -   プロセッサ[＃2142](https://github.com/pingcap/tiflow/pull/2142)の潜在的なデッドロック問題を修正

    -   バックアップと復元 (BR)

        -   復元中にすべてのシステムテーブルがフィルタリングされるバグを修正[＃1197](https://github.com/pingcap/br/issues/1197) [＃1201](https://github.com/pingcap/br/issues/1201)
        -   復元中に TDE が有効になっている場合に、バックアップと復元で「ファイルが既に存在します」というエラーが報告される問題を修正[＃1179](https://github.com/pingcap/br/issues/1179)

    -   TiDB Lightning

        -   一部の特殊データに対するTiDB Lightningpanic問題を修正[＃1213](https://github.com/pingcap/br/issues/1213)
        -   TiDB Lightningがインポートした大きな CSV ファイルを分割するときに報告される EOF エラーを修正[＃1133](https://github.com/pingcap/br/issues/1133)
        -   TiDB Lightningが`FLOAT`または`DOUBLE`タイプの`auto_increment`列目を持つテーブルをインポートすると、過度に大きなベース値が生成されるバグを修正しました[＃1186](https://github.com/pingcap/br/pull/1186)
        -   TiDBがParquetファイル[＃1277](https://github.com/pingcap/br/pull/1277)の`DECIMAL`型データを解析できない問題を修正
