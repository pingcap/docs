---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: TiDB データベースの CREATE INDEX の使用法の概要。
---

# インデックスの作成 {#create-index}

この文は既存のテーブルに新しいインデックスを追加します。これは[`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-alter-table.md)の代替構文であり、MySQLとの互換性のために用意されています。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 4つのvCPUを搭載したクラスタ[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)の場合、インデックス作成時にリソース制限がクラスタの安定性に影響を与えないように、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)手動で無効にすることをお勧めします。この設定を無効にすると、トランザクションを使用してインデックスを作成できるようになり、クラスタ全体への影響が軽減されます。

</CustomContent>

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

クエリのフィルタリング条件が特定の式に基づいているシナリオもあります。このようなシナリオでは、通常のインデックスが機能せず、テーブル全体をスキャンしてクエリを実行する必要があるため、クエリのパフォーマンスは比較的低下します。式インデックスは、式に基づいて作成できる特殊なインデックスの一種です。式インデックスを作成すると、TiDBは式ベースのクエリにそのインデックスを使用できるため、クエリのパフォーマンスが大幅に向上します。

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
> 式インデックス内の式は`(`と`)`で囲む必要があります。囲まない場合は構文エラーが報告されます。

通常のインデックスを削除するのと同じ方法で、式インデックスを削除できます。

```sql
DROP INDEX idx1 ON t1;
```

式インデックスには様々な種類の式が含まれます。正確性を保証するため、式インデックスの作成には、完全にテストされた一部の関数のみを使用できます。つまり、本番環境では、これらの関数のみが式で使用できます。これらの関数は、変数[`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520)をクエリすることで取得できます。現在、使用できる関数は次のとおりです。

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

上記のリストに含まれていない関数は、十分にテストされていないため、本番環境での関数は推奨されません。これは実験的とみなされます。演算子、 `CAST`などの他の式も実験的`CASE WHEN`みなされ、本番環境での本番は推奨されません。

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
> -   ROW関数(例: `CREATE TABLE t (j JSON, INDEX k (((j,j))));` 。
> -   [集計関数](/functions-and-operators/aggregate-group-by-functions.md) 。
>
> 式インデックスは暗黙的に名前（例： `_V$_{index_name}_{index_offset}` ）を取得します。列に既に設定されている名前で新しい式インデックスを作成しようとすると、エラーが発生します。また、同じ名前の新しい列を追加した場合もエラーが発生します。
>
> 式インデックスの式内の関数パラメータの数が正しいことを確認してください。
>
> インデックスの式に文字列関連の関数が含まれており、戻り値の型と長さの影響を受ける場合、式インデックスの作成に失敗する可能性があります。このような状況では、 `CAST()`関数を使用して、戻り値の型と長さを明示的に指定できます。例えば、 `REPEAT(a, 3)`式に基づいて式インデックスを作成するには、この式を`CAST(REPEAT(a, 3) AS CHAR(20))`に変更する必要があります。

クエリ文内の式が式インデックス内の式と一致する場合、オプティマイザはクエリに対して式インデックスを選択できます。ただし、統計情報によっては、オプティマイザが式インデックスを選択しない場合があります。このような場合は、オプティマイザヒントを使用して、オプティマイザに式インデックスを選択させることができます。

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

クエリが同じ式でソートされている場合、式のインデックスが適用されます。次の文を例に挙げましょう。

```sql
SELECT * FROM t ORDER BY LOWER(col1);
```

同じ式が集約関数（ `GROUP BY` ）に含まれる場合、式のインデックスが適用されます。次の文を例に挙げます。

```sql
SELECT MAX(LOWER(col1)) FROM t;
SELECT MIN(col1) FROM t GROUP BY LOWER(col1);
```

式インデックスに対応する式を確認するには、 [`SHOW INDEX`](/sql-statements/sql-statement-show-indexes.md)を実行するか、システムテーブル[`information_schema.tidb_indexes`](/information-schema/information-schema-tidb-indexes.md)とテーブル[`information_schema.STATISTICS`](/information-schema/information-schema-statistics.md)を確認してください。出力の`Expression`列が対応する式を示します。式以外のインデックスの場合、この列には`NULL`表示されます。

式インデックスの維持コストは、行が挿入または更新されるたびに式の値を計算する必要があるため、他のインデックスの維持コストよりも高くなります。式の値は既にインデックスに格納されているため、オプティマイザが式インデックスを選択する際に再計算する必要はありません。

したがって、クエリのパフォーマンスが挿入および更新のパフォーマンスを上回る場合は、式のインデックス作成を検討できます。

式インデックスはMySQLと同じ構文と制限事項を持ちます。式インデックスは、生成された非表示の仮想列にインデックスを作成することで実装されるため、サポートされる式はすべて[仮想生成列の制限](/generated-columns.md#limitations)継承します。

## 多値インデックス {#multi-valued-indexes}

多値インデックスは、配列の列に定義されるセカンダリインデックスの一種です。通常のインデックスでは、1つのインデックスレコードが1つのデータレコードに対応します（1:1）。多値インデックスでは、複数のインデックスレコードが1つのデータレコードに対応します（N:1）。多値インデックスは、JSON配列のインデックス作成に使用されます。例えば、 `zipcode`番目のフィールドに多値インデックスを定義すると、配列`zipcode`の各要素に対して1つのインデックスレコードが生成されます。

```json
{
    "user":"Bob",
    "user_id":31,
    "zipcode":[94477,94536]
}
```

### 複数値インデックスを作成する {#create-multi-valued-indexes}

式インデックスを作成する場合と同様に、インデックス定義で[`CAST(... AS ... ARRAY)`](/functions-and-operators/cast-functions-and-operators.md#cast)関数を使用することで、複数値インデックスを作成できます。

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

同じレコードに重複した値が存在する可能性がありますが、異なるレコードに重複した値が存在する場合は、エラーが報告されます。

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

書き込まれたデータは、複数値インデックスで定義された型と完全に一致する必要があります。一致しない場合、データの書き込みは失敗します。

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

詳細は[インデックスの選択 - 複数値インデックスを使用する](/choose-index.md#use-multi-valued-indexes)参照。

### 制限事項 {#limitations}

-   空の JSON 配列の場合、対応するインデックス レコードは生成されません。
-   `CAST(... AS ... ARRAY)`のターゲットタイプは`BINARY` 、 `JSON` 、 `YEAR` 、 `FLOAT` 、 `DECIMAL`のいずれにもなりません。ソースタイプは JSON である必要があります。
-   並べ替えに複数値インデックスを使用することはできません。
-   JSON 配列には複数値インデックスのみを作成できます。
-   複数値インデックスは主キーまたは外部キーにすることはできません。
-   複数値インデックスによって使用される追加のstorageスペース = 行あたりの配列要素の平均数 * 通常のセカンダリ インデックスによって使用されるスペース。
-   通常のインデックスと比較すると、DML 操作では複数値インデックスのインデックス レコードがより多く変更されるため、複数値インデックスは通常のインデックスよりもパフォーマンスに大きな影響を与えます。
-   複数値インデックスは特殊なタイプの式インデックスであるため、複数値インデックスには式インデックスと同じ制限があります。
-   テーブルで複数値インデックスが使用されている場合、 BR、TiCDC、またはTiDB Lightning を使用して、v6.6.0 より前の TiDB クラスターにテーブルをバックアップ、複製、またはインポートすることはできません。
-   複雑な条件を持つクエリの場合、TiDBは複数値インデックスを選択できない可能性があります。複数値インデックスでサポートされる条件パターンについては、 [複数値インデックスを使用する](/choose-index.md#use-multi-valued-indexes)を参照してください。

## 目に見えないインデックス {#invisible-index}

デフォルトでは、非表示のインデックスはクエリ オプティマイザーによって無視されるインデックスです。

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

TiDB v8.0.0 以降では、システム変数[`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800)を変更することで、オプティマイザーが非表示のインデックスを選択するようにすることができます。

詳細は[`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)参照。

## 関連するシステム変数 {#associated-system-variables}

`CREATE INDEX`文に関連付けられたシステム変数は`tidb_ddl_enable_fast_reorg` 、 `tidb_ddl_reorg_worker_cnt` 、 `tidb_ddl_reorg_batch_size` 、 `tidb_enable_auto_increment_in_generated` 、 `tidb_ddl_reorg_priority`です。詳細は[システム変数](/system-variables.md#tidb_ddl_reorg_worker_cnt)を参照してください。

## MySQLの互換性 {#mysql-compatibility}

-   TiDB Self-Managed およびTiDB Cloud Dedicated は`FULLTEXT`構文の解析をサポートしますが、 `FULLTEXT` 、 `HASH` 、および`SPATIAL`インデックスの使用はサポートしません。

    > **注記：**
    >
    > 現在、特定の AWS リージョンの {{{ .starter }} および {{{ .essential }}} クラスターのみが[`FULLTEXT`構文とインデックス](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)サポートしています。

-   TiDB `RTREE` `BTREE` `HASH`インデックス タイプを受け入れますが、それらを無視します。

-   降順インデックスはサポートされていません ( MySQL 5.7と同様)。

-   `CLUSTERED`型の主キーをテーブルに追加することはサポートされていません。3 型の主キーの詳細については、 `CLUSTERED` [クラスター化インデックス](/clustered-indexes.md)参照してください。

-   式インデックスはビューと互換性がありません。ビューを使用してクエリを実行する場合、式インデックスを同時に使用することはできません。

-   式インデックスはバインディングとの互換性に問題があります。式インデックスの式に定数が含まれる場合、対応するクエリに対して作成されるバインディングのスコープが拡張されます。例えば、式インデックス内の式が`a+1`で、対応するクエリ条件が`a+1 > 2`あるとします。この場合、作成されるバインディングは`a+? > ?`です。つまり、 `a+2 > 2`などの条件を持つクエリでも式インデックスの使用が強制され、実行プランの品質が低下します。さらに、これはSQLプラン管理（SPM）におけるベースラインのキャプチャとベースラインの進化にも影響を及ぼします。

-   多値インデックスで書き込まれるデータは、定義されたデータ型と完全に一致する必要があります。一致しない場合、データの書き込みは失敗します。詳細については、 [複数値インデックスを作成する](/sql-statements/sql-statement-create-index.md#create-multi-valued-indexes)参照してください。

-   `GLOBAL`インデックス オプションを使用して`UNIQUE KEY`を[グローバルインデックス](/partitioned-table.md#global-indexes)として設定することは、 [パーティションテーブル](/partitioned-table.md)の TiDB 拡張であり、MySQL とは互換性がありません。

## 参照 {#see-also}

-   [インデックスの選択](/choose-index.md)
-   [インデックス問題の解決方法](/wrong-index-solution.md)
-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [インデックスを削除](/sql-statements/sql-statement-drop-index.md)
-   [インデックス名の変更](/sql-statements/sql-statement-rename-index.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
