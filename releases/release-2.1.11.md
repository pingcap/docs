---
title: TiDB 2.1.11 Release Notes
summary: TiDB 2.1.11 は、2019 年 6 月 3 日にリリースされました。これには、TiDB、PD、TiKV、およびツールのさまざまな問題に対する修正が含まれています。主な修正としては、結合からの削除における不正なスキーマの修正、unix_timestamp() の計算エラー、および TiDB Ansible へのDrainerパラメータの追加などがあります。
---

# TiDB 2.1.11 リリースノート {#tidb-2-1-11-release-notes}

発売日: 2019年6月3日

TiDB バージョン: 2.1.11

TiDB Ansible バージョン: 2.1.11

## ティビ {#tidb}

-   `delete from join` [＃10595](https://github.com/pingcap/tidb/pull/10595)に誤ったスキーマが使用される問題を修正
-   組み込み`CONVERT()`が誤ったフィールド タイプ[＃10263](https://github.com/pingcap/tidb/pull/10263)を返す可能性がある問題を修正しました。
-   バケット数[＃10569](https://github.com/pingcap/tidb/pull/10569)を更新するときに重複していないフィードバックをマージする
-   `unix_timestamp()-unix_timestamp(now())` [＃10491](https://github.com/pingcap/tidb/pull/10491)の計算エラーを修正
-   MySQL 8.0 [＃10501](https://github.com/pingcap/tidb/pull/10501)との`period_diff`互換性の問題を修正
-   例外を避けるために統計を収集するときに`Virtual Column`スキップする[＃10628](https://github.com/pingcap/tidb/pull/10628)
-   `SHOW OPEN TABLES`ステートメント[＃10374](https://github.com/pingcap/tidb/pull/10374)支持する
-   場合によっては goroutine リークが発生する問題を修正[＃10656](https://github.com/pingcap/tidb/pull/10656)
-   `tidb_snapshot`変数を設定すると、場合によっては時間形式[＃10637](https://github.com/pingcap/tidb/pull/10637)の解析が正しく行われない可能性がある問題を修正しました。

## PD {#pd}

-   `balance-region` [＃1551](https://github.com/pingcap/pd/pull/1551)が原因でホットリージョンのスケジュールが失敗する可能性がある問題を修正しました。
-   ホットスポット関連のスケジュール優先度を高[＃1551](https://github.com/pingcap/pd/pull/1551)に設定する
-   2つの構成項目[＃1551](https://github.com/pingcap/pd/pull/1551)を追加する
    -   `hot-region-schedule-limit`同時ホットスポット スケジューリング タスクの最大数を制御します
    -   ホットリージョンを識別するには`hot-region-cache-hits-threshold`

## ティクヴ {#tikv}

-   リーダーと学習者が 1 人ずつしかいない場合に学習者が空のインデックスを読み取る問題を修正しました[＃4751](https://github.com/tikv/tikv/pull/4751)
-   スレッドプール内のプロセス`ScanLock`と`ResolveLock`高優先度に設定し、通常優先度[＃4791](https://github.com/tikv/tikv/pull/4791)のコマンドへの影響を軽減する
-   受信したスナップショット[＃4811](https://github.com/tikv/tikv/pull/4811)のすべてのファイルを同期する

## ツール {#tools}

-   TiDBBinlog
    -   GC中のデータ削除速度を制限し、 `WritePause` [＃620](https://github.com/pingcap/tidb-binlog/pull/620)によるQPSの低下を回避する

## TiDB アンシブル {#tidb-ansible}

-   Drainerパラメータ[＃760](https://github.com/pingcap/tidb-ansible/pull/760)を追加
