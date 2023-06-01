---
title: TiDB 3.0.14 Release Notes
---

# TiDB 3.0.14 リリースノート {#tidb-3-0-14-release-notes}

発売日：2020年5月9日

TiDB バージョン: 3.0.14

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `performance_schema`と`metrics_schema`のユーザー権限を読み取り/書き込みから読み取り専用に調整します[<a href="https://github.com/pingcap/tidb/pull/15417">#15417</a>](https://github.com/pingcap/tidb/pull/15417)

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `join`条件に`handle`属性[<a href="https://github.com/pingcap/tidb/pull/15734">#15734</a>](https://github.com/pingcap/tidb/pull/15734)の列に複数の同等の条件がある場合、 `index join`のクエリ結果が正しくない問題を修正します。
    -   `handle`属性[<a href="https://github.com/pingcap/tidb/pull/16079">#16079</a>](https://github.com/pingcap/tidb/pull/16079)の列に対して`fast analyze`操作を実行すると発生するpanicを修正しました。
    -   DDL ステートメントが`prepare`の方法で実行されると、DDL ジョブ構造の`query`フィールドが正しくなくなる問題を修正します。この問題により、 Binlog がデータ レプリケーションに使用されている場合に、アップストリームとダウンストリームの間でデータの不整合が発生する可能性があります。 [<a href="https://github.com/pingcap/tidb/pull/15443">#15443</a>](https://github.com/pingcap/tidb/pull/15443)

-   TiKV

    -   ロックのクリーンアップでリクエストを繰り返すとトランザクションのアトミック性が破壊される可能性がある問題を修正します[<a href="https://github.com/tikv/tikv/pull/7388">#7388</a>](https://github.com/tikv/tikv/pull/7388)

## 新機能 {#new-features}

-   TiDB

    -   `admin show ddl jobs`ステートメント[<a href="https://github.com/pingcap/tidb/pull/16428">#16428</a>](https://github.com/pingcap/tidb/pull/16428)のクエリ結果にスキーマ名列とテーブル名列を追加します。
    -   切り捨てられたテーブルのリカバリをサポートするために`RECOVER TABLE`構文を拡張します[<a href="https://github.com/pingcap/tidb/pull/15458">#15458</a>](https://github.com/pingcap/tidb/pull/15458)
    -   `SHOW GRANTS`ステートメント[<a href="https://github.com/pingcap/tidb/pull/16168">#16168</a>](https://github.com/pingcap/tidb/pull/16168)の権限チェックをサポートします。
    -   `LOAD DATA`ステートメント[<a href="https://github.com/pingcap/tidb/pull/16736">#16736</a>](https://github.com/pingcap/tidb/pull/16736)の権限チェックをサポートします。
    -   時刻と日付に関連する関数がパーティション キーとして使用される場合のパーティション プルーニングのパフォーマンスが向上します[<a href="https://github.com/pingcap/tidb/pull/15618">#15618</a>](https://github.com/pingcap/tidb/pull/15618)
    -   `dispatch error`のログレベルを`WARN`から`ERROR`に調整します[<a href="https://github.com/pingcap/tidb/pull/16232">#16232</a>](https://github.com/pingcap/tidb/pull/16232)
    -   クライアントに TLS [<a href="https://github.com/pingcap/tidb/pull/15415">#15415</a>](https://github.com/pingcap/tidb/pull/15415)の使用を強制する`require-secure-transport`起動オプションをサポートします。
    -   TLS が構成されている場合、TiDB コンポーネント間の HTTP 通信をサポートします[<a href="https://github.com/pingcap/tidb/pull/15419">#15419</a>](https://github.com/pingcap/tidb/pull/15419)
    -   現在のトランザクションの`start_ts`情報を`information_schema.processlist`テーブルに追加します[<a href="https://github.com/pingcap/tidb/pull/16160">#16160</a>](https://github.com/pingcap/tidb/pull/16160)
    -   クラスター間の通信に使用される TLS 証明書情報の自動再読み込みをサポート[<a href="https://github.com/pingcap/tidb/pull/15162">#15162</a>](https://github.com/pingcap/tidb/pull/15162)
    -   パーティション プルーニング[<a href="https://github.com/pingcap/tidb/pull/15628">#15628</a>](https://github.com/pingcap/tidb/pull/15628)を再構築することで、パーティション テーブルの読み取りパフォーマンスを向上させます。
    -   `range`パーティション テーブル[<a href="https://github.com/pingcap/tidb/pull/16521">#16521</a>](https://github.com/pingcap/tidb/pull/16521)のパーティション式として`floor(unix_timestamp(a))`が使用される場合、パーティション プルーニング機能をサポートします。
    -   `view`を含み、 `view` [<a href="https://github.com/pingcap/tidb/pull/16787">#16787</a>](https://github.com/pingcap/tidb/pull/16787)を更新しない`update`ステートメントの実行を許可します。
    -   ネストされた`view` s [<a href="https://github.com/pingcap/tidb/pull/15424">#15424</a>](https://github.com/pingcap/tidb/pull/15424)の作成を禁止する
    -   切り捨て禁止`view` [<a href="https://github.com/pingcap/tidb/pull/16420">#16420</a>](https://github.com/pingcap/tidb/pull/16420)
    -   この列が`public`状態にない場合、 `update`ステートメントを使用して列の値を明示的に更新することを禁止します[<a href="https://github.com/pingcap/tidb/pull/15576">#15576</a>](https://github.com/pingcap/tidb/pull/15576)
    -   `status`ポート占有時の TiDB 起動禁止[<a href="https://github.com/pingcap/tidb/pull/15466">#15466</a>](https://github.com/pingcap/tidb/pull/15466)
    -   `current_role`関数の文字セットを`binary`から`utf8mb4`に変更します[<a href="https://github.com/pingcap/tidb/pull/16083">#16083</a>](https://github.com/pingcap/tidb/pull/16083)
    -   新しいリージョンのデータを読み取るときに割り込み信号をチェックすることで`max-execution-time`の使いやすさを向上[<a href="https://github.com/pingcap/tidb/pull/15615">#15615</a>](https://github.com/pingcap/tidb/pull/15615)
    -   `auto_id` [<a href="https://github.com/pingcap/tidb/pull/16287">#16287</a>](https://github.com/pingcap/tidb/pull/16287)のキャッシュ ステップを明示的に設定するための`ALTER TABLE ... AUTO_ID_CACHE`構文を追加します。

-   TiKV

    -   楽観的トランザクション[<a href="https://github.com/tikv/tikv/pull/7605">#7605</a>](https://github.com/tikv/tikv/pull/7605)に多くの競合と`BatchRollback`条件が存在する場合のパフォーマンスを向上させます。
    -   悲観的トランザクション[<a href="https://github.com/tikv/tikv/pull/7584">#7584</a>](https://github.com/tikv/tikv/pull/7584)に多くの競合が存在する場合、悲観的ロック`waiter`頻繁に起動されるため、パフォーマンスが低下する問題を修正します。

-   ツール

    -   TiDB Lightning

        -   tidb-lightning-ctl [<a href="https://github.com/pingcap/tidb-lightning/pull/287">#287</a>](https://github.com/pingcap/tidb-lightning/pull/287)の`fetch-mode`サブコマンドを使用した TiKV クラスター モードの印刷のサポート

## バグの修正 {#bug-fixes}

-   TiDB

    -   SQLモードが`ALLOW_INVALID_DATES` [<a href="https://github.com/pingcap/tidb/pull/16170">#16170</a>](https://github.com/pingcap/tidb/pull/16170)の場合、 `WEEKEND`関数がMySQLと互換性がない問題を修正
    -   インデックス列に自動インクリメント主キー[<a href="https://github.com/pingcap/tidb/pull/16008">#16008</a>](https://github.com/pingcap/tidb/pull/16008)が含まれている場合、 `DROP INDEX`ステートメントの実行が失敗する問題を修正します。
    -   ステートメントの概要[<a href="https://github.com/pingcap/tidb/pull/15231">#15231</a>](https://github.com/pingcap/tidb/pull/15231)の`TABLE_NAMES`列の値が正しくない問題を修正
    -   プラン キャッシュが有効になっている場合、一部の式の結果が正しくない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/16184">#16184</a>](https://github.com/pingcap/tidb/pull/16184)
    -   `not` / `istrue` / `isfalse`関数の結果が正しくない問題を修正[<a href="https://github.com/pingcap/tidb/pull/15916">#15916</a>](https://github.com/pingcap/tidb/pull/15916)
    -   `MergeJoin`冗長インデックスを持つテーブルに対する操作によって引き起こされるpanicを修正[<a href="https://github.com/pingcap/tidb/pull/15919">#15919</a>](https://github.com/pingcap/tidb/pull/15919)
    -   述語が外部テーブル[<a href="https://github.com/pingcap/tidb/pull/16492">#16492</a>](https://github.com/pingcap/tidb/pull/16492)のみを参照する場合に、リンクが誤って単純化されることによって発生する問題を修正します。
    -   `CURRENT_ROLE`関数が`SET ROLE`ステートメントに起因するエラーを報告する問題を修正します[<a href="https://github.com/pingcap/tidb/pull/15569">#15569</a>](https://github.com/pingcap/tidb/pull/15569)
    -   このステートメントが`\` [<a href="https://github.com/pingcap/tidb/pull/16633">#16633</a>](https://github.com/pingcap/tidb/pull/16633)に遭遇した場合、 `LOAD DATA`ステートメントの結果が MySQL と互換性がないという問題を修正します。
    -   データベースの可視性が MySQL [<a href="https://github.com/pingcap/tidb/pull/14939">#14939</a>](https://github.com/pingcap/tidb/pull/14939)と互換性がない問題を修正
    -   `SET DEFAULT ROLE ALL`ステートメント[<a href="https://github.com/pingcap/tidb/pull/15585">#15585</a>](https://github.com/pingcap/tidb/pull/15585)の不正な権限チェックの問題を修正します。
    -   プラン キャッシュ[<a href="https://github.com/pingcap/tidb/pull/15818">#15818</a>](https://github.com/pingcap/tidb/pull/15818)が原因でパーティション プルーニングが失敗する問題を修正します。
    -   テーブルに対して同時 DDL 操作が実行され、ブロックが存在する場合、トランザクションは関連テーブル[<a href="https://github.com/pingcap/tidb/pull/15707">#15707</a>](https://github.com/pingcap/tidb/pull/15707)をロックしないため、トランザクションのコミット中に`schema change`が報告される問題を修正します。
    -   `IF(not_int, *, *)` [<a href="https://github.com/pingcap/tidb/pull/15356">#15356</a>](https://github.com/pingcap/tidb/pull/15356)の誤った動作を修正
    -   `CASE WHEN (not_int)` [<a href="https://github.com/pingcap/tidb/pull/15359">#15359</a>](https://github.com/pingcap/tidb/pull/15359)の誤った動作を修正
    -   現在のスキーマにない`view`を使用すると`Unknown column`エラー メッセージが返される問題を修正します[<a href="https://github.com/pingcap/tidb/pull/15866">#15866</a>](https://github.com/pingcap/tidb/pull/15866)
    -   時刻文字列の解析結果がMySQL [<a href="https://github.com/pingcap/tidb/pull/16242">#16242</a>](https://github.com/pingcap/tidb/pull/16242)と互換性がない問題を修正
    -   右側の子ノード[<a href="https://github.com/pingcap/tidb/pull/16528">#16528</a>](https://github.com/pingcap/tidb/pull/16528)に`null`列が存在する場合に`left join`で発生する可能性のある照合順序子のpanicを修正しました。
    -   TiKV が`StaleCommand`エラー メッセージ[<a href="https://github.com/pingcap/tidb/pull/16528">#16528</a>](https://github.com/pingcap/tidb/pull/16528)を返し続けると、SQL の実行がブロックされてもエラー メッセージが返されない問題を修正します。
    -   監査プラグインが有効になっているときにポートプローブによって発生する可能性のあるpanicを修正します[<a href="https://github.com/pingcap/tidb/pull/15967">#15967</a>](https://github.com/pingcap/tidb/pull/15967)
    -   `fast analyze`インデックス[<a href="https://github.com/pingcap/tidb/pull/15967">#15967</a>](https://github.com/pingcap/tidb/pull/15967)に対してのみ機能するときに発生するpanicを修正しました。
    -   場合によっては`SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST`ステートメント実行のpanicがある問題を修正[<a href="https://github.com/pingcap/tidb/pull/16309">#16309</a>](https://github.com/pingcap/tidb/pull/16309)
    -   メモリを割り当てる前にパーティションの数を確認せずにハッシュ パーティション テーブルを作成するときに、多数のパーティション (たとえば、 `9999999999999` ) を指定することによって発生する TiDB OOM の問題を修正します[<a href="https://github.com/pingcap/tidb/pull/16218">#16218</a>](https://github.com/pingcap/tidb/pull/16218)
    -   `information_schema.tidb_hot_table` [<a href="https://github.com/pingcap/tidb/pull/16726">#16726</a>](https://github.com/pingcap/tidb/pull/16726)のパーティションテーブルの情報が正しくない問題を修正
    -   パーティション選択アルゴリズムがハッシュパーティションテーブル[<a href="https://github.com/pingcap/tidb/pull/16070">#16070</a>](https://github.com/pingcap/tidb/pull/16070)に適用されない問題を修正します。
    -   MVCCシリーズのHTTP APIがパーティションテーブルをサポートしていない問題を修正[<a href="https://github.com/pingcap/tidb/pull/16191">#16191</a>](https://github.com/pingcap/tidb/pull/16191)
    -   `UNION`ステートメントのエラー処理と`SELECT`ステートメントのエラー処理の一貫性を保つ[<a href="https://github.com/pingcap/tidb/pull/16137">#16137</a>](https://github.com/pingcap/tidb/pull/16137)
    -   `VALUES`関数のパラメータの型が`bit(n)` [<a href="https://github.com/pingcap/tidb/pull/15486">#15486</a>](https://github.com/pingcap/tidb/pull/15486)の場合に正しく動作しない問題を修正
    -   `view`カラム名が長すぎる場合にTiDBの処理ロジックがMySQLと矛盾する問題を修正。この場合、システムは短い列名を自動的に生成します。 [<a href="https://github.com/pingcap/tidb/pull/14873">#14873</a>](https://github.com/pingcap/tidb/pull/14873)
    -   `(not not col)`が`col` [<a href="https://github.com/pingcap/tidb/pull/16094">#16094</a>](https://github.com/pingcap/tidb/pull/16094)として誤って最適化される問題を修正
    -   `IndexLookupJoin`プラン[<a href="https://github.com/pingcap/tidb/pull/15753">#15753</a>](https://github.com/pingcap/tidb/pull/15753)によって構築された内部テーブルの`range`が正しくない問題を修正
    -   `only_full_group_by`で括弧付きの式が正しくチェックされない問題を修正[<a href="https://github.com/pingcap/tidb/pull/16012">#16012</a>](https://github.com/pingcap/tidb/pull/16012)
    -   `select view_name.col_name from view_name`ステートメント実行時にエラーが返される問題を修正[<a href="https://github.com/pingcap/tidb/pull/15572">#15572</a>](https://github.com/pingcap/tidb/pull/15572)

-   TiKV

    -   隔離回復後にノードが正しく削除できない場合がある問題を修正[<a href="https://github.com/tikv/tikv/pull/7703">#7703</a>](https://github.com/tikv/tikv/pull/7703)
    -   リージョンマージ操作によって引き起こされるネットワーク分離中のデータ損失の問題を修正します[<a href="https://github.com/tikv/tikv/pull/7679">#7679</a>](https://github.com/tikv/tikv/pull/7679)
    -   学習者が正しく削除できない場合がある問題を修正[<a href="https://github.com/tikv/tikv/pull/7598">#7598</a>](https://github.com/tikv/tikv/pull/7598)
    -   生のキーと値のペアのスキャン結果が順序どおりにならない場合がある問題を修正します[<a href="https://github.com/tikv/tikv/pull/7597">#7597</a>](https://github.com/tikv/tikv/pull/7597)
    -   Raftメッセージのバッチが大きすぎる場合の再接続の問題を修正[<a href="https://github.com/tikv/tikv/pull/7542">#7542</a>](https://github.com/tikv/tikv/pull/7542)
    -   空のリクエストによって引き起こされる gRPC スレッドのデッドロックの問題を修正します[<a href="https://github.com/tikv/tikv/pull/7538">#7538</a>](https://github.com/tikv/tikv/pull/7538)
    -   マージ処理中に学習器を再起動する処理ロジックが正しくない問題を修正[<a href="https://github.com/tikv/tikv/pull/7457">#7457</a>](https://github.com/tikv/tikv/pull/7457)
    -   ロックのクリーンアップでリクエストを繰り返すとトランザクションのアトミック性が破壊される可能性がある問題を修正します[<a href="https://github.com/tikv/tikv/pull/7388">#7388</a>](https://github.com/tikv/tikv/pull/7388)
