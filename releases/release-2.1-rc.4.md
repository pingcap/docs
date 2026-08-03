---
title: TiDB 2.1 RC4 Release Notes
summary: TiDB 2.1 RC4は2018年10月23日にリリースされ、安定性、SQLオプティマイザ、統計情報、実行エンジンが改善されました。SQLオプティマイザ、実行エンジン、統計、サーバー、互換性、式、DDLに関する問題が修正されました。PDでは、tombstone TiKV、データ競合、PDサーバーのスタック、リーダー切り替えに関する問題が修正されました。TiKVでは、RocksDBの書き込みストール問題が最適化され、raftstoreのティックメトリクスが追加され、RocksDBとgrpcioがアップグレードされました。
---

# TiDB 2.1 RC4 リリースノート {#tidb-2-1-rc4-release-notes}

2018年10月23日にTiDB 2.1 RC4がリリースされました。TiDB 2.1 RC3と比較して、このリリースでは安定性、SQLオプティマイザー、統計情報、実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `UnionAll`の列プルーニングが場合によっては正しくない問題を修正[＃7941](https://github.com/pingcap/tidb/pull/7941)
    -   `UnionAll`演算子の結果が場合によっては正しくない問題を修正[＃8007](https://github.com/pingcap/tidb/pull/8007)
-   SQL実行エンジン
    -   `AVG`関数の精度の問題を修正 [＃7874](https://github.com/pingcap/tidb/pull/7874)
    -   `EXPLAIN ANALYZE`ステートメントを使用して、クエリ実行プロセス中の各演算子の実行時間と返された行数を含む実行時統計をチェックする機能をサポートします[＃7925](https://github.com/pingcap/tidb/pull/7925)
    -   テーブルの列が結果セットに複数回出現する場合の`PointGet`演算子のpanic問題を修正しました [＃7943](https://github.com/pingcap/tidb/pull/7943)
    -   `Limit`節値が大きすぎるために発生するpanic問題を修正しました [＃8002](https://github.com/pingcap/tidb/pull/8002)
    -   いくつかのケースで`AddDate`文`SubDate`実行中にpanic問題を修正しました[＃8009](https://github.com/pingcap/tidb/pull/8009)
-   統計
    -   結合インデックスのヒストグラム下限の接頭辞が範囲外であると判断される問題を修正[＃7856](https://github.com/pingcap/tidb/pull/7856)
    -   統計収集によるメモリリークの問題を修正[＃7873](https://github.com/pingcap/tidb/pull/7873)
    -   ヒストグラムが空の場合のpanic問題を修正[＃7928](https://github.com/pingcap/tidb/pull/7928)
    -   統計情報のアップロード時にヒストグラムの境界が範囲外になる問題を修正[＃7944](https://github.com/pingcap/tidb/pull/7944)
    -   統計サンプリングプロセスにおける値の最大長を制限する [＃7982](https://github.com/pingcap/tidb/pull/7982)
-   サーバ
    -   ラッチをリファクタリングしてトランザクションの競合の誤判断を回避し、同時トランザクションの実行パフォーマンスを向上させる[＃7711](https://github.com/pingcap/tidb/pull/7711)
    -   一部のケースでスロークエリを収集することによって発生するpanic問題を修正[＃7874](https://github.com/pingcap/tidb/pull/7847)
    -   `LOAD DATA`文で`ESCAPED BY`が空文字列の場合のpanic問題を修正 [＃8005](https://github.com/pingcap/tidb/pull/8005)
    -   「コプロセッサエラー」ログ情報を完了する [＃8006](https://github.com/pingcap/tidb/pull/8006)
-   互換性
    -   クエリが空の場合、 `SHOW PROCESSLIST`結果の`Command`フィールドを`Sleep`に設定します[＃7839](https://github.com/pingcap/tidb/pull/7839)
-   表現
    -   `SYSDATE`関数の定数の折り畳みの問題を修正 [＃7895](https://github.com/pingcap/tidb/pull/7895)
    -   `SUBSTRING_INDEX`が場合によってはパニックになる問題を修正[＃7897](https://github.com/pingcap/tidb/pull/7897)
-   DDL
    -   `invalid ddl job type`エラースローすることによって発生するスタックオーバーフローの問題を修正しました [＃7958](https://github.com/pingcap/tidb/pull/7958)
    -   `ADMIN CHECK TABLE`の結果が場合によっては正しくない問題を修正[＃7975](https://github.com/pingcap/tidb/pull/7975)

## PD {#pd}

-   Grafana からtombstone TiKV が削除されない問題を修正 [＃1261](https://github.com/pingcap/pd/pull/1261)
-   grpc-goがステータスを設定する際のデータ競合問題を修正 [＃1265](https://github.com/pingcap/pd/pull/1265)
-   etcdの起動失敗によりPDサーバーが停止する問題を修正[＃1267](https://github.com/pingcap/pd/pull/1267)
-   リーダー切り替え時にデータ競合が発生する可能性がある問題を修正[＃1273](https://github.com/pingcap/pd/pull/1273)
-   TiKVがtombstone になったときに追加の警告ログが出力される可能性がある問題を修正しました [＃1280](https://github.com/pingcap/pd/pull/1273)

## TiKV {#tikv}

-   スナップショット適用によって発生するRocksDB書き込み停止問題を最適化 [＃3606](https://github.com/tikv/tikv/pull/3606)
-   raftstore `tick`メトリックを追加 [＃3657](https://github.com/tikv/tikv/pull/3657)
-   RocksDBをアップグレードし、書き込みブロックの問題を修正し、 `IngestExternalFile` を実行するときに書き込み操作によってソースファイルが破損する可能性がある問題を修正しました。 [＃3661](https://github.com/tikv/tikv/pull/3661)
-   grpcio をアップグレードし、「ping が多すぎる」と誤って報告される問題を修正しました[＃3650](https://github.com/tikv/tikv/pull/3650)
