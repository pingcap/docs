---
title: TiDB 2.1.16 Release Notes
summary: TiDB 2.1.16 は 2019 年 8 月 15 日にリリースされました。SQL オプティマイザー、SQL 実行エンジン、サーバー、DDL、TiKV、TiDB Binlog、 TiDB Lightning 、TiDB Ansible に対するさまざまな修正と改善が含まれています。注目すべき変更点としては、SHOW ステートメント内のサブクエリのサポート、DATE_ADD 関数の問題の修正、TiDB BinlogのDrainerへの構成項目の追加などがあります。
---

# TiDB 2.1.16 リリースノート {#tidb-2-1-16-release-notes}

発売日: 2019年8月15日

TiDB バージョン: 2.1.16

TiDB Ansible バージョン: 2.1.16

## ティビ {#tidb}

-   SQL オプティマイザー
    -   時間列[＃11526](https://github.com/pingcap/tidb/pull/11526)の等号条件で行数が不正確に推定される問題を修正しました。
    -   `TIDB_INLJ`ヒントが有効にならない、または指定されたテーブル[＃11361](https://github.com/pingcap/tidb/pull/11361)に有効にならない問題を修正
    -   クエリの`NOT EXISTS`の実装をOUTER JOINからANTI JOINに変更して、より最適化された実行プラン[＃11291](https://github.com/pingcap/tidb/pull/11291)を見つけます。
    -   `SHOW`文内でサブクエリをサポートし、 `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` [＃11461](https://github.com/pingcap/tidb/pull/11461)のような構文が可能
    -   定数畳み込み最適化[＃11441](https://github.com/pingcap/tidb/pull/11441)によりクエリ`SELECT … CASE WHEN … ELSE NULL ...`が誤った結果を返す問題を修正
-   SQL実行エンジン
    -   `INTERVAL`が負の[＃11616](https://github.com/pingcap/tidb/pull/11616)場合に`DATE_ADD`関数が誤った結果を返す問題を修正しました
    -   `DATE_ADD`関数が`FLOAT` 、 `DOUBLE` 、または`DECIMAL`型の引数を受け入れるときに型変換を誤って実行するため、誤った結果が返される可能性がある問題を修正しました[＃11628](https://github.com/pingcap/tidb/pull/11628)
    -   CAST(JSON AS SIGNED)がオーバーフローしたときにエラーメッセージが不正確になる問題を修正[＃11562](https://github.com/pingcap/tidb/pull/11562)
    -   Executor [＃11598](https://github.com/pingcap/tidb/pull/11598)を閉じる処理中に 1 つの子ノードが閉じられずエラーが返された場合に、他の子ノードが閉じられない問題を修正しました。
    -   タイムアウト[＃11487](https://github.com/pingcap/tidb/pull/11487)までにリージョン分散のスケジュールが完了していない場合に、エラーではなく、正常に分割されたリージョンの数と完了したパーセンテージを返す`SPLIT TABLE`ステートメントをサポートします。
    -   MySQL [＃11505](https://github.com/pingcap/tidb/pull/11505)と互換性を持たせるために、 `REGEXP BINARY`関数で大文字と小文字を区別する
    -   `DATE_ADD` `DATE_SUB`結果の`YEAR`の値が 0 より小さいか[＃11477](https://github.com/pingcap/tidb/pull/11477)より大きい場合にオーバーフローするため、 `NULL`が正しく返されない問題を修正しました。
    -   実行が成功したかどうかを示すフィールドを`Succ`クエリテーブルに追加します[＃11412](https://github.com/pingcap/tidb/pull/11421)
    -   SQL 文に現在の時刻 ( `CURRENT_TIMESTAMP`や`NOW`など) の計算が含まれる場合に、現在のタイムスタンプを複数回取得することで発生する MySQL の非互換性の問題を修正しました[＃11392](https://github.com/pingcap/tidb/pull/11392)
    -   AUTO_INCREMENT列がFLOATまたはDOUBLE型[＃11389](https://github.com/pingcap/tidb/pull/11389)を処理できない問題を修正
    -   `CONVERT_TZ`関数が無効な引数[＃11357](https://github.com/pingcap/tidb/pull/11357)受け入れたときに`NULL`が正しく返されない問題を修正しました
    -   `PARTITION BY LIST`文でエラーが報告される問題を修正しました。(現在は構文のみがサポートされています。TiDB が文を実行すると、通常のテーブルが作成され、プロンプト メッセージが提供されます) [＃11236](https://github.com/pingcap/tidb/pull/11236)
    -   `Mod(%)` 、 `Multiple(*)` 、 `Minus(-)`演算で、小数点以下の桁数が多い場合（ `select 0.000 % 0.11234500000000000000`など）に、MySQL の結果と矛盾する`0`結果が返される問題を修正しました[＃11353](https://github.com/pingcap/tidb/pull/11353)
-   サーバ
    -   `OnInit`が[＃11426](https://github.com/pingcap/tidb/pull/11426)にコールバックされたときにプラグインが`NULL`ドメインを取得する問題を修正
    -   スキーマが削除された後でも、スキーマ内のテーブル情報が HTTP インターフェース経由で取得できる問題を修正しました[＃11586](https://github.com/pingcap/tidb/pull/11586)
-   DDL
    -   この操作によって自動インクリメント列に誤った結果が生じるのを避けるため、自動インクリメント列のインデックスの削除を禁止します[＃11402](https://github.com/pingcap/tidb/pull/11402)
    -   異なる文字セットと照合順序でテーブルを作成および変更するときに列の文字セットが正しくない問題を修正[＃11423](https://github.com/pingcap/tidb/pull/11423)
    -   `alter table ... set default...`とこの列を変更する別の DDL 文が並列で実行されると列スキーマが間違ってしまう可能性がある問題を修正[＃11374](https://github.com/pingcap/tidb/pull/11374)
    -   生成されたカラムA が生成されたカラムB に依存し、A がインデックス[＃11538](https://github.com/pingcap/tidb/pull/11538)の作成に使用される場合に、データのバックフィルが失敗する問題を修正しました。
    -   `ADMIN CHECK TABLE`操作を高速化[＃11538](https://github.com/pingcap/tidb/pull/11676)

## ティクヴ {#tikv}

-   クライアントが閉じられている TiKVリージョンにアクセスしたときにエラー メッセージを返す機能をサポート[＃4820](https://github.com/tikv/tikv/pull/4820)
-   リバース`raw_scan`および`raw_batch_scan`インターフェース[＃5148](https://github.com/tikv/tikv/pull/5148)をサポート

## ツール {#tools}

-   TiDBBinlog
    -   トランザクション[＃697](https://github.com/pingcap/tidb-binlog/pull/697)内の一部のステートメントの実行をスキップするために、 Drainerに`ignore-txn-commit-ts`構成項目を追加します。
    -   起動時に構成項目チェックを追加します。これにより、PumpとDrainerの実行が停止され、無効な構成項目に該当する場合にエラーメッセージが返されます[＃708](https://github.com/pingcap/tidb-binlog/pull/708)
    -   DrainerのノードID [＃706](https://github.com/pingcap/tidb-binlog/pull/706)を指定するためにDrainerに`node-id`設定を追加します。
-   TiDB Lightning
    -   2つのチェックサムが同時に実行されているときに`tikv_gc_life_time`元の値に戻らない問題を修正しました[＃224](https://github.com/pingcap/tidb-lightning/pull/224)

## TiDB アンシブル {#tidb-ansible}

-   Spark [＃842](https://github.com/pingcap/tidb-ansible/pull/842)に`log4j`設定ファイルを追加する
-   tispark jarパッケージをv2.1.2 [＃863](https://github.com/pingcap/tidb-ansible/pull/863)に更新する
-   TiDB Binlog がKafka または ZooKeeper [＃845](https://github.com/pingcap/tidb-ansible/pull/845)を使用する場合に Prometheus 構成ファイルが間違った形式で生成される問題を修正しました。
-   `rolling_update.yml`操作[＃888](https://github.com/pingcap/tidb-ansible/pull/888)実行する際にPDがLeaderの切り替えに失敗するバグを修正
-   PDノードのローリング更新ロジックを最適化 - 最初にフォロワーをアップグレードし、次にLeaderをアップグレード - 安定性を向上[＃895](https://github.com/pingcap/tidb-ansible/pull/895)
