---
title: TiDB 3.0.7 Release Notes
---

# TiDB 3.0.7 リリースノート {#tidb-3-0-7-release-notes}

発売日：2019年12月4日

TiDB バージョン: 3.0.7

TiDB Ansible バージョン: 3.0.7

## TiDB {#tidb}

-   TiDB サーバーのローカル時間が PD のタイムスタンプ[<a href="https://github.com/pingcap/tidb/pull/13868">#13868</a>](https://github.com/pingcap/tidb/pull/13868)より遅れているため、ロック TTL の値が大きすぎる問題を修正
-   `gotime.Local` [<a href="https://github.com/pingcap/tidb/pull/13793">#13793</a>](https://github.com/pingcap/tidb/pull/13793)を使用して文字列から日付を解析した後にタイムゾーンが正しくなくなる問題を修正
-   `builtinIntervalRealSig` [<a href="https://github.com/pingcap/tidb/pull/13767">#13767</a>](https://github.com/pingcap/tidb/pull/13767)の実装において`binSearch`関数がエラーを返さないため、結果が正しくない場合がある問題を修正
-   整数を符号なし浮動小数点または 10 進数型[<a href="https://github.com/pingcap/tidb/pull/13755">#13755</a>](https://github.com/pingcap/tidb/pull/13755)に変換すると精度が失われるため、データが正しくなくなる問題を修正
-   NaturalOuterJoinおよび[<a href="https://github.com/pingcap/tidb/pull/13739">#13739</a>](https://github.com/pingcap/tidb/pull/13739)で`USING`句を使用した場合に`not null`フラグが正しくリセットされず、結果が正しくない問題を修正
-   統計更新時にデータ競合が発生し、統計が不正確になる問題を修正[<a href="https://github.com/pingcap/tidb/pull/13687">#13687</a>](https://github.com/pingcap/tidb/pull/13687)

## TiKV {#tikv}

-   デッドロック マネージャーが有効なリージョン[<a href="https://github.com/tikv/tikv/pull/6110">#6110</a>](https://github.com/tikv/tikv/pull/6110)にあることを確認するために、デッドロック ディテクタが有効なリージョンのみを監視するようにします。
-   潜在的なメモリリークの問題を修正します[<a href="https://github.com/tikv/tikv/pull/6128">#6128</a>](https://github.com/tikv/tikv/pull/6128)
