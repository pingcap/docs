---
title: SQL FAQs
summary: TiDB SQLに関連する FAQ について説明します。
---

# SQLに関するよくある質問 {#sql-faqs}

このドキュメントでは、TiDB での SQL 操作に関する FAQ をまとめています。

## TiDB はセカンダリ キーをサポートしていますか? {#does-tidb-support-the-secondary-key}

はい。一意の[二次索引](/develop/dev-guide-create-secondary-indexes.md)を持つ非主キー列に[`NOT NULL`制約](/constraints.md#not-null)設定できます。この場合、列はセカンダリ キーとして機能します。

## 大きなテーブルで DDL 操作を実行する場合、TiDB はどのように機能しますか? {#how-does-tidb-perform-when-executing-ddl-operations-on-a-large-table}

大規模なテーブルでの TiDB の DDL 操作は通常は問題になりません。TiDB はオンライン DDL 操作をサポートしており、これらの DDL 操作は DML 操作をブロックしません。

列の追加、列の削除、インデックスの削除などの一部の DDL 操作では、TiDB はこれらの操作を迅速に実行できます。

インデックスの追加などの負荷の高い DDL 操作の場合、TiDB はデータをバックフィルする必要があります。これには時間がかかり (テーブルのサイズによって異なります)、追加のリソースが消費されます。オンライン トラフィックへの影響は調整可能です。TiDB は複数のスレッドでバックフィルを実行でき、消費されるリソースは次のシステム変数によって設定できます。

-   [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
-   [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
-   [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
-   [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

## 適切なクエリ プランを選択するにはどうすればよいですか? ヒントを使用する必要がありますか? または、ヒントを使用できますか? {#how-to-choose-the-right-query-plan-do-i-need-to-use-hints-or-can-i-use-hints}

TiDB にはコストベースのオプティマイザが含まれています。ほとんどの場合、オプティマイザが最適なクエリ プランを選択します。オプティマイザがうまく機能しない場合は、 [オプティマイザヒント](/optimizer-hints.md)使用してオプティマイザに介入することもできます。

さらに、 [SQLバインディング](/sql-plan-management.md#sql-binding)使用して特定の SQL ステートメントのクエリ プランを修正することもできます。

## 特定の SQL ステートメントの実行を防ぐにはどうすればよいですか? {#how-to-prevent-the-execution-of-a-particular-sql-statement}

[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)ヒントを使用して[SQL バインディング](/sql-plan-management.md#sql-binding)を作成し、特定のステートメントの実行時間を小さな値 (たとえば、1 ミリ秒) に制限することができます。このようにして、ステートメントはしきい値によって自動的に終了します。

たとえば、 `SELECT * FROM t1, t2 WHERE t1.id = t2.id`の実行を防ぐには、次の SQL バインディングを使用して、ステートメントの実行時間を 1 ミリ秒に制限できます。

```sql
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ MAX_EXECUTION_TIME(1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注記：**
>
> `MAX_EXECUTION_TIME`の精度は約 100 ミリ秒です。TiDB が SQL 文を終了する前に、TiKV 内のタスクが開始される場合があります。このような場合に TiKV リソースの消費を減らすには、 [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)から`ON`に設定することをお勧めします。

この SQL バインディングを削除すると、制限が解除されます。

```sql
DROP GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

## TiDB と互換性のある MySQL 変数は何ですか? {#what-are-the-mysql-variables-that-tidb-is-compatible-with}

[システム変数](/system-variables.md)参照。

## <code>ORDER BY</code>を省略した場合、結果の順序はMySQLと異なります。 {#the-order-of-results-is-different-from-mysql-when-code-order-by-code-is-omitted}

これはバグではありません。レコードのデフォルトの順序はさまざまな状況に依存し、一貫性は保証されません。

MySQL では、クエリが単一のスレッドで実行されるため、結果の順序は安定しているように見えます。ただし、新しいバージョンにアップグレードすると、クエリ プランが変わることがよくあります。結果の順序が必要な場合は、常に`ORDER BY`使用することをお勧めします。

参考文献は[ISO/IEC 9075:1992、データベース言語 SQL - 1992 年 7 月 30 日](http://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt)にあり、次のように述べられています。

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

`ORDER BY`で使用される列のリストが一意でない場合、ステートメントも非決定的であると見なされます。次の例では、列`a`に重複した値があります。したがって、決定的であることが保証されるのは`ORDER BY a, b`のみです。

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

TiDB では、システム変数[`tidb_enable_ordered_result_mode`](/system-variables.md#tidb_enable_ordered_result_mode)を使用して最終出力結果を自動的にソートすることもできます。

## TiDB は<code>SELECT FOR UPDATE</code>をサポートしていますか? {#does-tidb-support-code-select-for-update-code}

はい。悲観的ロック (TiDB v3.0.8 以降のデフォルト) を使用する場合、 `SELECT FOR UPDATE`目の実行は MySQL と同様に動作します。

楽観的ロックを使用する場合、 `SELECT FOR UPDATE`トランザクションの開始時にデータをロックしませんが、トランザクションのコミット時に競合をチェックします。チェックで競合が見つかった場合、コミットするトランザクションはロールバックされます。

詳細は[`SELECT`構文要素の説明](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements)参照。

## TiDB のコーデックは、UTF-8 文字列がメモリ比較可能であることを保証できますか? キーが UTF-8 をサポートする必要がある場合、コーディングに関する提案はありますか? {#can-the-codec-of-tidb-guarantee-that-the-utf-8-string-is-memcomparable-is-there-any-coding-suggestion-if-our-key-needs-to-support-utf-8}

TiDB はデフォルトで UTF-8 文字セットを使用し、現在は UTF-8 のみをサポートしています。TiDB の文字列は memcomparable 形式を使用します。

## トランザクション内のステートメントの最大数はいくつですか? {#what-is-the-maximum-number-of-statements-in-a-transaction}

トランザクション内のステートメントの最大数は、デフォルトでは 5000 です。

楽観的トランザクション モードでトランザクション再試行が有効になっている場合、デフォルトの上限は 5000 です[`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit)パラメータを使用して制限を調整できます。

## TiDB で、後から挿入されたデータの自動インクリメント ID が、前に挿入されたデータの自動インクリメント ID よりも小さくなるのはなぜですか? {#why-does-the-auto-increment-id-of-the-later-inserted-data-is-smaller-than-that-of-the-earlier-inserted-data-in-tidb}

TiDB の自動増分 ID 機能は、自動的に増分され一意であることが保証されるだけで、連続的に割り当てられることは保証されません。現在、TiDB は ID をバッチで割り当てています。データが複数の TiDB サーバーに同時に挿入される場合、割り当てられる ID は連続的ではありません。複数のスレッドが複数の`tidb-server`インスタンスに同時にデータを挿入する場合、後で挿入されるデータの自動増分 ID は小さくなる可能性があります。TiDB では、整数フィールドに`AUTO_INCREMENT`を指定できますが、1 つのテーブルに指定できる`AUTO_INCREMENT`フィールドは 1 つだけです。詳細については、 [自動増分ID](/mysql-compatibility.md#auto-increment-id)および[AUTO_INCREMENT属性](/auto-increment.md)を参照してください。

## TiDB の<code>sql_mode</code>を変更するにはどうすればよいですか? {#how-do-i-modify-the-code-sql-mode-code-in-tidb}

TiDB は、SESSION または GLOBAL ベースで[`sql_mode`](/system-variables.md#sql_mode)システム変数を変更することをサポートします。

-   [`GLOBAL`](/sql-statements/sql-statement-set-variable.md)スコープ変数への変更は、クラスターの残りのサーバーに伝播し、再起動後も保持されます。つまり、各 TiDBサーバーで`sql_mode`値を変更する必要はありません。
-   `SESSION`スコープ変数への変更は、現在のクライアント セッションにのみ影響します。サーバーを再起動すると、変更は失われます。

## エラー: <code>java.sql.BatchUpdateException:statement count 5001 exceeds the transaction limitation</code> {#error-code-java-sql-batchupdateexception-statement-count-5001-exceeds-the-transaction-limitation-code-while-using-sqoop-to-write-data-into-tidb-in-batches}

Sqoop では、 `--batch`各バッチで 100 個のステートメントをコミットすることを意味しますが、デフォルトでは各ステートメントに 100 個の SQL ステートメントが含まれます。したがって、100 * 100 = 10000 個の SQL ステートメントとなり、単一の TiDB トランザクションで許可されるステートメントの最大数である 5000 を超えます。

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

-   単一の TiDB トランザクション内のステートメントの制限数を増やすこともできますが、これによりメモリの消費量が増えます。詳細については、 [SQL 文の制限](/tidb-limitations.md#limitations-on-sql-statements)参照してください。

## TiDB には Oracle のフラッシュバック クエリのような機能がありますか? DDL をサポートしていますか? {#does-tidb-have-a-function-like-the-flashback-query-in-oracle-does-it-support-ddl}

はい、サポートしています。また、DDL もサポートしています。詳細については、 [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)参照してください。

## TiDB はデータを削除した後すぐにスペースを解放しますか? {#does-tidb-release-space-immediately-after-deleting-data}

`DELETE` `DROP`操作は`TRUNCATE`もデータを即時に解放しません。7 と`DROP`操作では、TiDB GC (ガベージ コレクション) 時間 (デフォルトでは 10 分) の`TRUNCATE`後にデータが削除され、領域が解放されます。11 `DELETE`操作では、データは削除されますが、圧縮が実行されるまで領域は即時に解放されません。

## データを削除するとクエリ速度が遅くなるのはなぜですか? {#why-does-the-query-speed-get-slow-after-data-is-deleted}

大量のデータを削除すると、無駄なキーが大量に残り、クエリの効率に影響します。この問題を解決するには、 [リージョン結合](/best-practices/massive-regions-best-practices.md#method-3-enable-region-merge)機能を使用できます。詳細については、 [TiDB ベストプラクティスのデータセクションの削除](https://en.pingcap.com/blog/tidb-best-practice/#write)を参照してください。

## データを削除した後、storageスペースの回復に時間がかかる場合はどうすればいいですか? {#what-should-i-do-if-it-is-slow-to-reclaim-storage-space-after-deleting-data}

TiDB はマルチバージョン同時実行制御 (MVCC) を使用するため、古いデータが新しいデータで上書きされると、古いデータは置き換えられず、新しいデータとともに保持されます。タイムスタンプは、データのバージョンを識別するために使用されます。データを削除しても、すぐにスペースが再利用されるわけではありません。同時トランザクションが行の以前のバージョンを参照できるように、ガベージ コレクションは遅延されます。これは、 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (デフォルト: `10m0s` ) システム変数を使用して構成できます。

## <code>SHOW PROCESSLIST</code>システム プロセス ID を表示しますか? {#does-code-show-processlist-code-display-the-system-process-id}

TiDB `SHOW PROCESSLIST`の表示内容は MySQL `SHOW PROCESSLIST`とほぼ同じです。TiDB `SHOW PROCESSLIST`ではシステムプロセス ID は表示されません。表示される ID は現在のセッション ID です。TiDB `SHOW PROCESSLIST`と MySQL `SHOW PROCESSLIST`の違いは次のとおりです。

-   TiDB は分散データベースであるため、 `tidb-server`インスタンスは SQL 文を解析および実行するためのステートレス エンジンです (詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md)を参照してください) `SHOW PROCESSLIST`には、クラスターで実行されているすべてのセッションのリストではなく、ユーザーが MySQL クライアントからログインする`tidb-server`インスタンスで実行されたセッション リストが表示されます。ただし、MySQL はスタンドアロン データベースであり、その`SHOW PROCESSLIST`には MySQL で実行されたすべての SQL 文が表示されます。
-   TiDB の`State`列は、クエリ実行中に継続的に更新されるわけではありません。TiDB は並列クエリをサポートしているため、各ステートメントが一度に複数の*状態*になる可能性があり、単一の値に簡略化することが困難です。

## SQL コミットの実行優先度を制御または変更するにはどうすればよいですか? {#how-to-control-or-change-the-execution-priority-of-sql-commits}

TiDB は、 [グローバル](/system-variables.md#tidb_force_priority)または個々のステートメント ベースでの優先度の変更をサポートしています。優先度には次の意味があります。

-   `HIGH_PRIORITY` : このステートメントの優先度は高いです。つまり、TiDB はこのステートメントを優先し、最初に実行します。

-   `LOW_PRIORITY` : このステートメントの優先度は低いです。つまり、TiDB は実行期間中にこのステートメントの優先度を下げます。

-   `DELAYED` : このステートメントは通常の優先度を持ち、 `tidb_force_priority`の`NO_PRIORITY`設定と同じです。

> **注記：**
>
> v6.6.0 以降、TiDB は[リソース管理](/tidb-resource-control.md)サポートします。この機能を使用すると、異なるリソース グループで異なる優先度の SQL ステートメントを実行できます。これらのリソース グループに適切なクォータと優先度を構成することで、異なる優先度の SQL ステートメントのスケジュール制御を向上させることができます。リソース制御を有効にすると、ステートメントの優先度は無効になります。異なる SQL ステートメントのリソース使用を管理するには、 [リソース管理](/tidb-resource-control.md)使用することをお勧めします。

上記の 2 つのパラメータを TiDB の DML と組み合わせて使用​​することができます。例:

1.  データベースに SQL ステートメントを記述して優先順位を調整します。

    ```sql
    SELECT HIGH_PRIORITY | LOW_PRIORITY | DELAYED COUNT(*) FROM table_name;
    INSERT HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name insert_values;
    DELETE HIGH_PRIORITY | LOW_PRIORITY | DELAYED FROM table_name;
    UPDATE HIGH_PRIORITY | LOW_PRIORITY | DELAYED table_reference SET assignment_list WHERE where_condition;
    REPLACE HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name;
    ```

2.  フル テーブル スキャン ステートメントは、自動的に低い優先度に調整されます。デフォルトでは、 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)は低い優先度です。

## TiDB での<code>auto analyze</code>のトリガー戦略は何ですか? {#what-s-the-trigger-strategy-for-code-auto-analyze-code-in-tidb}

テーブルまたはパーティションテーブルの単一パーティション内の行数が 1000 に達し、テーブルまたはパーティションの比率 (変更された行数 / 現在の行数の合計) が[`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)より大きい場合、 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)ステートメントが自動的にトリガーされます。

`tidb_auto_analyze_ratio`システム変数のデフォルト値は`0.5`で、この機能がデフォルトで有効になっていることを示します。 `tidb_auto_analyze_ratio`の値を[`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio)以上に設定することはお勧めしません (デフォルト値は`0.8` )。そうしないと、オプティマイザーが疑似統計を使用する可能性があります。 TiDB v5.3.0 では[`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)変数が導入され、これを`OFF`に設定すると、統計が古くても疑似統計は使用されません。

`auto analyze`無効にするには、システム変数[`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)を使用します。

## オプティマイザーヒントを使用してオプティマイザーの動作をオーバーライドできますか? {#can-i-use-optimizer-hints-to-override-the-optimizer-behavior}

TiDB は、 [ヒント](/optimizer-hints.md)と[SQL プラン管理](/sql-plan-management.md)を含む、デフォルトのクエリ オプティマイザの動作をオーバーライドする複数の方法をサポートしています。基本的な使用方法は MySQL と似ていますが、TiDB 固有の拡張機能がいくつかあります。

```sql
SELECT column_name FROM table_name USE INDEX（index_name）WHERE where_condition;
```

## DDL実行 {#ddl-execution}

このセクションでは、DDL ステートメントの実行に関連する問題について説明します。DDL 実行の原則の詳細については、 [DDL ステートメントの実行原則とベスト プラクティス](/ddl-introduction.md)を参照してください。

### さまざまな DDL 操作を実行するにはどのくらいの時間がかかりますか? {#how-long-does-it-take-to-perform-various-ddl-operations}

DDL 操作がブロックされておらず、各 TiDBサーバーがスキーマ バージョンを正常に更新でき、DDL 所有者ノードが正常に実行されていると仮定します。この場合、さまざまな DDL 操作の推定時間は次のようになります。

| DDL操作タイプ                                                                                                                                                                   | 予定時刻                              |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------- |
| 再編成DDL、例`MODIFY COLUMN` `ADD INDEX` （再編成タイプのデータ変更）                                                                                                                         | データ量、システム負荷、DDL パラメータ設定によって異なります。 |
| 一般的なDDL `DROP INDEX` `DROP DATABASE`以外のDDLタイプ`ALTER TABLE DROP` `TRUNCATE TABLE`例えば`CREATE DATABASE` （ `CREATE TABLE`データのみ`ALTER TABLE ADD` `DROP TABLE` 、 `MODIFY COLUMN` | 約1秒                               |

> **注記：**
>
> 上記は作業にかかる推定時間であり、実際の時間は異なる場合があります。

### DDL実行が遅い理由 {#possible-reasons-why-ddl-execution-is-slow}

-   ユーザー セッションで、DDL ステートメントの前に非自動コミット DML ステートメントがあり、非自動コミット DML ステートメントのコミット操作が遅い場合、DDL ステートメントの実行が遅くなります。つまり、TiDB は DDL ステートメントを実行する前に、コミットされていない DML ステートメントをコミットします。

-   複数の DDL ステートメントが同時に実行される場合、キューで待機する必要がある可能性があるため、後の DDL ステートメントの実行が遅くなる可能性があります。キューのシナリオには次のものがあります。

    -   同じタイプの DDL ステートメントをキューに入れる必要があります。たとえば、 `CREATE TABLE`と`CREATE DATABASE`どちらも一般的な DDL ステートメントであるため、両方の操作を同時に実行する場合はキューに入れる必要があります。TiDB v6.2.0 以降では、並列 DDL ステートメントがサポートされていますが、DDL 実行で TiDB コンピューティング リソースが過度に使用されるのを避けるために、同時実行の制限もあります。DDL が同時実行の制限を超えると、キューに入れられます。
    -   同じテーブルに対して実行される DDL 操作には依存関係があります。後の DDL ステートメントは、前の DDL 操作が完了するまで待機する必要があります。

-   クラスターが正常に起動された後、DDL モジュールが DDL 所有者を選出するため、最初の DDL 操作の実行時間が比較的長くなる可能性があります。

-   TiDB が終了し、TiDB が PD と正常に通信できなくなります (電源オフの状況を含む)。または、TiDB が`kill -9`コマンドによって終了し、TiDB が PD から登録データをタイムリーにクリアできなくなります。

-   クラスター内の特定の TiDB ノードと PD または TiKV の間で通信の問題が発生し、TiDB が最新のバージョン情報を時間内に取得できなくなります。

### <code>Information schema is changed</code>エラーの原因は何ですか? {#what-triggers-the-code-information-schema-is-changed-code-error}

SQL ステートメントを実行すると、TiDB は分離レベルに基づいてオブジェクトのスキーマ バージョンを決定し、それに応じて SQL ステートメントを処理します。TiDB は、オンラインの非同期 DDL 変更もサポートします。DML ステートメントを実行すると、同時に実行される DDL ステートメントが存在する可能性があり、各 SQL ステートメントが同じスキーマで実行されるようにする必要があります。したがって、DML を実行するときに DDL 操作が進行中の場合、TiDB は`Information schema is changed`エラーを報告する可能性があります。

v6.4.0 以降、TiDB は[メタデータロックメカニズム](/metadata-lock.md)を実装しました。これにより、DML ステートメントと DDL スキーマ変更の調整された実行が可能になり、ほとんどの`Information schema is changed`エラーを回避できます。

このエラー報告には、まだいくつかの原因があります。

-   原因 1: DML 操作に関係するテーブルの一部は、進行中の DDL 操作に関係するテーブルと同じです。進行中の DDL 操作を確認するには、 `ADMIN SHOW DDL`ステートメントを使用します。
-   原因 2: DML 操作が長時間にわたって実行されます。この期間中に多数の DDL ステートメントが実行され、1024 を超える`schema`バージョンの変更が発生します。このデフォルト値は、 `tidb_max_delta_schema_count`変数を変更することで変更できます。
-   原因 3: DML 要求を受け入れる TiDBサーバーが`schema information`ロードできません (TiDB と PD または TiKV 間の接続障害が原因と考えられます)。この期間中に多数の DDL ステートメントが実行され、100 を超える`schema`バージョンの変更が発生します。
-   原因 4: TiDB が再起動し、最初の DDL 操作が実行される前に、DML 操作が実行され、最初の DDL 操作に遭遇します (つまり、最初の DDL 操作が実行される前に、DML に対応するトランザクションが開始されます。そして、最初の`schema`バージョンの DDL が変更された後、DML に対応するトランザクションがコミットされます)。この DML 操作によってこのエラーが報告されます。

上記の原因のうち、原因 1 のみがテーブルに関連しています。原因 1 と原因 2 は、関連する DML 操作が失敗後に再試行されるため、アプリケーションには影響しません。原因 3 については、TiDB と TiKV/PD 間のネットワークを確認する必要があります。

> **注記：**
>
> -   現在、TiDB はバージョン`schema`変更をすべてキャッシュしません。
> -   各 DDL 操作では、 `schema`バージョンの変更の数は、対応する`schema state`バージョンの変更の数と同じです。
> -   異なる DDL 操作では、バージョン`schema`の変更の数が異なります。たとえば、 `CREATE TABLE`ステートメントではバージョン`schema`変更が 1 つ発生し、 `ADD COLUMN`ステートメントではバージョン 5 の変更が 4 つ発生します。

### 「情報スキーマが古くなっています」というエラーの原因は何ですか? {#what-are-the-causes-of-the-information-schema-is-out-of-date-error}

TiDB v6.5.0 より前では、DML ステートメントを実行するときに、TiDB が DDL リース (デフォルトでは 45 秒) 内に最新のスキーマをロードできない場合、 `Information schema is out of date`エラーが発生する可能性があります。考えられる原因は次のとおりです。

-   この DML を実行した TiDB インスタンスが強制終了され、この DML ステートメントに対応するトランザクションの実行に DDL リースよりも長い時間がかかりました。トランザクションがコミットされたときにエラーが発生しました。
-   この DML ステートメントの実行中に、TiDB は PD または TiKV に接続できませんでした。その結果、TiDB は DDL リース内でスキーマをロードできなかったか、キープアライブ設定により PD から切断されました。

### 高い同時実行性で DDL ステートメントを実行するとエラーが報告されますか? {#error-is-reported-when-executing-ddl-statements-under-high-concurrency}

高い同時実行性で DDL ステートメント (バッチでのテーブルの作成など) を実行すると、同時実行中のキーの競合により、これらのステートメントのごく一部が失敗する可能性があります。

同時実行 DDL ステートメントの数を 20 未満に抑えることをお勧めします。それ以外の場合は、クライアントから失敗したステートメントを再試行する必要があります。

### DDL 実行がブロックされるのはなぜですか? {#why-is-ddl-execution-blocked}

TiDB v6.2.0 より前のバージョンでは、TiDB は DDL ステートメントのタイプに基づいて、DDL ステートメントを 2 つの先入先出キューに割り当てます。具体的には、Reorg DDL は Reorg キューに、一般 DDL は一般キューに送られます。先入先出の制限と、同じテーブルで DDL ステートメントを連続して実行する必要があるため、実行中に複数の DDL ステートメントがブロックされる可能性があります。

たとえば、次の DDL ステートメントを考えてみましょう。

-   DDL1: `CREATE INDEX idx on t(a int);`
-   DDL2: `ALTER TABLE t ADD COLUMN b int;`
-   DDL3: `CREATE TABLE t1(a int);`

先入先出キューの制限により、DDL 3 は DDL 2 の実行を待機する必要があります。また、同じテーブル上の DDL ステートメントはシリアルで実行する必要があるため、DDL 2 は DDL 1 の実行を待機する必要があります。したがって、異なるテーブルで操作する場合でも、DDL 3 は DDL 1 が最初に実行されるまで待機する必要があります。

TiDB v6.2.0 以降、TiDB DDL モジュールは並行フレームワークを使用します。並行フレームワークでは、先入先出キューの制限がなくなりました。代わりに、TiDB はすべての DDL タスクから実行可能な DDL タスクを選択します。さらに、Reorg ワーカーの数がノードあたり約`CPU/4`に拡張されました。これにより、TiDB は並行フレームワークで複数のテーブルのインデックスを同時に構築できます。

クラスターが新しいクラスターであるか、以前のバージョンからアップグレードされたクラスターであるかに関係なく、TiDB は TiDB v6.2 以降のバージョンの同時実行フレームワークを自動的に使用します。手動で調整する必要はありません。

### DDL実行が停止した原因を特定する {#identify-the-cause-of-stuck-ddl-execution}

1.  DDL ステートメントの実行が遅くなるその他の理由を排除します。
2.  DDL 所有者ノードを識別するには、次のいずれかの方法を使用します。
    -   現在のクラスターの所有者を取得するには`curl http://{TiDBIP}:10080/info/all`使用します。
    -   監視ダッシュボード**DDL** &gt; **DDL META OPM**から特定の期間の所有者をビュー。

-   所有者が存在しない場合は、次を使用して所有者の選択を手動でトリガーしてみてください: `curl -X POST http://{TiDBIP}:10080/ddl/owner/resign` 。
-   所有者が存在する場合は、Goroutine スタックをエクスポートし、スタックしている可能性のある場所を確認します。

## SQL最適化 {#sql-optimization}

### TiDB実行プランの説明 {#tidb-execution-plan-description}

[クエリ実行プランを理解する](/explain-overview.md)参照。

### 統計収集 {#statistics-collection}

[統計入門](/statistics.md)参照。

### <code>select count(1)</code>を最適化するにはどうすればいいですか? {#how-to-optimize-code-select-count-1-code}

`count(1)`文はテーブル内の行の総数をカウントします。同時実行度を向上させると、速度が大幅に向上します。同時実行性を変更するには、 [`tidb_distsql_scan_concurrency`ドキュメント](/system-variables.md#tidb_distsql_scan_concurrency)を参照してください。ただし、CPU と I/O リソースにも依存します。TiDB はすべてのクエリで TiKV にアクセスします。データ量が少ない場合、MySQL はすべてメモリ内にあり、TiDB はネットワーク アクセスを実行する必要があります。

推奨事項:

-   ハードウェア構成を改善します。1 [ソフトウェアおよびハードウェアの要件](/hardware-and-software-requirements.md)参照してください。
-   同時実行性を向上させます。デフォルト値は 10 です。これを 50 に向上させて試すことができます。ただし、通常はデフォルト値の 2 ～ 4 倍の向上が得られます。
-   大量のデータの場合は`count`テストします。
-   TiKV 構成を最適化します。1 と[TiKV メモリのパフォーマンスを調整する](/tune-tikv-memory-performance.md) [TiKV スレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md)参照してください。
-   [コプロセッサーキャッシュ](/coprocessor-cache.md)有効にします。

### 現在の DDL ジョブの進行状況を表示するにはどうすればいいですか? {#how-to-view-the-progress-of-the-current-ddl-job}

`ADMIN SHOW DDL`使用すると、現在の DDL ジョブの進行状況を表示できます。操作は次のとおりです。

```sql
ADMIN SHOW DDL;
```

    *************************** 1. row ***************************
      SCHEMA_VER: 140
           OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
    RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
         SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc

上記の結果から、 `ADD INDEX`の操作が現在処理中であることがわかります。また、 `RUNNING_JOBS`列目の`RowCount`フィールドから、 `ADD INDEX`番目の操作によって 77312 行のインデックスが追加されたことがわかります。

### DDL ジョブを表示するにはどうすればいいですか? {#how-to-view-the-ddl-job}

-   `ADMIN SHOW DDL` : 実行中のDDLジョブを表示する
-   `ADMIN SHOW DDL JOBS` : 現在の DDL ジョブ キュー内のすべての結果 (実行中および実行待ちのタスクを含む) と、完了した DDL ジョブ キューの最後の 10 件の結果を表示します。
-   `ADMIN SHOW DDL JOBS QUERIES 'job_id' [, 'job_id'] ...` : `job_id`に対応する DDL タスクの元の SQL ステートメントを表示します。4 `job_id`実行中の DDL ジョブと DDL 履歴ジョブ キュー内の最後の 10 件の結果のみを検索します。

### TiDB は CBO (コストベース最適化) をサポートしていますか? サポートしている場合、どの程度サポートしていますか? {#does-tidb-support-cbo-cost-based-optimization-if-yes-to-what-extent}

はい。TiDB はコストベースのオプティマイザーを使用します。コスト モデルと統計は常に最適化されます。TiDB はハッシュ結合やソートマージ結合などの結合アルゴリズムもサポートしています。

### テーブルに対して<code>analyze</code>を実行する必要があるかどうかを判断するにはどうすればよいでしょうか? {#how-to-determine-whether-i-need-to-execute-code-analyze-code-on-a-table}

`SHOW STATS_HEALTHY`を使用して`Healthy`フィールドをビュー、通常、フィールド値が 60 より小さい場合はテーブルで`ANALYZE`を実行する必要があります。

### クエリ プランがツリーとして提示される場合の ID ルールは何ですか? このツリーの実行順序は何ですか? {#what-is-the-id-rule-when-a-query-plan-is-presented-as-a-tree-what-is-the-execution-order-for-this-tree}

これらの ID にはルールはありませんが、ID はユニークです。ID が生成されるとカウンターが動作し、プランが 1 つ生成されるたびに 1 が追加されます。実行順序は ID とは関係ありません。クエリ プラン全体はツリーになっており、実行プロセスはルート ノードから開始され、上位レベルにデータが連続的に返されます。クエリ プランの詳細については、 [TiDBクエリ実行プランを理解する](/explain-overview.md)参照してください。

### TiDB クエリ プランでは、 <code>cop</code>タスクは同じルートにあります。それらは同時に実行されますか? {#in-the-tidb-query-plan-code-cop-code-tasks-are-in-the-same-root-are-they-executed-concurrently}

現在、TiDB のコンピューティング タスクは、タスク`cop task`と`root task` 2 つの異なるタイプに属しています。

`cop task`分散実行のために KV エンドにプッシュダウンされるコンピューティング タスクです。2 `root task` TiDB エンドでの単一ポイント実行のためのコンピューティング タスクです。

通常、 `root task`の入力データは`cop task`から来ます。 `root task`データを処理しているとき、 TiKV の`cop task`同時にデータを処理し、 TiDB の`root task`のプルを待機できます。 したがって、 `cop`タスクは`root task`と同時に実行されていると見なすことができますが、それらのデータには上流と下流の関係があります。 実行プロセス中、それらはある時間内に同時に実行されます。 たとえば、最初の`cop task` [100, 200] のデータを処理し、2 番目の`cop task` [1, 100] のデータを処理します。 詳細については、 [TiDBクエリプランを理解する](/explain-overview.md)を参照してください。

## データベースの最適化 {#database-optimization}

### TiDBオプションを編集する {#edit-tidb-options}

[TiDB コマンド オプション](/command-line-flags-for-tidb-configuration.md)参照。

### ホットスポットの問題を回避し、負荷分散を実現するにはどうすればよいでしょうか? TiDB ではホット パーティションまたは範囲が問題になりますか? {#how-to-avoid-hotspot-issues-and-achieve-load-balancing-is-hot-partition-or-range-an-issue-in-tidb}

ホットスポットの原因となるシナリオについては、 [一般的な鍋](/troubleshoot-hot-spot-issues.md#common-hotspots)を参照してください。次の TiDB 機能は、ホットスポットの問題を解決するために設計されています。

-   [`SHARD_ROW_ID_BITS`](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)属性。この属性を設定すると、行 ID が分散されて複数の領域に書き込まれるため、書き込みホットスポットの問題が軽減されます。
-   [`AUTO_RANDOM`](/troubleshoot-hot-spot-issues.md#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)属性は、自動インクリメント主キーによってもたらされるホットスポットを解決するのに役立ちます。
-   [コプロセッサーキャッシュ](/coprocessor-cache.md) 、小さなテーブル上の読み取りホットスポットの場合。
-   [ロードベーススプリット](/configure-load-base-split.md) 、小さなテーブルの全テーブルスキャンなど、リージョン間の不均衡なアクセスによって発生するホットスポットの場合。
-   [キャッシュされたテーブル](/cached-tables.md) 、頻繁にアクセスされるが、めったに更新されない小さなホットスポット テーブルの場合。

ホットスポットによってパフォーマンスの問題が発生した場合は、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照して解決してください。

### TiKV のパフォーマンスを調整する {#tune-tikv-performance}

[TiKV スレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md)と[TiKV メモリのパフォーマンスを調整する](/tune-tikv-memory-performance.md)参照してください。
