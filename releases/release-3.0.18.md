---
title: TiDB 3.0.18 Release Notes
---

# TiDB3.0.18リリースノート {#tidb-3-0-18-release-notes}

発売日：2020年8月21日

TiDBバージョン：3.0.18

## 改善 {#improvements}

-   ツール

    -   TiDB Binlog

        -   ポンプGC構成のGoの継続時間形式をサポートする[＃996](https://github.com/pingcap/tidb-binlog/pull/996)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `Hash`関数による`decimal`タイプの誤った処理により、誤ったHashJoin結果が発生する問題を修正します[＃19185](https://github.com/pingcap/tidb/pull/19185)
    -   `Hash`関数による`set`型と`enum`型の誤った処理により、誤ったHashJoin結果[＃19175](https://github.com/pingcap/tidb/pull/19175)が発生する問題を修正します。
    -   悲観的ロックモードで重複キーのチェックが失敗する問題を修正します[＃19236](https://github.com/pingcap/tidb/pull/19236)
    -   `Apply`と`Union Scan`の演算子が間違った実行結果を引き起こす問題を修正します[＃19297](https://github.com/pingcap/tidb/pull/19297)
    -   一部のキャッシュされた実行プランがトランザクション[＃19274](https://github.com/pingcap/tidb/pull/19274)で誤って実行される問題を修正します

-   TiKV

    -   GC障害ログを`error`から`warning`レベル[＃8444](https://github.com/tikv/tikv/pull/8444)に変更します

-   ツール

    -   TiDB Lightning

        -   `--log-file`引数が有効にならない問題を修正します[＃345](https://github.com/pingcap/tidb-lightning/pull/345)
        -   TiDBバックエンド[＃357](https://github.com/pingcap/tidb-lightning/pull/357)を使用する場合の空のバイナリ/16進リテラルの構文エラーを修正します
        -   TiDBバックエンド[＃368](https://github.com/pingcap/tidb-lightning/pull/368)を使用する際の予期しない`switch-mode`の呼び出しを修正
