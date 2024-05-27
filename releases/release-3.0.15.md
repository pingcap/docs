---
title: TiDB 3.0.15 Release Notes
summary: TiDB 3.0.15 は 2020 年 6 月 5 日にリリースされました。新機能には、パーティション テーブルでの admin recovery index および admin check index ステートメントのサポート、およびメモリ割り当てメカニズムの最適化が含まれます。バグ修正では、浮動小数点数で XOR 演算を行うときに PointGet で結果が不正確になったり、TiDB と MySQL の間で結果が一致しなくなったりする問題が修正されています。TiKV では、メモリのデフラグと gRPC の切断に関連する問題が修正されています。
---

# TiDB 3.0.15 リリースノート {#tidb-3-0-15-release-notes}

発売日: 2020年6月5日

TiDB バージョン: 3.0.15

## 新機能 {#new-features}

-   ティビ

    -   パーティションテーブル内のクエリでプランキャッシュ機能の使用を禁止する[＃16759](https://github.com/pingcap/tidb/pull/16759)
    -   パーティションテーブル[＃17315](https://github.com/pingcap/tidb/pull/17315) [＃17390](https://github.com/pingcap/tidb/pull/17390)の`admin recover index`と`admin check index`ステートメントをサポートする
    -   範囲パーティション化されたテーブル[＃17318](https://github.com/pingcap/tidb/pull/17318)の`in`条件のパーティション プルーニングをサポート
    -   `SHOW CREATE TABLE`の出力を最適化し、パーティション名[＃16315](https://github.com/pingcap/tidb/pull/16315)に引用符を追加します。
    -   `GROUP_CONCAT`関数[＃16988](https://github.com/pingcap/tidb/pull/16988)の`ORDER BY`節をサポートする
    -   `CMSketch`統計のメモリ割り当てメカニズムを最適化して、ガベージコレクション（GC）がパフォーマンスに与える影響を軽減する[＃17543](https://github.com/pingcap/tidb/pull/17543)

-   PD

    -   PDがリーダー数に応じてスケジュールを実行するポリシーを追加する[＃2479](https://github.com/pingcap/pd/pull/2479)

## バグの修正 {#bug-fixes}

-   ティビ

    -   ディープコピーを使用して、 `Hash`集計関数の`enum`と`set`型のデータをコピーします。正確性の問題を修正しました[＃16890](https://github.com/pingcap/tidb/pull/16890)
    -   整数オーバーフロー[＃16753](https://github.com/pingcap/tidb/pull/16753)の処理ロジックが間違っているため、 `PointGet`誤った結果を返す問題を修正しました。
    -   クエリ述語[＃16557](https://github.com/pingcap/tidb/pull/16557)で`CHAR()`関数が使用されている場合に、誤った処理ロジックによって誤った結果が発生する問題を修正しました。
    -   `IsTrue`と`IsFalse`の関数[＃16627](https://github.com/pingcap/tidb/pull/16627)のstorageレイヤーと計算レイヤーで結果が一致しない問題を修正
    -   いくつかの式で誤った`NotNull`フラグを修正します (例: `case when` [＃16993](https://github.com/pingcap/tidb/pull/16993)
    -   一部のシナリオでオプティマイザが`TableDual`の物理プランを見つけられない問題を修正[＃17014](https://github.com/pingcap/tidb/pull/17014)
    -   ハッシュパーティションテーブル[＃17051](https://github.com/pingcap/tidb/pull/17051)でパーティション選択の構文が正しく反映されない問題を修正
    -   浮動小数点数[＃16976](https://github.com/pingcap/tidb/pull/16976)に対して XOR 演算を実行すると TiDB と MySQL の間で結果が矛盾する問題を修正
    -   準備された方法でDDL文を実行するときに発生するエラーを修正[＃17415](https://github.com/pingcap/tidb/pull/17415)
    -   IDアロケータ[＃17548](https://github.com/pingcap/tidb/pull/17548)のバッチサイズ計算の誤った処理ロジックを修正
    -   時間が高価なしきい値[＃17534](https://github.com/pingcap/tidb/pull/17534)を超えると`MAX_EXEC_TIME`ヒントが有効にならない問題を修正

-   ティクヴ

    -   長時間実行後にメモリのデフラグが効かなくなる問題を修正[＃7790](https://github.com/tikv/tikv/pull/7790)
    -   TiKV が誤って再起動された後にスナップショット ファイルを誤って削除することで発生するpanic問題を修正しました[＃7925](https://github.com/tikv/tikv/pull/7925)
    -   メッセージ パッケージが大きすぎるために発生する gRPC 切断を修正[＃7822](https://github.com/tikv/tikv/pull/7822)
