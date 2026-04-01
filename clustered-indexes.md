---
title: Clustered Indexes
summary: クラスタ化インデックスの概念、ユーザーシナリオ、使用方法、制限事項、および互換性について学びます。
---

# クラスター化インデックス {#clustered-indexes}

TiDBはバージョン5.0以降、クラスタ化インデックス機能をサポートしています。この機能は、主キーを含むテーブルへのデータの格納方法を制御します。これにより、TiDBは特定のクエリのパフォーマンスを向上させるような方法でテーブルを整理することができます。

この文脈における*「クラスタ化」*という用語は*、データの格納方法の構成を*指し、*連携して動作するデータベースサーバーのグループを*指すものではありません。一部のデータベース管理システムでは、クラスタ化されたインデックステーブルを*インデックス構成テーブル*（IOT）と呼んでいます。

現在、TiDBの主キーを含むテーブルは、以下の2つのカテゴリに分類されます。

-   `NONCLUSTERED` : テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを持つテーブルでは、行データのキーは TiDB によって暗黙的に割り当てられる内部値[`_tidb_rowid`](/tidb-rowid.md)で構成されます。主キーは基本的に一意のインデックスであるため、非クラスター化インデックスを持つテーブルでは、行を格納するために少なくとも 2 つのキーと値のペアが必要です。それらは次のとおりです。
    -   `_tidb_rowid` （キー） - 行データ（値）
    -   主キーデータ（キー） - `_tidb_rowid` （値）
-   `CLUSTERED` ：テーブルの主キーはクラスタ化インデックスです。クラスタ化インデックスを持つテーブルでは、行データのキーはユーザーが指定した主キーデータで構成されます。したがって、クラスタ化インデックスを持つテーブルでは、行を格納するために必要なキーと値のペアは1つだけです。それは次のとおりです。
    -   主キーデータ（キー） - 行データ（値）

> **注記：**
>
> TiDB はテーブルの`PRIMARY KEY`によるクラスタリングのみをサポートしています。クラスタ化インデックスが有効になっている場合、 *5* `PRIMARY KEY`*クラスタ化インデックス*という用語は互換的に使用されることがあります。9 `PRIMARY KEY`制約 (論理プロパティ) を指し、クラスタ化インデックスはデータの格納方法の物理的な実装を説明します。

## ユーザーシナリオ {#user-scenarios}

クラスター化インデックスを持たないテーブルと比較して、クラスター化インデックスを持つテーブルは、以下のシナリオにおいて、より優れたパフォーマンスとスループットのメリットを提供します。

-   データが挿入される際、クラスタ化インデックスによって、ネットワークからのインデックスデータの書き込み回数が1回削減されます。
-   同等の条件を持つクエリが主キーのみに関係する場合、クラスタ化インデックスによってネットワークからのインデックスデータの読み取り回数が1回削減されます。
-   範囲条件を含むクエリが主キーのみに関係する場合、クラスタ化インデックスはネットワークからのインデックスデータの読み取り回数を削減します。
-   同等条件または範囲条件を含むクエリが主キーのプレフィックスのみに関係する場合、クラスタ化インデックスはネットワークからのインデックスデータの複数回の読み取りを削減します。

一方、クラスタ化インデックスを持つテーブルにはいくつかの欠点があります。以下をご覧ください。

-   値が近い多数の主キーを挿入する場合、書き込みホットスポットの問題が発生する可能性があります。
-   主キーのデータ型が64ビットより大きい場合、特にセカンダリインデックスが複数存在する場合は、テーブルデータがより多くのstorage容量を消費します。

## 使用例 {#usages}

### クラスター化インデックスを持つテーブルを作成する {#create-a-table-with-clustered-indexes}

TiDB v5.0以降では、 `CREATE TABLE`ステートメントの`PRIMARY KEY`の後に非予約語`CLUSTERED`または`NONCLUSTERED`を追加することで、テーブルの主キーがクラスタ化インデックスであるかどうかを指定できます。例：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) CLUSTERED);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
```

列定義において、キーワード`KEY`とキーワード`PRIMARY KEY`は同じ意味を持つことに注意してください。

TiDBの「 [コメント構文](/comment-syntax.md)を使用して、主キーのタイプを指定することもできます。例：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] NONCLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] CLUSTERED */);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] NONCLUSTERED */);
```

キーワード`CLUSTERED` / `NONCLUSTERED`を明示的に指定しないステートメントの場合、デフォルトの動作はシステム変数[`@@global.tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)によって制御されます。この変数でサポートされている値は次のとおりです。

-   `OFF` 、プライマリキーがデフォルトで非クラスター化インデックスとして作成されることを示します。
-   `ON` 、プライマリキーがデフォルトでクラスタ化インデックスとして作成されることを示します。
-   `INT_ONLY` 、動作が構成項目`alter-primary-key`によって制御されることを示します。4 `alter-primary-key` `true`に設定されている場合、プライマリキーはデフォルトで非クラスタ化インデックスとして作成されます。8 `false`設定されている場合、整数列で構成されるプライマリキーのみがクラスタ化インデックスとして作成されます。

デフォルト値`@@global.tidb_enable_clustered_index`は`ON`です。

### クラスター化インデックスの追加または削除 {#add-or-drop-clustered-indexes}

TiDB は、テーブル作成後にクラスタ化インデックスを追加または削除することをサポートしていません。また、クラスタ化インデックスと非クラスタ化インデックス間の相互変換もサポートしていません。例:

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) CLUSTERED; -- Currently not supported.
ALTER TABLE t DROP PRIMARY KEY;     -- If the primary key is a clustered index, then not supported.
ALTER TABLE t DROP INDEX `PRIMARY`; -- If the primary key is a clustered index, then not supported.
```

### 非クラスター化インデックスの追加または削除 {#add-or-drop-non-clustered-indexes}

TiDBは、テーブル作成後に非クラスター化インデックスを追加または削除することをサポートしています。キーワード`NONCLUSTERED`を明示的に指定することも、省略することもできます。例：

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) NONCLUSTERED;
ALTER TABLE t ADD PRIMARY KEY(b, a); -- If you omit the keyword, the primary key is a non-clustered index by default.
ALTER TABLE t DROP PRIMARY KEY;
ALTER TABLE t DROP INDEX `PRIMARY`;
```

### 主キーがクラスタ化インデックスであるかどうかを確認してください。 {#check-whether-the-primary-key-is-a-clustered-index}

テーブルの主キーがクラスタ化インデックスであるかどうかは、以下のいずれかの方法で確認できます。

-   コマンド`SHOW CREATE TABLE`を実行します。
-   コマンド`SHOW INDEX FROM`を実行します。
-   システムテーブル`information_schema.tables`の`TIDB_PK_TYPE`列目をクエリします。

コマンド`SHOW CREATE TABLE`を実行すると、 `PRIMARY KEY`の属性が`CLUSTERED`か`NONCLUSTERED`を確認できます。例：

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

コマンド`SHOW INDEX FROM`を実行すると、 `Clustered`列目の結果が`YES`か`NO`を確認できます。例：

```sql
mysql> SHOW INDEX FROM t;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| t     |          0 | PRIMARY  |            1 | a           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
1 row in set (0.01 sec)
```

システムテーブル`information_schema.tables`の列`TIDB_PK_TYPE`照会して、結果が`CLUSTERED`か`NONCLUSTERED`を確認することもできます。例：

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

現在、クラスタ化インデックス機能にはいくつかの異なる制限があります。以下を参照してください。

-   サポート対象外であり、サポートプランにも含まれていない状況：
    -   属性[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)とクラスター化インデックスを併用することはサポートされていません。また、属性[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 、クラスター化インデックスが[`AUTO_RANDOM`](/auto-random.md)でないテーブルには適用されません。
    -   クラスタ化インデックスを持つテーブルのダウングレードはサポートされていません。そのようなテーブルをダウングレードする必要がある場合は、代わりに論理バックアップツールを使用してデータを移行してください。
-   まだサポートされていないが、サポート計画に含まれている状況：
    -   `ALTER TABLE`ステートメントを使用してクラスタ化インデックスを追加、削除、変更することはサポートされていません。

属性`SHARD_ROW_ID_BITS`とクラスター化インデックスを併用すると、TiDB は次のエラーを報告します。

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED) SHARD_ROW_ID_BITS = 3;
ERROR 8200 (HY000): Unsupported shard_row_id_bits for table with primary key as row id
```

## 互換性 {#compatibility}

### 以前のバージョンおよび後のバージョンのTiDBとの互換性 {#compatibility-with-earlier-and-later-tidb-versions}

TiDBは、クラスタ化インデックスを持つテーブルのアップグレードはサポートしていますが、ダウングレードはサポートしていません。つまり、新しいバージョンのTiDBにあるクラスタ化インデックスを持つテーブルのデータは、古いバージョンでは利用できません。

クラスタ化インデックス機能は、TiDB v3.0およびv4.0で部分的にサポートされています。以下の要件がすべて満たされている場合、デフォルトで有効になります。

-   この表には`PRIMARY KEY`が含まれています。
-   `PRIMARY KEY` 1列のみで構成されています。
-   `PRIMARY KEY`は`INTEGER`です。

TiDB v5.0以降、クラスタ化インデックス機能はすべてのタイプの主キーで完全にサポートされていますが、デフォルトの動作はTiDB v3.0およびv4.0と一貫しています。デフォルトの動作を変更するには、システム変数`@@tidb_enable_clustered_index` ～ `ON`または`OFF`を設定します。詳細については、 [クラスター化インデックスを持つテーブルを作成する](#create-a-table-with-clustered-indexes)参照してください。

### MySQLとの互換性 {#compatibility-with-mysql}

TiDB固有のコメント構文では、キーワード`CLUSTERED`と`NONCLUSTERED`コメントで囲むことができます。また、 `SHOW CREATE TABLE`の結果にはTiDB固有のSQLコメントも含まれます。MySQLデータベースおよび以前のバージョンのTiDBデータベースでは、これらのコメントは無視されます。

### TiDB移行ツールとの互換性 {#compatibility-with-tidb-migration-tools}

クラスタ化インデックス機能は、v5.0以降のバージョンにおいて、以下の移行ツールとのみ互換性があります。

-   バックアップおよび復元ツール： BR、 Dumpling、 TiDB Lightning。
-   データ移行およびレプリケーションツール：DMとTiCDC。

ただし、v5.0 BRツールを使用してテーブルをバックアップおよび復元しても、非クラスター化インデックスを持つテーブルをクラスター化インデックスを持つテーブルに変換することはできません。また、その逆も同様です。

### 他のTiDB機能との互換性 {#compatibility-with-other-tidb-features}

結合主キーまたは単一の非整数主キーを持つテーブルの場合、主キーを非クラスタ化インデックスからクラスタ化インデックスに変更すると、行データのキーも変更されます。そのため、TiDB バージョン 5.0 より前のバージョンで実行可能だった`SPLIT TABLE BY/BETWEEN`ステートメントは、TiDB バージョン 5.0 以降のバージョンでは動作しなくなります。クラスタ化インデックスを持つテーブルを`SPLIT TABLE BY/BETWEEN`使用して分割する場合は、整数値を指定する代わりに、主キー列の値を指定する必要があります。次の例を参照してください。

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

属性[`AUTO_RANDOM`](/auto-random.md)クラスタ化インデックスでのみ使用できます。それ以外の場合、TiDBは次のエラーを返します。

```sql
mysql> create table t (a bigint primary key nonclustered auto_random);
ERROR 8216 (HY000): Invalid auto random: column a is not the integer primary key, or the primary key is nonclustered
```
