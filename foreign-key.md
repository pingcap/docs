---
title: FOREIGN KEY Constraints
summary: TiDB データベースの FOREIGN KEY 制約の使用法の概要。
---

# 外部キー制約 {#foreign-key-constraints}

v6.6.0 以降、TiDB は、関連データのテーブル間参照を可能にする外部キー機能と、データの一貫性を維持するための外部キー制約をサポートします。

> **警告：**
>
> -   現在、外部キー機能は実験的です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。
> -   外部キー機能は通常、 [参照整合性](https://en.wikipedia.org/wiki/Referential_integrity)制約チェックを強制するために使用されます。パフォーマンスの低下を引き起こす可能性があるため、パフォーマンスが重要なシナリオで使用する前に徹底的なテストを実施することをお勧めします。

外部キーは子テーブルで定義されます。構文は次のとおりです。

```ebnf+diagram
ForeignKeyDef
         ::= ( 'CONSTRAINT' Identifier )? 'FOREIGN' 'KEY'
             Identifier? '(' ColumnName ( ',' ColumnName )* ')'
             'REFERENCES' TableName '(' ColumnName ( ',' ColumnName )* ')'
             ( 'ON' 'DELETE' ReferenceOption )?
             ( 'ON' 'UPDATE' ReferenceOption )?

ReferenceOption
         ::= 'RESTRICT'
           | 'CASCADE'
           | 'SET' 'NULL'
           | 'SET' 'DEFAULT'
           | 'NO' 'ACTION'
```

## ネーミング {#naming}

外部キーの命名は、次の規則に従います。

-   `CONSTRAINT identifier`に名前が指定されている場合は、指定された名前が使用されます。
-   `CONSTRAINT identifier`に名前が指定されておらず、 `FOREIGN KEY identifier`に名前が指定されている場合は、 `FOREIGN KEY identifier`に指定された名前が使用されます。
-   `CONSTRAINT identifier`と`FOREIGN KEY identifier`どちらにも名前が指定されていない場合は、 `fk_1` 、 `fk_2` 、 `fk_3`などの名前が自動的に生成されます。
-   外部キー名は現在のテーブル内で一意である必要があります。そうでない場合、外部キーの作成時にエラー`ERROR 1826: Duplicate foreign key constraint name 'fk'`が報告されます。

## 制限 {#restrictions}

外部キーを作成するときは、次の条件を満たす必要があります。

-   親テーブルも子テーブルも一時テーブルではありません。

-   ユーザーには親テーブルに対する権限`REFERENCES`あります。

-   親テーブルと子テーブルの外部キーによって参照される列は、同じデータ型であり、サイズ、精度、長さ、文字セット、および照合順序が同じです。

-   外部キーの列は、それ自体を参照することはできません。

-   外部キーの列と参照先の親テーブルの列には同じインデックスがあり、インデックスの列の順序は外部キーの列の順序と一致します。これは、外部キー制約チェックを実行するときに、インデックスを使用してテーブル全体のスキャンを回避するためです。

    -   親テーブルに対応する外部キー インデックスがない場合、エラー`ERROR 1822: Failed to add the foreign key constraint. Missing index for constraint 'fk' in the referenced table 't'`が報告されます。
    -   子テーブルに対応する外部キー インデックスがない場合、外部キーと同じ名前のインデックスが自動的に作成されます。

-   `BLOB`または`TEXT`タイプの列に外部キーを作成することはサポートされていません。

-   パーティションテーブルに外部キーを作成することはサポートされていません。

-   仮想生成列に外部キーを作成することはサポートされていません。

## 参照操作 {#reference-operations}

`UPDATE`または`DELETE`操作が親テーブルの外部キー値に影響する場合、子テーブルの対応する外部キー値は、外部キー定義の`ON UPDATE`または`ON DELETE`句で定義された参照操作によって決定されます。参照操作には次のものが含まれます。

-   `CASCADE` : `UPDATE`または`DELETE`操作が親テーブルに影響する場合、子テーブル内の一致する行を自動的に更新または削除します。カスケード操作は深さ優先方式で実行されます。
-   `SET NULL` : `UPDATE`または`DELETE`操作が親テーブルに影響する場合、子テーブルの一致する外部キー列を`NULL`に自動的に設定します。
-   `RESTRICT` : 子テーブルに一致する行が含まれている場合、 `UPDATE`または`DELETE`操作を拒否します。
-   `NO ACTION` : `RESTRICT`と同じ。
-   `SET DEFAULT` : `RESTRICT`と同じ。

親テーブルに一致する外部キー値がない場合、子テーブルでの`INSERT`または`UPDATE`操作は拒否されます。

外部キー定義で`ON DELETE`または`ON UPDATE`指定されていない場合、デフォルトの動作は`NO ACTION`なります。

外部キーが`STORED GENERATED COLUMN`に定義されている場合、 `CASCADE` 、 `SET NULL` 、および`SET DEFAULT`参照はサポートされません。

## 外部キーの使用例 {#usage-examples-of-foreign-keys}

次の例では、単一列の外部キーを使用して親テーブルと子テーブルを関連付けます。

```sql
CREATE TABLE parent (
    id INT KEY
);

CREATE TABLE child (
    id INT,
    pid INT,
    INDEX idx_pid (pid),
    FOREIGN KEY (pid) REFERENCES parent(id) ON DELETE CASCADE
);
```

以下は、 `product_order`テーブルに他の 2 つのテーブルを参照する 2 つの外部キーがある、より複雑な例です。1 つの外部キーは`product`テーブル上の 2 つのインデックスを参照し、もう 1 つは`customer`テーブル上の 1 つのインデックスを参照します。

```sql
CREATE TABLE product (
    category INT NOT NULL,
    id INT NOT NULL,
    price DECIMAL(20,10),
    PRIMARY KEY(category, id)
);

CREATE TABLE customer (
    id INT KEY
);

CREATE TABLE product_order (
    id INT NOT NULL AUTO_INCREMENT,
    product_category INT NOT NULL,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,

    PRIMARY KEY(id),
    INDEX (product_category, product_id),
    INDEX (customer_id),

    FOREIGN KEY (product_category, product_id)
      REFERENCES product(category, id)
      ON UPDATE CASCADE ON DELETE RESTRICT,

    FOREIGN KEY (customer_id)
      REFERENCES customer(id)
);
```

## 外部キー制約を作成する {#create-a-foreign-key-constraint}

外部キー制約を作成するには、次の`ALTER TABLE`ステートメントを使用できます。

```sql
ALTER TABLE table_name
    ADD [CONSTRAINT [identifier]] FOREIGN KEY
    [identifier] (col_name, ...)
    REFERENCES tbl_name (col_name,...)
    [ON DELETE reference_option]
    [ON UPDATE reference_option]
```

外部キーは自己参照、つまり同じテーブルを参照することができます。 `ALTER TABLE`を使用してテーブルに外部キー制約を追加する場合は、まず外部キーが参照する親テーブルの列にインデックスを作成する必要があります。

## 外部キー制約を削除する {#delete-a-foreign-key-constraint}

外部キー制約を削除するには、次の`ALTER TABLE`ステートメントを使用できます。

```sql
ALTER TABLE table_name DROP FOREIGN KEY fk_identifier;
```

外部キー制約が作成時に名前が付けられている場合は、その名前を参照して外部キー制約を削除できます。それ以外の場合は、制約を削除するには自動的に生成された制約名を使用する必要があります。外部キー名を表示するには、 `SHOW CREATE TABLE`使用します。

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

## 外部キー制約チェック {#foreign-key-constraint-check}

TiDB は、システム変数[`foreign_key_checks`](/system-variables.md#foreign_key_checks)によって制御される外部キー制約チェックをサポートしています。デフォルトでは、この変数は`ON`に設定されており、外部キー制約チェックが有効になっていることを意味します。この変数には、 `GLOBAL`と`SESSION` 2 つのスコープがあります。この変数を有効にしておくと、外部キー参照関係の整合性を確保できます。

外部キー制約チェックを無効にすると、次の効果が得られます。

-   外部キーによって参照される親テーブルを削除する場合、外部キー制約チェックが無効になっている場合にのみ削除が成功します。
-   データベースにデータをインポートする場合、テーブルの作成順序が外部キーの依存関係の順序と異なることがあり、テーブルの作成が失敗する可能性があります。外部キー制約チェックが無効になっている場合にのみ、テーブルを正常に作成できます。また、外部キー制約チェックを無効にすると、データのインポートが高速化されます。
-   データベースにデータをインポートするときに、子テーブルのデータを最初にインポートすると、エラーが報告されます。外部キー制約チェックが無効になっている場合にのみ、子テーブルのデータを正常にインポートできます。
-   実行される`ALTER TABLE`つの操作に外部キーの変更が含まれる場合、この操作は外部キー制約チェックが無効になっている場合にのみ成功します。

外部キー制約チェックが無効になっている場合、次のシナリオを除き、外部キー制約チェックと参照操作は実行されません。

-   `ALTER TABLE`の実行によって外部キーの定義が間違ってしまう可能性がある場合は、実行中にエラーが報告されます。
-   外部キーに必要なインデックスを削除する場合は、まず外部キーを削除する必要があります。そうしないと、エラーが報告されます。
-   外部キーを作成したが、関連する条件または制限を満たしていない場合は、エラーが報告されます。

## ロック {#locking}

`INSERT`または`UPDATE`が子テーブルの場合、外部キー制約は、対応する外部キー値が親テーブルに存在するかどうかを確認し、外部キー制約に違反する他の操作によって外部キー値が削除されるのを防ぐために、親テーブルの行をロックします。ロック動作は、親テーブルで外部キー値が配置されている行に対して`SELECT FOR UPDATE`操作を実行することと同じです。

TiDB は現在`LOCK IN SHARE MODE`サポートしていないため、子テーブルが大量の同時書き込みを受け入れ、参照される外部キー値のほとんどが同じである場合、深刻なロック競合が発生する可能性があります。大量の子テーブルデータを書き込む場合は[`foreign_key_checks`](/system-variables.md#foreign_key_checks)無効にすることをお勧めします。

## 外部キーの定義とメタデータ {#definition-and-metadata-of-foreign-keys}

外部キー制約の定義を表示するには、次[`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)ステートメントを実行します。

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

次のいずれかのシステム テーブルを使用して、外部キーに関する情報を取得することもできます。

-   [`INFORMATION_SCHEMA.KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)
-   [`INFORMATION_SCHEMA.TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)
-   [`INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`](/information-schema/information-schema-referential-constraints.md)

以下に例を示します。

`INFORMATION_SCHEMA.KEY_COLUMN_USAGE`システム テーブルから外部キーに関する情報を取得します。

```sql
mysql> SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA IS NOT NULL;
+--------------+---------------+------------------+-----------------+
| TABLE_SCHEMA | TABLE_NAME    | COLUMN_NAME      | CONSTRAINT_NAME |
+--------------+---------------+------------------+-----------------+
| test         | child         | pid              | fk_1            |
| test         | product_order | product_category | fk_1            |
| test         | product_order | product_id       | fk_1            |
| test         | product_order | customer_id      | fk_2            |
+--------------+---------------+------------------+-----------------+
```

`INFORMATION_SCHEMA.TABLE_CONSTRAINTS`システム テーブルから外部キーに関する情報を取得します。

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE='FOREIGN KEY'\G
***************************[ 1. row ]***************************
CONSTRAINT_CATALOG | def
CONSTRAINT_SCHEMA  | test
CONSTRAINT_NAME    | fk_1
TABLE_SCHEMA       | test
TABLE_NAME         | child
CONSTRAINT_TYPE    | FOREIGN KEY
```

`INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`システム テーブルから外部キーに関する情報を取得します。

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS\G
***************************[ 1. row ]***************************
CONSTRAINT_CATALOG        | def
CONSTRAINT_SCHEMA         | test
CONSTRAINT_NAME           | fk_1
UNIQUE_CONSTRAINT_CATALOG | def
UNIQUE_CONSTRAINT_SCHEMA  | test
UNIQUE_CONSTRAINT_NAME    | PRIMARY
MATCH_OPTION              | NONE
UPDATE_RULE               | NO ACTION
DELETE_RULE               | CASCADE
TABLE_NAME                | child
REFERENCED_TABLE_NAME     | parent
```

## 外部キーを使用した実行プランのビュー {#view-execution-plans-with-foreign-keys}

`EXPLAIN`ステートメントを使用して実行プランを表示できます。3 `Foreign_Key_Check`は、実行される DML ステートメントに対して外部キー制約チェックを実行します。

```sql
mysql> explain insert into child values (1,1);
+-----------------------+---------+------+---------------+-------------------------------+
| id                    | estRows | task | access object | operator info                 |
+-----------------------+---------+------+---------------+-------------------------------+
| Insert_1              | N/A     | root |               | N/A                           |
| └─Foreign_Key_Check_3 | 0.00    | root | table:parent  | foreign_key:fk_1, check_exist |
+-----------------------+---------+------+---------------+-------------------------------+
```

`EXPLAIN ANALYZE`ステートメントを使用して、外部キー参照動作の実行を表示できます。3 `Foreign_Key_Cascade`は、実行される DML ステートメントの外部キー参照を実行します。

```sql
mysql> explain analyze delete from parent where id = 1;
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
| id                               | estRows | actRows | task      | access object                   | execution info                                                                                                                                                                               | operator info                               | memory    | disk |
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
| Delete_2                         | N/A     | 0       | root      |                                 | time:117.3µs, loops:1                                                                                                                                                                        | N/A                                         | 380 Bytes | N/A  |
| ├─Point_Get_1                    | 1.00    | 1       | root      | table:parent                    | time:63.6µs, loops:2, Get:{num_rpc:1, total_time:29.9µs}                                                                                                                                     | handle:1                                    | N/A       | N/A  |
| └─Foreign_Key_Cascade_3          | 0.00    | 0       | root      | table:child, index:idx_pid      | total:1.28ms, foreign_keys:1                                                                                                                                                                 | foreign_key:fk_1, on_delete:CASCADE         | N/A       | N/A  |
|   └─Delete_7                     | N/A     | 0       | root      |                                 | time:904.8µs, loops:1                                                                                                                                                                        | N/A                                         | 1.11 KB   | N/A  |
|     └─IndexLookUp_11             | 10.00   | 1       | root      |                                 | time:869.5µs, loops:2, index_task: {total_time: 371.1µs, fetch_handle: 357.3µs, build: 1.25µs, wait: 12.5µs}, table_task: {total_time: 382.6µs, num: 1, concurrency: 5}                      |                                             | 9.13 KB   | N/A  |
|       ├─IndexRangeScan_9(Build)  | 10.00   | 1       | cop[tikv] | table:child, index:idx_pid(pid) | time:351.2µs, loops:3, cop_task: {num: 1, max: 282.3µs, proc_keys: 0, rpc_num: 1, rpc_time: 263µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}, tikv_task:{time:220.2µs, loops:0}   | range:[1,1], keep order:false, stats:pseudo | N/A       | N/A  |
|       └─TableRowIDScan_10(Probe) | 10.00   | 1       | cop[tikv] | table:child                     | time:223.9µs, loops:2, cop_task: {num: 1, max: 168.8µs, proc_keys: 0, rpc_num: 1, rpc_time: 154.5µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}, tikv_task:{time:145.6µs, loops:0} | keep order:false, stats:pseudo              | N/A       | N/A  |
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
```

## 互換性 {#compatibility}

### TiDB バージョン間の互換性 {#compatibility-between-tidb-versions}

v6.6.0 より前の TiDB では、外部キーを作成する構文がサポートされていますが、作成された外部キーは無効です。v6.6.0 より前に作成された TiDB クラスターを v6.6.0 以降にアップグレードすると、アップグレード前に作成された外部キーは無効のままになります。v6.6.0 以降のバージョンで作成`SHOW CREATE TABLE`れた外部キーのみが有効になります。無効な外部キーを削除して新しい外部キーを作成し、外部キー制約を有効にすることができます。1 ステートメントを使用して、外部キーが有効かどうかを確認できます。無効な外部キーには`/* FOREIGN KEY INVALID */`コメントがあります。

```sql
mysql> SHOW CREATE TABLE child\G
***************************[ 1. row ]***************************
Table        | child
Create Table | CREATE TABLE `child` (
  `id` int(11) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE /* FOREIGN KEY INVALID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

### TiDBツールとの互換性 {#compatibility-with-tidb-tools}

<CustomContent platform="tidb">

-   [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)外部キーをサポートしません。
-   [DM](/dm/dm-overview.md)外部キーをサポートしていません。DM は、データを TiDB に複製するときに、下流の TiDB の[`foreign_key_checks`](/system-variables.md#foreign_key_checks)無効にします。そのため、外部キーによって発生するカスケード操作は上流から下流に複製されず、データの不整合が発生する可能性があります。
-   [ティCDC](/ticdc/ticdc-overview.md) v6.6.0 は外部キーと互換性があります。以前のバージョンの TiCDC では、外部キーを持つテーブルを複製するときにエラーが報告される可能性があります。v6.6.0 より前のバージョンの TiCDC を使用する場合は、ダウンストリーム TiDB クラスターの`foreign_key_checks`無効にすることをお勧めします。
-   [BR](/br/backup-and-restore-overview.md) v6.6.0 は外部キーと互換性があります。以前のバージョンのBRでは、外部キーを持つテーブルを v6.6.0 以降のクラスターに復元するときにエラーが報告される可能性があります。v6.6.0 より前のBRを使用する場合は、クラスターを復元する前に、ダウンストリーム TiDB クラスターの`foreign_key_checks`を無効にすることをお勧めします。
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用する場合、ターゲット テーブルが外部キーを使用している場合は、データをインポートする前に、ダウンストリーム TiDB クラスターの`foreign_key_checks`無効にすることをお勧めします。v6.6.0 より前のバージョンでは、このシステム変数を無効にしても効果がなく、ダウンストリーム データベース ユーザーに`REFERENCES`権限を付与するか、ダウンストリーム データベースにターゲット テーブルを事前に手動で作成して、スムーズなデータ インポートを確保する必要があります。

</CustomContent>

-   [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)は外部キーと互換性があります。

<CustomContent platform="tidb">

-   [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用して上流データベースと下流データベース間でデータを比較する場合、データベースのバージョンが異なり、 [下流の TiDB に無効な外部キーがある](#compatibility-between-tidb-versions)があると、sync-diff-inspector によってテーブル スキーマの不整合エラーが報告されることがあります。これは、TiDB v6.6.0 で無効な外部キーに対して`/* FOREIGN KEY INVALID */`コメントが追加されたためです。

</CustomContent>

### MySQLとの互換性 {#compatibility-with-mysql}

名前を指定せずに外部キーを作成すると、TiDB によって生成される名前は MySQL によって生成される名前とは異なります。たとえば、TiDB によって生成される外部キー名は`fk_1` 、 `fk_2` 、 `fk_3`ですが、MySQL によって生成される外部キー名は`table_name_ibfk_1` 、 `table_name_ibfk_2` 、 `table_name_ibfk_3`です。

MySQL と TiDB はどちらも「インライン`REFERENCES`仕様」を解析しますが無視します。5 `FOREIGN KEY`の定義の一部である`REFERENCES`仕様のみがチェックされ、適用されます。次の例では、 `REFERENCES`句を使用して外部キー制約を作成します。

```sql
CREATE TABLE parent (
    id INT KEY
);

CREATE TABLE child (
    id INT,
    pid INT REFERENCES parent(id)
);

SHOW CREATE TABLE child;
```

出力は、 `child`テーブルに外部キーが含まれていないことを示しています。

```sql
+-------+-------------------------------------------------------------+
| Table | Create Table                                                |
+-------+-------------------------------------------------------------+
| child | CREATE TABLE `child` (                                      |
|       |   `id` int(11) DEFAULT NULL,                                |
|       |   `pid` int(11) DEFAULT NULL                                |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+-------------------------------------------------------------+
```
