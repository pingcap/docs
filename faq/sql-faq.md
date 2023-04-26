---
title: SQL FAQs
summary: Learn about the FAQs related to TiDB SQL.
---

# SQL に関するよくある質問 {#sql-faqs}

このドキュメントは、TiDB での SQL 操作に関する FAQ をまとめたものです。

## TiDB はセカンダリ キーをサポートしていますか? {#does-tidb-support-the-secondary-key}

はい。一意の[副次索引](/develop/dev-guide-create-secondary-indexes.md)を持つ非主キー列に[`NOT NULL`制約](/constraints.md#not-null)を持つことができます。この場合、列は 2 次キーとして機能します。

## 大きなテーブルで DDL 操作を実行するとき、TiDB はどのように動作しますか? {#how-does-tidb-perform-when-executing-ddl-operations-on-a-large-table}

通常、大きなテーブルに対する TiDB の DDL 操作は問題になりません。 TiDB はオンライン DDL 操作をサポートしており、これらの DDL 操作は DML 操作をブロックしません。

列の追加、列の削除、インデックスの削除などの一部の DDL 操作では、TiDB はこれらの操作をすばやく実行できます。

インデックスの追加などの重い DDL 操作の場合、TiDB はデータをバックフィルする必要があります。これには (テーブルのサイズによっては) 時間がかかり、追加のリソースが消費されます。オンライン トラフィックへの影響は調整可能です。 TiDB は複数のスレッドでバックフィルを実行でき、消費されるリソースは次のシステム変数で設定できます。

-   [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
-   [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
-   [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
-   [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

## 適切なクエリ プランを選択する方法ヒントを使用する必要がありますか?または、ヒントを使用できますか？ {#how-to-choose-the-right-query-plan-do-i-need-to-use-hints-or-can-i-use-hints}

TiDB には、コストベースのオプティマイザが含まれています。ほとんどの場合、オプティマイザーが最適なクエリ プランを選択します。オプティマイザがうまく機能しない場合でも、 [オプティマイザーのヒント](/optimizer-hints.md)使用してオプティマイザに介入できます。

さらに、 [SQL バインディング](/sql-plan-management.md#sql-binding)を使用して、特定の SQL ステートメントのクエリ プランを修正することもできます。

## 特定の SQL ステートメントの実行を防ぐ方法は? {#how-to-prevent-the-execution-of-a-particular-sql-statement}

[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)ヒントを使用して[SQL バインディング](/sql-plan-management.md#sql-binding)を作成し、特定のステートメントの実行時間を小さな値 (1 ミリ秒など) に制限できます。このように、ステートメントはしきい値によって自動的に終了します。

たとえば、 `SELECT * FROM t1, t2 WHERE t1.id = t2.id`の実行を防ぐには、次の SQL バインディングを使用してステートメントの実行時間を 1 ミリ秒に制限します。

```sql
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ MAX_EXECUTION_TIME(1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **ノート：**
>
> `MAX_EXECUTION_TIME`の精度は約 100 ミリ秒です。 TiDB が SQL ステートメントを終了する前に、TiKV のタスクが開始される場合があります。このような場合に TiKV リソースの消費を抑えるには、 [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540) ～ `ON`を設定することをお勧めします。

この SQL バインドを削除すると、制限が削除されます。

```sql
DROP GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

## TiDB と互換性のある MySQL 変数は何ですか? {#what-are-the-mysql-variables-that-tidb-is-compatible-with}

[システム変数](/system-variables.md)を参照してください。

## <code>ORDER BY</code>省略した場合、結果の順序が MySQL とは異なります {#the-order-of-results-is-different-from-mysql-when-code-order-by-code-is-omitted}

これはバグではありません。レコードのデフォルトの順序は、さまざまな状況に依存し、一貫性は保証されません。

クエリは単一のスレッドで実行されるため、MySQL での結果の順序は安定しているように見える場合があります。ただし、新しいバージョンにアップグレードすると、クエリ プランが変更されることがよくあります。結果の順序が必要な場合は常に`ORDER BY`を使用することをお勧めします。

参考文献は[ISO/IEC 9075:1992、データベース言語 SQL - 1992 年 7 月 30 日](http://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt)にあり、次のように述べられています。

> `<order by clause>`が指定されていない場合、 `<cursor specification>`で指定されたテーブルは T であり、T 内の行の順序は実装に依存します。

次の 2 つのクエリでは、両方の結果が有効であると見なされます。

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

`ORDER BY`で使用される列のリストが一意でない場合、ステートメントも非決定論的と見なされます。次の例では、列`a`に重複した値があります。したがって、 `ORDER BY a, b`だけが決定論的に保証されます。

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

次のステートメントでは、列`a`の順序は保証されますが、列`b`の順序は保証されません。

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

TiDB では、システム変数[`tidb_enable_ordered_result_mode`](/system-variables.md#tidb_enable_ordered_result_mode)を使用して、最終出力結果を自動的にソートすることもできます。

## TiDB は<code>SELECT FOR UPDATE</code>をサポートしていますか? {#does-tidb-support-code-select-for-update-code}

はい。悲観的ロック (TiDB v3.0.8 以降のデフォルト) を使用する場合、 `SELECT FOR UPDATE`回の実行は MySQL と同様に動作します。

楽観的ロックを使用する場合、 `SELECT FOR UPDATE`はトランザクションの開始時にデータをロックしませんが、トランザクションのコミット時に競合をチェックします。チェックで競合が明らかになった場合、コミットしているトランザクションはロールバックします。

詳細については、 [`SELECT`構文要素の説明](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements)を参照してください。

## TiDB のコーデックは、UTF-8 文字列が memcomparable であることを保証できますか?キーが UTF-8 をサポートする必要がある場合、コーディングに関する提案はありますか? {#can-the-codec-of-tidb-guarantee-that-the-utf-8-string-is-memcomparable-is-there-any-coding-suggestion-if-our-key-needs-to-support-utf-8}

TiDB はデフォルトで UTF-8 文字セットを使用し、現在は UTF-8 のみをサポートしています。 TiDB の文字列は memcomparable 形式を使用します。

## トランザクション内のステートメントの最大数はいくつですか? {#what-is-the-maximum-number-of-statements-in-a-transaction}

トランザクション内のステートメントの最大数は、デフォルトで 5000 です。

楽観的トランザクション モードでは、トランザクションの再試行が有効に[`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit)ている場合、デフォルトの上限は 5000 です。1 パラメータを使用して制限を調整できます。

## 後で挿入されたデータの自動インクリメント ID が、以前に TiDB に挿入されたデータよりも小さいのはなぜですか? {#why-does-the-auto-increment-id-of-the-later-inserted-data-is-smaller-than-that-of-the-earlier-inserted-data-in-tidb}

TiDB の自動インクリメント ID 機能は、自動的にインクリメンタルで一意であることのみが保証されていますが、順次割り当てられることは保証されていません。現在、TiDB は ID をバッチで割り当てています。データが複数の TiDB サーバーに同時に挿入される場合、割り当てられる ID は連続しません。複数のスレッドが同時に複数の`tidb-server`インスタンスにデータを挿入すると、後で挿入されるデータの自動インクリメント ID が小さくなることがあります。 TiDB では、整数フィールドに`AUTO_INCREMENT`を指定できますが、1 つのテーブルに`AUTO_INCREMENT`フィールドを 1 つだけ指定できます。詳細については、 [自動インクリメント ID](/mysql-compatibility.md#auto-increment-id)および[AUTO_INCREMENT 属性](/auto-increment.md)を参照してください。

## TiDB で<code>sql_mode</code>を変更するにはどうすればよいですか? {#how-do-i-modify-the-code-sql-mode-code-in-tidb}

TiDB は、SESSION または GLOBAL ベースでの[`sql_mode`](/system-variables.md#sql_mode)システム変数の変更をサポートしています。

-   [`GLOBAL`](/sql-statements/sql-statement-set-variable.md)スコープ変数への変更は、クラスターの残りのサーバーに伝達され、再起動後も保持されます。これは、各 TiDBサーバーで`sql_mode`値を変更する必要がないことを意味します。
-   `SESSION`のスコープ変数への変更は、現在のクライアント セッションにのみ影響します。サーバーを再起動すると、変更が失われます。

## エラー: <code>java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation</code> {#error-code-java-sql-batchupdateexecption-statement-count-5001-exceeds-the-transaction-limitation-code-while-using-sqoop-to-write-data-into-tidb-in-batches}

Sqoop では、 `--batch`各バッチで 100 個のステートメントをコミットすることを意味しますが、デフォルトでは各ステートメントには 100 個の SQL ステートメントが含まれます。したがって、100 * 100 = 10000 SQL ステートメントとなり、1 つの TiDB トランザクションで許可されるステートメントの最大数である 5000 を超えます。

2 つのソリューション:

-   次のように`-Dsqoop.export.records.per.statement=10`オプションを追加します。

    {{< copyable "" >}}

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

-   1 つの TiDB トランザクション内のステートメントの制限数を増やすこともできますが、これはより多くのメモリを消費します。詳細については、 [SQL ステートメントの制限](/tidb-limitations.md#limitations-on-sql-statements)を参照してください。

## TiDB には Oracle の Flashback Query のような機能がありますか? DDLをサポートしていますか? {#does-tidb-have-a-function-like-the-flashback-query-in-oracle-does-it-support-ddl}

はい、そうです。また、DDLもサポートしています。詳細については、 [`AS OF TIMESTAMP`句を使用した履歴データの読み取り](/as-of-timestamp.md)を参照してください。

## TiDB はデータを削除した直後にスペースを解放しますか? {#does-tidb-release-space-immediately-after-deleting-data}

`DELETE` 、 `TRUNCATE` 、および`DROP`操作のいずれも、データをすぐに解放しません。 `TRUNCATE`と`DROP`の操作では、TiDB GC (ガベージ コレクション) 時間 (既定では 10 分) の後、データが削除され、スペースが解放されます。 `DELETE`の操作では、データは削除されますが、圧縮が実行されるまでスペースはすぐには解放されません。

## データが削除された後、クエリの速度が遅くなるのはなぜですか? {#why-does-the-query-speed-get-slow-after-data-is-deleted}

大量のデータを削除すると、多くの不要なキーが残り、クエリの効率に影響します。この問題を解決するには、 [リージョンマージ](/best-practices/massive-regions-best-practices.md#method-3-enable-region-merge)機能を使用できます。詳細は[TiDB ベスト プラクティスのデータ セクションの削除](https://en.pingcap.com/blog/tidb-best-practice/#write)を参照してください。

## データを削除した後、storageスペースを再利用するのが遅い場合はどうすればよいですか? {#what-should-i-do-if-it-is-slow-to-reclaim-storage-space-after-deleting-data}

TiDB はマルチバージョン同時実行制御 (MVCC) を使用するため、古いデータが新しいデータで上書きされる場合、古いデータは置き換えられず、新しいデータと共に保持されます。タイムスタンプは、データのバージョンを識別するために使用されます。データを削除しても、すぐにスペースが再利用されるわけではありません。同時トランザクションが以前のバージョンの行を参照できるように、ガベージ コレクションが遅延されます。これは[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (デフォルト: `10m0s` ) システム変数で設定できます。

## <code>SHOW PROCESSLIST</code>システム プロセス ID を表示しますか? {#does-code-show-processlist-code-display-the-system-process-id}

TiDB `SHOW PROCESSLIST`の表示内容は MySQL `SHOW PROCESSLIST`とほぼ同じです。 TiDB `SHOW PROCESSLIST`はシステム プロセス ID を表示しません。表示される ID は、現在のセッション ID です。 TiDB `SHOW PROCESSLIST`と MySQL `SHOW PROCESSLIST`の違いは次のとおりです。

-   TiDB は分散データベースであるため、 `tidb-server`のインスタンスは SQL ステートメントを解析および実行するためのステートレス エンジンです (詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md)参照してください)。 `SHOW PROCESSLIST`クラスターで実行されているすべてのセッションのリストではなく、ユーザーが MySQL クライアントからログインする`tidb-server`インスタンスで実行されたセッションのリストを表示します。しかし、MySQL はスタンドアロン データベースであり、その`SHOW PROCESSLIST`には MySQL で実行されたすべての SQL ステートメントが表示されます。
-   TiDB の`State`列は、クエリの実行中に継続的に更新されるわけではありません。 TiDB は並列クエリをサポートしているため、各ステートメントは一度に複数の*状態*になる可能性があるため、単一の値に単純化することは困難です。

## SQLコミットの実行優先度を制御または変更する方法は? {#how-to-control-or-change-the-execution-priority-of-sql-commits}

TiDB は、 [グローバル](/system-variables.md#tidb_force_priority)または個々のステートメント単位での優先度の変更をサポートしています。プライオリティには次の意味があります。

-   `HIGH_PRIORITY` : このステートメントの優先度が高い。つまり、TiDB はこのステートメントに優先順位を与え、最初に実行します。

-   `LOW_PRIORITY` : このステートメントの優先度は低いです。つまり、実行期間中、TiDB はこのステートメントの優先度を下げます。

-   `DELAYED` : このステートメントは通常の優先度を持ち、 `tidb_force_priority`に対する`NO_PRIORITY`設定と同じです。

上記の 2 つのパラメーターを TiDB の DML と組み合わせて使用できます。例えば：

1.  データベースに SQL ステートメントを記述して、優先順位を調整します。

    {{< copyable "" >}}

    ```sql
    SELECT HIGH_PRIORITY | LOW_PRIORITY | DELAYED COUNT(*) FROM table_name;
    INSERT HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name insert_values;
    DELETE HIGH_PRIORITY | LOW_PRIORITY | DELAYED FROM table_name;
    UPDATE HIGH_PRIORITY | LOW_PRIORITY | DELAYED table_reference SET assignment_list WHERE where_condition;
    REPLACE HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name;
    ```

2.  フル テーブル スキャン ステートメントは、自動的に低い優先度に調整されます。デフォルトでは、 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)優先度は低くなります。

## TiDB での<code>auto analyze</code>のトリガー戦略は何ですか? {#what-s-the-trigger-strategy-for-code-auto-analyze-code-in-tidb}

トリガー戦略: `auto analyze` 、新しいテーブルの行数が 1000 に達し、このテーブルに 1 分間書き込み操作がない場合に自動的にトリガーされます。

比率 (変更された行数 / 現在の合計行数) が`tidb_auto_analyze_ratio`より大きい場合、 `analyze`ステートメントが自動的にトリガーされます。デフォルト値の`tidb_auto_analyze_ratio`は 0.5 で、この機能がデフォルトで有効になっていることを示します。安全性を確保するために、この機能が有効になっているときの最小値は 0.3 であり、デフォルト値が 0.8 である`pseudo-estimate-ratio`よりも小さくする必要があります。そうしないと、一定期間疑似統計が使用されます。 `tidb_auto_analyze_ratio` ～ 0.5 に設定することをお勧めします。

auto analyzeを無効にするには、システム変数`tidb_enable_auto_analyze`を使用します。

## オプティマイザーのヒントを使用してオプティマイザーの動作をオーバーライドできますか? {#can-i-use-optimizer-hints-to-override-the-optimizer-behavior}

TiDB は、 [ヒント](/optimizer-hints.md)や[SQL計画管理](/sql-plan-management.md)など、デフォルトのクエリ オプティマイザーの動作をオーバーライドする複数の方法をサポートしています。基本的な使用法は MySQL に似ていますが、TiDB 固有の拡張機能がいくつかあります。

```sql
SELECT column_name FROM table_name USE INDEX（index_name）WHERE where_condition;
```

## DDL の実行 {#ddl-execution}

このセクションでは、DDL ステートメントの実行に関連する問題をリストします。 DDL 実行の原則に関する詳細な説明については、 [DDL ステートメントの実行原則とベスト プラクティス](/ddl-introduction.md)を参照してください。

### さまざまな DDL 操作を実行するのにどのくらいの時間がかかりますか? {#how-long-does-it-take-to-perform-various-ddl-operations}

DDL 操作がブロックされておらず、各 TiDBサーバーがスキーマ バージョンを正常に更新でき、DDL 所有者ノードが正常に動作しているとします。この場合、さまざまな DDL 操作の推定時間は次のようになります。

| DDL操作タイプ                                                                                                                                                                                                    | 予定時刻                               |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------- |
| `ADD INDEX` 、 `MODIFY COLUMN`などの再編成 DDL (再編成タイプのデータ変更)                                                                                                                                                      | データ量、システム負荷、DDL パラメータの設定によって異なります。 |
| `CREATE DATABASE` 、 `CREATE TABLE` 、 `DROP DATABASE` 、 `DROP TABLE` 、 `TRUNCATE TABLE` 、 `ALTER TABLE ADD` 、 `ALTER TABLE DROP` 、 `MODIFY COLUMN` (メタデータの変更のみ)、 `DROP INDEX`などの一般的な DDL (Reorg 以外の DDL タイプ) | 約1秒                                |

> **ノート：**
>
> 上記は施術時間の目安です。実際の時間は異なる場合があります。

### DDL の実行が遅い考えられる理由 {#possible-reasons-why-ddl-execution-is-slow}

-   ユーザー セッションで、DDL ステートメントの前に非自動コミット DML ステートメントがあり、非自動コミット DML ステートメントのコミット操作が遅いと、DDL ステートメントの実行が遅くなります。つまり、TiDB は DDL ステートメントを実行する前に、コミットされていない DML ステートメントをコミットします。

-   複数の DDL ステートメントが一緒に実行されると、後の DDL ステートメントの実行は、キューで待機する必要がある可能性があるため、遅くなる可能性があります。キューイングのシナリオは次のとおりです。

    -   同じタイプの DDL ステートメントをキューに入れる必要があります。たとえば、 `CREATE TABLE`と`CREATE DATABASE`はどちらも一般的な DDL ステートメントであるため、両方の操作を同時に実行する場合は、キューに入れる必要があります。 TiDB v6.2.0 以降では、並列 DDL ステートメントがサポートされていますが、あまりにも多くの TiDB コンピューティング リソースを使用して DDL を実行することを避けるために、同時実行制限もあります。 DDL が同時実行制限を超えると、キューイングが発生します。
    -   同じテーブルに対して実行される DDL 操作には、それらの間に依存関係があります。後の DDL ステートメントは、前の DDL 操作が完了するまで待機する必要があります。

-   クラスターが正常に開始された後、DDL モジュールが DDL 所有者を選択しているため、最初の DDL 操作の実行時間が比較的長くなる場合があります。

-   TiDB が終了し、TiDB が PD と正常に通信できなくなります (電源オフ状態を含む)。または、TiDB は`kill -9`コマンドによって終了されます。これにより、TiDB は PD から登録データをタイムリーにクリアしません。

-   クラスタ内の特定の TiDB ノードと PD または TiKV との間で通信障害が発生し、TiDB が最新のバージョン情報を取得できなくなります。

### 何が<code>Information schema is changed</code>エラーを引き起こしますか? {#what-triggers-the-code-information-schema-is-changed-code-error}

SQL ステートメントを実行すると、TiDB は分離レベルに基づいてオブジェクトのスキーマ バージョンを判断し、それに応じて SQL ステートメントを処理します。 TiDB は、オンラインの非同期 DDL 変更もサポートしています。 DML ステートメントを実行すると、同時に実行される DDL ステートメントが存在する可能性があり、各 SQL ステートメントが同じスキーマで実行されるようにする必要があります。したがって、DML の実行時に DDL 操作が進行中の場合、TiDB は`Information schema is changed`エラーを報告することがあります。

v6.4.0 から、TiDB は[メタデータ ロック メカニズム](/metadata-lock.md)を実装しました。これにより、DML ステートメントと DDL スキーマ変更の調整された実行が可能になり、ほとんどの`Information schema is changed`エラーが回避されます。

現在、このエラー報告にはまだいくつかの原因があります。

-   原因 1: DML 操作に含まれるいくつかのテーブルは、進行中の DDL 操作に含まれるテーブルと同じです。進行中の DDL 操作を確認するには、 `ADMIN SHOW DDL`ステートメントを使用します。
-   原因 2: DML 操作が長時間続いています。この期間中、多くの DDL ステートメントが実行され、1024 を`schema`バージョン変更が発生しました。このデフォルト値は、変数`tidb_max_delta_schema_count`を変更することで変更できます。
-   原因 3: DML 要求を受け入れる TiDBサーバーが長時間`schema information`をロードできません (TiDB と PD または TiKV の間の接続障害が原因である可能性があります)。この期間中、多くの DDL ステートメントが実行され、 `schema`以上のバージョン変更が発生しました。
-   原因 4: TiDB の再起動後、最初の DDL 操作が実行される前に、DML 操作が実行され、最初の DDL 操作が発生します (つまり、最初の DDL 操作が実行される前に、DML に対応するトランザクションが開始されます。 DDL の最初の`schema`バージョンが変更され、DML に対応するトランザクションがコミットされます)、この DML 操作はこのエラーを報告します。

上記の原因のうち、原因 1 のみがテーブルに関連しています。関連する DML 操作は失敗後に再試行されるため、原因 1 と原因 2 はアプリケーションに影響しません。原因 3 については、TiDB と TiKV/PD 間のネットワークを確認する必要があります。

> **ノート：**
>
> -   現在、TiDB は`schema`のバージョン変更をすべてキャッシュするわけではありません。
> -   DDL 操作ごとに、 `schema`バージョン変更の数は、対応する`schema state`バージョン変更の数と同じです。
> -   DDL 操作が異なれば、 `schema`バージョン変更の数も異なります。たとえば、 `CREATE TABLE`ステートメントでは`schema`バージョン変更が 1 回行われますが、 `ADD COLUMN`ステートメントでは 4 回のバージョン変更が行われます。

### 「情報スキーマが古くなっています」エラーの原因は何ですか? {#what-are-the-causes-of-the-information-schema-is-out-of-date-error}

TiDB v6.5.0 より前では、DML ステートメントを実行するときに、TiDB が DDL リース (デフォルトでは 45 秒) 内で最新のスキーマをロードできなかった場合、 `Information schema is out of date`エラーが発生する可能性がありました。考えられる原因は次のとおりです。

-   この DML を実行した TiDB インスタンスが強制終了され、この DML ステートメントに対応するトランザクションの実行に DDL リースよりも時間がかかりました。トランザクションがコミットされたときに、エラーが発生しました。
-   TiDB は、この DML ステートメントの実行中に PD または TiKV に接続できませんでした。その結果、キープアライブ設定が原因で、TiDB が DDL リース内のスキーマのロードに失敗したか、PD から切断されました。

### 高い同時実行性の下で DDL ステートメントを実行するとエラーが報告されますか? {#error-is-reported-when-executing-ddl-statements-under-high-concurrency}

高い並行性で DDL ステートメント (バッチでのテーブルの作成など) を実行すると、同時実行中のキーの競合が原因で、これらのステートメントのごく一部が失敗する可能性があります。

同時 DDL ステートメントの数を 20 未満に保つことをお勧めします。それ以外の場合は、失敗したステートメントをクライアントから再試行する必要があります。

### DDL の実行がブロックされるのはなぜですか? {#why-is-ddl-execution-blocked}

TiDB v6.2.0 より前では、TiDB は、DDL ステートメントのタイプに基づいて、DDL ステートメントを 2 つの先入れ先出しキューに割り当てます。具体的には、Reorg DDL は Reorg キューに移動し、General DDL は一般キューに移動します。先入れ先出しの制限と、同じテーブルで DDL ステートメントを順次実行する必要があるため、実行中に複数の DDL ステートメントがブロックされる場合があります。

たとえば、次の DDL ステートメントについて考えてみます。

-   DDL 1: `CREATE INDEX idx on t(a int);`
-   DDL2: `ALTER TABLE t ADD COLUMN b int;`
-   DDL3: `CREATE TABLE t1(a int);`

先入れ先出しキューの制限により、DDL 3 は DDL 2 の実行を待機する必要があります。また、同じテーブルの DDL ステートメントはシリアルで実行する必要があるため、DDL 2 は DDL 1 が実行されるまで待機する必要があります。したがって、DDL 3 は、異なるテーブルで動作する場合でも、DDL 1 が最初に実行されるまで待機する必要があります。

TiDB v6.2.0 以降、TiDB DDL モジュールは並行フレームワークを使用します。並行フレームワークでは、先入れ先出しキューの制限がなくなりました。代わりに、TiDB はすべての DDL タスクから実行可能な DDL タスクを取得します。さらに、Reorg ワーカーの数が拡張され、ノードあたり約`CPU/4`になりました。これにより、TiDB は並行フレームワークで同時に複数のテーブルのインデックスを構築できます。

クラスターが新しいクラスターであるか、以前のバージョンからアップグレードされたクラスターであるかに関係なく、TiDB は TiDB v6.2 以降のバージョンで並行フレームワークを自動的に使用します。手動で調整する必要はありません。

### スタックした DDL 実行の原因を特定する {#identify-the-cause-of-stuck-ddl-execution}

1.  DDL ステートメントの実行を遅くするその他の理由を排除します。
2.  次のいずれかの方法を使用して、DDL 所有者ノードを識別します。
    -   `curl http://{TiDBIP}:10080/info/all`を使用して、現在のクラスターの所有者を取得します。
    -   監視ダッシュボード**DDL** &gt; <strong>DDL META OPM</strong>から特定の期間の所有者をビュー。

-   所有者が存在しない場合は、 `curl -X POST http://{TiDBIP}:10080/ddl/owner/resign`を使用して手動で所有者の選択をトリガーしてみてください。
-   所有者が存在する場合は、Goroutine スタックをエクスポートし、スタックしている可能性のある場所を確認します。

## SQL 最適化 {#sql-optimization}

### TiDB 実行計画の説明 {#tidb-execution-plan-description}

[クエリ実行計画を理解する](/explain-overview.md)を参照してください。

### 統計収集 {#statistics-collection}

[統計入門](/statistics.md)を参照してください。

### <code>select count(1)</code>を最適化する方法は? {#how-to-optimize-code-select-count-1-code}

`count(1)`ステートメントは、テーブル内の行の総数をカウントします。並行性の程度を向上させると、速度が大幅に向上する可能性があります。同時実行数を変更するには、 [`tidb_distsql_scan_concurrency`ドキュメント](/system-variables.md#tidb_distsql_scan_concurrency)を参照してください。ただし、CPU および I/O リソースにも依存します。 TiDB はすべてのクエリで TiKV にアクセスします。データ量が少ない場合、MySQL はすべてメモリ内にあり、TiDB はネットワーク アクセスを行う必要があります。

推奨事項:

-   ハードウェア構成を改善します。 [ソフトウェアとハードウェアの要件](/hardware-and-software-requirements.md)を参照してください。
-   同時性を改善します。デフォルト値は 10 です。50 に改善して試してみることができます。ただし、通常、改善はデフォルト値の 2 ～ 4 倍です。
-   大量のデータの場合は`count`をテストします。
-   TiKV 構成を最適化します。 [TiKV スレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md)と[TiKV メモリ パフォーマンスの調整](/tune-tikv-memory-performance.md)を参照してください。
-   [コプロセッサーキャッシュ](/coprocessor-cache.md)を有効にします。

### 現在の DDL ジョブの進行状況を表示する方法は? {#how-to-view-the-progress-of-the-current-ddl-job}

`ADMIN SHOW DDL`を使用して、現在の DDL ジョブの進行状況を表示できます。操作は次のとおりです。

```sql
ADMIN SHOW DDL;
```

```
*************************** 1. row ***************************
  SCHEMA_VER: 140
       OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
     SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
```

上記の結果から、 `ADD INDEX`操作が現在処理中であることがわかります。 `RUNNING_JOBS`列の`RowCount`フィールドから、 `ADD INDEX`操作で 77312 行のインデックスが追加されたことを取得することもできます。

### DDL ジョブを表示する方法 {#how-to-view-the-ddl-job}

-   `ADMIN SHOW DDL` : 実行中の DDL ジョブを表示する
-   `ADMIN SHOW DDL JOBS` : 現在の DDL ジョブ キュー内のすべての結果 (実行中および実行待ちのタスクを含む) と、完了した DDL ジョブ キュー内の最後の 10 個の結果を表示します。
-   `ADMIN SHOW DDL JOBS QUERIES 'job_id' [, 'job_id'] ...` : `job_id`に対応する DDL タスクの元の SQL ステートメントを表示します。 `job_id`は実行中の DDL ジョブのみを検索し、最後の 10 個の結果は DDL 履歴ジョブ キューに格納されます。

### TiDB は CBO (Cost-Based Optimization) をサポートしていますか?はいの場合、どの程度ですか？ {#does-tidb-support-cbo-cost-based-optimization-if-yes-to-what-extent}

はい。 TiDB はコストベースのオプティマイザーを使用します。コスト モデルと統計は常に最適化されています。 TiDB は、ハッシュ結合やソートマージ結合などの結合アルゴリズムもサポートしています。

### テーブルで<code>analyze</code>実行する必要があるかどうかを判断するにはどうすればよいですか? {#how-to-determine-whether-i-need-to-execute-code-analyze-code-on-a-table}

`SHOW STATS_HEALTHY`使用して`Healthy`フィールドをビュー、通常、フィールド値が 60 より小さい場合、テーブルで`ANALYZE`を実行する必要があります。

### クエリ プランをツリーとして表示する場合の ID ルールは何ですか?このツリーの実行順序は? {#what-is-the-id-rule-when-a-query-plan-is-presented-as-a-tree-what-is-the-execution-order-for-this-tree}

これらの ID にルールはありませんが、ID は一意です。 ID が生成されるとカウンターが機能し、1 つのプランが生成されると 1 つ追加されます。実行順序は ID とは関係ありません。クエリ プラン全体がツリーであり、実行プロセスはルート ノードから開始され、データは継続的に上位レベルに返されます。クエリ プランの詳細については、 [TiDB クエリ実行プランを理解する](/explain-overview.md)を参照してください。

### TiDB クエリ プランでは、 <code>cop</code>タスクは同じルートにあります。それらは同時に実行されますか？ {#in-the-tidb-query-plan-code-cop-code-tasks-are-in-the-same-root-are-they-executed-concurrently}

現在、TiDB のコンピューティング タスクは、 `cop task`と`root task`の 2 つの異なるタイプのタスクに属しています。

`cop task`は、分散実行のために KV エンドにプッシュされるコンピューティング タスクです。 `root task`は、TiDB 側でのシングル ポイント実行のコンピューティング タスクです。

通常、 `root task`の入力データは`cop task`から取得されます。 `root task`データを処理すると、TiKVの`cop task`が同時にデータを処理でき、TiDBの`root task`のプルを待ちます。したがって、 `cop`タスクは`root task`と同時に実行されると見なすことができます。しかし、彼らのデータには上流と下流の関係があります。実行プロセス中、それらはしばらくの間同時に実行されます。たとえば、最初の`cop task` [100, 200] のデータを処理し、2 番目の`cop task` [1, 100] のデータを処理しています。詳しくは[TiDB クエリ プランを理解する](/explain-overview.md)をご覧ください。

## データベースの最適化 {#database-optimization}

### TiDB オプションの編集 {#edit-tidb-options}

[TiDB コマンド オプション](/command-line-flags-for-tidb-configuration.md)を参照してください。

### ホットスポットの問題を回避し、負荷分散を実現する方法は?ホット パーティションまたは範囲は TiDB の問題ですか? {#how-to-avoid-hotspot-issues-and-achieve-load-balancing-is-hot-partition-or-range-an-issue-in-tidb}

ホットスポットの原因となるシナリオについては、 [一般的な鍋](/troubleshoot-hot-spot-issues.md#common-hotspots)を参照してください。次の TiDB 機能は、ホットスポットの問題を解決するのに役立つように設計されています。

-   [`SHARD_ROW_ID_BITS`](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)属性。この属性を設定すると、行 ID が分散されて複数のリージョンに書き込まれるため、書き込みホットスポットの問題を軽減できます。
-   自動インクリメント主キーによってもたらされるホットスポットを解決するのに役立つ[`AUTO_RANDOM`](/troubleshoot-hot-spot-issues.md#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)属性。
-   [コプロセッサーキャッシュ](/coprocessor-cache.md) 、小さなテーブルの読み取りホットスポット用。
-   [ロードベーススプリット](/configure-load-base-split.md) 、小さなテーブルのフル テーブル スキャンなど、リージョン間の不均衡なアクセスによって発生するホットスポットの場合。
-   [キャッシュされたテーブル](/cached-tables.md) 、頻繁にアクセスされるがほとんど更新されない小さなホットスポット テーブル用。

ホットスポットが原因でパフォーマンスの問題が発生した場合は、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照して解決してください。

### TiKV のパフォーマンスを調整する {#tune-tikv-performance}

[TiKV スレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md)と[TiKV メモリ パフォーマンスの調整](/tune-tikv-memory-performance.md)を参照してください。
