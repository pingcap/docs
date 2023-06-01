---
title: TiDB 2.1.16 Release Notes
---

# TiDB 2.1.16 リリースノート {#tidb-2-1-16-release-notes}

発売日：2019年8月15日

TiDB バージョン: 2.1.16

TiDB Ansible バージョン: 2.1.16

## TiDB {#tidb}

-   SQLオプティマイザー
    -   時間列[<a href="https://github.com/pingcap/tidb/pull/11526">#11526</a>](https://github.com/pingcap/tidb/pull/11526)の等しい条件の行数が不正確に推定される問題を修正
    -   `TIDB_INLJ`ヒントが有効にならない、または指定したテーブル[<a href="https://github.com/pingcap/tidb/pull/11361">#11361</a>](https://github.com/pingcap/tidb/pull/11361)に有効になる問題を修正
    -   より最適化された実行プランを見つけるために、クエリ内の`NOT EXISTS`の実装を OUTER JOIN から ANTI JOIN に変更します[<a href="https://github.com/pingcap/tidb/pull/11291">#11291</a>](https://github.com/pingcap/tidb/pull/11291)
    -   `SHOW`ステートメント内のサブクエリをサポートし、 `SHOW COLUMNS FROM tbl WHERE FIELDS IN (SELECT 'a')` [<a href="https://github.com/pingcap/tidb/pull/11461">#11461</a>](https://github.com/pingcap/tidb/pull/11461)などの構文を許可します。
    -   定数フォールディングの最適化[<a href="https://github.com/pingcap/tidb/pull/11441">#11441</a>](https://github.com/pingcap/tidb/pull/11441)によりクエリ`SELECT … CASE WHEN … ELSE NULL ...`が不正な結果を取得する問題を修正します。
-   SQL実行エンジン
    -   `INTERVAL`がマイナス[<a href="https://github.com/pingcap/tidb/pull/11616">#11616</a>](https://github.com/pingcap/tidb/pull/11616)の場合、 `DATE_ADD`関数が間違った結果を取得する問題を修正
    -   `DATE_ADD`関数が`FLOAT` 、 `DOUBLE` 、または`DECIMAL`型の引数を受け入れるときに誤って型変換を実行するため、誤った結果が得られる可能性がある問題を修正します。 [<a href="https://github.com/pingcap/tidb/pull/11628">#11628</a>](https://github.com/pingcap/tidb/pull/11628)
    -   CAST(JSON AS SIGNED) がオーバーフローした場合にエラー メッセージが不正確になる問題を修正[<a href="https://github.com/pingcap/tidb/pull/11562">#11562</a>](https://github.com/pingcap/tidb/pull/11562)
    -   Executor [<a href="https://github.com/pingcap/tidb/pull/11598">#11598</a>](https://github.com/pingcap/tidb/pull/11598)を閉じる処理中に 1 つの子ノードが閉じられずにエラーが返された場合、他の子ノードが閉じられない問題を修正
    -   タイムアウト[<a href="https://github.com/pingcap/tidb/pull/11487">#11487</a>](https://github.com/pingcap/tidb/pull/11487)前にリージョンスキャッターのスケジューリングが完了していない場合に、エラーではなく、正常に分割されたリージョンの数と完了したパーセンテージを返すステートメント`SPLIT TABLE`をサポートします。
    -   MySQL [<a href="https://github.com/pingcap/tidb/pull/11505">#11505</a>](https://github.com/pingcap/tidb/pull/11505)と互換性を持たせるために、 `REGEXP BINARY`の関数の大文字と小文字を区別するようにします。
    -   `DATE_ADD` / `DATE_SUB`の結果の`YEAR`の値が 0 より小さい場合、または 65535 [<a href="https://github.com/pingcap/tidb/pull/11477">#11477</a>](https://github.com/pingcap/tidb/pull/11477)より大きい場合にオーバーフローし、 `NULL`が正しく返されない問題を修正
    -   低速クエリ テーブルに、実行が成功したかどうかを示す`Succ`フィールドを追加します[<a href="https://github.com/pingcap/tidb/pull/11421">#11412</a>](https://github.com/pingcap/tidb/pull/11421)
    -   SQL ステートメントに現在時刻 ( `CURRENT_TIMESTAMP`や`NOW`など) の計算が含まれる場合に、現在のタイムスタンプを複数回フェッチすることによって引き起こされる MySQL の非互換性の問題を修正します[<a href="https://github.com/pingcap/tidb/pull/11392">#11392</a>](https://github.com/pingcap/tidb/pull/11392)
    -   AUTO_INCREMENT カラムが FLOAT または DOUBLE タイプ[<a href="https://github.com/pingcap/tidb/pull/11389">#11389</a>](https://github.com/pingcap/tidb/pull/11389)を処理しない問題を修正します。
    -   `CONVERT_TZ`関数が無効な引数[<a href="https://github.com/pingcap/tidb/pull/11357">#11357</a>](https://github.com/pingcap/tidb/pull/11357)を受け入れた場合、 `NULL`が正しく返されない問題を修正
    -   `PARTITION BY LIST`ステートメントによってエラーが報告される問題を修正します。 (現在、構文のみがサポートされています。TiDB がステートメントを実行すると、通常のテーブルが作成され、プロンプト メッセージが表示されます) [<a href="https://github.com/pingcap/tidb/pull/11236">#11236</a>](https://github.com/pingcap/tidb/pull/11236)
    -   10 進数の桁数 ( `select 0.000 % 0.11234500000000000000`など) が多い場合、 `Mod(%)` 、 `Multiple(*)` 、および`Minus(-)`操作で MySQL の結果と矛盾する`0`結果が返されるという問題を修正します[<a href="https://github.com/pingcap/tidb/pull/11353">#11353</a>](https://github.com/pingcap/tidb/pull/11353)
-   サーバ
    -   `OnInit`がコールバックされるとプラグインが`NULL`ドメインを取得する問題を修正[<a href="https://github.com/pingcap/tidb/pull/11426">#11426</a>](https://github.com/pingcap/tidb/pull/11426)
    -   スキーマが削除された後も、HTTP インターフェイスを介してスキーマ内のテーブル情報を取得できる問題を修正します[<a href="https://github.com/pingcap/tidb/pull/11586">#11586</a>](https://github.com/pingcap/tidb/pull/11586)
-   DDL
    -   この操作によって引き起こされる自動インクリメント列の誤った結果を避けるために、自動インクリメント列のインデックスの削除を禁止します[<a href="https://github.com/pingcap/tidb/pull/11402">#11402</a>](https://github.com/pingcap/tidb/pull/11402)
    -   異なる文字セットと照合順序でテーブルを作成および変更すると、列の文字セットが正しくなくなる問題を修正します[<a href="https://github.com/pingcap/tidb/pull/11423">#11423</a>](https://github.com/pingcap/tidb/pull/11423)
    -   `alter table ... set default...`とこの列を変更する別の DDL ステートメントが並行して実行されると、列スキーマが正しくなくなる可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/11374">#11374</a>](https://github.com/pingcap/tidb/pull/11374)
    -   カラムA が生成カラムB に依存しており、A を使用してインデックス[<a href="https://github.com/pingcap/tidb/pull/11538">#11538</a>](https://github.com/pingcap/tidb/pull/11538)を作成すると、データのバックフィルが失敗する問題を修正します。
    -   `ADMIN CHECK TABLE`操作[<a href="https://github.com/pingcap/tidb/pull/11676">#11538</a>](https://github.com/pingcap/tidb/pull/11676)の高速化

## TiKV {#tikv}

-   クライアントが閉じられている TiKVリージョンにアクセスしたときにエラー メッセージを返すサポート[<a href="https://github.com/tikv/tikv/pull/4820">#4820</a>](https://github.com/tikv/tikv/pull/4820)
-   リバース`raw_scan`および`raw_batch_scan`インターフェイスをサポート[<a href="https://github.com/tikv/tikv/pull/5148">#5148</a>](https://github.com/tikv/tikv/pull/5148)

## ツール {#tools}

-   TiDBBinlog
    -   Drainerに`ignore-txn-commit-ts`構成項目を追加して、トランザクション[<a href="https://github.com/pingcap/tidb-binlog/pull/697">#697</a>](https://github.com/pingcap/tidb-binlog/pull/697)内の一部のステートメントの実行をスキップします。
    -   起動時に構成項目チェックを追加します。これにより、PumpとDrainerの実行が停止され、無効な構成項目に一致するとエラー メッセージが返されます[<a href="https://github.com/pingcap/tidb-binlog/pull/708">#708</a>](https://github.com/pingcap/tidb-binlog/pull/708)
    -   Drainerに`node-id`構成を追加して、Drainer のノード ID [<a href="https://github.com/pingcap/tidb-binlog/pull/706">#706</a>](https://github.com/pingcap/tidb-binlog/pull/706)を指定します。
-   TiDB Lightning
    -   2つのチェックサムを同時に実行している場合、 `tikv_gc_life_time`元の値に戻すことができない問題を修正[<a href="https://github.com/pingcap/tidb-lightning/pull/224">#224</a>](https://github.com/pingcap/tidb-lightning/pull/224)

## TiDB Ansible {#tidb-ansible}

-   Spark [<a href="https://github.com/pingcap/tidb-ansible/pull/842">#842</a>](https://github.com/pingcap/tidb-ansible/pull/842)に`log4j`構成ファイルを追加します
-   tispark jar パッケージを v2.1.2 に更新します[<a href="https://github.com/pingcap/tidb-ansible/pull/863">#863</a>](https://github.com/pingcap/tidb-ansible/pull/863)
-   TiDB Binlog がKafka または ZooKeeper を使用する場合に、Prometheus 構成ファイルが間違った形式で生成される問題を修正します[<a href="https://github.com/pingcap/tidb-ansible/pull/845">#845</a>](https://github.com/pingcap/tidb-ansible/pull/845)
-   `rolling_update.yml`オペレーション[<a href="https://github.com/pingcap/tidb-ansible/pull/888">#888</a>](https://github.com/pingcap/tidb-ansible/pull/888)実行時に PD がLeaderの切り替えに失敗するバグを修正
-   安定性を向上させるために、PD ノードのローリング更新ロジックを最適化します (最初にフォロワーをアップグレードし、次にLeaderをアップグレードします[<a href="https://github.com/pingcap/tidb-ansible/pull/895">#895</a>](https://github.com/pingcap/tidb-ansible/pull/895)
