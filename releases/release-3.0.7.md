---
title: TiDB 3.0.7 Release Notes
---

# TiDB3.0.7リリースノート {#tidb-3-0-7-release-notes}

発売日：2019年12月4日

TiDBバージョン：3.0.7

TiDB Ansibleバージョン：3.0.7

## TiDB {#tidb}

-   TiDBサーバーの現地時間がPDのタイムスタンプより遅れているためにロックTTLの値が大きすぎるという問題を修正します[＃13868](https://github.com/pingcap/tidb/pull/13868)
-   `gotime.Local` [＃13793](https://github.com/pingcap/tidb/pull/13793)を使用して文字列から日付を解析した後、タイムゾーンが正しくない問題を修正します
-   `binSearch`関数は[＃13767](https://github.com/pingcap/tidb/pull/13767)の実装でエラーを返さないため、結果が正しくない可能性があるという問題を修正し`builtinIntervalRealSig` 。
-   整数を符号なし浮動小数点または10進型[＃13755](https://github.com/pingcap/tidb/pull/13755)に変換すると精度が失われるため、データが正しくないという問題を修正します。
-   NaturalOuterJoinおよびOuterJoin5で`USING`句を使用すると、 `not null`フラグが適切にリセットされないため、結果が正しくない問題を修正し[＃13739](https://github.com/pingcap/tidb/pull/13739) 。
-   統計が更新されるとデータ競合が発生するため、統計が正確でない問題を修正します[＃13687](https://github.com/pingcap/tidb/pull/13687)

## TiKV {#tikv}

-   デッドロック検出器が有効なリージョンのみを監視するようにして、デッドロックマネージャーが有効なリージョン[＃6110](https://github.com/tikv/tikv/pull/6110)にあることを確認します。
-   潜在的なメモリリークの問題を修正する[＃6128](https://github.com/tikv/tikv/pull/6128)
