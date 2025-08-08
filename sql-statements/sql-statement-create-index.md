---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: TiDB データベースの CREATE INDEX の使用法の概要。
---

# インデックスの作成 {#create-index}

This statement adds a new index to an existing table. It is an alternative syntax to [`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-alter-table.md), and included for MySQL compatibility.

## 概要 {#synopsis}

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
|   ("VISIBLE" | "INVISIBLE")
|   ("GLOBAL" | "LOCAL")

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

## 表現インデックス {#expression-index}

クエリのフィルタリング条件が特定の式に基づいているシナリオもあります。このようなシナリオでは、通常のインデックスが機能せず、テーブル全体をスキャンしてクエリを実行する必要があるため、クエリのパフォーマンスが比較的低下します。式インデックスは、式に基づいて作成できる特殊なインデックスの一種です。式インデックスを作成すると、TiDBは式ベースのクエリにそのインデックスを使用できるため、クエリのパフォーマンスが大幅に向上します。

たとえば、 `LOWER(col1)`に基づいてインデックスを作成する場合は、次の SQL ステートメントを実行します。

```sql
CREATE INDEX idx1 ON t1 ((LOWER(col1)));
```

または、次の同等のステートメントを実行することもできます。

```sql
ALTER TABLE t1 ADD INDEX idx1((LOWER(col1)));
```

テーブルを作成するときに式インデックスを指定することもできます。

```sql
CREATE TABLE t1 (
    col1 CHAR(10), 
    col2 CHAR(10),
    INDEX ((LOWER(col1)))
);
```

> **注記：**
>
> 式インデックス内の式は`(`と`)`で囲む必要があります。囲まない場合は構文エラーが発生します。

通常のインデックスを削除するのと同じ方法で、式インデックスを削除できます。

```sql
DROP INDEX idx1 ON t1;
```

Expression index involves various kinds of expressions. To ensure correctness, only some fully tested functions are allowed for creating an expression index. This means that only these functions are allowed in expressions in a production environment. You can get these functions by querying the [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520) variable. Currently, the allowed functions are as follows:

-   [`JSON_ARRAY()`](/functions-and-operators/json-functions.md)
-   [`JSON_ARRAY_APPEND()`](/functions-and-operators/json-functions.md)
-   [`JSON_ARRAY_INSERT()`](/functions-and-operators/json-functions.md)
-   [`JSON_CONTAINS()`](/functions-and-operators/json-functions.md)
-   [`JSON_CONTAINS_PATH()`](/functions-and-operators/json-functions.md)
-   [`JSON_DEPTH()`](/functions-and-operators/json-functions.md)
-   [`JSON_EXTRACT()`](/functions-and-operators/json-functions.md)
-   [`JSON_INSERT()`](/functions-and-operators/json-functions.md)
-   [`JSON_KEYS()`](/functions-and-operators/json-functions.md)
-   [`JSON_LENGTH()`](/functions-and-operators/json-functions.md)
-   [`JSON_MERGE_PATCH()`](/functions-and-operators/json-functions.md)
-   [`JSON_MERGE_PRESERVE()`](/functions-and-operators/json-functions.md)
-   [`JSON_OBJECT()`](/functions-and-operators/json-functions.md)
-   [`JSON_PRETTY()`](/functions-and-operators/json-functions.md)
-   [`JSON_QUOTE()`](/functions-and-operators/json-functions.md)
-   [`JSON_REMOVE()`](/functions-and-operators/json-functions.md)
-   [`JSON_REPLACE()`](/functions-and-operators/json-functions.md)
-   [`JSON_SCHEMA_VALID()`](/functions-and-operators/json-functions/json-functions-validate.md)
-   [`JSON_SEARCH()`](/functions-and-operators/json-functions.md)
-   [`JSON_SET()`](/functions-and-operators/json-functions.md)
-   [`JSON_STORAGE_SIZE()`](/functions-and-operators/json-functions.md)
-   [`JSON_TYPE()`](/functions-and-operators/json-functions.md)
-   [`JSON_UNQUOTE()`](/functions-and-operators/json-functions.md)
-   [`JSON_VALID()`](/functions-and-operators/json-functions.md)
-   [`LOWER()`](/functions-and-operators/string-functions.md#lower)
-   [`MD5()`](/functions-and-operators/encryption-and-compression-functions.md)
-   [`REVERSE()`](/functions-and-operators/string-functions.md#reverse)
-   [`TIDB_SHARD()`](/functions-and-operators/tidb-functions.md#tidb_shard)
-   [`UPPER()`](/functions-and-operators/string-functions.md#upper)
-   [`VITESS_HASH()`](/functions-and-operators/tidb-functions.md)

上記のリストに含まれていない関数は、十分にテストされていないため、本番環境での使用は推奨されません。これは実験的とみなされます。演算子、 `CAST`などの他`CASE WHEN`式も実験的とみなされ、本番環境での本番は推奨されません。

<CustomContent platform="tidb">

それでもこれらの式を使用したい場合は、 [TiDB構成ファイル](/tidb-configuration-file.md#allow-expression-index-new-in-v400)で次の設定を行うことができます。

```sql
allow-expression-index = true
```

</CustomContent>

> **注記：**
>
> 主キーに式インデックスを作成することはできません。
>
> 式インデックス内の式には、次の内容を含めることはできません。
>
> -   `RAND()`や`NOW()`などの揮発性関数。
> -   [システム変数](/system-variables.md)と[ユーザー変数](/user-defined-variables.md) 。
> -   サブクエリ。
> -   [`AUTO_INCREMENT`](/auto-increment.md)列。この制限は、システム変数[`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated)の値を`true`に設定することで解除できます。
> -   [ウィンドウ関数](/functions-and-operators/window-functions.md) 。
> -   ROW関数(例: `CREATE TABLE t (j JSON, INDEX k (((j,j))));` )。
> -   [集計関数](/functions-and-operators/aggregate-group-by-functions.md) 。
>
> 式インデックスは暗黙的に名前（例： `_V$_{index_name}_{index_offset}` ）を取得します。列に既に設定されている名前で新しい式インデックスを作成しようとすると、エラーが発生します。また、同じ名前の新しい列を追加した場合もエラーが発生します。
>
> 式インデックスの式内の関数パラメータの数が正しいことを確認してください。
>
> インデックスの式に文字列関連の関数が含まれており、戻り値の型と長さの影響を受ける場合、式インデックスの作成に失敗する可能性があります。このような状況では、関数`CAST()`使用して、戻り値の型と長さを明示的に指定できます。例えば、式`REPEAT(a, 3)`に基づいて式インデックスを作成するには、この式を`CAST(REPEAT(a, 3) AS CHAR(20))`に変更する必要があります。

クエリ文内の式が式インデックス内の式と一致する場合、オプティマイザはクエリに対して式インデックスを選択できます。ただし、統計情報によっては、オプティマイザが式インデックスを選択しない場合もあります。このような場合は、オプティマイザヒントを使用することで、オプティマイザに式インデックスを選択させることができます。

次の例では、式`LOWER(col1)`に式インデックス`idx`作成するとします。

クエリ文の結果が同じ式である場合、式インデックスが適用されます。次の文を例に挙げます。

```sql
SELECT LOWER(col1) FROM t;
```

フィルタリング条件に同じ式が含まれている場合、式インデックスが適用されます。以下の文を例に挙げます。

```sql
SELECT * FROM t WHERE LOWER(col1) = "a";
SELECT * FROM t WHERE LOWER(col1) > "a";
SELECT * FROM t WHERE LOWER(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE LOWER(col1) IN ("a", "b");
SELECT * FROM t WHERE LOWER(col1) > "a" AND LOWER(col1) < "b";
SELECT * FROM t WHERE LOWER(col1) > "b" OR LOWER(col1) < "a";
```

クエリが同じ式でソートされている場合、式インデックスが適用されます。次の文を例に挙げましょう。

```sql
SELECT * FROM t ORDER BY LOWER(col1);
```

同じ式が集約関数（ `GROUP BY` ）に含まれている場合、式のインデックスが適用されます。次の文を例に挙げましょう。

```sql
SELECT MAX(LOWER(col1)) FROM t;
SELECT MIN(col1) FROM t GROUP BY LOWER(col1);
```

式インデックスに対応する式を確認するには、 [`SHOW INDEX`](/sql-statements/sql-statement-show-indexes.md)実行するか、システムテーブル[`information_schema.tidb_indexes`](/information-schema/information-schema-tidb-indexes.md)とテーブル[`information_schema.STATISTICS`](/information-schema/information-schema-statistics.md)を確認してください。出力の`Expression`列が対応する式を示します。式以外のインデックスの場合、この列には`NULL`表示されます。

式インデックスの維持コストは、行が挿入または更新されるたびに式の値を計算する必要があるため、他のインデックスの維持コストよりも高くなります。式の値は既にインデックスに格納されているため、オプティマイザが式インデックスを選択する際に再計算する必要はありません。

したがって、クエリのパフォーマンスが挿入および更新のパフォーマンスを上回る場合は、式のインデックス作成を検討できます。

式インデックスはMySQLと同じ構文と制限事項を持ちます。生成された仮想列（非表示）にインデックスを作成することで実装されるため、サポートされる式はすべて[仮想生成列の制限](/generated-columns.md#limitations)継承します。

## 多値インデックス {#multi-valued-indexes}

多値インデックスは、配列の列に定義されるセカンダリインデックスの一種です。通常のインデックスでは、1つのインデックスレコードが1つのデータレコードに対応します（1:1）。多値インデックスでは、複数のインデックスレコードが1つのデータレコードに対応します（N:1）。多値インデックスはJSON配列のインデックス作成に使用されます。例えば、 `zipcode`フィールドに多値インデックスを定義すると、配列`zipcode`各要素に対して1つのインデックスレコードが生成されます。

```json
{
    "user":"Bob",
    "user_id":31,
    "zipcode":[94477,94536]
}
```

### 複数値インデックスを作成する {#create-multi-valued-indexes}

式インデックスを作成する場合と同様に、インデックス定義で[`CAST(... AS ... ARRAY)`](/functions-and-operators/cast-functions-and-operators.md#cast)関数を使用して、複数値インデックスを作成できます。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips((CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

複数値インデックスを一意のインデックスとして定義できます。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    UNIQUE INDEX zips( (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

複数値インデックスが一意のインデックスとして定義されている場合、重複するデータを挿入しようとするとエラーが報告されます。

```sql
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1,2]}');
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [2,3]}');
ERROR 1062 (23000): Duplicate entry '2' for key 'customers.zips'
```

同じレコードに重複した値が存在する可能性がありますが、異なるレコードに重複した値が存在する場合はエラーが報告されます。

```sql
-- Insert succeeded
mysql> INSERT INTO t1 VALUES('[1,1,2]');
mysql> INSERT INTO t1 VALUES('[3,3,3,4,4,4]');

-- Insert failed
mysql> INSERT INTO t1 VALUES('[1,2]');
mysql> INSERT INTO t1 VALUES('[2,3]');
```

複数値インデックスを複合インデックスとして定義することもできます。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

複数値インデックスが複合インデックスとして定義されている場合、複数値部分は任意の位置に出現できますが、出現できるのは 1 回だけです。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)), (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
ERROR 1235 (42000): This version of TiDB doesn't yet support 'more than one multi-valued key part per index'.
```

書き込まれるデータは、複数値インデックスで定義された型と完全に一致する必要があります。一致しない場合、データの書き込みは失敗します。

```sql
-- All elements in the zipcode field must be the UNSIGNED type.
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [-1]}');
ERROR 3752 (HY000): Value is out of range for expression index 'zips' at row 1

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": ["1"]}'); -- Incompatible with MySQL
ERROR 3903 (HY000): Invalid JSON value for CAST for expression index 'zips'

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1]}');
Query OK, 1 row affected (0.00 sec)
```

### 複数値インデックスを使用する {#use-multi-valued-indexes}

詳細は[インデックスの選択 - 複数値インデックスを使用する](/choose-index.md#use-multi-valued-indexes)ご覧ください。

### Limitations {#limitations}

-   For an empty JSON array, no corresponding index record is generated.
-   The target type in `CAST(... AS ... ARRAY)` cannot be any of `BINARY`, `JSON`, `YEAR`, `FLOAT`, and `DECIMAL`. The source type must be JSON.
-   You cannot use multi-valued indexes for sorting.
-   You can only create multi-valued indexes on a JSON array.
-   A multi-valued index cannot be a primary key or a foreign key.
-   The extra storage space used by a multi-valued index = the average number of array elements per row * the space used by a normal secondary index.
-   Compared with normal indexes, DML operations will modify more index records for multi-valued indexes, so multi-valued indexes will have a greater performance impact than normal indexes.
-   Because multi-valued indexes are a special type of expression index, multi-valued indexes have the same limitations as expression indexes.
-   If a table uses multi-valued indexes, you cannot back up, replicate, or import the table using BR, TiCDC, or TiDB Lightning to a TiDB cluster earlier than v6.6.0.
-   複雑な条件を持つクエリの場合、TiDBは複数値インデックスを選択できない可能性があります。複数値インデックスでサポートされる条件パターンについては、 [複数値インデックスを使用する](/choose-index.md#use-multi-valued-indexes)を参照してください。

## Invisible index {#invisible-index}

By default, invisible indexes are indexes that are ignored by the query optimizer:

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

TiDB v8.0.0 以降では、システム変数[`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800)変更することで、オプティマイザーが非表示のインデックスを選択するようにすることができます。

詳細は[`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)参照。

## Associated system variables {#associated-system-variables}

`CREATE INDEX`文に関連付けられているシステム変数は`tidb_ddl_enable_fast_reorg` 、 `tidb_ddl_reorg_worker_cnt` 、 `tidb_ddl_reorg_batch_size` 、 `tidb_enable_auto_increment_in_generated` 、 `tidb_ddl_reorg_priority`です。詳細は[システム変数](/system-variables.md#tidb_ddl_reorg_worker_cnt)を参照してください。

## MySQL compatibility {#mysql-compatibility}

-   TiDB supports parsing the `FULLTEXT` syntax but does not support using the `FULLTEXT`, `HASH`, and `SPATIAL` indexes.
-   TiDB accepts index types such as `HASH`, `BTREE` and `RTREE` in syntax for compatibility with MySQL, but ignores them.
-   Descending indexes are not supported (similar to MySQL 5.7).
-   `CLUSTERED`型の主キーをテーブルに追加することはサポートされていません。3 型`CLUSTERED`主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   Expression indexes are incompatible with views. When a query is executed using a view, the expression index cannot be used at the same time.
-   Expression indexes have compatibility issues with bindings. When the expression of an expression index has a constant, the binding created for the corresponding query expands its scope. For example, suppose that the expression in the expression index is `a+1`, and the corresponding query condition is `a+1 > 2`. In this case, the created binding is `a+? > ?`, which means that the query with the condition such as `a+2 > 2` is also forced to use the expression index and results in a poor execution plan. In addition, this also affects the baseline capturing and baseline evolution in SQL Plan Management (SPM).
-   多値インデックスで書き込まれるデータは、定義されたデータ型と完全に一致する必要があります。一致しない場合、データの書き込みは失敗します。詳細については、 [複数値インデックスを作成する](/sql-statements/sql-statement-create-index.md#create-multi-valued-indexes)参照してください。
-   `GLOBAL`インデックス オプションを使用して`UNIQUE KEY` [グローバルインデックス](/partitioned-table.md#global-indexes)として設定することは、 [パーティションテーブル](/partitioned-table.md)の TiDB 拡張であり、MySQL とは互換性がありません。

## See also {#see-also}

-   [インデックスの選択](/choose-index.md)
-   [インデックス問題の解決方法](/wrong-index-solution.md)
-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [インデックスの削除](/sql-statements/sql-statement-drop-index.md)
-   [インデックス名の変更](/sql-statements/sql-statement-rename-index.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
