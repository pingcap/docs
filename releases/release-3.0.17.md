---
title: TiDB 3.0.17 Release Notes
summary: TiDB 3.0.17は2020年8月3日にリリースされました。このリリースには、query-feedback-limit設定項目のデフォルト値の引き下げなどの改善や、空セットではなく実際のエラーメッセージを返すなどのバグ修正が含まれています。TiKVでは、ローリングアップデートのパフォーマンスを向上させるために、hibernate-timeout設定も追加されました。TiDB TiDB Lightning、ブラックホワイトリストフィルタ形式が非推奨となり、ログファイルフラグが無視される問題が修正されました。
---

# TiDB 3.0.17 リリースノート {#tidb-3-0-17-release-notes}

発売日: 2020年8月3日

TiDB バージョン: 3.0.17

## 改善点 {#improvements}

-   TiDB

    -   `query-feedback-limit`構成項目のデフォルト値を1024から512に減らし、統計フィードバックメカニズムを改善してクラスタ[＃18770](https://github.com/pingcap/tidb/pull/18770)への影響を軽減します。
    -   1 回のリクエストのバッチ分割数を制限する[＃18694](https://github.com/pingcap/tidb/pull/18694)
    -   TiDB クラスタ[＃18386](https://github.com/pingcap/tidb/pull/18386)に多くの履歴 DDL ジョブがある場合に`/tiflash/replica` HTTP API を高速化する
    -   インデックスの等価条件[＃17609](https://github.com/pingcap/tidb/pull/17609)行数推定の改善
    -   `kill tidb conn_id` [＃18506](https://github.com/pingcap/tidb/pull/18506)の実行を高速化する

-   TiKV

    -   ローリングアップデートのパフォーマンスを向上させるために、リージョンの休止状態を遅らせる`hibernate-timeout`構成を追加します[＃8207](https://github.com/tikv/tikv/pull/8207)

-   ツール

    -   TiDB Lightning

        -   `[black-white-list]` 、より新しい、より理解しやすいフィルター形式[＃332](https://github.com/pingcap/tidb-lightning/pull/332)で廃止されました。

## バグ修正 {#bug-fixes}

-   TiDB

    -   `IndexHashJoin`または`IndexMergeJoin`を含むクエリがpanic[＃18498](https://github.com/pingcap/tidb/pull/18498)に遭遇した場合、空のセットではなく実際のエラー メッセージを返します。
    -   `SELECT a FROM t HAVING t.a` [＃18432](https://github.com/pingcap/tidb/pull/18432)のようなSQL文の不明な列エラーを修正
    -   テーブルに主キーがない場合、またはテーブルにすでに整数の主キーがある場合は、テーブルに主キーを追加することを禁止します[＃18342](https://github.com/pingcap/tidb/pull/18342)
    -   `EXPLAIN FORMAT="dot" FOR CONNECTION` [＃17157](https://github.com/pingcap/tidb/pull/17157)実行すると空のセットを返します
    -   フォーマットトークン &#39;%r&#39;、&#39;%h&#39; [＃18725](https://github.com/pingcap/tidb/pull/18725)処理を修正`STR_TO_DATE`

-   TiKV

    -   リージョンマージ中に古いデータを読み取る可能性があるバグを修正[＃8111](https://github.com/tikv/tikv/pull/8111)
    -   スケジュール処理中のメモリリークの問題を修正[＃8355](https://github.com/tikv/tikv/pull/8355)

-   ツール

    -   TiDB Lightning

        -   `log-file`フラグが無視される問題を修正[＃345](https://github.com/pingcap/tidb-lightning/pull/345)
