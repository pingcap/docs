---
title: TiDB 2.1.12 Release Notes
---

# TiDB 2.1.12 リリースノート {#tidb-2-1-12-release-notes}

発売日：2019年6月13日

TiDB バージョン: 2.1.12

TiDB Ansible バージョン: 2.1.12

## TiDB {#tidb}

-   インデックス クエリ フィードバック[#10755](https://github.com/pingcap/tidb/pull/10755)を使用するときにデータ型が一致しないことによって発生する問題を修正します。
-   場合によっては、文字セットの変更によって BLOB 列がテキスト列に変更される問題を修正します[#10745](https://github.com/pingcap/tidb/pull/10745)
-   トランザクション内の`GRANT`オペレーションが誤って「重複エントリ」を報告する場合がある問題を修正[#10739](https://github.com/pingcap/tidb/pull/10739)
-   以下の機能のMySQLとの互換性を向上します。
    -   `DAYNAME`機能[#10732](https://github.com/pingcap/tidb/pull/10732)
    -   `MONTHNAME`機能[#10733](https://github.com/pingcap/tidb/pull/10733)
    -   `MONTH` [#10702](https://github.com/pingcap/tidb/pull/10702)を処理するときに`EXTRACT`関数の 0 値をサポートします。
    -   `DECIMAL`タイプは`TIMESTAMP`または`DATETIME` [#10734](https://github.com/pingcap/tidb/pull/10734)に変換できます
-   テーブルの文字セットを変更するときに列の文字セットを変更する[#10714](https://github.com/pingcap/tidb/pull/10714)
-   場合によっては[#10730](https://github.com/pingcap/tidb/pull/10730)進数を浮動小数点に変換するときのオーバーフローの問題を修正します。
-   TiDB および TiKV [#10710](https://github.com/pingcap/tidb/pull/10710)の gRPC で送受信されるメッセージの最大サイズが一貫していないために、一部の非常に大きなメッセージで「grpc: 最大値より大きいメッセージを受信しました」エラーが報告される問題を修正
-   場合によっては`ORDER BY`をフィルタリングしないことによって引き起こされるpanicの問題を修正します[#10488](https://github.com/pingcap/tidb/pull/10488)
-   複数のノードが存在する場合に`UUID`関数によって返される値が重複する可能性がある問題を修正します[#10711](https://github.com/pingcap/tidb/pull/10711)
-   `CAST(-num as datetime)`によって返される値を`error`から NULL [#10703](https://github.com/pingcap/tidb/pull/10703)に変更します。
-   場合によっては、符号なしヒストグラムが符号付き範囲と一致する問題を修正します[#10695](https://github.com/pingcap/tidb/pull/10695)
-   統計フィードバックが bigint の署名なし主キー[#10307](https://github.com/pingcap/tidb/pull/10307)に一致する場合、データの読み取りに関するエラーが誤って報告される問題を修正します。
-   パーティションテーブルの`Show Create Table`の結果が正しく表示されない場合がある問題を修正[#10690](https://github.com/pingcap/tidb/pull/10690)
-   一部の相関サブクエリ[#10670](https://github.com/pingcap/tidb/pull/10670)において、 `GROUP_CONCAT`集計関数の計算結果が正しくない問題を修正
-   スロークエリのメモリテーブルがスロークエリログを解析すると、結果が誤って表示される場合がある問題を修正[#10776](https://github.com/pingcap/tidb/pull/10776)

## PD {#pd}

-   極端な状況で etcd リーダーの選出がブロックされる問題を修正[#1576](https://github.com/pingcap/pd/pull/1576)

## TiKV {#tikv}

-   極限状態[#4799](https://github.com/tikv/tikv/pull/4734)でのリーダー転送プロセス中にリージョンが利用できない問題を修正
-   スナップショットの受信時にディスクへのデータのフラッシュが遅れたため、マシンの電源が異常に落ちたときに TiKV がデータを失う問題を修正します[#4850](https://github.com/tikv/tikv/pull/4850)
