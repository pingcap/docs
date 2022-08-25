---
title: TiDB 3.0.7 Release Notes
---

# TiDB 3.0.7 リリースノート {#tidb-3-0-7-release-notes}

発売日：2019年12月4日

TiDB バージョン: 3.0.7

TiDB アンシブル バージョン: 3.0.7

## TiDB {#tidb}

-   TiDB サーバーのローカル時刻が PD のタイムスタンプ[#13868](https://github.com/pingcap/tidb/pull/13868)より遅れているため、ロック TTL の値が大きすぎる問題を修正します。
-   `gotime.Local` [#13793](https://github.com/pingcap/tidb/pull/13793)を使用して文字列から日付を解析した後、タイムゾーンが正しくない問題を修正します
-   `builtinIntervalRealSig` [#13767](https://github.com/pingcap/tidb/pull/13767)の実装で`binSearch`関数がエラーを返さないため、結果が正しくない場合がある問題を修正
-   整数を符号なし浮動小数点や 10 進数に変換すると精度が失われ、データが正しくなくなる問題を修正[#13755](https://github.com/pingcap/tidb/pull/13755)
-   Natural Outer Join と Outer Join [#13739](https://github.com/pingcap/tidb/pull/13739)で`USING`句を使用すると、 `not null`フラグが正しくリセットされず、結果が正しくない問題を修正
-   統計更新時にデータ競合が発生し、統計が正確でない問題を修正[#13687](https://github.com/pingcap/tidb/pull/13687)

## TiKV {#tikv}

-   デッドロック ディテクターが有効なリージョンのみを監視するようにして、デッドロック マネージャーが有効なリージョン[#6110](https://github.com/tikv/tikv/pull/6110)にあることを確認します。
-   潜在的なメモリ リークの問題を修正する[#6128](https://github.com/tikv/tikv/pull/6128)
