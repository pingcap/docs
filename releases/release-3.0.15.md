---
title: TiDB 3.0.15 Release Notes
---

# TiDB 3.0.15 リリースノート {#tidb-3-0-15-release-notes}

発売日：2020年6月5日

TiDB バージョン: 3.0.15

## 新機能 {#new-features}

-   TiDB

    -   パーティション テーブル内のクエリでプラン キャッシュ機能を使用することを禁止する[#16759](https://github.com/pingcap/tidb/pull/16759)
    -   分割されたテーブルで`admin recover index`ステートメントと`admin check index`ステートメントをサポートする[#17315](https://github.com/pingcap/tidb/pull/17315) [#17390](https://github.com/pingcap/tidb/pull/17390)
    -   レンジ・パーティション・テーブルの`in`条件のパーティション・プルーニングをサポート[#17318](https://github.com/pingcap/tidb/pull/17318)
    -   `SHOW CREATE TABLE`の出力を最適化し、パーティション名に引用符を追加します[#16315](https://github.com/pingcap/tidb/pull/16315)
    -   `GROUP_CONCAT`機能[#16988](https://github.com/pingcap/tidb/pull/16988)で`ORDER BY`節をサポート
    -   `CMSketch`統計のメモリ割り当てメカニズムを最適化して、ガベージコレクション(GC) がパフォーマンスに与える影響を軽減する[#17543](https://github.com/pingcap/tidb/pull/17543)

-   PD

    -   PD が Leaders [#2479](https://github.com/pingcap/pd/pull/2479)の数に関してスケジューリングを行うポリシーを追加します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   ディープ コピーを使用して、 `enum`と`set`型のデータを`Hash`集計関数にコピーします。正確性の問題を修正する[#16890](https://github.com/pingcap/tidb/pull/16890)
    -   整数オーバーフローの処理ロジックが間違っているため、 `PointGet`が誤った結果を返す問題を修正[#16753](https://github.com/pingcap/tidb/pull/16753)
    -   クエリ述語[#16557](https://github.com/pingcap/tidb/pull/16557)で`CHAR()`関数が使用されている場合に、処理ロジックが正しくないために結果が正しくない問題を修正します。
    -   `IsTrue`と`IsFalse`関数のstorageレイヤーと計算レイヤーで結果が一致しない問題を修正[#16627](https://github.com/pingcap/tidb/pull/16627)
    -   `case when` [#16993](https://github.com/pingcap/tidb/pull/16993)など、一部の式の誤った`NotNull`フラグを修正します。
    -   一部のシナリオでオプティマイザーが`TableDual`の物理計画を見つけられない問題を修正します[#17014](https://github.com/pingcap/tidb/pull/17014)
    -   ハッシュパーティションテーブルでパーティション選択の構文が正しく反映されない問題を修正します[#17051](https://github.com/pingcap/tidb/pull/17051)
    -   XOR が浮動小数点数[#16976](https://github.com/pingcap/tidb/pull/16976)で動作するときの TiDB と MySQL の間の矛盾した結果を修正します。
    -   準備された方法で DDL ステートメントを実行すると発生するエラーを修正します[#17415](https://github.com/pingcap/tidb/pull/17415)
    -   ID アロケータ[#17548](https://github.com/pingcap/tidb/pull/17548)でバッチ サイズを計算する処理ロジックが正しくない問題を修正
    -   時間が高価なしきい値を超えると`MAX_EXEC_TIME` SQL ヒントが有効にならない問題を修正[#17534](https://github.com/pingcap/tidb/pull/17534)

-   TiKV

    -   長時間実行した後、メモリの最適化が有効にならない問題を修正[#7790](https://github.com/tikv/tikv/pull/7790)
    -   TiKV が誤って再起動された後、スナップショット ファイルを誤って削除することによって引き起こされるpanicの問題を修正します[#7925](https://github.com/tikv/tikv/pull/7925)
    -   大きすぎるメッセージ パッケージによる gRPC の切断を修正する[#7822](https://github.com/tikv/tikv/pull/7822)
