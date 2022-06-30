---
title: TiDB 2.0.9 Release Notes
---

# TiDB2.0.9リリースノート {#tidb-2-0-9-release-notes}

2018年11月19日、TiDB2.0.9がリリースされました。 TiDB 2.0.8と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   空の統計ヒストグラム[＃7927](https://github.com/pingcap/tidb/pull/7927)によって引き起こされる問題を修正します
-   場合によっては`UNION ALL`ステートメントのパニック問題を修正します[＃7942](https://github.com/pingcap/tidb/pull/7942)
-   間違ったDDLジョブによって引き起こされるスタックオーバーフローの問題を修正する[＃7959](https://github.com/pingcap/tidb/pull/7959)
-   `Commit`の操作の低速ログを追加します[＃7983](https://github.com/pingcap/tidb/pull/7983)
-   `Limit`の値が大きすぎることによって引き起こされるパニックの問題を修正します[＃8004](https://github.com/pingcap/tidb/pull/8004)
-   `USING`節[＃8048](https://github.com/pingcap/tidb/pull/8048)での`utf8mb4`文字セットの指定のサポート
-   `TRUNCATE`の組み込み関数が符号なし整数型[＃8069](https://github.com/pingcap/tidb/pull/8069)のパラメーターをサポートするようにします。
-   場合によっては、統計モジュールの主キーの選択性推定の問題を修正します[＃8150](https://github.com/pingcap/tidb/pull/8150)
-   `Session`変数を追加して、 `_tidb_rowid`を[＃8126](https://github.com/pingcap/tidb/pull/8126)に書き込むことができるかどうかを制御します
-   場合によっては`PhysicalProjection`のパニックの問題を修正します[＃8154](https://github.com/pingcap/tidb/pull/8154)
-   場合によっては`Union`ステートメントの不安定な結果を修正します[＃8168](https://github.com/pingcap/tidb/pull/8168)
-   `Insert`以外のステートメントで`NULL`が`values`によって返されない問題を修正します[＃8179](https://github.com/pingcap/tidb/pull/8179)
-   統計モジュールが古いデータをクリアできない場合があるという問題を修正します[＃8184](https://github.com/pingcap/tidb/pull/8184)
-   トランザクションの最大許容実行時間を構成可能なオプションにする[＃8209](https://github.com/pingcap/tidb/pull/8209)
-   場合によっては`expression rewriter`の間違った比較アルゴリズムを修正します[＃8288](https://github.com/pingcap/tidb/pull/8288)
-   `UNION ORDER BY`ステートメント[＃8307](https://github.com/pingcap/tidb/pull/8307)によって生成された余分な列を削除します
-   `admin show next_row_id`ステートメント[＃8274](https://github.com/pingcap/tidb/pull/8274)をサポートする
-   `Show Create Table`ステートメント[＃8321](https://github.com/pingcap/tidb/pull/8321)の特殊文字のエスケープの問題を修正します。
-   場合によっては`UNION`ステートメントの予期しないエラーを修正します[＃8318](https://github.com/pingcap/tidb/pull/8318)
-   DDLジョブをキャンセルすると、場合によってはスキーマのロールバックが発生しないという問題を修正します[＃8312](https://github.com/pingcap/tidb/pull/8312)
-   `tidb_max_chunk_size`をグローバル変数[＃8333](https://github.com/pingcap/tidb/pull/8333)に変更します
-   オーバーバウンドスキャンを回避するために、ticlientの`Scan`コマンドに上限を追加します[＃8309](https://github.com/pingcap/tidb/pull/8309) [＃8310](https://github.com/pingcap/tidb/pull/8310)

## PD {#pd}

-   etcdの起動エラーが原因でPDサーバーがスタックする問題を修正します[＃1267](https://github.com/pingcap/pd/pull/1267)
-   `pd-ctl` [＃1308](https://github.com/pingcap/pd/pull/1308)キーの読み取りに関連する問題を修正し[＃1298](https://github.com/pingcap/pd/pull/1298) [＃1299](https://github.com/pingcap/pd/pull/1299)
-   `regions/check`が間違った結果を返す問題を修正します[＃1311](https://github.com/pingcap/pd/pull/1311)
-   PDの参加に失敗した後、PDが参加を再開できない問題を修正します[＃1279](https://github.com/pingcap/pd/pull/1279)

## TiKV {#tikv}

-   `kv_scan`のインターフェイスに`end-key`の制限を追加します[＃3749](https://github.com/tikv/tikv/pull/3749)
-   `max-tasks-xxx`構成を破棄し、 [＃3093](https://github.com/tikv/tikv/pull/3093)を追加し`max-tasks-per-worker-xxx`
-   RocksDB3の`CompactFiles`の問題を修正し[＃3789](https://github.com/tikv/tikv/pull/3789)
