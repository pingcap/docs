---
title: TiDB 3.0.19 Release Notes
summary: TiDB 3.0.19は2020年9月25日にリリースされました。このバージョンでは、PDのインポートパスが変更され、著作権情報も変更されました。また、TiDB、TiKV、PDの改善点やバグの修正が含まれています。具体的には、QPSパフォーマンスの障害回復の影響を軽減し、同時実行性の調整をサポートするなどの改善があります。バグの修正では、クエリエラーやパニックの修正が含まれています。TiDB Lightningも厳密モードでの不正なUTF文字の検出問題が修正されています。
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

    -   QPS パフォーマンスに対する障害回復の影響を軽減する[#19764](https://github.com/pingcap/tidb/pull/19764)
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
