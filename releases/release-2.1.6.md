---
title: TiDB 2.1.6 Release Notes
---

# TiDB 2.1.6 リリースノート {#tidb-2-1-6-release-notes}

2019 年 3 月 15 日に、TiDB 2.1.6 がリリースされました。対応する TiDB Ansible 2.1.6 もリリースされています。 TiDB 2.1.5 と比較して、このリリースでは安定性、SQL オプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   ヒント`TIDB_INLJ` [#9615](https://github.com/pingcap/tidb/pull/9615)で両方のテーブルが指定されている場合、コストに基づいて外部テーブルを選択するようにプランナーを最適化します。
    -   `IndexScan`正しく選択できない場合がある問題を修正[#9587](https://github.com/pingcap/tidb/pull/9587)
    -   サブクエリ[#9551](https://github.com/pingcap/tidb/pull/9551)の`agg`関数のチェックの MySQL との非互換性を修正
    -   パニックを避けるために`show stats_histograms`有効な列のみを出力するようにします[#9502](https://github.com/pingcap/tidb/pull/9502)

-   サーバ
    -   Binlog [#9634](https://github.com/pingcap/tidb/pull/9634)を有効/無効にする`log_bin`変数をサポートします
    -   トランザクションの健全性チェックを追加して、誤ったトランザクションのコミットを回避します[#9559](https://github.com/pingcap/tidb/pull/9559)
    -   変数を設定するとpanic[#9539](https://github.com/pingcap/tidb/pull/9539)が発生する場合がある問題を修正

-   DDL
    -   `Create Table Like`ステートメントが場合によってpanicを引き起こす問題を修正[#9652](https://github.com/pingcap/tidb/pull/9652)
    -   etcd クライアントの`AutoSync`機能を有効にして、場合によっては TiDB と etcd 間の接続の問題を回避します[#9600](https://github.com/pingcap/tidb/pull/9600)

## TiKV {#tikv}

-   `protobuf`解析失敗により場合によっては`StoreNotMatch`エラーが発生する問題を修正[#4303](https://github.com/tikv/tikv/pull/4303)

## ツール {#tools}

-   稲妻
    -   インポーターのデフォルトの`region-split-size` 512 MiB [#4369](https://github.com/tikv/tikv/pull/4369)に変更します。
    -   メモリ使用量を削減するために、以前にメモリにキャッシュされた中間 SST をローカル ディスクに保存します[#4369](https://github.com/tikv/tikv/pull/4369)
    -   RocksDB のメモリ使用量を制限する[#4369](https://github.com/tikv/tikv/pull/4369)
    -   スケジューリングが完了する前にリージョンが分散してしまう問題を修正[#4369](https://github.com/tikv/tikv/pull/4369)
    -   大きなテーブルのデータとインデックスを個別にインポートして、バッチでインポートする際の時間消費を効果的に削減します[#132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   [#111](https://github.com/pingcap/tidb-lightning/pull/111)をサポート
    -   スキーマ名に英数字以外の文字が含まれているためにインポートが失敗するエラーを修正[#9547](https://github.com/pingcap/tidb/pull/9547)
