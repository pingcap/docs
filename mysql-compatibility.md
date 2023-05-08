---
title: MySQL Compatibility
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
---

# MySQL の互換性 {#mysql-compatibility}

TiDB は、 MySQL 5.7プロトコルおよびMySQL 5.7の一般的な機能と構文と高度な互換性があります。 MySQL 5.7のエコシステム ツール (PHPMyAdmin、Navicat、MySQL Workbench、mysqldump、および Mydumper/myloader) と MySQL クライアントを TiDB に使用できます。

ただし、MySQL の一部の機能はサポートされていません。これは、問題を解決するためのより良い方法 (JSON に取って代わられた XML関数など) があるか、必要な労力に対して現在の需要が不足している (ストアド プロシージャや関数など) ためである可能性があります。一部の機能は、分散システムとして実装するのが難しい場合もあります。

<CustomContent platform="tidb">

さらに、TiDB は MySQL レプリケーション プロトコルをサポートしていませんが、MySQL でデータをレプリケートするための特定のツールを提供します。

-   MySQL からのデータの複製: [TiDB データ移行 (DM)](/dm/dm-overview.md) 、MySQL/MariaDB から TiDB への完全なデータ移行と増分データ複製をサポートするツールです。
-   レプリケート データを MySQL: [TiCDC](/ticdc/ticdc-overview.md) 、TiKV 変更ログをプルして、TiDB の増分データをレプリケートするためのツールです。 TiCDC は[MySQL シンク](/ticdc/ticdc-overview.md#sink-support)使用して、TiDB の増分データを MySQL に複製します。

> **ノート：**
>
> このページでは、MySQL と TiDB の一般的な違いについて説明します。 [Security](/security-compatibility-with-mysql.md)と[ペシミスティックトランザクションモード](/pessimistic-transaction.md#difference-with-mysql-innodb)の互換性については、専用ページを参照してください。

</CustomContent>

## サポートされていない機能 {#unsupported-features}

-   ストアド プロシージャと関数
-   トリガー
-   イベント
-   ユーザー定義関数
-   `FOREIGN KEY`制約[#18209](https://github.com/pingcap/tidb/issues/18209)
-   `FULLTEXT`構文とインデックス[#1793](https://github.com/pingcap/tidb/issues/1793)
-   `SPATIAL` (別名`GIS` / `GEOMETRY` )関数、データ型、およびインデックス[#6347](https://github.com/pingcap/tidb/issues/6347)
-   `ascii` 、 `latin1` 、 `binary` 、 `utf8` 、 `utf8mb4` 、および`gbk`以外の文字セット。
-   SYSスキーマ
-   オプティマイザ トレース
-   XML 関数
-   X-プロトコル[#1109](https://github.com/pingcap/tidb/issues/1109)
-   セーブポイント[#6840](https://github.com/pingcap/tidb/issues/6840)
-   列レベルの権限[#9766](https://github.com/pingcap/tidb/issues/9766)
-   `XA`構文 (TiDB は内部で 2 フェーズ コミットを使用しますが、これは SQL インターフェイス経由で公開されません)
-   `CREATE TABLE tblName AS SELECT stmt`構文[#4754](https://github.com/pingcap/tidb/issues/4754)
-   `CHECK TABLE`構文[#4673](https://github.com/pingcap/tidb/issues/4673)
-   `CHECKSUM TABLE`構文[#1895](https://github.com/pingcap/tidb/issues/1895)
-   `REPAIR TABLE`構文
-   `OPTIMIZE TABLE`構文
-   `GET_LOCK`および`RELEASE_LOCK`関数[#14994](https://github.com/pingcap/tidb/issues/14994)
-   `LOAD DATA`と`REPLACE`キーワード[#24515](https://github.com/pingcap/tidb/issues/24515)
-   `HANDLER`ステートメント
-   `CREATE TABLESPACE`ステートメント

## MySQL とは異なる機能 {#features-that-are-different-from-mysql}

### 自動インクリメント ID {#auto-increment-id}

-   TiDB では、自動増分列はグローバルに一意です。それらは単一の TiDBサーバー上では増分ですが、必ずしも複数の TiDB サーバー間で増分されたり、順次割り当てられるとは限り*ません*。デフォルト値とカスタム値を混在させないことをお勧めします。そうしないと、 `Duplicated Error`エラー メッセージが表示される場合があります。

-   `tidb_allow_remove_auto_inc`システム変数を使用して、 `AUTO_INCREMENT`列属性の削除を許可または禁止できます。 column 属性を削除する構文は`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`です。

-   TiDB は`AUTO_INCREMENT`列属性の追加をサポートしておらず、この属性は削除すると復元できません。

-   詳細については[`AUTO_INCREMENT`](/auto-increment.md)参照してください。

> **ノート：**
>
> -   テーブルの作成時に主キーを指定しなかった場合、TiDB は`_tidb_rowid`を使用して行を識別します。この値の割り当ては、自動インクリメント列 (そのような列が存在する場合) とアロケーターを共有します。自動インクリメント列を主キーとして指定すると、TiDB はこの列を使用して行を識別します。この状況では、次の状況が発生する可能性があります。

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

<CustomContent platform="tidb">

> **ノート：**
>
> `AUTO_INCREMENT`属性は、本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)を使用することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> `AUTO_INCREMENT`属性は、本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)を使用することをお勧めします。

</CustomContent>

### パフォーマンススキーマ {#performance-schema}

<CustomContent platform="tidb">

TiDB は[プロメテウスとグラファナ](/tidb-monitoring-api.md)の組み合わせを使用して、パフォーマンス監視メトリックを格納およびクエリします。パフォーマンス スキーマ テーブルは、TiDB で空の結果を返します。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB Cloudでパフォーマンス メトリックを確認するには、 TiDB Cloudコンソールでクラスターの概要ページを確認するか、または[サードパーティの監視統合](/tidb-cloud/monitor-tidb-cluster.md#third-party-integrations)を使用します。パフォーマンス スキーマ テーブルは、TiDB で空の結果を返します。

</CustomContent>

### クエリ実行プラン {#query-execution-plan}

TiDB の Query Execution Plan ( `EXPLAIN` ) の出力形式、出力内容、 `EXPLAIN FOR`設定は、MySQL と大きく異なります。

MySQL システム変数`optimizer_switch` TiDB では読み取り専用であり、クエリ プランには影響しません。 MySQL と同様の構文で[オプティマイザーのヒント](/optimizer-hints.md)使用することもできますが、利用可能なヒントと実装は異なる場合があります。

詳細については[クエリ実行計画を理解する](/explain-overview.md)参照してください。

### 組み込み関数 {#built-in-functions}

TiDB は MySQL 組み込み関数のほとんどをサポートしていますが、すべてではありません。ステートメント`SHOW BUILTINS`は、使用可能な関数のリストを提供します。

参照: [TiDB SQL文法](https://pingcap.github.io/sqlgram/#functioncallkeyword) .

### DDL {#ddl}

TiDB では、サポートされているすべての DDL 変更がオンラインで実行されます。 MySQL での DDL 操作と比較して、TiDB での DDL 操作には次の主な制限があります。

-   `ALTER TABLE`つのステートメントで複数の操作を完了することはできません。たとえば、1 つのステートメントに複数の列またはインデックスを追加することはできません。 `Unsupported multi schema change`エラーが出力される場合があります。
-   TiDB の`ALTER TABLE`は、一部のデータ型の変更をサポートしていません。たとえば、TiDB は`DECIMAL`型から`DATE`型への変更をサポートしていません。データ型の変更がサポートされていない場合、TiDB は`Unsupported modify column: type %d not match origin %d`エラーを報告します。詳細については[`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)を参照してください。
-   `ALGORITHM={INSTANT,INPLACE,COPY}`構文は、TiDB でのアサーションとしてのみ関数、 `ALTER`アルゴリズムを変更しません。詳細については、 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)参照してください。
-   `CLUSTERED`タイプの主キーの追加/削除はサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   異なるタイプのインデックス ( `HASH|BTREE|RTREE|FULLTEXT` ) はサポートされておらず、指定すると解析されて無視されます。
-   TiDB は`HASH` 、 `RANGE` 、および`LIST`パーティショニング タイプをサポートします。サポートされていないパーティション タイプの場合、TiDB は`Warning: Unsupported partition type, treat as normal table`を返します。ここで、 `%s`は特定のパーティション タイプです。
-   テーブル パーティショニングは、 `ADD` 、 `DROP` 、および`TRUNCATE`操作をサポートします。他のパーティション操作は無視されます。次のテーブル パーティション構文はサポートされていません。

    -   `PARTITION BY KEY`
    -   `SUBPARTITION`
    -   `{CHECK|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD|REORGANIZE|COALESCE} PARTITION`

    詳細については、 [パーティショニング](/partitioned-table.md)を参照してください。

### テーブルを分析する {#analyze-table}

[統計収集](/statistics.md#manual-collection)は、MySQL/InnoDB では比較的軽量で短時間の操作であるという点で、TiDB では MySQL とは異なる動作をしますが、TiDB ではテーブルの統計を完全に再構築し、完了するまでにはるかに長い時間がかかる可能性があります。

これらの違いについては、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)で詳しく説明しています。

### <code>SELECT</code>構文の制限 {#limitations-of-code-select-code-syntax}

-   構文`SELECT ... INTO @variable`はサポートされていません。
-   構文`SELECT ... GROUP BY ... WITH ROLLUP`はサポートされていません。
-   構文`SELECT .. GROUP BY expr`は、 MySQL 5.7のように`GROUP BY expr ORDER BY expr`を意味しません。

詳細については、 [`SELECT`](/sql-statements/sql-statement-select.md)ステートメントのリファレンスを参照してください。

### <code>UPDATE</code>ステートメント {#code-update-code-statement}

[`UPDATE`](/sql-statements/sql-statement-update.md)文のリファレンスを参照してください。

### ビュー {#views}

TiDB のビューは更新できません。 `UPDATE` 、 `INSERT` 、 `DELETE`などの書き込み操作はサポートしていません。

### 一時テーブル {#temporary-tables}

詳細については、 [TiDB ローカル一時テーブルと MySQL 一時テーブルの互換性](/temporary-tables.md#compatibility-with-mysql-temporary-tables)を参照してください。

### 文字セットと照合 {#character-sets-and-collations}

-   TiDB でサポートされている文字セットと照合順序の詳細については、 [文字セットと照合の概要](/character-set-and-collation.md)を参照してください。

-   GBK 文字セットの MySQL 互換性については、 [GBK の互換性](/character-set-gbk.md#mysql-compatibility)を参照してください。

### ストレージ エンジン {#storage-engines}

互換性の理由から、TiDB は代替storageエンジンを使用してテーブルを作成する構文をサポートしています。実装では、TiDB はメタデータを InnoDBstorageエンジンとして記述します。

<CustomContent platform="tidb">

TiDB は MySQL と同様のstorageエンジンの抽象化をサポートしていますが、TiDBサーバーを起動するときに[`--store`](/command-line-flags-for-tidb-configuration.md#--store)オプションを使用してstorageエンジンを指定する必要があります。

</CustomContent>

### SQL モード {#sql-modes}

TiDB はほとんどの[SQL モード](/sql-mode.md)をサポートしています:

-   `Oracle`や`PostgreSQL`などの互換モードは解析されますが、無視されます。互換モードはMySQL 5.7で廃止され、MySQL 8.0 で削除されました。
-   `ONLY_FULL_GROUP_BY`モードには、 MySQL 5.7からのマイナー[意味の違い](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql)があります。
-   MySQL の`NO_DIR_IN_CREATE`および`NO_ENGINE_SUBSTITUTION` SQL モードは互換性のために受け入れられますが、TiDB には適用されません。

### デフォルトの違い {#default-differences}

-   デフォルトの文字セット:
    -   TiDB のデフォルト値は`utf8mb4`です。
    -   MySQL 5.7のデフォルト値は`latin1`です。
    -   MySQL 8.0 のデフォルト値は`utf8mb4`です。
-   デフォルトの照合順序:
    -   TiDB のデフォルトの照合順序`utf8mb4`は`utf8mb4_bin`です。
    -   MySQL 5.7のデフォルトの照合順序`utf8mb4`は`utf8mb4_general_ci`です。
    -   MySQL 8.0 のデフォルトの照合順序`utf8mb4`は`utf8mb4_0900_ai_ci`です。
-   デフォルト値`foreign_key_checks` :
    -   TiDB のデフォルト値は`OFF`で、現在 TiDB は`OFF`のみをサポートしています。
    -   MySQL 5.7のデフォルト値は`ON`です。
-   デフォルトの SQL モード:
    -   TiDB のデフォルトの SQL モードには、 `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`のモードが含まれます。
    -   MySQL のデフォルトの SQL モード:
        -   MySQL 5.7のデフォルトの SQL モードは TiDB と同じです。
        -   MySQL 8.0 のデフォルトの SQL モードには、 `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`のモードが含まれます。
-   デフォルト値`lower_case_table_names` :
    -   TiDB のデフォルト値は`2`で、現在 TiDB は`2`のみをサポートしています。
    -   MySQL のデフォルト値:
        -   Linux の場合: `0`
        -   Windows の場合: `1`
        -   macOS の場合: `2`
-   デフォルト値`explicit_defaults_for_timestamp` :
    -   TiDB のデフォルト値は`ON`で、現在 TiDB は`ON`のみをサポートしています。
    -   MySQL のデフォルト値:
        -   MySQL 5.7の場合: `OFF` 。
        -   MySQL 8.0 の場合: `ON` .

### 日時 {#date-and-time}

#### 名前付きタイムゾーン {#named-timezone}

-   TiDB は、計算のために現在システムにインストールされているすべてのタイム ゾーン ルールを使用します (通常は`tzdata`のパッケージ)。タイム ゾーン テーブル データをインポートしなくても、すべてのタイム ゾーン名を使用できます。タイム ゾーン テーブル データをインポートして計算規則を変更することはできません。
-   MySQL はデフォルトでローカル タイム ゾーンを使用し、システムに組み込まれている現在のタイム ゾーン規則 (夏時間の開始時期など) に基づいて計算します。また、タイム ゾーンは、タイム ゾーン名で[タイム ゾーン テーブル データのインポート](https://dev.mysql.com/doc/refman/5.7/en/time-zone-support.html#time-zone-installation)なしで指定することはできません。

### 型システムの違い {#type-system-differences}

次の列タイプは MySQL でサポートされていますが、TiDB ではサポート**されていません**。

-   FLOAT4/FLOAT8
-   `SQL_TSI_*` (SQL_TSI_MONTH、SQL_TSI_WEEK、SQL_TSI_DAY、SQL_TSI_HOUR、SQL_TSI_MINUTE、および SQL_TSI_SECOND を含み、SQL_TSI_YEAR を除く)

### 非推奨の機能による非互換性 {#incompatibility-caused-by-deprecated-features}

TiDB は、MySQL で非推奨としてマークされている次のような特定の機能を実装していません。

-   浮動小数点型の精度の指定。 MySQL 8.0 ではこの機能は[廃止する](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html) 、代わりに`DECIMAL`タイプを使用することをお勧めします。
-   `ZEROFILL`属性。 MySQL 8.0 [廃止する](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html)この機能があり、代わりにアプリケーションで数値をパディングすることをお勧めします。
