---
title: TiDB 2.1.6 Release Notes
---

# TiDB2.1.6リリースノート {#tidb-2-1-6-release-notes}

2019年3月15日、TiDB2.1.6がリリースされました。対応するTiDBAnsible2.1.6もリリースされています。このリリースでは、TiDB 2.1.5と比較して、安定性、SQLオプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー/エグゼキューター
    -   両方のテーブルが[＃9615](https://github.com/pingcap/tidb/pull/9615)のヒントで指定されている場合、コストに基づいて外部テーブルを選択するようにプランナーを最適化し`TIDB_INLJ`
    -   `IndexScan`が正しく選択できない場合があるという問題を修正します[＃9587](https://github.com/pingcap/tidb/pull/9587)
    -   サブクエリ[＃9551](https://github.com/pingcap/tidb/pull/9551)の`agg`関数のチェックのMySQLとの非互換性を修正しました
    -   パニックを回避するために、 `show stats_histograms`は有効な列のみを出力するようにします[＃9502](https://github.com/pingcap/tidb/pull/9502)

-   サーバ
    -   Binlogを有効/無効にする`log_bin`の変数をサポートし[＃9634](https://github.com/pingcap/tidb/pull/9634)
    -   誤ったトランザクションコミットを回避するために、トランザクションの健全性チェックを追加します[＃9559](https://github.com/pingcap/tidb/pull/9559)
    -   変数の設定がpanicにつながる可能性がある問題を修正します[＃9539](https://github.com/pingcap/tidb/pull/9539)

-   DDL
    -   `Create Table Like`ステートメントが場合によってはpanicを引き起こす問題を修正します[＃9652](https://github.com/pingcap/tidb/pull/9652)
    -   etcdクライアントの`AutoSync`機能を有効にして、場合によってはTiDBとetcd間の接続の問題を回避します[＃9600](https://github.com/pingcap/tidb/pull/9600)

## TiKV {#tikv}

-   `protobuf`の解析の失敗が場合によっては`StoreNotMatch`のエラーを引き起こすという問題を修正します[＃4303](https://github.com/tikv/tikv/pull/4303)

## ツール {#tools}

-   雷
    -   インポーターのデフォルト`region-split-size`を512MiB3に変更し[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   以前にメモリにキャッシュされた中間SSTをローカルディスクに保存して、メモリ使用量を削減します[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   [＃4369](https://github.com/tikv/tikv/pull/4369)のメモリ使用量を制限する
    -   スケジューリングが完了する前にリージョンが分散する問題を修正します[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   大きなテーブルのデータとインデックスを個別にインポートして、バッチでインポートする際の時間の消費を効果的に削減します[＃132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   [＃111](https://github.com/pingcap/tidb-lightning/pull/111)をサポート
    -   スキーマ名に英数字以外の文字が含まれているためにインポートが失敗するエラーを修正しました[＃9547](https://github.com/pingcap/tidb/pull/9547)
