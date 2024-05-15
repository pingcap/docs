---
title: TiDB 1.0.7 Release Notes
summary: TiDB 1.0.7 is released with various updates including optimization of commands, fixing data race and resource leak issues, adding session variable for log query control, and improving stability of test results. PD and TiKV also have updates to fix scheduling loss issues, compatibility issues, and add support for table scan and remote mode in tikv-ctl. To upgrade from 1.0.6 to 1.0.7, follow the rolling upgrade order of PD, TiKV, and TiDB.
---

# TiDB 1.0.7 リリースノート {#tidb-1-0-7-release-notes}

2018 年 1 月 22 日に、次の更新を含む TiDB 1.0.7 がリリースされました。

## ティビ {#tidb}

-   [`FIELD_LIST`コマンドを最適化する](https://github.com/pingcap/tidb/pull/5679)
-   [情報スキーマのデータ競合を修正](https://github.com/pingcap/tidb/pull/5676)
-   [読み取り専用ステートメントを履歴に追加しないようにする](https://github.com/pingcap/tidb/pull/5661)
-   [ログクエリを制御するための`session`変数を追加する](https://github.com/pingcap/tidb/pull/5659)
-   [統計情報のリソースリーク問題を修正](https://github.com/pingcap/tidb/pull/5657)
-   [ゴルーチンリークの問題を修正](https://github.com/pingcap/tidb/pull/5624)
-   [httpステータスサーバーのスキーマ情報APIを追加](https://github.com/pingcap/tidb/pull/5256)
-   [`IndexJoin`に関する問題を修正](https://github.com/pingcap/tidb/pull/5623)
-   [DDLで`RunWorker`がfalseの場合の動作を更新します](https://github.com/pingcap/tidb/pull/5604)
-   [統計におけるテスト結果の安定性を向上](https://github.com/pingcap/tidb/pull/5609)
-   [`CREATE TABLE`ステートメントの`PACK_KEYS`構文をサポート](https://github.com/pingcap/tidb/pull/5602)
-   [パフォーマンスを最適化するために、null プッシュダウン スキーマに`row_id`列を追加します。](https://github.com/pingcap/tidb/pull/5447)

## PD {#pd}

-   [異常な状況でスケジュールが失われる可能性がある問題を修正](https://github.com/pingcap/pd/pull/921)
-   [proto3との互換性の問題を修正](https://github.com/pingcap/pd/pull/919)
-   [ログを追加する](https://github.com/pingcap/pd/pull/917)

## ティクヴ {#tikv}

-   [`Table Scan`サポート](https://github.com/pingcap/tikv/pull/2657)
-   [tikv-ctl のリモート モードをサポートする](https://github.com/pingcap/tikv/pull/2377)
-   [tikv-ctl protoのフォーマット互換性の問題を修正](https://github.com/pingcap/tikv/pull/2668)
-   [PDからのスケジュールコマンドの消失を修正](https://github.com/pingcap/tikv/pull/2669)
-   [プッシュメトリックにタイムアウトを追加する](https://github.com/pingcap/tikv/pull/2686)

1.0.6 から 1.0.7 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。
