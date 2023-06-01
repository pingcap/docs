---
title: TiDB 1.0.7 Release Notes
---

# TiDB 1.0.7 リリースノート {#tidb-1-0-7-release-notes}

2018 年 1 月 22 日に、次の更新を含む TiDB 1.0.7 がリリースされました。

## TiDB {#tidb}

-   [<a href="https://github.com/pingcap/tidb/pull/5679">`FIELD_LIST`コマンドを最適化する</a>](https://github.com/pingcap/tidb/pull/5679)
-   [<a href="https://github.com/pingcap/tidb/pull/5676">情報スキーマのデータ競合を修正</a>](https://github.com/pingcap/tidb/pull/5676)
-   [<a href="https://github.com/pingcap/tidb/pull/5661">読み取り専用ステートメントを履歴に追加しないようにする</a>](https://github.com/pingcap/tidb/pull/5661)
-   [<a href="https://github.com/pingcap/tidb/pull/5659">ログクエリを制御する`session`変数を追加します。</a>](https://github.com/pingcap/tidb/pull/5659)
-   [<a href="https://github.com/pingcap/tidb/pull/5657">統計におけるリソースリークの問題を修正</a>](https://github.com/pingcap/tidb/pull/5657)
-   [<a href="https://github.com/pingcap/tidb/pull/5624">goroutine リークの問題を修正する</a>](https://github.com/pingcap/tidb/pull/5624)
-   [<a href="https://github.com/pingcap/tidb/pull/5256">httpステータスサーバーのスキーマ情報APIを追加</a>](https://github.com/pingcap/tidb/pull/5256)
-   [<a href="https://github.com/pingcap/tidb/pull/5623">`IndexJoin`に関する問題を修正する</a>](https://github.com/pingcap/tidb/pull/5623)
-   [<a href="https://github.com/pingcap/tidb/pull/5604">DDL で`RunWorker` false の場合の動作を更新する</a>](https://github.com/pingcap/tidb/pull/5604)
-   [<a href="https://github.com/pingcap/tidb/pull/5609">統計におけるテスト結果の安定性を向上させる</a>](https://github.com/pingcap/tidb/pull/5609)
-   [<a href="https://github.com/pingcap/tidb/pull/5602">`CREATE TABLE`ステートメントの`PACK_KEYS`構文のサポート</a>](https://github.com/pingcap/tidb/pull/5602)
-   [<a href="https://github.com/pingcap/tidb/pull/5447">パフォーマンスを最適化するために、null プッシュダウン スキーマの`row_id`列を追加します。</a>](https://github.com/pingcap/tidb/pull/5447)

## PD {#pd}

-   [<a href="https://github.com/pingcap/pd/pull/921">異常な状況で発生する可能性のあるスケジュール損失の問題を修正</a>](https://github.com/pingcap/pd/pull/921)
-   [<a href="https://github.com/pingcap/pd/pull/919">proto3との互換性の問題を修正</a>](https://github.com/pingcap/pd/pull/919)
-   [<a href="https://github.com/pingcap/pd/pull/917">ログを追加する</a>](https://github.com/pingcap/pd/pull/917)

## TiKV {#tikv}

-   [<a href="https://github.com/pingcap/tikv/pull/2657">サポート`Table Scan`</a>](https://github.com/pingcap/tikv/pull/2657)
-   [<a href="https://github.com/pingcap/tikv/pull/2377">tikv-ctlでリモートモードをサポート</a>](https://github.com/pingcap/tikv/pull/2377)
-   [<a href="https://github.com/pingcap/tikv/pull/2668">tikv-ctl protoのフォーマット互換性の問題を修正</a>](https://github.com/pingcap/tikv/pull/2668)
-   [<a href="https://github.com/pingcap/tikv/pull/2669">PD からのスケジューリング コマンドの損失を修正</a>](https://github.com/pingcap/tikv/pull/2669)
-   [<a href="https://github.com/pingcap/tikv/pull/2686">プッシュメトリクスにタイムアウトを追加する</a>](https://github.com/pingcap/tikv/pull/2686)

1.0.6 から 1.0.7 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。
