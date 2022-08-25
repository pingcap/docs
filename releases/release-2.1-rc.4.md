---
title: TiDB 2.1 RC4 Release Notes
---

# TiDB 2.1 RC4 リリースノート {#tidb-2-1-rc4-release-notes}

2018 年 10 月 23 日に、TiDB 2.1 RC4 がリリースされました。 TiDB 2.1 RC3 と比較して、このリリースでは、安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー
    -   `UnionAll`の列の刈り込みが正しくない場合がある問題を修正[#7941](https://github.com/pingcap/tidb/pull/7941)
    -   `UnionAll`演算子の結果が正しくない場合がある問題を修正[#8007](https://github.com/pingcap/tidb/pull/8007)
-   SQL 実行エンジン
    -   `AVG`関数[#7874](https://github.com/pingcap/tidb/pull/7874)の精度の問題を修正
    -   `EXPLAIN ANALYZE`ステートメントを使用して、クエリ実行プロセス中に実行時間と各演算子の返された行数を含むランタイム統計をチェックするサポート[#7925](https://github.com/pingcap/tidb/pull/7925)
    -   テーブルの列が結果セットに複数回表示される場合の`PointGet`演算子のpanicの問題を修正します[#7943](https://github.com/pingcap/tidb/pull/7943)
    -   `Limit`節[#8002](https://github.com/pingcap/tidb/pull/8002)の値が大きすぎるために発生するpanicの問題を修正します。
    -   場合によっては`AddDate` / `SubDate`ステートメントの実行プロセス中のpanicの問題を修正します[#8009](https://github.com/pingcap/tidb/pull/8009)
-   統計
    -   総合指数のヒストグラム下限の接頭辞が範囲[#7856](https://github.com/pingcap/tidb/pull/7856)外と判定される問題を修正
    -   統計収集[#7873](https://github.com/pingcap/tidb/pull/7873)によって引き起こされるメモリ リークの問題を修正します。
    -   ヒストグラムが空の場合のpanicの問題を修正します[#7928](https://github.com/pingcap/tidb/pull/7928)
    -   統計のアップロード時にヒストグラム バウンドが範囲外になる問題を修正します[#7944](https://github.com/pingcap/tidb/pull/7944)
    -   統計サンプリング プロセスで値の最大長を制限する[#7982](https://github.com/pingcap/tidb/pull/7982)
-   サーバ
    -   ラッチをリファクタリングして、トランザクション競合の誤判断を回避し、同時トランザクションの実行パフォーマンスを向上させます[#7711](https://github.com/pingcap/tidb/pull/7711)
    -   場合によっては遅いクエリを収集することによって引き起こされるpanicの問題を修正します[#7874](https://github.com/pingcap/tidb/pull/7847)
    -   `LOAD DATA`ステートメント[#8005](https://github.com/pingcap/tidb/pull/8005)で`ESCAPED BY`が空の文字列の場合のpanicの問題を修正します。
    -   「コプロセッサー・エラー」ログ情報を完成させる[#8006](https://github.com/pingcap/tidb/pull/8006)
-   互換性
    -   クエリが空の場合、 `SHOW PROCESSLIST`結果の`Command`フィールドを`Sleep`に設定します[#7839](https://github.com/pingcap/tidb/pull/7839)
-   式
    -   `SYSDATE`関数[#7895](https://github.com/pingcap/tidb/pull/7895)の一定の折り畳みの問題を修正します。
    -   `SUBSTRING_INDEX`場合によってはパニックになる問題を修正[#7897](https://github.com/pingcap/tidb/pull/7897)
-   DDL
    -   `invalid ddl job type`エラー[#7958](https://github.com/pingcap/tidb/pull/7958)をスローすることによって引き起こされるスタック オーバーフローの問題を修正します。
    -   `ADMIN CHECK TABLE`の結果が正しくない場合がある問題を修正[#7975](https://github.com/pingcap/tidb/pull/7975)

## PD {#pd}

-   Tombstone TiKV が Grafana [#1261](https://github.com/pingcap/pd/pull/1261)から削除されない問題を修正
-   grpc-go がステータス[#1265](https://github.com/pingcap/pd/pull/1265)を構成するときのデータ競合の問題を修正します
-   etcdの起動失敗によりPDサーバーが動かなくなる問題を修正[#1267](https://github.com/pingcap/pd/pull/1267)
-   リーダーの切り替え時にデータ競合が発生する可能性がある問題を修正[#1273](https://github.com/pingcap/pd/pull/1273)
-   TiKV が tombstone [#1280](https://github.com/pingcap/pd/pull/1273)になると余分な警告ログが出力されることがある問題を修正

## TiKV {#tikv}

-   スナップショットの適用によって発生する RocksDB の書き込み停止の問題を最適化する[#3606](https://github.com/tikv/tikv/pull/3606)
-   raftstore の追加`tick`メトリクス[#3657](https://github.com/tikv/tikv/pull/3657)
-   RocksDB をアップグレードし、書き込みブロックの問題を修正し、実行時に書き込み操作によってソース ファイルが破損する可能性があることを確認します`IngestExternalFile` [#3661](https://github.com/tikv/tikv/pull/3661)
-   grpcio をアップグレードし、「too many pings」が誤って報告される問題を修正します[#3650](https://github.com/tikv/tikv/pull/3650)
