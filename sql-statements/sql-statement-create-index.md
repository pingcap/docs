---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE INDEX for the TiDB database.
---

# インデックスの作成 {#create-index}

このステートメントは、既存のテーブルに新しいインデックスを追加します。これは`ALTER TABLE .. ADD INDEX`の代替構文であり、MySQLとの互換性のために含まれています。

## あらすじ {#synopsis}

```ebnf+diagram
CreateIndexStmt ::=
    'CREATE' IndexKeyTypeOpt 'INDEX' IfNotExists Identifier IndexTypeOpt 'ON' TableName '(' IndexPartSpecificationList ')' IndexOptionList IndexLockAndAlgorithmOpt

IndexKeyTypeOpt ::=
    ( 'UNIQUE' | 'SPATIAL' | 'FULLTEXT' )?

IfNotExists ::=
    ( 'IF' 'NOT' 'EXISTS' )?

IndexTypeOpt ::=
    IndexType?

IndexPartSpecificationList ::=
    IndexPartSpecification ( ',' IndexPartSpecification )*

IndexOptionList ::=
    IndexOption*

IndexLockAndAlgorithmOpt ::=
    ( LockClause AlgorithmClause? | AlgorithmClause LockClause? )?

IndexType ::=
    ( 'USING' | 'TYPE' ) IndexTypeName

IndexPartSpecification ::=
    ( ColumnName OptFieldLen | '(' Expression ')' ) Order

IndexOption ::=
    'KEY_BLOCK_SIZE' '='? LengthNum
|   IndexType
|   'WITH' 'PARSER' Identifier
|   'COMMENT' stringLit
|   IndexInvisible

IndexTypeName ::=
    'BTREE'
|   'HASH'
|   'RTREE'

ColumnName ::=
    Identifier ( '.' Identifier ( '.' Identifier )? )?

OptFieldLen ::=
    FieldLen?

IndexNameList ::=
    ( Identifier | 'PRIMARY' )? ( ',' ( Identifier | 'PRIMARY' ) )*

KeyOrIndex ::=
    'Key' | 'Index'
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)

mysql> CREATE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)

mysql> ALTER TABLE t1 DROP INDEX c1;
Query OK, 0 rows affected (0.30 sec)

mysql> CREATE UNIQUE INDEX c1 ON t1 (c1);
Query OK, 0 rows affected (0.31 sec)
```

## 式インデックス {#expression-index}

一部のシナリオでは、クエリのフィルタリング条件は特定の式に基づいています。これらのシナリオでは、通常のインデックスを有効にできないため、クエリのパフォーマンスは比較的低くなります。クエリは、テーブル全体をスキャンすることによってのみ実行できます。式インデックスは、式に作成できる特殊なインデックスの一種です。式インデックスが作成されると、TiDBは式ベースのクエリにインデックスを使用できるため、クエリのパフォーマンスが大幅に向上します。

たとえば、 `lower(col1)`に基づいてインデックスを作成する場合は、次のSQLステートメントを実行します。

{{< copyable "" >}}

```sql
CREATE INDEX idx1 ON t1 ((lower(col1)));
```

または、次の同等のステートメントを実行できます。

{{< copyable "" >}}

```sql
ALTER TABLE t1 ADD INDEX idx1((lower(col1)));
```

テーブルを作成するときに、式インデックスを指定することもできます。

{{< copyable "" >}}

```sql
CREATE TABLE t1(col1 char(10), col2 char(10), index((lower(col1))));
```

> **ノート**
>
> 式インデックスの式は、「（」および「）」で囲む必要があります。それ以外の場合は、構文エラーが報告されます。

通常のインデックスを削除するのと同じ方法で、式インデックスを削除できます。

{{< copyable "" >}}

```sql
DROP INDEX idx1 ON t1;
```

> **ノート：**
>
> 式インデックスには、さまざまな種類の式が含まれます。正確性を確保するために、完全にテストされた一部の関数のみが式インデックスの作成を許可されています。これは、これらの関数のみが実稼働環境の式で許可されることを意味します。これらの関数は、 `tidb_allow_function_for_expression_index`の変数をクエリすることで取得できます。将来のバージョンでは、さらに多くの機能がリストに追加される可能性があります。
>
> {{< copyable "" >}}
>
> ```sql
> mysql> select @@tidb_allow_function_for_expression_index;
> +--------------------------------------------+
> | @@tidb_allow_function_for_expression_index |
> +--------------------------------------------+
> | lower, md5, reverse, upper, vitess_hash    |
> +--------------------------------------------+
> 1 row in set (0.00 sec)
> ```
>
> 上記の戻り結果に含まれていない関数の場合、これらの関数は十分にテストされておらず、実験的ものと見なすことができる実稼働環境には推奨されません。演算子、 `cast`などの他の式も実験的ものと見`case when` 、本番環境には推奨されません。ただし、それでもこれらの式を使用する場合は、 [TiDB構成ファイル](/tidb-configuration-file.md#allow-expression-index-new-in-v400)で次の構成を行うことができます。
>
> {{< copyable "" >}}
>
> ```sql
> allow-expression-index = true
> ```
>
> 主キーに式インデックスを作成することはできません。
>
> 式インデックスの式に次の内容を含めることはできません。
>
> -   `rand()`や`now()`などの揮発性関数。
> -   システム変数とユーザー変数。
> -   サブクエリ。
> -   `AUTO_INCREMENT`列。 `tidb_enable_auto_increment_in_generated` （システム変数）の値を`true`に設定することで、この制限を取り除くことができます。
> -   ウィンドウ関数。
> -   `create table t (j json, key k (((j,j))));`などのROW関数。
> -   集計関数。
>
> 式インデックスは暗黙的に名前を取ります（たとえば、 `_V$_{index_name}_{index_offset}` ）。列にすでにある名前で新しい式インデックスを作成しようとすると、エラーが発生します。また、同じ名前の新しい列を追加すると、エラーも発生します。
>
> 式インデックスの式の関数パラメータの数が正しいことを確認してください。
>
> インデックスの式に、返されるタイプと長さの影響を受ける文字列関連の関数が含まれている場合、式インデックスの作成が失敗する可能性があります。この状況では、 `cast()`関数を使用して、返されるタイプと長さを明示的に指定できます。たとえば、 `repeat(a, 3)`式に基づいて式インデックスを作成するには、この式を`cast(repeat(a, 3) as char(20))`に変更する必要があります。

クエリステートメントの式が式インデックスの式と一致する場合、オプティマイザはクエリの式インデックスを選択できます。統計によっては、オプティマイザが式インデックスを選択しない場合があります。この状況では、オプティマイザのヒントを使用して、オプティマイザに式インデックスを選択させることができます。

次の例では、式`lower(col1)`に式インデックス`idx`を作成するとします。

クエリステートメントの結果が同じ式である場合、式インデックスが適用されます。例として、次のステートメントを取り上げます。

{{< copyable "" >}}

```sql
SELECT lower(col1) FROM t;
```

同じ式がフィルタリング条件に含まれている場合、式インデックスが適用されます。例として、次のステートメントを取り上げます。

{{< copyable "" >}}

```sql
SELECT * FROM t WHERE lower(col1) = "a";
SELECT * FROM t WHERE lower(col1) > "a";
SELECT * FROM t WHERE lower(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE lower(col1) in ("a", "b");
SELECT * FROM t WHERE lower(col1) > "a" AND lower(col1) < "b";
SELECT * FROM t WHERE lower(col1) > "b" OR lower(col1) < "a";
```

クエリが同じ式でソートされている場合、式インデックスが適用されます。例として、次のステートメントを取り上げます。

{{< copyable "" >}}

```sql
SELECT * FROM t ORDER BY lower(col1);
```

同じ式がaggregate（ `GROUP BY` ）関数に含まれている場合、式インデックスが適用されます。例として、次のステートメントを取り上げます。

{{< copyable "" >}}

```sql
SELECT max(lower(col1)) FROM t；
SELECT min(col1) FROM t GROUP BY lower(col1);
```

式インデックスに対応する式を確認するには、 `show index`を実行するか、システムテーブル`information_schema.tidb_indexes`とテーブル`information_schema.STATISTICS`を確認してください。出力の`Expression`列は、対応する式を示しています。非式インデックスの場合、列には`NULL`が表示されます。

行が挿入または更新されるたびに式の値を計算する必要があるため、式インデックスを維持するコストは他のインデックスを維持するコストよりも高くなります。式の値はすでにインデックスに格納されているため、オプティマイザが式のインデックスを選択するときに、この値を再計算する必要はありません。

したがって、クエリのパフォーマンスが挿入と更新のパフォーマンスを上回っている場合は、式のインデックス作成を検討できます。

式インデックスには、MySQLと同じ構文と制限があります。これらは、生成された非表示の仮想列にインデックスを作成することで実装されるため、サポートされている式はすべて[仮想生成列の制限](/generated-columns.md#limitations)を継承します。

## 見えないインデックス {#invisible-index}

非表示のインデックスは、クエリオプティマイザによって無視されるインデックスです。

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

詳細については、 [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)を参照してください。

## 関連するシステム変数 {#associated-system-variables}

`CREATE INDEX`ステートメントに関連付けられているシステム変数は、 `tidb_ddl_reorg_worker_cnt` 、 `tidb_ddl_reorg_priority` `tidb_ddl_reorg_batch_size` `tidb_enable_auto_increment_in_generated`詳細は[システム変数](/system-variables.md#tidb_ddl_reorg_worker_cnt)を参照してください。

## MySQLの互換性 {#mysql-compatibility}

-   `FULLTEXT` 、および`HASH`のインデックスはサポートさ`SPATIAL`ていません。
-   降順インデックスはサポートされていません（MySQL 5.7と同様）。
-   `CLUSTERED`タイプの主キーをテーブルに追加することはサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化されたインデックス](/clustered-indexes.md)を参照してください。
-   式インデックスはビューと互換性がありません。ビューを使用してクエリを実行する場合、式インデックスを同時に使用することはできません。
-   式インデックスには、バインディングとの互換性の問題があります。式インデックスの式に定数がある場合、対応するクエリに対して作成されたバインディングはそのスコープを拡張します。たとえば、式インデックスの式が`a+1`であり、対応するクエリ条件が`a+1 > 2`であるとします。この場合、作成されたバインディングは`a+? > ?`です。これは、 `a+2 > 2`などの条件を持つクエリも式インデックスを使用するように強制され、実行プランが不十分になることを意味します。さらに、これはSQL Plan Management（SPM）のベースラインキャプチャとベースラインの進化にも影響します。

## も参照してください {#see-also}

-   [インデックスの選択](/choose-index.md)
-   [インデックス問題の解決方法](/wrong-index-solution.md)
-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [ドロップインデックス](/sql-statements/sql-statement-drop-index.md)
-   [インデックスの名前を変更](/sql-statements/sql-statement-rename-index.md)
-   [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
-   [説明](/sql-statements/sql-statement-explain.md)
