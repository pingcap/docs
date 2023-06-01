---
title: TiDB 2.0.9 Release Notes
---

# TiDB 2.0.9 リリースノート {#tidb-2-0-9-release-notes}

2018 年 11 月 19 日に、TiDB 2.0.9 がリリースされました。 TiDB 2.0.8 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   空の統計ヒストグラムによって引き起こされる問題を修正します[<a href="https://github.com/pingcap/tidb/pull/7927">#7927</a>](https://github.com/pingcap/tidb/pull/7927)
-   場合によっては`UNION ALL`ステートメントのpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/7942">#7942</a>](https://github.com/pingcap/tidb/pull/7942)
-   間違った DDL ジョブによって引き起こされるスタック オーバーフローの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/7959">#7959</a>](https://github.com/pingcap/tidb/pull/7959)
-   `Commit`操作[<a href="https://github.com/pingcap/tidb/pull/7983">#7983</a>](https://github.com/pingcap/tidb/pull/7983)の遅いログを追加します
-   大きすぎる`Limit`値[<a href="https://github.com/pingcap/tidb/pull/8004">#8004</a>](https://github.com/pingcap/tidb/pull/8004)によって引き起こされるpanicの問題を修正
-   `USING`条項[<a href="https://github.com/pingcap/tidb/pull/8048">#8048</a>](https://github.com/pingcap/tidb/pull/8048)での`utf8mb4`文字セットの指定をサポート
-   `TRUNCATE`組み込み関数が符号なし整数型[<a href="https://github.com/pingcap/tidb/pull/8069">#8069</a>](https://github.com/pingcap/tidb/pull/8069)のパラメータをサポートするようにします。
-   場合によっては統計モジュールの主キーの選択性推定の問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8150">#8150</a>](https://github.com/pingcap/tidb/pull/8150)
-   `Session`変数を追加して、 [<a href="https://github.com/pingcap/tidb/pull/8126">#8126</a>](https://github.com/pingcap/tidb/pull/8126)に`_tidb_rowid`を書き込めるかどうかを制御します。
-   場合によっては`PhysicalProjection`のpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/8154">#8154</a>](https://github.com/pingcap/tidb/pull/8154)
-   場合によっては`Union`ステートメントの結果が不安定になる問題を修正[<a href="https://github.com/pingcap/tidb/pull/8168">#8168</a>](https://github.com/pingcap/tidb/pull/8168)
-   `Insert`以外のステートメント[<a href="https://github.com/pingcap/tidb/pull/8179">#8179</a>](https://github.com/pingcap/tidb/pull/8179)で`values`によって`NULL`が返されない問題を修正します。
-   場合によっては統計モジュールが古いデータを消去できない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8184">#8184</a>](https://github.com/pingcap/tidb/pull/8184)
-   トランザクションの最大許容実行時間を構成可能なオプションにします[<a href="https://github.com/pingcap/tidb/pull/8209">#8209</a>](https://github.com/pingcap/tidb/pull/8209)
-   場合によっては`expression rewriter`の間違った比較アルゴリズムを修正しました[<a href="https://github.com/pingcap/tidb/pull/8288">#8288</a>](https://github.com/pingcap/tidb/pull/8288)
-   `UNION ORDER BY`ステートメント[<a href="https://github.com/pingcap/tidb/pull/8307">#8307</a>](https://github.com/pingcap/tidb/pull/8307)によって生成された余分な列を削除します。
-   `admin show next_row_id`ステートメント[<a href="https://github.com/pingcap/tidb/pull/8274">#8274</a>](https://github.com/pingcap/tidb/pull/8274)をサポートします
-   `Show Create Table`ステートメント[<a href="https://github.com/pingcap/tidb/pull/8321">#8321</a>](https://github.com/pingcap/tidb/pull/8321)の特殊文字のエスケープの問題を修正します。
-   場合によっては`UNION`ステートメントの予期しないエラーを修正します[<a href="https://github.com/pingcap/tidb/pull/8318">#8318</a>](https://github.com/pingcap/tidb/pull/8318)
-   DDL ジョブをキャンセルしても、場合によってはスキーマがロールバックされない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8312">#8312</a>](https://github.com/pingcap/tidb/pull/8312)
-   `tidb_max_chunk_size`をグローバル変数[<a href="https://github.com/pingcap/tidb/pull/8333">#8333</a>](https://github.com/pingcap/tidb/pull/8333)に変更します
-   オーバーバウンドスキャンを避けるために、ticlient の`Scan`コマンドに上限を追加します[<a href="https://github.com/pingcap/tidb/pull/8309">#8309</a>](https://github.com/pingcap/tidb/pull/8309) [<a href="https://github.com/pingcap/tidb/pull/8310">#8310</a>](https://github.com/pingcap/tidb/pull/8310)

## PD {#pd}

-   etcd の起動失敗により PDサーバーが停止する問題を修正[<a href="https://github.com/pingcap/pd/pull/1267">#1267</a>](https://github.com/pingcap/pd/pull/1267)
-   `pd-ctl`リージョンキーの読み取りに関連する問題を修正します[<a href="https://github.com/pingcap/pd/pull/1298">#1298</a>](https://github.com/pingcap/pd/pull/1298) [<a href="https://github.com/pingcap/pd/pull/1299">#1299</a>](https://github.com/pingcap/pd/pull/1299) [<a href="https://github.com/pingcap/pd/pull/1308">#1308</a>](https://github.com/pingcap/pd/pull/1308)
-   `regions/check` API が間違った結果を返す問題を修正[<a href="https://github.com/pingcap/pd/pull/1311">#1311</a>](https://github.com/pingcap/pd/pull/1311)
-   PD 参加失敗後に PD が参加を再開できない問題を修正[<a href="https://github.com/pingcap/pd/pull/1279">#1279</a>](https://github.com/pingcap/pd/pull/1279)

## TiKV {#tikv}

-   `kv_scan`インターフェース[<a href="https://github.com/tikv/tikv/pull/3749">#3749</a>](https://github.com/tikv/tikv/pull/3749)に`end-key`制限を追加します。
-   `max-tasks-xxx`構成を放棄し、 `max-tasks-per-worker-xxx` [<a href="https://github.com/tikv/tikv/pull/3093">#3093</a>](https://github.com/tikv/tikv/pull/3093)を追加します
-   RocksDB [<a href="https://github.com/tikv/tikv/pull/3789">#3789</a>](https://github.com/tikv/tikv/pull/3789)の`CompactFiles`問題を修正
