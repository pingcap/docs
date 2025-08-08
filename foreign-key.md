---
title: FOREIGN KEY Constraints
summary: TiDB データベースの FOREIGN KEY 制約の使用法の概要。
---

# 外部キー制約 {#foreign-key-constraints}

外部キーは関連データのテーブル間参照を可能にし、外部キー制約は関連データの一貫性を確保します。TiDBはv6.6.0以降、外部キーと外部キー制約をサポートしています。v8.5.0以降、この機能は一般提供となります。

> **警告：**
>
> 外部キー機能は通常、 [参照整合性](https://en.wikipedia.org/wiki/Referential_integrity)制約チェックを強制するために使用されます。パフォーマンスの低下を引き起こす可能性があるため、パフォーマンスが重視されるシナリオで使用する前に、徹底的なテストを実施することをお勧めします。

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
-   外部キー名は現在のテーブル内で一意である必要があります。一意でない場合、外部キーの作成時にエラー`ERROR 1826: Duplicate foreign key constraint name 'fk'`が報告されます。

## 制限 {#restrictions}

外部キーを作成するときは、次の条件を満たす必要があります。

-   親テーブルも子テーブルも一時テーブルではありません。

-   ユーザーには親テーブルに対する権限`REFERENCES`あります。

-   親テーブルと子テーブルの外部キーによって参照される列は同じデータ型であり、サイズ、精度、長さ、文字セット、および照合順序が同じです。

-   外部キーの列はそれ自体を参照できません。

-   外部キーの列と参照先の親テーブルの列は同じインデックスを持ち、インデックス内の列の順序は外部キーの順序と一致しています。これは、外部キー制約のチェックを行う際に、インデックスを使用してテーブル全体のスキャンを回避するためです。

    -   親テーブルに対応する外部キー インデックスがない場合、エラー`ERROR 1822: Failed to add the foreign key constraint. Missing index for constraint 'fk' in the referenced table 't'`が報告されます。
    -   子テーブルに対応する外部キー インデックスがない場合、外部キーと同じ名前のインデックスが自動的に作成されます。

-   `BLOB`または`TEXT`タイプの列に外部キーを作成することはサポートされていません。

-   パーティションテーブルに外部キーを作成することはサポートされていません。

-   仮想生成列に外部キーを作成することはサポートされていません。

## 参照操作 {#reference-operations}

`UPDATE`または`DELETE`操作が親テーブルの外部キー値に影響を与える場合、子テーブルの対応する外部キー値は、外部キー定義の`ON UPDATE`または`ON DELETE`節で定義された参照操作によって決定されます。参照操作には以下のものが含まれます。

-   `CASCADE` : `UPDATE`または`DELETE`操作が親テーブルに影響を及ぼす場合、子テーブル内の対応する行を自動的に更新または削除します。カスケード操作は深さ優先方式で実行されます。
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

以下はより複雑な例です。テーブル`product_order`には、他の2つのテーブルを参照する外部キーが2つあります。1つの外部キーはテーブル`product`の2つのインデックスを参照し、もう1つの外部キーはテーブル`customer`の1つのインデックスを参照します。

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

外部キーは自己参照、つまり同じテーブルを参照することができます。1 `ALTER TABLE`使用してテーブルに外部キー制約を追加する場合は、まず外部キーが参照する親テーブルの列にインデックスを作成する必要があります。

## 外部キー制約を削除する {#delete-a-foreign-key-constraint}

外部キー制約を削除するには、次の`ALTER TABLE`ステートメントを使用できます。

```sql
ALTER TABLE table_name DROP FOREIGN KEY fk_identifier;
```

外部キー制約の作成時に名前が付けられている場合は、その名前を参照して外部キー制約を削除できます。そうでない場合は、自動的に生成された制約名を使用して制約を削除する必要があります。外部キー名を表示するには、 `SHOW CREATE TABLE`使用します。

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

TiDBは外部キー制約チェックをサポートしており、これはシステム変数[`foreign_key_checks`](/system-variables.md#foreign_key_checks)によって制御されます。デフォルトでは、この変数は`ON`に設定されており、外部キー制約チェックが有効であることを意味します。この変数には`GLOBAL`と`SESSION` 2つのスコープがあります。この変数を有効のままにしておくことで、外部キー参照関係の整合性を確保できます。

外部キー制約チェックを無効にした場合の効果は次のとおりです。

-   外部キーによって参照される親テーブルを削除する場合、外部キー制約チェックが無効になっている場合にのみ削除が成功します。
-   データベースにデータをインポートする際、テーブルの作成順序が外部キーの依存関係の順序と異なる場合があり、テーブルの作成に失敗する可能性があります。外部キー制約のチェックを無効にした場合のみ、テーブルを正常に作成できます。また、外部キー制約のチェックを無効にすると、データのインポート速度が向上します。
-   データベースにデータをインポートする際、子テーブルのデータを先にインポートするとエラーが発生します。子テーブルのデータを正常にインポートするには、外部キー制約チェックを無効にしてください。
-   実行される操作`ALTER TABLE`外部キーの変更が含まれる場合、この操作は外部キー制約チェックが無効になっている場合にのみ成功します。

外部キー制約チェックが無効になっている場合、次のシナリオを除き、外部キー制約チェックと参照操作は実行されません。

-   `ALTER TABLE`の実行によって外部キーの定義が間違ってしまう可能性がある場合は、実行中にエラーが報告されます。
-   外部キーに必要なインデックスを削除する場合は、まず外部キーを削除する必要があります。そうしないと、エラーが報告されます。
-   外部キーを作成したが、関連する条件または制限を満たしていない場合は、エラーが報告されます。

## ロック {#locking}

子テーブルが`INSERT`または`UPDATE`場合、外部キー制約は対応する外部キー値が親テーブルに存在するかどうかを確認し、外部キー制約に違反する他の操作によって外部キー値が削除されるのを防ぐため、親テーブルの行をロックします。このロック動作は、親テーブルで外部キー値が配置されている行に対して`SELECT FOR UPDATE`操作を実行するのと同等です。

TiDBは現在`LOCK IN SHARE MODE`サポートしていないため、子テーブルが大量の同時書き込みを受け付け、参照される外部キー値のほとんどが同じ場合、深刻なロック競合が発生する可能性があります。子テーブルに大量のデータを書き込む場合は、 [`foreign_key_checks`](/system-variables.md#foreign_key_checks)無効にすることをお勧めします。

## 外部キーの定義とメタデータ {#definition-and-metadata-of-foreign-keys}

外部キー制約の定義を表示するには、次の[`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)ステートメントを実行します。

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

`EXPLAIN`ステートメントを使用して実行プランを表示できます。3 `Foreign_Key_Check`演算子は、実行されるDMLステートメントの外部キー制約チェックを実行します。

```sql
mysql> explain insert into child values (1,1);
+-----------------------+---------+------+---------------+-------------------------------+
| id                    | estRows | task | access object | operator info                 |
+-----------------------+---------+------+---------------+-------------------------------+
| Insert_1              | N/A     | root |               | N/A                           |
| └─Foreign_Key_Check_3 | 0.00    | root | table:parent  | foreign_key:fk_1, check_exist |
+-----------------------+---------+------+---------------+-------------------------------+
```

`EXPLAIN ANALYZE`ステートメントを使用すると、外部キー参照の動作の実行状況を確認できます。3 演算子`Foreign_Key_Cascade` 、実行される DML ステートメントの外部キー参照を実行します。

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

### TiDBバージョン間の互換性 {#compatibility-between-tidb-versions}

v6.6.0より前のTiDBでは、外部キーを作成する構文がサポートされていますが、作成された外部キーは無効です。v6.6.0より前に作成されたTiDBクラスターをv6.6.0以降にアップグレードした場合、アップグレード前に作成された外部キーは無効のままです。v6.6.0以降のバージョンで作成された外部キーのみが有効になります。無効な外部キーを削除し、新しい外部キーを作成することで、外部キー制約を有効にすることができます。1 `SHOW CREATE TABLE`を使用して、外部キーが有効かどうかを確認できます。無効な外部キーには`/* FOREIGN KEY INVALID */`コメントが付きます。

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

-   [DM](/dm/dm-overview.md)外部キーをサポートしていません。DMは、TiDBへのデータレプリケーション時に下流TiDBの[`foreign_key_checks`](/system-variables.md#foreign_key_checks)無効にします。そのため、外部キーによるカスケード操作は上流から下流にレプリケーションされず、データの不整合が発生する可能性があります。
-   [TiCDC](/ticdc/ticdc-overview.md) v6.6.0は外部キーと互換性があります。以前のバージョンのTiCDCでは、外部キーを持つテーブルのレプリケーション時にエラーが報告される可能性があります。v6.6.0より前のバージョンのTiCDCを使用する場合は、下流のTiDBクラスターの`foreign_key_checks`無効にすることをお勧めします。
-   [BR](/br/backup-and-restore-overview.md) v6.6.0 は外部キーと互換性があります。以前のバージョンのBRでは、外部キーを持つテーブルを v6.6.0 以降のクラスターにリストアするとエラーが報告される可能性があります。v6.6.0 より前のBRを使用する場合は、クラスターをリストアする前に、下流の TiDB クラスターの`foreign_key_checks`無効にすることをお勧めします。
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用する場合、ターゲットテーブルが外部キーを使用している場合は、データをインポートする前に、下流 TiDB クラスターの`foreign_key_checks`無効にすることをお勧めします。v6.6.0 より前のバージョンでは、このシステム変数を無効にしても効果はありません。スムーズなデータインポートを確実に行うには、下流データベースユーザーに`REFERENCES`権限を付与するか、下流データベースにターゲットテーブルを事前に手動で作成しておく必要があります。

</CustomContent>

-   [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)外部キーと互換性があります。

<CustomContent platform="tidb">

-   上流データベースと下流データベース間でデータを比較する際に[同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)使用する際、データベースのバージョンが異なり、かつ[下流のTiDBに無効な外部キーがある](#compatibility-between-tidb-versions)存在する場合、sync-diff-inspector がテーブルスキーマ不整合エラーを報告することがあります。これは、TiDB v6.6.0 で無効な外部キーに対して`/* FOREIGN KEY INVALID */`コメントが追加されたためです。

</CustomContent>

### MySQLとの互換性 {#compatibility-with-mysql}

名前を指定せずに外部キーを作成した場合、TiDBによって生成される名前はMySQLによって生成される名前とは異なります。例えば、TiDBによって生成される外部キー名は`fk_1` 、 `fk_2` 、 `fk_3`ですが、MySQLによって生成される外部キー名は`table_name_ibfk_1` 、 `table_name_ibfk_2` 、 `table_name_ibfk_3`です。

MySQLとTiDBはどちらも「インライン`REFERENCES`仕様」を解析しますが、無視します。5 `FOREIGN KEY`定義のうち、 `REFERENCES`仕様のみがチェックされ、適用されます。次の例では、 `REFERENCES`句を使用して外部キー制約を作成します。

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
|       |   `id` int DEFAULT NULL,                                |
|       |   `pid` int DEFAULT NULL                                |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+-------------------------------------------------------------+
```
