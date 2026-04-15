---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: TiDBデータベースにおけるCREATE INDEXの使用方法の概要。
---

# インデックスを作成する {#create-index}

このステートメントは、既存のテーブルに新しいインデックスを追加します。これは、 [`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-alter-table.md)の代替構文であり、MySQL との互換性のために含まれています。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 4 vCPUを搭載した[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタの場合、インデックス作成中にリソース制限がクラスタの安定性に影響を与えないように、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)手動で無効にすることをお勧めします。この設定を無効にすることで、トランザクションを使用してインデックスを作成できるようになり、クラスタ全体への影響を軽減できます。

</CustomContent>

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

## 式インデックス or 関数インデックス {#expression-index}

クエリのフィルタリング条件が特定の式に基づいている場合、通常のインデックスが効果を発揮せず、テーブル全体をスキャンしてクエリを実行するしかないため、クエリのパフォーマンスは比較的低くなります。式インデックスは、式に基づいて作成できる特殊なインデックスです。式インデックスが作成されると、TiDB はそのインデックスを式ベースのクエリに使用できるようになり、クエリのパフォーマンスが大幅に向上します。

例えば、 `LOWER(col1)`に基づいてインデックスを作成する場合は、次の SQL ステートメントを実行します。

```sql
CREATE INDEX idx1 ON t1 ((LOWER(col1)));
```

または、以下の同等のステートメントを実行することもできます。

```sql
ALTER TABLE t1 ADD INDEX idx1((LOWER(col1)));
```

テーブルを作成する際に、式インデックスを指定することもできます。

```sql
CREATE TABLE t1 (
    col1 CHAR(10), 
    col2 CHAR(10),
    INDEX ((LOWER(col1)))
);
```

> **注記：**
>
> 式インデックス内の式は`(`と`)`で囲む必要があります。そうでない場合、構文エラーが報告されます。

式インデックスを削除する方法は、通常のインデックスを削除する方法と同じです。

```sql
DROP INDEX idx1 ON t1;
```

式インデックス or 関数インデックスには、さまざまな種類の式が含まれます。正確性を確保するため、式インデックスの作成には、完全にテストされた一部の関数のみが許可されています。つまり、本番環境では、これらの関数のみが式で使用できます。これらの関数は、 [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520)変数を照会することで取得できます。現在、許可されている関数は以下のとおりです。

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

上記のリストに含まれていない関数は、十分にテストされておらず、本番環境での関数は推奨されません。これらは実験的とみなされます。演算子、 `CAST` 、 `CASE WHEN`などの他の式も実験的とみなされ、本番環境での本番は推奨されません。

<CustomContent platform="tidb">

それでもこれらの式を使用したい場合は、 [TiDB設定ファイル](/tidb-configuration-file.md#allow-expression-index-new-in-v400)で次の構成を行うことができます。

```sql
allow-expression-index = true
```

</CustomContent>

> **注記：**
>
> 主キーに対して式インデックスを作成することはできません。
>
> 式インデックス内の式には、以下の内容を含めることはできません。
>
> -   `RAND()`や`NOW()`などの揮発性関数。
> -   [システム変数](/system-variables.md)と[ユーザー変数](/user-defined-variables.md)。
> -   サブクエリ。
> -   [`AUTO_INCREMENT`](/auto-increment.md)列。tidb_enable_auto_increment_in_generated (システム変数) の値を`true`に設定することで[`tidb_enable_auto_increment_in_generated`](/system-variables.md#tidb_enable_auto_increment_in_generated)この制限を解除できます。
> -   [ウィンドウ関数](/functions-and-operators/window-functions.md)。
> -   `CREATE TABLE t (j JSON, INDEX k (((j,j))));`のような ROW関数。
> -   [集計関数](/functions-and-operators/aggregate-group-by-functions.md)。
>
> 式インデックスは暗黙的に名前を取得します（例： `_V$_{index_name}_{index_offset}` ）。既に列に付けられている名前で新しい式インデックスを作成しようとすると、エラーが発生します。また、同じ名前で新しい列を追加しようとした場合も、エラーが発生します。
>
> 式インデックスの式に含まれる関数パラメータの数が正しいことを確認してください。
>
> インデックスの式に、戻り値の型と長さによって影響を受ける文字列関連の関数が含まれている場合、式インデックスの作成が失敗する可能性があります。このような場合は、 `CAST()`関数を使用して、戻り値の型と長さを明示的に指定できます。たとえば、 `REPEAT(a, 3)`式に基づいて式インデックスを作成するには、この式を`CAST(REPEAT(a, 3) AS CHAR(20))`に変更する必要があります。

クエリ文の式が式インデックスの式と一致する場合、オプティマイザはクエリに対して式インデックスを選択できます。ただし、統計情報によっては、オプティマイザが式インデックスを選択しない場合もあります。このような場合は、オプティマイザヒントを使用することで、オプティマイザに式インデックスを選択させることができます。

以下の例では、式`idx` `LOWER(col1)` } を作成するとします。

クエリ文の結果が同じ式である場合、式インデックスが適用されます。次の文を例にとります。

```sql
SELECT LOWER(col1) FROM t;
```

フィルタリング条件に同じ式が含まれている場合、式のインデックスが適用されます。以下のステートメントを例に挙げます。

```sql
SELECT * FROM t WHERE LOWER(col1) = "a";
SELECT * FROM t WHERE LOWER(col1) > "a";
SELECT * FROM t WHERE LOWER(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE LOWER(col1) IN ("a", "b");
SELECT * FROM t WHERE LOWER(col1) > "a" AND LOWER(col1) < "b";
SELECT * FROM t WHERE LOWER(col1) > "b" OR LOWER(col1) < "a";
```

クエリが同じ式でソートされている場合、式インデックスが適用されます。次のステートメントを例に挙げます。

```sql
SELECT * FROM t ORDER BY LOWER(col1);
```

同じ式が集約関数（ `GROUP BY` ）に含まれている場合、式のインデックスが適用されます。次のステートメントを例にとります。

```sql
SELECT MAX(LOWER(col1)) FROM t;
SELECT MIN(col1) FROM t GROUP BY LOWER(col1);
```

式インデックスに対応する式を確認するには、 [`SHOW INDEX`](/sql-statements/sql-statement-show-indexes.md)を実行するか、システム テーブル[`information_schema.tidb_indexes`](/information-schema/information-schema-tidb-indexes.md)およびテーブル[`information_schema.STATISTICS`](/information-schema/information-schema-statistics.md)を確認してください。出力の`Expression`列は、対応する式を示します。式インデックス以外の場合は、 `NULL`が表示されます。

式インデックスの維持コストは、他のインデックスの維持コストよりも高くなります。これは、行が挿入または更新されるたびに式の値を計算する必要があるためです。式の値は既にインデックスに格納されているため、オプティマイザが式インデックスを選択する際に、この値を再計算する必要はありません。

したがって、クエリのパフォーマンスが挿入および更新のパフォーマンスを上回る場合は、式にインデックスを作成することを検討できます。

式インデックスには、MySQL と同じ構文と制限があります。これらは、生成された非表示の仮想列にインデックスを作成することによって実装されるため、サポートされる式はすべての[仮想生成列の制限](/generated-columns.md#limitations)制限を継承します。

## 多値インデックス {#multi-valued-indexes}

マルチバリューインデックスは、配列列に定義されるセカンダリインデックスの一種です。通常のインデックスでは、1つのインデックスレコードが1つのデータレコードに対応します（1:1）。マルチバリューインデックスでは、複数のインデックスレコードが1つのデータレコードに対応します（N:1）。マルチバリューインデックスは、JSON配列のインデックス付けに使用されます。たとえば、 `zipcode`フィールドに定義されたマルチバリューインデックスは`zipcode`配列の各要素に対して1つのインデックスレコードを生成します。

```json
{
    "user":"Bob",
    "user_id":31,
    "zipcode":[94477,94536]
}
```

### 複数値インデックスを作成する {#create-multi-valued-indexes}

式インデックスを作成するのと同様に、インデックス定義で[`CAST(... AS ... ARRAY)`](/functions-and-operators/cast-functions-and-operators.md#cast)関数を使用することで、複数値のインデックスを作成できます。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips((CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

複数値インデックスを一意インデックスとして定義することができます。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    UNIQUE INDEX zips( (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
```

複数値インデックスを一意インデックスとして定義した場合、重複データを挿入しようとするとエラーが報告されます。

```sql
mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [1,2]}');
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO customers VALUES (1, 'pingcap', '{"zipcode": [2,3]}');
ERROR 1062 (23000): Duplicate entry '2' for key 'customers.zips'
```

同じレコード内に重複する値が存在することは許容されるが、異なるレコード内に重複する値が存在する場合はエラーが報告される。

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

多値インデックスが複合インデックスとして定義される場合、多値部分は任意の位置に現れることができますが、一度しか現れません。

```sql
mysql> CREATE TABLE customers (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name CHAR(10),
    custinfo JSON,
    INDEX zips(name, (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)), (CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
);
ERROR 1235 (42000): This version of TiDB doesn't yet support 'more than one multi-valued key part per index'.
```

書き込まれるデータは、多値インデックスで定義された型と完全に一致する必要があります。一致しない場合、データの書き込みは失敗します。

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

詳細については [インデックスの選択 - 複数値インデックスを使用する](/choose-index.md#use-multi-valued-indexes)参照してください。

### 制限事項 {#limitations}

-   空のJSON配列の場合、対応するインデックスレコードは生成されません。
-   `CAST(... AS ... ARRAY)`のターゲットタイプは`BINARY` 、 `JSON` 、 `YEAR` 、 `FLOAT` 、および`DECIMAL`いずれにもなりません。ソースタイプは JSON である必要があります。
-   複数値インデックスをソートに使用することはできません。
-   JSON配列に対してのみ、複数値のインデックスを作成できます。
-   複数値インデックスは、主キーまたは外部キーとして使用することはできません。
-   複数値インデックスが使用する追加のstorage領域は、1行あたりの配列要素の平均数×通常のセカンダリインデックスが使用する領域に等しくなります。
-   通常のインデックスと比較して、多値インデックスではDML操作によって変更されるインデックスレコードの数が多くなるため、多値インデックスは通常のインデックスよりもパフォーマンスに大きな影響を与えます。
-   多値インデックスは式インデックスの特殊なタイプであるため、式インデックスと同様の制限があります。
-   テーブルが複数値インデックスを使用している場合、 BR、TiCDC、またはTiDB Lightningを使用して、v6.6.0より前のTiDBクラスタにテーブルをバックアップ、レプリケート、またはインポートすることはできません。
-   複雑な条件を含むクエリの場合、TiDB は複数値のインデックスを選択できない場合があります。多値インデックスでサポートされる条件パターンについては、 [複数値インデックスを使用する](/choose-index.md#use-multi-valued-indexes)を参照してください。

## 非表示インデックス {#invisible-index}

デフォルトでは、非表示インデックスとはクエリ最適化ツールによって無視されるインデックスのことです。

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

TiDB v8.0.0以降では、システム変数[`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800)変更することで、オプティマイザに非表示のインデックスを選択させることができます。

詳細については、 [`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)参照してください。

## 関連するシステム変数 {#associated-system-variables}

`CREATE INDEX`ステートメントに関連付けられているシステム変数は、 `tidb_ddl_enable_fast_reorg` 、 `tidb_ddl_reorg_worker_cnt` 、 `tidb_ddl_reorg_batch_size` 、 `tidb_enable_auto_increment_in_generated` 、および`tidb_ddl_reorg_priority` 。 詳細[システム変数](/system-variables.md#tidb_ddl_reorg_worker_cnt)を参照してください。

## MySQLとの互換性 {#mysql-compatibility}

-   TiDB Self-Managed およびTiDB Cloud Dedicatedは`FULLTEXT`構文の解析をサポートしていますが、 `FULLTEXT` 、 `HASH` 、および`SPATIAL`インデックスの使用はサポートしていません。

    > **注記：**
    >
    > 現在、特定の AWS リージョンのTiDB Cloud StarterとTiDB Cloud Essentialインスタンスのみが[`FULLTEXT`構文と索引](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)をサポートしています。

-   TiDB は、MySQL との互換性のために、 `HASH` 、 `BTREE` 、 `RTREE`などのインデックス タイプを構文で受け入れますが、それらを無視します。

-   降順インデックスはサポートされていません（ MySQL 5.7と同様）。

-   `CLUSTERED`タイプの主キーをテーブルに追加することはサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、[クラスター化インデックス](/clustered-indexes.md)を参照してください。

-   式インデックスはビューと互換性がありません。ビューを使用してクエリを実行する場合、式インデックスを同時に使用することはできません。

-   式インデックスはバインディングとの互換性に問題があります。式インデックスの式に定数が含まれている場合、対応するクエリ用に作成されるバインディングのスコープが拡張されます。たとえば、式インデックスの式が`a+1`で、対応するクエリ条件が`a+1 > 2`であるとします。この場合、作成されるバインディングは`a+? > ?`となり、 `a+2 > 2`のような条件を持つクエリも式インデックスの使用を強制され、実行プランが最適化されません。さらに、これは SQL プラン管理 (SPM) におけるベースラインのキャプチャとベースラインの進化にも影響します。

-   複数値インデックスを使用して書き込まれるデータは、定義されたデータ型と正確に一致する必要があります。そうしないと、データの書き込みは失敗します。詳細については、 [複数値インデックスを作成する](/sql-statements/sql-statement-create-index.md#create-multi-valued-indexes)参照してください。

-   `UNIQUE KEY`インデックス オプションを使用して、 `GLOBAL`を[グローバルインデックス](/global-indexes.md)として設定することは[パーティション化されたテーブル](/partitioned-table.md)の TiDB 拡張機能であり、MySQL とは互換性がありません。

## 関連項目 {#see-also}

-   [インデックス選択](/choose-index.md)
-   [インデックス問題の解決方法](/wrong-index-solution.md)
-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [インデックスを削除](/sql-statements/sql-statement-drop-index.md)
-   [インデックス名の変更](/sql-statements/sql-statement-rename-index.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [テーブルを作成する](/sql-statements/sql-statement-create-table.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
