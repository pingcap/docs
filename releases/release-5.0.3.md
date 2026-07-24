---
title: TiDB 5.0.3 Release Notes
summary: TiDB 5.0.3は2021年7月2日にリリースされました。このリリースには、TiDB、TiKV、PD、 TiFlash、およびTiCDC、バックアップ＆リストア（BR）、 TiDB Lightningなどのツールに対する互換性の変更、機能強化、改善、バグ修正、アップデートが含まれています。主な変更点としては、 TiFlashへの演算子と関数のプッシュダウンのサポート、TiCDCのメモリ消費制限、TiDB、TiKV、PD、 TiFlashのさまざまな問題に対するバグ修正などがあります。
---

# TiDB 5.0.3 リリースノート {#tidb-5-0-3-release-notes}

発売日：2021年7月2日

TiDB バージョン: 5.0.3

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   v4.0 クラスターを v5.0 以降のバージョン (dev または v5.1) にアップグレードすると、 `tidb_multi_statement_mode`変数のデフォルト値が`WARN`から`OFF`に変更されます。
    -   TiDBはMySQL 5.7のnoop変数`innodb_default_row_format`と互換性を持つようになりました。この変数を設定しても効果はありません[＃23541](https://github.com/pingcap/tidb/issues/23541)

## 機能強化 {#feature-enhancements}

-   ツール

    -   TiCDC

        -   ノードの変更フィード情報とヘルス情報を取得するためのHTTP APIを追加します。 [＃1955](https://github.com/pingcap/tiflow/pull/1955)
        -   kafka シンクに SASL/SCRAM サポートを追加する [＃1942](https://github.com/pingcap/tiflow/pull/1942)
        -   TiCDCをサーバーレベルで`--data-dir`サポートする [＃2070](https://github.com/pingcap/tiflow/pull/2070)

## 改善点 {#improvements}

-   TiDB

    -   `TopN`演算子をTiFlash にプッシュダウンするサポート [＃25162](https://github.com/pingcap/tidb/pull/25162)
    -   組み込み関数`json_unquote()`をTiKV にプッシュダウンする機能をサポート [＃24415](https://github.com/pingcap/tidb/issues/24415)
    -   デュアルテーブルからユニオンブランチを削除することをサポート [＃25614](https://github.com/pingcap/tidb/pull/25614)
    -   内蔵機能`replace()` TiFlash にプッシュダウンする機能をサポート [＃25565](https://github.com/pingcap/tidb/pull/25565)
    -   `day()`関数`unix_timestamp()` `concat()` TiFlash に`concat_ws()`ダウンする`datediff()` `year()` `datesub()` [＃25564](https://github.com/pingcap/tidb/pull/25564)
    -   集計オペレータのコスト係数を最適化する [＃25241](https://github.com/pingcap/tidb/pull/25241)
    -   `Limit`演算子をTiFlash にプッシュダウンするサポート [＃25159](https://github.com/pingcap/tidb/pull/25159)
    -   内蔵機能`str_to_date` TiFlash にプッシュダウンする機能をサポート [＃25148](https://github.com/pingcap/tidb/pull/25148)
    -   MPP外部結合がテーブル行数に基づいてビルドテーブルを選択できるようにします。 [＃25142](https://github.com/pingcap/tidb/pull/25142)
    -   `abs()`関数`left()` `right()` TiFlash にプッシュダウンする機能をサポート [＃25133](https://github.com/pingcap/tidb/pull/25133)
    -   ブロードキャストカルテシアン結合をTiFlash にプッシュダウンする機能をサポート [＃25106](https://github.com/pingcap/tidb/pull/25106)
    -   `Union All`演算子をTiFlash にプッシュダウンするサポート [＃25051](https://github.com/pingcap/tidb/pull/25051)
    -   リージョンに基づいて、異なるTiFlashノード間でMPPクエリワークロードのバランスをとることをサポート [＃24724](https://github.com/pingcap/tidb/pull/24724)
    -   MPPクエリ実行後にキャッシュ内の古い領域を無効にする機能をサポート[＃24432](https://github.com/pingcap/tidb/pull/24432)
    -   フォーマット指定子`%b/%M/%r/%T` の組み込み関数`str_to_date`の MySQL 互換性を改善しました [＃25767](https://github.com/pingcap/tidb/pull/25767)

-   TiKV

    -   TiCDCシンクのメモリ消費を制限する[＃10305](https://github.com/tikv/tikv/pull/10305)
    -   TiCDC 古い値キャッシュのメモリ制限の上限を追加します。 [＃10313](https://github.com/tikv/tikv/pull/10313)

-   PD

    -   TiDB Dashboardをv2021.06.15.1 に更新 [＃3798](https://github.com/pingcap/pd/pull/3798)

-   TiFlash

    -   `STRING`型から`DOUBLE`型へのキャストをサポート
    -   `STR_TO_DATE()`機能をサポートする
    -   複数のスレッドを使用して右外部結合の非結合データを最適化する
    -   デカルト結合をサポートする
    -   `LEFT()`と`RIGHT()`関数をサポート
    -   MPPクエリで古いリージョンを自動的に無効化する機能をサポート
    -   `ABS()`機能をサポートする

-   ツール

    -   TiCDC

        -   gRPCの再接続ロジックを改良し、KVクライアントのスループットを向上させる[＃1586](https://github.com/pingcap/tiflow/issues/1586) [＃1501](https://github.com/pingcap/tiflow/issues/1501#issuecomment-820027078) [＃1682](https://github.com/pingcap/tiflow/pull/1682) [＃1393](https://github.com/pingcap/tiflow/issues/1393) [＃1847](https://github.com/pingcap/tiflow/pull/1847) [＃1905](https://github.com/pingcap/tiflow/issues/1905) [＃1904](https://github.com/pingcap/tiflow/issues/1904)
        -   ソーターのI/Oエラーをよりユーザーフレンドリーにする

## バグ修正 {#bug-fixes}

-   TiDB

    -   `SET`型列でマージ結合を使用すると誤った結果が返される問題を修正しました [＃25669](https://github.com/pingcap/tidb/issues/25669)
    -   `IN`式の引数におけるデータ破損の問題を修正 [＃25591](https://github.com/pingcap/tidb/issues/25591)
    -   GCのセッションがグローバル変数の影響を受けないようにする[＃24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリで`limit`を使用するときに発生するpanic問題を修正 [＃25344](https://github.com/pingcap/tidb/issues/25344)
    -   `Limit` を使用してパーティションテーブルをクエリしたときに返される誤った値を修正しました [＃24636](https://github.com/pingcap/tidb/issues/24636)
    -   `IFNULL` `ENUM`または`SET`タイプの列に正しく反映されない問題を修正 [＃24944](https://github.com/pingcap/tidb/issues/24944)
    -   結合サブクエリの`count` `first_row` に変更することで発生する誤った結果を修正しました [＃24865](https://github.com/pingcap/tidb/issues/24865)
    -   `ParallelApply` `TopN`演算子下で使用された場合に発生するクエリ ハングの問題を修正しました [＃24930](https://github.com/pingcap/tidb/issues/24930)
    -   マルチカラムプレフィックスインデックスを使用してSQL文を実行したときに予想よりも多くの結果が返される問題を修正[＃24356](https://github.com/pingcap/tidb/issues/24356)
    -   `<=>`演算子が正しく機能しない問題を修正[＃24477](https://github.com/pingcap/tidb/issues/24477)
    -   並列`Apply`演算子のデータ競合問題を修正 [＃23280](https://github.com/pingcap/tidb/issues/23280)
    -   PartitionUnion演算子のIndexMerge結果をソートするときに`index out of range`エラーが報告される問題を修正しました [＃23919](https://github.com/pingcap/tidb/issues/23919)
    -   `tidb_snapshot`変数を予想外に大きな値に設定するとトランザクション分離損なわれる可能性がある問題を修正しました [＃25680](https://github.com/pingcap/tidb/issues/25680)
    -   ODBCスタイルの定数（たとえば、 `{d '2020-01-01'}` ）を式として使用できない問題を修正しました。 [＃25531](https://github.com/pingcap/tidb/issues/25531)
    -   `SELECT DISTINCT` `Batch Get`に変換すると誤った結果になる問題を修正[＃25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashからTiKVへのクエリのバックオフがトリガーされない問題を修正[＃23665](https://github.com/pingcap/tidb/issues/23665) [＃24421](https://github.com/pingcap/tidb/issues/24421)
    -   `only_full_group_by` チェックするときに発生する`index-out-of-range`エラーを修正します) [＃23839](https://github.com/pingcap/tidb/issues/23839)
    -   相関サブクエリのインデックス結合の結果が間違っている問題を修正[＃25799](https://github.com/pingcap/tidb/issues/25799)

-   TiKV

    -   間違った`tikv_raftstore_hibernated_peer_state`指標を修正する[＃10330](https://github.com/tikv/tikv/issues/10330)
    -   コプロセッサの関数`json_unquote()`の間違った引数の型を修正 [＃10176](https://github.com/tikv/tikv/issues/10176)
    -   場合によってはACIDの破壊を避けるために、正常なシャットダウン中にコールバックのクリアをスキップする[＃10353](https://github.com/tikv/tikv/issues/10353) [＃10307](https://github.com/tikv/tikv/issues/10307)
    -   Leaderのレプリカ読み取りで読み取りインデックスが共有されるバグを修正しました [＃10347](https://github.com/tikv/tikv/issues/10347)
    -   `DOUBLE`を`DOUBLE` に変換する間違った関数を修正 [＃25200](https://github.com/pingcap/tidb/issues/25200)

-   PD

    -   スケジューラの起動後にTTL設定をロードするときに発生するデータ競合の問題を修正しました[＃3771](https://github.com/tikv/pd/issues/3771)
    -   TiDBの`TIKV_REGION_PEERS`テーブルの`is_learner`フィールドが正しくないというバグを修正しました[＃3372](https://github.com/tikv/pd/issues/3372) [＃24293](https://github.com/pingcap/tidb/issues/24293)
    -   ゾーン内のすべての TiKV ノードがオフラインまたはダウンしている場合、PD が他のゾーンへのレプリカをスケジュールしない問題を修正[＃3705](https://github.com/tikv/pd/issues/3705)
    -   スキャッタリージョンスケジューラを追加した後にPDがpanicになる可能性がある問題を修正[＃3762](https://github.com/tikv/pd/pull/3762)

-   TiFlash

    -   分割失敗によりTiFlashが再起動し続ける問題を修正
    -   TiFlashがデルタデータを削除できない潜在的な問題を修正
    -   TiFlashが`CAST`関数で非バイナリ文字に間違ったパディングを追加するバグを修正しました
    -   複雑な`GROUP BY`列の集計クエリを処理するときに誤った結果が発生する問題を修正しました
    -   書き込み圧力が高い場合に発生するTiFlash panic問題を修正
    -   右結合キーが null 値ではなく、左結合キーが null 値の場合に発生するpanicを修正しました。
    -   `read-index`リクエストに長い時間がかかる可能性がある問題を修正しました
    -   読み取り負荷が大きい場合に発生するpanic問題を修正しました
    -   `Date_Format`の関数が`STRING`番目の型引数と`NULL`値で呼び出されたときに発生する可能性のあるpanic問題を修正しました。

-   ツール

    -   TiCDC

        -   チェックポイント更新するときに TiCDC 所有者が終了する問題を修正しました [＃1902](https://github.com/pingcap/tiflow/issues/1902)
        -   MySQLシンクがエラーに遭遇して一時停止した後に、一部のMySQL接続がリークする可能性があるバグを修正しました[＃1946](https://github.com/pingcap/tiflow/pull/1946)
        -   TiCDCが`/proc/meminfo` の読み取りに失敗した場合に発生するpanic問題を修正しました [＃2024](https://github.com/pingcap/tiflow/pull/2024)
        -   TiCDC のランタイムメモリ消費を削減する[#2012](https://github.com/pingcap/tiflow/pull/2012) [＃1958](https://github.com/pingcap/tiflow/pull/1958)
        -   解決された ts の計算が遅れることによって TiCDCサーバーのpanicを引き起こす可能性があるバグを修正しました。 [＃1576](https://github.com/pingcap/tiflow/issues/1576)
        -   プロセッサ潜在的なデッドロック問題を修正 [＃2142](https://github.com/pingcap/tiflow/pull/2142)

    -   Backup & Restore (BR)

        -   復元中にすべてのシステムテーブルがフィルタリングされるバグを修正[＃1197](https://github.com/pingcap/br/issues/1197) [＃1201](https://github.com/pingcap/br/issues/1201)
        -   復元中にTDEが有効になっていると、バックアップと復元で「ファイルが既に存在します」というエラーが報告される問題を修正しました[＃1179](https://github.com/pingcap/br/issues/1179)

    -   TiDB Lightning

        -   一部の特殊データにおけるTiDB Lightning panic問題を修正[＃1213](https://github.com/pingcap/br/issues/1213)
        -   TiDB Lightningがインポートした大きなCSVファイルを分割する際に報告されるEOFエラーを修正しました[＃1133](https://github.com/pingcap/br/issues/1133)
        -   TiDB Lightningが`FLOAT`または`DOUBLE`タイプの`auto_increment`列を持つテーブルをインポートするときに過度に大きなベース値が生成されるバグを修正しました[＃1186](https://github.com/pingcap/br/pull/1186)
        -   TiDBがParquetファイル内の`DECIMAL`種類のデータを解析できない問題を修正 [＃1277](https://github.com/pingcap/br/pull/1277)
