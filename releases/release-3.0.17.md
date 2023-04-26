---
title: TiDB 3.0.17 Release Notes
---

# TiDB 3.0.17 リリースノート {#tidb-3-0-17-release-notes}

発売日：2020年8月3日

TiDB バージョン: 3.0.17

## 改良点 {#improvements}

-   TiDB

    -   `query-feedback-limit`構成項目のデフォルト値を 1024 から 512 に減らし、統計フィードバック メカニズムを改善してクラスターへの影響を緩和します[#18770](https://github.com/pingcap/tidb/pull/18770)
    -   1 つのリクエストのバッチ分割数を制限する[#18694](https://github.com/pingcap/tidb/pull/18694)
    -   TiDB クラスタにヒストリ DDL ジョブが多い場合の HTTP API の高速化`/tiflash/replica` [#18386](https://github.com/pingcap/tidb/pull/18386)
    -   インデックスが等しい条件[#17609](https://github.com/pingcap/tidb/pull/17609)の行数の見積もりを改善する
    -   `kill tidb conn_id` [#18506](https://github.com/pingcap/tidb/pull/18506)の実行速度を上げる

-   TiKV

    -   ローリング更新のパフォーマンスを向上させるためにリージョンの休止状態を遅らせる`hibernate-timeout`構成を追加します[#8207](https://github.com/tikv/tikv/pull/8207)

-   ツール

    -   TiDB Lightning

        -   `[black-white-list]`より新しく理解しやすいフィルター形式[#332](https://github.com/pingcap/tidb-lightning/pull/332)で廃止されました。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `IndexHashJoin`または`IndexMergeJoin`含むクエリでpanic[#18498](https://github.com/pingcap/tidb/pull/18498)が発生した場合、空のセットではなく実際のエラー メッセージを返します。
    -   `SELECT a FROM t HAVING t.a` [#18432](https://github.com/pingcap/tidb/pull/18432)などの SQL ステートメントの不明な列エラーを修正します。
    -   テーブルに主キーがない場合、またはテーブルに整数の主キーが既にある場合に、テーブルの主キーを追加することを禁止する[#18342](https://github.com/pingcap/tidb/pull/18342)
    -   `EXPLAIN FORMAT="dot" FOR CONNECTION` [#17157](https://github.com/pingcap/tidb/pull/17157)の実行時に空のセットを返す
    -   `STR_TO_DATE`のフォーマット トークン &#39;%r&#39;、&#39;%h&#39; の処理を修正[#18725](https://github.com/pingcap/tidb/pull/18725)

-   TiKV

    -   リージョンのマージ中に古いデータを読み取る可能性があるバグを修正します[#8111](https://github.com/tikv/tikv/pull/8111)
    -   スケジューリング プロセス中のメモリリークの問題を修正します[#8355](https://github.com/tikv/tikv/pull/8355)

-   ツール

    -   TiDB Lightning

        -   `log-file`フラグが無視される問題を修正[#345](https://github.com/pingcap/tidb-lightning/pull/345)
