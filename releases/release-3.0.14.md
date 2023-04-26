---
title: TiDB 3.0.14 Release Notes
---

# TiDB 3.0.14 リリースノート {#tidb-3-0-14-release-notes}

発売日：2020年5月9日

TiDB バージョン: 3.0.14

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `performance_schema`と`metrics_schema`のユーザー権限を読み取り/書き込みから読み取り専用に調整する[#15417](https://github.com/pingcap/tidb/pull/15417)

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `handle`属性[#15734](https://github.com/pingcap/tidb/pull/15734)のカラムで`join`条件に複数の同等条件がある場合、 `index join`のクエリ結果が正しくない問題を修正
    -   `handle`属性[#16079](https://github.com/pingcap/tidb/pull/16079)の列に対して`fast analyze`操作を行うとパニックが発生するpanicを修正
    -   `prepare`の方法で DDL ステートメントを実行すると、DDL ジョブ構造の`query`フィールドが正しくない問題を修正します。この問題により、 Binlog がデータ レプリケーションに使用されている場合、アップストリームとダウンストリームの間でデータの不整合が発生する可能性があります。 [#15443](https://github.com/pingcap/tidb/pull/15443)

-   TiKV

    -   ロックのクリーンアップでリクエストを繰り返すと、トランザクションの原子性が失われる可能性があるという問題を修正します[#7388](https://github.com/tikv/tikv/pull/7388)

## 新機能 {#new-features}

-   TiDB

    -   `admin show ddl jobs`ステートメント[#16428](https://github.com/pingcap/tidb/pull/16428)のクエリ結果にスキーマ名列とテーブル名列を追加します。
    -   `RECOVER TABLE`構文を拡張して、切り捨てられたテーブルの回復をサポートする[#15458](https://github.com/pingcap/tidb/pull/15458)
    -   `SHOW GRANTS`ステートメント[#16168](https://github.com/pingcap/tidb/pull/16168)の権限チェックをサポート
    -   `LOAD DATA`ステートメント[#16736](https://github.com/pingcap/tidb/pull/16736)の権限チェックをサポート
    -   時刻と日付に関連する関数がパーティション キーとして使用される場合のパーティション プルーニングのパフォーマンスを向上させます[#15618](https://github.com/pingcap/tidb/pull/15618)
    -   `dispatch error`のログレベルを`WARN`から`ERROR` [#16232](https://github.com/pingcap/tidb/pull/16232)に調整します
    -   クライアントに TLS [#15415](https://github.com/pingcap/tidb/pull/15415)の使用を強制する`require-secure-transport`起動オプションをサポート
    -   TLS が構成されている場合、TiDB コンポーネント間の HTTP 通信をサポートします[#15419](https://github.com/pingcap/tidb/pull/15419)
    -   `start_ts`現在のトランザクションの情報を`information_schema.processlist`テーブルに追加します[#16160](https://github.com/pingcap/tidb/pull/16160)
    -   クラスタ間の通信に使用される TLS 証明書情報の自動リロードをサポート[#15162](https://github.com/pingcap/tidb/pull/15162)
    -   パーティションプルーニングを再構築することにより、パーティション化されたテーブルの読み取りパフォーマンスを向上させます[#15628](https://github.com/pingcap/tidb/pull/15628)
    -   `range`パーティション テーブル[#16521](https://github.com/pingcap/tidb/pull/16521)のパーティション式として`floor(unix_timestamp(a))`が使用される場合、パーティション プルーニング機能をサポートします。
    -   `view`を含み、 `view` [#16787](https://github.com/pingcap/tidb/pull/16787)を更新しない`update`ステートメントの実行を許可する
    -   ネストした`view` s [#15424](https://github.com/pingcap/tidb/pull/15424)の作成を禁止する
    -   切り捨て禁止`view` [#16420](https://github.com/pingcap/tidb/pull/16420)
    -   この列が`public`状態でない場合、 `update`ステートメントを使用して列の値を明示的に更新することを禁止する[#15576](https://github.com/pingcap/tidb/pull/15576)
    -   `status`ポート占有時の TiDB 起動禁止[#15466](https://github.com/pingcap/tidb/pull/15466)
    -   `current_role`関数の文字セットを`binary`から`utf8mb4`に変更します[#16083](https://github.com/pingcap/tidb/pull/16083)
    -   新しいリージョンのデータが読み込まれるときに割り込み信号をチェックすることで、 `max-execution-time`使いやすさが向上します[#15615](https://github.com/pingcap/tidb/pull/15615)
    -   `auto_id` [#16287](https://github.com/pingcap/tidb/pull/16287)のキャッシュ ステップを明示的に設定するための`ALTER TABLE ... AUTO_ID_CACHE`構文を追加します。

-   TiKV

    -   楽観的トランザクションで競合が多く、 `BatchRollback`条件が存在する場合のパフォーマンスを向上させます[#7605](https://github.com/tikv/tikv/pull/7605)
    -   悲観的トランザクションに多くの競合が存在する場合、悲観的ロック`waiter`頻繁に起こされるために発生するパフォーマンスの低下の問題を修正します[#7584](https://github.com/tikv/tikv/pull/7584)

-   ツール

    -   TiDB Lightning

        -   tidb-lightning-ctl [#287](https://github.com/pingcap/tidb-lightning/pull/287)の`fetch-mode`サブコマンドを使用した TiKV クラスター モードの印刷をサポート

## バグの修正 {#bug-fixes}

-   TiDB

    -   SQL モードが`ALLOW_INVALID_DATES` [#16170](https://github.com/pingcap/tidb/pull/16170)の場合、 `WEEKEND`関数が MySQL と互換性がない問題を修正
    -   インデックス列に自動インクリメント主キー[#16008](https://github.com/pingcap/tidb/pull/16008)が含まれている場合、 `DROP INDEX`ステートメントの実行に失敗する問題を修正します。
    -   ステートメントの概要[#15231](https://github.com/pingcap/tidb/pull/15231)の`TABLE_NAMES`列の値が正しくない問題を修正します。
    -   プラン キャッシュが有効になっている場合、一部の式の結果が正しくない問題を修正します[#16184](https://github.com/pingcap/tidb/pull/16184)
    -   `not` / `istrue` / `isfalse`関数の結果が正しくない問題を修正[#15916](https://github.com/pingcap/tidb/pull/15916)
    -   `MergeJoin`冗長インデックスを持つテーブルでの操作によって引き起こされるpanicを修正します[#15919](https://github.com/pingcap/tidb/pull/15919)
    -   述語が外部テーブルのみを参照している場合に、リンクを誤って単純化することによって引き起こされる問題を修正します[#16492](https://github.com/pingcap/tidb/pull/16492)
    -   `CURRENT_ROLE`関数が`SET ROLE`ステートメントに起因するエラーを報告する問題を修正します[#15569](https://github.com/pingcap/tidb/pull/15569)
    -   このステートメントが`\` [#16633](https://github.com/pingcap/tidb/pull/16633)に遭遇すると、 `LOAD DATA`ステートメントの結果が MySQL と互換性がないという問題を修正します。
    -   データベースの可視性が MySQL [#14939](https://github.com/pingcap/tidb/pull/14939)と互換性がないという問題を修正
    -   `SET DEFAULT ROLE ALL`ステートメント[#15585](https://github.com/pingcap/tidb/pull/15585)の権限チェックが正しくない問題を修正
    -   プラン キャッシュが原因でパーティション プルーニングが失敗する問題を修正します[#15818](https://github.com/pingcap/tidb/pull/15818)
    -   トランザクションが関連するテーブルをロックしないため、テーブルで同時 DDL 操作が実行され、ブロックが存在する場合、トランザクションのコミット中に`schema change`が報告される問題を修正します[#15707](https://github.com/pingcap/tidb/pull/15707)
    -   `IF(not_int, *, *)` [#15356](https://github.com/pingcap/tidb/pull/15356)の誤った動作を修正
    -   `CASE WHEN (not_int)` [#15359](https://github.com/pingcap/tidb/pull/15359)の誤った動作を修正
    -   現在のスキーマ[#15866](https://github.com/pingcap/tidb/pull/15866)にない`view`を使用すると`Unknown column`エラー メッセージが返される問題を修正します。
    -   時刻文字列の解析結果が MySQL [#16242](https://github.com/pingcap/tidb/pull/16242)と互換性がない問題を修正
    -   右側の子ノード[#16528](https://github.com/pingcap/tidb/pull/16528)に`null`列が存在する場合に`left join`照合順序演算子がパニックになる可能panicがある問題を修正しました
    -   TiKV が`StaleCommand`エラー メッセージ[#16528](https://github.com/pingcap/tidb/pull/16528)を返し続けると、SQL 実行がブロックされているにもかかわらず、エラー メッセージが返されない問題を修正します。
    -   監査プラグインが有効になっているときにポートプローブによって引き起こされる可能性のあるpanicを修正します[#15967](https://github.com/pingcap/tidb/pull/15967)
    -   `fast analyze`インデックスのみで動作するときに発生するpanicを修正します[#15967](https://github.com/pingcap/tidb/pull/15967)
    -   場合によっては`SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST`ステートメントの実行で発生する可能panicを修正します[#16309](https://github.com/pingcap/tidb/pull/16309)
    -   メモリを割り当てる前にパーティションの数を確認せずにハッシュ パーティション テーブルを作成すると、多数のパーティション (たとえば`9999999999999` ) を指定することによって発生する TiDB OOM の問題を修正します[#16218](https://github.com/pingcap/tidb/pull/16218)
    -   `information_schema.tidb_hot_table` [#16726](https://github.com/pingcap/tidb/pull/16726)で分割されたテーブルの誤った情報の問題を修正します。
    -   パーティション選択アルゴリズムがハッシュパーティションテーブルで有効にならない問題を修正します[#16070](https://github.com/pingcap/tidb/pull/16070)
    -   MVCCシリーズのHTTP APIが分割テーブルに対応していない問題を修正[#16191](https://github.com/pingcap/tidb/pull/16191)
    -   `UNION`ステートメントのエラー処理と`SELECT`ステートメントのエラー処理の一貫性を保つ[#16137](https://github.com/pingcap/tidb/pull/16137)
    -   `VALUES`関数のパラメーターの型が`bit(n)` [#15486](https://github.com/pingcap/tidb/pull/15486)の場合に正しく動作しない問題を修正
    -   `view`カラム名が長すぎると、TiDBの処理ロジックがMySQLと矛盾する問題を修正。この場合、システムは短い列名を自動的に生成します。 [#14873](https://github.com/pingcap/tidb/pull/14873)
    -   `(not not col)`が`col` [#16094](https://github.com/pingcap/tidb/pull/16094)として誤って最適化される問題を修正
    -   `IndexLookupJoin`のプランで構築された内部テーブルの`range`が正しくない問題を修正[#15753](https://github.com/pingcap/tidb/pull/15753)
    -   `only_full_group_by`が括弧付きの式を正しくチェックできない問題を修正[#16012](https://github.com/pingcap/tidb/pull/16012)
    -   `select view_name.col_name from view_name`文実行時にエラーが返る問題を修正[#15572](https://github.com/pingcap/tidb/pull/15572)

-   TiKV

    -   隔離復旧後、ノードを正常に削除できない場合がある問題を修正[#7703](https://github.com/tikv/tikv/pull/7703)
    -   リージョン Merge 操作によるネットワーク分離中のデータ損失の問題を修正します[#7679](https://github.com/tikv/tikv/pull/7679)
    -   学習者を正しく削除できない場合がある問題を修正[#7598](https://github.com/tikv/tikv/pull/7598)
    -   生のキーと値のペアのスキャン結果が順不同である可能性がある問題を修正します[#7597](https://github.com/tikv/tikv/pull/7597)
    -   Raftメッセージのバッチが大きすぎる場合の再接続の問題を修正します[#7542](https://github.com/tikv/tikv/pull/7542)
    -   空のリクエストによって引き起こされる gRPC スレッドのデッドロックの問題を修正します[#7538](https://github.com/tikv/tikv/pull/7538)
    -   マージ処理中に学習器を再起動する処理ロジックが正しくない問題を修正[#7457](https://github.com/tikv/tikv/pull/7457)
    -   ロックのクリーンアップでリクエストを繰り返すと、トランザクションの原子性が失われる可能性があるという問題を修正します[#7388](https://github.com/tikv/tikv/pull/7388)
