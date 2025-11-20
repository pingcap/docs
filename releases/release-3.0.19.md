---
title: TiDB 3.0.19 Release Notes
summary: TiDB 3.0.19は2020年9月25日にリリースされました。互換性に関する変更には、インポートパスと著作権情報の更新が含まれます。障害回復の影響を軽減し、同時実行調整をサポートし、調整不可能な値を設定する機能強化が行われました。クエリエラー、権限チェック、型変更、制約チェック、テーブルロックの解放、演算子処理、panic解析に関するバグ修正も行われました。TiDB TiDB Lightningなどのツールでは、プロセス終了タイミングに関する修正も行われました。
---

# TiDB 3.0.19 リリースノート {#tidb-3-0-19-release-notes}

発売日：2020年9月25日

TiDBバージョン: 3.0.19

## 互換性の変更 {#compatibility-changes}

-   PD

    -   インポートパスを`pingcap/pd`から`tikv/pd` [＃2779](https://github.com/pingcap/pd/pull/2779)に変更します
    -   著作権情報を`PingCAP, Inc`から`TiKV Project Authors` [＃2777](https://github.com/pingcap/pd/pull/2777)に変更します

## 改善点 {#improvements}

-   ティドブ

    -   障害回復によるQPSパフォーマンスへの影響を軽減する[＃19764](https://github.com/pingcap/tidb/pull/19764)
    -   `union`演算子[＃19885](https://github.com/pingcap/tidb/pull/19885)の同時実行の調整をサポート

-   ティクブ

    -   `sync-log` ～ `true`を調整不可の値[＃8636](https://github.com/tikv/tikv/pull/8636)として設定する

-   PD

    -   PD再起動[＃2789](https://github.com/pingcap/pd/pull/2789)アラートルールを追加する

## バグ修正 {#bug-fixes}

-   ティドブ

    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正[＃20050](https://github.com/pingcap/tidb/pull/20050)
    -   `SHOW STATS_META`と`SHOW STATS_BUCKET`の権限チェックを追加する[＃19759](https://github.com/pingcap/tidb/pull/19759)
    -   小数型を整数型に変更することを禁止する[＃19681](https://github.com/pingcap/tidb/pull/19681)
    -   `ENUM`型列[＃20045](https://github.com/pingcap/tidb/pull/20045) `SET`変更する際に制約がチェックされない問題を修正
    -   panic後にtidb-serverがテーブルロックを解放しないバグを修正[＃20021](https://github.com/pingcap/tidb/pull/20021)
    -   `WHERE`節[＃19901](https://github.com/pingcap/tidb/pull/19901)で`OR`演算子が正しく処理されないバグを修正

-   ティクブ

    -   理由フレーズが欠落している応答を解析するときに TiKV がパニックを起こすバグを修正[＃8540](https://github.com/tikv/tikv/pull/8540)

-   ツール

    -   TiDB Lightning

        -   厳密モード[＃378](https://github.com/pingcap/tidb-lightning/pull/378)でCSVに無効なUTF文字が検出された場合、 TiDB Lightningプロセスが時間内に終了しない問題を修正しました。
