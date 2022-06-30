---
title: MySQL Compatibility
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
---

# MySQLの互換性 {#mysql-compatibility}

TiDBは、MySQL5.7プロトコルおよびMySQL5.7の一般的な機能と構文と高い互換性があります。 MySQL 5.7のエコシステムツール（PHPMyAdmin、Navicat、MySQL Workbench、mysqldump、およびMydumper / myloader）とMySQLクライアントをTiDBに使用できます。

ただし、MySQLの一部の機能はサポートされていません。これは、問題を解決するためのより良い方法（JSONに置き換えられたXML関数など）があるか、現在の需要と必要な労力（ストアドプロシージャや関数など）が不足していることが原因である可能性があります。一部の機能は、分散システムとして実装するのが難しい場合もあります。

-   さらに、TiDBはMySQLレプリケーションプロトコルをサポートしていませんが、MySQLでデータをレプリケートするための特定のツールを提供します。
    -   MySQLからのデータの複製： [TiDBデータ移行（DM）](/dm/dm-overview.md)は、MySQL/MariaDBからTiDBへの完全なデータ移行と増分データ複製をサポートするツールです。
    -   MySQLへのデータの複製： [TiCDC](/ticdc/ticdc-overview.md)は、TiKV変更ログをプルすることによってTiDBの増分データを複製するためのツールです。 TiCDCは[MySQLシンク](/ticdc/ticdc-overview.md#sink-support)を使用して、TiDBの増分データをMySQLに複製します。

> **ノート：**
>
> このページでは、MySQLとTiDBの一般的な違いについて説明します。 [安全](/security-compatibility-with-mysql.md)と[悲観的なトランザクションモード](/pessimistic-transaction.md#difference-with-mysql-innodb)の互換性については、専用ページを参照してください。

## サポートされていない機能 {#unsupported-features}

-   ストアドプロシージャと関数
-   トリガー
-   イベント
-   ユーザー定義関数
-   `FOREIGN KEY`制約[＃18209](https://github.com/pingcap/tidb/issues/18209)
-   `FULLTEXT`構文とインデックス[＃1793](https://github.com/pingcap/tidb/issues/1793)
-   `SPATIAL` （ `GIS`とも呼ばれ`GEOMETRY` ）関数、データ型、およびインデックス[＃6347](https://github.com/pingcap/tidb/issues/6347)
-   `ascii` 、 `binary` `latin1` `utf8`の`utf8mb4` `gbk` 。
-   SYSスキーマ
-   オプティマイザートレース
-   XML関数
-   Xプロトコル[＃1109](https://github.com/pingcap/tidb/issues/1109)
-   セーブポイント[＃6840](https://github.com/pingcap/tidb/issues/6840)
-   列レベルの特権[＃9766](https://github.com/pingcap/tidb/issues/9766)
-   `XA`構文（TiDBは内部で2フェーズコミットを使用しますが、これはSQLインターフェイスを介して公開されません）
-   `CREATE TABLE tblName AS SELECT stmt`構文[＃4754](https://github.com/pingcap/tidb/issues/4754)
-   `CHECK TABLE`構文[＃4673](https://github.com/pingcap/tidb/issues/4673)
-   `CHECKSUM TABLE`構文[＃1895](https://github.com/pingcap/tidb/issues/1895)
-   `REPAIR TABLE`構文
-   `OPTIMIZE TABLE`構文
-   `GET_LOCK`および`RELEASE_LOCK`関数[＃14994](https://github.com/pingcap/tidb/issues/14994)
-   [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)と`REPLACE`キーワード[＃24515](https://github.com/pingcap/tidb/issues/24515)
-   `HANDLER`ステートメント
-   `CREATE TABLESPACE`ステートメント

## MySQLとは異なる機能 {#features-that-are-different-from-mysql}

### 自動インクリメントID {#auto-increment-id}

-   TiDBでは、自動増分列はグローバルに一意です。これらは単一のTiDBサーバーではインクリメンタルですが、複数のTiDBサーバー間でインクリメンタルである必要*はなく*、順番に割り当てられる必要もありません。デフォルト値とカスタム値を混在させないことをお勧めします。そうしないと、 `Duplicated Error`のエラーメッセージが表示される場合があります。

-   `tidb_allow_remove_auto_inc`システム変数を使用して、 `AUTO_INCREMENT`列属性の削除を許可または禁止できます。列属性を削除する構文は`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`です。

-   TiDBは`AUTO_INCREMENT`列属性の追加をサポートしておらず、一度削除するとこの属性を回復することはできません。

-   詳細については、 [`AUTO_INCREMENT`](/auto-increment.md)を参照してください。

> **ノート：**
>
> -   テーブルの作成時に主キーを指定しなかった場合、TiDBは`_tidb_rowid`を使用して行を識別します。この値の割り当ては、自動インクリメント列とアロケータを共有します（そのような列が存在する場合）。主キーとして自動インクリメント列を指定すると、TiDBはこの列を使用して行を識別します。この状況では、次の状況が発生する可能性があります。

```sql
mysql> CREATE TABLE t(id INT UNIQUE KEY AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> INSERT INTO t VALUES(),(),();
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT _tidb_rowid, id FROM t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           4 |    1 |
|           5 |    2 |
|           6 |    3 |
+-------------+------+
3 rows in set (0.01 sec)
```

> **ノート：**
>
> `AUTO_INCREMENT`属性は、実稼働環境でホットスポットを引き起こす可能性があります。詳細については、 [HotSpotの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)を使用することをお勧めします。

### パフォーマンススキーマ {#performance-schema}

TiDBは、 [プロメテウスとグラファナ](/tidb-monitoring-api.md)の組み合わせを使用して、パフォーマンス監視メトリックを格納および照会します。パフォーマンススキーマテーブルは、TiDBに空の結果を返します。

### クエリ実行プラン {#query-execution-plan}

`EXPLAIN FOR`のクエリ実行プラン（ `EXPLAIN` ）の出力形式、出力内容、および特権設定は、MySQLのものとは大きく異なります。

MySQLシステム変数`optimizer_switch`はTiDBでは読み取り専用であり、クエリプランには影響しません。 MySQLと同様の構文で[オプティマイザーのヒント](/optimizer-hints.md)を使用することもできますが、使用可能なヒントと実装が異なる場合があります。

詳細については、 [クエリ実行プランを理解する](/explain-overview.md)を参照してください。

### 内蔵機能 {#built-in-functions}

TiDBは、MySQLの組み込み関数のほとんどをサポートしていますが、すべてをサポートしているわけではありません。ステートメント`SHOW BUILTINS`は、使用可能な関数のリストを提供します。

参照： [TiDBSQL文法](https://pingcap.github.io/sqlgram/#functioncallkeyword) 。

### DDL {#ddl}

TiDBでは、サポートされているすべてのDDL変更はオンラインで実行されます。 MySQLのDDL操作と比較して、TiDBのDDL操作には次の主要な制限があります。

-   `ALTER TABLE`のステートメントで複数の操作を完了することはできません。たとえば、1つのステートメントに複数の列またはインデックスを追加することはできません。そうしないと、 `Unsupported multi schema change`エラーが出力される可能性があります。
-   TiDBの`ALTER TABLE`は、一部のデータ型の変更をサポートしていません。たとえば、TiDBは`DECIMAL`タイプから`DATE`タイプへの変更をサポートしていません。データ型の変更がサポートされていない場合、TiDBは`Unsupported modify column: type %d not match origin %d`エラーを報告します。詳細については、 [`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)を参照してください。
-   `ALGORITHM={INSTANT,INPLACE,COPY}`構文は、TiDBのアサーションとしてのみ機能し、 `ALTER`アルゴリズムを変更しません。詳細については、 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)を参照してください。
-   `CLUSTERED`タイプの主キーの追加/削除はサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化されたインデックス](/clustered-indexes.md)を参照してください。
-   さまざまなタイプのインデックス（ `HASH|BTREE|RTREE|FULLTEXT` ）はサポートされておらず、指定すると解析されて無視されます。
-   テーブルパーティショニングは、 `HASH` 、および`RANGE`のパーティショニングタイプをサポートし`LIST` 。サポートされていないパーティションタイプの場合、 `Warning: Unsupported partition type %s, treat as normal table`エラーが出力されることがあります`%s`は特定のパーティションタイプです。
-   テーブルパーティショニングは、 `ADD` 、および`DROP`の操作もサポートし`TRUNCATE` 。他のパーティション操作は無視されます。次のテーブルパーティション構文はサポートされていません。

    -   `PARTITION BY KEY`
    -   `SUBPARTITION`
    -   `{CHECK|TRUNCATE|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD|REORGANIZE|COALESCE} PARTITION`

    詳細については、 [パーティショニング](/partitioned-table.md)を参照してください。

### テーブルを分析する {#analyze-table}

[統計収集](/statistics.md#manual-collection)は、MySQLとMySQLでの動作が異なります。つまり、MySQL / InnoDBでは比較的軽量で短期間の操作ですが、TiDBではテーブルの統計を完全に再構築し、完了するまでにはるかに長い時間がかかる可能性があります。

これらの違いについては、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)で詳しく説明しています。

### <code>SELECT</code>構文の制限 {#limitations-of-code-select-code-syntax}

-   構文`SELECT ... INTO @variable`はサポートされていません。
-   構文`SELECT ... GROUP BY ... WITH ROLLUP`はサポートされていません。
-   構文`SELECT .. GROUP BY expr`は、MySQL5.7のように`GROUP BY expr ORDER BY expr`を意味しません。

詳細については、 [`SELECT`](/sql-statements/sql-statement-select.md)ステートメントのリファレンスを参照してください。

### <code>UPDATE</code>ステートメント {#code-update-code-statement}

[`UPDATE`](/sql-statements/sql-statement-update.md)ステートメントのリファレンスを参照してください。

### ビュー {#views}

TiDBのビューは更新できません。 `UPDATE`などの`INSERT`操作はサポートして`DELETE`ません。

### 一時テーブル {#temporary-tables}

詳細については、 [TiDBローカル一時テーブルとMySQL一時テーブル間の互換性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)を参照してください。

### 文字セットと照合 {#character-sets-and-collations}

-   TiDBでサポートされている文字セットと照合の詳細については、 [文字セットと照合の概要](/character-set-and-collation.md)を参照してください。

-   GBK文字セットのMySQL互換性については、 [GBKの互換性](/character-set-gbk.md#mysql-compatibility)を参照してください。

### ストレージエンジン {#storage-engines}

互換性の理由から、TiDBは代替ストレージエンジンでテーブルを作成する構文をサポートしています。実装では、TiDBはメタデータをInnoDBストレージエンジンとして記述します。

TiDBはMySQLと同様のストレージエンジンの抽象化をサポートしていますが、TiDBサーバーを起動するときに[`--store`](/command-line-flags-for-tidb-configuration.md#--store)オプションを使用してストレージエンジンを指定する必要があります。

### SQLモード {#sql-modes}

TiDBはほとんどの[SQLモード](/sql-mode.md)をサポートします：

-   `Oracle`や`PostgreSQL`などの互換モードは解析されますが、無視されます。互換モードはMySQL5.7で非推奨になり、MySQL8.0で削除されました。
-   `ONLY_FULL_GROUP_BY`モードには、MySQL5.7のマイナー[意味の違い](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql)があります。
-   MySQLの`NO_DIR_IN_CREATE`および`NO_ENGINE_SUBSTITUTION`モードは互換性のために受け入れられていますが、TiDBには適用されません。

### デフォルトの違い {#default-differences}

-   デフォルトの文字セット：
    -   TiDBのデフォルト値は`utf8mb4`です。
    -   MySQL5.7のデフォルト値は`latin1`です。
    -   MySQL8.0のデフォルト値は`utf8mb4`です。
-   デフォルトの照合順序：
    -   TiDBのデフォルトの`utf8mb4`の照合順序は`utf8mb4_bin`です。
    -   MySQL5.7の`utf8mb4`のデフォルトの照合順序は`utf8mb4_general_ci`です。
    -   MySQL8.0のデフォルトの`utf8mb4`の照合順序は`utf8mb4_0900_ai_ci`です。
-   デフォルト値`foreign_key_checks` ：
    -   TiDBのデフォルト値は`OFF`で、現在TiDBは`OFF`のみをサポートしています。
    -   MySQL5.7のデフォルト値は`ON`です。
-   デフォルトのSQLモード：
    -   TiDBのデフォルトのSQLモードには、次のモードが含まれ`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION` 。
    -   MySQLのデフォルトのSQLモード：
        -   MySQL5.7のデフォルトのSQLモードはTiDBと同じです。
        -   MySQL 8.0のデフォルトのSQLモードには、次のモードが含まれてい`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION` 。
-   デフォルト値`lower_case_table_names` ：
    -   TiDBのデフォルト値は`2`で、現在TiDBは`2`のみをサポートしています。
    -   MySQLのデフォルト値：
        -   Linuxの場合： `0`
        -   Windowsの場合： `1`
        -   macOSの場合： `2`
-   デフォルト値`explicit_defaults_for_timestamp` ：
    -   TiDBのデフォルト値は`ON`で、現在TiDBは`ON`のみをサポートしています。
    -   MySQLのデフォルト値：
        -   MySQL 5.7の場合： `OFF` 。
        -   MySQL 8.0の場合： `ON` 。

### 日時 {#date-and-time}

#### 名前付きタイムゾーン {#named-timezone}

-   TiDBは、現在システムにインストールされているすべてのタイムゾーンルールを計算に使用します（通常は`tzdata`のパッケージ）。タイムゾーンテーブルデータをインポートせずに、すべてのタイムゾーン名を使用できます。タイムゾーンテーブルデータをインポートして計算ルールを変更することはできません。
-   MySQLはデフォルトでローカルタイムゾーンを使用し、計算のためにシステムに組み込まれている現在のタイムゾーンルール（夏時間を開始するタイミングなど）に依存します。また、タイムゾーンは[タイムゾーンテーブルデータのインポート](https://dev.mysql.com/doc/refman/5.7/en/time-zone-support.html#time-zone-installation)なしのタイムゾーン名で指定することはできません。

### 型システムの違い {#type-system-differences}

次の列タイプはMySQLでサポートされていますが、TiDBではサポートされてい**ません**。

-   FLOAT4 / FLOAT8
-   `SQL_TSI_*` （SQL_TSI_MONTH、SQL_TSI_WEEK、SQL_TSI_DAY、SQL_TSI_HOUR、SQL_TSI_MINUTE、およびSQL_TSI_SECONDを含み、SQL_TSI_YEARを除く）

### 非推奨の機能によって引き起こされる非互換性 {#incompatibility-caused-by-deprecated-features}

TiDBは、MySQLで非推奨としてマークされている特定の機能を実装していません。

-   浮動小数点型の精度を指定します。 MySQL 8.0 [非推奨](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)この機能であり、代わりに`DECIMAL`タイプを使用することをお勧めします。
-   `ZEROFILL`属性。 MySQL 8.0 [非推奨](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html)この機能。代わりに、アプリケーションに数値を埋め込むことをお勧めします。
