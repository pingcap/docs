---
title: TiDB 4.0 RC Release Notes
---

# TiDB 4.0 RC リリース ノート {#tidb-4-0-rc-release-notes}

発売日：2020年4月8日

TiDB バージョン: 4.0.0-rc

TiUPバージョン：0.0.3

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかり、これらの問題は新しいバージョンで修正されています。最新の 4.0.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   tidb-server ステータス ポートが占有されている場合、アラート ログを返す代わりに開始を拒否します[#15177](https://github.com/pingcap/tidb/pull/15177)

-   TiKV

    -   悲観的トランザクションで`pipelined`機能をサポートし、TPC-C のパフォーマンスを 20% 向上させます。リスクとしては、実行中のロック障害によりトランザクションのコミットが失敗する可能性があることです[#6984](https://github.com/tikv/tikv/pull/6984)
    -   新しいクラスターでは`unify-read-pool`構成項目をデフォルトで有効にし、古いクラスターではこの項目の以前の設定を使用します[#7059](https://github.com/tikv/tikv/pull/7059)

-   ツール

    -   TiDBBinlog

        -   Common Name [#934](https://github.com/pingcap/tidb-binlog/pull/934)を検証するための設定項目を追加します

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `PREPARE`ステートメントを使用して DDL ジョブを実行すると、内部レコード[#15435](https://github.com/pingcap/tidb/pull/15435)のジョブ クエリが正しくないために、上流と下流の間のレプリケーションが失敗する可能性がある問題を修正します。
    -   `Read Commited`分離レベル[#15471](https://github.com/pingcap/tidb/pull/15471)でのサブクエリの結果が正しくない問題を修正
    -   インライン投影の最適化[#15411](https://github.com/pingcap/tidb/pull/15411)によって引き起こされる不正確な結果の問題を修正します。
    -   SQLヒント`INL_MERGE_JOIN`が正しく実行されない場合がある問題を修正[#15515](https://github.com/pingcap/tidb/pull/15515)
    -   `AutoRandom`属性を持つ列に負の数値が明示的に書き込まれると、これらの列がリベースされる問題を修正します[#15397](https://github.com/pingcap/tidb/pull/15397)

## 新機能 {#new-features}

-   TiDB

    -   大文字と小文字を区別しない照合順序を追加して、ユーザーが新しいクラスターで`utf8mb4_general_ci`と`utf8_general_ci`有効にできるようにします[#33](https://github.com/pingcap/tidb/projects/33)
    -   切り捨てられたテーブルのリカバリをサポートするために`RECOVER TABLE`構文を拡張します[#15398](https://github.com/pingcap/tidb/pull/15398)
    -   tidb-server ステータス ポートが占有されている場合、アラート ログを返す代わりに開始を拒否します[#15177](https://github.com/pingcap/tidb/pull/15177)
    -   シーケンスをデフォルトの列値として使用する場合の書き込みパフォーマンスを最適化する[#15216](https://github.com/pingcap/tidb/pull/15216)
    -   DDL ジョブの詳細をクエリする`DDLJobs`システム テーブルを追加します[#14837](https://github.com/pingcap/tidb/pull/14837)
    -   `aggFuncSum`パフォーマンスを最適化する[#14887](https://github.com/pingcap/tidb/pull/14887)
    -   `EXPLAIN` [#15507](https://github.com/pingcap/tidb/pull/15507)の出力を最適化する

-   TiKV

    -   悲観的トランザクションで`pipelined`機能をサポートし、TPC-C のパフォーマンスを 20% 向上させます。リスクとしては、実行中のロック障害によりトランザクションのコミットが失敗する可能性があることです[#6984](https://github.com/tikv/tikv/pull/6984)
    -   HTTP ポート[#5393](https://github.com/tikv/tikv/pull/5393)での TLS のサポート
    -   新しいクラスターでは`unify-read-pool`構成項目をデフォルトで有効にし、古いクラスターではこの項目の以前の設定を使用します[#7059](https://github.com/tikv/tikv/pull/7059)

-   PD

    -   HTTP API [#2258](https://github.com/pingcap/pd/pull/2258)を介したデフォルトの PD 構成情報の取得のサポート

-   ツール

    -   TiDBBinlog

        -   Common Name [#934](https://github.com/pingcap/tidb-binlog/pull/934)を検証するための設定項目を追加します

    -   TiDB Lightning

        -   TiDB Lightning [#281](https://github.com/pingcap/tidb-lightning/pull/281) [#275](https://github.com/pingcap/tidb-lightning/pull/275)のパフォーマンスを最適化する

## バグの修正 {#bug-fixes}

-   TiDB

    -   `PREPARE`ステートメントを使用して DDL ジョブを実行すると、内部レコード[#15435](https://github.com/pingcap/tidb/pull/15435)のジョブ クエリが正しくないために、上流と下流の間のレプリケーションが失敗する可能性がある問題を修正します。
    -   `Read Commited`分離レベル[#15471](https://github.com/pingcap/tidb/pull/15471)でのサブクエリの結果が正しくない問題を修正
    -   `INSERT ... VALUES`を使用して`BIT(N)`データ型を指定すると誤った動作が発生する可能性がある問題を修正します[#15350](https://github.com/pingcap/tidb/pull/15350)
    -   `ErrorCount`の値が正しく合計されないため、DDL ジョブの内部再試行が予期した結果を完全に達成できない問題を修正します[#15373](https://github.com/pingcap/tidb/pull/15373)
    -   TiDB がTiFlash [#15505](https://github.com/pingcap/tidb/pull/15505)に接続するとガベージ コレクションが異常に動作することがある問題を修正
    -   インライン投影の最適化[#15411](https://github.com/pingcap/tidb/pull/15411)によって引き起こされる誤った結果の問題を修正します。
    -   SQLヒント`INL_MERGE_JOIN`が正しく実行されない場合がある問題を修正[#15515](https://github.com/pingcap/tidb/pull/15515)
    -   `AutoRandom`属性を持つ列に負の数値が明示的に書き込まれると、これらの列がリベースされる問題を修正します[#15397](https://github.com/pingcap/tidb/pull/15397)

-   TiKV
    -   Follower Readpanicが有効になっている場合にリーダーを転送することによって発生する可能性のあるパニックを修正しました[#7101](https://github.com/tikv/tikv/pull/7101)

-   ツール

    -   TiDB Lightning

        -   バックエンドがTiDB [#283](https://github.com/pingcap/tidb-lightning/pull/283)の場合、文字変換エラーによりデータエラーが発生する問題を修正

    -   TiCDC

        -   MySQL シンクが DDL ステートメント[#353](https://github.com/pingcap/tiflow/pull/353)を実行しているときに、ダウンストリームに`test`スキーマが存在しない場合にエラーが返される問題を修正します。
        -   CDC cli [#351](https://github.com/pingcap/tiflow/pull/351)でのリアルタイム対話モードのサポート
        -   データ レプリケーション中にアップストリームのテーブルをレプリケートできるかどうかのチェックをサポート[#368](https://github.com/pingcap/tiflow/pull/368)
        -   Kafka [#344](https://github.com/pingcap/tiflow/pull/344)への非同期書き込みをサポート
