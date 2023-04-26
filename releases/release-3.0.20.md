---
title: TiDB 3.0.20 Release Notes
---

# TiDB 3.0.20 リリースノート {#tidb-3-0-20-release-notes}

発売日：2020年12月25日

TiDB バージョン: 3.0.20

## 互換性の変更 {#compatibility-change}

-   TiDB

    -   `enable-streaming`構成アイテム[#21054](https://github.com/pingcap/tidb/pull/21054)を非推奨にします

## 改良点 {#improvements}

-   TiDB

    -   `LOAD DATA`ステートメントの準備時にエラーを発生させる[#21222](https://github.com/pingcap/tidb/pull/21222)

-   TiKV

    -   `end_point_slow_log_threshold`構成アイテム[#9145](https://github.com/tikv/tikv/pull/9145)を追加

## バグの修正 {#bug-fixes}

-   TiDB

    -   悲観的トランザクション[#21706](https://github.com/pingcap/tidb/pull/21706)のトランザクション ステータスの誤ったキャッシュを修正します。
    -   `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [#21319](https://github.com/pingcap/tidb/pull/21319)のクエリ時に発生する不正確な統計の問題を修正します。
    -   データベース名が純粋な下位表現でない場合、データが正しく削除されない可能性が`DELETE`問題を修正[#21205](https://github.com/pingcap/tidb/pull/21205)
    -   再帰ビュー[#21000](https://github.com/pingcap/tidb/pull/21000)のビルド時に発生するスタック オーバーフローの問題を修正します。
    -   TiKV クライアント[#20863](https://github.com/pingcap/tidb/pull/20863)のゴルーチン リークの問題を修正
    -   `year`タイプ[#20828](https://github.com/pingcap/tidb/pull/20828)の誤ったデフォルトのゼロ値を修正
    -   インデックス ルックアップ ジョイン[#20791](https://github.com/pingcap/tidb/pull/20791)でのゴルーチン リークの問題を修正します。
    -   悲観的トランザクション[#20681](https://github.com/pingcap/tidb/pull/20681)で`INSERT SELECT FOR UPDATE`を実行すると不正な形式のパケットが返される問題を修正
    -   不明なタイムゾーンを修正する`'posixrules'` [#20605](https://github.com/pingcap/tidb/pull/20605)
    -   符号なし整数型をビット型に変換する際に発生する問題を修正[#20362](https://github.com/pingcap/tidb/pull/20362)
    -   ビット型列[#20339](https://github.com/pingcap/tidb/pull/20339)の破損した既定値を修正します。
    -   等しい条件の 1 つが`Enum`または`Set`タイプ[#20296](https://github.com/pingcap/tidb/pull/20296)である場合に誤った結果になる可能性がある問題を修正
    -   `!= any()` [#20061](https://github.com/pingcap/tidb/pull/20061)の間違った動作を修正
    -   `BETWEEN...AND...`の型変換が無効な結果を返す問題を修正[#21503](https://github.com/pingcap/tidb/pull/21503)
    -   `ADDDATE`関数[#21008](https://github.com/pingcap/tidb/pull/21008)との互換性の問題を修正します。
    -   新しく追加された`Enum`列[#20999](https://github.com/pingcap/tidb/pull/20999)に正しいデフォルト値を設定します
    -   `SELECT DATE_ADD('2007-03-28 22:08:28',INTERVAL "-2.-2" SECOND)`のような SQL ステートメントの結果を MySQL [#20627](https://github.com/pingcap/tidb/pull/20627)と互換性があるように修正します。
    -   列タイプを変更するときの誤ったデフォルト値を修正します[#20532](https://github.com/pingcap/tidb/pull/20532)
    -   入力引数が`float`または`decimal`型[#20469](https://github.com/pingcap/tidb/pull/20469)の場合、 `timestamp`関数が間違った結果になる問題を修正
    -   統計[#20424](https://github.com/pingcap/tidb/pull/20424)の潜在的なデッドロックの問題を修正
    -   オーバーフローした float 型のデータが挿入される問題を修正[#20251](https://github.com/pingcap/tidb/pull/20251)

-   TiKV

    -   コミットされたトランザクションでキーがロックされ、削除されている場合、キーが存在することを示すエラーが返される問題を修正します[#8931](https://github.com/tikv/tikv/pull/8931)

-   PD

    -   PD の起動時および古いリージョンが多すぎる場合に出力されるログが多すぎる問題を修正します[#3064](https://github.com/pingcap/pd/pull/3064)
