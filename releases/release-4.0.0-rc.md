---
title: TiDB 4.0 RC Release Notes
---

# TiDB 4.0 RC リリースノート {#tidb-4-0-rc-release-notes}

発売日：2020年4月8日

TiDB バージョン: 4.0.0-rc

TiUPバージョン: 0.0.3

> **警告：**
>
> このバージョンにはいくつかの既知の問題があり、これらの問題は新しいバージョンで修正されています。最新の 4.0.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   tidb-server ステータス ポートが占有されている場合、アラート ログを返す代わりに開始を拒否する[#15177](https://github.com/pingcap/tidb/pull/15177)

-   TiKV

    -   TPC-C のパフォーマンスを 20% 向上させる悲観的トランザクションの`pipelined`機能をサポートします。リスクは、実行中のロックの失敗により、トランザクションのコミットが失敗する可能性があることです[#6984](https://github.com/tikv/tikv/pull/6984)
    -   デフォルトで新しいクラスターで`unify-read-pool`構成項目を有効にし、古いクラスターでこの項目の以前の設定を使用します[#7059](https://github.com/tikv/tikv/pull/7059)

-   ツール

    -   TiDBBinlog

        -   Common Name [#934](https://github.com/pingcap/tidb-binlog/pull/934)を検証するための構成アイテムを追加します。

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `PREPARE`ステートメントでDDLジョブを実行すると、内部レコードのジョブクエリが正しくないため、アップストリームとダウンストリーム間のレプリケーションが失敗する可能性がある問題を修正[#15435](https://github.com/pingcap/tidb/pull/15435)
    -   サブクエリの結果が`Read Commited`分離レベル[#15471](https://github.com/pingcap/tidb/pull/15471)になる問題を修正
    -   Inline Projection の最適化によって引き起こされる不正確な結果の問題を修正します[#15411](https://github.com/pingcap/tidb/pull/15411)
    -   SQL Hint `INL_MERGE_JOIN`が正しく実行されない場合がある問題を修正[#15515](https://github.com/pingcap/tidb/pull/15515)
    -   負の数がこれらの列に明示的に書き込まれると、 `AutoRandom`属性を持つ列がリベースされる問題を修正します[#15397](https://github.com/pingcap/tidb/pull/15397)

## 新機能 {#new-features}

-   TiDB

    -   大文字と小文字を区別しない照合順序を追加して、ユーザーが新しいクラスターで`utf8mb4_general_ci`と`utf8_general_ci`を有効にできるようにします[#33](https://github.com/pingcap/tidb/projects/33)
    -   `RECOVER TABLE`構文を拡張して、切り捨てられたテーブルの回復をサポートする[#15398](https://github.com/pingcap/tidb/pull/15398)
    -   tidb-server ステータス ポートが占有されている場合、アラート ログを返す代わりに開始を拒否する[#15177](https://github.com/pingcap/tidb/pull/15177)
    -   デフォルト列値としてシーケンスを使用する書き込みパフォーマンスを最適化します[#15216](https://github.com/pingcap/tidb/pull/15216)
    -   `DDLJobs`システム テーブルを追加して、DDL ジョブの詳細を照会します[#14837](https://github.com/pingcap/tidb/pull/14837)
    -   `aggFuncSum`パフォーマンスを最適化する[#14887](https://github.com/pingcap/tidb/pull/14887)
    -   `EXPLAIN` [#15507](https://github.com/pingcap/tidb/pull/15507)の出力を最適化する

-   TiKV

    -   TPC-C のパフォーマンスを 20% 向上させる悲観的トランザクションの`pipelined`機能をサポートします。リスクは、実行中のロックの失敗により、トランザクションのコミットが失敗する可能性があることです[#6984](https://github.com/tikv/tikv/pull/6984)
    -   HTTP ポート[#5393](https://github.com/tikv/tikv/pull/5393)での TLS のサポート
    -   デフォルトで新しいクラスターで`unify-read-pool`構成項目を有効にし、古いクラスターでこの項目の以前の設定を使用します[#7059](https://github.com/tikv/tikv/pull/7059)

-   PD

    -   HTTP API [#2258](https://github.com/pingcap/pd/pull/2258)を介したデフォルトの PD 構成情報の取得をサポート

-   ツール

    -   TiDBBinlog

        -   Common Name [#934](https://github.com/pingcap/tidb-binlog/pull/934)を検証するための構成アイテムを追加します。

    -   TiDB Lightning

        -   TiDB Lightning [#281](https://github.com/pingcap/tidb-lightning/pull/281) [#275](https://github.com/pingcap/tidb-lightning/pull/275)のパフォーマンスを最適化する

## バグの修正 {#bug-fixes}

-   TiDB

    -   `PREPARE`ステートメントでDDLジョブを実行すると、内部レコードのジョブクエリが正しくないため、アップストリームとダウンストリーム間のレプリケーションが失敗する可能性がある問題を修正[#15435](https://github.com/pingcap/tidb/pull/15435)
    -   サブクエリの結果が`Read Commited`分離レベル[#15471](https://github.com/pingcap/tidb/pull/15471)になる問題を修正
    -   `INSERT ... VALUES`を使用して`BIT(N)`データ型[#15350](https://github.com/pingcap/tidb/pull/15350)を指定すると、誤った動作が発生する可能性がある問題を修正します。
    -   `ErrorCount`の値が正しく合計されないため、DDL ジョブの内部再試行が期待される結果を完全に達成しないという問題を修正します[#15373](https://github.com/pingcap/tidb/pull/15373)
    -   TiDB がTiFlash [#15505](https://github.com/pingcap/tidb/pull/15505)に接続するとガベージ コレクションが異常に動作することがある問題を修正
    -   Inline Projection の最適化[#15411](https://github.com/pingcap/tidb/pull/15411)が原因で誤った結果が生じる問題を修正
    -   SQL Hint `INL_MERGE_JOIN`が正しく実行されない場合がある問題を修正[#15515](https://github.com/pingcap/tidb/pull/15515)
    -   負の数がこれらの列に明示的に書き込まれると、 `AutoRandom`属性を持つ列がリベースされる問題を修正します[#15397](https://github.com/pingcap/tidb/pull/15397)

-   TiKV
    -   Follower Readpanicが有効になっているときにリーダーを転送することによって引き起こされる可能性のあるパニックを修正します[#7101](https://github.com/tikv/tikv/pull/7101)

-   ツール

    -   TiDB Lightning

        -   バックエンドがTiDB [#283](https://github.com/pingcap/tidb-lightning/pull/283)の場合、文字変換エラーによりデータエラーが発生する問題を修正

    -   TiCDC

        -   MySQL シンクが DDL ステートメント[#353](https://github.com/pingcap/tiflow/pull/353)を実行しているときに、下流に`test`スキーマが存在しない場合にエラーが返される問題を修正
        -   CDC cli [#351](https://github.com/pingcap/tiflow/pull/351)でリアルタイム インタラクティブ モードをサポート
        -   データ複製時にアップストリームのテーブルが複製可能かどうかのチェックをサポート[#368](https://github.com/pingcap/tiflow/pull/368)
        -   Kafka [#344](https://github.com/pingcap/tiflow/pull/344)への非同期書き込みをサポート
