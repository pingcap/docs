---
title: TiDB 3.0.15 Release Notes
summary: TiDB 3.0.15は2020年6月5日にリリースされました。新機能には、パーティションテーブルにおけるadmin-recover-index文とadmin-check-index文のサポート、およびメモリ割り当てメカニズムの最適化が含まれます。バグ修正では、PointGetで結果が不正確になる問題や、浮動小数点数に対するXOR演算時にTiDBとMySQL間で結果が一致しない問題などが修正されています。TiKVでは、メモリのデフラグとgRPCの切断に関連する問題が修正されています。
---

# TiDB 3.0.15 リリースノート {#tidb-3-0-15-release-notes}

発売日：2020年6月5日

TiDB バージョン: 3.0.15

## 新機能 {#new-features}

-   TiDB

    -   パーティションテーブル内のクエリでプランキャッシュ機能の使用を禁止する[＃16759](https://github.com/pingcap/tidb/pull/16759)
    -   パーティションテーブル の`admin recover index`と`admin check index`ステートメントをサポートします [＃17390](https://github.com/pingcap/tidb/pull/17390) [＃17315](https://github.com/pingcap/tidb/pull/17315)
    -   範囲パーティションテーブルの条件`in`のパーティションプルーニングをサポート [＃17318](https://github.com/pingcap/tidb/pull/17318)
    -   `SHOW CREATE TABLE`の出力を最適化し、パーティション名に引用符を追加します。 [＃16315](https://github.com/pingcap/tidb/pull/16315)
    -   `GROUP_CONCAT`関数の`ORDER BY`句をサポートする [＃16988](https://github.com/pingcap/tidb/pull/16988)
    -   `CMSketch`統計のメモリ割り当てメカニズムを最適化して、ガベージコレクション（GC）がパフォーマンスに与える影響を軽減する[＃17543](https://github.com/pingcap/tidb/pull/17543)

-   PD

    -   PDがリーダーの数に基づいてスケジュールを実行するポリシーを追加します。 [＃2479](https://github.com/pingcap/pd/pull/2479)

## バグ修正 {#bug-fixes}

-   TiDB

    -   ディープコピーを使用して、 `Hash`集計関数の`enum`と`set`型のデータをコピーします。正確性の問題を修正しました[＃16890](https://github.com/pingcap/tidb/pull/16890)
    -   整数オーバーフローの処理ロジックが間違っているため、 `PointGet`誤った結果を返す問題を修正しました [＃16753](https://github.com/pingcap/tidb/pull/16753)
    -   クエリ述語で関数`CHAR()`が使用されている場合に、誤った処理ロジックによって誤った結果が発生する問題を修正しました。 [＃16557](https://github.com/pingcap/tidb/pull/16557)
    -   `IsTrue`と`IsFalse`関数のストレージレイヤーと計算レイヤーで結果が一致しない問題を修正 [＃16627](https://github.com/pingcap/tidb/pull/16627)
    -   いくつかの式における誤った`NotNull`フラグ（ `case when` など）を修正します。 [＃16993](https://github.com/pingcap/tidb/pull/16993)
    -   一部のシナリオでオプティマイザが`TableDual`物理プランを見つけられない問題を修正[＃17014](https://github.com/pingcap/tidb/pull/17014)
    -   ハッシュパーティションテーブルでパーティション選択の構文が正しく反映されない問題を修正しました。 [＃17051](https://github.com/pingcap/tidb/pull/17051)
    -   浮動小数点数に対して XOR 演算を実行すると TiDB と MySQL の間で結果が一致しない問題を修正しました。 [＃16976](https://github.com/pingcap/tidb/pull/16976)
    -   準備された方法でDDL文を実行するときに発生するエラーを修正[＃17415](https://github.com/pingcap/tidb/pull/17415)
    -   IDアロケータのバッチサイズ計算の誤った処理ロジックを修正 [＃17548](https://github.com/pingcap/tidb/pull/17548)
    -   実行時間が大きいしきい値を超えたときに`MAX_EXEC_TIME`ヒントが有効にならない問題を修正 [＃17534](https://github.com/pingcap/tidb/pull/17534)

-   TiKV

    -   長時間実行後にメモリのデフラグが効かなくなる問題を修正[＃7790](https://github.com/tikv/tikv/pull/7790)
    -   TiKV が誤って再起動された後にスナップショットファイルを誤って削除することによって発生するpanicの問題を修正しました[＃7925](https://github.com/tikv/tikv/pull/7925)
    -   メッセージパッケージが大きすぎるために発生する gRPC の切断を修正[＃7822](https://github.com/tikv/tikv/pull/7822)
