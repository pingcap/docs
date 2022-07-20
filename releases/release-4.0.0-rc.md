---
title: TiDB 4.0 RC Release Notes
---

# TiDB4.0RCリリースノート {#tidb-4-0-rc-release-notes}

発売日：2020年4月8日

TiDBバージョン：4.0.0-rc

TiUPバージョン：0.0.3

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の4.0.xバージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   tidb-serverステータスポートが占有されているときにアラートログを返す代わりに開始を拒否する[＃15177](https://github.com/pingcap/tidb/pull/15177)

-   TiKV

    -   TPC-Cのパフォーマンスを20％向上させる、悲観的なトランザクションの`pipelined`つの機能をサポートします。リスクは、実行中のロックの失敗が原因でトランザクションのコミットが失敗する可能性があることです[＃6984](https://github.com/tikv/tikv/pull/6984)
    -   デフォルトで新しいクラスターで`unify-read-pool`の構成アイテムを有効にし、古いクラスターでこのアイテムの以前の設定を使用します[＃7059](https://github.com/tikv/tikv/pull/7059)

-   ツール

    -   TiDB Binlog

        -   共通名[＃934](https://github.com/pingcap/tidb-binlog/pull/934)を確認するための構成アイテムを追加します

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   内部レコード[＃15435](https://github.com/pingcap/tidb/pull/15435)のジョブクエリが正しくないために、 `PREPARE`ステートメントを使用してDDLジョブを実行すると、アップストリームとダウンストリーム間のレプリケーションが失敗する可能性がある問題を修正します。
    -   `Read Commited`分離レベル[＃15471](https://github.com/pingcap/tidb/pull/15471)での誤ったサブクエリ結果の問題を修正します
    -   インラインプロジェクションの最適化によって引き起こされる誤った結果の問題を修正します[＃15411](https://github.com/pingcap/tidb/pull/15411)
    -   SQLヒント`INL_MERGE_JOIN`が誤って実行される場合があるという問題を修正します[＃15515](https://github.com/pingcap/tidb/pull/15515)
    -   これらの列に負の数が明示的に書き込まれると、 `AutoRandom`属性の列がリベースされる問題を修正します[＃15397](https://github.com/pingcap/tidb/pull/15397)

## 新機能 {#new-features}

-   TiDB

    -   大文字と小文字を区別しない照合順序を追加して、ユーザーが新しいクラスタ[＃33](https://github.com/pingcap/tidb/projects/33)で`utf8mb4_general_ci`と`utf8_general_ci`を有効にできるようにします。
    -   切り捨てられたテーブルの回復をサポートするために`RECOVER TABLE`構文を拡張します[＃15398](https://github.com/pingcap/tidb/pull/15398)
    -   tidb-serverステータスポートが占有されているときにアラートログを返す代わりに開始を拒否する[＃15177](https://github.com/pingcap/tidb/pull/15177)
    -   シーケンスをデフォルトの列値として使用する書き込みパフォーマンスを最適化する[＃15216](https://github.com/pingcap/tidb/pull/15216)
    -   `DDLJobs`システムテーブルを追加して、DDLジョブの詳細をクエリします[＃14837](https://github.com/pingcap/tidb/pull/14837)
    -   `aggFuncSum`のパフォーマンスを最適化する[＃14887](https://github.com/pingcap/tidb/pull/14887)
    -   [＃15507](https://github.com/pingcap/tidb/pull/15507)の`EXPLAIN`を最適化する

-   TiKV

    -   TPC-Cのパフォーマンスを20％向上させる、悲観的なトランザクションの`pipelined`つの機能をサポートします。リスクは、実行中のロックの失敗が原因でトランザクションのコミットが失敗する可能性があることです[＃6984](https://github.com/tikv/tikv/pull/6984)
    -   HTTPポート[＃5393](https://github.com/tikv/tikv/pull/5393)でTLSをサポートする
    -   デフォルトで新しいクラスターで`unify-read-pool`の構成アイテムを有効にし、古いクラスターでこのアイテムの以前の設定を使用します[＃7059](https://github.com/tikv/tikv/pull/7059)

-   PD

    -   [＃2258](https://github.com/pingcap/pd/pull/2258)を介したデフォルトのPD構成情報の取得をサポート

-   ツール

    -   TiDB Binlog

        -   共通名[＃934](https://github.com/pingcap/tidb-binlog/pull/934)を確認するための構成アイテムを追加します

    -   TiDB Lightning

        -   TiDB Lightning [＃281](https://github.com/pingcap/tidb-lightning/pull/281) [＃275](https://github.com/pingcap/tidb-lightning/pull/275)を最適化する

## バグの修正 {#bug-fixes}

-   TiDB

    -   内部レコード[＃15435](https://github.com/pingcap/tidb/pull/15435)のジョブクエリが正しくないために、 `PREPARE`ステートメントを使用してDDLジョブを実行すると、アップストリームとダウンストリーム間のレプリケーションが失敗する可能性がある問題を修正します。
    -   `Read Commited`分離レベル[＃15471](https://github.com/pingcap/tidb/pull/15471)での誤ったサブクエリ結果の問題を修正します
    -   `INSERT ... VALUES`を使用して`BIT(N)`データ型[＃15350](https://github.com/pingcap/tidb/pull/15350)を指定するときに発生する可能性のある誤った動作の問題を修正します
    -   `ErrorCount`の値が正しく合計されないため、DDLジョブの内部再試行が期待される結果を完全に達成しないという問題を修正します[＃15373](https://github.com/pingcap/tidb/pull/15373)
    -   TiDBがTiFlash1に接続したときにガベージコレクションが異常に機能する可能性がある問題を修正し[＃15505](https://github.com/pingcap/tidb/pull/15505)
    -   インラインプロジェクションの最適化によって引き起こされる誤った結果の問題を修正します[＃15411](https://github.com/pingcap/tidb/pull/15411)
    -   SQLヒント`INL_MERGE_JOIN`が誤って実行される場合があるという問題を修正します[＃15515](https://github.com/pingcap/tidb/pull/15515)
    -   これらの列に負の数が明示的に書き込まれると、 `AutoRandom`属性の列がリベースされる問題を修正します[＃15397](https://github.com/pingcap/tidb/pull/15397)

-   TiKV
    -   フォロワー読み取り機能が有効になっているときにリーダーを転送することによって発生する可能性のあるpanicを修正します[＃7101](https://github.com/tikv/tikv/pull/7101)

-   ツール

    -   TiDB Lightning

        -   バックエンドがTiDB1の場合の文字変換のエラーによって引き起こされるデータエラーの問題を修正し[＃283](https://github.com/pingcap/tidb-lightning/pull/283)

    -   TiCDC

        -   MySQLシンクがDDLステートメント[＃353](https://github.com/pingcap/tiflow/pull/353)を実行しているときに、 `test`のスキーマがダウンストリームに存在しない場合にエラーが返される問題を修正します。
        -   [＃351](https://github.com/pingcap/tiflow/pull/351)でリアルタイムインタラクティブモードをサポートする
        -   データ複製中にアップストリームのテーブルを複製できるかどうかのチェックをサポート[＃368](https://github.com/pingcap/tiflow/pull/368)
        -   [＃344](https://github.com/pingcap/tiflow/pull/344)への非同期書き込みをサポート
