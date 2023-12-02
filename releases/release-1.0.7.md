---
title: TiDB 1.0.7 Release Notes
---

# TiDB 1.0.7 リリースノート {#tidb-1-0-7-release-notes}

2018 年 1 月 22 日に、次の更新を含む TiDB 1.0.7 がリリースされました。

## TiDB {#tidb}

-   [`FIELD_LIST`コマンドを最適化する](https://github.com/pingcap/tidb/pull/5679)
-   [情報スキーマのデータ競合を修正](https://github.com/pingcap/tidb/pull/5676)
-   [読み取り専用ステートメントを履歴に追加しないようにする](https://github.com/pingcap/tidb/pull/5661)
-   [ログクエリを制御する`session`変数を追加します。](https://github.com/pingcap/tidb/pull/5659)
-   [統計におけるリソースリークの問題を修正](https://github.com/pingcap/tidb/pull/5657)
-   [goroutine リークの問題を修正する](https://github.com/pingcap/tidb/pull/5624)
-   [httpステータスサーバーのスキーマ情報APIを追加](https://github.com/pingcap/tidb/pull/5256)
-   [`IndexJoin`に関する問題を修正する](https://github.com/pingcap/tidb/pull/5623)
-   [DDL で`RunWorker` false の場合の動作を更新する](https://github.com/pingcap/tidb/pull/5604)
-   [統計におけるテスト結果の安定性を向上させる](https://github.com/pingcap/tidb/pull/5609)
-   [`CREATE TABLE`ステートメントの`PACK_KEYS`構文のサポート](https://github.com/pingcap/tidb/pull/5602)
-   [パフォーマンスを最適化するために、null プッシュダウン スキーマの`row_id`列を追加します。](https://github.com/pingcap/tidb/pull/5447)

## PD {#pd}

-   [異常な状況で発生する可能性のあるスケジュール損失の問題を修正](https://github.com/pingcap/pd/pull/921)
-   [proto3との互換性の問題を修正](https://github.com/pingcap/pd/pull/919)
-   [ログを追加する](https://github.com/pingcap/pd/pull/917)

## TiKV {#tikv}

-   [`Table Scan`をサポート](https://github.com/pingcap/tikv/pull/2657)
-   [tikv-ctlでリモートモードをサポート](https://github.com/pingcap/tikv/pull/2377)
-   [tikv-ctl protoのフォーマット互換性の問題を修正](https://github.com/pingcap/tikv/pull/2668)
-   [PD からのスケジューリング コマンドの損失を修正](https://github.com/pingcap/tikv/pull/2669)
-   [プッシュメトリクスにタイムアウトを追加する](https://github.com/pingcap/tikv/pull/2686)

1.0.6 から 1.0.7 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。
