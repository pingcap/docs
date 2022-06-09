---
title: TiDB 3.0.14 Release Notes
---

# TiDB3.0.14リリースノート {#tidb-3-0-14-release-notes}

発売日：2020年5月9日

TiDBバージョン：3.0.14

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `performance_schema`と`metrics_schema`のユーザー権限を読み取り/書き込みから読み取り専用[＃15417](https://github.com/pingcap/tidb/pull/15417)に調整します

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `join`条件が`handle`属性[＃15734](https://github.com/pingcap/tidb/pull/15734)の列に複数の同等の条件を持っている場合、 `index join`のクエリ結果が正しくない問題を修正します。
    -   `handle`属性[＃16079](https://github.com/pingcap/tidb/pull/16079)の列で`fast analyze`操作を実行するときに発生するパニックを修正します。
    -   DDLステートメントが`prepare`の方法で実行されたときに、DDLジョブ構造の`query`フィールドが正しくないという問題を修正します。この問題により、Binlogがデータレプリケーションに使用されている場合、アップストリームとダウンストリームの間でデータの不整合が発生する可能性があります。 [＃15443](https://github.com/pingcap/tidb/pull/15443)

-   TiKV

    -   ロックのクリーンアップで繰り返し要求すると、トランザクションの原子性が破壊される可能性があるという問題を修正します[＃7388](https://github.com/tikv/tikv/pull/7388)

## 新機能 {#new-features}

-   TiDB

    -   `admin show ddl jobs`ステートメントのクエリ結果にスキーマ名列とテーブル名列を追加します[＃16428](https://github.com/pingcap/tidb/pull/16428)
    -   切り捨てられたテーブルの回復をサポートするために`RECOVER TABLE`構文を拡張します[＃15458](https://github.com/pingcap/tidb/pull/15458)
    -   `SHOW GRANTS`ステートメント[＃16168](https://github.com/pingcap/tidb/pull/16168)の特権チェックをサポートします。
    -   `LOAD DATA`ステートメント[＃16736](https://github.com/pingcap/tidb/pull/16736)の特権チェックをサポートします。
    -   日時に関連する機能をパーティションキーとして使用する場合のパーティションプルーニングのパフォーマンスを向上させる[＃15618](https://github.com/pingcap/tidb/pull/15618)
    -   `dispatch error`のログレベルを`WARN`から[＃16232](https://github.com/pingcap/tidb/pull/16232)に調整し`ERROR`
    -   クライアントに[＃15415](https://github.com/pingcap/tidb/pull/15415)の使用を強制する`require-secure-transport`のスタートアップオプションをサポートする
    -   TLSが構成されている場合にTiDBコンポーネント間のHTTP通信をサポートする[＃15419](https://github.com/pingcap/tidb/pull/15419)
    -   現在のトランザクションの`start_ts`の情報を`information_schema.processlist`のテーブルに追加します[＃16160](https://github.com/pingcap/tidb/pull/16160)
    -   クラスタ間の通信に使用されるTLS証明書情報の自動リロードをサポート[＃15162](https://github.com/pingcap/tidb/pull/15162)
    -   パーティションプルーニングを再構築することにより、パーティションテーブルの読み取りパフォーマンスを向上させます[＃15628](https://github.com/pingcap/tidb/pull/15628)
    -   `range`パーティションテーブル[＃16521](https://github.com/pingcap/tidb/pull/16521)のパーティション式として`floor(unix_timestamp(a))`が使用されている場合、パーティションプルーニング機能をサポートします。
    -   `view`を含み、 [＃16787](https://github.com/pingcap/tidb/pull/16787)を更新しない`update`ステートメントの実行を許可し`view` 。
    -   [＃15424](https://github.com/pingcap/tidb/pull/15424)された`view`の作成を禁止する
    -   [＃16420](https://github.com/pingcap/tidb/pull/16420)を禁止する`view`
    -   この列が`public`状態でない場合、 `update`ステートメントを使用して列の値を明示的に更新することを禁止します[＃15576](https://github.com/pingcap/tidb/pull/15576)
    -   `status`ポートが占有されているときにTiDBを開始することを禁止する[＃15466](https://github.com/pingcap/tidb/pull/15466)
    -   `current_role`関数の文字セットを`binary`から[＃16083](https://github.com/pingcap/tidb/pull/16083)に変更し`utf8mb4`
    -   新しいリージョンのデータが読み取られたときに割り込み信号をチェックすることにより、 `max-execution-time`の使いやすさを向上させます[＃15615](https://github.com/pingcap/tidb/pull/15615)
    -   [＃16287](https://github.com/pingcap/tidb/pull/16287)のキャッシュステップを明示的に設定するための`ALTER TABLE ... AUTO_ID_CACHE`構文を追加し`auto_id` 。

-   TiKV

    -   多くの競合があり、 `BatchRollback`の条件が楽観的なトランザクションに存在する場合のパフォーマンスを向上させます[＃7605](https://github.com/tikv/tikv/pull/7605)
    -   ペシミスティックトランザクション[＃7584](https://github.com/tikv/tikv/pull/7584)に多くの競合が存在する場合、ペシミスティックロック`waiter`が頻繁にウェイクアップされるために発生するパフォーマンスの低下の問題を修正します。

-   ツール

    -   TiDB Lightning

        -   tidb-lightning- [＃287](https://github.com/pingcap/tidb-lightning/pull/287)の`fetch-mode`サブコマンドを使用したTiKVクラスタモードの印刷をサポートします。

## バグの修正 {#bug-fixes}

-   TiDB

    -   SQLモードが35の場合、 `WEEKEND` [＃16170](https://github.com/pingcap/tidb/pull/16170)関数がMySQLと互換性がないという問題を修正し`ALLOW_INVALID_DATES` 。
    -   インデックス列に自動インクリメントの主キー[＃16008](https://github.com/pingcap/tidb/pull/16008)が含まれている場合に、 `DROP INDEX`ステートメントが実行されない問題を修正します。
    -   ステートメントの概要[＃15231](https://github.com/pingcap/tidb/pull/15231)の`TABLE_NAMES`列の値が正しくない問題を修正します。
    -   プランキャッシュが有効になっている場合、一部の式の結果が正しくない問題を修正します[＃16184](https://github.com/pingcap/tidb/pull/16184)
    -   `not`関数の結果が正しくない[＃15916](https://github.com/pingcap/tidb/pull/15916)を修正し`istrue` `isfalse`
    -   冗長インデックスを持つテーブルでの`MergeJoin`操作によって引き起こされるパニックを修正します[＃15919](https://github.com/pingcap/tidb/pull/15919)
    -   述部が外部テーブル[＃16492](https://github.com/pingcap/tidb/pull/16492)のみを参照している場合に、リンクを誤って単純化することによって引き起こされる問題を修正します。
    -   `CURRENT_ROLE`関数が`SET ROLE`ステートメント[＃15569](https://github.com/pingcap/tidb/pull/15569)によって引き起こされたエラーを報告する問題を修正します。
    -   このステートメントが[＃16633](https://github.com/pingcap/tidb/pull/16633)に遭遇したときに、 `LOAD DATA`ステートメントの結果がMySQLと互換性がないという問題を修正し`\` 。
    -   データベースの可視性がMySQL1と互換性がないという問題を修正し[＃14939](https://github.com/pingcap/tidb/pull/14939)
    -   `SET DEFAULT ROLE ALL`ステートメント[＃15585](https://github.com/pingcap/tidb/pull/15585)の誤った特権チェックの問題を修正します
    -   プランキャッシュ[＃15818](https://github.com/pingcap/tidb/pull/15818)によって引き起こされるパーティションプルーニングの失敗の問題を修正します
    -   トランザクションが関連するテーブル[＃15707](https://github.com/pingcap/tidb/pull/15707)をロックしないため、テーブルで同時DDL操作が実行され、ブロッキングが存在する場合に、トランザクションのコミット中に`schema change`が報告される問題を修正します。
    -   [＃15356](https://github.com/pingcap/tidb/pull/15356)の誤った動作を修正し`IF(not_int, *, *)`
    -   [＃15359](https://github.com/pingcap/tidb/pull/15359)の誤った動作を修正し`CASE WHEN (not_int)`
    -   現在のスキーマにない`view`を使用すると`Unknown column`エラーメッセージが返される問題を修正します[＃15866](https://github.com/pingcap/tidb/pull/15866)
    -   時間文字列の解析結果がMySQL1と互換性がないという問題を修正し[＃16242](https://github.com/pingcap/tidb/pull/16242)
    -   右側の子ノード[＃16528](https://github.com/pingcap/tidb/pull/16528)に`null`列が存在する場合に、照合順序演算子が`left join`でパニックになる可能性を修正します。
    -   TiKVが`StaleCommand`のエラーメッセージを返し続けるとSQLの実行がブロックされてもエラーメッセージが返されない問題を修正します[＃16528](https://github.com/pingcap/tidb/pull/16528)
    -   監査プラグインが有効になっているときにポートプローブによって引き起こされる可能性のあるパニックを修正します[＃15967](https://github.com/pingcap/tidb/pull/15967)
    -   `fast analyze`がインデックスのみで機能する場合に発生するパニックを修正します[＃15967](https://github.com/pingcap/tidb/pull/15967)
    -   場合によっては`SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST`ステートメントの実行で発生する可能性のあるパニックを修正します[＃16309](https://github.com/pingcap/tidb/pull/16309)
    -   メモリを割り当てる前にパーティションの数を確認せずにハッシュパーティションテーブルを作成するときに、多数のパーティション（たとえば、 `9999999999999` ）を指定することによって発生するTiDBOOMの問題を修正します[＃16218](https://github.com/pingcap/tidb/pull/16218)
    -   [＃16726](https://github.com/pingcap/tidb/pull/16726)のパーティションテーブルの誤った情報の問題を修正し`information_schema.tidb_hot_table`
    -   パーティション選択アルゴリズムがハッシュパーティションテーブル[＃16070](https://github.com/pingcap/tidb/pull/16070)で有効にならない問題を修正します
    -   MVCCシリーズのHTTPAPIがパーティションテーブルをサポートしない問題を修正します[＃16191](https://github.com/pingcap/tidb/pull/16191)
    -   `UNION`ステートメントのエラー処理を`SELECT`ステートメントのエラー処理と一致させてください[＃16137](https://github.com/pingcap/tidb/pull/16137)
    -   `VALUES`関数のパラメータータイプが[＃15486](https://github.com/pingcap/tidb/pull/15486)の場合の誤った動作の問題を修正し`bit(n)`
    -   `view`列の名前が長すぎると、TiDBの処理ロジックがMySQLと矛盾する問題を修正します。この場合、システムは自動的に短い列名を生成します。 [＃14873](https://github.com/pingcap/tidb/pull/14873)
    -   `(not not col)`が[＃16094](https://github.com/pingcap/tidb/pull/16094)として誤って最適化される問題を修正し`col`
    -   `IndexLookupJoin`のプランによって構築された内部テーブルの誤った`range`の問題を修正します[＃15753](https://github.com/pingcap/tidb/pull/15753)
    -   `only_full_group_by`が角かっこ[＃16012](https://github.com/pingcap/tidb/pull/16012)で式を正しくチェックできない問題を修正します
    -   `select view_name.col_name from view_name`ステートメントの実行時にエラーが返される問題を修正します[＃15572](https://github.com/pingcap/tidb/pull/15572)

-   TiKV

    -   場合によっては、分離リカバリ後にノードを正しく削除できない問題を修正します[＃7703](https://github.com/tikv/tikv/pull/7703)
    -   リージョンマージ操作によって引き起こされるネットワーク分離中のデータ損失の問題を修正します[＃7679](https://github.com/tikv/tikv/pull/7679)
    -   場合によっては学習者を正しく削除できない問題を修正します[＃7598](https://github.com/tikv/tikv/pull/7598)
    -   生のキーと値のペアのスキャン結果が順序どおりになっていない可能性がある問題を修正します[＃7597](https://github.com/tikv/tikv/pull/7597)
    -   Raftメッセージのバッチが大きすぎる場合の再接続の問題を修正します[＃7542](https://github.com/tikv/tikv/pull/7542)
    -   空のリクエストによって引き起こされるgRPCスレッドのデッドロックの問題を修正します[＃7538](https://github.com/tikv/tikv/pull/7538)
    -   マージプロセス中に学習者を再起動する処理ロジックが正しくないという問題を修正します[＃7457](https://github.com/tikv/tikv/pull/7457)
    -   ロックのクリーンアップで繰り返し要求すると、トランザクションの原子性が破壊される可能性があるという問題を修正します[＃7388](https://github.com/tikv/tikv/pull/7388)
