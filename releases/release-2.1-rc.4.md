---
title: TiDB 2.1 RC4 Release Notes
summary: TiDB 2.1 RC4 は、安定性、SQL オプティマイザー、統計情報、実行エンジンの改善を伴い、2018 年 10 月 23 日にリリースされました。修正には、SQL オプティマイザー、実行エンジン、統計、サーバー、互換性、式、DDL に関する問題が含まれます。PD では、tombstone TiKV、データ競合、PDサーバーの停止、リーダー切り替えに関する問題が修正されています。TiKV では、RocksDB 書き込み停止の問題が最適化され、raftstore ティック メトリックが追加され、RocksDB と grpcio がアップグレードされています。
---

# TiDB 2.1 RC4 リリースノート {#tidb-2-1-rc4-release-notes}

2018 年 10 月 23 日に、TiDB 2.1 RC4 がリリースされました。TiDB 2.1 RC3 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、実行エンジンが大幅に改善されています。

## ティビ {#tidb}

-   SQL オプティマイザー
    -   `UnionAll`の列のプルーニングが場合によっては正しくない問題を修正[＃7941](https://github.com/pingcap/tidb/pull/7941)
    -   `UnionAll`演算子の結果が場合によっては正しくない問題を修正[＃8007](https://github.com/pingcap/tidb/pull/8007)
-   SQL実行エンジン
    -   `AVG`関数[＃7874](https://github.com/pingcap/tidb/pull/7874)の精度の問題を修正
    -   `EXPLAIN ANALYZE`ステートメントを使用して、クエリ実行プロセス中の各演算子の実行時間と返された行数などの実行時統計を確認することをサポートします[＃7925](https://github.com/pingcap/tidb/pull/7925)
    -   テーブルの列が結果セット[＃7943](https://github.com/pingcap/tidb/pull/7943)に複数回出現する場合の`PointGet`演算子のpanic問題を修正
    -   `Limit`節[＃8002](https://github.com/pingcap/tidb/pull/8002)の値が大きすぎるために発生するpanic問題を修正
    -   一部のケースで`AddDate`ステートメントの実行プロセス中にpanicが発生`SubDate`問題を修正しました[＃8009](https://github.com/pingcap/tidb/pull/8009)
-   統計
    -   結合インデックスのヒストグラム下限のプレフィックスが範囲外であると判断される問題を修正[＃7856](https://github.com/pingcap/tidb/pull/7856)
    -   統計収集によるメモリリークの問題を修正[＃7873](https://github.com/pingcap/tidb/pull/7873)
    -   ヒストグラムが空の場合のpanic問題を修正[＃7928](https://github.com/pingcap/tidb/pull/7928)
    -   統計情報のアップロード時にヒストグラムの境界が範囲外になる問題を修正[＃7944](https://github.com/pingcap/tidb/pull/7944)
    -   統計サンプリングプロセスにおける値の最大長を制限する[＃7982](https://github.com/pingcap/tidb/pull/7982)
-   サーバ
    -   ラッチをリファクタリングしてトランザクションの競合の誤判断を回避し、同時トランザクションの実行パフォーマンスを向上させる[＃7711](https://github.com/pingcap/tidb/pull/7711)
    -   一部のケースで遅いクエリを収集することで発生するpanic問題を修正[＃7874](https://github.com/pingcap/tidb/pull/7847)
    -   `LOAD DATA`文[＃8005](https://github.com/pingcap/tidb/pull/8005)で`ESCAPED BY`空文字列の場合にpanic問題を修正
    -   「コプロセッサエラー」ログ情報[＃8006](https://github.com/pingcap/tidb/pull/8006)完了する
-   互換性
    -   クエリが空の場合、 `SHOW PROCESSLIST`結果の`Command`フィールドを`Sleep`に設定します[＃7839](https://github.com/pingcap/tidb/pull/7839)
-   表現
    -   `SYSDATE`関数[＃7895](https://github.com/pingcap/tidb/pull/7895)の定数畳み込みの問題を修正
    -   `SUBSTRING_INDEX`場合によってはパニックになる問題を修正[＃7897](https://github.com/pingcap/tidb/pull/7897)
-   DDL
    -   `invalid ddl job type`エラー[＃7958](https://github.com/pingcap/tidb/pull/7958)をスローすることで発生するスタックオーバーフローの問題を修正
    -   `ADMIN CHECK TABLE`の結果が場合によっては正しくない問題を修正[＃7975](https://github.com/pingcap/tidb/pull/7975)

## PD {#pd}

-   Grafana [＃1261](https://github.com/pingcap/pd/pull/1261)から墓石 TiKV が削除されない問題を修正
-   grpc-goがステータス[＃1265](https://github.com/pingcap/pd/pull/1265)を設定する際のデータ競合問題を修正
-   etcd の起動失敗により PDサーバーが停止する問題を修正[＃1267](https://github.com/pingcap/pd/pull/1267)
-   リーダー切り替え時にデータ競合が発生する可能性がある問題を修正[＃1273](https://github.com/pingcap/pd/pull/1273)
-   TiKVがトゥームストーン[＃1280](https://github.com/pingcap/pd/pull/1273)になったときに追加の警告ログが出力される可能性がある問題を修正

## ティクヴ {#tikv}

-   スナップショット[＃3606](https://github.com/tikv/tikv/pull/3606)の適用によって発生する RocksDB 書き込み停止の問題を最適化します。
-   raftstore `tick`メトリック[＃3657](https://github.com/tikv/tikv/pull/3657)を追加
-   RocksDBをアップグレードし、書き込みブロックの問題を修正し、 `IngestExternalFile` [＃3661](https://github.com/tikv/tikv/pull/3661)を実行するときに書き込み操作によってソースファイルが破損する可能性がある問題を修正しました。
-   grpcio をアップグレードし、「ping が多すぎる」と誤って報告される問題を修正[＃3650](https://github.com/tikv/tikv/pull/3650)
