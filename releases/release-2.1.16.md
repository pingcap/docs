---
title: TiDB 2.1.16 Release Notes
---

# TiDB 2.1.16 リリースノート {#tidb-2-1-16-release-notes}

発売日：2019年8月15日

TiDB バージョン: 2.1.16

TiDB Ansible バージョン: 2.1.16

## TiDB {#tidb}

-   SQLオプティマイザー
    -   時間列[#11526](https://github.com/pingcap/tidb/pull/11526)の等しい条件の行数が不正確に推定される問題を修正
    -   `TIDB_INLJ`ヒントが有効にならない、または指定したテーブル[#11361](https://github.com/pingcap/tidb/pull/11361)に有効になる問題を修正
    -   より最適化された実行プランを見つけるために、クエリ内の`NOT EXISTS`の実装を OUTER JOIN から ANTI JOIN に変更します[#11291](https://github.com/pingcap/tidb/pull/11291)
    -   `SHOW`ステートメント内のサブクエリをサポートし、 `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` [#11461](https://github.com/pingcap/tidb/pull/11461)などの構文を許可します。
    -   定数フォールディングの最適化[#11441](https://github.com/pingcap/tidb/pull/11441)によりクエリ`SELECT … CASE WHEN … ELSE NULL ...`が不正な結果を取得する問題を修正します。
-   SQL実行エンジン
    -   `INTERVAL`がマイナス[#11616](https://github.com/pingcap/tidb/pull/11616)の場合、 `DATE_ADD`関数が間違った結果を取得する問題を修正
    -   `DATE_ADD`関数が`FLOAT` 、 `DOUBLE` 、または`DECIMAL`型の引数を受け取るときに誤って型変換を実行するため、誤った結果が得られる可能性がある問題を修正します。 [#11628](https://github.com/pingcap/tidb/pull/11628)
    -   CAST(JSON AS SIGNED) がオーバーフローした場合にエラー メッセージが不正確になる問題を修正[#11562](https://github.com/pingcap/tidb/pull/11562)
    -   Executor [#11598](https://github.com/pingcap/tidb/pull/11598)を閉じる処理中に 1 つの子ノードが閉じられずにエラーが返された場合、他の子ノードが閉じられない問題を修正
    -   タイムアウト[#11487](https://github.com/pingcap/tidb/pull/11487)前にリージョンスキャッターのスケジューリングが完了していない場合に、エラーではなく、正常に分割されたリージョンの数と完了したパーセンテージを返すステートメント`SPLIT TABLE`をサポートします。
    -   MySQL [#11505](https://github.com/pingcap/tidb/pull/11505)と互換性を持たせるために、 `REGEXP BINARY`の関数の大文字と小文字を区別するようにします。
    -   `DATE_ADD` / `DATE_SUB`の結果の`YEAR`の値が 0 より小さい場合、または 65535 [#11477](https://github.com/pingcap/tidb/pull/11477)より大きい場合にオーバーフローしてしまい、 `NULL`正しく返されない問題を修正
    -   低速クエリ テーブルに、実行が成功したかどうかを示す`Succ`フィールドを追加します[#11412](https://github.com/pingcap/tidb/pull/11421)
    -   SQL ステートメントに現在時刻 ( `CURRENT_TIMESTAMP`や`NOW`など) の計算が含まれる場合に、現在のタイムスタンプを複数回フェッチすることによって引き起こされる MySQL の非互換性の問題を修正します[#11392](https://github.com/pingcap/tidb/pull/11392)
    -   AUTO_INCREMENT カラムが FLOAT または DOUBLE タイプ[#11389](https://github.com/pingcap/tidb/pull/11389)を処理しない問題を修正します。
    -   `CONVERT_TZ`関数が無効な引数[#11357](https://github.com/pingcap/tidb/pull/11357)を受け入れた場合、 `NULL`が正しく返されない問題を修正
    -   `PARTITION BY LIST`ステートメントによってエラーが報告される問題を修正します。 (現在、構文のみがサポートされています。TiDB がステートメントを実行すると、通常のテーブルが作成され、プロンプト メッセージが表示されます) [#11236](https://github.com/pingcap/tidb/pull/11236)
    -   10 進数の桁数 ( `select 0.000 % 0.11234500000000000000`など) が多い場合、 `Mod(%)` 、 `Multiple(*)` 、および`Minus(-)`操作で MySQL の結果と矛盾する`0`結果が返される問題を修正します[#11353](https://github.com/pingcap/tidb/pull/11353)
-   サーバ
    -   `OnInit`がコールバックされるとプラグインが`NULL`ドメインを取得する問題を修正[#11426](https://github.com/pingcap/tidb/pull/11426)
    -   スキーマが削除された後も、HTTP インターフェイスを介してスキーマ内のテーブル情報を取得できる問題を修正します[#11586](https://github.com/pingcap/tidb/pull/11586)
-   DDL
    -   この操作によって引き起こされる自動インクリメント列の誤った結果を避けるために、自動インクリメント列のインデックスの削除を禁止します[#11402](https://github.com/pingcap/tidb/pull/11402)
    -   異なる文字セットと照合順序でテーブルを作成および変更すると、列の文字セットが正しくなくなる問題を修正します[#11423](https://github.com/pingcap/tidb/pull/11423)
    -   `alter table ... set default...`とこの列を変更する別の DDL ステートメントが並行して実行されると、列スキーマが正しくなくなる可能性がある問題を修正します[#11374](https://github.com/pingcap/tidb/pull/11374)
    -   カラムA が生成カラムB に依存しており、A を使用してインデックス[#11538](https://github.com/pingcap/tidb/pull/11538)を作成すると、データのバックフィルが失敗する問題を修正します。
    -   `ADMIN CHECK TABLE`操作[#11538](https://github.com/pingcap/tidb/pull/11676)の高速化

## TiKV {#tikv}

-   クライアントが閉じられている TiKVリージョンにアクセスしたときにエラー メッセージを返すサポート[#4820](https://github.com/tikv/tikv/pull/4820)
-   リバース`raw_scan`および`raw_batch_scan`インターフェイスをサポート[#5148](https://github.com/tikv/tikv/pull/5148)

## ツール {#tools}

-   TiDBBinlog
    -   Drainerに`ignore-txn-commit-ts`構成項目を追加して、トランザクション[#697](https://github.com/pingcap/tidb-binlog/pull/697)内の一部のステートメントの実行をスキップします。
    -   起動時に構成項目チェックを追加します。これにより、PumpとDrainerの実行が停止され、無効な構成項目に一致するとエラー メッセージが返されます[#708](https://github.com/pingcap/tidb-binlog/pull/708)
    -   Drainerに`node-id`構成を追加して、Drainer のノード ID [#706](https://github.com/pingcap/tidb-binlog/pull/706)を指定します。
-   TiDB Lightning
    -   2つのチェックサムを同時に実行している場合、 `tikv_gc_life_time`元の値に戻すことができない問題を修正[#224](https://github.com/pingcap/tidb-lightning/pull/224)

## TiDB Ansible {#tidb-ansible}

-   Spark [#842](https://github.com/pingcap/tidb-ansible/pull/842)に`log4j`構成ファイルを追加します
-   tispark jar パッケージを v2.1.2 に更新します[#863](https://github.com/pingcap/tidb-ansible/pull/863)
-   TiDB Binlog がKafka または ZooKeeper を使用する場合に、Prometheus 構成ファイルが間違った形式で生成される問題を修正します[#845](https://github.com/pingcap/tidb-ansible/pull/845)
-   `rolling_update.yml`オペレーション[#888](https://github.com/pingcap/tidb-ansible/pull/888)実行時に PD がLeaderの切り替えに失敗するバグを修正
-   安定性を向上させるために、PD ノードのローリング更新ロジックを最適化します (最初にフォロワーをアップグレードし、次にLeaderをアップグレードします[#895](https://github.com/pingcap/tidb-ansible/pull/895)
