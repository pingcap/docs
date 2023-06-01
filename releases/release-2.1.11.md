---
title: TiDB 2.1.11 Release Notes
---

# TiDB 2.1.11 リリースノート {#tidb-2-1-11-release-notes}

発売日：2019年6月3日

TiDB バージョン: 2.1.11

TiDB Ansible バージョン: 2.1.11

## TiDB {#tidb}

-   `delete from join` [#10595](https://github.com/pingcap/tidb/pull/10595)に間違ったスキーマが使用される問題を修正
-   組み込み`CONVERT()`間違ったフィールド タイプ[#10263](https://github.com/pingcap/tidb/pull/10263)を返す可能性がある問題を修正
-   バケット数[#10569](https://github.com/pingcap/tidb/pull/10569)を更新するときに重複しないフィードバックをマージします
-   `unix_timestamp()-unix_timestamp(now())` [#10491](https://github.com/pingcap/tidb/pull/10491)の計算エラーを修正
-   `period_diff`と MySQL 8.0 [#10501](https://github.com/pingcap/tidb/pull/10501)の非互換性の問題を修正します。
-   例外を避けるために統計を収集するときは`Virtual Column`スキップします[#10628](https://github.com/pingcap/tidb/pull/10628)
-   `SHOW OPEN TABLES`ステートメント[#10374](https://github.com/pingcap/tidb/pull/10374)をサポートします
-   場合によっては goroutine リークが発生することがある問題を修正[#10656](https://github.com/pingcap/tidb/pull/10656)
-   場合によっては`tidb_snapshot`変数を設定すると、時刻形式[#10637](https://github.com/pingcap/tidb/pull/10637)の解析が正しく行われない問題を修正します。

## PD {#pd}

-   `balance-region` [#1551](https://github.com/pingcap/pd/pull/1551)により hotsリージョンのスケジュールが失敗する場合がある問題を修正
-   ホットスポット関連のスケジュール優先順位を高[#1551](https://github.com/pingcap/pd/pull/1551)に設定します。
-   2 つの構成アイテムを追加[#1551](https://github.com/pingcap/pd/pull/1551)
    -   `hot-region-schedule-limit` : 同時ホットスポット スケジューリング タスクの最大数を制御します。
    -   ホットリージョンを識別する場合は`hot-region-cache-hits-threshold`

## TiKV {#tikv}

-   リーダーと学習者が 1 人だけの場合、学習者が空のインデックスを読み取る問題を修正します[#4751](https://github.com/tikv/tikv/pull/4751)
-   スレッド プール内の`ScanLock`と`ResolveLock`高い優先度で処理し、通常の優先度[#4791](https://github.com/tikv/tikv/pull/4791)のコマンドへの影響を軽減します。
-   受信したスナップショットのすべてのファイルを同期します[#4811](https://github.com/tikv/tikv/pull/4811)

## ツール {#tools}

-   TiDBBinlog
    -   `WritePause` [#620](https://github.com/pingcap/tidb-binlog/pull/620)による QPS の低下を避けるために、GC 中のデータ削除速度を制限します。

## TiDB Ansible {#tidb-ansible}

-   Drainerパラメータの追加[#760](https://github.com/pingcap/tidb-ansible/pull/760)
