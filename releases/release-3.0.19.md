---
title: TiDB 3.0.19 Release Notes
---

# TiDB 3.0.19 リリースノート {#tidb-3-0-19-release-notes}

発売日：2020年9月25日

TiDB バージョン: 3.0.19

## 互換性の変更 {#compatibility-changes}

-   PD

    -   インポート パスを`pingcap/pd`から`tikv/pd`に変更します[<a href="https://github.com/pingcap/pd/pull/2779">#2779</a>](https://github.com/pingcap/pd/pull/2779)
    -   著作権情報を`PingCAP, Inc`から`TiKV Project Authors`に変更します[<a href="https://github.com/pingcap/pd/pull/2777">#2777</a>](https://github.com/pingcap/pd/pull/2777)

## 改善点 {#improvements}

-   TiDB

    -   QPS パフォーマンスに対する障害回復の影響を軽減する[<a href="https://github.com/pingcap/tidb/pull/19764">#19764</a>](https://github.com/pingcap/tidb/pull/19764)
    -   `union`オペレーター[<a href="https://github.com/pingcap/tidb/pull/19885">#19885</a>](https://github.com/pingcap/tidb/pull/19885)の同時実行性の調整をサポート

-   TiKV

    -   `sync-log` ～ `true`を調整不可能な値として設定します[<a href="https://github.com/tikv/tikv/pull/8636">#8636</a>](https://github.com/tikv/tikv/pull/8636)

-   PD

    -   PD 再起動[<a href="https://github.com/pingcap/pd/pull/2789">#2789</a>](https://github.com/pingcap/pd/pull/2789)のアラート ルールを追加します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正[<a href="https://github.com/pingcap/tidb/pull/20050">#20050</a>](https://github.com/pingcap/tidb/pull/20050)
    -   `SHOW STATS_META`と`SHOW STATS_BUCKET`の権限チェックを追加[<a href="https://github.com/pingcap/tidb/pull/19759">#19759</a>](https://github.com/pingcap/tidb/pull/19759)
    -   10 進数型から整数型[<a href="https://github.com/pingcap/tidb/pull/19681">#19681</a>](https://github.com/pingcap/tidb/pull/19681)への変更を禁止します。
    -   `ENUM`型の列[<a href="https://github.com/pingcap/tidb/pull/20045">#20045</a>](https://github.com/pingcap/tidb/pull/20045)を変更する際に制約がチェックされない問題`SET`修正
    -   panic[<a href="https://github.com/pingcap/tidb/pull/20021">#20021</a>](https://github.com/pingcap/tidb/pull/20021)の後に tidb-server がテーブルのロックを解放しないバグを修正
    -   `WHERE`節[<a href="https://github.com/pingcap/tidb/pull/19901">#19901</a>](https://github.com/pingcap/tidb/pull/19901)で`OR`演算子が正しく処理されないバグを修正

-   TiKV

    -   理由フレーズ[<a href="https://github.com/tikv/tikv/pull/8540">#8540</a>](https://github.com/tikv/tikv/pull/8540)が欠落している応答を解析すると TiKV がパニックになるバグを修正

-   ツール

    -   TiDB Lightning

        -   厳密モード[<a href="https://github.com/pingcap/tidb-lightning/pull/378">#378</a>](https://github.com/pingcap/tidb-lightning/pull/378)で CSV 内に不正な UTF 文字が検出された場合に、 TiDB Lightningプロセスが時間内に終了しない問題を修正しました。
