---
title: TiDB 2.1.11 Release Notes
---

# TiDB2.1.11リリースノート {#tidb-2-1-11-release-notes}

発売日：2019年6月3日

TiDBバージョン：2.1.11

TiDB Ansibleバージョン：2.1.11

## TiDB {#tidb}

-   [＃10595](https://github.com/pingcap/tidb/pull/10595)に誤ったスキーマが使用される問題を修正し`delete from join`
-   組み込み`CONVERT()`が誤ったフィールドタイプ[＃10263](https://github.com/pingcap/tidb/pull/10263)を返す可能性がある問題を修正します
-   バケット数[＃10569](https://github.com/pingcap/tidb/pull/10569)を更新するときに、重複していないフィードバックをマージします
-   `unix_timestamp()-unix_timestamp(now())`の計算エラーを[＃10491](https://github.com/pingcap/tidb/pull/10491)
-   `period_diff`の非互換性の問題をMySQL8.03と修正し[＃10501](https://github.com/pingcap/tidb/pull/10501)
-   例外を回避するために統計を収集するときは`Virtual Column`をスキップしてください[＃10628](https://github.com/pingcap/tidb/pull/10628)
-   `SHOW OPEN TABLES`ステートメント[＃10374](https://github.com/pingcap/tidb/pull/10374)をサポートする
-   場合によってはゴルーチンリークが発生する可能性があるという問題を修正します[＃10656](https://github.com/pingcap/tidb/pull/10656)
-   場合によっては`tidb_snapshot`変数を設定すると、時間形式[＃10637](https://github.com/pingcap/tidb/pull/10637)の誤った解析が発生する可能性があるという問題を修正します。

## PD {#pd}

-   13が原因で`balance-region`のスケジュールが失敗する可能性がある問題を修正し[＃1551](https://github.com/pingcap/pd/pull/1551)
-   ホットスポット関連のスケジューリングの優先順位を高い[＃1551](https://github.com/pingcap/pd/pull/1551)に設定します
-   2つの構成アイテムを追加する[＃1551](https://github.com/pingcap/pd/pull/1551)
    -   `hot-region-schedule-limit`は、同時ホットスポットスケジューリングタスクの最大数を制御します
    -   `hot-region-cache-hits-threshold`は、ホットリージョンを識別します

## TiKV {#tikv}

-   リーダーと学習者が1人だけの場合に学習者が空のインデックスを読み取る問題を修正します[＃4751](https://github.com/tikv/tikv/pull/4751)
-   通常の優先度[＃4791](https://github.com/tikv/tikv/pull/4791)のコマンドへの影響を減らすために、優先度の高いスレッドプールでプロセス`ScanLock`と`ResolveLock`を実行します。
-   受信したスナップショットのすべてのファイルを同期する[＃4811](https://github.com/tikv/tikv/pull/4811)

## ツール {#tools}

-   TiDB Binlog
    -   `WritePause` [＃620](https://github.com/pingcap/tidb-binlog/pull/620)によって引き起こされるQPSの低下を回避するために、GC中のデータ削除速度を制限します。

## TiDB Ansible {#tidb-ansible}

-   Drainerパラメータの追加[＃760](https://github.com/pingcap/tidb-ansible/pull/760)
