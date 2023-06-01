---
title: TiDB 3.0.20 Release Notes
---

# TiDB 3.0.20 リリースノート {#tidb-3-0-20-release-notes}

発売日：2020年12月25日

TiDB バージョン: 3.0.20

## 互換性の変更 {#compatibility-change}

-   TiDB

    -   `enable-streaming`構成アイテム[#21054](https://github.com/pingcap/tidb/pull/21054)を非推奨にする

## 改善点 {#improvements}

-   TiDB

    -   `LOAD DATA`ステートメント[#21222](https://github.com/pingcap/tidb/pull/21222)の準備時にエラーが発生します。

-   TiKV

    -   `end_point_slow_log_threshold`設定項目[#9145](https://github.com/tikv/tikv/pull/9145)を追加します

## バグの修正 {#bug-fixes}

-   TiDB

    -   悲観的トランザクション[#21706](https://github.com/pingcap/tidb/pull/21706)のトランザクション ステータスの誤ったキャッシュを修正しました。
    -   `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [#21319](https://github.com/pingcap/tidb/pull/21319)のクエリ時に発生する不正確な統計の問題を修正します。
    -   データベース名が純粋な下位表現ではない場合、データが正しく削除されない場合が`DELETE`問題を修正します[#21205](https://github.com/pingcap/tidb/pull/21205)
    -   再帰的ビュー[#21000](https://github.com/pingcap/tidb/pull/21000)の構築時に発生するスタック オーバーフローの問題を修正します。
    -   TiKV クライアント[#20863](https://github.com/pingcap/tidb/pull/20863)での goroutine リークの問題を修正
    -   `year`タイプ[#20828](https://github.com/pingcap/tidb/pull/20828)の誤ったデフォルトのゼロ値を修正
    -   インデックス検索結合[#20791](https://github.com/pingcap/tidb/pull/20791)での goroutine リークの問題を修正
    -   `INSERT SELECT FOR UPDATE`を実行すると、悲観的トランザクション[#20681](https://github.com/pingcap/tidb/pull/20681)で不正な形式のパケットが返される問題を修正します。
    -   不明なタイムゾーンを修正する`'posixrules'` [#20605](https://github.com/pingcap/tidb/pull/20605)
    -   符号なし整数型をビット型[#20362](https://github.com/pingcap/tidb/pull/20362)に変換するときに発生する問題を修正します。
    -   ビット型列[#20339](https://github.com/pingcap/tidb/pull/20339)の破損したデフォルト値を修正
    -   等しい条件の 1 つが`Enum`または`Set`タイプ[#20296](https://github.com/pingcap/tidb/pull/20296)である場合に不正確になる可能性がある結果を修正しました。
    -   `!= any()` [#20061](https://github.com/pingcap/tidb/pull/20061)の誤った動作を修正
    -   `BETWEEN...AND...`の型変換で無効な結果が返される問題を修正[#21503](https://github.com/pingcap/tidb/pull/21503)
    -   `ADDDATE`機能[#21008](https://github.com/pingcap/tidb/pull/21008)との互換性の問題を修正
    -   新しく追加された`Enum`列[#20999](https://github.com/pingcap/tidb/pull/20999)に正しいデフォルト値を設定します。
    -   MySQL [#20627](https://github.com/pingcap/tidb/pull/20627)と互換性があるように、 `SELECT DATE_ADD('2007-03-28 22:08:28',INTERVAL "-2.-2" SECOND)`のような SQL ステートメントの結果を修正しました。
    -   列タイプ[#20532](https://github.com/pingcap/tidb/pull/20532)を変更するときの誤ったデフォルト値を修正しました。
    -   入力引数が`float`または`decimal`型[#20469](https://github.com/pingcap/tidb/pull/20469)の場合、 `timestamp`関数が間違った結果を取得する問題を修正
    -   統計[#20424](https://github.com/pingcap/tidb/pull/20424)の潜在的なデッドロックの問題を修正
    -   オーバーフローしたfloat型データが挿入される問題を修正[#20251](https://github.com/pingcap/tidb/pull/20251)

-   TiKV

    -   コミットされたトランザクションでこのキーがロックされ削除された場合、キーが存在することを示すエラーが返される問題を修正します[#8931](https://github.com/tikv/tikv/pull/8931)

-   PD

    -   PD の起動時、および古いリージョン[#3064](https://github.com/pingcap/pd/pull/3064)が多すぎる場合に出力されるログが多すぎる問題を修正します。
