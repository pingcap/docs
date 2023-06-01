---
title: TiDB 3.0.17 Release Notes
---

# TiDB 3.0.17 リリースノート {#tidb-3-0-17-release-notes}

発売日：2020年8月3日

TiDB バージョン: 3.0.17

## 改善点 {#improvements}

-   TiDB

    -   `query-feedback-limit`構成項目のデフォルト値を 1024 から 512 に減らし、統計フィードバック メカニズムを改善してクラスター[#18770](https://github.com/pingcap/tidb/pull/18770)への影響を軽減します。
    -   1 つのリクエストのバッチ分割数を制限する[#18694](https://github.com/pingcap/tidb/pull/18694)
    -   TiDB クラスターに多数の履歴 DDL ジョブがある場合の`/tiflash/replica` HTTP API の高速化[#18386](https://github.com/pingcap/tidb/pull/18386)
    -   インデックス等しい条件[#17609](https://github.com/pingcap/tidb/pull/17609)の行数推定を改善しました。
    -   `kill tidb conn_id` [#18506](https://github.com/pingcap/tidb/pull/18506)の実行を高速化します。

-   TiKV

    -   ローリング アップデートのパフォーマンスを向上させるために、リージョンの休止状態を遅らせる`hibernate-timeout`構成を追加します[#8207](https://github.com/tikv/tikv/pull/8207)

-   ツール

    -   TiDB Lightning

        -   `[black-white-list]` 、より新しくわかりやすいフィルター形式[#332](https://github.com/pingcap/tidb-lightning/pull/332)で非推奨になりました。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `IndexHashJoin`または`IndexMergeJoin`含むクエリでpanicが発生した場合、空のセットではなく実際のエラー メッセージを返します[#18498](https://github.com/pingcap/tidb/pull/18498)
    -   `SELECT a FROM t HAVING t.a` [#18432](https://github.com/pingcap/tidb/pull/18432)のような SQL ステートメントの不明な列エラーを修正しました。
    -   テーブルに主キーがない場合、またはテーブルにすでに整数の主キーがある場合、テーブルへの主キーの追加を禁止します[#18342](https://github.com/pingcap/tidb/pull/18342)
    -   `EXPLAIN FORMAT="dot" FOR CONNECTION` [#17157](https://github.com/pingcap/tidb/pull/17157)を実行すると空のセットを返します
    -   修正`STR_TO_DATE`のフォーマット トークン &#39;%r&#39;、&#39;%h&#39; の処理[#18725](https://github.com/pingcap/tidb/pull/18725)

-   TiKV

    -   リージョンのマージ中に古いデータを読み取る可能性があるバグを修正[#8111](https://github.com/tikv/tikv/pull/8111)
    -   スケジューリングプロセス中のメモリリークの問題を修正[#8355](https://github.com/tikv/tikv/pull/8355)

-   ツール

    -   TiDB Lightning

        -   `log-file`フラグが無視される問題を修正[#345](https://github.com/pingcap/tidb-lightning/pull/345)
