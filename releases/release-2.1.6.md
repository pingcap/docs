---
title: TiDB 2.1.6 Release Notes
---

# TiDB 2.1.6 リリースノート {#tidb-2-1-6-release-notes}

2019 年 3 月 15 日に、TiDB 2.1.6 がリリースされました。対応する TiDB Ansible 2.1.6 もリリースされています。 TiDB 2.1.5 と比較して、このリリースでは安定性、SQL オプティマイザ、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   Hint of `TIDB_INLJ` [#9615](https://github.com/pingcap/tidb/pull/9615)で両方のテーブルが指定されている場合、コストに基づいて外側のテーブルを選択するように Planner を最適化します。
    -   `IndexScan`正しく選択できない場合がある問題を修正[#9587](https://github.com/pingcap/tidb/pull/9587)
    -   サブクエリ[#9551](https://github.com/pingcap/tidb/pull/9551)のチェックイン`agg`関数の MySQL との非互換性を修正
    -   パニックを避けるために、有効な列`show stats_histograms`を出力するようにします[#9502](https://github.com/pingcap/tidb/pull/9502)

-   サーバ
    -   Binlog [#9634](https://github.com/pingcap/tidb/pull/9634)を有効/無効にする`log_bin`変数をサポート
    -   トランザクションのサニティ チェックを追加して、誤ったトランザクション コミットを回避する[#9559](https://github.com/pingcap/tidb/pull/9559)
    -   変数を設定するとpanic[#9539](https://github.com/pingcap/tidb/pull/9539)が発生する可能性がある問題を修正します

-   DDL
    -   `Create Table Like`ステートメントが場合によってはpanicを引き起こす問題を修正します[#9652](https://github.com/pingcap/tidb/pull/9652)
    -   場合によっては TiDB と etcd 間の接続の問題を回避するために、etcd クライアントの`AutoSync`機能を有効にします[#9600](https://github.com/pingcap/tidb/pull/9600)

## TiKV {#tikv}

-   `protobuf`解析エラーが場合によっては`StoreNotMatch`エラー[#4303](https://github.com/tikv/tikv/pull/4303)を引き起こす問題を修正します。

## ツール {#tools}

-   雷
    -   インポーターのデフォルト`region-split-size` 512 MiB [#4369](https://github.com/tikv/tikv/pull/4369)に変更
    -   以前にメモリにキャッシュされた中間 SST をローカル ディスクに保存して、メモリ使用量を削減します[#4369](https://github.com/tikv/tikv/pull/4369)
    -   RocksDB [#4369](https://github.com/tikv/tikv/pull/4369)のメモリ使用量を制限する
    -   スケジューリングが完了する前にリージョンが分散する問題を修正します[#4369](https://github.com/tikv/tikv/pull/4369)
    -   大きなテーブルのデータとインデックスを個別にインポートして、バッチでインポートする際の時間消費を効果的に削減する[#132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   CSV [#111](https://github.com/pingcap/tidb-lightning/pull/111)をサポート
    -   スキーマ名に英数字以外の文字が含まれているためにインポートが失敗するエラーを修正します[#9547](https://github.com/pingcap/tidb/pull/9547)
