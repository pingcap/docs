---
title: Clustered Indexes
summary: クラスター化インデックスの概念、ユーザー シナリオ、使用法、制限、および互換性について学習します。
---

# クラスター化インデックス {#clustered-indexes}

TiDBはバージョン5.0以降、クラスター化インデックス機能をサポートしています。この機能は、主キーを含むテーブルへのデータの格納方法を制御します。これにより、TiDBは特定のクエリのパフォーマンスを向上させる方法でテーブルを整理できるようになります。

ここでの*「クラスター化」*という用語は*、データの保存方法の構成*を指し、*連携して動作するデータベースサーバーのグループを*指すものではありません。一部のデータベース管理システムでは、クラスター化インデックステーブルを*インデックス構成テーブル*（IOT）と呼びます。

現在、TiDB の主キーを含むテーブルは次の 2 つのカテゴリに分類されます。

-   `NONCLUSTERED` : テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを持つテーブルでは、行データのキーはTiDBによって暗黙的に割り当てられた内部`_tidb_rowid`で構成されます。主キーは本質的に一意のインデックスであるため、非クラスター化インデックスを持つテーブルでは、行を格納するために少なくとも2つのキーと値のペアが必要です。これらのペアは次のとおりです。
    -   `_tidb_rowid` (キー) - 行データ (値)
    -   主キーデータ（キー） - `_tidb_rowid` （値）
-   `CLUSTERED` : テーブルの主キーはクラスター化インデックスです。クラスター化インデックスを持つテーブルでは、行データのキーはユーザーが指定した主キーデータで構成されます。したがって、クラスター化インデックスを持つテーブルでは、行を格納するために必要なキーと値のペアは1つだけです。これは次のようになります。
    -   主キーデータ（キー） - 行データ（値）

> **注記：**
>
> TiDB は、テーブルの`PRIMARY KEY`によるクラスタリングのみをサポートします。クラスター化インデックスが有効になっている場合、 *「* `PRIMARY KEY`と*「クラスター化インデックス」*は同じ意味で使用できます。 `PRIMARY KEY`は制約（論理プロパティ）を指し、「クラスター化インデックス」はデータの格納方法の物理的な実装を表します。

## ユーザーシナリオ {#user-scenarios}

非クラスター化インデックスを持つテーブルと比較すると、クラスター化インデックスを持つテーブルでは、次のシナリオでパフォーマンスとスループットの利点が向上します。

-   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
-   同等の条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
-   範囲条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
-   同等条件または範囲条件を持つクエリに主キー プレフィックスのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。

一方、クラスター化インデックスを持つテーブルには、いくつかの欠点があります。以下をご覧ください。

-   近い値を持つ主キーを多数挿入すると、書き込みホットスポットの問題が発生する可能性があります。
-   主キーのデータ型が 64 ビットより大きい場合、特に複数のセカンダリ インデックスがある場合、テーブル データはより多くのstorageスペースを占有します。

## 使用法 {#usages}

### クラスター化インデックスを持つテーブルを作成する {#create-a-table-with-clustered-indexes}

TiDB v5.0以降では、 `CREATE TABLE`文の`PRIMARY KEY`後に非予約キーワード`CLUSTERED`または`NONCLUSTERED`追加することで、テーブルの主キーがクラスター化インデックスであるかどうかを指定できます。例：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) CLUSTERED);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
```

キーワード`KEY`と`PRIMARY KEY`列定義では同じ意味を持つことに注意してください。

TiDBでは、 [コメント構文](/comment-syntax.md)使って主キーの型を指定することもできます。例：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] NONCLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] CLUSTERED */);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] NONCLUSTERED */);
```

キーワード`CLUSTERED` / `NONCLUSTERED`を明示的に指定しないステートメントの場合、デフォルトの動作はシステム変数[`@@global.tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)によって制御されます。この変数でサポートされている値は次のとおりです。

-   `OFF`主キーがデフォルトで非クラスター化インデックスとして作成されることを示します。
-   `ON` 、主キーがデフォルトでクラスター化インデックスとして作成されることを示します。
-   `INT_ONLY` 、動作が設定項目`alter-primary-key`によって制御されることを示します。4 `alter-primary-key` `true`に設定すると、主キーはデフォルトで非クラスター化インデックスとして作成されます`false`に設定すると、整数列で構成される主キーのみがクラスター化インデックスとして作成されます。

`@@global.tidb_enable_clustered_index`のデフォルト値は`ON`です。

### クラスター化インデックスの追加または削除 {#add-or-drop-clustered-indexes}

TiDBは、テーブル作成後のクラスター化インデックスの追加や削除をサポートしていません。また、クラスター化インデックスと非クラスター化インデックス間の相互変換もサポートしていません。例えば：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) CLUSTERED; -- Currently not supported.
ALTER TABLE t DROP PRIMARY KEY;     -- If the primary key is a clustered index, then not supported.
ALTER TABLE t DROP INDEX `PRIMARY`; -- If the primary key is a clustered index, then not supported.
```

### 非クラスター化インデックスを追加または削除する {#add-or-drop-non-clustered-indexes}

TiDBは、テーブル作成後に非クラスター化インデックスを追加または削除できます。キーワード`NONCLUSTERED`明示的に指定するか、省略することができます。例：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) NONCLUSTERED;
ALTER TABLE t ADD PRIMARY KEY(b, a); -- If you omit the keyword, the primary key is a non-clustered index by default.
ALTER TABLE t DROP PRIMARY KEY;
ALTER TABLE t DROP INDEX `PRIMARY`;
```

### 主キーがクラスター化インデックスであるかどうかを確認する {#check-whether-the-primary-key-is-a-clustered-index}

次のいずれかの方法を使用して、テーブルの主キーがクラスター化インデックスであるかどうかを確認できます。

-   コマンド`SHOW CREATE TABLE`を実行します。
-   コマンド`SHOW INDEX FROM`を実行します。
-   システムテーブル`information_schema.tables`の`TIDB_PK_TYPE`列をクエリします。

コマンド`SHOW CREATE TABLE`実行すると、 `PRIMARY KEY`の属性が`CLUSTERED`か`NONCLUSTERED`を確認できます。例:

```sql
mysql> SHOW CREATE TABLE t;
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                      |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` bigint NOT NULL,
  `b` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

コマンド`SHOW INDEX FROM`実行すると、列`Clustered`の結果が`YES`か`NO`確認できます。例:

```sql
mysql> SHOW INDEX FROM t;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| t     |          0 | PRIMARY  |            1 | a           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
1 row in set (0.01 sec)
```

システムテーブル`information_schema.tables`の列`TIDB_PK_TYPE`クエリして、結果が`CLUSTERED`か`NONCLUSTERED`確認することもできます。例えば、次のようになります。

```sql
mysql> SELECT TIDB_PK_TYPE FROM information_schema.tables WHERE table_schema = 'test' AND table_name = 't';
+--------------+
| TIDB_PK_TYPE |
+--------------+
| CLUSTERED    |
+--------------+
1 row in set (0.03 sec)
```

## 制限事項 {#limitations}

現在、クラスター化インデックス機能にはいくつかの異なる制限事項があります。以下をご覧ください。

-   サポートされず、サポート プランにも含まれない状況:
    -   クラスター化インデックスと属性[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)併用はサポートされていません。また、属性[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 、属性[`AUTO_RANDOM`](/auto-random.md)以外のクラスター化インデックスを持つテーブルには適用されません。
    -   クラスター化インデックスを持つテーブルのダウングレードはサポートされていません。このようなテーブルをダウングレードする必要がある場合は、代わりに論理バックアップツールを使用してデータを移行してください。
-   まだサポートされていないがサポート計画に含まれている状況:
    -   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。

クラスター化インデックスを属性`SHARD_ROW_ID_BITS`と一緒に使用すると、TiDB は次のエラーを報告します。

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED) SHARD_ROW_ID_BITS = 3;
ERROR 8200 (HY000): Unsupported shard_row_id_bits for table with primary key as row id
```

## 互換性 {#compatibility}

### 以前のバージョンおよびそれ以降の TiDB バージョンとの互換性 {#compatibility-with-earlier-and-later-tidb-versions}

TiDB は、クラスター化インデックスを持つテーブルのアップグレードをサポートしますが、そのようなテーブルのダウングレードはサポートしません。つまり、新しいバージョンの TiDB のクラスター化インデックスを持つテーブルのデータは、以前のバージョンでは使用できません。

クラスター化インデックス機能は、TiDB v3.0 および v4.0 で部分的にサポートされています。以下の要件が完全に満たされている場合、デフォルトで有効になります。

-   表には`PRIMARY KEY`が含まれています。
-   `PRIMARY KEY` 1 つの列のみで構成されます。
-   `PRIMARY KEY`は`INTEGER`です。

TiDB v5.0以降、クラスター化インデックス機能はすべての種類の主キーで完全にサポートされていますが、デフォルトの動作はTiDB v3.0およびv4.0と同じです。デフォルトの動作を変更するには、システム変数`@@tidb_enable_clustered_index`を`ON`または`OFF`設定できます。詳細については、 [クラスター化インデックスを持つテーブルを作成する](#create-a-table-with-clustered-indexes)参照してください。

### MySQLとの互換性 {#compatibility-with-mysql}

TiDB固有のコメント構文では、キーワード`CLUSTERED`と`NONCLUSTERED`コメントで囲むことができます。5 `SHOW CREATE TABLE`結果には、TiDB固有のSQLコメントも含まれます。MySQLデータベースおよび以前のバージョンのTiDBデータベースでは、これらのコメントは無視されます。

### TiDB移行ツールとの互換性 {#compatibility-with-tidb-migration-tools}

クラスター化インデックス機能は、バージョン 5.0 以降の次の移行ツールとのみ互換性があります。

-   バックアップおよび復元ツール: BR、 Dumpling、およびTiDB Lightning。
-   データ移行およびレプリケーション ツール: DM および TiCDC。

ただし、v5.0 BRツールを使用してテーブルをバックアップおよび復元しても、非クラスター化インデックスを持つテーブルをクラスター化インデックスを持つテーブルに変換することはできません。また、その逆も同様です。

### 他の TiDB 機能との互換性 {#compatibility-with-other-tidb-features}

複合主キーまたは整数以外の単一の主キーを持つテーブルの場合、主キーを非クラスター化インデックスからクラスター化インデックスに変更すると、その行データのキーも変更されます。したがって、TiDB バージョン 5.0 より前のバージョンで実行可能な`SPLIT TABLE BY/BETWEEN`ステートメントは、TiDB バージョン 5.0 以降では実行できなくなります。クラスター化インデックスを持つテーブルを`SPLIT TABLE BY/BETWEEN`を使用して分割する場合は、整数値ではなく、主キー列の値を指定する必要があります。次の例を参照してください。

```sql
mysql> create table t (a int, b varchar(255), primary key(a, b) clustered);
Query OK, 0 rows affected (0.01 sec)
mysql> split table t between (0) and (1000000) regions 5;
ERROR 1105 (HY000): Split table region lower value count should be 2
mysql> split table t by (0), (50000), (100000);
ERROR 1136 (21S01): Column count doesn't match value count at row 0
mysql> split table t between (0, 'aaa') and (1000000, 'zzz') regions 5;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  4 |                    1 |
+--------------------+----------------------+
1 row in set (0.00 sec)
mysql> split table t by (0, ''), (50000, ''), (100000, '');
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  3 |                    1 |
+--------------------+----------------------+
1 row in set (0.01 sec)
```

属性[`AUTO_RANDOM`](/auto-random.md)クラスター化インデックスでのみ使用できます。それ以外の場合、TiDBは次のエラーを返します。

```sql
mysql> create table t (a bigint primary key nonclustered auto_random);
ERROR 8216 (HY000): Invalid auto random: column a is not the integer primary key, or the primary key is nonclustered
```
