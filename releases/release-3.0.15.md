---
title: TiDB 3.0.15 Release Notes
---

# TiDB 3.0.15 リリースノート {#tidb-3-0-15-release-notes}

発売日：2020年6月5日

TiDB バージョン: 3.0.15

## 新機能 {#new-features}

-   TiDB

    -   パーティション テーブル内のクエリでプラン キャッシュ機能を使用することを禁止します[#16759](https://github.com/pingcap/tidb/pull/16759)
    -   パーティションテーブルで`admin recover index`および`admin check index`ステートメントをサポート[#17315](https://github.com/pingcap/tidb/pull/17315) [#17390](https://github.com/pingcap/tidb/pull/17390)
    -   レンジ パーティション テーブル[#17318](https://github.com/pingcap/tidb/pull/17318)の`in`条件のパーティション プルーニングをサポートします。
    -   `SHOW CREATE TABLE`の出力を最適化し、パーティション名に引用符を追加します[#16315](https://github.com/pingcap/tidb/pull/16315)
    -   `GROUP_CONCAT`機能[#16988](https://github.com/pingcap/tidb/pull/16988)の`ORDER BY`句をサポートします。
    -   `CMSketch`統計のメモリ割り当てメカニズムを最適化して、パフォーマンスに対するガベージコレクション(GC) の影響を軽減します[#17543](https://github.com/pingcap/tidb/pull/17543)

-   PD

    -   リーダー[#2479](https://github.com/pingcap/pd/pull/2479)の数に基づいて PD がスケジューリングを実行するポリシーを追加します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   ディープ コピーを使用して、 `Hash`集計関数の`enum`と`set`型のデータをコピーします。正確さの問題を修正する[#16890](https://github.com/pingcap/tidb/pull/16890)
    -   整数オーバーフロー[#16753](https://github.com/pingcap/tidb/pull/16753)の処理ロジックが間違っているため、 `PointGet`が間違った結果を返す問題を修正
    -   クエリ述語[#16557](https://github.com/pingcap/tidb/pull/16557)で`CHAR()`関数が使用されている場合に、不正な処理ロジックが原因で不正な結果が発生する問題を修正します。
    -   `IsTrue`と`IsFalse`関数のstorageレイヤーと計算レイヤーで結果が矛盾する問題を修正[#16627](https://github.com/pingcap/tidb/pull/16627)
    -   `case when` [#16993](https://github.com/pingcap/tidb/pull/16993)などの一部の式の誤った`NotNull`フラグを修正しました。
    -   一部のシナリオ[#17014](https://github.com/pingcap/tidb/pull/17014)で、オプティマイザーが`TableDual`物理プランを見つけられない問題を修正します。
    -   ハッシュパーティションテーブル[#17051](https://github.com/pingcap/tidb/pull/17051)でパーティション選択の構文が正しく有効にならない問題を修正します。
    -   XOR が浮動小数点数[#16976](https://github.com/pingcap/tidb/pull/16976)で演算される場合に、TiDB と MySQL の間で一貫性のない結果が修正されました。
    -   準備された方法で DDL ステートメントを実行するときに発生するエラーを修正します[#17415](https://github.com/pingcap/tidb/pull/17415)
    -   ID アロケーター[#17548](https://github.com/pingcap/tidb/pull/17548)でバッチ サイズを計算する誤った処理ロジックを修正しました。
    -   時間が高価なしきい値[#17534](https://github.com/pingcap/tidb/pull/17534)を超えると、 `MAX_EXEC_TIME` SQL ヒントが有効にならない問題を修正します。

-   TiKV

    -   長時間実行するとメモリのデフラグが有効にならない問題を修正[#7790](https://github.com/tikv/tikv/pull/7790)
    -   TiKV が誤って再起動された後、スナップショット ファイルを誤って削除することによって引き起こされるpanicの問題を修正します[#7925](https://github.com/tikv/tikv/pull/7925)
    -   大きすぎるメッセージ パッケージによって引き起こされる gRPC 切断を修正します[#7822](https://github.com/tikv/tikv/pull/7822)
