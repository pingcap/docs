---
title: TiDB 2.1.12 Release Notes
---

# TiDB2.1.12リリースノート {#tidb-2-1-12-release-notes}

発売日：2019年6月13日

TiDBバージョン：2.1.12

TiDB Ansibleバージョン：2.1.12

## TiDB {#tidb}

-   インデックスクエリフィードバックを使用するときにデータ型が一致しないために発生する問題を修正します[＃10755](https://github.com/pingcap/tidb/pull/10755)
-   場合によっては文字セットの変更によってblob列がテキスト列に変更される問題を修正します[＃10745](https://github.com/pingcap/tidb/pull/10745)
-   トランザクションの`GRANT`の操作が誤って「重複エントリ」を報告する場合があるという問題を修正します[＃10739](https://github.com/pingcap/tidb/pull/10739)
-   次の機能のMySQLとの互換性を改善します
    -   `DAYNAME`機能[＃10732](https://github.com/pingcap/tidb/pull/10732)
    -   `MONTHNAME`機能[＃10733](https://github.com/pingcap/tidb/pull/10733)
    -   35を処理するときに`EXTRACT`関数の`MONTH`値をサポートし[＃10702](https://github.com/pingcap/tidb/pull/10702)
    -   `DECIMAL`タイプは`TIMESTAMP`または[＃10734](https://github.com/pingcap/tidb/pull/10734)に変換でき`DATETIME`
-   テーブルの文字セットを変更しながら、列の文字セットを変更する[＃10714](https://github.com/pingcap/tidb/pull/10714)
-   場合によっては、小数を浮動小数点に変換するときのオーバーフローの問題を修正します[＃10730](https://github.com/pingcap/tidb/pull/10730)
-   一部の非常に大きなメッセージが、TiDBおよびTiKV1の[＃10710](https://github.com/pingcap/tidb/pull/10710)によって送受信されるメッセージの最大サイズが一貫していないために発生する「grpc：受信メッセージが最大より大きい」エラーを報告する問題を修正します。
-   `ORDER BY`が場合によってはNULLをフィルタリングしないことによって引き起こされるpanicの問題を修正します[＃10488](https://github.com/pingcap/tidb/pull/10488)
-   複数のノードが存在する場合、 `UUID`関数によって返される値が重複する可能性がある問題を修正します[＃10711](https://github.com/pingcap/tidb/pull/10711)
-   `CAST(-num as datetime)`によって返される値を`error`からNULL5に変更し[＃10703](https://github.com/pingcap/tidb/pull/10703)
-   場合によっては、符号なしヒストグラムが符号付き範囲を満たす問題を修正します[＃10695](https://github.com/pingcap/tidb/pull/10695)
-   統計フィードバックがbigintunsignedプライマリキー[＃10307](https://github.com/pingcap/tidb/pull/10307)に一致したときに、データの読み取りでエラーが誤って報告される問題を修正します。
-   パーティション化されたテーブルの`Show Create Table`の結果が正しく表示されない場合があるという問題を修正します[＃10690](https://github.com/pingcap/tidb/pull/10690)
-   一部の相関サブクエリでは、 `GROUP_CONCAT`集計関数の計算結果が正しくないという問題を修正します[＃10670](https://github.com/pingcap/tidb/pull/10670)
-   遅いクエリのメモリテーブルが遅いクエリログを解析するときに結果が誤って表示される問題を修正します[＃10776](https://github.com/pingcap/tidb/pull/10776)

## PD {#pd}

-   etcdリーダー選出が極端な条件でブロックされる問題を修正します[＃1576](https://github.com/pingcap/pd/pull/1576)

## TiKV {#tikv}

-   極限状態でのリーダー移籍プロセス中にリージョンが利用できないという問題を修正します[＃4799](https://github.com/tikv/tikv/pull/4734)
-   スナップショットの受信時にディスクへのデータフラッシュが遅れたために、マシンの電源が異常に低下したときにTiKVがデータを失う問題を修正します[＃4850](https://github.com/tikv/tikv/pull/4850)
