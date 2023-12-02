---
title: TiDB 3.0.7 Release Notes
---

# TiDB 3.0.7 リリースノート {#tidb-3-0-7-release-notes}

発売日：2019年12月4日

TiDB バージョン: 3.0.7

TiDB Ansible バージョン: 3.0.7

## TiDB {#tidb}

-   TiDB サーバーのローカル時間が PD のタイムスタンプ[#13868](https://github.com/pingcap/tidb/pull/13868)より遅れているため、ロック TTL の値が大きすぎる問題を修正
-   `gotime.Local` [#13793](https://github.com/pingcap/tidb/pull/13793)を使用して文字列から日付を解析した後にタイムゾーンが正しくなくなる問題を修正
-   `builtinIntervalRealSig` [#13767](https://github.com/pingcap/tidb/pull/13767)の実装において`binSearch`関数がエラーを返さないため、結果が正しくない場合がある問題を修正
-   整数を符号なし浮動小数点または 10 進数型[#13755](https://github.com/pingcap/tidb/pull/13755)に変換すると精度が失われるため、データが正しくなくなる問題を修正
-   Natural external join および external join [#13739](https://github.com/pingcap/tidb/pull/13739)で`USING`句が使用されている場合、 `not null`フラグが適切にリセットされないため、結果が正しくない問題を修正します。
-   統計更新時にデータ競合が発生し、統計が不正確になる問題を修正[#13687](https://github.com/pingcap/tidb/pull/13687)

## TiKV {#tikv}

-   デッドロック マネージャーが有効なリージョン[#6110](https://github.com/tikv/tikv/pull/6110)にあることを確認するために、デッドロック ディテクタが有効なリージョンのみを監視するようにします。
-   潜在的なメモリリークの問題を修正します[#6128](https://github.com/tikv/tikv/pull/6128)
