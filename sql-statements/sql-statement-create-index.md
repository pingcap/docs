---
title: CREATE INDEX | TiDB SQL Statement Reference
summary: TiDB データベースの CREATE INDEX の使用法の概要。
---

# インデックスの作成 {#create-index}

このステートメントは、既存のテーブルに新しいインデックスを追加します。これは`ALTER TABLE .. ADD INDEX`の代替構文であり、MySQL との互換性のために含まれています。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 4 つの vCPU を備えた[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)のクラスターの場合、インデックス作成中にリソース制限がクラスターの安定性に影響するのを防ぐために、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)手動で無効にすることをお勧めします。この設定を無効にすると、トランザクションを使用してインデックスを作成できるようになり、クラスターへの全体的な影響が軽減されます。

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

## 表現インデックス {#expression-index}

一部のシナリオでは、クエリのフィルタリング条件は特定の式に基づいています。これらのシナリオでは、通常のインデックスが機能せず、テーブル全体をスキャンすることによってのみクエリを実行できるため、クエリのパフォーマンスは比較的低くなります。式インデックスは、式に作成できる特殊なインデックスの一種です。式インデックスが作成されると、TiDB は式ベースのクエリにインデックスを使用できるため、クエリのパフォーマンスが大幅に向上します。

たとえば、 `lower(col1)`に基づいてインデックスを作成する場合は、次の SQL ステートメントを実行します。

```sql
CREATE INDEX idx1 ON t1 ((lower(col1)));
```

または、次の同等のステートメントを実行することもできます。

```sql
ALTER TABLE t1 ADD INDEX idx1((lower(col1)));
```

テーブルを作成するときに、式インデックスを指定することもできます。

```sql
CREATE TABLE t1(col1 char(10), col2 char(10), index((lower(col1))));
```

> **注記：**
>
> 式インデックス内の式は`(`と`)`で囲む必要があります。そうでない場合は、構文エラーが報告されます。

通常のインデックスを削除するのと同じ方法で、式インデックスを削除できます。

```sql
DROP INDEX idx1 ON t1;
```

式インデックスには、さまざまな種類の式が含まれます。正確性を保証するために、式インデックスの作成には、完全にテストされた一部の関数のみが許可されます。つまり、実本番環境では、これらの関数のみが式で許可されます。これらの関数は、 `tidb_allow_function_for_expression_index`変数をクエリすることで取得できます。現在、許可されている関数は次のとおりです。

    json_array, json_array_append, json_array_insert, json_contains, json_contains_path, json_depth, json_extract, json_insert, json_keys, json_length, json_merge_patch, json_merge_preserve, json_object, json_pretty, json_quote, json_remove, json_replace, json_search, json_set, json_storage_size, json_type, json_unquote, json_valid, lower, md5, reverse, tidb_shard, upper, vitess_hash

上記のリストに含まれていない関数は、完全にテストされておらず、本番環境では推奨されません。 `case when`関数の`cast`の式も実験的と見なしており、実稼働本番では推奨されません。

<CustomContent platform="tidb">

それでもこれらの式を使用したい場合は、 [TiDB 構成ファイル](/tidb-configuration-file.md#allow-expression-index-new-in-v400)で次の設定を行うことができます。

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
> -   `rand()`や`now()`などの揮発性関数。
> -   システム変数とユーザー変数。
> -   サブクエリ。
> -   `AUTO_INCREMENT`列。この制限は、 `tidb_enable_auto_increment_in_generated` (システム変数) の値を`true`に設定することで解除できます。
> -   ウィンドウ関数。
> -   ROW関数(例: `create table t (j json, key k (((j,j))));` 。
> -   集計関数。
>
> 式インデックスは暗黙的に名前を取得します (例: `_V$_{index_name}_{index_offset}` )。列にすでにある名前で新しい式インデックスを作成しようとすると、エラーが発生します。また、同じ名前で新しい列を追加した場合も、エラーが発生します。
>
> 式インデックスの式内の関数パラメータの数が正しいことを確認してください。
>
> インデックスの式に、返される型と長さの影響を受ける文字列関連の関数が含まれている場合、式インデックスの作成に失敗する可能性があります。このような状況では、 `cast()`関数を使用して、返される型と長さを明示的に指定できます。たとえば、 `repeat(a, 3)`式に基づいて式インデックスを作成するには、この式を`cast(repeat(a, 3) as char(20))`に変更する必要があります。

クエリ ステートメント内の式が式インデックス内の式と一致する場合、オプティマイザーはクエリの式インデックスを選択できます。統計によっては、オプティマイザーが式インデックスを選択しない場合もあります。このような場合は、オプティマイザー ヒントを使用して、オプティマイザーに式インデックスを選択させることができます。

次の例では、式`lower(col1)`に式インデックス`idx`作成するとします。

クエリ ステートメントの結果が同じ式である場合、式インデックスが適用されます。次のステートメントを例に挙げます。

```sql
SELECT lower(col1) FROM t;
```

フィルタリング条件に同じ式が含まれている場合は、式のインデックスが適用されます。次のステートメントを例に挙げます。

```sql
SELECT * FROM t WHERE lower(col1) = "a";
SELECT * FROM t WHERE lower(col1) > "a";
SELECT * FROM t WHERE lower(col1) BETWEEN "a" AND "b";
SELECT * FROM t WHERE lower(col1) in ("a", "b");
SELECT * FROM t WHERE lower(col1) > "a" AND lower(col1) < "b";
SELECT * FROM t WHERE lower(col1) > "b" OR lower(col1) < "a";
```

クエリが同じ式でソートされている場合は、式インデックスが適用されます。次のステートメントを例に挙げます。

```sql
SELECT * FROM t ORDER BY lower(col1);
```

同じ式が集約関数（ `GROUP BY` ）に含まれている場合は、式のインデックスが適用されます。次の文を例に挙げます。

```sql
SELECT max(lower(col1)) FROM t;
SELECT min(col1) FROM t GROUP BY lower(col1);
```

式インデックスに対応する式を確認するには、 `show index`を実行するか、システム テーブル`information_schema.tidb_indexes`とテーブル`information_schema.STATISTICS`を確認します。出力の`Expression`列は対応する式を示します。式以外のインデックスの場合、列には`NULL`表示されます。

式インデックスの維持コストは、行が挿入または更新されるたびに式の値を計算する必要があるため、他のインデックスの維持コストよりも高くなります。式の値は既にインデックスに格納されているため、オプティマイザーが式インデックスを選択するときにこの値を再計算する必要はありません。

したがって、クエリのパフォーマンスが挿入および更新のパフォーマンスを上回る場合は、式のインデックス作成を検討できます。

式インデックスには、MySQL と同じ構文と制限があります。これらは、生成された非表示の仮想列にインデックスを作成することによって実装されるため、サポートされている式はすべて[仮想生成列の制限](/generated-columns.md#limitations)継承します。

## 多値インデックス {#multi-valued-indexes}

多値インデックスは、配列列に定義されるセカンダリ インデックスの一種です。通常のインデックスでは、1 つのインデックス レコードが 1 つのデータ レコードに対応します (1:1)。多値インデックスでは、複数のインデックス レコードが 1 つのデータ レコードに対応します (N:1)。多値インデックスは、JSON 配列のインデックスに使用されます。たとえば、 `zipcode`フィールドに定義された多値インデックスは、 `zipcode`配列の各要素に対して 1 つのインデックス レコードを生成します。

```json
{
    "user":"Bob",
    "user_id":31,
    "zipcode":[94477,94536]
}
```

### 複数値インデックスを作成する {#create-multi-valued-indexes}

式インデックスを作成する場合と同様に、インデックス定義で`CAST(... AS ... ARRAY)`式を使用して、複数値インデックスを作成できます。

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

複数値インデックスが一意のインデックスとして定義されている場合、重複データを挿入しようとするとエラーが報告されます。

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

書き込まれるデータは、複数値インデックスで定義された型と正確に一致する必要があります。一致しない場合、データの書き込みは失敗します。

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

詳細は[インデックスの選択 - 複数値インデックスを使用する](/choose-index.md#use-multi-valued-indexes)参照してください。

### 制限事項 {#limitations}

-   空の JSON 配列の場合、対応するインデックス レコードは生成されません。
-   `CAST(... AS ... ARRAY)`のターゲット タイプは、 `BINARY` 、 `JSON` 、 `YEAR` 、 `FLOAT` 、 `DECIMAL`のいずれにもなりません。ソース タイプは JSON である必要があります。
-   並べ替えに複数値インデックスを使用することはできません。
-   複数値インデックスは JSON 配列にのみ作成できます。
-   複数値インデックスは主キーまたは外部キーにすることはできません。
-   複数値インデックスによって使用される追加のstorageスペース = 行あたりの配列要素の平均数 * 通常のセカンダリ インデックスによって使用されるスペース。
-   通常のインデックスと比較すると、DML 操作では複数値インデックスのインデックス レコードがより多く変更されるため、複数値インデックスは通常のインデックスよりもパフォーマンスに大きな影響を与えます。
-   多値インデックスは特殊なタイプの式インデックスであるため、多値インデックスには式インデックスと同じ制限があります。
-   テーブルで複数値インデックスが使用されている場合、 BR、TiCDC、またはTiDB Lightning を使用して、v6.6.0 より前の TiDB クラスターにテーブルをバックアップ、複製、またはインポートすることはできません。
-   複数値インデックスの収集された統計が不足しているため、現在、複数値インデックスの選択率は固定された仮定に基づいています。クエリが複数の複数値インデックスにヒットすると、TiDB は最適なインデックスを選択できない可能性があります。このような場合は、 [`use_index_merge`](/optimizer-hints.md#use_index_merget1_name-idx1_name--idx2_name-)オプティマイザ ヒントを使用して固定実行プランを適用することをお勧めします。
-   複雑な条件を持つクエリの場合、TiDB は複数値インデックスを選択できない可能性があります。複数値インデックスでサポートされる条件パターンの詳細については、 [複数値インデックスを使用する](/choose-index.md#use-multi-valued-indexes)を参照してください。

## 目に見えないインデックス {#invisible-index}

非表示のインデックスは、クエリ オプティマイザーによって無視されるインデックスです。

```sql
CREATE TABLE t1 (c1 INT, c2 INT, UNIQUE(c2));
CREATE UNIQUE INDEX c1 ON t1 (c1) INVISIBLE;
```

詳細は[`ALTER INDEX`](/sql-statements/sql-statement-alter-index.md)参照。

## 関連するシステム変数 {#associated-system-variables}

`CREATE INDEX`ステートメントに関連付けられているシステム変数は`tidb_ddl_enable_fast_reorg` 、 `tidb_ddl_reorg_worker_cnt` 、 `tidb_ddl_reorg_batch_size` 、 `tidb_enable_auto_increment_in_generated` 、および`tidb_ddl_reorg_priority`です。詳細については[システム変数](/system-variables.md#tidb_ddl_reorg_worker_cnt)を参照してください。

## MySQL 互換性 {#mysql-compatibility}

-   TiDB は`FULLTEXT`および`SPATIAL`構文の解析をサポートしていますが、 `FULLTEXT` 、 `HASH` 、および`SPATIAL`インデックスの使用はサポートしていません。
-   降順インデックスはサポートされていません ( MySQL 5.7と同様)。
-   `CLUSTERED`タイプの主キーをテーブルに追加することはサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   式インデックスはビューと互換性がありません。ビューを使用してクエリを実行する場合、式インデックスを同時に使用することはできません。
-   式インデックスには、バインディングとの互換性の問題があります。式インデックスの式に定数がある場合、対応するクエリに対して作成されたバインディングのスコープが拡張されます。たとえば、式インデックスの式が`a+1`で、対応するクエリ条件が`a+1 > 2`あるとします。この場合、作成されたバインディングは`a+? > ?`です。つまり、 `a+2 > 2`などの条件を持つクエリでも式インデックスの使用が強制され、実行プランが不十分になります。さらに、これは SQL プラン管理 (SPM) のベースライン キャプチャとベースラインの進化にも影響します。
-   複数値インデックスで書き込まれるデータは、定義されたデータ型と完全に一致する必要があります。一致しない場合、データの書き込みは失敗します。詳細については、 [複数値インデックスを作成する](/sql-statements/sql-statement-create-index.md#create-multi-valued-indexes)参照してください。

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
