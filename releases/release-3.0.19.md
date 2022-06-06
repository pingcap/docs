---
title: TiDB 3.0.19 Release Notes
---

# TiDB3.0.19リリースノート {#tidb-3-0-19-release-notes}

発売日：2020年9月25日

TiDBバージョン：3.0.19

## 互換性の変更 {#compatibility-changes}

-   PD

    -   インポートパスを`pingcap/pd`から[＃2779](https://github.com/pingcap/pd/pull/2779)に変更し`tikv/pd`
    -   著作権情報を`PingCAP, Inc`から[＃2777](https://github.com/pingcap/pd/pull/2777)に変更し`TiKV Project Authors`

## 改善 {#improvements}

-   TiDB

    -   QPSパフォーマンスに対する障害回復の影響を軽減する[＃19764](https://github.com/pingcap/tidb/pull/19764)
    -   `union`演算子の同時実行性の調整をサポート[＃19885](https://github.com/pingcap/tidb/pull/19885)

-   TiKV

    -   調整不可能な`true` `sync-log`設定します[＃8636](https://github.com/tikv/tikv/pull/8636)

-   PD

    -   PD再起動のアラートルールを追加する[＃2789](https://github.com/pingcap/pd/pull/2789)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `slow-log`ファイルが存在しない場合に発生するクエリエラーを修正します[＃20050](https://github.com/pingcap/tidb/pull/20050)
    -   `SHOW STATS_META`と[＃19759](https://github.com/pingcap/tidb/pull/19759)の特権チェックを追加し`SHOW STATS_BUCKET`
    -   10進数タイプを整数タイプ[＃19681](https://github.com/pingcap/tidb/pull/19681)に変更することを禁止します
    -   `ENUM`タイプの列`SET`を変更するときに制約がチェックされない問題を修正し[＃20045](https://github.com/pingcap/tidb/pull/20045)
    -   パニック後にtidb-serverがテーブルロックを解放しないバグを修正します[＃20021](https://github.com/pingcap/tidb/pull/20021)
    -   `WHERE`節[＃19901](https://github.com/pingcap/tidb/pull/19901)で`OR`演算子が正しく処理されないバグを修正します。

-   TiKV

    -   理由フレーズが欠落している応答を解析するときにTiKVがパニックになるバグを修正します[＃8540](https://github.com/tikv/tikv/pull/8540)

-   ツール

    -   TiDB Lightning

        -   厳密モード[＃378](https://github.com/pingcap/tidb-lightning/pull/378)でCSVで不正なUTF文字に遭遇したときに、TiDBLightningプロセスが時間内に終了しない問題を修正します。
