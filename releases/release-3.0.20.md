---
title: TiDB 3.0.20 Release Notes
summary: TiDB 3.0.20は2020年12月25日にリリースされました。このリリースには、TiDB、TiKV、PDの互換性に関する変更、改善、バグ修正が含まれています。主なバグ修正には、トランザクションステータスのキャッシュの誤り、統計の不正確さ、スタックオーバーフローに関する問題への対処が含まれます。
---

# TiDB 3.0.20 リリースノート {#tidb-3-0-20-release-notes}

発売日：2020年12月25日

TiDB バージョン: 3.0.20

## 互換性の変更 {#compatibility-change}

-   TiDB

    -   `enable-streaming`構成項目[＃21054](https://github.com/pingcap/tidb/pull/21054)廃止する

## 改善点 {#improvements}

-   TiDB

    -   `LOAD DATA`文[＃21222](https://github.com/pingcap/tidb/pull/21222)を準備するときにエラーが発生する

-   TiKV

    -   `end_point_slow_log_threshold`構成項目[＃9145](https://github.com/tikv/tikv/pull/9145)追加する

## バグ修正 {#bug-fixes}

-   TiDB

    -   悲観的トランザクションのトランザクションステータスの誤ったキャッシュを修正[＃21706](https://github.com/pingcap/tidb/pull/21706)
    -   `INFORMATION_SCHEMA.TIDB_HOT_REGIONS` [＃21319](https://github.com/pingcap/tidb/pull/21319)をクエリするときに発生する不正確な統計の問題を修正しました
    -   データベース名が純粋な下位表現でない場合、データが正しく削除[＃21205](https://github.com/pingcap/tidb/pull/21205)れない可能性がある問題を修正しました`DELETE`
    -   再帰ビュー[＃21000](https://github.com/pingcap/tidb/pull/21000)構築時に発生するスタックオーバーフローの問題を修正
    -   TiKVクライアント[＃20863](https://github.com/pingcap/tidb/pull/20863)のgoroutineリークの問題を修正
    -   `year`型[＃20828](https://github.com/pingcap/tidb/pull/20828)の誤ったデフォルトのゼロ値を修正
    -   インデックス検索結合[＃20791](https://github.com/pingcap/tidb/pull/20791)におけるゴルーチンリークの問題を修正
    -   `INSERT SELECT FOR UPDATE`実行すると悲観的トランザクション[＃20681](https://github.com/pingcap/tidb/pull/20681)で不正なパケットが返される問題を修正
    -   不明なタイムゾーンを修正`'posixrules'` [＃20605](https://github.com/pingcap/tidb/pull/20605)
    -   符号なし整数型をビット型[＃20362](https://github.com/pingcap/tidb/pull/20362)に変換するときに発生する問題を修正しました
    -   ビット型列[＃20339](https://github.com/pingcap/tidb/pull/20339)の破損したデフォルト値を修正
    -   等価条件の1つが`Enum`または`Set`タイプ[＃20296](https://github.com/pingcap/tidb/pull/20296)である場合に、潜在的に誤った結果を修正します。
    -   `!= any()` [＃20061](https://github.com/pingcap/tidb/pull/20061)の誤った動作を修正する
    -   `BETWEEN...AND...`型変換で無効な結果が返される問題を修正[＃21503](https://github.com/pingcap/tidb/pull/21503)
    -   `ADDDATE`機能[＃21008](https://github.com/pingcap/tidb/pull/21008)の互換性の問題を修正
    -   新しく追加された`Enum`列[＃20999](https://github.com/pingcap/tidb/pull/20999)の正しいデフォルト値を設定する
    -   `SELECT DATE_ADD('2007-03-28 22:08:28',INTERVAL "-2.-2" SECOND)`ようなSQL文の結果をMySQL [＃20627](https://github.com/pingcap/tidb/pull/20627)と互換性があるように修正します
    -   列タイプ[＃20532](https://github.com/pingcap/tidb/pull/20532)を変更するときに誤ったデフォルト値を修正
    -   入力引数が`float`または`decimal`型の場合に`timestamp`関数が間違った結果を取得する問題を修正しました[＃20469](https://github.com/pingcap/tidb/pull/20469)
    -   統計[＃20424](https://github.com/pingcap/tidb/pull/20424)における潜在的なデッドロック問題を修正
    -   オーバーフローしたfloat型データが挿入される問題を修正[＃20251](https://github.com/pingcap/tidb/pull/20251)

-   TiKV

    -   コミットされたトランザクションでキーがロックされ削除されたときに、キーが存在することを示すエラーが返される問題を修正しました[＃8931](https://github.com/tikv/tikv/pull/8931)

-   PD

    -   PD の起動時および古いリージョンが多すぎる場合にログが大量に出力される問題を修正しました[＃3064](https://github.com/pingcap/pd/pull/3064)
