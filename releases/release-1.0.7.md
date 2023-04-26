---
title: TiDB 1.0.7 Release Notes
---

# TiDB 1.0.7 リリースノート {#tidb-1-0-7-release-notes}

2018 年 1 月 22 日に、TiDB 1.0.7 がリリースされ、次の更新が行われました。

## TiDB {#tidb}

-   [`FIELD_LIST`コマンドを最適化する](https://github.com/pingcap/tidb/pull/5679)
-   [情報スキーマのデータ競合を修正](https://github.com/pingcap/tidb/pull/5676)
-   [読み取り専用ステートメントを履歴に追加しない](https://github.com/pingcap/tidb/pull/5661)
-   [ログ クエリを制御する`session`変数を追加する](https://github.com/pingcap/tidb/pull/5659)
-   [統計のリソース リークの問題を修正](https://github.com/pingcap/tidb/pull/5657)
-   [ゴルーチンリークの問題を修正](https://github.com/pingcap/tidb/pull/5624)
-   [http ステータスサーバーのスキーマ情報 API を追加します。](https://github.com/pingcap/tidb/pull/5256)
-   [`IndexJoin`に関する問題を修正する](https://github.com/pingcap/tidb/pull/5623)
-   [DDL で`RunWorker` false の場合の動作を更新します](https://github.com/pingcap/tidb/pull/5604)
-   [統計におけるテスト結果の安定性の向上](https://github.com/pingcap/tidb/pull/5609)
-   [`CREATE TABLE`ステートメントの<code>PACK_KEYS</code>構文をサポート](https://github.com/pingcap/tidb/pull/5602)
-   [null プッシュダウン スキーマの`row_id`列を追加してパフォーマンスを最適化する](https://github.com/pingcap/tidb/pull/5447)

## PD {#pd}

-   [異常な状態で発生する可能性のあるスケジュール損失の問題を修正](https://github.com/pingcap/pd/pull/921)
-   [proto3 との互換性の問題を修正](https://github.com/pingcap/pd/pull/919)
-   [ログを追加する](https://github.com/pingcap/pd/pull/917)

## TiKV {#tikv}

-   [サポート`Table Scan`](https://github.com/pingcap/tikv/pull/2657)
-   [tikv-ctl でリモートモードをサポート](https://github.com/pingcap/tikv/pull/2377)
-   [tikv-ctl proto のフォーマット互換性の問題を修正](https://github.com/pingcap/tikv/pull/2668)
-   [PD からのスケジューリング コマンドの損失を修正](https://github.com/pingcap/tikv/pull/2669)
-   [Push メトリクスにタイムアウトを追加](https://github.com/pingcap/tikv/pull/2686)

1.0.6 から 1.0.7 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従ってください。
