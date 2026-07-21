---
title: Clustered Indexes
summary: クラスター化インデックスの概念、ユーザーシナリオ、使用方法、制限事項、および互換性について学びます。
---

# クラスター化インデックス {#clustered-indexes}

TiDBはバージョン5.0以降、クラスター化インデックス機能をサポートしています。この機能は、主キーを含むテーブルへのデータの格納方法を制御します。これにより、TiDBは特定のクエリのパフォーマンスを向上させるような方法でテーブルを整理することができます。

この文脈における*「クラスター化」*という用語は*、データの格納方法の構成を*指し、*連携して動作するデータベースサーバーのグループを*指すものではありません。一部のデータベース管理システムでは、クラスター化されたインデックステーブルを*インデックス構成テーブル*（IOT）と呼んでいます。

現在、TiDBの主キーを含むテーブルは、以下の2つのカテゴリに分類されます。

-   `NONCLUSTERED` : テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを持つテーブルでは、行データのキーは、TiDB によって暗黙的に割り当てられる内部の[`_tidb_rowid`](/tidb-rowid.md)値で構成されます。主キーは基本的に一意インデックスであるため、非クラスター化インデックスを持つテーブルでは、行を格納するために少なくとも 2 つのキーと値のペアが必要です。それらは次のとおりです。
    -   `_tidb_rowid` （キー） - 行データ（値）
    -   主キーデータ（キー） - `_tidb_rowid` （値）
-   `CLUSTERED` : テーブルの主キーはクラスター化インデックスです。クラスター化インデックスを持つテーブルでは、行データのキーはユーザーが指定した主キーデータで構成されます。したがって、クラスター化インデックスを持つテーブルでは、行を格納するために必要なキーと値のペアは1つだけです。それは次のとおりです。
    -   主キーデータ（キー） - 行データ（値）

> **Note:**
>
> TiDB は、テーブルの`PRIMARY KEY`によるクラスタリングのみをサポートしています。クラスター化インデックスが有効になっている場合、 *{* `PRIMARY KEY`と*クラスター化インデックス*という用語は同じ意味で使用されることがあります。 `PRIMARY KEY`は制約 (論理プロパティ) を指し、クラスター化インデックスはデータの格納方法の物理的な実装を表します。

## ユーザーシナリオ {#user-scenarios}

クラスター化インデックスを持たないテーブルと比較して、クラスター化インデックスを持つテーブルは、以下のシナリオにおいて、より優れたパフォーマンスとスループットのメリットを提供します。

-   データが挿入される際、クラスター化インデックスによって、ネットワークからのインデックスデータの書き込み回数が1回削減されます。
-   同等の条件を持つクエリが主キーのみに関係する場合、クラスター化インデックスによってネットワークからのインデックスデータの読み取り回数が1回削減されます。
-   範囲条件を含むクエリが主キーのみに関係する場合、クラスター化インデックスはネットワークからのインデックスデータの読み取り回数を削減します。
-   同等条件または範囲条件を含むクエリが主キーのプレフィックスのみに関係する場合、クラスター化インデックスはネットワークからのインデックスデータの複数回の読み取りを削減します。

一方、クラスター化インデックスを持つテーブルにはいくつかの欠点があります。以下をご覧ください。

-   値が近い多数の主キーを挿入する場合、書き込みホットスポットの問題が発生する可能性があります。
-   主キーのデータ型が64ビットより大きい場合、特にセカンダリインデックスが複数存在する場合は、テーブルデータがより多くのストレージ容量を消費します。

## 使用例 {#usages}

### クラスター化インデックスを持つテーブルを作成する {#create-a-table-with-clustered-indexes}

TiDB v5.0以降では、 `CLUSTERED`の`NONCLUSTERED`の後に、予約語ではないキーワード`PRIMARY KEY`または`CREATE TABLE`を追加することで、テーブルの主キーがクラスター化インデックスであるかどうかを指定できます。例：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY CLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT KEY NONCLUSTERED, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) CLUSTERED);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) NONCLUSTERED);
```

列定義において、キーワード`KEY`と`PRIMARY KEY`は同じ意味を持つことに注意してください。

TiDB の[コメント構文](/comment-syntax.md)使用して主キーのタイプを指定することもできます。例えば：

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] CLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT PRIMARY KEY /*T![clustered_index] NONCLUSTERED */, b VARCHAR(255));
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] CLUSTERED */);
CREATE TABLE t (a BIGINT, b VARCHAR(255), PRIMARY KEY(a, b) /*T![clustered_index] NONCLUSTERED */);
```

キーワード`CLUSTERED` / `NONCLUSTERED`明示的に指定しないステートメントの場合、デフォルトの動作はシステム変数[`@@global.tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)によって制御されます。この変数でサポートされている値は次のとおりです。

-   `OFF`は、主キーがデフォルトで非クラスター化インデックスとして作成されることを示します。
-   `ON`は、主キーがデフォルトでクラスター化インデックスとして作成されることを示します。
-   `INT_ONLY`は、動作が構成項目`alter-primary-key`によって制御されることを示します。 `alter-primary-key`が`true`に設定されている場合、プライマリ キーはデフォルトで非クラスター化インデックスとして作成されます。 `false`に設定されている場合、整数列で構成されるプライマリ キーのみがクラスター化インデックスとして作成されます。

`@@global.tidb_enable_clustered_index`のデフォルト値は`ON`です。

### クラスター化インデックスの追加または削除 {#add-or-drop-clustered-indexes}

TiDB は、テーブル作成後にクラスター化インデックスを追加または削除することをサポートしていません。また、クラスター化インデックスと非クラスター化インデックス間の相互変換もサポートしていません。例:

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) CLUSTERED; -- Currently not supported.
ALTER TABLE t DROP PRIMARY KEY;     -- If the primary key is a clustered index, then not supported.
ALTER TABLE t DROP INDEX `PRIMARY`; -- If the primary key is a clustered index, then not supported.
```

### 非クラスター化インデックスの追加または削除 {#add-or-drop-non-clustered-indexes}

TiDB は、テーブル作成後に非クラスター化インデックスを追加または削除することをサポートしています。キーワード`NONCLUSTERED`を明示的に指定することも、省略することもできます。例:

```sql
ALTER TABLE t ADD PRIMARY KEY(b, a) NONCLUSTERED;
ALTER TABLE t ADD PRIMARY KEY(b, a); -- If you omit the keyword, the primary key is a non-clustered index by default.
ALTER TABLE t DROP PRIMARY KEY;
ALTER TABLE t DROP INDEX `PRIMARY`;
```

### 主キーがクラスター化インデックスであるかどうかを確認してください。 {#check-whether-the-primary-key-is-a-clustered-index}

テーブルの主キーがクラスター化インデックスであるかどうかは、以下のいずれかの方法で確認できます。

-   コマンド`SHOW CREATE TABLE`を実行します。
-   コマンド`SHOW INDEX FROM`を実行します。
-   システムテーブル`TIDB_PK_TYPE`の`information_schema.tables`列をクエリします。

コマンド`SHOW CREATE TABLE`を実行すると、 `PRIMARY KEY`の属性が`CLUSTERED`か`NONCLUSTERED`かを確認できます。例:

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

コマンド`SHOW INDEX FROM`を実行すると、列`Clustered`の結果が`YES`または`NO`のどちらを表示しているかを確認できます。例:

```sql
mysql> SHOW INDEX FROM t;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| t     |          0 | PRIMARY  |            1 | a           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
1 row in set (0.01 sec)
```

システムテーブル`TIDB_PK_TYPE`の列`information_schema.tables`をクエリして、結果が`CLUSTERED`か`NONCLUSTERED`かを確認することもできます。例:

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

現在、クラスター化インデックス機能にはいくつかの異なる制限があります。以下を参照してください。

-   サポート対象外であり、サポートプランにも含まれていない状況：
    -   クラスター化インデックスと属性[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を併用することはサポートされていません。また、属性[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) [`AUTO_RANDOM`](/auto-random.md)ではないクラスター化インデックスを持つテーブルには適用されません。
    -   クラスター化インデックスを持つテーブルのダウングレードはサポートされていません。そのようなテーブルをダウングレードする必要がある場合は、代わりに論理バックアップツールを使用してデータを移行してください。
-   まだサポートされていないが、サポート計画に含まれている状況：
    -   `ALTER TABLE`ステートメントを使用したクラスター化インデックスの追加、削除、および変更はサポートされていません。

クラスター化インデックスを属性`SHARD_ROW_ID_BITS`と一緒に使用すると、TiDB は次のエラーを報告します。

```sql
mysql> CREATE TABLE t (a VARCHAR(255) PRIMARY KEY CLUSTERED) SHARD_ROW_ID_BITS = 3;
ERROR 8200 (HY000): Unsupported shard_row_id_bits for table with primary key as row id
```

## 互換性 {#compatibility}

### 以前のバージョンおよび後のバージョンのTiDBとの互換性 {#compatibility-with-earlier-and-later-tidb-versions}

TiDBは、クラスター化インデックスを持つテーブルのアップグレードはサポートしていますが、ダウングレードはサポートしていません。つまり、新しいバージョンのTiDBにあるクラスター化インデックスを持つテーブルのデータは、古いバージョンでは利用できません。

クラスター化インデックス機能は、TiDB v3.0およびv4.0で部分的にサポートされています。以下の要件がすべて満たされている場合、デフォルトで有効になります。

-   テーブルには`PRIMARY KEY`が含まれています。
-   `PRIMARY KEY`は 1 つの列のみで構成されています。
-   `PRIMARY KEY`は`INTEGER`です。

TiDB v5.0 以降、クラスター化インデックス機能はすべてのタイプの主キーに対して完全にサポートされていますが、デフォルトの動作は TiDB v3.0 および v4.0 と一貫しています。デフォルトの動作を変更するには、システム変数`@@tidb_enable_clustered_index`を`ON`または`OFF`に設定します。詳細については、[クラスター化インデックスを持つテーブルを作成する](#create-a-table-with-clustered-indexes)を参照してください。

### MySQLとの互換性 {#compatibility-with-mysql}

TiDB固有のコメント構文では、キーワード`CLUSTERED`と`NONCLUSTERED`をコメントで囲むことができます。 `SHOW CREATE TABLE`の結果にも、TiDB固有のSQLコメントが含まれます。MySQLデータベースおよび以前のバージョンのTiDBデータベースでは、これらのコメントは無視されます。

### TiDB移行ツールとの互換性 {#compatibility-with-tidb-migration-tools}

クラスター化インデックス機能は、v5.0以降のバージョンにおいて、以下の移行ツールとのみ互換性があります。

-   バックアップおよび復元ツール： BR、 Dumpling、 TiDB Lightning。
-   データ移行およびレプリケーションツール：DMとTiCDC。

ただし、v5.0 BRツールを使用してテーブルをバックアップおよび復元しても、非クラスター化インデックスを持つテーブルをクラスター化インデックスを持つテーブルに変換することはできません。また、その逆も同様です。

### 他のTiDB機能との互換性 {#compatibility-with-other-tidb-features}

結合主キーまたは単一の非整数主キーを持つテーブルの場合、主キーを非クラスター化インデックスからクラスター化インデックスに変更すると、行データのキーも変更されます。そのため、TiDB バージョン 5.0 より前のバージョンで実行可能だった`SPLIT TABLE BY/BETWEEN`ステートメントは、TiDB バージョン 5.0 以降では動作しなくなります。 `SPLIT TABLE BY/BETWEEN`を使用してクラスター化インデックスを持つテーブルを分割する場合は、整数値を指定する代わりに、主キー列の値を指定する必要があります。次の例を参照してください。

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

[`AUTO_RANDOM`](/auto-random.md)属性は、クラスター化インデックスでのみ使用できます。それ以外の場合、TiDBは次のエラーを返します。

```sql
mysql> create table t (a bigint primary key nonclustered auto_random);
ERROR 8216 (HY000): Invalid auto random: column a is not the integer primary key, or the primary key is nonclustered
```

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="TiDB SQL Tuning Lab 1: Clustered and Non-Clustered Indexes" type="lab" link="https://labs.tidb.io/labs/dba_307_lab_ff0" imgSrc="https://lab-static.pingcap.com/quick-demo/307-01.png" duration="90 mins" />
</RelatedResources>
