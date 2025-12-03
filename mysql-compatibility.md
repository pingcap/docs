---
title: MySQL Compatibility
summary: TiDB と MySQL の互換性、およびサポートされていない機能と異なる機能について学習します。
---

# MySQLの互換性 {#mysql-compatibility}

<CustomContent platform="tidb">

TiDBは、MySQLプロトコル、およびMySQL 5.7とMySQL 8.0の共通機能と構文と高い互換性があります。MySQLエコシステムツール（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver、 [もっと](/develop/dev-guide-third-party-support.md#gui) ）とMySQLクライアントはTiDBでも使用できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDBは、MySQLプロトコル、およびMySQL 5.7とMySQL 8.0の共通機能と構文と高い互換性があります。MySQLエコシステムツール（PHPMyAdmin、Navicat、MySQL Workbench、DBeaver、 [もっと](https://docs.pingcap.com/tidb/stable/dev-guide-third-party-support#gui) ）とMySQLクライアントはTiDBでも使用できます。

</CustomContent>

ただし、MySQLの一部の機能はTiDBではサポートされていません。これは、問題を解決するより優れた方法（XML関数の代わりにJSONを使用するなど）が存在するため、あるいは、必要な労力に対して需要が不足しているため（ストアドプロシージャや関数など）、といった理由が考えられます。さらに、一部の機能は分散システムへの実装が難しい場合もあります。

<CustomContent platform="tidb">

TiDBはMySQLレプリケーションプロトコルをサポートしていないことに注意してください。代わりに、MySQLでデータをレプリケーションするための専用ツールが提供されています。

-   MySQL からデータを複製: [TiDB データ移行 (DM)](/dm/dm-overview.md) 、MySQL または MariaDB から TiDB への完全なデータ移行と増分データ複製をサポートするツールです。
-   MySQLへのデータ複製： [TiCDC](/ticdc/ticdc-overview.md) 、TiKVの変更ログを取得してTiDBの増分データを複製するツールです。TiCDCは[MySQLシンク](/ticdc/ticdc-overview.md#replication-consistency)を使用して、TiDBの増分データをMySQLに複製します。

</CustomContent>

<CustomContent platform="tidb">

> **注記：**
>
> このページでは、MySQLとTiDBの一般的な違いについて説明します。セキュリティ分野におけるMySQLとの互換性の詳細については、 [MySQLとのSecurity互換性](/security-compatibility-with-mysql.md)参照してください。

</CustomContent>

[TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=mysql_compatibility)で TiDB の機能を試すことができます。

## サポートされていない機能 {#unsupported-features}

-   ストアドプロシージャと関数

-   トリガー

-   イベント

-   ユーザー定義関数

-   `FULLTEXT`構文とインデックス[＃1793](https://github.com/pingcap/tidb/issues/1793)

    > **注記：**
    >
    > 現在、特定の AWS リージョンのTiDB Cloud Starter およびTiDB Cloud Essential クラスターのみが[`FULLTEXT`構文とインデックス](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)サポートしています。TiDB Self-Managed およびTiDB Cloud Dedicated は`FULLTEXT`構文の解析をサポートしていますが、 `FULLTEXT`インデックスの使用はサポートしていません。

-   `SPATIAL` （ `GIS` / `GEOMETRY`とも呼ばれる）関数、データ型、インデックス[＃6347](https://github.com/pingcap/tidb/issues/6347)

-   `ascii` 、 `latin1` 、 `binary` 、 `utf8` 、 `utf8mb4` 、 `gbk`以外の文字セット。

-   オプティマイザートレース

-   XML関数

-   Xプロトコル[＃1109](https://github.com/pingcap/tidb/issues/1109)

-   列レベルの権限[＃9766](https://github.com/pingcap/tidb/issues/9766)

-   `XA`構文 (TiDB は内部的に 2 フェーズ コミットを使用しますが、これは SQL インターフェース経由では公開されません)

-   `CREATE TABLE tblName AS SELECT stmt`構文[＃4754](https://github.com/pingcap/tidb/issues/4754)

-   `CHECK TABLE`構文[＃4673](https://github.com/pingcap/tidb/issues/4673)

-   `CHECKSUM TABLE`構文[＃1895](https://github.com/pingcap/tidb/issues/1895)

-   `REPAIR TABLE`構文

-   `OPTIMIZE TABLE`構文

-   `HANDLER`ステートメント

-   `CREATE TABLESPACE`ステートメント

-   「セッション トラッカー: OK パケットに GTID コンテキストを追加する」

-   降順インデックス[＃2519](https://github.com/pingcap/tidb/issues/2519)

-   `SKIP LOCKED`構文[＃18207](https://github.com/pingcap/tidb/issues/18207)

-   横方向導出表[＃40328](https://github.com/pingcap/tidb/issues/40328)

-   JOIN ON サブクエリ[＃11414](https://github.com/pingcap/tidb/issues/11414)

## MySQLとの違い {#differences-from-mysql}

### 自動増分ID {#auto-increment-id}

-   TiDBでは、自動増分列の値（ID）はグローバルに一意であり、単一のTiDBサーバー内では増分されます。複数のTiDBサーバー間でIDを増分するには、 [`AUTO_INCREMENT` MySQL互換モード](/auto-increment.md#mysql-compatibility-mode)を使用します。ただし、IDは必ずしも順番に割り当てられるわけではないため、 `Duplicated Error`というメッセージが表示されないように、デフォルト値とカスタム値を混在させないようにすることをお勧めします。

-   システム変数`tidb_allow_remove_auto_inc`を使用して、列属性`AUTO_INCREMENT`削除を許可または禁止できます。列属性を削除するには、構文`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`を使用します。

-   TiDB は`AUTO_INCREMENT`列属性の追加をサポートしておらず、一度削除すると回復できません。

-   TiDB v6.6.0以前のバージョンでは、TiDBの自動インクリメント列はMySQL InnoDBと同様に動作し、主キーまたはインデックスプレフィックスである必要があります。v7.0.0以降ではこの制限がなくなり、より柔軟なテーブル主キー定義が可能になります[＃40580](https://github.com/pingcap/tidb/issues/40580)

詳細については[`AUTO_INCREMENT`](/auto-increment.md)参照してください。

> **注記：**
>
> -   テーブル作成時に主キーを指定しない場合、TiDBは行を識別するために`_tidb_rowid`使用します。この値の割り当ては、自動インクリメント列（存在する場合）とアロケータを共有します。自動インクリメント列を主キーとして指定すると、TiDBはこの列を使用して行を識別します。この場合、以下の状況が発生する可能性があります。

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

ご覧のとおり、共有アロケータがあるため、 `id`は毎回 2 ずつ増加します。3 [MySQL互換モード](/auto-increment.md#mysql-compatibility-mode)この動作は変わり、共有アロケータがないため、数値のスキップは発生しません。

<CustomContent platform="tidb">

> **注記：**
>
> `AUTO_INCREMENT`属性は本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)使用することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> `AUTO_INCREMENT`属性は本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)使用することをお勧めします。

</CustomContent>

### パフォーマンススキーマ {#performance-schema}

<CustomContent platform="tidb">

TiDBは、パフォーマンス監視メトリックの保存とクエリに[プロメテウスとグラファナ](/tidb-monitoring-api.md)の組み合わせを使用します。TiDBでは、ほとんどの場合、 [パフォーマンススキーマテーブル](/performance-schema/performance-schema.md)結果を返しません。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB Cloudのパフォーマンス メトリックを確認するには、 TiDB Cloudコンソールのクラスター概要ページを確認するか、 [サードパーティの監視統合](/tidb-cloud/third-party-monitoring-integrations.md)使用します。ほとんどの場合、 [パフォーマンススキーマテーブル](/performance-schema/performance-schema.md) TiDB で空の結果を返します。

</CustomContent>

### クエリ実行プラン {#query-execution-plan}

TiDB のクエリ実行プラン ( `EXPLAIN` ) の出力形式、内容、権限設定は`EXPLAIN FOR` MySQL とは大きく異なります。

TiDBでは、MySQLシステム変数`optimizer_switch`読み取り専用であり、クエリプランには影響しません。オプティマイザヒントはMySQLと同様の構文で使用できますが、利用可能なヒントとその実装は異なる場合があります。

詳細については[クエリ実行プランを理解する](/explain-overview.md)を参照してください。

### 組み込み関数 {#built-in-functions}

TiDBはMySQLの組み込み関数のほとんどをサポートしていますが、すべてをサポートしているわけではありません。使用可能な関数のリストを取得するには、ステートメント[`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md)を使用します。

### DDL操作 {#ddl-operations}

TiDBでは、サポートされているすべてのDDL変更をオンラインで実行できます。ただし、MySQLと比較して、TiDBのDDL操作にはいくつかの大きな制限があります。

-   単一の`ALTER TABLE`ステートメントを使用してテーブル内の複数のスキーマオブジェクト（列やインデックスなど）を変更する場合、複数の変更で同じオブジェクトを指定することはサポートされていません。例えば、 `ALTER TABLE t1 MODIFY COLUMN c1 INT, DROP COLUMN c1`コマンドを実行すると、 `Unsupported operate same column/index`エラーが出力されます。
-   `TIFLASH REPLICA` 、 `SHARD_ROW_ID_BITS` 、 `AUTO_ID_CACHE`などの複数の TiDB 固有のスキーマ オブジェクトを単一の`ALTER TABLE`ステートメントを使用して変更することはサポートされていません。
-   TiDBは、 `ALTER TABLE`使用した一部のデータ型の変更をサポートしていません。例えば、 `DECIMAL`型から`DATE`型への変更はサポートしていません。データ型の変更がサポートされていない場合、TiDBは`Unsupported modify column: type %d not match origin %d`エラーを報告します。詳細は[`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)を参照してください。
-   `ALGORITHM={INSTANT,INPLACE,COPY}`構文はTiDBにおけるアサーションとしてのみ関数、 `ALTER`アルゴリズムを変更するものではありません。詳細は[`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)参照してください。
-   `CLUSTERED`型の主キーの追加/削除はサポートされていません。3 `CLUSTERED`の主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   異なるタイプのインデックス（ `HASH|BTREE|RTREE|FULLTEXT` ）はサポートされておらず、指定された場合は解析されて無視されます。
-   TiDBは`HASH` 、 `RANGE` 、 `LIST` 、 `KEY`パーティションタイプをサポートしています。サポートされていないパーティションタイプの場合、TiDBは`Warning: Unsupported partition type %s, treat as normal table`返します。ここで、 `%s`はサポートされていないパーティションタイプを表します。
-   範囲、範囲列、リスト、およびリスト列でパーティション化されたテーブルは`ADD` `DROP` `TRUNCATE`および`REORGANIZE`演算をサポートします。その他のパーティション演算は無視されます。
-   ハッシュおよびキーパーティションテーブルは`COALESCE` `ADD` `TRUNCATE`をサポートします。その他のパーティション操作は無視されます。
-   次の構文はパーティション テーブルではサポートされていません。

    -   `SUBPARTITION`
    -   `{CHECK|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD} PARTITION`

    パーティション分割の詳細については、 [パーティショニング](/partitioned-table.md)参照してください。

### 表の分析 {#analyzing-tables}

TiDBでは、テーブルの統計情報を完全に再構築するという点でMySQLとは[統計収集](/statistics.md#manual-collection) 、より多くのリソースを消費し、完了までに長い時間がかかります。一方、MySQL/InnoDBは比較的軽量で、短時間で終了する操作を実行します。

詳細については[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)を参照してください。

### <code>SELECT</code>構文の制限 {#limitations-of-code-select-code-syntax}

TiDB は次の`SELECT`構文をサポートしていません。

-   `SELECT ... INTO @variable`
-   MySQL 5.7のように、 `SELECT .. GROUP BY expr` `GROUP BY expr ORDER BY expr`意味するわけではありません。

詳細については、 [`SELECT`](/sql-statements/sql-statement-select.md)ステートメントのリファレンスを参照してください。

### <code>UPDATE</code>ステートメント {#code-update-code-statement}

[`UPDATE`](/sql-statements/sql-statement-update.md)文の参照を参照してください。

### ビュー {#views}

TiDB 内のビューは更新できず、 `UPDATE` 、 `INSERT` 、 `DELETE`などの書き込み操作をサポートしません。

### 一時テーブル {#temporary-tables}

詳細については[TiDB ローカル一時テーブルと MySQL 一時テーブル間の互換性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)参照してください。

### 文字セットと照合順序 {#character-sets-and-collations}

-   TiDB でサポートされている文字セットと照合順序の詳細については、 [文字セットと照合順序の概要](/character-set-and-collation.md)参照してください。

-   GBK 文字セットの MySQL 互換性については、 [GBK互換性](/character-set-gbk.md#mysql-compatibility)を参照してください。

-   TiDB は、テーブルで使用される文字セットを国別文字セットとして継承します。

### ストレージエンジン {#storage-engines}

TiDBでは、代替storageエンジンを使用してテーブルを作成できます。ただし、TiDBで記述されるメタデータは、互換性を確保するためにInnoDBstorageエンジン用です。

<CustomContent platform="tidb">

[`--store`](/command-line-flags-for-tidb-configuration.md#--store)オプションを使用してstorageエンジンを指定するには、TiDBサーバーを起動する必要があります。このstorageエンジンの抽象化機能は MySQL に似ています。

</CustomContent>

### SQLモード {#sql-modes}

TiDB は、ほとんど[SQLモード](/sql-mode.md)をサポートします。

-   互換モード（ `Oracle`など`PostgreSQL`は解析されますが無視されます。互換モードはMySQL 5.7で非推奨となり、MySQL 8.0で削除されました。
-   `ONLY_FULL_GROUP_BY`モードには、 MySQL 5.7からのマイナー[意味の違い](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql)あります。
-   MySQL の SQL モード`NO_DIR_IN_CREATE`および`NO_ENGINE_SUBSTITUTION`は互換性のために受け入れられますが、TiDB には適用されません。

### デフォルトの違い {#default-differences}

TiDB は、MySQL 5.7および MySQL 8.0 と比較するとデフォルトで違いがあります。

-   デフォルトの文字セット:
    -   TiDB のデフォルト値は`utf8mb4`です。
    -   MySQL 5.7のデフォルト値は`latin1`です。
    -   MySQL 8.0 のデフォルト値は`utf8mb4`です。
-   デフォルトの照合順序:
    -   TiDB のデフォルトの照合順序は`utf8mb4_bin`です。
    -   MySQL 5.7のデフォルトの照合順序は`utf8mb4_general_ci`です。
    -   MySQL 8.0 のデフォルトの照合順序は`utf8mb4_0900_ai_ci`です。
-   デフォルトの SQL モード:
    -   TiDB のデフォルトの SQL モードには次のモードが含まれます: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION` 。
    -   MySQL のデフォルトの SQL モード:
        -   MySQL 5.7のデフォルトの SQL モードは TiDB と同じです。
        -   MySQL 8.0 のデフォルトの SQL モードには、次のモードが含まれます: `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION` 。
-   デフォルト値`lower_case_table_names` :
    -   TiDB のデフォルト値は`2`で、現在は`2`のみがサポートされています。
    -   MySQL のデフォルトは次の値になります。
        -   Linuxの場合： `0` 。テーブル名とデータベース名は、 `CREATE TABLE`または`CREATE DATABASE`ステートメントで指定された大文字と小文字の区別に従ってディスクに保存されます。名前の比較では大文字と小文字が区別されます。
        -   Windowsの場合： `1` 。これは、テーブル名がディスク上に小文字で保存され、名前の比較では大文字と小文字が区別されないことを意味します。MySQLは、storageおよび検索時にすべてのテーブル名を小文字に変換します。この動作は、データベース名とテーブルエイリアスにも適用されます。
        -   macOSの場合： `2` 。テーブル名とデータベース名は、 `CREATE TABLE`または`CREATE DATABASE`ステートメントで指定された大文字と小文字の区別に従ってディスクに保存されますが、MySQLは検索時に小文字に変換します。名前の比較では大文字と小文字は区別されません。
-   デフォルト値`explicit_defaults_for_timestamp` :
    -   TiDB のデフォルト値は`ON`で、現在は`ON`のみがサポートされています。
    -   MySQL のデフォルトは次の値になります。
        -   MySQL 5.7の場合: `OFF` .
        -   MySQL 8.0 の場合: `ON` .

### 日時 {#date-and-time}

TiDB は、次の点を考慮して名前付きタイムゾーンをサポートします。

-   TiDBは、システムに現在インストールされているすべてのタイムゾーンルール（通常は`tzdata`パッケージ）を計算に使用します。これにより、タイムゾーンテーブルデータをインポートすることなく、すべてのタイムゾーン名を使用できます。タイムゾーンテーブルデータをインポートしても、計算ルールは変更されません。
-   現在、MySQLはデフォルトでローカルタイムゾーンを使用し、その後、システムに組み込まれている現在のタイムゾーンルール（例えば、サマータイムの開始時期など）に基づいて計算を行います。1 [タイムゾーンテーブルデータのインポート](https://dev.mysql.com/doc/refman/8.0/en/time-zone-support.html#time-zone-installation)指定しないと、MySQLはタイムゾーンを名前で指定できません。

### 型システムの違い {#type-system-differences}

次の列タイプは MySQL ではサポートされていますが、TiDB では**サポートされていません**。

-   `SQL_TSI_*` (SQL_TSI_MONTH、SQL_TSI_WEEK、SQL_TSI_DAY、SQL_TSI_HOUR、SQL_TSI_MINUTE、および SQL_TSI_SECOND が含まれますが、SQL_TSI_YEAR は含まれません)

### 正規表現 {#regular-expressions}

`REGEXP_INSTR()` 、 `REGEXP_LIKE()` 、 `REGEXP_REPLACE()` 、 `REGEXP_SUBSTR()`を含む、TiDB 正規表現と MySQL の互換性については、 [MySQLとの正規表現の互換性](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)参照してください。

### 非推奨の機能による非互換性 {#incompatibility-due-to-deprecated-features}

TiDB は、MySQL で非推奨となった次のような特定の機能を実装していません。

-   浮動小数点型の精度を指定します。MySQL 8.0 [非推奨](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)ではこの機能はサポートされておらず、代わりに`DECIMAL`型を使用することをお勧めします。
-   `ZEROFILL`属性。MySQL 8.0 [非推奨](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html)ではこの機能がサポートされておらず、代わりにアプリケーションで数値を埋め込むことが推奨されます。

### <code>CREATE RESOURCE GROUP</code> 、 <code>DROP RESOURCE GROUP</code> 、および<code>ALTER RESOURCE GROUP</code>ステートメント {#code-create-resource-group-code-code-drop-resource-group-code-and-code-alter-resource-group-code-statements}

リソースグループの作成、変更、削除を行う以下のステートメントは、MySQLとは異なるパラメータをサポートしています。詳細については、以下のドキュメントをご覧ください。

-   [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md)
-   [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md)
-   [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md)

## MySQL InnoDB の悲観的トランザクション（ロック）の違い {#differences-on-pessimistic-transaction-lock-with-mysql-innodb}

TiDB と MySQL InnoDB の悲観的トランザクション (ロック) の違いについては、 [MySQL InnoDBとの違い](/pessimistic-transaction.md#differences-from-mysql-innodb)参照してください。
