---
title: TiDB 2.1.11 Release Notes
summary: TiDB 2.1.11は2019年6月3日にリリースされました。TiDB、PD、TiKV、ツールにおける様々な問題の修正が含まれています。主な修正点としては、結合からの削除におけるスキーマの誤り、unix_timestamp()の計算エラー、TiDB AnsibleへのDrainerパラメータの追加などが挙げられます。
---

# TiDB 2.1.11 リリースノート {#tidb-2-1-11-release-notes}

発売日：2019年6月3日

TiDB バージョン: 2.1.11

TiDB Ansible バージョン: 2.1.11

## TiDB {#tidb}

-   `delete from join` に誤ったスキーマが使用される問題を修正 [＃10595](https://github.com/pingcap/tidb/pull/10595)
-   組み込み`CONVERT()`不正なフィールドタイプを返す可能性がある問題を修正 [＃10263](https://github.com/pingcap/tidb/pull/10263)
-   バケット数を更新するときに重複していないフィードバックをマージする [＃10569](https://github.com/pingcap/tidb/pull/10569)
-   `unix_timestamp()-unix_timestamp(now())` の計算エラーを修正 [＃10491](https://github.com/pingcap/tidb/pull/10491)
-   MySQL 8.0 との`period_diff`互換性の問題を修正 [＃10501](https://github.com/pingcap/tidb/pull/10501)
-   例外を回避するために統計を収集するときに`Virtual Column`スキップする[＃10628](https://github.com/pingcap/tidb/pull/10628)
-   `SHOW OPEN TABLES`ステートメントサポートする [＃10374](https://github.com/pingcap/tidb/pull/10374)
-   場合によっては goroutine リークが発生する可能性がある問題を修正[＃10656](https://github.com/pingcap/tidb/pull/10656)
-   `tidb_snapshot`変数を設定すると、場合によっては時間形式の解析が正しく行われない可能性がある問題を修正しました。 [＃10637](https://github.com/pingcap/tidb/pull/10637)

## PD {#pd}

-   `balance-region` によりホットリージョンのスケジュールが失敗する可能性がある問題を修正しました [＃1551](https://github.com/pingcap/pd/pull/1551)
-   ホットスポット関連のスケジュール優先度を高く設定[＃1551](https://github.com/pingcap/pd/pull/1551)
-   2つの構成項目追加する [＃1551](https://github.com/pingcap/pd/pull/1551)
    -   `hot-region-schedule-limit`同時ホットスポット スケジューリング タスクの最大数を制御します
    -   ホットリージョンを識別するには`hot-region-cache-hits-threshold`

## TiKV {#tikv}

-   リーダーとラーナーが1つずつしかない場合にラーナーが空のインデックスを読み取る問題を修正しました。 [＃4751](https://github.com/tikv/tikv/pull/4751)
-   スレッドプール内のプロセス`ScanLock`と`ResolveLock`高優先度に設定し、通常優先度コマンドへの影響を軽減します。 [＃4791](https://github.com/tikv/tikv/pull/4791)
-   受信したスナップショットのすべてのファイルを同期する [＃4811](https://github.com/tikv/tikv/pull/4811)

## ツール {#tools}

-   TiDB Binlog
    -   GC中のデータ削除速度を制限して、 `WritePause` によるQPSの低下を回避する [＃620](https://github.com/pingcap/tidb-binlog/pull/620)

## TiDB Ansible {#tidb-ansible}

-   Drainerパラメータを追加 [＃760](https://github.com/pingcap/tidb-ansible/pull/760)
