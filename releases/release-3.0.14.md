---
title: TiDB 3.0.14 Release Notes
summary: TiDB 3.0.14 は 2020 年 5 月 9 日にリリースされました。このリリースには、互換性の変更、重要なバグ修正、新機能、バグ修正、および TiDB、TiKV、ツールの改善が含まれています。バグ修正には、クエリ結果の問題、panicの発生、および不正な動作が含まれます。新機能には、強化された構文サポートとパフォーマンスの向上が含まれます。
---

# TiDB 3.0.14 リリースノート {#tidb-3-0-14-release-notes}

発売日: 2020年5月9日

TiDB バージョン: 3.0.14

## 互換性の変更 {#compatibility-changes}

-   ティビ

    -   `performance_schema`と`metrics_schema`のユーザー権限を読み取り/書き込みから読み取り専用に調整します[＃15417](https://github.com/pingcap/tidb/pull/15417)

## 重要なバグ修正 {#important-bug-fixes}

-   ティビ

    -   `join`条件に`handle`属性[＃15734](https://github.com/pingcap/tidb/pull/15734)を持つ列に複数の同等の条件がある場合に`index join`のクエリ結果が正しくない問題を修正しました。
    -   `handle`属性[＃16079](https://github.com/pingcap/tidb/pull/16079)を持つ列に対して`fast analyze`操作を実行するときに発生するpanicを修正
    -   DDL ステートメントが`prepare`の方法で実行されると、DDL ジョブ構造の`query`フィールドが正しくないという問題を修正しました。この問題により、データ レプリケーションにBinlogが使用されている場合に、上流と下流の間でデータの不整合が発生する可能性があります[＃15443](https://github.com/pingcap/tidb/pull/15443)

-   ティクヴ

    -   ロックのクリーンアップの繰り返し要求によりトランザクションの原子性が破壊される可能性がある問題を修正[＃7388](https://github.com/tikv/tikv/pull/7388)

## 新機能 {#new-features}

-   ティビ

    -   `admin show ddl jobs`ステートメント[＃16428](https://github.com/pingcap/tidb/pull/16428)のクエリ結果にスキーマ名列とテーブル名列を追加します。
    -   切り捨てられたテーブル[＃15458](https://github.com/pingcap/tidb/pull/15458)の回復をサポートするために`RECOVER TABLE`構文を拡張します
    -   `SHOW GRANTS`文[＃16168](https://github.com/pingcap/tidb/pull/16168)の権限チェックをサポートする
    -   `LOAD DATA`文[＃16736](https://github.com/pingcap/tidb/pull/16736)の権限チェックをサポートする
    -   日付と時間に関連する関数をパーティションキーとして使用する場合のパーティションプルーニングのパフォーマンスを向上[＃15618](https://github.com/pingcap/tidb/pull/15618)
    -   `dispatch error`のログレベルを`WARN`から`ERROR`に調整します[＃16232](https://github.com/pingcap/tidb/pull/16232)
    -   クライアントにTLS [＃15415](https://github.com/pingcap/tidb/pull/15415)の使用を強制する`require-secure-transport`起動オプションをサポートする
    -   TLSが設定されている場合にTiDBコンポーネント間のHTTP通信をサポートする[＃15419](https://github.com/pingcap/tidb/pull/15419)
    -   現在のトランザクションの`start_ts`情報を`information_schema.processlist`テーブル[＃16160](https://github.com/pingcap/tidb/pull/16160)に追加します
    -   クラスター間の通信に使用されるTLS証明書情報の自動再読み込みをサポート[＃15162](https://github.com/pingcap/tidb/pull/15162)
    -   パーティションプルーニング[＃15628](https://github.com/pingcap/tidb/pull/15628)を再構築することで、パーティションテーブルの読み取りパフォーマンスを向上します。
    -   `range`パーティションテーブル[＃16521](https://github.com/pingcap/tidb/pull/16521)のパーティション式として`floor(unix_timestamp(a))`が使用される場合のパーティションプルーニング機能をサポートします。
    -   `view`含み、 `view` [＃16787](https://github.com/pingcap/tidb/pull/16787)を更新しない`update`文の実行を許可する
    -   ネストされた`view` s [＃15424](https://github.com/pingcap/tidb/pull/15424)作成を禁止する
    -   切り捨てを禁止する`view` [＃16420](https://github.com/pingcap/tidb/pull/16420)
    -   列が`public`状態[＃15576](https://github.com/pingcap/tidb/pull/15576)でない場合に、 `update`ステートメントを使用して列の値を明示的に更新することを禁止します。
    -   `status`ポートが占有されている場合に TiDB の起動を禁止する[＃15466](https://github.com/pingcap/tidb/pull/15466)
    -   `current_role`関数の文字セットを`binary`から`utf8mb4`に変更します[＃16083](https://github.com/pingcap/tidb/pull/16083)
    -   新しいリージョンのデータが読み取られたときに割り込み信号をチェックすることで、使いやすさ`max-execution-time`向上します[＃15615](https://github.com/pingcap/tidb/pull/15615)
    -   `auto_id` [＃16287](https://github.com/pingcap/tidb/pull/16287)のキャッシュステップを明示的に設定するための`ALTER TABLE ... AUTO_ID_CACHE`構文を追加します。

-   ティクヴ

    -   楽観的トランザクション[＃7605](https://github.com/tikv/tikv/pull/7605)で多くの競合と`BatchRollback`条件が存在する場合のパフォーマンスを向上
    -   悲観的トランザクション[＃7584](https://github.com/tikv/tikv/pull/7584)に多くの競合が存在する場合に悲観的ロック`waiter`が頻繁に起動されるために発生するパフォーマンス低下の問題を修正しました

-   ツール

    -   TiDB Lightning

        -   tidb-lightning-ctl [＃287](https://github.com/pingcap/tidb-lightning/pull/287)の`fetch-mode`サブコマンドを使用して TiKV クラスター モードの印刷をサポートします。

## バグ修正 {#bug-fixes}

-   ティビ

    -   SQLモードが`ALLOW_INVALID_DATES` [＃16170](https://github.com/pingcap/tidb/pull/16170)の場合、 `WEEKEND`関数がMySQLと互換性がない問題を修正しました。
    -   インデックス列に自動増分主キー[＃16008](https://github.com/pingcap/tidb/pull/16008)が含まれている場合に`DROP INDEX`ステートメントの実行が失敗する問題を修正しました。
    -   ステートメントサマリー[＃15231](https://github.com/pingcap/tidb/pull/15231)の`TABLE_NAMES`列目の値が間違っている問題を修正
    -   プランキャッシュが有効な場合に一部の式で誤った結果が発生する問題を修正[＃16184](https://github.com/pingcap/tidb/pull/16184)
    -   `not` / `istrue` / `isfalse`関数の結果が正しくない問題を修正[＃15916](https://github.com/pingcap/tidb/pull/15916)
    -   冗長インデックス[＃15919](https://github.com/pingcap/tidb/pull/15919)を持つテーブルに対する`MergeJoin`操作によって発生するpanicを修正
    -   述語が外部テーブル[＃16492](https://github.com/pingcap/tidb/pull/16492)のみを参照する場合にリンクを誤って簡略化することで発生する問題を修正しました。
    -   `CURRENT_ROLE`関数が`SET ROLE`ステートメント[＃15569](https://github.com/pingcap/tidb/pull/15569)によって発生したエラーを報告する問題を修正しました
    -   この文が`\` [＃16633](https://github.com/pingcap/tidb/pull/16633)に遭遇すると、 `LOAD DATA`文の結果がMySQLと互換性がない問題を修正しました。
    -   データベースの可視性がMySQL [＃14939](https://github.com/pingcap/tidb/pull/14939)と互換性がない問題を修正
    -   `SET DEFAULT ROLE ALL`文[＃15585](https://github.com/pingcap/tidb/pull/15585)の権限チェックが正しく行われない問題を修正
    -   プランキャッシュ[＃15818](https://github.com/pingcap/tidb/pull/15818)によるパーティションプルーニングの失敗の問題を修正
    -   トランザクションが関連テーブル[＃15707](https://github.com/pingcap/tidb/pull/15707)をロックしないため、テーブルに対して同時 DDL 操作が実行され、ブロッキングが存在する場合に、トランザクションのコミット中に`schema change`報告される問題を修正しました。
    -   `IF(not_int, *, *)` [＃15356](https://github.com/pingcap/tidb/pull/15356)の誤った動作を修正
    -   `CASE WHEN (not_int)` [＃15359](https://github.com/pingcap/tidb/pull/15359)の誤った動作を修正
    -   現在のスキーマ[＃15866](https://github.com/pingcap/tidb/pull/15866)に含まれていない`view`使用すると`Unknown column`エラー メッセージが返される問題を修正しました
    -   時間文字列の解析結果がMySQL [＃16242](https://github.com/pingcap/tidb/pull/16242)と互換性がない問題を修正
    -   右の子ノード[＃16528](https://github.com/pingcap/tidb/pull/16528)に`null`列が存在する場合に`left join`の照合順序子がパニックになる可能panicを修正
    -   TiKV が`StaleCommand`エラー メッセージ[＃16528](https://github.com/pingcap/tidb/pull/16528)を返し続けている場合に SQL 実行がブロックされているにもかかわらずエラー メッセージが返されない問題を修正しました。
    -   監査プラグインが有効になっているときにポートプローブによって発生する可能性のあるpanicを修正[＃15967](https://github.com/pingcap/tidb/pull/15967)
    -   `fast analyze`インデックス[＃15967](https://github.com/pingcap/tidb/pull/15967)のみで動作する場合のpanicを修正
    -   場合によっては`SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST`文の実行でpanicが発生する可能性があった問題を修正[＃16309](https://github.com/pingcap/tidb/pull/16309)
    -   ハッシュパーティションテーブルを作成する際に、メモリを割り当てる前にパーティション数をチェックせずに、多数のパーティション（たとえば`9999999999999` ）を指定すると TiDB OOM が発生する問題を修正しました[＃16218](https://github.com/pingcap/tidb/pull/16218)
    -   `information_schema.tidb_hot_table` [＃16726](https://github.com/pingcap/tidb/pull/16726)のパーティションテーブルの情報が間違っている問題を修正
    -   ハッシュパーティションテーブル[＃16070](https://github.com/pingcap/tidb/pull/16070)でパーティション選択アルゴリズムが有効にならない問題を修正
    -   MVCCシリーズのHTTP APIがパーティションテーブルをサポートしていない問題を修正[＃16191](https://github.com/pingcap/tidb/pull/16191)
    -   `UNION`番目の文のエラー処理を`SELECT`番目の文のエラー処理と一致させる[＃16137](https://github.com/pingcap/tidb/pull/16137)
    -   `VALUES`関数のパラメータ型が`bit(n)` [＃15486](https://github.com/pingcap/tidb/pull/15486)の場合に不正な動作が発生する問題を修正
    -   `view`列名が長すぎる場合に TiDB の処理ロジックが MySQL と一致しない問題を修正しました。この場合、システムは短い列名を自動的に生成します[＃14873](https://github.com/pingcap/tidb/pull/14873)
    -   `(not not col)`誤って`col` [＃16094](https://github.com/pingcap/tidb/pull/16094)として最適化される問題を修正
    -   `IndexLookupJoin`プラン[＃15753](https://github.com/pingcap/tidb/pull/15753)で構築された内部テーブルの`range`間違っている問題を修正
    -   `only_full_group_by`括弧付きの式を正しくチェックできない問題を修正[＃16012](https://github.com/pingcap/tidb/pull/16012)
    -   `select view_name.col_name from view_name`文を実行するとエラーが返される問題を修正[＃15572](https://github.com/pingcap/tidb/pull/15572)

-   ティクヴ

    -   一部のケースで分離回復後にノードを正しく削除できない問題を修正[＃7703](https://github.com/tikv/tikv/pull/7703)
    -   リージョンマージ操作[＃7679](https://github.com/tikv/tikv/pull/7679)によってネットワーク分離中に発生するデータ損失の問題を修正
    -   学習者を正しく削除できないことがある問題を修正[＃7598](https://github.com/tikv/tikv/pull/7598)
    -   生のキーと値のペアのスキャン結果が順序どおりに行われない可能性がある問題を修正[＃7597](https://github.com/tikv/tikv/pull/7597)
    -   Raftメッセージのバッチが大きすぎる場合の再接続の問題を修正[＃7542](https://github.com/tikv/tikv/pull/7542)
    -   空のリクエスト[＃7538](https://github.com/tikv/tikv/pull/7538)によって発生する gRPC スレッドのデッドロックの問題を修正
    -   マージ処理中に学習者を再起動する処理ロジックが正しくない問題を修正[＃7457](https://github.com/tikv/tikv/pull/7457)
    -   ロックのクリーンアップの繰り返し要求によりトランザクションの原子性が破壊される可能性がある問題を修正[＃7388](https://github.com/tikv/tikv/pull/7388)
