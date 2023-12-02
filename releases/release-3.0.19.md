---
title: TiDB 3.0.19 Release Notes
---

# TiDB 3.0.19 リリースノート {#tidb-3-0-19-release-notes}

発売日：2020年9月25日

TiDB バージョン: 3.0.19

## 互換性の変更 {#compatibility-changes}

-   PD

    -   インポート パスを`pingcap/pd`から`tikv/pd`に変更します[#2779](https://github.com/pingcap/pd/pull/2779)
    -   著作権情報を`PingCAP, Inc`から`TiKV Project Authors`に変更します[#2777](https://github.com/pingcap/pd/pull/2777)

## 改善点 {#improvements}

-   TiDB

    -   障害回復による QPS パフォーマンスへの影響を軽減[#19764](https://github.com/pingcap/tidb/pull/19764)
    -   `union`オペレーター[#19885](https://github.com/pingcap/tidb/pull/19885)の同時実行性の調整をサポート

-   TiKV

    -   `sync-log` ～ `true`を調整不可能な値として設定します[#8636](https://github.com/tikv/tikv/pull/8636)

-   PD

    -   PD 再起動[#2789](https://github.com/pingcap/pd/pull/2789)のアラート ルールを追加します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正[#20050](https://github.com/pingcap/tidb/pull/20050)
    -   `SHOW STATS_META`と`SHOW STATS_BUCKET`の権限チェックを追加[#19759](https://github.com/pingcap/tidb/pull/19759)
    -   10 進数型から整数型[#19681](https://github.com/pingcap/tidb/pull/19681)への変更を禁止します。
    -   `ENUM`型`SET`列[#20045](https://github.com/pingcap/tidb/pull/20045)を変更する際に制約がチェックされない問題を修正
    -   panic[#20021](https://github.com/pingcap/tidb/pull/20021)の後に tidb-server がテーブルのロックを解放しないバグを修正
    -   `WHERE`節[#19901](https://github.com/pingcap/tidb/pull/19901)で`OR`演算子が正しく処理されないバグを修正

-   TiKV

    -   理由フレーズ[#8540](https://github.com/tikv/tikv/pull/8540)が欠落している応答を解析すると TiKV がパニックになるバグを修正

-   ツール

    -   TiDB Lightning

        -   厳密モード[#378](https://github.com/pingcap/tidb-lightning/pull/378)で CSV 内に不正な UTF 文字が検出された場合に、 TiDB Lightningプロセスが時間内に終了しない問題を修正しました。
