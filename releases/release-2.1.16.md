---
title: TiDB 2.1.16 Release Notes
---

# TiDB 2.1.16 リリースノート {#tidb-2-1-16-release-notes}

発売日：2019年8月15日

TiDB バージョン: 2.1.16

TiDB アンシブル バージョン: 2.1.16

## TiDB {#tidb}

-   SQL オプティマイザー
    -   時刻列[#11526](https://github.com/pingcap/tidb/pull/11526)の等号条件で行数が不正確に見積もられる問題を修正
    -   `TIDB_INLJ`ヒントが有効にならない、または指定したテーブルで有効になる問題を修正[#11361](https://github.com/pingcap/tidb/pull/11361)
    -   クエリの`NOT EXISTS`の実装を OUTER JOIN から ANTI JOIN に変更して、より最適化された実行プランを見つけます[#11291](https://github.com/pingcap/tidb/pull/11291)
    -   `SHOW`ステートメント内のサブクエリをサポートし、 `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` [#11461](https://github.com/pingcap/tidb/pull/11461)などの構文を許可します
    -   定数折り畳みの最適化が原因で`SELECT … CASE WHEN … ELSE NULL ...`クエリが誤った結果を取得する問題を修正します[#11441](https://github.com/pingcap/tidb/pull/11441)
-   SQL 実行エンジン
    -   `INTERVAL`が負の[#11616](https://github.com/pingcap/tidb/pull/11616)の場合に`DATE_ADD`関数が間違った結果になる問題を修正します。
    -   `DATE_ADD`関数が`FLOAT` 、 `DOUBLE` 、または`DECIMAL`型の引数を受け入れると型変換が正しく行われず、誤った結果が得られる可能性がある問題を修正します[#11628](https://github.com/pingcap/tidb/pull/11628)
    -   CAST(JSON AS SIGNED) オーバーフロー時のエラーメッセージが不正確になる問題を修正[#11562](https://github.com/pingcap/tidb/pull/11562)
    -   Executor [#11598](https://github.com/pingcap/tidb/pull/11598)を閉じる処理中に 1 つの子ノードの閉じに失敗し、エラーを返すと、他の子ノードが閉じられない問題を修正します。
    -   [#11487](https://github.com/pingcap/tidb/pull/11487)前にリージョン分散のスケジューリングが完了していない場合に、エラーではなく、正常に分割されたリージョンの数と完了したリージョンを返す`SPLIT TABLE`ステートメントをサポートします。
    -   MySQL [#11505](https://github.com/pingcap/tidb/pull/11505)と互換性があるように、 `REGEXP BINARY`の関数で大文字と小文字を区別する
    -   `DATE_ADD` / `DATE_SUB`の結果の`YEAR`の値が 0 より小さいか 65535 より大きいとオーバーフローするため、 `NULL`が正しく返されない問題を修正[#11477](https://github.com/pingcap/tidb/pull/11477)
    -   実行が成功したかどうかを示す`Succ`フィールドをスロー クエリ テーブルに追加します[#11412](https://github.com/pingcap/tidb/pull/11421)
    -   SQL ステートメントに現在時刻の計算が含まれる場合 ( `CURRENT_TIMESTAMP`または`NOW`など)、現在のタイムスタンプを複数回取得することによって発生する MySQL の非互換性の問題を修正します[#11392](https://github.com/pingcap/tidb/pull/11392)
    -   AUTO_INCREMENT 列が FLOAT または DOUBLE 型を処理しない問題を修正します[#11389](https://github.com/pingcap/tidb/pull/11389)
    -   `CONVERT_TZ`関数が無効な引数[#11357](https://github.com/pingcap/tidb/pull/11357)を受け入れると`NULL`が正しく返されない問題を修正
    -   `PARTITION BY LIST`ステートメントでエラーが報告される問題を修正します。 (現在、構文のみがサポートされています。TiDB がステートメントを実行すると、通常のテーブルが作成され、プロンプト メッセージが表示されます) [#11236](https://github.com/pingcap/tidb/pull/11236)
    -   `Mod(%)` 、 `Multiple(*)` 、および`Minus(-)`の操作で、10 進数の桁数が多い場合 ( `select 0.000 % 0.11234500000000000000`など) `0`結果が MySQL の結果と一致しない問題を修正[#11353](https://github.com/pingcap/tidb/pull/11353)
-   サーバ
    -   `OnInit`が[#11426](https://github.com/pingcap/tidb/pull/11426)にコールバックされると、プラグインが`NULL`ドメインを取得する問題を修正します。
    -   スキーマが削除された後も、スキーマ内のテーブル情報が HTTP インターフェースを介して取得できる問題を修正します[#11586](https://github.com/pingcap/tidb/pull/11586)
-   DDL
    -   この操作による自動インクリメント列の誤った結果を回避するために、自動インクリメント列のインデックスの削除を許可しない[#11402](https://github.com/pingcap/tidb/pull/11402)
    -   異なる文字セットと照合順序でテーブルを作成および変更すると、列の文字セットが正しくない問題を修正します[#11423](https://github.com/pingcap/tidb/pull/11423)
    -   `alter table ... set default...`と、この列を変更する別の DDL ステートメントが並行して実行されると、列のスキーマが間違っている可能性がある問題を修正します[#11374](https://github.com/pingcap/tidb/pull/11374)
    -   生成カラムA が生成カラムB に依存し、生成列 A を使用してインデックス[#11538](https://github.com/pingcap/tidb/pull/11538)を作成すると、データのバックフィルに失敗する問題を修正します。
    -   スピードアップ`ADMIN CHECK TABLE`オペレーション[#11538](https://github.com/pingcap/tidb/pull/11676)

## TiKV {#tikv}

-   クローズされている TiKVリージョンにクライアントがアクセスしたときにエラー メッセージを返すサポート[#4820](https://github.com/tikv/tikv/pull/4820)
-   リバース`raw_scan`および`raw_batch_scan`インターフェイスをサポート[#5148](https://github.com/tikv/tikv/pull/5148)

## ツール {#tools}

-   TiDBBinlog
    -   Drainerに`ignore-txn-commit-ts`構成項目を追加して、トランザクション[#697](https://github.com/pingcap/tidb-binlog/pull/697)の一部のステートメントの実行をスキップします。
    -   起動時に構成項目チェックを追加します。これにより、 PumpとDrainerの実行が停止し、無効な構成項目を満たすとエラー メッセージが返されます[#708](https://github.com/pingcap/tidb-binlog/pull/708)
    -   Drainerに`node-id`構成を追加して、Drainer のノード ID [#706](https://github.com/pingcap/tidb-binlog/pull/706)を指定します。
-   TiDB Lightning
    -   2 つのチェックサムが同時に実行されている場合、 `tikv_gc_life_time`が元の値に戻されない問題を修正します[#224](https://github.com/pingcap/tidb-lightning/pull/224)

## TiDB アンシブル {#tidb-ansible}

-   Spark [#842](https://github.com/pingcap/tidb-ansible/pull/842)に`log4j`構成ファイルを追加します。
-   tispark jar パッケージを v2.1.2 に更新する[#863](https://github.com/pingcap/tidb-ansible/pull/863)
-   TiDB Binlog がKafka または ZooKeeper [#845](https://github.com/pingcap/tidb-ansible/pull/845)を使用する場合、Prometheus 構成ファイルが間違った形式で生成される問題を修正します。
-   PDが`rolling_update.yml`操作[#888](https://github.com/pingcap/tidb-ansible/pull/888)実行時にLeaderの切り替えに失敗する不具合を修正
-   PD ノードのローリング アップデートのロジックを最適化します - 最初にフォロワーをアップグレードし、次にLeaderをアップグレードします - 安定性を向上させます[#895](https://github.com/pingcap/tidb-ansible/pull/895)
