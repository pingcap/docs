---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE INDEX for the TiDB database.
---

# インデックスの作成 {#create-index}

このステートメントは、既存のテーブルに新しいインデックスを追加します。これは`ALTER TABLE .. ADD INDEX`の代替構文であり、MySQL との互換性のために組み込まれています。

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

一部のシナリオでは、クエリのフィルター条件は特定の式に基づきます。これらのシナリオでは、通常のインデックスが有効にならず、テーブル全体をスキャンすることによってのみクエリを実行できるため、クエリのパフォーマンスが比較的低くなります。式インデックスは、式に対して作成できる特殊なインデックスの一種です。式インデックスが作成されると、TiDB はそのインデックスを式ベースのクエリに使用できるようになり、クエリのパフォーマンスが大幅に向上します。

たとえば、 `lower(col1)`に基づいてインデックスを作成する場合は、次の SQL ステートメントを実行します。

```sql
CREATE INDEX idx1 ON t1 ((lower(col1)));
```

または、次の同等のステートメントを実行することもできます。

```sql
ALTER TABLE t1 ADD INDEX idx1((lower(col1)));
```

テーブルの作成時に式インデックスを指定することもできます。

```sql
CREATE TABLE t1(col1 char(10), col2 char(10), index((lower(col1))));
```

> **注記：**
>
> 式インデックス内の式は、 `(`と`)`で囲む必要があります。それ以外の場合は、構文エラーが報告されます。

式インデックスは、通常のインデックスを削除するのと同じ方法で削除できます。

```sql
DROP INDEX idx1 ON t1;
```

表現インデックスにはさまざまな種類の表現が含まれます。正確性を確保するために、完全にテストされた一部の関数のみが式インデックスの作成に使用できます。これは、本番環境の式ではこれらの関数のみが許可されることを意味します。これらの関数は、 `tidb_allow_function_for_expression_index`変数をクエリすることで取得できます。現在、許可されている関数は次のとおりです。

    json_array, json_array_append, json_array_insert, json_contains, json_contains_path, json_depth, json_extract, json_insert, json_keys, json_length, json_merge_patch, json_merge_preserve, json_object, json_pretty, json_quote, json_remove, json_replace, json_search, json_set, json_storage_size, json_type, json_unquote, json_valid, lower, md5, reverse, tidb_shard, upper, vitess_hash

上記のリストに含まれていない関数については、完全にはテストされて関数ず、実験的とみなされるため、本番環境では推奨されません。演算子、 `cast` 、 `case when`などの他の式も実験的ものとみなされ、本番では推奨されません。

<CustomContent platform="tidb">

これらの式を引き続き使用したい場合は、 [TiDB 設定ファイル](/tidb-configuration-file.md#allow-expression-index-new-in-v400)で次の構成を行うことができます。

```sql
allow-expression-index = true
```

</CustomContent>

> **注記：**
>
> 式インデックスは主キーに作成できません。
>
> 式インデックスの式には、次の内容を含めることはできません。
>
> -   `rand()`や`now()`などの揮発性関数。
> -   システム変数とユーザー変数。
> -   サブクエリ。
> -   `AUTO_INCREMENT`列。この制限を解除するには、 `tidb_enable_auto_increment_in_generated` (システム変数) の値を`true`に設定します。
> -   ウィンドウ関数。
> -   ROW関数( `create table t (j json, key k (((j,j))));`など)。
> -   集計関数。
>
> 式インデックスは暗黙的に名前を使用します (たとえば、 `_V$_{index_name}_{index_offset}` )。列に既に付けられている名前を使用して新しい式インデックスを作成しようとすると、エラーが発生します。また、同じ名前の新しい列を追加した場合もエラーが発生します。
>
> 式インデックスの式内の関数パラメータの数が正しいことを確認してください。
>
> インデックスの式に文字列関連の関数が含まれている場合、返される型と長さの影響を受けて、式インデックスの作成が失敗することがあります。この状況では、 `cast()`関数を使用して、返される型と長さを明示的に指定できます。たとえば、 `repeat(a, 3)`式に基づいて式インデックスを作成するには、この式を`cast(repeat(a, 3) as char(20))`に変更する必要があります。

クエリ ステートメントの式が式インデックスの式と一致する場合、オプティマイザはクエリの式インデックスを選択できます。場合によっては、オプティマイザは統計に応じて式インデックスを選択しないことがあります。この状況では、オプティマイザー ヒントを使用して、オプティマイザーに式インデックスを強制的に選択させることができます。

次の例では、式`lower(col1)`に式インデックス`idx`を作成すると仮定します。

クエリ ステートメントの結果が同じ式である場合、式インデックスが適用されます。次のステートメントを例として取り上げます。

```sql
SELECT lower(col1) FROM t;
```

フィルタ条件に同じ式が含まれる場合、式インデックスが適用されます。次のステートメントを例として取り上げます。

```sql
SELECT * FROM t WHERE lower(col1) = "a";
SELECT * FROM t WHERE lower(col1) > "a";
SELECT * FROM t WHERE lower(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE lower(col1) in ("a", "b");
SELECT * FROM t WHERE lower(col1) > "a" AND lower(col1) < "b";
SELECT * FROM t WHERE lower(col1) > "b" OR lower(col1) < "a";
```

クエリが同じ式で並べ替えられる場合、式インデックスが適用されます。次のステートメントを例として取り上げます。

```sql
SELECT * FROM t ORDER BY lower(col1);
```

同じ式が集計 ( `GROUP BY` )関数に含まれている場合、式インデックスが適用されます。次のステートメントを例として取り上げます。

```sql
SELECT max(lower(col1)) FROM t;
SELECT min(col1) FROM t GROUP BY lower(col1);
```

式インデックスに対応する式を確認するには、 `show index`実行するか、システム テーブル`information_schema.tidb_indexes`とテーブル`information_schema.STATISTICS`を確認します。出力の`Expression`列は、対応する式を示します。式以外のインデックスの場合、列には`NULL`が表示されます。

行が挿入または更新されるたびに式の値を計算する必要があるため、式インデックスを維持するコストは他のインデックスを維持するコストよりも高くなります。式の値はすでにインデックスに格納されているため、オプティマイザが式インデックスを選択するときにこの値を再計算する必要はありません。

したがって、クエリのパフォーマンスが挿入および更新のパフォーマンスを上回る場合は、式のインデックス作成を検討できます。

式インデックスには、MySQL と同じ構文と制限があります。これらは、生成された非表示の仮想列にインデックスを作成することによって実装されるため、サポートされる式はすべて[仮想生成列の制限事項](/generated-columns.md#limitations)を継承します。

## 多値インデックス {#multi-valued-indexes}

複数値インデックスは、配列列に定義される一種のセカンダリ インデックスです。通常のインデックスでは、1 つのインデックス レコードと 1 つのデータ レコードが 1 対 1 で対応します。多値インデックスでは、複数のインデックス レコードが 1 つのデータ レコードに対応します (N:1)。複数値インデックスは、JSON 配列のインデックス付けに使用されます。たとえば、 `zipcode`フィールドに定義された複数値インデックスは、 `zipcode`配列の要素ごとに 1 つのインデックス レコードを生成します。

```json
{
    "user":"Bob",
    "user_id":31,
    "zipcode":[94477,94536]
}
```

### 複数値のインデックスを作成する {#create-multi-valued-indexes}

複数値インデックスを作成するには、式インデックスの作成としてインデックス定義で`CAST(... AS ... ARRAY)`式を使用します。

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

複数値インデックスが一意のインデックスとして定義されている場合、重複したデータを挿入しようとするとエラーが報告されます。

```sql
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1,2]}');
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [2,3]}');
ERROR 1062 (23000): Duplicate entry '2' for key 'customers.zips'
```

同じレコードに重複値を含めることはできますが、異なるレコードに重複値がある場合はエラーが報告されます。

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

書き込まれるデータは、複数値インデックスで定義された型と正確に一致する必要があります。それ以外の場合、データの書き込みは失敗します。

```sql
-- All elements in the zipcode field must be the UNSIGNED type.
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [-1]}');
ERROR 3752 (HY000): Value is out of range for expression index 'zips' at row 1

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": ["1"]}'); -- Incompatible with MySQL
ERROR 3903 (HY000): Invalid JSON value for CAST for expression index 'zips'

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1]}');
Query OK, 1 row affected (0.00 sec)
```

### 複数値のインデックスを使用する {#use-multi-valued-indexes}

詳細については[インデックスの選択 - 複数値のインデックスを使用する](/choose-index.md#use-multi-valued-indexes)参照してください。

### 制限事項 {#limitations}

-   空の JSON 配列の場合、対応するインデックス レコードは生成されません。
-   `CAST(... AS ... ARRAY)`のターゲット タイプは、 `BINARY` 、 `JSON` 、 `YEAR` 、 `FLOAT` 、および`DECIMAL`のいずれにもできません。ソースタイプはJSONである必要があります。
-   ソートに複数値インデックスを使用することはできません。
-   複数値のインデックスは JSON 配列にのみ作成できます。
-   複数値インデックスを主キーまたは外部キーにすることはできません。
-   多値インデックスによって使用される追加のstorage域 = 行あたりの配列要素の平均数 * 通常のセカンダリ インデックスによって使用されるスペース。
-   通常のインデックスと比較して、DML 操作では複数値インデックスのより多くのインデックス レコードが変更されるため、複数値インデックスは通常のインデックスよりもパフォーマンスに大きな影響を与えます。
-   複数値インデックスは特殊なタイプの式インデックスであるため、複数値インデックスには式インデックスと同じ制限があります。
-   テーブルで複数値インデックスが使用されている場合、 BR、 TiCDC 、またはTiDB Lightningを使用してテーブルを v6.6.0 より前の TiDB クラスターにバックアップ、複製、またはインポートすることはできません。
-   多値インデックスについて収集された統計が不足しているため、現在、多値インデックスの選択率は固定の仮定に基づいています。クエリが複数の複数値インデックスにヒットすると、TiDB は最適なインデックスを選択できない可能性があります。このような場合は、 [`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)オプティマイザ ヒントを使用して固定実行計画を強制することをお勧めします。
-   複雑な条件を含むクエリの場合、TiDB は複数値のインデックスを選択できない場合があります。多値インデックスでサポートされる条件パターンについては、 [複数値のインデックスを使用する](/choose-index.md#use-multi-valued-indexes)を参照してください。

## 見えないインデックス {#invisible-index}

非表示のインデックスは、クエリ オプティマイザーによって無視されるインデックスです。

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

詳細は[`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)を参照してください。

## 関連するシステム変数 {#associated-system-variables}

`CREATE INDEX`ステートメントに関連付けられたシステム変数は`tidb_ddl_enable_fast_reorg` 、 `tidb_ddl_reorg_worker_cnt` 、 `tidb_ddl_reorg_batch_size` 、 `tidb_enable_auto_increment_in_generated` 、および`tidb_ddl_reorg_priority`です。詳細は[システム変数](/system-variables.md#tidb_ddl_reorg_worker_cnt)を参照してください。

## MySQLの互換性 {#mysql-compatibility}

-   TiDB は`FULLTEXT`および`SPATIAL`構文の解析をサポートしていますが、 `FULLTEXT` 、 `HASH` 、および`SPATIAL`インデックスの使用はサポートしていません。
-   降順インデックスはサポートされていません ( MySQL 5.7と同様)。
-   `CLUSTERED`タイプの主キーのテーブルへの追加はサポートされていません。 `CLUSTERED`種類の主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   式インデックスはビューと互換性がありません。ビューを使用してクエリを実行する場合、式インデックスを同時に使用することはできません。
-   式インデックスにはバインディングとの互換性の問題があります。式インデックスの式に定数がある場合、対応するクエリに対して作成されたバインディングのスコープが拡張されます。たとえば、式インデックスの式が`a+1`で、対応するクエリ条件が`a+1 > 2`であるとします。この場合、作成されたバインディングは`a+? > ?`です。これは、 `a+2 > 2`などの条件を持つクエリでも式インデックスの使用が強制され、不適切な実行プランが生じることを意味します。さらに、これは SQL Plan Management (SPM) のベースラインの取得とベースラインの進化にも影響します。
-   複数値インデックスを使用して書き込まれるデータは、定義されたデータ型と正確に一致する必要があります。そうしないと、データの書き込みは失敗します。詳細は[複数値のインデックスを作成する](/sql-statements/sql-statement-create-index.md#create-multi-valued-indexes)を参照してください。

## こちらも参照 {#see-also}

-   [インデックスの選択](/choose-index.md)
-   [インデックス問題の解決方法](/wrong-index-solution.md)
-   [インデックスの追加](/sql-statements/sql-statement-add-index.md)
-   [ドロップインデックス](/sql-statements/sql-statement-drop-index.md)
-   [インデックスの名前を変更](/sql-statements/sql-statement-rename-index.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
-   [列の追加](/sql-statements/sql-statement-add-column.md)
-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
