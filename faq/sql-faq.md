---
title: SQL FAQs
summary: Learn about the FAQs related to TiDB SQL.
---

# SQLに関するFAQ {#sql-faqs}

このドキュメントは、TiDBでのSQL操作に関連するFAQをまとめたものです。

## TiDBと互換性のあるMySQL変数は何ですか？ {#what-are-the-mysql-variables-that-tidb-is-compatible-with}

[システム変数](/system-variables.md)を参照してください。

## <code>ORDER BY</code>を省略した場合、結果の順序はMySQLとは異なります。 {#the-order-of-results-is-different-from-mysql-when-code-order-by-code-is-omitted}

バグではありません。レコードのデフォルトの順序は、一貫性を保証することなく、さまざまな状況によって異なります。

クエリはシングルスレッドで実行されるため、MySQLでの結果の順序は安定しているように見える場合があります。ただし、新しいバージョンにアップグレードすると、クエリプランが変更される可能性があります。結果の順序が必要な場合は常に`ORDER BY`を使用することをお勧めします。

参照は[ISO / IEC 9075：1992、データベース言語SQL-1992年7月30日](http://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt)にあり、次のように述べられています。

> `<order by clause>`が指定されていない場合、 `<cursor specification>`で指定されたテーブルはTであり、Tの行の順序は実装に依存します。

次の2つのクエリでは、両方の結果が正当であると見なされます。

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

`ORDER BY`で使用されている列のリストが一意でない場合も、ステートメントは非決定論的であると見なされます。次の例では、列`a`の値が重複しています。したがって、 `ORDER BY a, b`だけが決定論的に保証されます。

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

```sql
> select * from t order by a; -- the order of column a is guaranteed, but b is not
+------+------+
| a    | b    |
+------+------+
|    1 |    1 |
|    2 |    2 |
|    2 |    1 |
+------+------+
3 rows in set (0.00 sec)
```

## TiDBは<code>SELECT FOR UPDATE</code>をサポートしていますか？ {#does-tidb-support-code-select-for-update-code}

はい。ペシミスティックロック（TiDB v3.0以降のデフォルト）を使用する場合、 `SELECT FOR UPDATE`の実行はMySQLと同様に動作します。

楽観的ロックを使用する場合、 `SELECT FOR UPDATE`はトランザクションの開始時にデータをロックしませんが、トランザクションがコミットされるときに競合をチェックします。チェックで競合が明らかになった場合、コミットしているトランザクションはロールバックします。

## TiDBのコーデックは、UTF-8文字列が比較可能であることを保証できますか？キーがUTF-8をサポートする必要がある場合、コーディングの提案はありますか？ {#can-the-codec-of-tidb-guarantee-that-the-utf-8-string-is-memcomparable-is-there-any-coding-suggestion-if-our-key-needs-to-support-utf-8}

TiDBはデフォルトでUTF-8文字セットを使用し、現在はUTF-8のみをサポートしています。 TiDBの文字列は、memcomparable形式を使用します。

## トランザクション内のステートメントの最大数はいくつですか？ {#what-is-the-maximum-number-of-statements-in-a-transaction}

トランザクション内のステートメントの最大数は、デフォルトで5000です。

## 後で挿入されたデータの自動インクリメントIDが、TiDBに以前に挿入されたデータの自動インクリメントIDよりも小さいのはなぜですか？ {#why-does-the-auto-increment-id-of-the-later-inserted-data-is-smaller-than-that-of-the-earlier-inserted-data-in-tidb}

TiDBの自動インクリメントID機能は、自動的にインクリメンタルで一意であることが保証されているだけで、順次割り当てられることは保証されていません。現在、TiDBはIDをバッチで割り当てています。データが複数のTiDBサーバーに同時に挿入される場合、割り当てられたIDはシーケンシャルではありません。複数のスレッドが同時に複数の`tidb-server`インスタンスにデータを挿入する場合、後で挿入されるデータの自動インクリメントIDが小さくなる場合があります。 TiDBでは、整数フィールドに`AUTO_INCREMENT`を指定できますが、1つのテーブルに`AUTO_INCREMENT`フィールドを1つだけ指定できます。詳細については、 [自動インクリメントID](/mysql-compatibility.md#auto-increment-id)を参照してください。

## <code>sql_mode</code>でsql_modeを変更するにはどうすればよいですか？ {#how-do-i-modify-the-code-sql-mode-code-in-tidb}

TiDBは、SESSIONまたはGLOBALベースで[`sql_mode`](/system-variables.md#sql_mode)のシステム変数の変更をサポートします。 [`GLOBAL`](/sql-statements/sql-statement-set-variable.md)のスコープ変数への変更は、クラスタの残りのサーバーに伝播し、再起動後も保持されます。これは、各TiDBサーバーで`sql_mode`の値を変更する必要がないことを意味します。

## エラー： <code>java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation</code>ます {#error-code-java-sql-batchupdateexecption-statement-count-5001-exceeds-the-transaction-limitation-code-while-using-sqoop-to-write-data-into-tidb-in-batches}

Sqoopでは、 `--batch`は各バッチで100個のステートメントをコミットすることを意味しますが、デフォルトでは、各ステートメントには100個のSQLステートメントが含まれています。したがって、100 * 100 = 10000 SQLステートメント。これは5000を超えます。これは、単一のTiDBトランザクションで許可されるステートメントの最大数です。

2つの解決策：

-   次のように`-Dsqoop.export.records.per.statement=10`のオプションを追加します。

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

-   1つのTiDBトランザクションで制限された数のステートメントを増やすこともできますが、これはより多くのメモリを消費します。

## TiDBにはOracleのフラッシュバッククエリのような機能がありますか？ DDLをサポートしていますか？ {#does-tidb-have-a-function-like-the-flashback-query-in-oracle-does-it-support-ddl}

はい、そうです。また、DDLもサポートしています。詳細については、 [TiDBが履歴バージョンからデータを読み取る方法](/read-historical-data.md)を参照してください。

## TiDBはデータを削除した直後にスペースを解放しますか？ {#does-tidb-release-space-immediately-after-deleting-data}

`DELETE` 、および`TRUNCATE`の操作のいずれも、データをすぐに解放しませ`DROP` 。 `TRUNCATE`および`DROP`の操作では、TiDB GC（ガベージコレクション）時間（デフォルトでは10分）の後、データが削除され、スペースが解放されます。 `DELETE`回の操作では、データは削除されますが、圧縮が実行されるまでスペースはすぐには解放されません。

## データが削除された後、クエリ速度が遅くなるのはなぜですか？ {#why-does-the-query-speed-get-slow-after-data-is-deleted}

大量のデータを削除すると、多くの役に立たないキーが残り、クエリの効率に影響します。現在、 [リージョンマージ](/best-practices/massive-regions-best-practices.md)つの機能が開発中であり、この問題の解決が期待されています。詳細については、 [TiDBベストプラクティスのデータセクションの削除](https://en.pingcap.com/blog/tidb-best-practice/#write)を参照してください。

## データを削除した後にストレージスペースを再利用するのが遅い場合はどうすればよいですか？ {#what-should-i-do-if-it-is-slow-to-reclaim-storage-space-after-deleting-data}

TiDBはマルチバージョン同時実行制御（MVCC）を使用するため、データを削除してもすぐにスペースが再利用されるわけではありません。ガベージコレクションは、同時トランザクションが以前のバージョンの行を表示できるように遅延されます。これは、 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) （デフォルト： `10m0s` ）システム変数を介して構成できます。

## <code>SHOW PROCESSLIST</code>はシステムプロセスIDを表示しますか？ {#does-code-show-processlist-code-display-the-system-process-id}

TiDB1の表示内容は`SHOW PROCESSLIST`の表示内容とほぼ同じ`SHOW PROCESSLIST` 。 `show processlist`はシステムプロセスIDを表示しません。表示されるIDは、現在のセッションIDです。 `show processlist`と`show processlist`の違いは次のとおりです。

-   TiDBは分散データベースであるため、 `tidb-server`インスタンスはSQLステートメントを解析および実行するためのステートレスエンジンです（詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md)を参照してください）。 `show processlist`は、クラスタで実行されているすべてのセッションのリストではなく、ユーザーがMySQLクライアントからログインする`tidb-server`インスタンスで実行されたセッションリストを表示します。ただし、MySQLはスタンドアロンデータベースであり、その`show processlist`にはMySQLで実行されたすべてのSQLステートメントが表示されます。
-   TiDBの`State`列は、クエリの実行中に継続的に更新されません。 TiDBは並列クエリをサポートしているため、各ステートメントは一度に複数の*状態*になる可能性があり、したがって、単一の値に単純化することは困難です。

## SQLコミットの実行優先度を制御または変更するにはどうすればよいですか？ {#how-to-control-or-change-the-execution-priority-of-sql-commits}

[グローバル](/tidb-configuration-file.md#force-priority) [セッションごと](/system-variables.md#tidb_force_priority)または個別のステートメントに基づいて優先度を変更することをサポートしています。優先度には次の意味があります。

-   `HIGH_PRIORITY` ：このステートメントの優先度は高くなります。つまり、TiDBはこのステートメントを優先し、最初に実行します。

-   `LOW_PRIORITY` ：このステートメントの優先度は低くなります。つまり、TiDBは実行期間中にこのステートメントの優先度を下げます。

上記の2つのパラメータをTiDBのDMLと組み合わせて使用できます。例えば：

1.  データベースにSQLステートメントを記述して、優先度を調整します。

    {{< copyable "" >}}

    ```sql
    select HIGH_PRIORITY | LOW_PRIORITY count(*) from table_name;
    insert HIGH_PRIORITY | LOW_PRIORITY into table_name insert_values;
    delete HIGH_PRIORITY | LOW_PRIORITY from table_name;
    update HIGH_PRIORITY | LOW_PRIORITY table_reference set assignment_list where where_condition;
    replace HIGH_PRIORITY | LOW_PRIORITY into table_name;
    ```

2.  全表スキャンステートメントは、自動的に低い優先度に調整されます。デフォルトでは、 `analyze`の優先度は低くなっています。

## TiDBでの<code>auto analyze</code>のトリガー戦略は何ですか？ {#what-s-the-trigger-strategy-for-code-auto-analyze-code-in-tidb}

トリガー戦略： `auto analyze`は、新しいテーブルの行数が1000に達し、このテーブルに1分以内に書き込み操作がない場合に自動的にトリガーされます。

変更された数または現在の合計行数が`tidb_auto_analyze_ratio`より大きい場合、 `analyze`ステートメントが自動的にトリガーされます。デフォルト値の`tidb_auto_analyze_ratio`は0.5で、この機能がデフォルトで有効になっていることを示します。安全性を確保するために、機能が有効になっているときの最小値は0.3であり、デフォルト値が0.8である`pseudo-estimate-ratio`より小さくする必要があります。そうでない場合、疑似統計が一定期間使用されます。 `tidb_auto_analyze_ratio`を0.5に設定することをお勧めします。

自動分析は、システム変数`tidb_enable_auto_analyze`を使用して無効にできます。

## ヒントを使用してオプティマイザーの動作をオーバーライドできますか？ {#can-i-use-hints-to-override-the-optimizer-behavior}

TiDBは、 [ヒント](/optimizer-hints.md)と[SQL計画管理](/sql-plan-management.md)を含む、デフォルトのクエリオプティマイザの動作をオーバーライドする複数の方法をサポートしています。基本的な使用法はMySQLに似ていますが、いくつかのTiDB固有の拡張機能があります。

{{< copyable "" >}}

```sql
SELECT column_name FROM table_name USE INDEX（index_name）WHERE where_condition;
```

## <code>Information schema is changed</code>というエラーが報告されるのはなぜですか？ {#why-the-code-information-schema-is-changed-code-error-is-reported}

TiDBは、 `schema`回を使用してSQLステートメントを処理し、オンライン非同期DDL変更をサポートします。 DMLステートメントとDDLステートメントは同時に実行される可能性があり、各ステートメントが同じ`schema`を使用して実行されることを確認する必要があります。したがって、DML操作が進行中のDDL操作と一致すると、 `Information schema is changed`エラーが報告される場合があります。 DML操作中のエラー報告が多すぎるのを防ぐために、いくつかの改善が行われました。

現在、このエラー報告にはまだいくつかの理由があります（最初の1つだけがテーブルに関連しています）：

-   DML操作に関係するいくつかのテーブルは、進行中のDDL操作に関係するテーブルと同じです。
-   DML操作は長時間続きます。この期間中に、多くのDDLステートメントが実行されたため、1024を超える`schema`バージョンの変更が発生します。 `tidb_max_delta_schema_count`変数を変更することにより、このデフォルト値を変更できます。
-   DML要求を受け入れるTiDBサーバーは、 `schema information`を長時間ロードできません（TiDBとPDまたはTiKV間の接続障害が原因である可能性があります）。この期間中に、多くのDDLステートメントが実行されたため、100を超える`schema`バージョンの変更が発生しました。
-   TiDBの再起動後、最初のDDL操作が実行される前に、DML操作が実行され、最初のDDL操作が発生します（つまり、最初のDDL操作が実行される前に、DMLに対応するトランザクションが開始されます。最初の`schema`バージョンの後DDLが変更され、DMLに対応するトランザクションがコミットされた場合、このDML操作はこのエラーを報告します。

> **ノート：**
>
> -   現在、TiDBは`schema`のバージョンの変更をすべてキャッシュしているわけではありません。
> -   DDL操作ごとに、 `schema`のバージョン変更の数は、対応する`schema state`のバージョン変更の数と同じです。
> -   DDL操作が異なると、 `schema`バージョンの変更の数も異なります。たとえば、 `CREATE TABLE`ステートメントは1つの`schema`バージョン変更を引き起こし、 `ADD COLUMN`ステートメントは4つを引き起こします。

## 「情報スキーマが古くなっています」エラーの原因は何ですか？ {#what-are-the-causes-of-the-information-schema-is-out-of-date-error}

DMLステートメントの実行時に、TiDBがDDLリース内の最新のスキーマ（デフォルトでは45秒）のロードに失敗すると、 `Information schema is out of date`エラーが発生する可能性があります。考えられる原因は次のとおりです。

-   このDMLを実行したTiDBインスタンスが強制終了され、このDMLステートメントに対応するトランザクションの実行にDDLリースよりも時間がかかりました。トランザクションがコミットされたときに、エラーが発生しました。
-   このDMLステートメントの実行中に、TiDBがPDまたはTiKVに接続できませんでした。その結果、キープアライブ設定が原因で、TiDBがDDLリース内のスキーマのロードに失敗したか、PDから切断されました。

## 高い同時実行性でDDLステートメントを実行するとエラーが報告されますか？ {#error-is-reported-when-executing-ddl-statements-under-high-concurrency}

高い同時実行性でDDLステートメント（バッチでのテーブルの作成など）を実行すると、同時実行中のキーの競合が原因で、これらのステートメントのごく一部が失敗する可能性があります。

同時DDLステートメントの数を20未満に保つことをお勧めします。それ以外の場合は、失敗したステートメントをクライアントから再試行する必要があります。

## SQLの最適化 {#sql-optimization}

### TiDB実行プランの説明 {#tidb-execution-plan-description}

[クエリ実行プランを理解する](/explain-overview.md)を参照してください。

### 統計収集 {#statistics-collection}

[統計入門](/statistics.md)を参照してください。

### <code>select count(1)</code>を最適化する方法は？ {#how-to-optimize-code-select-count-1-code}

`count(1)`ステートメントは、テーブル内の行の総数をカウントします。並行性の程度を改善すると、速度を大幅に向上させることができます。並行性を変更するには、 [資料](/system-variables.md#tidb_distsql_scan_concurrency)を参照してください。ただし、CPUとI/Oリソースにも依存します。 TiDBは、すべてのクエリでTiKVにアクセスします。データ量が少ない場合、すべてのMySQLはメモリ内にあり、TiDBはネットワークアクセスを実行する必要があります。

推奨事項：

1.  ハードウェア構成を改善します。 [ソフトウェアとハードウェアの要件](/hardware-and-software-requirements.md)を参照してください。
2.  並行性を改善します。デフォルト値は10です。50に改善して試してみることができます。ただし、通常、改善はデフォルト値の2〜4倍です。
3.  大量のデータの場合は`count`をテストします。
4.  TiKV構成を最適化します。 [TiKVスレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md)と[TiKVメモリパフォーマンスの調整](/tune-tikv-memory-performance.md)を参照してください。
5.  [コプロセッサーキャッシュ](/coprocessor-cache.md)を有効にします。

### 現在のDDLジョブの進行状況を表示するにはどうすればよいですか？ {#how-to-view-the-progress-of-the-current-ddl-job}

`admin show ddl`を使用して、現在のDDLジョブの進行状況を表示できます。操作は次のとおりです。

{{< copyable "" >}}

```sql
admin show ddl;
```

```
*************************** 1. row ***************************
  SCHEMA_VER: 140
       OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
     SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
```

上記の結果から、 `add index`の操作が現在処理されていることがわかります。また、 `RUNNING_JOBS`列の`RowCount`フィールドから、 `add index`操作で77312行のインデックスが追加されたことを確認できます。

### DDLジョブを表示する方法は？ {#how-to-view-the-ddl-job}

-   `admin show ddl` ：実行中のDDLジョブを表示します
-   `admin show ddl jobs` ：現在のDDLジョブキュー（実行中および実行を待機しているタスクを含む）のすべての結果と、完了したDDLジョブキューの最後の10件の結果を表示します。
-   `admin show ddl job queries 'job_id' [, 'job_id'] ...` ： `job_id`に対応するDDLタスクの元のSQLステートメントを表示します。 `job_id`は実行中のDDLジョブのみを検索し、最後の10件はDDL履歴ジョブキューになります。

### TiDBはCBO（コストベースの最適化）をサポートしていますか？はいの場合、どの程度ですか？ {#does-tidb-support-cbo-cost-based-optimization-if-yes-to-what-extent}

はい。 TiDBはコストベースのオプティマイザを使用します。コストモデルと統計は常に最適化されています。 TiDBは、ハッシュ結合やソートマージ結合などの結合アルゴリズムもサポートしています。

### テーブルに対して<code>analyze</code>を実行する必要があるかどうかを判断するにはどうすればよいですか？ {#how-to-determine-whether-i-need-to-execute-code-analyze-code-on-a-table}

`show stats_healthy`を使用して`Healthy`フィールドをビューします。通常、フィールド値が60より小さい場合は、テーブルで`analyze`を実行する必要があります。

### クエリプランがツリーとして表示される場合のIDルールとは何ですか？このツリーの実行順序は何ですか？ {#what-is-the-id-rule-when-a-query-plan-is-presented-as-a-tree-what-is-the-execution-order-for-this-tree}

これらのIDにはルールはありませんが、IDは一意です。 IDが生成されると、カウンターが機能し、1つのプランが生成されるとカウンターが追加されます。実行順序はIDとは関係ありません。クエリプラン全体がツリーであり、実行プロセスはルートノードから開始され、データは継続的に上位レベルに返されます。クエリプランの詳細については、 [TiDBクエリ実行プランを理解する](/explain-overview.md)を参照してください。

### TiDBクエリプランでは、 <code>cop</code>タスクは同じルートにあります。それらは同時に実行されますか？ {#in-the-tidb-query-plan-code-cop-code-tasks-are-in-the-same-root-are-they-executed-concurrently}

現在、TiDBのコンピューティングタスクは、 `cop task`と`root task`の2つの異なるタイプのタスクに属しています。

`cop task`は、分散実行のためにKV側にプッシュダウンされるコンピューティングタスクです。 `root task`は、TiDB側でのシングルポイント実行の計算タスクです。

通常、 `root task`の入力データは`cop task`から取得されます。 `root task`がデータを処理する場合、 `cop task`のTiKVが同時にデータを処理し、 `root task`のTiDBがプルされるのを待ちます。したがって、 `cop`個のタスクが同時に実行されたと見なすことができます。しかし、それらのデータにはアップストリームとダウンストリームの関係があります。実行プロセス中、それらはしばらくの間同時に実行されます。たとえば、最初の`cop task`は[100、200]のデータを処理し、次の`cop task`は[1、100]のデータを処理しています。詳細については、 [TiDBクエリプランを理解する](/explain-overview.md)を参照してください。

## データベースの最適化 {#database-optimization}

### TiDBオプションの編集 {#edit-tidb-options}

[TiDBコマンドオプション](/command-line-flags-for-tidb-configuration.md)を参照してください。

### ホットスポットを分散させる方法は？ {#how-to-scatter-the-hotspots}

TiDBでは、データは管理のためにリージョンに分割されます。一般に、TiDBホットスポットとは、リージョン内の読み取り/書き込みホットスポットを意味します。 TiDBでは、主キー（PK）が整数ではないテーブル、またはPKがないテーブルの場合、リージョンのホットスポットを分散するように`SHARD_ROW_ID_BITS`を構成することで、リージョンを適切に分割できます。詳細については、 `SHARD_ROW_ID_BITS`の紹介を参照して[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 。

### TiKVのパフォーマンスを調整する {#tune-tikv-performance}

[TiKVスレッドのパフォーマンスを調整する](/tune-tikv-thread-performance.md)と[TiKVメモリパフォーマンスの調整](/tune-tikv-memory-performance.md)を参照してください。
