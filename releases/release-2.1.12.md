---
title: TiDB 2.1.12 Release Notes
---

# TiDB 2.1.12 リリースノート {#tidb-2-1-12-release-notes}

発売日：2019年6月13日

TiDB バージョン: 2.1.12

TiDB アンシブル バージョン: 2.1.12

## TiDB {#tidb}

-   インデックス クエリ フィードバック[#10755](https://github.com/pingcap/tidb/pull/10755)を使用する場合のデータ型の不一致によって発生する問題を修正します。
-   場合によっては文字セットの変更によって blob 列が text 列に変更される問題を修正します[#10745](https://github.com/pingcap/tidb/pull/10745)
-   トランザクションの`GRANT`操作で、場合によっては「重複入力」が誤って報告される問題を修正します[#10739](https://github.com/pingcap/tidb/pull/10739)
-   以下の機能の MySQL との互換性を向上させます。
    -   `DAYNAME`機能[#10732](https://github.com/pingcap/tidb/pull/10732)
    -   `MONTHNAME`機能[#10733](https://github.com/pingcap/tidb/pull/10733)
    -   `MONTH` [#10702](https://github.com/pingcap/tidb/pull/10702)を処理する場合、 `EXTRACT`関数の 0 値をサポートします。
    -   `DECIMAL`タイプは`TIMESTAMP`または`DATETIME` [#10734](https://github.com/pingcap/tidb/pull/10734)に変換できます
-   テーブルの文字セットを変更しながら列の文字セットを変更する[#10714](https://github.com/pingcap/tidb/pull/10714)
-   場合によっては[#10730](https://github.com/pingcap/tidb/pull/10730)進数を浮動小数点数に変換する際のオーバーフローの問題を修正します。
-   TiDB および TiKV [#10710](https://github.com/pingcap/tidb/pull/10710)の gRPC で送受信されるメッセージの最大サイズの不一致が原因で、一部の非常に大きなメッセージで「grpc: received message large than max」エラーが報告される問題を修正します。
-   `ORDER BY`場合によっては NULL をフィルタリングしないことによって引き起こさpanicの問題を修正します[#10488](https://github.com/pingcap/tidb/pull/10488)
-   複数のノードが存在する場合、 `UUID`関数によって返される値が重複する可能性がある問題を修正します[#10711](https://github.com/pingcap/tidb/pull/10711)
-   `CAST(-num as datetime)`が返す値を`error`から NULL [#10703](https://github.com/pingcap/tidb/pull/10703)に変更します
-   場合によっては、符号なしヒストグラムが符号付き範囲を満たす問題を修正します[#10695](https://github.com/pingcap/tidb/pull/10695)
-   統計フィードバックが bigint unsigned primary key [#10307](https://github.com/pingcap/tidb/pull/10307)に一致する場合、データの読み取りで誤ってエラーが報告される問題を修正します。
-   分割されたテーブルの`Show Create Table`の結果が正しく表示されない場合がある問題を修正[#10690](https://github.com/pingcap/tidb/pull/10690)
-   `GROUP_CONCAT`集約関数の計算結果が一部の相関サブクエリで正しくない問題を修正[#10670](https://github.com/pingcap/tidb/pull/10670)
-   スロークエリのメモリテーブルがスロークエリのログをパースすると、結果が正しく表示されない場合がある問題を修正[#10776](https://github.com/pingcap/tidb/pull/10776)

## PD {#pd}

-   極端な状況で etcd リーダーの選出がブロックされる問題を修正します[#1576](https://github.com/pingcap/pd/pull/1576)

## TiKV {#tikv}

-   極端な状況でリーダーの転送プロセス中にリージョンが使用できない問題を修正します[#4799](https://github.com/tikv/tikv/pull/4734)
-   スナップショット受信時のディスクへのデータフラッシュの遅延により、マシンの電源異常時に TiKV がデータを失う問題を修正[#4850](https://github.com/tikv/tikv/pull/4850)
