---
title: TiDB 3.0.17 Release Notes
---

# TiDB3.0.17リリースノート {#tidb-3-0-17-release-notes}

発売日：2020年8月3日

TiDBバージョン：3.0.17

## 改善 {#improvements}

-   TiDB

    -   `query-feedback-limit`構成項目のデフォルト値を1024から512に減らし、統計フィードバックメカニズムを改善して、クラスタ[＃18770](https://github.com/pingcap/tidb/pull/18770)への影響を緩和します。
    -   1つのリクエストのバッチ分割数を制限する[＃18694](https://github.com/pingcap/tidb/pull/18694)
    -   TiDBクラスタ[＃18386](https://github.com/pingcap/tidb/pull/18386)に多くの履歴DDLジョブがある場合、 `/tiflash/replica`つのHTTPAPIを高速化します。
    -   インデックスが等しい条件[＃17609](https://github.com/pingcap/tidb/pull/17609)の行数の推定を改善します
    -   `kill tidb conn_id`の実行を[＃18506](https://github.com/pingcap/tidb/pull/18506)アップ

-   TiKV

    -   ローリング更新のパフォーマンスを向上させるために、リージョンの休止状態を遅らせる`hibernate-timeout`の構成を追加します[＃8207](https://github.com/tikv/tikv/pull/8207)

-   ツール

    -   TiDB Lightning

        -   `[black-white-list]`は、より新しく、理解しやすいフィルター形式[＃332](https://github.com/pingcap/tidb-lightning/pull/332)で非推奨になりました。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `IndexHashJoin`つまたは`IndexMergeJoin`を含むクエリでpanicが発生した場合は、空のセットではなく実際のエラーメッセージを返します[＃18498](https://github.com/pingcap/tidb/pull/18498)
    -   `SELECT a FROM t HAVING t.a`のようなSQLステートメントの不明な列エラーを修正し[＃18432](https://github.com/pingcap/tidb/pull/18432)
    -   テーブルに主キーがない場合、またはテーブルにすでに整数の主キーがある場合は、テーブルに主キーを追加することを禁止します[＃18342](https://github.com/pingcap/tidb/pull/18342)
    -   `EXPLAIN FORMAT="dot" FOR CONNECTION`を実行すると空のセットを返し[＃17157](https://github.com/pingcap/tidb/pull/17157)
    -   フォーマットトークン&#39;％r&#39;、&#39;％ [＃18725](https://github.com/pingcap/tidb/pull/18725)の`STR_TO_DATE`の処理を修正

-   TiKV

    -   リージョンのマージ中に古いデータを読み取る可能性があるバグを修正します[＃8111](https://github.com/tikv/tikv/pull/8111)
    -   スケジューリングプロセス中のメモリリークの問題を修正します[＃8355](https://github.com/tikv/tikv/pull/8355)

-   ツール

    -   TiDB Lightning

        -   `log-file`フラグが無視される問題を修正します[＃345](https://github.com/pingcap/tidb-lightning/pull/345)
