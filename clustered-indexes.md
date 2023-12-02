---
title: Clustered Indexes
summary: Learn the concept, user scenarios, usages, limitations, and compatibility of clustered indexes.
---

# クラスター化インデックス {#clustered-indexes}

TiDB は v5.0 以降、クラスター化インデックス機能をサポートしています。この機能は、主キーを含むテーブルにデータを格納する方法を制御します。これにより、特定のクエリのパフォーマンスを向上できる方法でテーブルを編成する機能が TiDB に提供されます。

この文脈での*「クラスタ化」*という用語は*、連携して動作するデータベース サーバーのグループ*ではなく、*データの保存方法の構成*を指します。一部のデータベース管理システムでは、クラスター化インデックスを*インデックス構成テーブル*(IOT) と呼びます。

現在、TiDB の主キーを含むテーブルは次の 2 つのカテゴリに分類されています。

-   `NONCLUSTERED` : テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを備えたテーブルでは、行データのキーは TiDB によって暗黙的に割り当てられた内部`_tidb_rowid`で構成されます。主キーは本質的に一意のインデックスであるため、非クラスター化インデックスを持つテーブルでは、行を格納するために少なくとも 2 つのキーと値のペアが必要です。
    -   `_tidb_rowid` (キー) - 行データ (値)
    -   主キーデータ（キー） - `_tidb_rowid` （値）
-   `CLUSTERED` : テーブルの主キーはクラスター化インデックスです。クラスター化インデックスを備えたテーブルでは、行データのキーはユーザーが指定した主キー データで構成されます。したがって、クラスター化インデックスを備えたテーブルでは、行を格納するために次のキーと値のペアが 1 つだけ必要になります。
    -   主キーデータ(key) - 行データ(value)

> **注記：**
>
> TiDB は、テーブルの`PRIMARY KEY`によるクラスタリングのみをサポートします。クラスター化インデックスが有効になっている場合、 *5*と*クラスター化インデックス*`PRIMARY KEY`用語は同じ意味で使用される場合があります。 `PRIMARY KEY`は制約 (論理プロパティ) を指し、クラスター化インデックスはデータの格納方法の物理的な実装を示します。

## ユーザーシナリオ {#user-scenarios}

非クラスター化インデックスを含むテーブルと比較して、クラスター化インデックスを含むテーブルは、次のシナリオでパフォーマンスとスループットの利点が大きくなります。

-   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
-   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
-   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
-   同等条件または範囲条件を含むクエリに主キー プレフィックスのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。

一方、クラスター化インデックスを備えたテーブルにはいくつかの欠点があります。以下を参照してください。

-   近い値を持つ多数の主キーを挿入すると、書き込みホットスポットの問題が発生する可能性があります。
-   主キーのデータ型が 64 ビットより大きい場合、特に複数のセカンダリ インデックスがある場合、テーブル データはより多くのstorage領域を占有します。

## 用途 {#usages}

## クラスター化インデックスを含むテーブルを作成する {#create-a-table-with-clustered-indexes}

TiDB v5.0 以降、 `CREATE TABLE`ステートメントの`PRIMARY KEY`の後に非予約キーワード`CLUSTERED`または`NONCLUSTERED`を追加して、テーブルの主キーがクラスター化インデックスであるかどうかを指定できます。例えば：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) CLUSTERED);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
```

キーワード`KEY`と`PRIMARY KEY`は列定義では同じ意味を持ちます。

TiDB の[コメント構文](/comment-syntax.md)使用して主キーのタイプを指定することもできます。例えば：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] NONCLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] CLUSTERED */);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] NONCLUSTERED */);
```

キーワード`CLUSTERED` `NONCLUSTERED`明示的に指定していないステートメントの場合、デフォルトの動作はシステム変数[`@@global.tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)によって制御されます。この変数でサポートされている値は次のとおりです。

-   `OFF` 、主キーがデフォルトで非クラスター化インデックスとして作成されることを示します。
-   `ON` 、主キーがデフォルトでクラスター化インデックスとして作成されることを示します。
-   `INT_ONLY` 、動作が構成項目`alter-primary-key`によって制御されることを示します。 `alter-primary-key`が`true`に設定されている場合、主キーはデフォルトで非クラスター化インデックスとして作成されます。 `false`に設定すると、整数列で構成される主キーのみがクラスター化インデックスとして作成されます。

デフォルト値の`@@global.tidb_enable_clustered_index`は`ON`です。

### クラスター化インデックスの追加または削除 {#add-or-drop-clustered-indexes}

TiDB は、テーブルの作成後のクラスター化インデックスの追加または削除をサポートしていません。また、クラスター化インデックスと非クラスター化インデックス間の相互変換もサポートしません。例えば：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) CLUSTERED; -- Currently not supported.
ALTER TABLE t DROP PRIMARY KEY;     -- If the primary key is a clustered index, then not supported.
ALTER TABLE t DROP INDEX `PRIMARY`; -- If the primary key is a clustered index, then not supported.
```

### 非クラスター化インデックスの追加または削除 {#add-or-drop-non-clustered-indexes}

TiDB は、テーブルの作成後の非クラスター化インデックスの追加または削除をサポートします。キーワード`NONCLUSTERED`明示的に指定することも、省略することもできます。例えば：

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

コマンド`SHOW CREATE TABLE`を実行すると、 `PRIMARY KEY`の属性が`CLUSTERED`か`NONCLUSTERED`かを確認できます。例えば：

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

コマンド`SHOW INDEX FROM`を実行すると、列`Clustered`の結果が`YES`または`NO`を示すかどうかを確認できます。例えば：

```sql
mysql> SHOW INDEX FROM t;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| t     |          0 | PRIMARY  |            1 | a           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
1 row in set (0.01 sec)
```

システム テーブル`information_schema.tables`の列`TIDB_PK_TYPE`クエリして、結果が`CLUSTERED`か`NONCLUSTERED`かを確認することもできます。例えば：

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

現在、クラスター化インデックス機能にはいくつかの異なる種類の制限があります。以下を参照してください。

-   サポートされていない、またはサポート プランに含まれていない状況:
    -   クラスター化インデックスと属性[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)の併用はサポートされていません。また、属性[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 、クラスター化インデックスのあるテーブルには効果がありません。
    -   クラスター化インデックスを含むテーブルのダウングレードはサポートされていません。このようなテーブルをダウングレードする必要がある場合は、代わりに論理バックアップ ツールを使用してデータを移行してください。
-   まだサポートされていないがサポート計画に含まれている状況:
    -   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。
-   特定のバージョンの制限:
    -   v5.0 では、クラスター化インデックス機能と TiDB Binlogの併用はサポートされていません。 TiDB Binlogが有効になった後、TiDB では主キーのクラスター化インデックスとして単一の整数列の作成のみが許可されます。 TiDB Binlog は、クラスター化インデックスを持つ既存のテーブルのデータ変更 (挿入、削除、更新など) をダウンストリームに複製しません。クラスター化インデックスを含むテーブルをダウンストリームにレプリケートする必要がある場合は、クラスターを v5.1 にアップグレードするか、代わりにレプリケーションに[TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)を使用してください。

TiDB Binlogを有効にした後、作成したクラスター化インデックスが単一の整数主キーではない場合、TiDB は次のエラーを返します。

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED);
ERROR 8200 (HY000): Cannot create clustered index table when the binlog is ON
```

クラスター化インデックスを属性`SHARD_ROW_ID_BITS`とともに使用すると、TiDB は次のエラーを報告します。

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED) SHARD_ROW_ID_BITS = 3;
ERROR 8200 (HY000): Unsupported shard_row_id_bits for table with primary key as row id
```

## 互換性 {#compatibility}

### 以前および以降の TiDB バージョンとの互換性 {#compatibility-with-earlier-and-later-tidb-versions}

TiDB は、クラスター化インデックスを備えたテーブルのアップグレードをサポートしますが、そのようなテーブルのダウングレードはサポートしません。つまり、新しい TiDB バージョンのクラスター化インデックスを備えたテーブルのデータは、以前の TiDB バージョンでは使用できません。

クラスター化インデックス機能は、TiDB v3.0 および v4.0 で部分的にサポートされています。次の要件が完全に満たされている場合、デフォルトで有効になります。

-   テーブルには`PRIMARY KEY`含まれています。
-   `PRIMARY KEY`は 1 つの列のみで構成されます。
-   `PRIMARY KEY`は`INTEGER`です。

TiDB v5.0 以降、クラスター化インデックス機能はすべてのタイプの主キーに対して完全にサポートされていますが、デフォルトの動作は TiDB v3.0 および v4.0 と一貫しています。デフォルトの動作を変更するには、システム変数`@@tidb_enable_clustered_index` ～ `ON`または`OFF`を構成します。詳細については、 [クラスター化インデックスを含むテーブルを作成する](#create-a-table-with-clustered-indexes)を参照してください。

### MySQLとの互換性 {#compatibility-with-mysql}

TiDB 固有のコメント構文は、コメント内でキーワード`CLUSTERED`と`NONCLUSTERED`をラップすることをサポートしています。 `SHOW CREATE TABLE`の結果には、TiDB 固有の SQL コメントも含まれています。以前のバージョンの MySQL データベースと TiDB データベースは、これらのコメントを無視します。

### TiDB 移行ツールとの互換性 {#compatibility-with-tidb-migration-tools}

クラスター化インデックス機能は、v5.0 以降のバージョンの次の移行ツールとのみ互換性があります。

-   バックアップおよび復元ツール: BR、 Dumpling、およびTiDB Lightning。
-   データ移行およびレプリケーション ツール: DM および TiCDC。

ただし、v5.0 BRツールを使用してテーブルをバックアップおよび復元することによって、非クラスター化インデックスを含むテーブルをクラスター化インデックスを含むテーブルに変換することはできません (その逆の場合も同様)。

### 他の TiDB 機能との互換性 {#compatibility-with-other-tidb-features}

結合主キーまたは単一の非整数主キーを持つテーブルの場合、主キーを非クラスター化インデックスからクラスター化インデックスに変更すると、その行データのキーも変更されます。したがって、v5.0 より前の TiDB バージョンで実行可能な`SPLIT TABLE BY/BETWEEN`ステートメントは、v5.0 以降の TiDB バージョンでは機能しなくなります。 `SPLIT TABLE BY/BETWEEN`を使用してクラスター化インデックスを含むテーブルを分割する場合は、整数値を指定するのではなく、主キー列の値を指定する必要があります。次の例を参照してください。

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

属性[`AUTO_RANDOM`](/auto-random.md)クラスター化インデックスでのみ使用できます。それ以外の場合、TiDB は次のエラーを返します。

```sql
mysql> create table t (a bigint primary key nonclustered auto_random);
ERROR 8216 (HY000): Invalid auto random: column a is not the integer primary key, or the primary key is nonclustered
```
