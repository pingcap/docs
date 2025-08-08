---
title: TiDB 3.0.18 Release Notes
summary: TiDB 3.0.18は2020年8月21日にリリースされました。このリリースには、TiDB Binlogの改善と、TiDBおよびTiKVのバグ修正が含まれています。TiDBのバグ修正には、小数点、集合、列挙型の処理に関する問題、重複キーとキャッシュされた実行プランに関する問題が含まれます。TiKVのバグ修正には、GC失敗ログレベルの変更が含まれます。TiDB TiDB Lightning、ログファイル引数、構文エラー、予期しない呼び出しに関する問題も修正されました。
---

# TiDB 3.0.18 リリースノート {#tidb-3-0-18-release-notes}

発売日：2020年8月21日

TiDB バージョン: 3.0.18

## 改善点 {#improvements}

-   ツール

    -   TiDBBinlog

        -   Pump GC 構成[＃996](https://github.com/pingcap/tidb-binlog/pull/996)の Go の時間期間形式をサポートします。

## バグ修正 {#bug-fixes}

-   TiDB

    -   `Hash`関数による`decimal`型の誤った処理により、HashJoin 結果が誤っている問題を修正[＃19185](https://github.com/pingcap/tidb/pull/19185)
    -   `Hash`関数による`set`と`enum`型の誤った処理により、HashJoinの結果が誤っている問題を修正しました[＃19175](https://github.com/pingcap/tidb/pull/19175)
    -   悲観的ロックモード[＃19236](https://github.com/pingcap/tidb/pull/19236)で重複キーのチェックが失敗する問題を修正
    -   `Apply`と`Union Scan`演算子が間違った実行結果を引き起こす問題を修正しました[＃19297](https://github.com/pingcap/tidb/pull/19297)
    -   トランザクション[＃19274](https://github.com/pingcap/tidb/pull/19274)で一部のキャッシュされた実行プランが誤って実行される問題を修正しました

-   TiKV

    -   GC失敗ログを`error`から`warning`レベル[＃8444](https://github.com/tikv/tikv/pull/8444)に変更する

-   ツール

    -   TiDB Lightning

        -   `--log-file`引数が有効にならない問題を修正[＃345](https://github.com/pingcap/tidb-lightning/pull/345)
        -   TiDB バックエンド[＃357](https://github.com/pingcap/tidb-lightning/pull/357)使用時の空のバイナリ/16 進リテラルの構文エラーを修正しました
        -   TiDBバックエンド[＃368](https://github.com/pingcap/tidb-lightning/pull/368)使用時の予期しない`switch-mode`呼び出しを修正
