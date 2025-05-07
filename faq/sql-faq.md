---
title: SQL FAQs
summary: TiDB SQLに関連する FAQ について説明します。
---

# SQLに関するよくある質問 {#sql-faqs}

このドキュメントでは、TiDB での SQL 操作に関する FAQ をまとめています。

## TiDB はセカンダリキーをサポートしていますか? {#does-tidb-support-the-secondary-key}

はい。主キーではない列に、一意の[セカンダリインデックス](/develop/dev-guide-create-secondary-indexes.md)持つ[`NOT NULL`制約](/constraints.md#not-null)設定できます。この場合、その列はセカンダリキーとして機能します。

## 大きなテーブルで DDL 操作を実行する場合、TiDB はどのように機能しますか? {#how-does-tidb-perform-when-executing-ddl-operations-on-a-large-table}

大規模なテーブルに対するTiDBのDDL操作は、通常は問題になりません。TiDBはオンラインDDL操作をサポートしており、これらのDDL操作はDML操作をブロックしません。

列の追加、列の削除、インデックスの削除などの一部の DDL 操作では、TiDB はこれらの操作を迅速に実行できます。

インデックスの追加など、一部の負荷の高いDDL操作では、TiDBはデータのバックフィルを行う必要があります。この処理には（テーブルのサイズに応じて）長い時間がかかり、追加のリソースを消費します。オンライントラフィックへの影響は調整可能です。TiDBは複数のスレッドでバックフィルを実行でき、消費されるリソースは以下のシステム変数によって設定できます。

-   [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
-   [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
-   [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
-   [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

## 適切なクエリプランを選択するにはどうすればよいですか？ヒントを使用する必要がありますか？それとも、ヒントを使用できますか？ {#how-to-choose-the-right-query-plan-do-i-need-to-use-hints-or-can-i-use-hints}

TiDBにはコストベースのオプティマイザが搭載されています。ほとんどの場合、オプティマイザが最適なクエリプランを選択します。オプティマイザがうまく機能しない場合でも、 [オプティマイザヒント](/optimizer-hints.md)使用してオプティマイザに介入することができます。

さらに、 [SQLバインディング](/sql-plan-management.md#sql-binding)使用して、特定の SQL ステートメントのクエリ プランを修正することもできます。

## 特定の SQL ステートメントの実行を防ぐにはどうすればよいでしょうか? {#how-to-prevent-the-execution-of-a-particular-sql-statement}

TiDB v7.5.0以降のバージョンでは、 [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md)ステートメントを使用して特定のSQL文を終了できます。詳細については、 [予想よりも多くのリソースを消費するクエリ（ランナウェイクエリ）を管理する](/tidb-resource-control.md#query-watch-parameters)参照してください。

TiDB v7.5.0より前のバージョンでは、 [`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)ヒントを使用して[SQLバインディング](/sql-plan-management.md#sql-binding)作成し、特定のステートメントの実行時間を小さな値（例えば1ミリ秒）に制限することができます。これにより、ステートメントはしきい値によって自動的に終了します。

たとえば、 `SELECT * FROM t1, t2 WHERE t1.id = t2.id`の実行を防ぐには、次の SQL バインディングを使用して、ステートメントの実行時間を 1 ミリ秒に制限できます。

```sql
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ MAX_EXECUTION_TIME(1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注記：**
>
> `MAX_EXECUTION_TIME`の精度は約100ミリ秒です。TiDBがSQL文を終了する前に、TiKV内のタスクが開始される場合があります。このような場合にTiKVのリソース消費を抑えるには、 [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)から`ON`に設定することをお勧めします。

この SQL バインディングを削除すると、制限が解除されます。

```sql
DROP GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

## TiDB と互換性のある MySQL 変数は何ですか? {#what-are-the-mysql-variables-that-tidb-is-compatible-with}

[システム変数](/system-variables.md)参照。

## <code>ORDER BY</code>を省略した場合、結果の順序はMySQLと異なります。 {#the-order-of-results-is-different-from-mysql-when-code-order-by-code-is-omitted}

これはバグではありません。レコードのデフォルトの順序は様々な状況に依存し、一貫性は保証されません。

MySQLでは、クエリが単一スレッドで実行されるため、結果の順序は安定しているように見えるかもしれません。しかし、新しいバージョンにアップグレードすると、クエリプランが変更される場合があります。結果の順序を指定したい場合は、常に`ORDER BY`使用することをお勧めします。

参照文献は[ISO/IEC 9075:1992、データベース言語 SQL - 1992年7月30日](http://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt)にあり、次のように述べられています。

> `<order by clause>`が指定されていない場合、 `<cursor specification>`によって指定されたテーブルは T であり、T 内の行の順序は実装に依存します。

次の 2 つのクエリでは、両方の結果が正当であると見なされます。

```sql
> select * from t;
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    2 |
+------+------+
2 rows in set (0.00 sec)
```

```sql
> select * from t; -- the order of results is not guaranteed
+------+------+
| a    | b    |
+------+------+
|    2 |    2 |
|    1 |    1 |
+------+------+
2 rows in set (0.00 sec)
```

`ORDER BY`で使用されている列のリストが一意でない場合、この文も非決定的であるとみなされます。次の例では、列`a`重複した値があります。したがって、決定的であることが保証されるのは`ORDER BY a, b`のみです。

```sql
> select * from t order by a;
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    1 |
|    2 |    2 |
+------+------+
3 rows in set (0.00 sec)
```

次のステートメントでは、列`a`の順序は保証されますが、 `b`の順序は保証されません。

```sql
> select * from t order by a;
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    2 |
|    2 |    1 |
+------+------+
3 rows in set (0.00 sec)
```

TiDB では、システム変数[`tidb_enable_ordered_result_mode`](/system-variables.md#tidb_enable_ordered_result_mode)使用して、最終出力結果を自動的にソートすることもできます。

## TiDB は<code>SELECT FOR UPDATE</code>サポートしていますか? {#does-tidb-support-code-select-for-update-code}

はい。悲観的ロック（TiDB v3.0.8 以降のデフォルト）を使用する場合、 `SELECT FOR UPDATE`実行は MySQL と同様に動作します。

楽観的ロックを使用する場合、 `SELECT FOR UPDATE`トランザクションの開始時にデータをロックしませんが、トランザクションのコミット時に競合をチェックします。チェックで競合が見つかった場合、コミットしたトランザクションはロールバックされます。

詳細は[`SELECT`構文要素の説明](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements)参照。

## TiDBのコーデックは、UTF-8文字列がmemcomparableであることを保証できますか？キーがUTF-8をサポートする必要がある場合、コーディングに関する提案はありますか？ {#can-the-codec-of-tidb-guarantee-that-the-utf-8-string-is-memcomparable-is-there-any-coding-suggestion-if-our-key-needs-to-support-utf-8}

TiDBのデフォルトの文字セットは`utf8mb4`です。文字列はmemcomparable形式です。TiDBの文字セットの詳細については、 [文字セットと照合順序](/character-set-and-collation.md)参照してください。

## トランザクション内のステートメントの最大数はいくつですか? {#what-is-the-maximum-number-of-statements-in-a-transaction}

トランザクション内のステートメントの最大数は、デフォルトでは 5000 です。

楽観的トランザクション モードでトランザクションの再試行が有効になっている場合、デフォルトの上限は 5000 です。1 [`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit)を使用して制限を調整できます。

## TiDB で、後から挿入されたデータの自動増分 ID が、前に挿入されたデータの自動増分 ID よりも小さくなるのはなぜですか? {#why-does-the-auto-increment-id-of-the-later-inserted-data-is-smaller-than-that-of-the-earlier-inserted-data-in-tidb}

TiDBの自動増分ID機能は、自動的に増分され一意であることが保証されるだけで、連続的に割り当てられることは保証されません。現在、TiDBはIDをバッチで割り当てています。複数のTiDBサーバーに同時にデータが挿入された場合、割り当てられるIDは連続的ではありません。複数のスレッドが`tidb-server`のインスタンスに同時にデータを挿入した場合、後で挿入されたデータの自動増分IDは小さくなる可能性があります。TiDBでは整数フィールドに`AUTO_INCREMENT`指定できますが、1つのテーブルに`AUTO_INCREMENT`フィールドは1つしか指定できません。詳細については、 [自動増分ID](/mysql-compatibility.md#auto-increment-id)と[AUTO_INCREMENT属性](/auto-increment.md)参照してください。

## TiDB の<code>sql_mode</code>を変更するにはどうすればよいですか? {#how-do-i-modify-the-code-sql-mode-code-in-tidb}

TiDB は、SESSION または GLOBAL ベースで[`sql_mode`](/system-variables.md#sql_mode)システム変数を変更することをサポートしています。

-   [`GLOBAL`](/sql-statements/sql-statement-set-variable.md)スコープの変数への変更は、クラスター内の残りのサーバーに伝播し、再起動後も保持されます。つまり、各 TiDBサーバーで`sql_mode`値を変更する必要はありません。
-   `SESSION`スコープ変数への変更は、現在のクライアントセッションにのみ影響します。サーバーを再起動すると、変更は失われます。

## エラー: <code>java.sql.BatchUpdateException:statement count 5001 exceeds the transaction limitation</code> {#error-code-java-sql-batchupdateexception-statement-count-5001-exceeds-the-transaction-limitation-code-while-using-sqoop-to-write-data-into-tidb-in-batches}

Sqoopでは、 `--batch`各バッチで100文をコミットすることを意味しますが、デフォルトでは各文に100個のSQL文が含まれます。つまり、100 * 100 = 10000文となり、これは単一のTiDBトランザクションで許可される文の最大数である5000を超えます。

2つの解決策:

-   次のように`-Dsqoop.export.records.per.statement=10`オプションを追加します。

    ```bash
    sqoop export \
        -Dsqoop.export.records.per.statement=10 \
        --connect jdbc:mysql://mysql.example.com/sqoop \
        --username sqoop ${user} \
        --password ${passwd} \
        --table ${tab_name} \
        --export-dir ${dir} \
        --batch
    ```

-   単一のTiDBトランザクション内のステートメント数の制限を増やすこともできますが、これによりメモリ消費量が増加します。詳細については[SQL文の制限](/tidb-limitations.md#limitations-on-sql-statements)参照してください。

## TiDB には Oracle のフラッシュバック クエリのような機能がありますか? DDL をサポートしていますか? {#does-tidb-have-a-function-like-the-flashback-query-in-oracle-does-it-support-ddl}

はい、サポートしています。DDLもサポートしています。詳細は[`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)ご覧ください。

## TiDB はデータを削除した後すぐにスペースを解放しますか? {#does-tidb-release-space-immediately-after-deleting-data}

`DELETE` `TRUNCATE`操作`DROP`いずれもデータを即時に解放しません。7と`TRUNCATE` `DROP`操作では、TiDB GC（ガベージコレクション）時間（デフォルトでは10分）後にデータが削除され、領域が解放されます。11 `DELETE`操作では、データは削除されますが、圧縮が実行されるまで領域は即時に解放されません。

## データを削除するとクエリ速度が遅くなるのはなぜですか? {#why-does-the-query-speed-get-slow-after-data-is-deleted}

大量のデータを削除すると、多くの無駄なキーが残り、クエリの効率に影響します。この問題を解決するには、 [リージョン結合](/best-practices/massive-regions-best-practices.md#method-3-enable-region-merge)機能を使用できます。詳細については、 [TiDBベストプラクティスのデータセクションの削除](https://www.pingcap.com/blog/tidb-best-practice/#write)参照してください。

## データを削除した後、storageスペースの回復に時間がかかる場合はどうすればよいでしょうか? {#what-should-i-do-if-it-is-slow-to-reclaim-storage-space-after-deleting-data}

TiDBはマルチバージョン同時実行制御（MVCC）を使用しているため、古いデータが新しいデータで上書きされる際、古いデータは置き換えられず、新しいデータと共に保持されます。データのバージョンを識別するためにタイムスタンプが使用されます。データを削除しても、すぐに領域が解放されるわけではありません。同時実行トランザクションが以前のバージョンの行を参照できるように、ガベージコレクションは遅延されます。これは、システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) （デフォルト： `10m0s` ）で設定できます。

## <code>SHOW PROCESSLIST</code>システム プロセス ID を表示しますか? {#does-code-show-processlist-code-display-the-system-process-id}

TiDB `SHOW PROCESSLIST`の表示内容は MySQL `SHOW PROCESSLIST`とほぼ同じです。TiDB `SHOW PROCESSLIST`ではシステムプロセスIDが表示されません。表示されるのは現在のセッションIDです。TiDB `SHOW PROCESSLIST`と MySQL `SHOW PROCESSLIST`の違いは次のとおりです。

-   TiDBは分散データベースであるため、 `tidb-server`インスタンスはSQL文を解析および実行するためのステートレスエンジンです（詳細は[TiDBアーキテクチャ](/tidb-architecture.md)参照）。5 `SHOW PROCESSLIST` 、ユーザーがMySQLクライアントからログインした`tidb-server`インスタンスで実行されたセッションリストを表示します。クラスタ内で実行されているすべてのセッションのリストではありません。ただし、MySQLはスタンドアロンデータベースであり、 `SHOW PROCESSLIST`はMySQLで実行されたすべてのSQL文を表示します。
-   TiDBの`State`列目は、クエリ実行中に継続的に更新されるわけではありません。TiDBは並列クエリをサポートしているため、各ステートメントが複数の*状態*にある場合があり、単一の値に単純化することが困難です。

## SQL コミットの実行優先度を制御または変更するにはどうすればよいですか? {#how-to-control-or-change-the-execution-priority-of-sql-commits}

TiDBは、 [グローバル](/system-variables.md#tidb_force_priority)単位または個々のステートメント単位での優先度の変更をサポートしています。優先度は以下の意味を持ちます。

-   `HIGH_PRIORITY` : このステートメントの優先度は高いです。つまり、TiDB はこのステートメントを優先し、最初に実行します。

-   `LOW_PRIORITY` : このステートメントの優先度は低いです。つまり、TiDB は実行期間中にこのステートメントの優先度を下げます。

-   `DELAYED` : このステートメントは通常の優先度を持ち、 `tidb_force_priority`の`NO_PRIORITY`設定と同じです。

> **注記：**
>
> TiDB v6.6.0以降、 [リソース管理](/tidb-resource-control.md)サポートします。この機能を使用すると、異なるリソースグループで異なる優先度のSQL文を実行できます。これらのリソースグループに適切なクォータと優先度を設定することで、優先度の異なるSQL文のスケジュールをより適切に制御できます。リソース制御を有効にすると、文の優先度は適用されなくなります。異なるSQL文のリソース使用量を管理するには、 [リソース管理](/tidb-resource-control.md)使用することをお勧めします。

上記の2つのパラメータをTiDBのDMLと組み合わせて使用できます。例：

1.  データベースに SQL ステートメントを記述して優先順位を調整します。

    ```sql
    SELECT HIGH_PRIORITY | LOW_PRIORITY | DELAYED COUNT(*) FROM table_name;
    INSERT HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name insert_values;
    DELETE HIGH_PRIORITY | LOW_PRIORITY | DELAYED FROM table_name;
    UPDATE HIGH_PRIORITY | LOW_PRIORITY | DELAYED table_reference SET assignment_list WHERE where_condition;
    REPLACE HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name;
    ```

2.  フル テーブル スキャン ステートメントは、自動的に低い優先度に調整されます。 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 、デフォルトで低い優先度を持ちます。

## TiDB での<code>auto analyze</code>のトリガー戦略は何ですか? {#what-s-the-trigger-strategy-for-code-auto-analyze-code-in-tidb}

テーブル内の行数またはパーティションテーブルの単一パーティションの行数が 1000 に達し、テーブルまたはパーティションの比率 (変更された行数 / 現在の行数の合計) が[`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)を超えると、 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)ステートメントが自動的にトリガーされます。

システム変数`tidb_auto_analyze_ratio`のデフォルト値は`0.5`で、この機能がデフォルトで有効になっていることを示します。システム変数`tidb_auto_analyze_ratio`を[`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)以上（デフォルト値は`0.8` ）に設定することは推奨されません。そうしないと、オプティマイザーが疑似統計を使用する可能性があります。TiDB v5.3.0 では[`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)変数が導入され、これを`OFF`に設定すると、統計が古くても疑似統計は使用されません。

`auto analyze`無効にするには、システム変数[`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)使用します。

## オプティマイザーヒントを使用してオプティマイザーの動作をオーバーライドできますか? {#can-i-use-optimizer-hints-to-override-the-optimizer-behavior}

TiDBは、 [ヒント](/optimizer-hints.md)と[SQLプラン管理](/sql-plan-management.md)を含む、デフォルトのクエリオプティマイザの動作をオーバーライドする複数の方法をサポートしています。基本的な使用方法はMySQLと同様ですが、TiDB固有の拡張機能がいくつかあります。

```sql
SELECT column_name FROM table_name USE INDEX（index_name）WHERE where_condition;
```

## DDL実行 {#ddl-execution}

このセクションでは、DDL文の実行に関連する問題を列挙します。DDL実行の原則に関する詳細な説明については、 [DDL ステートメントの実行原則とベストプラクティス](/ddl-introduction.md)参照してください。

### さまざまな DDL 操作を実行するにはどのくらいの時間がかかりますか? {#how-long-does-it-take-to-perform-various-ddl-operations}

DDL操作がブロックされておらず、各TiDBサーバーがスキーマバージョンを正常に更新でき、DDLオーナーノードが正常に動作していると仮定します。この場合、各種DDL操作の推定時間は以下のとおりです。

| DDL操作タイプ                                                                                                                                                                   | 推定所要時間                            |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------- |
| 再編成DDL（ `ADD INDEX`など`MODIFY COLUMN` （再編成タイプのデータ変更）                                                                                                                        | データ量、システム負荷、DDL パラメータ設定によって異なります。 |
| 一般`ALTER TABLE DROP`な`DROP TABLE` （Reorg `ALTER TABLE ADD`の`DROP DATABASE` `CREATE TABLE` ）、 `TRUNCATE TABLE` ： `CREATE DATABASE` （メタデータのみ変更） `DROP INDEX` `MODIFY COLUMN` | 約1秒                               |

> **注記：**
>
> 上記は作業にかかる推定時間です。実際の時間は異なる場合があります。

### DDL実行が遅い理由 {#possible-reasons-why-ddl-execution-is-slow}

-   ユーザーセッションにおいて、DDL文の前に非自動コミットDML文があり、その非自動コミットDML文のコミット処理が遅い場合、DDL文の実行速度が低下します。つまり、TiDBはDDL文を実行する前に、コミットされていないDML文をコミットします。

-   複数のDDL文を同時に実行する場合、後続のDDL文はキュー内で待機する必要があるため、実行速度が遅くなる可能性があります。キューイングのシナリオには以下が含まれます。

    -   同じ種類のDDL文はキューに登録する必要があります。例えば、 `CREATE TABLE`と`CREATE DATABASE`どちらも一般的なDDL文であるため、両方の操作が同時に実行される場合はキューに登録する必要があります。TiDB v6.2.0以降では並列DDL文がサポートされていますが、DDL実行にTiDBの計算リソースが過度に使用されるのを防ぐため、同時実行数制限も設けられています。DDL文が同時実行数制限を超えると、キューに登録されます。
    -   同じテーブルに対して実行されるDDL操作は依存関係にあります。後続のDDL文は、前のDDL操作が完了するまで待機する必要があります。

-   クラスターが正常に起動した後、DDL モジュールが DDL 所有者を選出するため、最初の DDL 操作の実行時間が比較的長くなる可能性があります。

-   TiDBが終了し、PDと正常に通信できなくなります（電源オフの状態も含む）。または、TiDBがコマンド`kill -9`によって終了し、PDから登録データを適切なタイミングで消去できなくなります。

-   クラスター内の特定の TiDB ノードと PD または TiKV の間で通信の問題が発生し、TiDB が最新のバージョン情報を時間内に取得できなくなります。

### <code>Information schema is changed</code>エラーの原因は何ですか? {#what-triggers-the-code-information-schema-is-changed-code-error}

SQL文を実行する際、TiDBは分離レベルに基づいてオブジェクトのスキーマバージョンを決定し、それに応じてSQL文を処理します。TiDBはオンラインの非同期DDL変更もサポートしています。DML文を実行する際、複数のDDL文が同時に実行される可能性があり、各SQL文が同じスキーマに対して実行されるようにする必要があります。そのため、DML実行時にDDL操作が進行中の場合、TiDBはエラー`Information schema is changed`報告する可能性があります。

v6.4.0 以降、TiDB は[メタデータロックメカニズム](/metadata-lock.md)実装しており、これにより DML ステートメントと DDL スキーマの変更の調整された実行が可能になり、ほとんどの`Information schema is changed`エラーを回避できます。

このエラー報告には、まだいくつかの原因があります。

-   原因1: DML操作に関係するテーブルの一部は、進行中のDDL操作に関係するテーブルと同じです。進行中のDDL操作を確認するには、 `ADMIN SHOW DDL`ステートメントを使用してください。
-   原因2：DML操作が長時間実行されています。この期間中に多数のDDL文が実行され、1024を超える`schema`バージョンの変更が発生しています。このデフォルト値は、変数`tidb_max_delta_schema_count`変更することで変更できます。
-   原因3：DMLリクエストを受け付けるTiDBサーバーが長時間`schema information`できない状態です（TiDBとPDまたはTiKV間の接続障害が原因と考えられます）。この期間中に多数のDDL文が実行され、100件を超える`schema`バージョンの変更が発生しました。
-   原因 4: TiDB が再起動し、最初の DDL 操作が実行される前に、DML 操作が実行され、最初の DDL 操作に遭遇します (つまり、最初の DDL 操作が実行される前に、DML に対応するトランザクションが開始されます。そして、DDL の最初の`schema`バージョンが変更された後、DML に対応するトランザクションがコミットされます)。この DML 操作によってこのエラーが報告されます。

上記の原因のうち、テーブルに関連するのは原因1のみです。原因1と原因2は、関連するDML操作が失敗後に再試行されるため、アプリケーションには影響しません。原因3については、TiDBとTiKV/PD間のネットワークを確認する必要があります。

> **注記：**
>
> -   現在、TiDB はバージョン`schema`の変更をすべてキャッシュしません。
> -   各 DDL 操作では、 `schema`バージョンの変更の数は、対応する`schema state`バージョンの変更の数と同じです。
> -   DDL操作によって、バージョン`schema`変更回数は異なります。例えば、 `CREATE TABLE`文ではバージョン`schema`変更が1回発生し、 `ADD COLUMN`文ではバージョン5の変更が4回発生します。

### 「情報スキーマが古くなっています」というエラーの原因は何ですか? {#what-are-the-causes-of-the-information-schema-is-out-of-date-error}

DML文の実行時に、TiDBがDDLリース（デフォルトでは45秒）内に最新のスキーマをロードできない場合、エラー`Information schema is out of date`が発生する可能性があります。考えられる原因は以下のとおりです。

-   このDMLを実行したTiDBインスタンスが強制終了され、このDML文に対応するトランザクションの実行にDDLリースよりも長い時間がかかりました。トランザクションがコミットされた際にエラーが発生しました。
-   このDML文の実行中に、TiDBはPDまたはTiKVへの接続に失敗しました。その結果、TiDBはDDLリース内でスキーマのロードに失敗したか、キープアライブ設定によりPDから切断されました。

### 高い同時実行性で DDL ステートメントを実行するとエラーが報告されますか? {#error-is-reported-when-executing-ddl-statements-under-high-concurrency}

高い同時実行性で DDL ステートメント (バッチでのテーブル作成など) を実行すると、同時実行中のキーの競合により、これらのステートメントのごく一部が失敗する可能性があります。

同時実行 DDL ステートメントの数を 20 未満に保つことをお勧めします。それ以外の場合は、失敗したステートメントをクライアントから再試行する必要があります。

### DDL 実行がブロックされるのはなぜですか? {#why-is-ddl-execution-blocked}

TiDB v6.2.0より前のバージョンでは、DDL文の種類に基づいて、2つの先入先出キューにDDL文を割り当てていました。具体的には、再編成DDLは再編成キューに、一般DDLは一般キューに割り当てられます。先入先出の制限と、同一テーブルに対するDDL文の連続実行の必要性により、複数のDDL文が実行中にブロックされる可能性があります。

たとえば、次の DDL ステートメントを考えます。

-   DDL 1: `CREATE INDEX idx on t(a int);`
-   DDL 2: `ALTER TABLE t ADD COLUMN b int;`
-   DDL 3: `CREATE TABLE t1(a int);`

先入先出キューの制限により、DDL 3 は DDL 2 の実行を待機する必要があります。また、同じテーブル上の DDL 文はシリアルで実行する必要があるため、DDL 2 は DDL 1 の実行を待機する必要があります。そのため、DDL 3 と DDL 2 が異なるテーブルに対して実行される場合でも、DDL 3 は DDL 1 が先に実行されるまで待機する必要があります。

TiDB v6.2.0以降、TiDB DDLモジュールは並列フレームワークを採用しています。並列フレームワークでは、先入先出キューの制限がなくなりました。代わりに、TiDBはすべてのDDLタスクの中から実行可能なDDLタスクを選択します。さらに、Reorgワーカーの数がノードあたり約`CPU/4`に拡張されました。これにより、TiDBは並列フレームワーク内で複数のテーブルのインデックスを同時に構築できます。

新規クラスタでも、以前のバージョンからアップグレードしたクラスタでも、TiDB v6.2以降のバージョンでは、TiDBは自動的にコンカレントフレームワークを使用します。手動で調整する必要はありません。

### DDL実行のスタックの原因を特定する {#identify-the-cause-of-stuck-ddl-execution}

1.  DDL ステートメントの実行が遅くなる他の理由を排除します。
2.  DDL 所有者ノードを識別するには、次のいずれかの方法を使用します。
    -   現在のクラスターの所有者を取得するには、 `curl http://{TiDBIP}:10080/info/all`使用します。
    -   監視ダッシュボードの**DDL** &gt; **DDL META OPM**から、特定の期間の所有者をビュー。

-   所有者が存在しない場合は、次を実行して所有者の選択を手動でトリガーしてみてください: `curl -X POST http://{TiDBIP}:10080/ddl/owner/resign` 。
-   所有者が存在する場合は、Goroutine スタックをエクスポートし、スタックしている可能性のある場所を確認します。

## JDBC接続で使用される照合順序 {#collation-used-in-jdbc-connections}

このセクションでは、JDBC接続で使用される照合順序に関する質問を示します。TiDBでサポートされている文字セットと照合順序については、 [文字セットと照合順序](/character-set-and-collation.md)参照してください。

### JDBC URL で<code>connectionCollation</code>が構成されていない場合、JDBC 接続ではどの照合順序が使用されますか? {#what-collation-is-used-in-a-jdbc-connection-when-code-connectioncollation-code-is-not-configured-in-the-jdbc-url}

JDBC URL に`connectionCollation`が設定されていない場合、次の 2 つのシナリオが考えられます。

**シナリオ 1** : JDBC URL に`connectionCollation`も`characterEncoding`設定されていない

-   Connector/J 8.0.25以前のバージョンでは、JDBCドライバはサーバーのデフォルトの文字セットを使用しようとします。TiDBのデフォルトの文字セットは`utf8mb4`であるため、ドライバは接続照合順序として`utf8mb4_bin`使用します。
-   Connector/J 8.0.26 以降のバージョンでは、JDBC ドライバーは`utf8mb4`文字セットを使用し、戻り値`SELECT VERSION()`に基づいて照合順序を自動的に選択します。

    -   戻り値が`8.0.1`未満の場合、ドライバは接続照合順序として`utf8mb4_general_ci`使用します。TiDB はドライバに従い、照合順序として`utf8mb4_general_ci`使用します。
    -   戻り値が`8.0.1`以上の場合、ドライバは接続照合順序として`utf8mb4_0900_ai_ci`使用します。TiDB v7.4.0 以降のバージョンではドライバに従い、照合順序として`utf8mb4_0900_ai_ci`使用しますが、TiDB v7.4.0 より前のバージョンでは`utf8mb4_0900_ai_ci`照合順序がサポートされていないため、デフォルトの照合順序`utf8mb4_bin`使用されます。

**シナリオ2** ：JDBC URLに`characterEncoding=utf8`が設定されていますが、 `connectionCollation`設定されていません。JDBCドライバーはマッピングルールに従って`utf8mb4`文字セットを使用します。照合順序はシナリオ1で説明したルールに従って決定されます。

### TiDB をアップグレードした後、照合順序の変更をどのように処理しますか? {#how-to-handle-collation-changes-after-upgrading-tidb}

TiDB v7.4 以前のバージョンでは、 `connectionCollation`が構成されておらず、JDBC URL で`characterEncoding`構成されていないか`UTF-8`に設定されている場合、TiDB [`collation_connection`](/system-variables.md#collation_connection)変数はデフォルトで`utf8mb4_bin`照合順序に設定されます。

TiDB v7.4以降、 `connectionCollation`が設定されておらず、JDBC URLで`characterEncoding`設定されていないか`UTF-8`に設定されている場合、 [`collation_connection`](/system-variables.md#collation_connection)変数の値はJDBCドライバのバージョンによって異なります。例えば、Connector/J 8.0.26以降のバージョンでは、JDBCドライバはデフォルトで`utf8mb4`文字セットを使用し、接続照合順序として`utf8mb4_general_ci`使用します。TiDBはドライバに従い、 [`collation_connection`](/system-variables.md#collation_connection)変数は`utf8mb4_0900_ai_ci`照合順序を使用します。詳細については、 [JDBC接続で使用される照合順序](#what-collation-is-used-in-a-jdbc-connection-when-connectioncollation-is-not-configured-in-the-jdbc-url)参照してください。

以前のバージョンから v7.4 以降にアップグレードする場合 (たとえば、v6.5 から v7.5)、JDBC 接続で`collation_connection` `utf8mb4_bin`として維持する必要がある場合は、JDBC URL で`connectionCollation`パラメータを構成することをお勧めします。

以下は、TiDB v6.5 での一般的な JDBC URL 構成です。

    spring.datasource.url=JDBC:mysql://{TiDBIP}:{TiDBPort}/{DBName}?characterEncoding=UTF-8&useSSL=false&useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSqlLimit=10000&prepStmtCacheSize=1000&useConfigs=maxPerformance&rewriteBatchedStatements=true&defaultFetchSize=-2147483648&allowMultiQueries=true

TiDB v7.5 以降のバージョンにアップグレードした後は、JDBC URL に`connectionCollation`パラメータを設定することをお勧めします。

    spring.datasource.url=JDBC:mysql://{TiDBIP}:{TiDBPort}/{DBName}?characterEncoding=UTF-8&connectionCollation=utf8mb4_bin&useSSL=false&useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSqlLimit=10000&prepStmtCacheSize=1000&useConfigs=maxPerformance&rewriteBatchedStatements=true&defaultFetchSize=-2147483648&allowMultiQueries=true

### <code>utf8mb4_bin</code>と<code>utf8mb4_0900_ai_ci</code>照合順序の違いは何ですか? {#what-are-the-differences-between-the-code-utf8mb4-bin-code-and-code-utf8mb4-0900-ai-ci-code-collations}

| 照合                   | 大文字と小文字を区別 | 末尾のスペースを無視する | アクセントを重視 | 比較方法                  |
| -------------------- | ---------- | ------------ | -------- | --------------------- |
| `utf8mb4_bin`        | はい         | はい           | はい       | バイナリ値を比較する            |
| `utf8mb4_0900_ai_ci` | いいえ        | いいえ          | いいえ      | Unicodeソートアルゴリズムを使用する |

例えば：

```sql
-- utf8mb4_bin is case-sensitive
SELECT 'apple' = 'Apple' COLLATE utf8mb4_bin;  -- Returns 0 (FALSE)

-- utf8mb4_0900_ai_ci is case-insensitive
SELECT 'apple' = 'Apple' COLLATE utf8mb4_0900_ai_ci;  -- Returns 1 (TRUE)

-- utf8mb4_bin ignores trailing spaces
SELECT 'Apple ' = 'Apple' COLLATE utf8mb4_bin; -- Returns 1 (TRUE)

-- utf8mb4_0900_ai_ci does not ignore trailing spaces
SELECT 'Apple ' = 'Apple' COLLATE utf8mb4_0900_ai_ci; -- Returns 0 (FALSE)

-- utf8mb4_bin is accent-sensitive
SELECT 'café' = 'cafe' COLLATE utf8mb4_bin;  -- Returns 0 (FALSE)

-- utf8mb4_0900_ai_ci is accent-insensitive
SELECT 'café' = 'cafe' COLLATE utf8mb4_0900_ai_ci;  -- Returns 1 (TRUE)
```

## SQL最適化 {#sql-optimization}

### TiDB実行プランの説明 {#tidb-execution-plan-description}

[クエリ実行プランを理解する](/explain-overview.md)参照。

### 統計収集 {#statistics-collection}

[統計入門](/statistics.md)参照。

### <code>select count(1)</code>を最適化するにはどうすればいいですか? {#how-to-optimize-code-select-count-1-code}

`count(1)`文はテーブル内の行の総数をカウントします。同時実行性を向上させることで、速度を大幅に向上させることができます。同時実行性を変更するには、 [`tidb_distsql_scan_concurrency`ドキュメント](/system-variables.md#tidb_distsql_scan_concurrency)を参照してください。ただし、これはCPUとI/Oリソースにも依存します。TiDBはすべてのクエリでTiKVにアクセスします。データ量が少ない場合、MySQLはすべてメモリ内に保存されるため、TiDBはネットワークアクセスを実行する必要があります。

推奨事項:

-   ハードウェア構成を改善してください。1 [ソフトウェアおよびハードウェア要件](/hardware-and-software-requirements.md)参照してください。
-   同時実行性を改善します。デフォルト値は10です。50に上げて試してみることもできますが、通常はデフォルト値の2～4倍の改善が見られます。
-   大量のデータの場合は`count`をテストします。
-   TiKV設定を最適化します。1と[TiKV スレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md) [TiKVメモリのパフォーマンスを調整する](/tune-tikv-memory-performance.md)参照してください。
-   [コプロセッサーキャッシュ](/coprocessor-cache.md)を有効にします。

### 現在の DDL ジョブの進行状況を表示するにはどうすればよいでしょうか? {#how-to-view-the-progress-of-the-current-ddl-job}

`ADMIN SHOW DDL`使用すると、現在の DDL ジョブの進行状況を表示できます。操作は以下のとおりです。

```sql
ADMIN SHOW DDL;
```

    *************************** 1. row ***************************
      SCHEMA_VER: 140
           OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
    RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
         SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc

上記の結果から、 `ADD INDEX`操作が現在処理中であることがわかります。また、 `RUNNING_JOBS`列目の`RowCount`番目のフィールドから、 `ADD INDEX`操作によって77312行のインデックスが追加されたことがわかります。

### DDL ジョブを表示するにはどうすればいいですか? {#how-to-view-the-ddl-job}

-   `ADMIN SHOW DDL` : 実行中のDDLジョブを表示する
-   `ADMIN SHOW DDL JOBS` : 現在の DDL ジョブ キュー内のすべての結果 (実行中および実行待ちのタスクを含む) と、完了した DDL ジョブ キューの最後の 10 件の結果を表示します。
-   `ADMIN SHOW DDL JOBS QUERIES 'job_id' [, 'job_id'] ...` : `job_id`に対応する DDL タスクの元の SQL ステートメントを表示します。4 `job_id`実行中の DDL ジョブと DDL 履歴ジョブ キュー内の最後の 10 件の結果のみを検索します。

### TiDB は CBO (コストベース最適化) をサポートしていますか? サポートしている場合、どの程度サポートしていますか? {#does-tidb-support-cbo-cost-based-optimization-if-yes-to-what-extent}

はい。TiDBはコストベースオプティマイザを使用しています。コストモデルと統計は常に最適化されています。また、TiDBはハッシュ結合やソートマージ結合などの結合アルゴリズムもサポートしています。

### テーブルで<code>analyze</code>を実行する必要があるかどうかを判断するにはどうすればよいでしょうか? {#how-to-determine-whether-i-need-to-execute-code-analyze-code-on-a-table}

`SHOW STATS_HEALTHY`を使用して`Healthy`フィールドをビュー、通常、フィールド値が 60 より小さい場合はテーブルで`ANALYZE`実行する必要があります。

### クエリプランがツリーとして表現される場合のIDルールは何ですか？このツリーの実行順序は何ですか？ {#what-is-the-id-rule-when-a-query-plan-is-presented-as-a-tree-what-is-the-execution-order-for-this-tree}

これらのIDにはルールはありませんが、IDは一意です。IDが生成されるとカウンターが動作し、プランが1つ生成されるごとに1が加算されます。実行順序はIDとは無関係です。クエリプラン全体はツリー構造になっており、実行プロセスはルートノードから開始され、データは上位レベルへと連続的に返されます。クエリプランの詳細については、 [TiDBクエリ実行プランを理解する](/explain-overview.md)参照してください。

### TiDBクエリプランでは、 <code>cop</code>タスクは同じルートにあります。それらは同時に実行されますか？ {#in-the-tidb-query-plan-code-cop-code-tasks-are-in-the-same-root-are-they-executed-concurrently}

現在、 TiDB のコンピューティング タスクは、タスク`cop task`と`root task` 2 つの異なるタイプに属しています。

`cop task`は、分散実行のために KV エンドにプッシュダウンされるコンピューティング タスクです。2 `root task` 、TiDB エンドでの単一ポイント実行のためのコンピューティング タスクです。

通常、 `root task`の入力データは`cop task`から取得されます。5 `root task`データを処理している間、TiKVの`cop task`同時にデータを処理し、TiDBの`root task`からのプルを待機します。したがって、 `cop`タスクは`root task`と並行して実行されていると見なすことができますが、それらのデータには上流と下流の関係があります。実行プロセス中、それらはしばらくの間並行して実行されます。たとえば、最初の`cop task`は[100, 200]のデータを処理し、2番目の`cop task` [1, 100]のデータを処理します。詳細は[TiDBクエリプランの理解](/explain-overview.md)参照してください。

## データベースの最適化 {#database-optimization}

### TiDBオプションを編集する {#edit-tidb-options}

[TiDBコマンドオプション](/command-line-flags-for-tidb-configuration.md)参照。

### ホットスポットの問題を回避し、負荷分散を実現するにはどうすればよいですか? TiDB ではホット パーティションまたはホット範囲が問題になりますか? {#how-to-avoid-hotspot-issues-and-achieve-load-balancing-is-hot-partition-or-range-an-issue-in-tidb}

ホットスポットが発生するシナリオについては、 [一般的な鍋料理](/troubleshoot-hot-spot-issues.md#common-hotspots)を参照してください。次の TiDB 機能は、ホットスポットの問題を解決するために設計されています。

-   [`SHARD_ROW_ID_BITS`](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)属性。この属性を設定すると、行IDが複数のリージョンに分散して書き込まれるため、書き込みホットスポットの問題を軽減できます。
-   [`AUTO_RANDOM`](/troubleshoot-hot-spot-issues.md#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)属性は、自動インクリメント主キーによってもたらされるホットスポットを解決するのに役立ちます。
-   [コプロセッサーキャッシュ](/coprocessor-cache.md) 、小さなテーブル上の読み取りホットスポットの場合。
-   [ロードベーススプリット](/configure-load-base-split.md) 、小さなテーブルの完全なテーブルスキャンなど、リージョン間の不均衡なアクセスによって発生するホットスポットの場合。
-   [キャッシュされたテーブル](/cached-tables.md) 、頻繁にアクセスされるが、めったに更新されない小さなホットスポット テーブル用。

ホットスポットによってパフォーマンスの問題が発生した場合は、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照して解決してください。

### TiKV のパフォーマンスを調整する {#tune-tikv-performance}

[TiKV スレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md)と[TiKVメモリのパフォーマンスを調整する](/tune-tikv-memory-performance.md)参照してください。
