---
title: TiDB 3.0.18 Release Notes
---

# TiDB 3.0.18 リリースノート {#tidb-3-0-18-release-notes}

発売日：2020年8月21日

TiDB バージョン: 3.0.18

## 改善点 {#improvements}

-   ツール

    -   TiDBBinlog

        -   Pump GC 構成[#996](https://github.com/pingcap/tidb-binlog/pull/996)の Go の期間形式をサポートします。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `Hash`関数による`decimal`型の処理を誤ると、間違った HashJoin 結果が発生する問題を修正[#19185](https://github.com/pingcap/tidb/pull/19185)
    -   `Hash`関数による`set`と`enum`のタイプの処理が間違っていると、間違った HashJoin 結果が発生する問題を修正します[#19175](https://github.com/pingcap/tidb/pull/19175)
    -   悲観的ロックモード[#19236](https://github.com/pingcap/tidb/pull/19236)で重複キーのチェックに失敗する問題を修正
    -   `Apply`と`Union Scan`演算子により誤った実行結果が発生する問題を修正[#19297](https://github.com/pingcap/tidb/pull/19297)
    -   キャッシュされた実行プランの一部がトランザクション[#19274](https://github.com/pingcap/tidb/pull/19274)で誤って実行される問題を修正

-   TiKV

    -   GC 失敗ログを`error`から`warning`レベル[#8444](https://github.com/tikv/tikv/pull/8444)に変更します。

-   ツール

    -   TiDB Lightning

        -   `--log-file`引数が有効にならない問題を修正[#345](https://github.com/pingcap/tidb-lightning/pull/345)
        -   TiDB-backend [#357](https://github.com/pingcap/tidb-lightning/pull/357)を使用する場合の空のバイナリ/16 進リテラルの構文エラーを修正
        -   TiDB-backend [#368](https://github.com/pingcap/tidb-lightning/pull/368)使用時の予期しない`switch-mode`呼び出しを修正
