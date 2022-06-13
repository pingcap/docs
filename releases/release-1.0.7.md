---
title: TiDB 1.0.7 Release Notes
---

# TiDB1.0.7リリースノート {#tidb-1-0-7-release-notes}

2018年1月22日に、TiDB1.0.7が次のアップデートでリリースされます。

## TiDB {#tidb}

-   [`FIELD_LIST`コマンドを最適化する](https://github.com/pingcap/tidb/pull/5679)
-   [情報スキーマのデータ競合を修正](https://github.com/pingcap/tidb/pull/5676)
-   [履歴に読み取り専用ステートメントを追加しないでください](https://github.com/pingcap/tidb/pull/5661)
-   [`session`変数を追加して、ログクエリを制御します](https://github.com/pingcap/tidb/pull/5659)
-   [統計のリソースリークの問題を修正します](https://github.com/pingcap/tidb/pull/5657)
-   [ゴルーチンリークの問題を修正する](https://github.com/pingcap/tidb/pull/5624)
-   [httpステータスサーバーのスキーマ情報APIを追加します](https://github.com/pingcap/tidb/pull/5256)
-   [`IndexJoin`に関する問題を修正します](https://github.com/pingcap/tidb/pull/5623)
-   [DDLで`RunWorker`がfalseの場合の動作を更新します](https://github.com/pingcap/tidb/pull/5604)
-   [統計におけるテスト結果の安定性を向上させる](https://github.com/pingcap/tidb/pull/5609)
-   [`CREATE TABLE`ステートメントの<code>PACK_KEYS</code>構文をサポートします](https://github.com/pingcap/tidb/pull/5602)
-   [パフォーマンスを最適化するために、nullプッシュダウンスキーマの`row_id`列を追加します](https://github.com/pingcap/tidb/pull/5447)

## PD {#pd}

-   [異常な状態で発生する可能性のあるスケジューリング損失の問題を修正](https://github.com/pingcap/pd/pull/921)
-   [proto3との互換性の問題を修正します](https://github.com/pingcap/pd/pull/919)
-   [ログを追加する](https://github.com/pingcap/pd/pull/917)

## TiKV {#tikv}

-   [`Table Scan`サポート](https://github.com/pingcap/tikv/pull/2657)
-   [tikv-ctlでリモートモードをサポートする](https://github.com/pingcap/tikv/pull/2377)
-   [tikv-ctlprotoのフォーマット互換性の問題を修正](https://github.com/pingcap/tikv/pull/2668)
-   [PDからのスケジューリングコマンドの損失を修正](https://github.com/pingcap/tikv/pull/2669)
-   [プッシュメトリックにタイムアウトを追加](https://github.com/pingcap/tikv/pull/2686)

1.0.6から1.0.7にアップグレードするには、PD-&gt;TiKV-&gt;TiDBのローリングアップグレードの順序に従います。
