---
title: TiDB 2.1 RC4 Release Notes
---

# TiDB2.1RC4リリースノート {#tidb-2-1-rc4-release-notes}

2018年10月23日、TiDB2.1RC4がリリースされました。このリリースでは、TiDB 2.1 RC3と比較して、安定性、SQLオプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `UnionAll`の列プルーニングが誤っている場合があるという問題を修正します[＃7941](https://github.com/pingcap/tidb/pull/7941)
    -   `UnionAll`演算子の結果が正しくない場合があるという問題を修正します[＃8007](https://github.com/pingcap/tidb/pull/8007)
-   SQL実行エンジン
    -   `AVG`関数[＃7874](https://github.com/pingcap/tidb/pull/7874)の精度の問題を修正します
    -   `EXPLAIN ANALYZE`ステートメントを使用して、実行時間やクエリ実行プロセス中に返された各演算子の行数などの実行時統計を確認することをサポートします[＃7925](https://github.com/pingcap/tidb/pull/7925)
    -   テーブルの列が結果セット[＃7943](https://github.com/pingcap/tidb/pull/7943)に複数回表示される場合の、 `PointGet`演算子のパニックの問題を修正します。
    -   `Limit`節[＃8002](https://github.com/pingcap/tidb/pull/8002)の値が大きすぎるために発生するパニックの問題を修正します。
    -   場合によっては`AddDate`ステートメントの実行プロセス中のパニックの問題を修正し[＃8009](https://github.com/pingcap/tidb/pull/8009) `SubDate`
-   統計
    -   結合されたインデックスのヒストグラムの下限のプレフィックスが範囲[＃7856](https://github.com/pingcap/tidb/pull/7856)外であると判断する問題を修正します。
    -   統計収集によって引き起こされるメモリリークの問題を修正します[＃7873](https://github.com/pingcap/tidb/pull/7873)
    -   ヒストグラムが空の場合のパニックの問題を修正します[＃7928](https://github.com/pingcap/tidb/pull/7928)
    -   統計がアップロードされているときにヒストグラムの境界が範囲外になる問題を修正します[＃7944](https://github.com/pingcap/tidb/pull/7944)
    -   統計サンプリングプロセスの値の最大長を制限する[＃7982](https://github.com/pingcap/tidb/pull/7982)
-   サーバ
    -   ラッチをリファクタリングして、トランザクションの競合の誤判断を回避し、同時トランザクションの実行パフォーマンスを向上させます[＃7711](https://github.com/pingcap/tidb/pull/7711)
    -   場合によっては遅いクエリを収集することによって引き起こされるパニックの問題を修正します[＃7874](https://github.com/pingcap/tidb/pull/7847)
    -   `LOAD DATA`ステートメント[＃8005](https://github.com/pingcap/tidb/pull/8005)で`ESCAPED BY`が空の文字列である場合のパニックの問題を修正します。
    -   「コプロセッサー・エラー」ログ情報を完成させます[＃8006](https://github.com/pingcap/tidb/pull/8006)
-   互換性
    -   クエリが空の場合は、 `SHOW PROCESSLIST`の結果の`Command`のフィールドを`Sleep`に設定します[＃7839](https://github.com/pingcap/tidb/pull/7839)
-   式
    -   `SYSDATE`関数[＃7895](https://github.com/pingcap/tidb/pull/7895)の定数畳み込みの問題を修正します
    -   `SUBSTRING_INDEX`が場合によってはパニックになる問題を修正します[＃7897](https://github.com/pingcap/tidb/pull/7897)
-   DDL
    -   `invalid ddl job type`エラー[＃7958](https://github.com/pingcap/tidb/pull/7958)をスローすることによって引き起こされるスタックオーバーフローの問題を修正します
    -   `ADMIN CHECK TABLE`の結果が正しくない場合があるという問題を修正します[＃7975](https://github.com/pingcap/tidb/pull/7975)

## PD {#pd}

-   トゥームストーンTiKVが[＃1261](https://github.com/pingcap/pd/pull/1261)から削除されない問題を修正します
-   grpc-goがステータス[＃1265](https://github.com/pingcap/pd/pull/1265)を設定するときのデータ競合の問題を修正します
-   etcdの起動エラーが原因でPDサーバーがスタックする問題を修正します[＃1267](https://github.com/pingcap/pd/pull/1267)
-   リーダーの切り替え中にデータ競合が発生する可能性がある問題を修正します[＃1273](https://github.com/pingcap/pd/pull/1273)
-   TiKVがトゥームストーン[＃1280](https://github.com/pingcap/pd/pull/1273)になったときに追加の警告ログが出力される可能性がある問題を修正します

## TiKV {#tikv}

-   スナップショットの適用によって引き起こされるRocksDB書き込みストールの問題を最適化する[＃3606](https://github.com/tikv/tikv/pull/3606)
-   `tick`メトリックを追加[＃3657](https://github.com/tikv/tikv/pull/3657)
-   RocksDBをアップグレードし、書き込みブロックの問題を修正し、 `IngestExternalFile`の実行時に書き込み操作によってソースファイルが損傷する可能性があることを修正し[＃3661](https://github.com/tikv/tikv/pull/3661) 。
-   grpcioをアップグレードし、「pingが多すぎる」と誤って報告される問題を修正します[＃3650](https://github.com/tikv/tikv/pull/3650)
