---
title: TiDB 2.1.6 Release Notes
summary: TiDB 2.1.6 および TiDB Ansible 2.1.6 は、2019 年 3 月 15 日にリリースされました。このリリースには、安定性、SQL オプティマイザー、統計、および実行エンジンの改善が含まれています。SQL オプティマイザー/エグゼキューター、サーバー、DDL、TiKV、およびツールで修正と機能強化が行われました。注目すべき変更には、log_bin 変数のサポート、トランザクションの健全性チェック、およびスキーマ名に英数字以外の文字が含まれていることによるインポートの失敗の修正が含まれます。
---

# TiDB 2.1.6 リリースノート {#tidb-2-1-6-release-notes}

2019 年 3 月 15 日に、TiDB 2.1.6 がリリースされました。対応する TiDB Ansible 2.1.6 もリリースされました。TiDB 2.1.5 と比較して、このリリースでは安定性、SQL オプティマイザー、統計、実行エンジンが大幅に改善されています。

## ティビ {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   ヒント`TIDB_INLJ` [＃9615](https://github.com/pingcap/tidb/pull/9615)で両方のテーブルが指定されている場合、コストに基づいて外部テーブルを選択するようにプランナーを最適化します。
    -   `IndexScan`正しく選択されない場合がある問題を修正[＃9587](https://github.com/pingcap/tidb/pull/9587)
    -   サブクエリ[＃9551](https://github.com/pingcap/tidb/pull/9551)の`agg`関数のチェックに関する MySQL との非互換性を修正
    -   パニックを回避するために、 `show stats_histograms`有効な列のみを出力する[＃9502](https://github.com/pingcap/tidb/pull/9502)

-   サーバ
    -   Binlog [＃9634](https://github.com/pingcap/tidb/pull/9634)を有効/無効にする`log_bin`変数をサポートします
    -   誤ったトランザクションコミットを回避するためにトランザクションの健全性チェックを追加する[＃9559](https://github.com/pingcap/tidb/pull/9559)
    -   変数を設定するとpanicが発生する可能性がある問題を修正[＃9539](https://github.com/pingcap/tidb/pull/9539)

-   DDL
    -   `Create Table Like`文が場合によってはpanicを引き起こす問題を修正[＃9652](https://github.com/pingcap/tidb/pull/9652)
    -   場合によっては TiDB と etcd 間の接続の問題を回避するために、etcd クライアントの`AutoSync`機能を有効にします[＃9600](https://github.com/pingcap/tidb/pull/9600)

## ティクヴ {#tikv}

-   `protobuf`解析失敗により、場合によっては`StoreNotMatch`エラー[＃4303](https://github.com/tikv/tikv/pull/4303)発生する問題を修正

## ツール {#tools}

-   稲妻
    -   インポーターのデフォルト`region-split-size` 512 MiB [＃4369](https://github.com/tikv/tikv/pull/4369)に変更
    -   メモリ使用量を削減するために、以前にメモリにキャッシュされた中間SSTをローカルディスクに保存します[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   RocksDB [＃4369](https://github.com/tikv/tikv/pull/4369)のメモリ使用量を制限する
    -   スケジュールが完了する前にリージョンが分散される問題を修正[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   大規模なテーブルのデータとインデックスを個別にインポートすることで、バッチインポート時の時間消費を効果的に削減します[＃132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   CSV [＃111](https://github.com/pingcap/tidb-lightning/pull/111)サポート
    -   スキーマ名に英数字以外の文字が含まれているためにインポートが失敗するエラーを修正[＃9547](https://github.com/pingcap/tidb/pull/9547)
