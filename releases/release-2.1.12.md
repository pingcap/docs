---
title: TiDB 2.1.12 Release Notes
summary: TiDB 2.1.12は2019年6月13日にリリースされました。データ型の不一致、文字セットの変更、GRANT操作に関する問題など、様々なバグ修正と改善が含まれています。また、MySQLとの互換性が向上し、関数、データ変換、エラーレポートに関する問題にも対処しています。さらに、PDとTiKVもアップデートされ、リーダー選出、リーダー移行時および電源障害時のデータ可用性に関する問題も修正されました。
---

# TiDB 2.1.12 リリースノート {#tidb-2-1-12-release-notes}

発売日：2019年6月13日

TiDB バージョン: 2.1.12

TiDB Ansible バージョン: 2.1.12

## TiDB {#tidb}

-   インデックスクエリフィードバック[＃10755](https://github.com/pingcap/tidb/pull/10755)を使用する際に、一致しないデータ型によって発生する問題を修正しました
-   一部のケースで文字セットの変更により BLOB 列がテキスト列に変更される問題を修正[＃10745](https://github.com/pingcap/tidb/pull/10745)
-   トランザクション内の`GRANT`の操作が、場合によっては「重複エントリ」を誤って報告する問題を修正しました[＃10739](https://github.com/pingcap/tidb/pull/10739)
-   以下の機能のMySQLとの互換性を向上
    -   `DAYNAME`機能[＃10732](https://github.com/pingcap/tidb/pull/10732)
    -   `MONTHNAME`機能[＃10733](https://github.com/pingcap/tidb/pull/10733)
    -   `MONTH` [＃10702](https://github.com/pingcap/tidb/pull/10702)を処理するときに`EXTRACT`関数の 0 値をサポートする
    -   `DECIMAL`型は`TIMESTAMP`または`DATETIME`に変換可能[＃10734](https://github.com/pingcap/tidb/pull/10734)
-   テーブルの文字セット[＃10714](https://github.com/pingcap/tidb/pull/10714)を変更するときに列の文字セットも変更する
-   一部のケースで小数を浮動小数点数に変換するときに発生するオーバーフローの問題を修正[＃10730](https://github.com/pingcap/tidb/pull/10730)
-   TiDB と TiKV [＃10710](https://github.com/pingcap/tidb/pull/10710)の gRPC で送受信されるメッセージの最大サイズが一致していないために、一部の非常に大きなメッセージで「grpc: 受信したメッセージが最大値を超えています」というエラーが報告される問題を修正しました。
-   `ORDER BY`一部のケースでNULLをフィルタリングしないことによって発生するpanic問題を修正[＃10488](https://github.com/pingcap/tidb/pull/10488)
-   複数のノードが存在する場合、 `UUID`関数によって返される値が重複する可能性がある問題を修正しました[＃10711](https://github.com/pingcap/tidb/pull/10711)
-   `CAST(-num as datetime)`によって返される値を`error`から NULL [＃10703](https://github.com/pingcap/tidb/pull/10703)に変更します
-   符号なしヒストグラムが符号付き範囲と一致する場合がある問題を修正[＃10695](https://github.com/pingcap/tidb/pull/10695)
-   統計フィードバックがbigint unsigned primary key [＃10307](https://github.com/pingcap/tidb/pull/10307)に一致すると、データの読み取りで誤ってエラーが報告される問題を修正しました。
-   パーティションテーブルの場合の`Show Create Table`の結果が、場合によっては正しく表示されない問題を修正しました[＃10690](https://github.com/pingcap/tidb/pull/10690)
-   `GROUP_CONCAT`集計関数の計算結果が一部の相関サブクエリに対して正しくない問題を修正[＃10670](https://github.com/pingcap/tidb/pull/10670)
-   スロークエリのメモリテーブルがスロークエリログを解析する際に、結果が誤って表示される場合がある問題を修正[＃10776](https://github.com/pingcap/tidb/pull/10776)

## PD {#pd}

-   極端な状況でetcdリーダー選出がブロックされる問題を修正[＃1576](https://github.com/pingcap/pd/pull/1576)

## TiKV {#tikv}

-   極端な状況でリーダー移行プロセス中にリージョンが利用できなくなる問題を修正[＃4799](https://github.com/tikv/tikv/pull/4734)
-   スナップショット[＃4850](https://github.com/tikv/tikv/pull/4850)受信時にディスクへのデータフラッシュが遅れることが原因で、マシンの電源が異常に落ちたときにTiKVがデータを失う問題を修正しました。
