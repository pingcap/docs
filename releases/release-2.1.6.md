---
title: TiDB 2.1.6 Release Notes
summary: TiDB 2.1.6およびTiDB Ansible 2.1.6は、2019年3月15日にリリースされました。このリリースでは、安定性、SQLオプティマイザー、統計、実行エンジンが改善されています。SQLオプティマイザー/エグゼキューター、サーバー、DDL、TiKV、ツールの修正と機能強化が行われました。主な変更点としては、log_bin変数のサポート、トランザクションのサニティチェック、スキーマ名に英数字以外の文字が含まれていることによるインポートエラーの修正などが挙げられます。
---

# TiDB 2.1.6 リリースノート {#tidb-2-1-6-release-notes}

2019年3月15日にTiDB 2.1.6がリリースされました。対応するTiDB Ansible 2.1.6もリリースされました。このリリースでは、TiDB 2.1.5と比較して、安定性、SQLオプティマイザー、統計、実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   `TIDB_INLJ` [＃9615](https://github.com/pingcap/tidb/pull/9615)のヒントで両方のテーブルが指定されている場合、コストに基づいて外側のテーブルを選択するようにプランナーを最適化します。
    -   `IndexScan`正しく選択されない場合がある問題を修正[＃9587](https://github.com/pingcap/tidb/pull/9587)
    -   サブクエリ[＃9551](https://github.com/pingcap/tidb/pull/9551)の`agg`関数のチェックにおけるMySQLとの非互換性を修正
    -   パニックを回避するために、 `show stats_histograms`有効な列のみを出力する[＃9502](https://github.com/pingcap/tidb/pull/9502)

-   サーバ
    -   Binlog [＃9634](https://github.com/pingcap/tidb/pull/9634)有効/無効にする`log_bin`変数をサポートします
    -   誤ったトランザクションコミットを回避するためにトランザクションの健全性チェックを追加する[＃9559](https://github.com/pingcap/tidb/pull/9559)
    -   変数を設定するとpanicが発生する可能性がある問題を修正[＃9539](https://github.com/pingcap/tidb/pull/9539)

-   DDL
    -   `Create Table Like`文が場合によってはpanicを引き起こす問題を修正[＃9652](https://github.com/pingcap/tidb/pull/9652)
    -   場合によってはTiDBとetcd間の接続の問題を回避するためにetcdクライアントの`AutoSync`機能を有効にする[＃9600](https://github.com/pingcap/tidb/pull/9600)

## TiKV {#tikv}

-   `protobuf`解析失敗により、場合によっては`StoreNotMatch`エラー[＃4303](https://github.com/tikv/tikv/pull/4303)が発生する問題を修正しました

## ツール {#tools}

-   稲妻
    -   インポーターのデフォルト`region-split-size` 512 MiB [＃4369](https://github.com/tikv/tikv/pull/4369)に変更
    -   メモリ使用量を削減するために、以前にメモリにキャッシュされた中間SSTをローカルディスクに保存します[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   RocksDB [＃4369](https://github.com/tikv/tikv/pull/4369)のメモリ使用量を制限する
    -   スケジュールが完了する前にリージョンが分散される問題を修正[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   大規模なテーブルのデータとインデックスを個別にインポートすることで、バッチインポート時の時間消費を効果的に削減します[＃132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   CSV [＃111](https://github.com/pingcap/tidb-lightning/pull/111)サポート
    -   スキーマ名に英数字以外の文字が含まれているためにインポートが失敗するエラーを修正[＃9547](https://github.com/pingcap/tidb/pull/9547)
