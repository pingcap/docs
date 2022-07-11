---
title: TiDB 3.0.20 Release Notes
---

# TiDB3.0.20リリースノート {#tidb-3-0-20-release-notes}

発売日：2020年12月25日

TiDBバージョン：3.0.20

## 互換性の変更 {#compatibility-change}

-   TiDB

    -   `enable-streaming`構成アイテム[＃21054](https://github.com/pingcap/tidb/pull/21054)を廃止します

## 改善 {#improvements}

-   TiDB

    -   `LOAD DATA`ステートメント[＃21222](https://github.com/pingcap/tidb/pull/21222)を準備するときにエラーを発生させます

-   TiKV

    -   `end_point_slow_log_threshold`の構成アイテム[＃9145](https://github.com/tikv/tikv/pull/9145)を追加します

## バグの修正 {#bug-fixes}

-   TiDB

    -   悲観的なトランザクションのトランザクションステータスの誤ったキャッシュを修正する[＃21706](https://github.com/pingcap/tidb/pull/21706)
    -   `INFORMATION_SCHEMA.TIDB_HOT_REGIONS`をクエリするときに発生する不正確な統計の問題を修正し[＃21319](https://github.com/pingcap/tidb/pull/21319)
    -   データベース名が純粋な下位表現でない場合に`DELETE`がデータを正しく削除しない可能性があるという問題を修正します[＃21205](https://github.com/pingcap/tidb/pull/21205)
    -   再帰ビューを構築するときに発生するスタックオーバーフローの問題を修正します[＃21000](https://github.com/pingcap/tidb/pull/21000)
    -   TiKVクライアント[＃20863](https://github.com/pingcap/tidb/pull/20863)でのゴルーチンリークの問題を修正します
    -   `year`タイプ[＃20828](https://github.com/pingcap/tidb/pull/20828)の誤ったデフォルトのゼロ値を修正
    -   インデックスルックアップ結合[＃20791](https://github.com/pingcap/tidb/pull/20791)でのゴルーチンリークの問題を修正します
    -   `INSERT SELECT FOR UPDATE`を実行すると、悲観的なトランザクション[＃20681](https://github.com/pingcap/tidb/pull/20681)で不正な形式のパケットが返される問題を修正します。
    -   不明なタイムゾーンを[＃20605](https://github.com/pingcap/tidb/pull/20605)する`'posixrules'`
    -   符号なし整数型をビット型[＃20362](https://github.com/pingcap/tidb/pull/20362)に変換するときに発生する問題を修正します
    -   ビットタイプ列[＃20339](https://github.com/pingcap/tidb/pull/20339)の破損したデフォルト値を修正します
    -   等しい条件の1つが`Enum`または`Set`タイプ[＃20296](https://github.com/pingcap/tidb/pull/20296)である場合に、潜在的に誤った結果を修正します
    -   [＃20061](https://github.com/pingcap/tidb/pull/20061)の間違った動作を修正し`!= any()`
    -   `BETWEEN...AND...`の型変換が無効な結果を返す問題を修正します[＃21503](https://github.com/pingcap/tidb/pull/21503)
    -   `ADDDATE`関数[＃21008](https://github.com/pingcap/tidb/pull/21008)との互換性の問題を修正します
    -   新しく追加された`Enum`列[＃20999](https://github.com/pingcap/tidb/pull/20999)の正しいデフォルト値を設定します
    -   MySQL3と互換性があるように`SELECT DATE_ADD('2007-03-28 22:08:28',INTERVAL "-2.-2" SECOND)`のようなSQLステートメントの結果を修正し[＃20627](https://github.com/pingcap/tidb/pull/20627)
    -   列タイプ[＃20532](https://github.com/pingcap/tidb/pull/20532)を変更するときの誤ったデフォルト値を修正
    -   入力引数が`float`または`decimal`タイプ[＃20469](https://github.com/pingcap/tidb/pull/20469)の場合に`timestamp`関数が間違った結果を得る問題を修正します
    -   統計[＃20424](https://github.com/pingcap/tidb/pull/20424)の潜在的なデッドロックの問題を修正します
    -   オーバーフローしたfloat型データが挿入される問題を修正します[＃20251](https://github.com/pingcap/tidb/pull/20251)

-   TiKV

    -   コミットされたトランザクションでこのキーがロックされて削除されたときにキーが存在することを示すエラーが返される問題を修正します[＃8931](https://github.com/tikv/tikv/pull/8931)

-   PD

    -   PDの開始時、および古いリージョンが多すぎる場合に出力されるログが多すぎる問題を修正します[＃3064](https://github.com/pingcap/pd/pull/3064)
