---
title: MySQL Compatibility
summary: TiDBとMySQLの互換性、およびサポートされていない機能や異なる機能について学びましょう。
---

# MySQLとの互換性 {#mysql-compatibility}

<CustomContent platform="tidb">

TiDBはMySQLプロトコルと高い互換性を持ち、 MySQL 5.7およびMySQL 8.0の共通機能と構文に対応しています。MySQLのエコシステムツール（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver [もっと](/develop/dev-guide-third-party-support.md#gui)）およびMySQLクライアントはTiDBで使用できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDBはMySQLプロトコルと高い互換性を持ち、 MySQL 5.7およびMySQL 8.0の共通機能と構文に対応しています。MySQLのエコシステムツール（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver [もっと](https://docs.pingcap.com/tidb/stable/dev-guide-third-party-support#gui)）およびMySQLクライアントはTiDBで使用できます。

</CustomContent>

ただし、TiDBではMySQLの一部の機能はサポートされていません。これは、問題を解決するより良い方法（XML関数の代わりにJSONを使用するなど）が存在するため、または必要な労力に対して現在の需要が不足しているため（ストアドプロシージャや関数など）と考えられます。さらに、一部の機能は分散システムでの実装が難しい場合もあります。

<CustomContent platform="tidb">

TiDBはMySQLレプリケーションプロトコルをサポートしていない点に注意が必要です。代わりに、MySQLでデータをレプリケートするための専用ツールが提供されています。

-   MySQL からデータを複製する: [TiDBデータ移行（DM）](/dm/dm-overview.md)は、MySQL または MariaDB から TiDB への完全なデータ移行と増分データレプリケーションをサポートするツールです。
-   データをMySQLに複製する: [TiCDC](/ticdc/ticdc-overview.md)は、TiKV変更ログを取得してTiDBの増分データを複製するためのツールです。TiCDCは[MySQLシンク](/ticdc/ticdc-overview.md#replication-consistency)を使用して、TiDBの増分データをMySQLに複製します。

</CustomContent>

<CustomContent platform="tidb">

> **注記：**
>
> このページでは、MySQL と TiDB の一般的な違いについて説明します。セキュリティ分野における MySQL との互換性の詳細については、 [MySQLとのSecurity互換性](/security-compatibility-with-mysql.md)を参照してください。

</CustomContent>

[TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=mysql_compatibility)でTiDBの機能を試すことができます。

## サポートされていない機能 {#unsupported-features}

-   ストアドプロシージャと関数

-   トリガー

-   イベント

-   ユーザー定義関数

-   `FULLTEXT`構文とインデックス [#1793](https://github.com/pingcap/tidb/issues/1793)

    > **注記：**
    >
    > 現在、特定の AWS リージョンのTiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスのみが[`FULLTEXT`構文と索引](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)インデックスをサポートしています。TiDB Self-Managed およびTiDB Cloud Dedicatedは`FULLTEXT`構文の解析をサポートしていますが、 `FULLTEXT`インデックスの使用はサポートしていません。

-   `SPATIAL` （別名`GIS` / `GEOMETRY` ）関数、データ型、およびインデックス [#6347](https://github.com/pingcap/tidb/issues/6347)

-   `ascii` 、 `latin1` 、 `binary` 、 `utf8` 、 `utf8mb4` 、および`gbk` 。

-   オプティマイザトレース

-   XML関数

-   Xプロトコル [#1109](https://github.com/pingcap/tidb/issues/1109)

-   `XA`構文（TiDBは内部的に2フェーズコミットを使用しますが、これはSQLインターフェース経由では公開されません）

-   `CREATE TABLE tblName AS SELECT stmt`構文 [#4754](https://github.com/pingcap/tidb/issues/4754)

-   `CHECK TABLE`構文 [#4673](https://github.com/pingcap/tidb/issues/4673)

-   `CHECKSUM TABLE`構文 [#1895](https://github.com/pingcap/tidb/issues/1895)

-   `REPAIR TABLE`構文

-   `OPTIMIZE TABLE`構文

-   `HANDLER`ステートメント

-   `CREATE TABLESPACE`ステートメント

-   「セッショントラッカー：OKパケットにGTIDコンテキストを追加する」

-   降順インデックス [#2519](https://github.com/pingcap/tidb/issues/2519)

-   `SKIP LOCKED`構文 [#18207](https://github.com/pingcap/tidb/issues/18207)

-   側方派生テーブル [#40328](https://github.com/pingcap/tidb/issues/40328)

-   サブクエリ [#11414](https://github.com/pingcap/tidb/issues/11414)で結合します

## MySQLとの違い {#differences-from-mysql}

### 自動インクリメントID {#auto-increment-id}

-   TiDBでは、自動インクリメントされる列値（ID）は、単一のTiDBサーバー内でグローバルに一意であり、インクリメントされます。複数のTiDBサーバー間でIDをインクリメントするには、[`AUTO_INCREMENT` MySQL互換モード](/auto-increment.md#mysql-compatibility-mode)を使用できます。ただし、IDは必ずしも順番に割り当てられるとは限らないため、 `Duplicated Error`メッセージが表示されないように、デフォルト値とカスタム値を混在させないことをお勧めします。

-   `tidb_allow_remove_auto_inc`システム変数を使用すると、 `AUTO_INCREMENT`列属性の削除を許可または禁止できます。列属性を削除するには、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`構文を使用します。

-   TiDBは`AUTO_INCREMENT`列属性の追加をサポートしておらず、一度削除すると復元できません。

-   TiDB v6.6.0以前のバージョンでは、TiDBの自動インクリメント列はMySQL InnoDBと同様に動作し、主キーまたはインデックスプレフィックスである必要があります。v7.0.0以降、TiDBはこの制限を撤廃し、より柔軟なテーブル主キー定義を可能にしました。 [#40580](https://github.com/pingcap/tidb/issues/40580)

詳細については、 [`AUTO_INCREMENT`](/auto-increment.md)参照してください。

> **注記：**
>
> -   テーブル作成時に主キーを指定しない場合、TiDB は`_tidb_rowid`を使用して行を識別します。この値の割り当ては、自動インクリメント列 (そのような列が存在する場合) とアロケータを共有します。自動インクリメント列を主キーとして指定した場合、TiDB はこの列を使用して行を識別します。この場合、次のような状況が発生する可能性があります。

```sql
mysql> CREATE TABLE t(id INT UNIQUE KEY AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> INSERT INTO t VALUES();
Query OK, 1 rows affected (0.00 sec)

mysql> SELECT _tidb_rowid, id FROM t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           2 |    1 |
|           4 |    3 |
|           6 |    5 |
+-------------+------+
3 rows in set (0.01 sec)
```

図に示すように、共有アロケータのため、 `id`は毎回 2 ずつ増加します。この動作は[MySQL互換モード](/auto-increment.md#mysql-compatibility-mode)では変更され、共有アロケータがないため、数値のスキップは発生しません。

<CustomContent platform="tidb">

> **注記：**
>
> `AUTO_INCREMENT`属性により、本番環境でホットスポットが発生する可能性があります。詳細については[HotSpotの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)使用することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> `AUTO_INCREMENT`属性により、本番環境でホットスポットが発生する可能性があります。詳細については[HotSpotの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)を参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)使用することをお勧めします。

</CustomContent>

### パフォーマンス図 {#performance-schema}

<CustomContent platform="tidb">

TiDB は[プロメテウスとグラファナ](/tidb-monitoring-api.md)グラファナの組み合わせを利用して、パフォーマンス監視メトリックの保存とクエリを実行します。 TiDB では、ほとんどの [パフォーマンススキーマテーブル](/performance-schema/performance-schema.md)結果を返しません。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB Cloudのパフォーマンス メトリックを確認するには、 TiDB Cloudコンソールのクラスター概要ページを確認するか、 [サードパーティ製監視ツールとの連携](/tidb-cloud/third-party-monitoring-integrations.md)を使用します。ほとんどの [パフォーマンススキーマテーブル](/performance-schema/performance-schema.md)TiDB で空の結果を返します。

</CustomContent>

### クエリ実行プラン {#query-execution-plan}

TiDB のクエリ実行プラン ( `EXPLAIN` / `EXPLAIN FOR` ) の出力形式、内容、および権限設定は、MySQL のものとは大きく異なります。

TiDBでは、MySQLシステム変数`optimizer_switch`は読み取り専用であり、クエリプランには影響を与えません。オプティマイザヒントはMySQLと同様の構文で使用できますが、使用可能なヒントとその実装は異なる場合があります。

詳細については、[クエリ実行プランを理解する](/explain-overview.md)を参照してください。

### 組み込み関数 {#built-in-functions}

TiDBはMySQLの組み込み関数のほとんどをサポートしていますが、すべてではありません。使用可能な関数の一覧を取得するには、 [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md)ステートメントを使用してください。

### DDL操作 {#ddl-operations}

TiDBでは、サポートされているすべてのDDL変更をオンラインで実行できます。ただし、TiDBのDDL操作には、MySQLと比較していくつかの大きな制限があります。

-   単一の`ALTER TABLE`ステートメントを使用してテーブルの複数のスキーマ オブジェクト (列やインデックスなど) を変更する場合、同じオブジェクトを複数の変更で指定することはサポートされていません。たとえば、 `ALTER TABLE t1 MODIFY COLUMN c1 INT, DROP COLUMN c1`コマンドを実行すると、 `Unsupported operate same column/index`エラーが出力されます。
-   `ALTER TABLE` 、 `TIFLASH REPLICA`のように、単一の`SHARD_ROW_ID_BITS`ステートメントを使用して`AUTO_ID_CACHE` 。
-   TiDB は`ALTER TABLE`を使用した一部のデータ型の変更をサポートしていません。たとえば、TiDB は`DECIMAL`型から`DATE`型への変更をサポートしていません。データ型の変更がサポートされていない場合、TiDB は`Unsupported modify column: type %d not match origin %d`エラーを報告します。詳細については、 [`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)を参照してください。
-   `ALGORITHM={INSTANT,INPLACE,COPY}`構文はTiDBではアサーションとしてのみ関数し、 `ALTER`アルゴリズムを変更しません。詳細については、 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)参照してください。
-   `CLUSTERED`タイプの主キーの追加/削除はサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、[クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   異なるタイプのインデックス（ `HASH|BTREE|RTREE|FULLTEXT` ）はサポートされておらず、指定されても解析されて無視されます。
-   TiDB は`HASH` 、 `RANGE` 、 `LIST` 、および`KEY`パーティションタイプをサポートしています。サポートされていないパーティションタイプの場合、TiDB は`Warning: Unsupported partition type %s, treat as normal table`を返します。ここで、 `%s`はサポートされていない特定のパーティションタイプです。
-   Range、Range COLUMNS、List、およびList COLUMNSパーティションテーブルは、 `ADD` 、 `DROP` 、 `TRUNCATE` 、および`REORGANIZE`操作をサポートします。その他のパーティション操作は無視されます。
-   ハッシュおよびキーパーティションテーブルは`ADD` 、 `COALESCE` 、および`TRUNCATE`操作をサポートします。その他のパーティション操作は無視されます。
-   パーティションテーブルでは、以下の構文はサポートされていません。

    -   `SUBPARTITION`
    -   `{CHECK|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD} PARTITION`

    パーティショニングの詳細については、[パーティショニング](/partitioned-table.md)を参照してください。

### 表の分析 {#analyzing-tables}

TiDBでは、[統計の収集](/statistics.md#manual-collection)MySQLとは異なり、テーブルの統計情報を完全に再構築するため、より多くのリソースを消費し、完了までに時間がかかります。一方、MySQL/InnoDBでは、比較的軽量で短時間で完了する処理です。

詳細については、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)を参照してください。

### <code>SELECT</code>構文の制限事項 {#limitations-of-code-select-code-syntax}

TiDB は、次の`SELECT`構文をサポートしていません。

-   `SELECT ... INTO @variable`
-   `SELECT .. GROUP BY expr` MySQL 5.7のように`GROUP BY expr ORDER BY expr`を意味しません。

詳細については、 [`SELECT`](/sql-statements/sql-statement-select.md)文のリファレンスを参照してください。

### <code>UPDATE</code>文 {#code-update-code-statement}

[`UPDATE`](/sql-statements/sql-statement-update.md)文のリファレンスを参照してください。

### 閲覧数 {#views}

TiDB のビューは更新できず、 `UPDATE` 、 `INSERT` 、 `DELETE`などの書き込み操作をサポートしていません。

### 一時テーブル {#temporary-tables}

詳細については、 [TiDBローカル一時テーブルとMySQL一時テーブルの互換性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)参照してください。

### 文字セットと照合 {#character-sets-and-collations}

-   TiDB でサポートされている文字セットと照合順序については、[文字セットと照合の概要](/character-set-and-collation.md)参照してください。

-   GBK文字セットのMySQL互換性に関する情報については、 [GBK互換性](/character-set-gbk.md#mysql-compatibility)を参照してください。

-   TiDBは、テーブルで使用されている文字セットを各国語の文字セットとして継承します。

### ストレージエンジン {#storage-engines}

TiDBでは、代替storageエンジンを使用してテーブルを作成できます。ただし、互換性を確保するため、TiDBで記述されているメタデータはInnoDBstorageエンジン向けとなっています。

<CustomContent platform="tidb">

[`--store`](/command-line-flags-for-tidb-configuration.md#--store)オプションを使用してstorageエンジンを指定するには、TiDBサーバーを起動する必要があります。このstorageエンジンの抽象化機能は、MySQL と同様です。

</CustomContent>

### SQLモード {#sql-modes}

TiDB はほとんどの[SQLモード](/sql-mode.md)をサポートしています。

-   `Oracle`や`PostgreSQL`などの互換モードは解析されますが、無視されます。互換モードはMySQL 5.7で非推奨となり、MySQL 8.0 で削除されました。
-   `ONLY_FULL_GROUP_BY`モードには、 MySQL 5.7との小さな[意味の違い](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql)あります。
-   MySQL の`NO_DIR_IN_CREATE`および`NO_ENGINE_SUBSTITUTION` SQL モードは互換性のために受け入れられていますが、TiDB には適用できません。

### デフォルトの差異 {#default-differences}

TiDBは、MySQL 5.7およびMySQL 8.0と比較して、デフォルト設定にいくつかの違いがあります。

-   デフォルトの文字セット:
    -   TiDB のデフォルト値は`utf8mb4`です。
    -   MySQL 5.7のデフォルト値は`latin1`です。
    -   MySQL 8.0 のデフォルト値は`utf8mb4`です。
-   デフォルトの照合順序:
    -   TiDB のデフォルトの照合照合順序は`utf8mb4_bin`です。
    -   MySQL 5.7のデフォルトの照合照合順序は`utf8mb4_general_ci`です。
    -   MySQL 8.0 のデフォルトの照合照合順序は`utf8mb4_0900_ai_ci`です。
-   デフォルトのSQLモード:
    -   TiDB のデフォルトの SQL モードには、次のモードが含まれます: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION` 。
    -   MySQLのデフォルトのSQLモード：
        -   MySQL 5.7のデフォルトのSQLモードは、TiDBと同じです。
        -   MySQL 8.0 のデフォルトの SQL モードには、次のモードが含まれます: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION` 。
-   `lower_case_table_names`のデフォルト値:
    -   TiDB のデフォルト値は`2`であり、現在サポートされているのは`2`のみです。
    -   MySQLのデフォルト値は以下のとおりです。
        -   Linux の場合: `0` 。これは、テーブル名とデータベース名が`CREATE TABLE`または`CREATE DATABASE` 。名前の比較では大文字小文字が区別されます。
        -   Windows の場合: `1` 。これは、テーブル名がディスク上に小文字で保存され、名前の比較では大文字と小文字が区別されないことを意味します。MySQL は、storage時および検索時にすべてのテーブル名を小文字に変換します。この動作は、データベース名とテーブルエイリアスにも適用されます。
        -   macOS の場合: `2` 。これは、テーブル名とデータベース名が`CREATE TABLE`または`CREATE DATABASE`ステートメントで指定された文字の大文字小文字に従ってディスクに保存されますが、MySQL は検索時にそれらを小文字に変換します。名前の比較では大文字小文字は区別されません。
-   `explicit_defaults_for_timestamp`のデフォルト値:
    -   TiDB のデフォルト値は`ON`であり、現在サポートされているのは`ON`のみです。
    -   MySQLのデフォルト値は以下のとおりです。
        -   MySQL 5.7の場合: `OFF` 。
        -   MySQL 8.0 の場合: `ON` 。

### 日時 {#date-and-time}

TiDBは、以下の点を考慮して、名前付きタイムゾーンをサポートしています。

-   TiDBは、計算にシステムに現在インストールされているすべてのタイムゾーンルール（通常は`tzdata`パッケージ）を使用します。これにより、タイムゾーンテーブルデータをインポートすることなく、すべてのタイムゾーン名を使用できます。タイムゾーンテーブルデータをインポートしても、計算ルールは変更されません。
-   現在、MySQL はデフォルトでローカル タイムゾーンを使用し、システムに組み込まれている現在のタイムゾーン ルール (夏時間の開始時など) に基づいて計算します。 [タイムゾーンテーブルデータのインポート](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation)インポートがないと、MySQL は名前でタイムゾーンを指定できません。

### タイプシステムの違い {#type-system-differences}

以下の列タイプはMySQLではサポートされていますが、TiDBでは**サポートされていません**。

-   `SQL_TSI_*` （SQL_TSI_MONTH、SQL_TSI_WEEK、SQL_TSI_DAY、SQL_TSI_HOUR、SQL_TSI_MINUTE、SQL_TSI_SECONDを含みますが、SQL_TSI_YEARは含みません）

### 正規表現 {#regular-expressions}

`REGEXP_INSTR()` 、 `REGEXP_LIKE()` 、および`REGEXP_REPLACE()`含む、MySQL `REGEXP_SUBSTR()` [MySQLとの正規表現互換性](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)を参照してください。

### 非推奨機能による非互換性 {#incompatibility-due-to-deprecated-features}

TiDBは、MySQLで非推奨となった特定の機能を実装していません。例えば、以下の機能などです。

-   浮動小数点型の精度を指定する。MySQL 8.0 ではこの機能[非推奨](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)、代わりに`DECIMAL`型を使用することをお勧めします。
-   `ZEROFILL`属性。MySQL 8.0ではこの機能[非推奨](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html)、代わりにアプリケーションで数値をパディングすることをお勧めします。

### <code>CREATE RESOURCE GROUP</code> 、 <code>DROP RESOURCE GROUP</code> 、および<code>ALTER RESOURCE GROUP</code>ステートメント {#code-create-resource-group-code-code-drop-resource-group-code-and-code-alter-resource-group-code-statements}

リソースグループの作成、変更、削除に関する以下のステートメントは、MySQLとは異なるパラメータをサポートしています。詳細については、以下のドキュメントを参照してください。

-   [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)
-   [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)
-   [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)

## MySQL InnoDBとの悲観的トランザクション（ロック）に関する相違点 {#differences-on-pessimistic-transaction-lock-with-mysql-innodb}

TiDB と MySQL InnoDB の悲観的トランザクション (ロック) の違いについては、 [MySQL InnoDBとの違い](/pessimistic-transaction.md#differences-from-mysql-innodb)参照してください。
