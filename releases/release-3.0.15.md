---
title: TiDB 3.0.15 Release Notes
---

# TiDB3.0.15リリースノート {#tidb-3-0-15-release-notes}

発売日：2020年6月5日

TiDBバージョン：3.0.15

## 新機能 {#new-features}

-   TiDB

    -   プランキャッシュ機能を使用するためにパーティションテーブルでのクエリを禁止する[＃16759](https://github.com/pingcap/tidb/pull/16759)
    -   パーティションテーブルで`admin recover index`および`admin check index` [＃17390](https://github.com/pingcap/tidb/pull/17390)をサポートする[＃17315](https://github.com/pingcap/tidb/pull/17315)
    -   Rangeパーティションテーブル[＃17318](https://github.com/pingcap/tidb/pull/17318)の`in`条件のパーティションプルーニングをサポートします。
    -   `SHOW CREATE TABLE`の出力を最適化し、パーティション名[＃16315](https://github.com/pingcap/tidb/pull/16315)に引用符を追加します。
    -   `GROUP_CONCAT`関数[＃16988](https://github.com/pingcap/tidb/pull/16988)の`ORDER BY`節をサポートします。
    -   `CMSketch`統計のメモリ割り当てメカニズムを最適化して、パフォーマンス[＃17543](https://github.com/pingcap/tidb/pull/17543)に対するガベージコレクション（GC）の影響を減らします。

-   PD

    -   PDがリーダーの数に関してスケジューリングを実行するポリシーを追加します[＃2479](https://github.com/pingcap/pd/pull/2479)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ディープコピーを使用して、 `Hash`集計関数の`enum`型および`set`型データをコピーします。正しさの問題を修正する[＃16890](https://github.com/pingcap/tidb/pull/16890)
    -   整数オーバーフロー[＃16753](https://github.com/pingcap/tidb/pull/16753)の処理ロジックが間違っているために、 `PointGet`が誤った結果を返す問題を修正します。
    -   クエリ述語[＃16557](https://github.com/pingcap/tidb/pull/16557)で`CHAR()`関数が使用されている場合に、誤った処理ロジックによって引き起こされる誤った結果の問題を修正します。
    -   `IsTrue`および`IsFalse`関数のストレージレイヤーと計算レイヤーでの一貫性のない結果の問題を修正します[＃16627](https://github.com/pingcap/tidb/pull/16627)
    -   [＃16993](https://github.com/pingcap/tidb/pull/16993)などの一部の式の誤った`NotNull`フラグを修正し`case when`
    -   一部のシナリオでオプティマイザが`TableDual`の物理計画を見つけられないという問題を修正します[＃17014](https://github.com/pingcap/tidb/pull/17014)
    -   パーティション選択の構文がハッシュパーティションテーブル[＃17051](https://github.com/pingcap/tidb/pull/17051)で正しく有効にならない問題を修正します。
    -   XORが浮動小数点数[＃16976](https://github.com/pingcap/tidb/pull/16976)で動作する場合の、TiDBとMySQL間の一貫性のない結果を修正します。
    -   準備された方法でDDLステートメントを実行するときに発生するエラーを修正します[＃17415](https://github.com/pingcap/tidb/pull/17415)
    -   IDアロケータ[＃17548](https://github.com/pingcap/tidb/pull/17548)でバッチサイズを計算する誤った処理ロジックを修正します
    -   時間が高価なしきい値を超えたときに`MAX_EXEC_TIME`ヒントが有効にならない問題を修正します[＃17534](https://github.com/pingcap/tidb/pull/17534)

-   TiKV

    -   長時間実行した後、メモリの最適化が効果的でない問題を修正します[＃7790](https://github.com/tikv/tikv/pull/7790)
    -   TiKVが誤って再起動された後にスナップショットファイルを誤って削除することによって引き起こされるpanicの問題を修正します[＃7925](https://github.com/tikv/tikv/pull/7925)
    -   メッセージパッケージが大きすぎるために発生するgRPC切断を修正します[＃7822](https://github.com/tikv/tikv/pull/7822)
