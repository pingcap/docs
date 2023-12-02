---
title: SQL FAQs
summary: Learn about the FAQs related to TiDB SQL.
---

# SQL FAQ {#sql-faqs}

このドキュメントには、TiDB での SQL 操作に関連する FAQ がまとめられています。

## TiDB は二次キーをサポートしていますか? {#does-tidb-support-the-secondary-key}

はい。一意の[セカンダリインデックス](/develop/dev-guide-create-secondary-indexes.md)を持つ非主キー列に[`NOT NULL`制約](/constraints.md#not-null)設定できます。この場合、列は 2 次キーとして機能します。

## 大きなテーブルで DDL 操作を実行する場合、TiDB はどのように動作しますか? {#how-does-tidb-perform-when-executing-ddl-operations-on-a-large-table}

大きなテーブルに対する TiDB の DDL 操作は、通常は問題になりません。 TiDB はオンライン DDL 操作をサポートしており、これらの DDL 操作は DML 操作をブロックしません。

列の追加、列の削除、インデックスの削除などの一部の DDL 操作については、TiDB はこれらの操作を迅速に実行できます。

インデックスの追加など、一部の負荷の高い DDL 操作の場合、TiDB はデータをバックフィルする必要がありますが、これには (テーブルのサイズに応じて) 時間がかかり、追加のリソースが消費されます。オンライン トラフィックへの影響は調整可能です。 TiDB は複数のスレッドでバックフィルを実行でき、消費されるリソースは次のシステム変数で設定できます。

-   [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
-   [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
-   [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
-   [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

## 適切なクエリ プランを選択するにはどうすればよいですか?ヒントを使用する必要がありますか?それともヒントを使えばいいのでしょうか？ {#how-to-choose-the-right-query-plan-do-i-need-to-use-hints-or-can-i-use-hints}

TiDB にはコストベースのオプティマイザーが含まれています。ほとんどの場合、オプティマイザーは最適なクエリ プランを選択します。オプティマイザがうまく機能しない場合でも、 [オプティマイザーのヒント](/optimizer-hints.md)使用してオプティマイザに介入できます。

さらに、 [SQLバインディング](/sql-plan-management.md#sql-binding)を使用して、特定の SQL ステートメントのクエリ プランを修正することもできます。

## 特定の SQL ステートメントの実行を防ぐにはどうすればよいですか? {#how-to-prevent-the-execution-of-a-particular-sql-statement}

[`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen)ヒントを使用して[SQLバインディング](/sql-plan-management.md#sql-binding)を作成すると、特定のステートメントの実行時間を小さい値 (1ms など) に制限できます。このようにして、ステートメントはしきい値によって自動的に終了します。

たとえば、 `SELECT * FROM t1, t2 WHERE t1.id = t2.id`の実行を防ぐには、次の SQL バインディングを使用してステートメントの実行時間を 1 ミリ秒に制限します。

```sql
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ MAX_EXECUTION_TIME(1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **注記：**
>
> `MAX_EXECUTION_TIME`の精度は約 100ms です。 TiDB が SQL ステートメントを終了する前に、TiKV のタスクが開始される可能性があります。このような場合に TiKV リソースの消費を軽減するには、 [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540) ～ `ON`を設定することをお勧めします。

この SQL バインディングを削除すると、制限が解除されます。

```sql
DROP GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

## TiDB と互換性のある MySQL 変数は何ですか? {#what-are-the-mysql-variables-that-tidb-is-compatible-with}

[システム変数](/system-variables.md)を参照してください。

## <code>ORDER BY</code>省略した場合、結果の順序がMySQLと異なります {#the-order-of-results-is-different-from-mysql-when-code-order-by-code-is-omitted}

それはバグではありません。デフォルトのレコードの順序はさまざまな状況に依存しますが、一貫性は保証されません。

クエリは単一スレッドで実行されるため、MySQL の結果の順序は安定しているように見える場合があります。ただし、新しいバージョンにアップグレードすると、クエリ プランが変更される可能性があるのが一般的です。結果の順序が必要な場合は常に`ORDER BY`を使用することをお勧めします。

参考文献は[ISO/IEC 9075:1992、データベース言語 SQL - 1992 年 7 月 30 日](http://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt)にあり、次のように述べられています。

> `<order by clause>`が指定されていない場合、 `<cursor specification>`で指定されるテーブルは T であり、T 内の行の順序は実装に依存します。

次の 2 つのクエリでは、両方の結果が正当であるとみなされます。

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

`ORDER BY`で使用される列のリストが一意でない場合、そのステートメントも非決定的であるとみなされます。次の例では、列`a`に重複した値があります。したがって、決定性が保証されるのは`ORDER BY a, b`だけです。

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

次のステートメントでは、列`a`の順序は保証されていますが、列`b`の順序は保証されていません。

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

TiDB では、システム変数[`tidb_enable_ordered_result_mode`](/system-variables.md#tidb_enable_ordered_result_mode)を使用して、最終出力結果を自動的に並べ替えることもできます。

## TiDB は<code>SELECT FOR UPDATE</code>をサポートしていますか? {#does-tidb-support-code-select-for-update-code}

はい。悲観的ロック (TiDB v3.0.8 以降のデフォルト) を使用する場合、 `SELECT FOR UPDATE`は MySQL と同様に動作します。

楽観的ロックを使用する場合、 `SELECT FOR UPDATE`はトランザクションの開始時にデータをロックしませんが、トランザクションのコミット時に競合をチェックします。チェックによって競合が判明した場合、コミット中のトランザクションはロールバックされます。

詳細は[`SELECT`構文要素の説明](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements)を参照してください。

## TiDB のコーデックは、UTF-8 文字列が memcomparable であることを保証できますか?キーが UTF-8 をサポートする必要がある場合、コーディングに関する提案はありますか? {#can-the-codec-of-tidb-guarantee-that-the-utf-8-string-is-memcomparable-is-there-any-coding-suggestion-if-our-key-needs-to-support-utf-8}

TiDB はデフォルトで UTF-8 文字セットを使用し、現在は UTF-8 のみをサポートしています。 TiDB の文字列は memcomparable 形式を使用します。

## トランザクション内のステートメントの最大数はどれくらいですか? {#what-is-the-maximum-number-of-statements-in-a-transaction}

トランザクション内のステートメントの最大数は、デフォルトでは 5000 です。

楽観的トランザクション モードでは、トランザクションの再試行が有効な場合、デフォルトの上限は 5000 です[`stmt-count-limit`](/tidb-configuration-file.md#stmt-count-limit)パラメータを使用して制限を調整できます。

## TiDB で後から挿入されたデータの自動インクリメント ID が、前に挿入されたデータの自動インクリメント ID より小さいのはなぜですか? {#why-does-the-auto-increment-id-of-the-later-inserted-data-is-smaller-than-that-of-the-earlier-inserted-data-in-tidb}

TiDB の自動インクリメント ID 機能は、自動的に増分され、一意であることが保証されるだけで、連続的に割り当てられることは保証されません。現在、TiDB はバッチで ID を割り当てています。データが複数の TiDB サーバーに同時に挿入される場合、割り当てられる ID は連続しません。複数のスレッドが複数の`tidb-server`インスタンスにデータを同時に挿入すると、後から挿入されたデータの自動インクリメント ID が小さくなる可能性があります。 TiDB では、整数フィールドに`AUTO_INCREMENT`指定できますが、1 つのテーブル内で`AUTO_INCREMENT`フィールドは 1 つだけ許可されます。詳細については、 [自動インクリメントID](/mysql-compatibility.md#auto-increment-id)および[AUTO_INCREMENT 属性](/auto-increment.md)を参照してください。

## TiDB で<code>sql_mode</code>を変更するにはどうすればよいですか? {#how-do-i-modify-the-code-sql-mode-code-in-tidb}

TiDB は、SESSION または GLOBAL ベースでのシステム[`sql_mode`](/system-variables.md#sql_mode)の変更をサポートします。

-   [`GLOBAL`](/sql-statements/sql-statement-set-variable.md)スコープ変数への変更はクラスターの残りのサーバーに伝播し、再起動後も保持されます。これは、各 TiDBサーバーで`sql_mode`値を変更する必要がないことを意味します。
-   `SESSION`のスコープ変数への変更は、現在のクライアント セッションにのみ影響します。サーバーを再起動すると、変更は失われます。

## エラー: Sqoop を使用してデータを TiDB にバッチで書き込むときに、 <code>java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation</code> {#error-code-java-sql-batchupdateexecption-statement-count-5001-exceeds-the-transaction-limitation-code-while-using-sqoop-to-write-data-into-tidb-in-batches}

Sqoop では、 `--batch`各バッチで 100 個のステートメントをコミットすることを意味しますが、デフォルトでは各ステートメントに 100 個の SQL ステートメントが含まれます。したがって、SQL ステートメントは 100 * 100 = 10000 となり、単一の TiDB トランザクションで許可されるステートメントの最大数である 5000 を超えます。

2 つの解決策:

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

-   単一の TiDB トランザクション内の限られた数のステートメントを増やすこともできますが、これによりより多くのメモリが消費されます。詳細は[SQL ステートメントの制限事項](/tidb-limitations.md#limitations-on-sql-statements)を参照してください。

## TiDBにはOracleのフラッシュバッククエリのような機能はありますか？ DDLをサポートしていますか? {#does-tidb-have-a-function-like-the-flashback-query-in-oracle-does-it-support-ddl}

はい、そうです。また、DDL もサポートしています。詳細は[`AS OF TIMESTAMP`句を使用した履歴データの読み取り](/as-of-timestamp.md)を参照してください。

## TiDB はデータを削除した後すぐにスペースを解放しますか? {#does-tidb-release-space-immediately-after-deleting-data}

`DELETE` 、 `TRUNCATE` 、および`DROP`操作はいずれも、データを直ちに解放しません。 `TRUNCATE`と`DROP`の操作では、TiDB GC (ガベージ コレクション) 時間 (デフォルトでは 10 分) が経過すると、データが削除され、スペースが解放されます。 `DELETE`の操作では、データは削除されますが、圧縮が実行されるまでスペースはすぐには解放されません。

## データを削除するとクエリ速度が遅くなるのはなぜですか? {#why-does-the-query-speed-get-slow-after-data-is-deleted}

大量のデータを削除すると、不要なキーが大量に残り、クエリの効率に影響します。この問題を解決するには、 [リージョンのマージ](/best-practices/massive-regions-best-practices.md#method-3-enable-region-merge)機能を使用できます。詳細は[TiDB ベスト プラクティスのデータの削除セクション](https://en.pingcap.com/blog/tidb-best-practice/#write)を参照してください。

## データを削除した後にstorage領域を再利用するのが遅い場合はどうすればよいですか? {#what-should-i-do-if-it-is-slow-to-reclaim-storage-space-after-deleting-data}

TiDB はマルチバージョン同時実行制御 (MVCC) を使用しているため、古いデータが新しいデータで上書きされる場合、古いデータは置き換えられず、新しいデータとともに保持されます。タイムスタンプはデータのバージョンを識別するために使用されます。データを削除しても、すぐにスペースが再利用されるわけではありません。ガベージ コレクションは、同時トランザクションが以前のバージョンの行を参照できるように遅延されます。これは[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (デフォルト: `10m0s` ) システム変数を介して構成できます。

## <code>SHOW PROCESSLIST</code>システム プロセス ID を表示しますか? {#does-code-show-processlist-code-display-the-system-process-id}

TiDB `SHOW PROCESSLIST`の表示内容は MySQL `SHOW PROCESSLIST`とほぼ同じです。 TiDB `SHOW PROCESSLIST`はシステム プロセス ID を表示しません。表示される ID は現在のセッション ID です。 TiDB `SHOW PROCESSLIST`と MySQL `SHOW PROCESSLIST`の違いは次のとおりです。

-   TiDB は分散データベースであるため、 `tidb-server`のインスタンスは SQL ステートメントを解析して実行するためのステートレス エンジンです (詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md)参照)。 `SHOW PROCESSLIST`クラスター内で実行されているすべてのセッションのリストではなく、ユーザーが MySQL クライアントからログインする`tidb-server`インスタンスで実行されたセッションのリストが表示されます。ただし、MySQL はスタンドアロン データベースであり、MySQL で実行された`SHOW PROCESSLIST`の SQL ステートメントが表示されます。
-   TiDB の`State`列は、クエリの実行中に継続的に更新されるわけではありません。 TiDB は並列クエリをサポートしているため、各ステートメントは同時に複数の*状態*になる可能性があるため、単一の値に単純化することが困難です。

## SQLコミットの実行優先順位を制御または変更するにはどうすればよいですか? {#how-to-control-or-change-the-execution-priority-of-sql-commits}

TiDB は、 [グローバル](/system-variables.md#tidb_force_priority)または個々のステートメントごとの優先順位の変更をサポートしています。優先順位には次の意味があります。

-   `HIGH_PRIORITY` : このステートメントの優先順位は高くなります。つまり、TiDB はこのステートメントに優先順位を与え、最初に実行します。

-   `LOW_PRIORITY` : このステートメントの優先順位は低くなります。つまり、TiDB は実行期間中にこのステートメントの優先順位を下げます。

-   `DELAYED` : このステートメントは通常の優先順位を持ち、 `tidb_force_priority`の`NO_PRIORITY`設定と同じです。

上記 2 つのパラメータを TiDB の DML と組み合わせて使用​​できます。例えば：

1.  データベースに SQL ステートメントを記述して優先度を調整します。

    ```sql
    SELECT HIGH_PRIORITY | LOW_PRIORITY | DELAYED COUNT(*) FROM table_name;
    INSERT HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name insert_values;
    DELETE HIGH_PRIORITY | LOW_PRIORITY | DELAYED FROM table_name;
    UPDATE HIGH_PRIORITY | LOW_PRIORITY | DELAYED table_reference SET assignment_list WHERE where_condition;
    REPLACE HIGH_PRIORITY | LOW_PRIORITY | DELAYED INTO table_name;
    ```

2.  フルテーブルスキャンステートメントは、自動的に低い優先順位に調整されます。 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)デフォルトで優先度が低くなります。

## TiDB での<code>auto analyze</code>のトリガー戦略は何ですか? {#what-s-the-trigger-strategy-for-code-auto-analyze-code-in-tidb}

トリガー戦略: `auto analyze` 、新しいテーブルの行数が 1000 に達し、このテーブルに 1 分間書き込み操作がない場合に自動的にトリガーされます。

比率 (変更された行数 / 現在の合計行数) が`tidb_auto_analyze_ratio`より大きい場合、 `analyze`ステートメントが自動的にトリガーされます。デフォルト値の`tidb_auto_analyze_ratio`は 0.5 で、この機能がデフォルトで有効であることを示します。安全性を確保するため、この機能が有効な場合の最小値は 0.3 であり、デフォルト値が 0.8 である`pseudo-estimate-ratio`より小さい必要があります。そうでない場合は、一定期間疑似統計が使用されます。 `tidb_auto_analyze_ratio` ～ 0.5 に設定することをお勧めします。

auto analyzeを無効にするには、システム変数`tidb_enable_auto_analyze`を使用します。

## オプティマイザーのヒントを使用してオプティマイザーの動作をオーバーライドできますか? {#can-i-use-optimizer-hints-to-override-the-optimizer-behavior}

TiDB は、デフォルトのクエリ オプティマイザーの動作をオーバーライドする複数の方法 ( [ヒント](/optimizer-hints.md)や[SQL計画管理](/sql-plan-management.md)など) をサポートしています。基本的な使用法は MySQL と似ていますが、TiDB 固有の拡張機能がいくつかあります。

```sql
SELECT column_name FROM table_name USE INDEX（index_name）WHERE where_condition;
```

## DDL の実行 {#ddl-execution}

このセクションでは、DDL ステートメントの実行に関連する問題をリストします。 DDL の実行原理の詳細については、 [DDL ステートメントの実行原則とベスト プラクティス](/ddl-introduction.md)を参照してください。

### さまざまな DDL 操作を実行するのにどれくらい時間がかかりますか? {#how-long-does-it-take-to-perform-various-ddl-operations}

DDL 操作がブロックされず、各 TiDBサーバーがスキーマ バージョンを正常に更新でき、DDL 所有者ノードが正常に実行されていると仮定します。この場合、さまざまな DDL 操作の推定時間は次のとおりです。

| DDL 操作の種類                                                                                                                                                                                                 | 予定時刻                              |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------- |
| Reorg DDL ( `ADD INDEX` 、 `MODIFY COLUMN`など) (Reorg タイプのデータ変更)                                                                                                                                            | データ量、システム負荷、DDL パラメータ設定によって異なります。 |
| 一般的な DDL (Reorg 以外の DDL タイプ)、 `CREATE DATABASE` 、 `CREATE TABLE` 、 `DROP DATABASE` 、 `DROP TABLE` 、 `TRUNCATE TABLE` 、 `ALTER TABLE ADD` 、 `ALTER TABLE DROP` 、 `MODIFY COLUMN` (メタデータのみ変更)、 `DROP INDEX` | 約1秒                               |

> **注記：**
>
> 上記は作業にかかる時間の目安です。実際の時間は異なる場合があります。

### DDL の実行が遅い考えられる理由 {#possible-reasons-why-ddl-execution-is-slow}

-   ユーザー セッションで、DDL ステートメントの前に非自動コミット DML ステートメントがあり、非自動コミット DML ステートメントのコミット操作が遅い場合、DDL ステートメントの実行が遅くなります。つまり、TiDB は、DDL ステートメントを実行する前に、コミットされていない DML ステートメントをコミットします。

-   複数の DDL ステートメントを同時に実行すると、後続の DDL ステートメントはキューで待機する必要があるため、実行が遅くなる可能性があります。キューイングのシナリオには次のものが含まれます。

    -   同じ種類の DDL ステートメントをキューに入れる必要があります。たとえば、 `CREATE TABLE`と`CREATE DATABASE`はどちらも一般的な DDL ステートメントであるため、両方の操作を同時に実行する場合はキューに入れる必要があります。 TiDB v6.2.0 以降、並列 DDL ステートメントがサポートされていますが、あまりにも多くの TiDB コンピューティング リソースを使用する DDL 実行を避けるために、同時実行制限もあります。キューイングは、DDL が同時実行制限を超えると発生します。
    -   同じテーブルに対して実行される DDL 操作には、それらの間に依存関係があります。後の DDL ステートメントは、前の DDL 操作が完了するまで待機する必要があります。

-   クラスターが正常に起動した後、DDL モジュールが DDL 所有者を選択しているため、最初の DDL 操作の実行時間が比較的長くなる可能性があります。

-   TiDB が終了すると、TiDB は PD と正常に通信できなくなります (電源オフの状況を含む)。または、TiDB が`kill -9`コマンドによって終了され、TiDB が PD から登録データをタイムリーに消去できなくなります。

-   クラスター内の特定の TiDB ノードと PD または TiKV の間で通信の問題が発生し、TiDB が最新のバージョン情報を時間内に取得できなくなります。

### <code>Information schema is changed</code> 」エラーは何がトリガーされますか? {#what-triggers-the-code-information-schema-is-changed-code-error}

SQL ステートメントを実行するとき、TiDB は分離レベルに基づいてオブジェクトのスキーマ バージョンを決定し、それに応じて SQL ステートメントを処理します。 TiDB は、オンラインの非同期 DDL 変更もサポートしています。 DML ステートメントを実行するときは、同時に実行される DDL ステートメントが存在する可能性があるため、各 SQL ステートメントが同じスキーマで実行されるようにする必要があります。したがって、DML を実行するときに、DDL 操作が進行中の場合、TiDB は`Information schema is changed`エラーを報告する可能性があります。

v6.4.0 以降、TiDB は[メタデータのロック機構](/metadata-lock.md)を実装しました。これにより、DML ステートメントと DDL スキーマ変更の調整された実行が可能になり、ほとんどの`Information schema is changed`エラーが回避されます。

このエラー報告には、まだいくつかの原因が考えられます。

-   原因 1: DML 操作に関係する一部のテーブルは、進行中の DDL 操作に関係するテーブルと同じです。進行中の DDL 操作を確認するには、 `ADMIN SHOW DDL`ステートメントを使用します。
-   原因 2: DML 操作が長時間継続します。この期間中、多くの DDL ステートメントが実行され、1024 を`schema`バージョン変更が発生しました。 `tidb_max_delta_schema_count`変数を変更することで、このデフォルト値を変更できます。
-   原因 3: DML リクエストを受け入れる TiDBサーバーは、長時間`schema information`ロードできません (TiDB と PD または TiKV の間の接続障害が原因である可能性があります)。この期間中、多くの DDL ステートメントが実行され、100 を超える`schema`バージョンの変更が発生しました。
-   原因 4: TiDB の再起動後、最初の DDL 操作が実行される前に、DML 操作が実行され、その後最初の DDL 操作が発生します (つまり、最初の DDL 操作が実行される前に、DML に対応するトランザクションが開始されます。 DDL の最初の`schema`バージョンが変更され、DML に対応するトランザクションがコミットされると、この DML 操作でこのエラーが報告されます。

前述の原因のうち、テーブルに関連しているのは原因 1 のみです。関連する DML 操作は失敗後に再試行されるため、原因 1 と原因 2 はアプリケーションには影響しません。原因 3 の場合は、TiDB と TiKV/PD 間のネットワークを確認する必要があります。

> **注記：**
>
> -   現在、TiDB は`schema`バージョンの変更をすべてキャッシュするわけではありません。
> -   各 DDL 操作について、 `schema`バージョン変更の数は、対応する`schema state`バージョン変更の数と同じです。
> -   DDL 操作が異なると、 `schema`変更の数も異なります。たとえば、 `CREATE TABLE`ステートメントでは`schema`バージョン変更が 1 つ発生し、 `ADD COLUMN`ステートメントでは 4 つのバージョン変更が発生します。

### 「情報スキーマが古くなっています」エラーの原因は何ですか? {#what-are-the-causes-of-the-information-schema-is-out-of-date-error}

TiDB v6.5.0 より前では、DML ステートメントの実行時に、TiDB が DDL リース (デフォルトでは 45 秒) 内で最新のスキーマのロードに失敗すると、 `Information schema is out of date`エラーが発生する可能性がありました。考えられる原因は次のとおりです。

-   この DML を実行した TiDB インスタンスが強制終了され、この DML ステートメントに対応するトランザクションの実行に DDL リースよりも長い時間がかかりました。トランザクションがコミットされたときにエラーが発生しました。
-   この DML ステートメントの実行中に、TiDB は PD または TiKV に接続できませんでした。その結果、TiDB は DDL リース内でスキーマをロードできなかったか、キープアライブ設定が原因で PD から切断されました。

### 高い同時実行性で DDL ステートメントを実行するとエラーが報告されますか? {#error-is-reported-when-executing-ddl-statements-under-high-concurrency}

高い同時実行性で DDL ステートメント (バッチでのテーブルの作成など) を実行すると、同時実行中のキーの競合により、これらのステートメントのごく一部が失敗する可能性があります。

同時 DDL ステートメントの数を 20 未満に保つことをお勧めします。それ以外の場合は、失敗したステートメントをクライアントから再試行する必要があります。

### DDL の実行がブロックされるのはなぜですか? {#why-is-ddl-execution-blocked}

TiDB v6.2.0 より前では、TiDB は、DDL ステートメントのタイプに基づいて、DDL ステートメントを 2 つの先入れ先出しキューに割り当てます。具体的には、Reorg DDL は Reorg キューに送られ、General DDL は一般キューに送られます。先入れ先出しの制限と、同じテーブル上で DDL ステートメントをシリアルに実行する必要があるため、複数の DDL ステートメントが実行中にブロックされる可能性があります。

たとえば、次の DDL ステートメントを考えてみましょう。

-   DDL 1: `CREATE INDEX idx on t(a int);`
-   DDL 2: `ALTER TABLE t ADD COLUMN b int;`
-   DDL 3: `CREATE TABLE t1(a int);`

先入れ先出しキューの制限により、DDL 3 は DDL 2 が実行されるまで待機する必要があります。また、同じテーブル上の DDL ステートメントはシリアルに実行する必要があるため、DDL 2 は DDL 1 が実行されるまで待機する必要があります。したがって、DDL 3 は、異なるテーブルで動作する場合でも、DDL 1 が最初に実行されるまで待機する必要があります。

TiDB v6.2.0 以降、TiDB DDL モジュールは同時フレームワークを使用します。同時フレームワークでは、先入れ先出しキューの制限がなくなりました。代わりに、TiDB はすべての DDL タスクから実行できる DDL タスクを選択します。さらに、Reorg ワーカーの数が拡張され、ノードあたり約`CPU/4`になりました。これにより、TiDB は並行フレームワークで複数のテーブルのインデックスを同時に構築できます。

クラスターが新しいクラスターであっても、以前のバージョンからアップグレードされたクラスターであっても、TiDB は TiDB v6.2 以降のバージョンの同時フレームワークを自動的に使用します。手動で調整する必要はありません。

### DDL 実行のスタックの原因を特定する {#identify-the-cause-of-stuck-ddl-execution}

1.  DDL ステートメントの実行を遅くする他の理由を取り除きます。
2.  次のいずれかの方法を使用して、DDL 所有者ノードを識別します。
    -   現在のクラスターの所有者を取得するには、 `curl http://{TiDBIP}:10080/info/all`を使用します。
    -   監視ダッシュボードの**[DDL]** &gt; **[DDL META OPM]**から、特定の期間の所有者をビュー。

-   所有者が存在しない場合は、次のコマンドを使用して所有者の選択を手動でトリガーしてみてください。 `curl -X POST http://{TiDBIP}:10080/ddl/owner/resign` 。
-   所有者が存在する場合は、Goroutine スタックをエクスポートし、スタックしている可能性のある場所を確認します。

## SQLの最適化 {#sql-optimization}

### TiDB 実行計画の説明 {#tidb-execution-plan-description}

[クエリ実行計画を理解する](/explain-overview.md)を参照してください。

### 統計収集 {#statistics-collection}

[統計入門](/statistics.md)を参照してください。

### <code>select count(1)</code>を最適化するにはどうすればよいですか? {#how-to-optimize-code-select-count-1-code}

`count(1)`ステートメントは、テーブル内の行の総数をカウントします。並行性の程度を改善すると、速度が大幅に向上します。同時実行性を変更するには、 [`tidb_distsql_scan_concurrency`ドキュメント](/system-variables.md#tidb_distsql_scan_concurrency)を参照してください。ただし、CPU と I/O リソースにも依存します。 TiDB はクエリごとに TiKV にアクセスします。データ量が少ない場合、MySQL はすべてメモリ内にあり、TiDB はネットワーク アクセスを行う必要があります。

推奨事項:

-   ハードウェア構成を改善します。 [ソフトウェアとハ​​ードウェアの要件](/hardware-and-software-requirements.md)を参照してください。
-   同時実行性を改善します。デフォルト値は 10 です。50 に改善して試してみてください。ただし、通常、改善はデフォルト値の 2 ～ 4 倍です。
-   データ量が多い場合は`count`をテストしてください。
-   TiKV 構成を最適化します。 [TiKV スレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md)と[TiKV メモリ パフォーマンスを調整する](/tune-tikv-memory-performance.md)を参照してください。
-   [コプロセッサーキャッシュ](/coprocessor-cache.md)を有効にします。

### 現在の DDL ジョブの進行状況を確認するにはどうすればよいですか? {#how-to-view-the-progress-of-the-current-ddl-job}

`ADMIN SHOW DDL`を使用すると、現在の DDL ジョブの進行状況を表示できます。操作は次のとおりです。

```sql
ADMIN SHOW DDL;
```

    *************************** 1. row ***************************
      SCHEMA_VER: 140
           OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
    RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
         SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc

上記の結果から、現在`ADD INDEX`オペレーションが処理中であることがわかります。また、 `RUNNING_JOBS`列の`RowCount`フィールドから、 `ADD INDEX`操作により 77312 行のインデックスが追加されたことがわかります。

### DDL ジョブを表示するにはどうすればよいですか? {#how-to-view-the-ddl-job}

-   `ADMIN SHOW DDL` : 実行中の DDL ジョブを表示します。
-   `ADMIN SHOW DDL JOBS` : 現在の DDL ジョブ キュー内のすべての結果 (実行中および実行待ちのタスクを含む) と、完了した DDL ジョブ キュー内の最後の 10 件の結果を表示します。
-   `ADMIN SHOW DDL JOBS QUERIES 'job_id' [, 'job_id'] ...` : `job_id`に対応する DDL タスクの元の SQL ステートメントを表示します。 `job_id`実行中の DDL ジョブのみを検索し、DDL 履歴ジョブ キュー内の最後の 10 件の結果を検索します。

### TiDB は CBO (コストベースの最適化) をサポートしていますか? 「はい」の場合、どの程度ですか? {#does-tidb-support-cbo-cost-based-optimization-if-yes-to-what-extent}

はい。 TiDB はコストベースのオプティマイザーを使用します。コストモデルと統計は常に最適化されています。 TiDB は、ハッシュ結合やソートマージ結合などの結合アルゴリズムもサポートしています。

### テーブルに対して<code>analyze</code>実行する必要があるかどうかを判断するにはどうすればよいですか? {#how-to-determine-whether-i-need-to-execute-code-analyze-code-on-a-table}

`SHOW STATS_HEALTHY`使用して`Healthy`フィールドをビュー。通常、フィールド値が 60 より小さい場合はテーブルで`ANALYZE`を実行する必要があります。

### クエリ プランがツリーとして表示される場合の ID ルールは何ですか?このツリーの実行順序は何ですか? {#what-is-the-id-rule-when-a-query-plan-is-presented-as-a-tree-what-is-the-execution-order-for-this-tree}

これらの ID に対するルールは存在しませんが、ID は一意です。 IDが生成されるとカウンタが働き、プランが1つ生成されると1つ加算されます。実行順序は ID とは関係ありません。クエリ プラン全体はツリーであり、実行プロセスはルート ノードから開始され、データは継続的に上位レベルに返されます。クエリ プランの詳細については、 [TiDB クエリ実行プランについて](/explain-overview.md)を参照してください。

### TiDB クエリ プランでは、 <code>cop</code>タスクは同じルートにあります。それらは同時に実行されますか? {#in-the-tidb-query-plan-code-cop-code-tasks-are-in-the-same-root-are-they-executed-concurrently}

現在、TiDB のコンピューティング タスクは 2 つの異なるタイプのタスク ( `cop task`と`root task`に属しています。

`cop task`は、分散実行のために KV エンドにプッシュダウンされるコンピューティング タスクです。 `root task`は、TiDB 側でのシングル ポイント実行のコンピューティング タスクです。

通常、入力データ`root task`は`cop task`から取得されます。 `root task`データを処理するとき、TiKV の`cop task`は同時にデータを処理でき、TiDB の`root task`のプルを待ちます。したがって、 `cop`タスクは`root task`と同時に実行されると考えることができます。しかし、それらのデータには上流と下流の関係があります。実行プロセス中、ある時間内で同時に実行されます。たとえば、最初の`cop task` [100, 200] のデータを処理し、2 番目の`cop task` [1, 100] のデータを処理します。詳細については、 [TiDB クエリ プランを理解する](/explain-overview.md)参照してください。

## データベースの最適化 {#database-optimization}

### TiDB オプションの編集 {#edit-tidb-options}

[TiDB コマンドのオプション](/command-line-flags-for-tidb-configuration.md)を参照してください。

### ホットスポットの問題を回避し、負荷分散を実現するにはどうすればよいですか? TiDB ではホット パーティションまたは範囲が問題になりますか? {#how-to-avoid-hotspot-issues-and-achieve-load-balancing-is-hot-partition-or-range-an-issue-in-tidb}

ホットスポットの原因となるシナリオについては、 [一般的な鍋](/troubleshoot-hot-spot-issues.md#common-hotspots)を参照してください。次の TiDB 機能は、ホットスポットの問題の解決に役立つように設計されています。

-   [`SHARD_ROW_ID_BITS`](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)の属性。この属性を設定すると、行 ID が分散されて複数のリージョンに書き込まれるため、書き込みホットスポットの問題が軽減されます。
-   [`AUTO_RANDOM`](/troubleshoot-hot-spot-issues.md#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)属性。自動インクリメント主キーによってもたらされるホットスポットの解決に役立ちます。
-   [コプロセッサーキャッシュ](/coprocessor-cache.md) 、小さなテーブル上の読み取りホットスポットの場合。
-   [ロードベースの分割](/configure-load-base-split.md) : 小さなテーブルのフルテーブルスキャンなど、リージョン間の不均衡なアクセスによって引き起こされるホットスポットの場合。
-   [キャッシュされたテーブル](/cached-tables.md) : 頻繁にアクセスされるがほとんど更新されない小さなホットスポット テーブル。

ホットスポットが原因でパフォーマンスの問題が発生している場合は、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照して解決してください。

### TiKV のパフォーマンスを調整する {#tune-tikv-performance}

[TiKV スレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md)と[TiKV メモリ パフォーマンスを調整する](/tune-tikv-memory-performance.md)を参照してください。
