---
title: TiDB 2.0.9 Release Notes
---

# TiDB 2.0.9 リリースノート {#tidb-2-0-9-release-notes}

2018 年 11 月 19 日に、TiDB 2.0.9 がリリースされました。 TiDB 2.0.8 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   空の統計ヒストグラムによって引き起こされる問題を修正します[#7927](https://github.com/pingcap/tidb/pull/7927)
-   場合によっては`UNION ALL`ステートメントのpanicの問題を修正[#7942](https://github.com/pingcap/tidb/pull/7942)
-   間違った DDL ジョブによって引き起こされるスタック オーバーフローの問題を修正します[#7959](https://github.com/pingcap/tidb/pull/7959)
-   `Commit`操作[#7983](https://github.com/pingcap/tidb/pull/7983)の遅いログを追加します
-   大きすぎる`Limit`値[#8004](https://github.com/pingcap/tidb/pull/8004)によって引き起こされるpanicの問題を修正
-   `USING`条項[#8048](https://github.com/pingcap/tidb/pull/8048)での`utf8mb4`文字セットの指定をサポート
-   `TRUNCATE`組み込み関数が符号なし整数型[#8069](https://github.com/pingcap/tidb/pull/8069)のパラメータをサポートするようにします。
-   場合によっては統計モジュールの主キーの選択性推定の問題を修正します[#8150](https://github.com/pingcap/tidb/pull/8150)
-   `Session`変数を追加して、 [#8126](https://github.com/pingcap/tidb/pull/8126)に`_tidb_rowid`を書き込めるかどうかを制御します。
-   場合によっては`PhysicalProjection`のpanicの問題を修正[#8154](https://github.com/pingcap/tidb/pull/8154)
-   場合によっては`Union`ステートメントの結果が不安定になる問題を修正[#8168](https://github.com/pingcap/tidb/pull/8168)
-   `Insert`以外のステートメント[#8179](https://github.com/pingcap/tidb/pull/8179)で`values`によって`NULL`が返されない問題を修正します。
-   場合によっては統計モジュールが古いデータを消去できない問題を修正します[#8184](https://github.com/pingcap/tidb/pull/8184)
-   トランザクションの最大許容実行時間を構成可能なオプションにします[#8209](https://github.com/pingcap/tidb/pull/8209)
-   場合によっては`expression rewriter`の間違った比較アルゴリズムを修正しました[#8288](https://github.com/pingcap/tidb/pull/8288)
-   `UNION ORDER BY`ステートメント[#8307](https://github.com/pingcap/tidb/pull/8307)によって生成された余分な列を削除します。
-   `admin show next_row_id`ステートメント[#8274](https://github.com/pingcap/tidb/pull/8274)をサポートします
-   `Show Create Table`ステートメント[#8321](https://github.com/pingcap/tidb/pull/8321)の特殊文字のエスケープの問題を修正します。
-   場合によっては`UNION`ステートメントの予期しないエラーを修正します[#8318](https://github.com/pingcap/tidb/pull/8318)
-   DDL ジョブをキャンセルしても、場合によってはスキーマがロールバックされない問題を修正します[#8312](https://github.com/pingcap/tidb/pull/8312)
-   `tidb_max_chunk_size`をグローバル変数[#8333](https://github.com/pingcap/tidb/pull/8333)に変更します
-   オーバーバウンドスキャンを避けるために、ticlient の`Scan`コマンドに上限を追加します[#8309](https://github.com/pingcap/tidb/pull/8309) [#8310](https://github.com/pingcap/tidb/pull/8310)

## PD {#pd}

-   etcd の起動失敗により PDサーバーが停止する問題を修正[#1267](https://github.com/pingcap/pd/pull/1267)
-   `pd-ctl`リージョンキーの読み取りに関連する問題を修正します[#1298](https://github.com/pingcap/pd/pull/1298) [#1299](https://github.com/pingcap/pd/pull/1299) [#1308](https://github.com/pingcap/pd/pull/1308)
-   `regions/check` API が間違った結果を返す問題を修正[#1311](https://github.com/pingcap/pd/pull/1311)
-   PD 参加失敗後に PD が参加を再開できない問題を修正[#1279](https://github.com/pingcap/pd/pull/1279)

## TiKV {#tikv}

-   `kv_scan`インターフェース[#3749](https://github.com/tikv/tikv/pull/3749)に`end-key`制限を追加します。
-   `max-tasks-xxx`構成を放棄し、 `max-tasks-per-worker-xxx` [#3093](https://github.com/tikv/tikv/pull/3093)を追加します
-   RocksDB [#3789](https://github.com/tikv/tikv/pull/3789)の`CompactFiles`問題を修正
