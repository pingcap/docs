---
title: TiDB 3.0.20 Release Notes
---

# TiDB 3.0.20 リリースノート {#tidb-3-0-20-release-notes}

発売日：2020年12月25日

TiDB バージョン: 3.0.20

## 互換性の変更 {#compatibility-change}

-   TiDB

    -   `enable-streaming`構成アイテム[<a href="https://github.com/pingcap/tidb/pull/21054">#21054</a>](https://github.com/pingcap/tidb/pull/21054)を非推奨にする

## 改善点 {#improvements}

-   TiDB

    -   `LOAD DATA`ステートメント[<a href="https://github.com/pingcap/tidb/pull/21222">#21222</a>](https://github.com/pingcap/tidb/pull/21222)の準備時にエラーが発生します。

-   TiKV

    -   `end_point_slow_log_threshold`設定項目[<a href="https://github.com/tikv/tikv/pull/9145">#9145</a>](https://github.com/tikv/tikv/pull/9145)を追加します

## バグの修正 {#bug-fixes}

-   TiDB

    -   悲観的トランザクション[<a href="https://github.com/pingcap/tidb/pull/21706">#21706</a>](https://github.com/pingcap/tidb/pull/21706)のトランザクション ステータスの誤ったキャッシュを修正しました。
    -   `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [<a href="https://github.com/pingcap/tidb/pull/21319">#21319</a>](https://github.com/pingcap/tidb/pull/21319)のクエリ時に発生する不正確な統計の問題を修正します。
    -   データベース名が純粋な下位表現ではない場合、データが正しく削除されない場合が`DELETE`問題を修正します[<a href="https://github.com/pingcap/tidb/pull/21205">#21205</a>](https://github.com/pingcap/tidb/pull/21205)
    -   再帰的ビュー[<a href="https://github.com/pingcap/tidb/pull/21000">#21000</a>](https://github.com/pingcap/tidb/pull/21000)の構築時に発生するスタック オーバーフローの問題を修正します。
    -   TiKV クライアント[<a href="https://github.com/pingcap/tidb/pull/20863">#20863</a>](https://github.com/pingcap/tidb/pull/20863)での goroutine リークの問題を修正
    -   `year`タイプ[<a href="https://github.com/pingcap/tidb/pull/20828">#20828</a>](https://github.com/pingcap/tidb/pull/20828)の誤ったデフォルトのゼロ値を修正
    -   インデックス検索結合[<a href="https://github.com/pingcap/tidb/pull/20791">#20791</a>](https://github.com/pingcap/tidb/pull/20791)での goroutine リークの問題を修正
    -   `INSERT SELECT FOR UPDATE`を実行すると、悲観的トランザクション[<a href="https://github.com/pingcap/tidb/pull/20681">#20681</a>](https://github.com/pingcap/tidb/pull/20681)で不正な形式のパケットが返される問題を修正します。
    -   不明なタイムゾーンを修正する`'posixrules'` [<a href="https://github.com/pingcap/tidb/pull/20605">#20605</a>](https://github.com/pingcap/tidb/pull/20605)
    -   符号なし整数型をビット型[<a href="https://github.com/pingcap/tidb/pull/20362">#20362</a>](https://github.com/pingcap/tidb/pull/20362)に変換するときに発生する問題を修正します。
    -   ビット型列[<a href="https://github.com/pingcap/tidb/pull/20339">#20339</a>](https://github.com/pingcap/tidb/pull/20339)の破損したデフォルト値を修正
    -   等しい条件の 1 つが`Enum`または`Set`タイプ[<a href="https://github.com/pingcap/tidb/pull/20296">#20296</a>](https://github.com/pingcap/tidb/pull/20296)である場合に不正確になる可能性がある結果を修正しました。
    -   `!= any()` [<a href="https://github.com/pingcap/tidb/pull/20061">#20061</a>](https://github.com/pingcap/tidb/pull/20061)の誤った動作を修正
    -   `BETWEEN...AND...`の型変換で無効な結果が返される問題を修正[<a href="https://github.com/pingcap/tidb/pull/21503">#21503</a>](https://github.com/pingcap/tidb/pull/21503)
    -   `ADDDATE`機能[<a href="https://github.com/pingcap/tidb/pull/21008">#21008</a>](https://github.com/pingcap/tidb/pull/21008)との互換性の問題を修正
    -   新しく追加された`Enum`列[<a href="https://github.com/pingcap/tidb/pull/20999">#20999</a>](https://github.com/pingcap/tidb/pull/20999)に正しいデフォルト値を設定します。
    -   MySQL [<a href="https://github.com/pingcap/tidb/pull/20627">#20627</a>](https://github.com/pingcap/tidb/pull/20627)と互換性があるように、 `SELECT DATE_ADD('2007-03-28 22:08:28',INTERVAL "-2.-2" SECOND)`のような SQL ステートメントの結果を修正しました。
    -   列タイプ[<a href="https://github.com/pingcap/tidb/pull/20532">#20532</a>](https://github.com/pingcap/tidb/pull/20532)を変更するときの誤ったデフォルト値を修正しました。
    -   入力引数が`float`または`decimal`型[<a href="https://github.com/pingcap/tidb/pull/20469">#20469</a>](https://github.com/pingcap/tidb/pull/20469)の場合、 `timestamp`関数が間違った結果を取得する問題を修正
    -   統計[<a href="https://github.com/pingcap/tidb/pull/20424">#20424</a>](https://github.com/pingcap/tidb/pull/20424)の潜在的なデッドロックの問題を修正
    -   オーバーフローしたfloat型データが挿入される問題を修正[<a href="https://github.com/pingcap/tidb/pull/20251">#20251</a>](https://github.com/pingcap/tidb/pull/20251)

-   TiKV

    -   コミットされたトランザクションでこのキーがロックされ削除された場合、キーが存在することを示すエラーが返される問題を修正します[<a href="https://github.com/tikv/tikv/pull/8931">#8931</a>](https://github.com/tikv/tikv/pull/8931)

-   PD

    -   PD の起動時、および古いリージョン[<a href="https://github.com/pingcap/pd/pull/3064">#3064</a>](https://github.com/pingcap/pd/pull/3064)が多すぎる場合に出力されるログが多すぎる問題を修正します。
