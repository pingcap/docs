---
title: TiDB 3.0.7 Release Notes
summary: TiDB 3.0.7は2019年12月4日にリリースされました。ロックTTL、タイムゾーン解析、結果精度、データ精度、統計精度に関する問題の修正が含まれています。TiKVにもアップデートが適用され、デッドロック検出が改善され、メモリリークの問題が解決されました。
---

# TiDB 3.0.7 リリースノート {#tidb-3-0-7-release-notes}

発売日：2019年12月4日

TiDB バージョン: 3.0.7

TiDB Ansible バージョン: 3.0.7

## TiDB {#tidb}

-   TiDBサーバーのローカル時間がPDのタイムスタンプ[＃13868](https://github.com/pingcap/tidb/pull/13868)より遅れているためにロックTTLの値が大きすぎる問題を修正しました
-   `gotime.Local` [＃13793](https://github.com/pingcap/tidb/pull/13793)を使用して文字列から日付を解析した後にタイムゾーンが正しくない問題を修正しました
-   `builtinIntervalRealSig` [＃13767](https://github.com/pingcap/tidb/pull/13767)の実装で`binSearch`関数がエラーを返さないため、結果が正しくない可能性がある問題を修正しました。
-   整数を符号なし浮動小数点型または小数型に変換すると精度が失われ、データが正しくなくなる問題を修正[＃13755](https://github.com/pingcap/tidb/pull/13755)
-   Natural Outer JoinとOuter Join [＃13739](https://github.com/pingcap/tidb/pull/13739)で`USING`節が使用されている場合に`not null`フラグが適切にリセットされないため、結果が正しくないという問題を修正しました。
-   統計情報の更新時にデータ競合が発生し、統計情報が正確でない問題を修正しました[＃13687](https://github.com/pingcap/tidb/pull/13687)

## TiKV {#tikv}

-   デッドロック検出器が有効な領域のみを監視するようにして、デッドロックマネージャが有効なリージョン[＃6110](https://github.com/tikv/tikv/pull/6110)にあることを確認します。
-   潜在的なメモリリークの問題を修正[＃6128](https://github.com/tikv/tikv/pull/6128)
