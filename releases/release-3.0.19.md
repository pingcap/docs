---
title: TiDB 3.0.19 Release Notes
---

# TiDB 3.0.19 リリースノート {#tidb-3-0-19-release-notes}

発売日：2020年9月25日

TiDB バージョン: 3.0.19

## 互換性の変更 {#compatibility-changes}

-   PD

    -   インポート パスを`pingcap/pd`から`tikv/pd` [#2779](https://github.com/pingcap/pd/pull/2779)に変更します
    -   著作権情報を`PingCAP, Inc`から`TiKV Project Authors` [#2777](https://github.com/pingcap/pd/pull/2777)に変更します

## 改良点 {#improvements}

-   TiDB

    -   QPS パフォーマンスに対する障害復旧の影響を軽減する[#19764](https://github.com/pingcap/tidb/pull/19764)
    -   `union`オペレーター[#19885](https://github.com/pingcap/tidb/pull/19885)の並行性の調整をサポート

-   TiKV

    -   `sync-log` ～ `true`を調整不可の値として設定[#8636](https://github.com/tikv/tikv/pull/8636)

-   PD

    -   PD 再起動[#2789](https://github.com/pingcap/pd/pull/2789)のアラート ルールを追加します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正[#20050](https://github.com/pingcap/tidb/pull/20050)
    -   `SHOW STATS_META`と`SHOW STATS_BUCKET` [#19759](https://github.com/pingcap/tidb/pull/19759)の権限チェックを追加
    -   10 進数型から整数型への変更を禁止する[#19681](https://github.com/pingcap/tidb/pull/19681)
    -   `ENUM`型の列を変更する`SET`制約がチェックされない問題を修正[#20045](https://github.com/pingcap/tidb/pull/20045)
    -   tidb-server がpanic後にテーブル ロックを解放しないバグを修正します[#20021](https://github.com/pingcap/tidb/pull/20021)
    -   `WHERE`節[#19901](https://github.com/pingcap/tidb/pull/19901)で`OR`演算子が正しく処理されないバグを修正

-   TiKV

    -   理由フレーズが欠落している応答を解析するときに TiKV がパニックになるバグを修正します[#8540](https://github.com/tikv/tikv/pull/8540)

-   ツール

    -   TiDB Lightning

        -   Strict モード[#378](https://github.com/pingcap/tidb-lightning/pull/378)で CSV に不正な UTF 文字が含まれている場合、 TiDB Lightningプロセスが時間内に終了しない問題を修正します。
