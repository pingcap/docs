---
title: TiDB 2.0.9 Release Notes
summary: TiDB 2.0.9は2018年11月19日にリリースされ、システムの互換性と安定性が大幅に向上しました。このリリースには、統計ヒストグラムの空、UNION ALL文のpanic問題、スタックオーバーフロー問題、utf8mb4文字セットの指定のサポートなど、さまざまな問題の修正が含まれています。PDとTiKVでは、サーバーの起動失敗とインターフェース制限に関連する問題も修正されました。
---

# TiDB 2.0.9 リリースノート {#tidb-2-0-9-release-notes}

2018年11月19日にTiDB 2.0.9がリリースされました。このリリースでは、TiDB 2.0.8と比較して、システムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   統計ヒストグラムが空であることによる問題を修正 [＃7927](https://github.com/pingcap/tidb/pull/7927)
-   いくつかのケースで`UNION ALL`文のpanic問題を修正[＃7942](https://github.com/pingcap/tidb/pull/7942)
-   間違ったDDLジョブによって発生するスタックオーバーフローの問題を修正[＃7959](https://github.com/pingcap/tidb/pull/7959)
-   `Commit`操作のスローログを追加する [＃7983](https://github.com/pingcap/tidb/pull/7983)
-   `Limit`値が大きすぎるために発生するpanic問題を修正しました[＃8004](https://github.com/pingcap/tidb/pull/8004)
-   `USING`句で`utf8mb4`文字セットの指定をサポート [＃8048](https://github.com/pingcap/tidb/pull/8048)
-   `TRUNCATE`組み込み関数が符号なし整数型のパラメータをサポートするようにする [＃8069](https://github.com/pingcap/tidb/pull/8069)
-   一部のケースにおける統計モジュールの主キーの選択性推定の問題を修正[＃8150](https://github.com/pingcap/tidb/pull/8150)
-   `Session`変数を追加して、 `_tidb_rowid` に書き込むことができるかどうかを制御します。 [＃8126](https://github.com/pingcap/tidb/pull/8126)
-   `PhysicalProjection`で場合によってはpanic問題を修正[＃8154](https://github.com/pingcap/tidb/pull/8154)
-   いくつかのケースで`Union`文の不安定な結果を修正[＃8168](https://github.com/pingcap/tidb/pull/8168)
-   `Insert`以外の文で`NULL`が`values`を返さない問題を修正 [＃8179](https://github.com/pingcap/tidb/pull/8179)
-   統計モジュールが古いデータをクリアできないことがある問題を修正[＃8184](https://github.com/pingcap/tidb/pull/8184)
-   トランザクションの最大許容実行時間を構成可能なオプションにする[＃8209](https://github.com/pingcap/tidb/pull/8209)
-   `expression rewriter`のいくつかのケースでの誤った比較アルゴリズムを修正[＃8288](https://github.com/pingcap/tidb/pull/8288)
-   `UNION ORDER BY`文で生成された余分な列を削除します [＃8307](https://github.com/pingcap/tidb/pull/8307)
-   `admin show next_row_id`ステートメントをサポートする [＃8274](https://github.com/pingcap/tidb/pull/8274)
-   `Show Create Table`文の特殊文字のエスケープ問題を修正 [＃8321](https://github.com/pingcap/tidb/pull/8321)
-   いくつかのケースで`UNION`文の予期しないエラーを修正[＃8318](https://github.com/pingcap/tidb/pull/8318)
-   DDLジョブをキャンセルしてもスキーマがロールバックされない場合がある問題を修正[＃8312](https://github.com/pingcap/tidb/pull/8312)
-   `tidb_max_chunk_size`をグローバル変数に変更する [＃8333](https://github.com/pingcap/tidb/pull/8333)
-   ticlientの`Scan`コマンドに上限を追加して、オーバーバウンドスキャン を回避する [＃8310](https://github.com/pingcap/tidb/pull/8310) [＃8309](https://github.com/pingcap/tidb/pull/8309)

## PD {#pd}

-   etcdの起動失敗によりPDサーバーが停止する問題を修正[＃1267](https://github.com/pingcap/pd/pull/1267)
-   リージョンキーの読み取りに関連する問題を修正`pd-ctl` [＃1298](https://github.com/pingcap/pd/pull/1298) [＃1299](https://github.com/pingcap/pd/pull/1299) [＃1308](https://github.com/pingcap/pd/pull/1308)
-   `regions/check` APIが間違った結果を返す問題を修正[＃1311](https://github.com/pingcap/pd/pull/1311)
-   PD参加失敗後にPDが参加を再開できない問題を修正[＃1279](https://github.com/pingcap/pd/pull/1279)

## TiKV {#tikv}

-   `kv_scan`インターフェースに`end-key`制限を追加する [＃3749](https://github.com/tikv/tikv/pull/3749)
-   `max-tasks-xxx`構成を削除し、 `max-tasks-per-worker-xxx` を追加する [＃3093](https://github.com/tikv/tikv/pull/3093)
-   RocksDB の`CompactFiles`問題を修正 [＃3789](https://github.com/tikv/tikv/pull/3789)
