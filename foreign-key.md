---
title: FOREIGN KEY Constraints
summary: TiDBデータベースにおける外部キー制約の使用方法の概要。
---

# 外部キー制約 {#foreign-key-constraints}

外部キーは関連データのテーブル間参照を可能にし、外部キー制約は関連データの一貫性を保証します。TiDBはバージョン6.6.0以降、外部キーと外部キー制約をサポートしています。この機能はバージョン8.5.0から一般利用可能になります。

> **警告：**
>
> 外部キー機能は通常、 [参照整合性](https://en.wikipedia.org/wiki/Referential_integrity)チェックを強制するために使用されます。パフォーマンスの低下を引き起こす可能性があるため、パフォーマンスが重要なシナリオで使用する前に、徹底的なテストを実施することをお勧めします。

外部キーは子テーブルで定義されます。構文は以下のとおりです。

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

外部キーの命名は、以下の規則に従います。

-   `CONSTRAINT identifier`で名前が指定されている場合は、指定された名前が使用されます。
-   `CONSTRAINT identifier`に名前が指定されていない場合でも、 `FOREIGN KEY identifier`に名前が指定されている場合は、 `FOREIGN KEY identifier`に指定された名前が使用されます。
-   `CONSTRAINT identifier`も`FOREIGN KEY identifier`も名前を指定しない場合、 `fk_1` 、 `fk_2` 、 `fk_3`などの名前が自動的に生成されます。
-   外部キー名は、現在のテーブル内で一意である必要があります。そうでない場合、外部キーの作成時にエラー`ERROR 1826: Duplicate foreign key constraint name 'fk'`が報告されます。

## 制限 {#restrictions}

外部キーを作成する際には、以下の条件を満たす必要があります。

-   親テーブルも子テーブルも、一時テーブルではありません。

-   ユーザーは親テーブルに対して`REFERENCES`権限を持っています。

-   親テーブルと子テーブルの外部キーによって参照される列は、同じデータ型であり、同じサイズ、精度、長さ、文字セット、および照合順序を持っています。

-   外部キーの列は、自身を参照することはできません。

-   外部キーの列と参照先の親テーブルの列には同じインデックスが設定されており、インデックス内の列の順序は外部キーの列の順序と一致しています。これは、外部キー制約チェックを実行する際に、インデックスを使用してテーブル全体のスキャンを回避するためです。

    -   親テーブルに対応する外部キーインデックスがない場合、エラー`ERROR 1822: Failed to add the foreign key constraint. Missing index for constraint 'fk' in the referenced table 't'`が報告されます。
    -   子テーブルに対応する外部キーインデックスが存在しない場合、外部キーと同じ名前のインデックスが自動的に作成されます。

-   `BLOB`または`TEXT`型の列に外部キーを作成することはサポートされていません。

-   パーティションテーブルに外部キーを作成することはサポートされていません。

-   仮想生成列に外部キーを作成することはサポートされていません。

## 参照操作 {#reference-operations}

`UPDATE`または`DELETE`操作が親テーブルの外部キー値に影響を与える場合、子テーブルの対応する外部キー値は、外部キー定義の`ON UPDATE`または`ON DELETE`句で定義された参照操作によって決定されます。参照操作には、次のものが含まれます。

-   `CASCADE` : `UPDATE`または`DELETE`操作が親テーブルに影響を与える場合、子テーブルの対応する行を自動的に更新または削除します。カスケード操作は深さ優先で実行されます。
-   `SET NULL` : `NULL`操作が親テーブルに影響を与える場合、子テーブルの対応する外部キー列を自動的に {{B `UPDATE` `DELETE`に設定します。
-   `RESTRICT` : 子テーブルに一致する行が含まれている場合、 `UPDATE`または`DELETE`操作を拒否します。
-   `NO ACTION` : `RESTRICT`と同じです。
-   `SET DEFAULT` : `RESTRICT`と同じです。

親テーブルに一致する外部キー値がない場合、子テーブルに対する`INSERT`または`UPDATE`操作は拒否されます。

外部キー定義で`ON DELETE`または`ON UPDATE`が指定されていない場合、デフォルトの動作は`NO ACTION`です。

外部キーが`STORED GENERATED COLUMN`で定義されている場合、 `CASCADE` 、 `SET NULL` 、および`SET DEFAULT`の参照はサポートされません。

## 外部キーの使用例 {#usage-examples-of-foreign-keys}

次の例では、単一列の外部キーを使用して親テーブルと子テーブルを関連付けています。

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

以下は`product_order`テーブルに、他の 2 つのテーブルを参照する 2 つの外部キーがある、より複雑な例です。一方の外部キーは`product`テーブルの 2 つのインデックスを参照し、もう一方の外部キーは`customer`テーブルの 1 つのインデックスを参照します。

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

外部キーは自己参照型、つまり同じテーブルを参照する型にすることができます。 `ALTER TABLE`を使用してテーブルに外部キー制約を追加する場合は、まず外部キーが参照する親テーブルの列にインデックスを作成する必要があります。

## 外部キー制約を削除する {#delete-a-foreign-key-constraint}

外部キー制約を削除するには、次の`ALTER TABLE`ステートメントを使用できます。

```sql
ALTER TABLE table_name DROP FOREIGN KEY fk_identifier;
```

外部キー制約が作成時に名前付けされている場合は、その名前を参照して外部キー制約を削除できます。そうでない場合は、自動的に生成された制約名を使用して制約を削除する必要があります。 `SHOW CREATE TABLE`を使用すると、外部キー名を表示できます。

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

## 外部キー制約チェック {#foreign-key-constraint-check}

TiDBは外部キー制約チェックをサポートしており、これはシステム変数[`foreign_key_checks`](/system-variables.md#foreign_key_checks)によって制御されます。デフォルトでは、この変数は`ON`に設定されており、外部キー制約チェックが有効になっています。この変数には`GLOBAL`と`SESSION` 2つのスコープがあります。この変数を有効にしておくことで、外部キー参照関係の整合性を確保できます。

外部キー制約チェックを無効にした場合の影響は以下のとおりです。

-   外部キーによって参照されている親テーブルを削除する場合、削除が成功するのは、外部キー制約チェックが無効になっている場合のみです。
-   データベースにデータをインポートする際、テーブルの作成順序が外部キーの依存関係の順序と異なる場合があり、その結果、テーブルの作成が失敗する可能性があります。外部キー制約チェックを無効にした場合にのみ、テーブルを正常に作成できます。さらに、外部キー制約チェックを無効にすることで、データインポートの速度を向上させることができます。
-   データベースにデータをインポートする際、子テーブルのデータが先にインポートされるとエラーが発生します。外部キー制約チェックを無効にした場合にのみ、子テーブルのデータを正常にインポートできます。
-   実行される`ALTER TABLE`操作に外部キーの変更が含まれる場合、この操作は外部キー制約チェックが無効になっている場合にのみ成功します。

外部キー制約チェックが無効になっている場合、以下のシナリオを除き、外部キー制約チェックおよび参照操作は実行されません。

-   `ALTER TABLE`の実行によって外部キーの定義が誤っている可能性がある場合でも、実行中にエラーが報告されます。
-   外部キーに必要なインデックスを削除する場合は、まず外部キー自体を削除する必要があります。そうしないと、エラーが発生します。
-   外部キーを作成した際に、関連する条件や制約を満たしていない場合、エラーが報告されます。

## ロック {#locking}

`INSERT` `UPDATE`子テーブルに挿入または子テーブルに挿入すると、外部キー制約は、対応する外部キー値が親テーブルに存在するかどうかを確認し、他の操作が外部キー値を削除して外部キー制約に違反するのを防ぐために、親テーブルの対応する行をロックします。

デフォルトでは、悲観的トランザクションでは、親テーブルの行に対する外部キーチェックのロック動作は、対応する行に対して`SELECT ... FOR UPDATE`を使用してロック読み取りを実行すること（つまり、排他ロックを取得すること）と同等です。子テーブルに対する高同時書き込みシナリオで、多数のトランザクションが同じ親テーブルの行を繰り返し参照する場合、深刻なロック競合が発生する可能性があります。

システム変数[`tidb_foreign_key_check_in_shared_lock`](/system-variables.md#tidb_foreign_key_check_in_shared_lock-new-in-v856)有効にすると、外部キーチェックで共有ロックを使用できるようになります。共有ロックを使用すると、複数のトランザクションが同じ親テーブルの行に対して同時に外部キーチェックを実行できるため、ロックの競合が軽減され、子テーブルへの同時書き込みのパフォーマンスが向上します。

## 外部キーの定義とメタデータ {#definition-and-metadata-of-foreign-keys}

外部キー制約の定義を表示するには、 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)ステートメントを実行します。

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

外部キーに関する情報は、以下のいずれかのシステムテーブルを使用して取得することもできます。

-   [`INFORMATION_SCHEMA.KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)
-   [`INFORMATION_SCHEMA.TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)
-   [`INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`](/information-schema/information-schema-referential-constraints.md)

以下に例を示します。

`INFORMATION_SCHEMA.KEY_COLUMN_USAGE`システムテーブルから外部キーに関する情報を取得します。

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

`INFORMATION_SCHEMA.TABLE_CONSTRAINTS`システムテーブルから外部キーに関する情報を取得します。

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

`INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`システムテーブルから外部キーに関する情報を取得します。

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

## 外部キーを使用した実行計画をビュー {#view-execution-plans-with-foreign-keys}

`EXPLAIN`ステートメントを使用すると、実行プランを表示できます。 `Foreign_Key_Check`演算子は、実行される DML ステートメントに対して外部キー制約チェックを実行します。

```sql
mysql> explain insert into child values (1,1);
+-----------------------+---------+------+---------------+-------------------------------+
| id                    | estRows | task | access object | operator info                 |
+-----------------------+---------+------+---------------+-------------------------------+
| Insert_1              | N/A     | root |               | N/A                           |
| └─Foreign_Key_Check_3 | 0.00    | root | table:parent  | foreign_key:fk_1, check_exist |
+-----------------------+---------+------+---------------+-------------------------------+
```

`EXPLAIN ANALYZE`ステートメントを使用すると、外部キー参照の動作を確認できます。 `Foreign_Key_Cascade`演算子は、実行される DML ステートメントに対して外部キー参照を実行します。

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

### TiDBバージョンの互換性 {#compatibility-between-tidb-versions}

バージョン 6.6.0 より前の TiDB では、外部キーを作成する構文がサポートされていましたが、作成された外部キーは無効でした。バージョン 6.6.0 より前に作成された TiDB クラスタをバージョン 6.6.0 以降にアップグレードしても、アップグレード前に作成された外部キーは無効のままです。バージョン 6.6.0 以降で作成された外部キーのみが有効です。無効な外部キーを削除して新しい外部キーを作成することで、外部キー制約を有効にできます。 `SHOW CREATE TABLE`ステートメントを使用して、外部キーが有効かどうかを確認できます。無効な外部キーには`/* FOREIGN KEY INVALID */`コメントが付きます。

```sql
mysql> SHOW CREATE TABLE child\G
***************************[ 1. row ]***************************
Table        | child
Create Table | CREATE TABLE `child` (
  `id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE /* FOREIGN KEY INVALID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

### TiDBツールとの互換性 {#compatibility-with-tidb-tools}

<CustomContent platform="tidb">

-   [DM](/dm/dm-overview.md) : v8.5.6以降、DMは実験的機能として外部キー制約を使用するテーブルのレプリケーションをサポートしています。サポートされているシナリオと制限事項については、 [DM互換性カタログ](/dm/dm-compatibility-catalog.md#foreign-key-cascade-operations)を参照してください。 v8.5.6より前のバージョンでは、DMはTiDBへのデータレプリケーション時に[`foreign_key_checks`](/system-variables.md#foreign_key_checks)システム変数を無効にするため、カスケード操作はダウンストリームクラスタにレプリケートされません。
-   [TiCDC](/ticdc/ticdc-overview.md) v6.6.0 は外部キーに対応しています。以前のバージョンの TiCDC では、外部キーを持つテーブルをレプリケートする際にエラーが発生する場合があります。TiCDC バージョン 6.6.0 より前のバージョンを使用する場合は、ダウンストリーム TiDB クラスタの`foreign_key_checks`を無効にすることをお勧めします。
-   [BR](/br/backup-and-restore-overview.md) v6.6.0 は外部キーに対応しています。以前のバージョンのBRでは、外部キーを持つテーブルを v6.6.0 以降のクラスタに復元する際にエラーが発生する場合があります。v6.6.0 より前のバージョンのBRを使用する場合は、クラスタを復元する前に、ダウンストリーム TiDB クラスタの`foreign_key_checks`無効にすることをお勧めします。
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用する場合、対象テーブルで外部キーが使用されている場合は、データのインポート前にダウンストリーム TiDB クラスタの`foreign_key_checks`を無効にすることをお勧めします。v6.6.0 より前のバージョンでは、このシステム変数を無効にしても効果がなく、ダウンストリーム データベース ユーザーに`REFERENCES`権限を付与するか、ダウンストリーム データベースに対象テーブルを事前に手動で作成して、スムーズなデータインポートを確保する必要があります。

</CustomContent>

-   [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)外国語キーに対応しています。

<CustomContent platform="tidb">

-   [同期差分検査ツール](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用してアップストリーム データベースとダウンストリーム データベースの間でデータを比較するときに、データベースのバージョンが異なり、[下流のTiDBに無効な外部キーがあります](#compatibility-between-tidb-versions)がある場合、sync-diff-inspector はテーブル スキーマの不整合エラーを報告することがあります。これは、TiDB v6.6.0 が無効な外部キーに対する`/* FOREIGN KEY INVALID */`コメントを追加しているためです。

</CustomContent>

### MySQLとの互換性 {#compatibility-with-mysql}

外部キーを作成する際に名前を指定しない場合、TiDB によって生成される名前は MySQL によって生成される名前とは異なります。たとえば、TiDB によって生成される外部キー名は`fk_1` 、 `fk_2` 、 `fk_3`ですが、MySQL によって生成される外部キー名は`table_name_ibfk_1` 、 `table_name_ibfk_2` 、 `table_name_ibfk_3`です。

MySQLとTiDBはどちらも「インライン`REFERENCES`仕様」を解析しますが、無視します。 `REFERENCES`定義の一部である`FOREIGN KEY`仕様のみがチェックされ、適用されます。次の例では`REFERENCES`句を使用して外部キー制約を作成します。

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

出力結果から、 `child`テーブルには外部キーが存在しないことがわかります。

```sql
+-------+-------------------------------------------------------------+
| Table | Create Table                                                |
+-------+-------------------------------------------------------------+
| child | CREATE TABLE `child` (                                      |
|       |   `id` int DEFAULT NULL,                                |
|       |   `pid` int DEFAULT NULL                                |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+-------------------------------------------------------------+
```
