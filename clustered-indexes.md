---
title: Clustered Indexes
summary: Learn the concept, user scenarios, usages, limitations, and compatibility of clustered indexes.
---

# クラスター化インデックス {#clustered-indexes}

TiDBは、v5.0以降のクラスター化インデックス機能をサポートしています。この機能は、主キーを含むテーブルにデータを格納する方法を制御します。 TiDBは、特定のクエリのパフォーマンスを向上させる方法でテーブルを整理する機能を提供します。

このコンテキストでの*クラスター化*という用語<em>は、データの保存方法の編成を</em>指し、<em>一緒に動作するデータベースサーバーのグループでは</em>ありません。一部のデータベース管理システムでは、クラスター化インデックスを<em>インデックス編成テーブル</em>（IOT）と呼んでいます。

現在、TiDBの主キーを含むテーブルは、次の2つのカテゴリに分類されます。

-   `NONCLUSTERED` ：テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを持つテーブルでは、行データのキーは、TiDBによって暗黙的に割り当てられた内部`_tidb_rowid`で構成されます。主キーは本質的に一意のインデックスであるため、非クラスター化インデックスを持つテーブルには、行を格納するために少なくとも2つのキーと値のペアが必要です。
    -   `_tidb_rowid` （キー）-行データ（値）
    -   主キーデータ（キー） `_tidb_rowid` （値）
-   `CLUSTERED` ：テーブルの主キーはクラスター化インデックスです。クラスタ化インデックスを持つテーブルでは、行データのキーは、ユーザーが指定した主キーデータで構成されます。したがって、クラスター化インデックスを持つテーブルは、行を格納するために1つのキーと値のペアのみを必要とします。
    -   主キーデータ（キー）-行データ（値）

> **ノート：**
>
> TiDBは、テーブルの`PRIMARY KEY`によるクラスタリングのみをサポートします。クラスター化インデックスを有効にすると*、* `PRIMARY KEY`という用語と<em>クラスター化インデックス</em>は同じ意味で使用される場合があります。 `PRIMARY KEY`は制約（論理プロパティ）を示し、クラスター化されたインデックスはデータの格納方法の物理的な実装を示します。

## ユーザーシナリオ {#user-scenarios}

非クラスター化インデックスを持つテーブルと比較して、クラスター化インデックスを持つテーブルは、次のシナリオでパフォーマンスとスループットの利点が向上します。

-   データが挿入されると、クラスター化されたインデックスにより、ネットワークからのインデックスデータの書き込みが1回減ります。
-   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックスデータの読み取りを1回減らします。
-   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックスデータの複数の読み取りを減らします。
-   同等または範囲の条件を持つクエリに主キープレフィックスのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックスデータの複数の読み取りを削減します。

一方、クラスター化インデックスを持つテーブルには、いくつかの欠点があります。以下を参照してください。

-   近い値を持つ多数の主キーを挿入すると、書き込みホットスポットの問題が発生する可能性があります。
-   主キーのデータ型が64ビットより大きい場合、特に複数のセカンダリインデックスがある場合、テーブルデータはより多くのストレージスペースを占有します。

## 使用法 {#usages}

## クラスタ化インデックスを使用してテーブルを作成する {#create-a-table-with-clustered-indexes}

TiDB v5.0以降、 `CREATE TABLE`ステートメントの`PRIMARY KEY`の後に予約されていないキーワード`CLUSTERED`または`NONCLUSTERED`を追加して、テーブルの主キーがクラスター化インデックスであるかどうかを指定できます。例えば：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) CLUSTERED);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
```

キーワード`KEY`と`PRIMARY KEY`は、列の定義で同じ意味を持つことに注意してください。

TiDBの[コメント構文](/comment-syntax.md)を使用して、主キーのタイプを指定することもできます。例えば：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] NONCLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] CLUSTERED */);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] NONCLUSTERED */);
```

キーワード`CLUSTERED`を明示的に指定しないステートメントの場合、デフォルトの動作はシステム変数`NONCLUSTERED`によって制御され`@@global.tidb_enable_clustered_index` 。この変数でサポートされている値は次のとおりです。

-   `OFF`は、主キーがデフォルトで非クラスター化インデックスとして作成されることを示します。
-   `ON`は、主キーがデフォルトでクラスター化インデックスとして作成されることを示します。
-   `INT_ONLY`は、動作が構成項目`alter-primary-key`によって制御されていることを示します。 `alter-primary-key`が`true`に設定されている場合、主キーはデフォルトで非クラスター化インデックスとして作成されます。 `false`に設定すると、整数列で構成される主キーのみがクラスター化インデックスとして作成されます。

デフォルト値の`@@global.tidb_enable_clustered_index`は`INT_ONLY`です。

### クラスタ化インデックスを追加または削除する {#add-or-drop-clustered-indexes}

TiDBは、テーブルの作成後のクラスター化インデックスの追加または削除をサポートしていません。また、クラスター化インデックスと非クラスター化インデックス間の相互変換もサポートしていません。例えば：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) CLUSTERED; -- Currently not supported.
ALTER TABLE t DROP PRIMARY KEY;     -- If the primary key is a clustered index, then not supported.
ALTER TABLE t DROP INDEX `PRIMARY`; -- If the primary key is a clustered index, then not supported.
```

### 非クラスター化インデックスを追加または削除する {#add-or-drop-non-clustered-indexes}

TiDBは、テーブルの作成後に非クラスター化インデックスを追加または削除することをサポートしています。キーワード`NONCLUSTERED`を明示的に指定することも、省略することもできます。例えば：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) NONCLUSTERED;
ALTER TABLE t ADD PRIMARY KEY(b, a); -- If you omit the keyword, the primary key is a non-clustered index by default.
ALTER TABLE t DROP PRIMARY KEY;
ALTER TABLE t DROP INDEX `PRIMARY`;
```

### 主キーがクラスター化インデックスであるかどうかを確認します {#check-whether-the-primary-key-is-a-clustered-index}

次のいずれかの方法を使用して、テーブルの主キーがクラスター化インデックスであるかどうかを確認できます。

-   コマンド`SHOW CREATE TABLE`を実行します。
-   コマンド`SHOW INDEX FROM`を実行します。
-   システムテーブル`information_schema.tables`の`TIDB_PK_TYPE`列をクエリします。

コマンド`SHOW CREATE TABLE`を実行すると、 `PRIMARY KEY`の属性が`CLUSTERED`であるか`NONCLUSTERED`であるかを確認できます。例えば：

```sql
mysql> SHOW CREATE TABLE t;
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                      |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` bigint(20) NOT NULL,
  `b` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

コマンド`SHOW INDEX FROM`を実行することにより、列`Clustered`の結果が`YES`または`NO`を示しているかどうかを確認できます。例えば：

```sql
mysql> SHOW INDEX FROM t;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| t     |          0 | PRIMARY  |            1 | a           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
1 row in set (0.01 sec)
```

システムテーブル`information_schema.tables`の列`TIDB_PK_TYPE`にクエリを実行して、結果が`CLUSTERED`か`NONCLUSTERED`かを確認することもできます。例えば：

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

現在、クラスター化インデックス機能にはいくつかの異なるタイプの制限があります。以下を参照してください。

-   サポートされておらず、サポートプランに含まれていない状況：
    -   クラスタ化インデックスを属性[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)と一緒に使用することはサポートされていません。また、属性[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)は、クラスター化インデックスを持つテーブルには有効になりません。
    -   クラスタ化インデックスを使用したテーブルのダウングレードはサポートされていません。このようなテーブルをダウングレードする必要がある場合は、代わりに論理バックアップツールを使用してデータを移行してください。
-   まだサポートされていないが、サポート計画に含まれている状況：
    -   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。
-   特定のバージョンの制限：
    -   v5.0では、クラスター化インデックス機能をTiDBBinlogと一緒に使用することはサポートされていません。 TiDB Binlogを有効にすると、TiDBでは主キーのクラスター化インデックスとして単一の整数列のみを作成できます。 TiDB Binlogは、クラスター化インデックスを持つ既存のテーブルのデータ変更（挿入、削除、更新など）をダウンストリームに複製しません。クラスタ化インデックスを使用してテーブルをダウンストリームにレプリケートする必要がある場合は、クラスタをv5.1にアップグレードするか、代わりにレプリケーションに[TiCDC](/ticdc/ticdc-overview.md)を使用します。

TiDB Binlogを有効にした後、作成するクラスター化インデックスが単一の整数の主キーでない場合、TiDBは次のエラーを返します。

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED);
ERROR 8200 (HY000): Cannot create clustered index table when the binlog is ON
```

クラスタ化インデックスを属性`SHARD_ROW_ID_BITS`と一緒に使用すると、TiDBは次のエラーを報告します。

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED) SHARD_ROW_ID_BITS = 3;
ERROR 8200 (HY000): Unsupported shard_row_id_bits for table with primary key as row id
```

## 互換性 {#compatibility}

### 以前およびそれ以降のTiDBバージョンとの互換性 {#compatibility-with-earlier-and-later-tidb-versions}

TiDBは、クラスター化インデックスを使用したテーブルのアップグレードをサポートしますが、そのようなテーブルのダウングレードはサポートしません。つまり、新しいバージョンのクラスター化インデックスを使用したテーブルのデータは、以前のバージョンでは使用できません。

クラスター化インデックス機能は、TiDBv3.0およびv4.0で部分的にサポートされています。次の要件が完全に満たされると、デフォルトで有効になります。

-   テーブルには`PRIMARY KEY`が含まれています。
-   `PRIMARY KEY`は1つの列のみで構成されます。
-   `PRIMARY KEY`は`INTEGER`です。

TiDB v5.0以降、クラスター化インデックス機能はすべてのタイプの主キーで完全にサポートされていますが、デフォルトの動作はTiDBv3.0およびv4.0と一貫しています。デフォルトの動作を変更するには、システム変数`@@tidb_enable_clustered_index`を`ON`または`OFF`に構成します。詳細については、 [クラスタ化インデックスを使用してテーブルを作成する](#create-a-table-with-clustered-indexes)を参照してください。

### MySQLとの互換性 {#compatibility-with-mysql}

TiDB固有のコメント構文は、キーワード`CLUSTERED`と`NONCLUSTERED`をコメントでラップすることをサポートします。 `SHOW CREATE TABLE`の結果には、TiDB固有のSQLコメントも含まれています。以前のバージョンのMySQLデータベースおよびTiDBデータベースは、これらのコメントを無視します。

### TiDB移行ツールとの互換性 {#compatibility-with-tidb-migration-tools}

クラスタ化インデックス機能は、v5.0以降のバージョンの次の移行ツールとのみ互換性があります。

-   バックアップと復元のツール：BR、Dumpling、TiDBLightning。
-   データ移行およびレプリケーションツール：DMおよびTiCDC。

ただし、v5.0 BRツールを使用してテーブルをバックアップおよび復元することによって、非クラスター化インデックスを持つテーブルをクラスター化インデックスを持つテーブルに変換することはできません。その逆も同様です。

### 他のTiDB機能との互換性 {#compatibility-with-other-tidb-features}

結合された主キーまたは単一の非整数主キーを持つテーブルの場合、主キーを非クラスター化インデックスからクラスター化インデックスに変更すると、その行データのキーも変更されます。したがって、v5.0より前のバージョンのTiDBで実行可能な`SPLIT TABLE BY/BETWEEN`のステートメントは、v5.0以降のバージョンのTiDBでは機能しなくなります。 `SPLIT TABLE BY/BETWEEN`を使用してクラスター化インデックスを使用してテーブルを分割する場合は、整数値を指定する代わりに、主キー列の値を指定する必要があります。次の例を参照してください。

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

属性[`AUTO_RANDOM`](/auto-random.md)は、クラスター化インデックスでのみ使用できます。それ以外の場合、TiDBは次のエラーを返します。

```sql
mysql> create table t (a bigint primary key nonclustered auto_random);
ERROR 8216 (HY000): Invalid auto random: column a is not the integer primary key, or the primary key is nonclustered
```
