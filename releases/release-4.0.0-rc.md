---
title: TiDB 4.0 RC Release Notes
summary: TiDB 4.0 RC は 2020 年 4 月 8 日にリリースされました。互換性の変更、バグ修正、新機能、ツールが含まれています。TiKV は悲観的トランザクションの `pipelined` 機能をサポートし、TPC-C パフォーマンスが 20% 向上します。TiDB は大文字と小文字を区別しない照合順序を追加し、`RECOVER TABLE` 構文を強化します。TiKV は HTTP ポートで TLS をサポートするようになりました。PD は HTTP API を介してデフォルトの PD 構成情報を取得することをサポートします。バグ修正には、レプリケーション、サブクエリ結果、DDL ジョブの内部再試行に関する問題が含まれます。TiDB TiDB Lightningや TiCDC などのツールにもバグ修正と新機能があります。
---

# TiDB 4.0 RC リリースノート {#tidb-4-0-rc-release-notes}

発売日: 2020年4月8日

TiDB バージョン: 4.0.0-rc

TiUPバージョン: 0.0.3

> **警告：**
>
> このバージョンではいくつかの既知の問題が見つかりましたが、これらの問題は新しいバージョンで修正されています。最新の 4.0.x バージョンを使用することをお勧めします。

## 互換性の変更 {#compatibility-changes}

-   ティビ

    -   tidb-server ステータス ポートが使用中の場合、アラート ログを返す代わりに開始を拒否します[＃15177](https://github.com/pingcap/tidb/pull/15177)

-   ティクヴ

    -   悲観的トランザクションの`pipelined`機能をサポートし、TPC-Cのパフォーマンスを20%向上させます。実行中のロック失敗によりトランザクションのコミットが失敗するリスクがあります[＃6984](https://github.com/tikv/tikv/pull/6984)
    -   新しいクラスターではデフォルトで`unify-read-pool`構成項目を有効にし、古いクラスターではこの項目の以前の設定を使用します[＃7059](https://github.com/tikv/tikv/pull/7059)

-   ツール

    -   TiDBBinlog

        -   共通名[＃934](https://github.com/pingcap/tidb-binlog/pull/934)を検証するための設定項目を追加する

## 重要なバグ修正 {#important-bug-fixes}

-   ティビ

    -   内部レコード[＃15435](https://github.com/pingcap/tidb/pull/15435)のジョブクエリが正しくないため、 `PREPARE`ステートメントを使用して DDL ジョブを実行すると、アップストリームとダウンストリーム間のレプリケーションが失敗する可能性がある問題を修正しました。
    -   分離レベル`Read Committed` [＃15471](https://github.com/pingcap/tidb/pull/15471)でのサブクエリ結果が不正確になる問題を修正
    -   インライン投影の最適化によって誤った結果が発生する問題を修正[＃15411](https://github.com/pingcap/tidb/pull/15411)
    -   SQLヒント`INL_MERGE_JOIN`が場合によっては誤って実行される問題を修正[＃15515](https://github.com/pingcap/tidb/pull/15515)
    -   `AutoRandom`属性の列に負の数が明示的に書き込まれると、それらの列がリベースされる問題を修正[＃15397](https://github.com/pingcap/tidb/pull/15397)

## 新機能 {#new-features}

-   ティビ

    -   大文字と小文字を区別しない照合順序を追加して、ユーザーが新しいクラスター[＃33](https://github.com/pingcap/tidb/projects/33)で`utf8mb4_general_ci`と`utf8_general_ci`を有効にできるようにします。
    -   切り捨てられたテーブル[＃15398](https://github.com/pingcap/tidb/pull/15398)回復をサポートするために`RECOVER TABLE`構文を拡張します
    -   tidb-server ステータス ポートが使用中の場合、アラート ログを返す代わりに開始を拒否します[＃15177](https://github.com/pingcap/tidb/pull/15177)
    -   デフォルトの列値としてシーケンスを使用する書き込みパフォーマンスを最適化する[＃15216](https://github.com/pingcap/tidb/pull/15216)
    -   DDLジョブ[＃14837](https://github.com/pingcap/tidb/pull/14837)の詳細を照会するためのシステムテーブル`DDLJobs`を追加します
    -   `aggFuncSum`パフォーマンス[＃14887](https://github.com/pingcap/tidb/pull/14887)を最適化する
    -   `EXPLAIN` [＃15507](https://github.com/pingcap/tidb/pull/15507)の出力を最適化する

-   ティクヴ

    -   悲観的トランザクションの`pipelined`機能をサポートし、TPC-Cのパフォーマンスを20%向上させます。実行中のロック失敗によりトランザクションのコミットが失敗するリスクがあります[＃6984](https://github.com/tikv/tikv/pull/6984)
    -   HTTPポート[＃5393](https://github.com/tikv/tikv/pull/5393)でTLSをサポート
    -   新しいクラスターではデフォルトで`unify-read-pool`構成項目を有効にし、古いクラスターではこの項目の以前の設定を使用します[＃7059](https://github.com/tikv/tikv/pull/7059)

-   PD

    -   HTTP API [＃2258](https://github.com/pingcap/pd/pull/2258)を介してデフォルトの PD 構成情報を取得する機能をサポート

-   ツール

    -   TiDBBinlog

        -   共通名[＃934](https://github.com/pingcap/tidb-binlog/pull/934)を検証するための設定項目を追加します

    -   TiDB Lightning

        -   TiDB Lightning [＃281](https://github.com/pingcap/tidb-lightning/pull/281) [＃275](https://github.com/pingcap/tidb-lightning/pull/275)のパフォーマンスを最適化する

## バグの修正 {#bug-fixes}

-   ティビ

    -   内部レコード[＃15435](https://github.com/pingcap/tidb/pull/15435)のジョブクエリが正しくないため、 `PREPARE`ステートメントを使用して DDL ジョブを実行すると、アップストリームとダウンストリーム間のレプリケーションが失敗する可能性がある問題を修正しました。
    -   分離レベル`Read Committed` [＃15471](https://github.com/pingcap/tidb/pull/15471)でのサブクエリ結果が不正確になる問題を修正
    -   `INSERT ... VALUES`を使用して`BIT(N)`データ型[＃15350](https://github.com/pingcap/tidb/pull/15350)を指定する場合に発生する可能性のある誤った動作の問題を修正しました。
    -   `ErrorCount`の値が正しく合計されないため、DDL ジョブの内部再試行で期待どおりの結果が完全に得られない問題を修正しました[＃15373](https://github.com/pingcap/tidb/pull/15373)
    -   TiDBがTiFlash [＃15505](https://github.com/pingcap/tidb/pull/15505)に接続したときにガベージコレクションが異常に動作する可能性がある問題を修正
    -   インライン投影の最適化によって誤った結果が発生する問題を修正[＃15411](https://github.com/pingcap/tidb/pull/15411)
    -   SQLヒント`INL_MERGE_JOIN`が場合によっては誤って実行される問題を修正[＃15515](https://github.com/pingcap/tidb/pull/15515)
    -   `AutoRandom`属性の列に負の数が明示的に書き込まれると、それらの列がリベースされる問題を修正[＃15397](https://github.com/pingcap/tidb/pull/15397)

-   ティクヴ
    -   Follower Read機能が有効になっているときにリーダーを転送すると発生する可能性のあるpanicを修正[＃7101](https://github.com/tikv/tikv/pull/7101)

-   ツール

    -   TiDB Lightning

        -   バックエンドがTiDB [＃283](https://github.com/pingcap/tidb-lightning/pull/283)の場合に文字変換エラーによって発生するデータエラーの問題を修正しました。

    -   ティCDC

        -   MySQLシンクがDDL文[＃353](https://github.com/pingcap/tiflow/pull/353)を実行する際に、下流に`test`スキーマが存在しない場合エラーが返される問題を修正
        -   CDC cli [＃351](https://github.com/pingcap/tiflow/pull/351)のリアルタイムインタラクティブモードをサポート
        -   データレプリケーション中に上流のテーブルが複製可能かどうかのチェックをサポート[＃368](https://github.com/pingcap/tiflow/pull/368)
        -   Kafka [＃344](https://github.com/pingcap/tiflow/pull/344)への非同期書き込みをサポート
