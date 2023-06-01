---
title: TiDB 2.1 RC4 Release Notes
---

# TiDB 2.1 RC4 リリースノート {#tidb-2-1-rc4-release-notes}

2018 年 10 月 23 日に、TiDB 2.1 RC4 がリリースされました。 TiDB 2.1 RC3 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   場合によっては`UnionAll`の列プルーニングが正しくない問題を修正[<a href="https://github.com/pingcap/tidb/pull/7941">#7941</a>](https://github.com/pingcap/tidb/pull/7941)
    -   `UnionAll`演算子の結果が正しくない場合がある問題を修正[<a href="https://github.com/pingcap/tidb/pull/8007">#8007</a>](https://github.com/pingcap/tidb/pull/8007)
-   SQL実行エンジン
    -   `AVG`関数[<a href="https://github.com/pingcap/tidb/pull/7874">#7874</a>](https://github.com/pingcap/tidb/pull/7874)の精度の問題を修正
    -   `EXPLAIN ANALYZE`ステートメントを使用して、クエリ実行プロセス中に各演算子の実行時間や返される行数などの実行時統計を確認するサポート[<a href="https://github.com/pingcap/tidb/pull/7925">#7925</a>](https://github.com/pingcap/tidb/pull/7925)
    -   テーブルの列が結果セット[<a href="https://github.com/pingcap/tidb/pull/7943">#7943</a>](https://github.com/pingcap/tidb/pull/7943)に複数回出現する場合の`PointGet`演算子のpanicの問題を修正します。
    -   `Limit`サブ句[<a href="https://github.com/pingcap/tidb/pull/8002">#8002</a>](https://github.com/pingcap/tidb/pull/8002)の値が大きすぎることによって引き起こされるpanicの問題を修正
    -   場合によっては`AddDate` / `SubDate`ステートメントの実行プロセス中にpanicが発生する問題を修正しました[<a href="https://github.com/pingcap/tidb/pull/8009">#8009</a>](https://github.com/pingcap/tidb/pull/8009)
-   統計
    -   結合インデックスのヒストグラム下限のプレフィックスが範囲外と判定される問題を修正しました[<a href="https://github.com/pingcap/tidb/pull/7856">#7856</a>](https://github.com/pingcap/tidb/pull/7856)
    -   統計収集によって発生するメモリリークの問題を修正[<a href="https://github.com/pingcap/tidb/pull/7873">#7873</a>](https://github.com/pingcap/tidb/pull/7873)
    -   ヒストグラムが空の場合のpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/7928">#7928</a>](https://github.com/pingcap/tidb/pull/7928)
    -   統計のアップロード時にヒストグラムの境界が範囲外になる問題を修正[<a href="https://github.com/pingcap/tidb/pull/7944">#7944</a>](https://github.com/pingcap/tidb/pull/7944)
    -   統計サンプリング プロセスの値の最大長を制限する[<a href="https://github.com/pingcap/tidb/pull/7982">#7982</a>](https://github.com/pingcap/tidb/pull/7982)
-   サーバ
    -   トランザクション競合の誤判断を回避し、同時トランザクションの実行パフォーマンスを向上させるためのラッチのリファクタリング[<a href="https://github.com/pingcap/tidb/pull/7711">#7711</a>](https://github.com/pingcap/tidb/pull/7711)
    -   場合によっては遅いクエリの収集によって引き起こされるpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/7847">#7874</a>](https://github.com/pingcap/tidb/pull/7847)
    -   `LOAD DATA`ステートメントの`ESCAPED BY`が空の文字列である場合のpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8005">#8005</a>](https://github.com/pingcap/tidb/pull/8005)
    -   「コプロセッサエラー」ログ情報を完了します[<a href="https://github.com/pingcap/tidb/pull/8006">#8006</a>](https://github.com/pingcap/tidb/pull/8006)
-   互換性
    -   クエリが空の場合、 `SHOW PROCESSLIST`結果の`Command`フィールドを`Sleep`に設定します[<a href="https://github.com/pingcap/tidb/pull/7839">#7839</a>](https://github.com/pingcap/tidb/pull/7839)
-   式
    -   `SYSDATE`関数[<a href="https://github.com/pingcap/tidb/pull/7895">#7895</a>](https://github.com/pingcap/tidb/pull/7895)の定数フォールディングの問題を修正
    -   `SUBSTRING_INDEX`場合によってはパニックになる問題を修正[<a href="https://github.com/pingcap/tidb/pull/7897">#7897</a>](https://github.com/pingcap/tidb/pull/7897)
-   DDL
    -   `invalid ddl job type`エラー[<a href="https://github.com/pingcap/tidb/pull/7958">#7958</a>](https://github.com/pingcap/tidb/pull/7958)のスローによって引き起こされるスタック オーバーフローの問題を修正します。
    -   `ADMIN CHECK TABLE`の結果が正しくない場合がある問題を修正[<a href="https://github.com/pingcap/tidb/pull/7975">#7975</a>](https://github.com/pingcap/tidb/pull/7975)

## PD {#pd}

-   Grafana [<a href="https://github.com/pingcap/pd/pull/1261">#1261</a>](https://github.com/pingcap/pd/pull/1261)から墓石 TiKV が削除されない問題を修正
-   grpc-go がステータス[<a href="https://github.com/pingcap/pd/pull/1265">#1265</a>](https://github.com/pingcap/pd/pull/1265)を設定するときのデータ競合の問題を修正
-   etcd の起動失敗により PDサーバーが停止する問題を修正[<a href="https://github.com/pingcap/pd/pull/1267">#1267</a>](https://github.com/pingcap/pd/pull/1267)
-   リーダー切り替え時にデータ競合が発生する場合がある問題を修正[<a href="https://github.com/pingcap/pd/pull/1273">#1273</a>](https://github.com/pingcap/pd/pull/1273)
-   TiKVがtombstone [<a href="https://github.com/pingcap/pd/pull/1273">#1280</a>](https://github.com/pingcap/pd/pull/1273)になったときに余分な警告ログが出力される場合がある問題を修正

## TiKV {#tikv}

-   スナップショットの適用によって発生する RocksDB の書き込み停止問題を最適化する[<a href="https://github.com/tikv/tikv/pull/3606">#3606</a>](https://github.com/tikv/tikv/pull/3606)
-   raftstore `tick`メトリクス[<a href="https://github.com/tikv/tikv/pull/3657">#3657</a>](https://github.com/tikv/tikv/pull/3657)を追加
-   RocksDB をアップグレードし、書き込みブロックの問題と、 `IngestExternalFile` [<a href="https://github.com/tikv/tikv/pull/3661">#3661</a>](https://github.com/tikv/tikv/pull/3661)の実行時に書き込み操作によってソース ファイルが破損する可能性がある問題を修正します。
-   grpcio をアップグレードし、「ping が多すぎる」と誤って報告される問題を修正します[<a href="https://github.com/tikv/tikv/pull/3650">#3650</a>](https://github.com/tikv/tikv/pull/3650)
