---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE INDEX for the TiDB database.
---

# インデックスを作成 {#create-index}

このステートメントは、既存のテーブルに新しいインデックスを追加します。これは`ALTER TABLE .. ADD INDEX`の代替構文であり、MySQL との互換性のために含まれています。

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

## 発現指数 {#expression-index}

一部のシナリオでは、クエリのフィルター条件が特定の式に基づいています。これらのシナリオでは、通常のインデックスが有効にならないため、クエリのパフォーマンスは比較的低く、クエリはテーブル全体をスキャンすることによってのみ実行できます。式インデックスは、式で作成できる特別なインデックスの一種です。式インデックスが作成されると、TiDB はそのインデックスを式ベースのクエリに使用できるため、クエリのパフォーマンスが大幅に向上します。

たとえば、 `lower(col1)`に基づいてインデックスを作成する場合は、次の SQL ステートメントを実行します。

{{< copyable "" >}}

```sql
CREATE INDEX idx1 ON t1 ((lower(col1)));
```

または、次の同等のステートメントを実行できます。

{{< copyable "" >}}

```sql
ALTER TABLE t1 ADD INDEX idx1((lower(col1)));
```

テーブルを作成するときに、式のインデックスを指定することもできます。

{{< copyable "" >}}

```sql
CREATE TABLE t1(col1 char(10), col2 char(10), index((lower(col1))));
```

> **ノート：**
>
> 式インデックス内の式は、 `(`と`)`で囲む必要があります。そうしないと、構文エラーが報告されます。

通常のインデックスを削除するのと同じ方法で、式のインデックスを削除できます。

{{< copyable "" >}}

```sql
DROP INDEX idx1 ON t1;
```

表現インデックスには、さまざまな種類の表現が含まれます。正確性を確保するために、完全にテストされた一部の関数のみが式インデックスの作成に使用できます。これは、これらの関数のみが本番環境の式で許可されることを意味します。これらの関数は、 `tidb_allow_function_for_expression_index`変数をクエリすることで取得できます。現在、許可されている関数は次のとおりです。

```
json_array, json_array_append, json_array_insert, json_contains, json_contains_path, json_depth, json_extract, json_insert, json_keys, json_length, json_merge_patch, json_merge_preserve, json_object, json_pretty, json_quote, json_remove, json_replace, json_search, json_set, json_storage_size, json_type, json_unquote, json_valid, lower, md5, reverse, tidb_shard, upper, vitess_hash
```

上記のリストに含まれていない関数については、それらの関数は完全にはテストされておらず、本番環境には推奨されません。これは実験的ものと見なすことができます。演算子、 `cast` 、および`case when`などの他の式も実験的ものと見なされ、本番では推奨されません。

<CustomContent platform="tidb">

これらの式を引き続き使用する場合は、 [TiDB 構成ファイル](/tidb-configuration-file.md#allow-expression-index-new-in-v400)で次の構成を行うことができます。

{{< copyable "" >}}

```sql
allow-expression-index = true
```

</CustomContent>

> **ノート：**
>
> 主キーに式インデックスを作成することはできません。
>
> 式インデックスの式には、次のコンテンツを含めることはできません:
>
> -   `rand()`や`now()`などの揮発性関数。
> -   システム変数とユーザー変数。
> -   サブクエリ。
> -   `AUTO_INCREMENT`列。 `tidb_enable_auto_increment_in_generated` (システム変数) の値を`true`に設定すると、この制限を取り除くことができます。
> -   ウィンドウ関数。
> -   `create table t (j json, key k (((j,j))));`などの ROW関数。
> -   集約関数。
>
> 式のインデックスは暗黙的に名前 ( `_V$_{index_name}_{index_offset}`など) を使用します。列に既に付けられている名前で新しい式インデックスを作成しようとすると、エラーが発生します。また、同じ名前の新しい列を追加すると、エラーが発生します。
>
> 式インデックスの式の関数パラメーターの数が正しいことを確認してください。
>
> インデックスの式に文字列関連の関数が含まれている場合、返される型と長さの影響を受けて、式インデックスの作成に失敗することがあります。この状況では、 `cast()`関数を使用して、返される型と長さを明示的に指定できます。たとえば、式`repeat(a, 3)`に基づいて式インデックスを作成するには、この式を`cast(repeat(a, 3) as char(20))`に変更する必要があります。

クエリ ステートメントの式が式インデックスの式と一致する場合、オプティマイザはクエリの式インデックスを選択できます。統計によっては、オプティマイザーが式インデックスを選択しない場合があります。この状況では、オプティマイザ ヒントを使用して、オプティマイザに強制的に式インデックスを選択させることができます。

次の例では、式`lower(col1)`に式インデックス`idx`を作成するとします。

クエリ ステートメントの結果が同じ式である場合は、式のインデックスが適用されます。例として、次のステートメントを取り上げます。

{{< copyable "" >}}

```sql
SELECT lower(col1) FROM t;
```

絞り込み条件に同じ表現が含まれる場合は、表現インデックスが適用されます。例として、次のステートメントを取り上げます。

{{< copyable "" >}}

```sql
SELECT * FROM t WHERE lower(col1) = "a";
SELECT * FROM t WHERE lower(col1) > "a";
SELECT * FROM t WHERE lower(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE lower(col1) in ("a", "b");
SELECT * FROM t WHERE lower(col1) > "a" AND lower(col1) < "b";
SELECT * FROM t WHERE lower(col1) > "b" OR lower(col1) < "a";
```

クエリが同じ式で並べ替えられている場合は、式のインデックスが適用されます。例として、次のステートメントを取り上げます。

{{< copyable "" >}}

```sql
SELECT * FROM t ORDER BY lower(col1);
```

集計 ( `GROUP BY` )関数に同じ式が含まれている場合は、式のインデックスが適用されます。例として、次のステートメントを取り上げます。

{{< copyable "" >}}

```sql
SELECT max(lower(col1)) FROM t;
SELECT min(col1) FROM t GROUP BY lower(col1);
```

式インデックスに対応する式を確認するには、 `show index`実行するか、システム テーブル`information_schema.tidb_indexes`およびテーブル`information_schema.STATISTICS`を確認します。出力の`Expression`列は、対応する式を示します。非式インデックスの場合、列には`NULL`が表示されます。

行が挿入または更新されるたびに式の値を計算する必要があるため、式インデックスを維持するコストは他のインデックスを維持するコストよりも高くなります。式の値はすでにインデックスに格納されているため、オプティマイザが式のインデックスを選択するときに、この値を再計算する必要はありません。

したがって、クエリのパフォーマンスが挿入および更新のパフォーマンスを上回る場合は、式のインデックス作成を検討できます。

式インデックスには、MySQL と同じ構文と制限があります。これらは、生成された非表示の仮想列にインデックスを作成することによって実装されるため、サポートされている式はすべて[仮想生成列の制限](/generated-columns.md#limitations)を継承します。

## 見えないインデックス {#invisible-index}

非表示のインデックスは、クエリ オプティマイザーによって無視されるインデックスです。

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

詳細については、 [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)を参照してください。

## 関連するシステム変数 {#associated-system-variables}

`CREATE INDEX`ステートメントに関連付けられているシステム変数は`tidb_ddl_enable_fast_reorg` 、 `tidb_ddl_reorg_worker_cnt` 、 `tidb_ddl_reorg_batch_size` 、 `tidb_enable_auto_increment_in_generated` 、および`tidb_ddl_reorg_priority`です。詳細は[システム変数](/system-variables.md#tidb_ddl_reorg_worker_cnt)を参照。

## MySQL の互換性 {#mysql-compatibility}

-   TiDB は`FULLTEXT`および`SPATIAL`構文の解析をサポートしていますが、 `FULLTEXT` 、 `HASH` 、および`SPATIAL`インデックスの使用はサポートしていません。
-   降順のインデックスはサポートされていません ( MySQL 5.7と同様)。
-   `CLUSTERED`タイプの主キーをテーブルに追加することはサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   式インデックスはビューと互換性がありません。ビューを使用してクエリを実行する場合、式インデックスは同時に使用できません。
-   式インデックスには、バインディングとの互換性の問題があります。式インデックスの式に定数がある場合、対応するクエリに対して作成されたバインディングはそのスコープを拡張します。たとえば、式インデックスの式が`a+1`で、対応するクエリ条件が`a+1 > 2`であるとします。この場合、作成されたバインディングは`a+? > ?`です。これは、 `a+2 > 2`などの条件を持つクエリも式インデックスを使用することを余儀なくされ、不適切な実行計画になることを意味します。さらに、これは SQL 計画管理 (SPM) でのベースラインの取得とベースラインの進化にも影響します。

## こちらもご覧ください {#see-also}

-   [インデックスの選択](/choose-index.md)
-   [インデックス問題の解決方法](/wrong-index-solution.md)
-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [ドロップインデックス](/sql-statements/sql-statement-drop-index.md)
-   [インデックスの名前を変更](/sql-statements/sql-statement-rename-index.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [テーブルを作成](/sql-statements/sql-statement-create-table.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
