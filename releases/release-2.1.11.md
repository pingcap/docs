---
title: TiDB 2.1.11 Release Notes
---

# TiDB 2.1.11 リリースノート {#tidb-2-1-11-release-notes}

リリース日: 2019 年 6 月 3 日

TiDB バージョン: 2.1.11

TiDB アンシブル バージョン: 2.1.11

## TiDB {#tidb}

-   `delete from join` [#10595](https://github.com/pingcap/tidb/pull/10595)に誤ったスキーマが使用される問題を修正
-   ビルトイン`CONVERT()`間違ったフィールド タイプ[#10263](https://github.com/pingcap/tidb/pull/10263)を返すことがある問題を修正
-   バケット数[#10569](https://github.com/pingcap/tidb/pull/10569)の更新時に重複していないフィードバックをマージする
-   `unix_timestamp()-unix_timestamp(now())` [#10491](https://github.com/pingcap/tidb/pull/10491)の計算エラーを修正
-   `period_diff`の MySQL 8.0 との非互換性の問題を修正[#10501](https://github.com/pingcap/tidb/pull/10501)
-   例外を避けるために統計を収集するときは`Virtual Column`スキップします[#10628](https://github.com/pingcap/tidb/pull/10628)
-   `SHOW OPEN TABLES`ステートメント[#10374](https://github.com/pingcap/tidb/pull/10374)をサポート
-   場合によってはゴルーチンリークが発生する問題を修正[#10656](https://github.com/pingcap/tidb/pull/10656)
-   場合によっては`tidb_snapshot`変数を設定すると、時刻形式[#10637](https://github.com/pingcap/tidb/pull/10637)が正しく解析されない可能性があるという問題を修正します。

## PD {#pd}

-   `balance-region` [#1551](https://github.com/pingcap/pd/pull/1551)が原因で hotsリージョンがスケジュールに失敗する可能性がある問題を修正します
-   ホットスポット関連のスケジューリング優先度を高い[#1551](https://github.com/pingcap/pd/pull/1551)に設定します
-   2 つの構成アイテムを追加する[#1551](https://github.com/pingcap/pd/pull/1551)
    -   同時ホットスポット スケジューリング タスクの最大数を制御する場合は`hot-region-schedule-limit`
    -   `hot-region-cache-hits-threshold`はホットリージョンを識別する

## TiKV {#tikv}

-   リーダーが 1 人、学習者が 1 人しかいない場合、学習者が空のインデックスを読み取る問題を修正します[#4751](https://github.com/tikv/tikv/pull/4751)
-   通常の優先度[#4791](https://github.com/tikv/tikv/pull/4791)のコマンドへの影響を軽減するために、優先度の高いスレッド プール内のプロセス`ScanLock`と`ResolveLock`
-   受信したスナップショットのすべてのファイルを同期する[#4811](https://github.com/tikv/tikv/pull/4811)

## ツール {#tools}

-   TiDBBinlog
    -   GC 中のデータ削除速度を制限して、 `WritePause` [#620](https://github.com/pingcap/tidb-binlog/pull/620)による QPS の低下を回避します。

## TiDB アンシブル {#tidb-ansible}

-   Drainerパラメータの追加[#760](https://github.com/pingcap/tidb-ansible/pull/760)
