---
title: MySQL Compatibility
summary: Learn about the compatibility of TiDB with MySQL, and the unsupported and different features.
---

# MySQL の互換性 {#mysql-compatibility}

TiDB は、 MySQL 5.7プロトコル、およびMySQL 5.7の共通機能および構文と高い互換性があります。 MySQL 5.7のエコシステム ツール (PHPMyAdmin、Navicat、MySQL Workbench、mysqldump、および Mydumper/myloader) および MySQL クライアントを TiDB に使用できます。

ただし、MySQL の一部の機能はサポートされていません。これは、問題を解決するためのより良い方法 (JSON に置き換わる XML関数など) が存在するか、必要な労力に対して現在の需要が不足している (ストアド プロシージャや関数など) ことが考えられます。一部の機能は、分散システムとして実装するのが難しい場合もあります。

<CustomContent platform="tidb">

さらに、TiDB は MySQL レプリケーション プロトコルをサポートしませんが、MySQL でデータをレプリケートするための特定のツールを提供します。

-   MySQL からのデータの複製: [<a href="/dm/dm-overview.md">TiDB データ移行 (DM)</a>](/dm/dm-overview.md) 、MySQL/MariaDB から TiDB への完全なデータ移行と増分データ複製をサポートするツールです。
-   MySQL へのデータの複製: [<a href="/ticdc/ticdc-overview.md">TiCDC</a>](/ticdc/ticdc-overview.md) TiKV 変更ログをプルすることで TiDB の増分データを複製するためのツールです。 TiCDC は[<a href="/ticdc/ticdc-overview.md#replication-consistency">MySQLシンク</a>](/ticdc/ticdc-overview.md#replication-consistency)使用して、TiDB の増分データを MySQL にレプリケートします。

</CustomContent>

<CustomContent platform="tidb">

> **ノート：**
>
> このページでは、MySQL と TiDB の一般的な違いについて説明します。 [<a href="/security-compatibility-with-mysql.md">Security</a>](/security-compatibility-with-mysql.md)と[<a href="/pessimistic-transaction.md#difference-with-mysql-innodb">悲観的トランザクションモード</a>](/pessimistic-transaction.md#difference-with-mysql-innodb)の互換性については専用ページを参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> MySQL と TiDB のトランザクションの違いについては、 [<a href="/pessimistic-transaction.md#difference-with-mysql-innodb">悲観的トランザクションモード</a>](/pessimistic-transaction.md#difference-with-mysql-innodb)を参照してください。

</CustomContent>

## サポートされていない機能 {#unsupported-features}

-   ストアド プロシージャと関数
-   トリガー
-   イベント
-   ユーザー定義関数
-   `FULLTEXT`構文とインデックス[<a href="https://github.com/pingcap/tidb/issues/1793">#1793</a>](https://github.com/pingcap/tidb/issues/1793)
-   `SPATIAL` ( `GIS` / `GEOMETRY`とも呼ばれる)関数、データ型、インデックス[<a href="https://github.com/pingcap/tidb/issues/6347">#6347</a>](https://github.com/pingcap/tidb/issues/6347)
-   `ascii` 、 `latin1` 、 `binary` 、 `utf8` 、 `utf8mb4` 、および`gbk`以外の文字セット。
-   SYSスキーマ
-   オプティマイザートレース
-   XML関数
-   Xプロトコル[<a href="https://github.com/pingcap/tidb/issues/1109">#1109</a>](https://github.com/pingcap/tidb/issues/1109)
-   列レベルの権限[<a href="https://github.com/pingcap/tidb/issues/9766">#9766</a>](https://github.com/pingcap/tidb/issues/9766)
-   `XA`構文 (TiDB は内部的に 2 フェーズ コミットを使用しますが、これは SQL インターフェイス経由では公開されません)
-   `CREATE TABLE tblName AS SELECT stmt`構文[<a href="https://github.com/pingcap/tidb/issues/4754">#4754</a>](https://github.com/pingcap/tidb/issues/4754)
-   `CHECK TABLE`構文[<a href="https://github.com/pingcap/tidb/issues/4673">#4673</a>](https://github.com/pingcap/tidb/issues/4673)
-   `CHECKSUM TABLE`構文[<a href="https://github.com/pingcap/tidb/issues/1895">#1895</a>](https://github.com/pingcap/tidb/issues/1895)
-   `REPAIR TABLE`の構文
-   `OPTIMIZE TABLE`の構文
-   `HANDLER`ステートメント
-   `CREATE TABLESPACE`ステートメント
-   「セッション トラッカー: GTID コンテキストを OK パケットに追加」

## MySQL と異なる機能 {#features-that-are-different-from-mysql}

### 自動インクリメントID {#auto-increment-id}

-   TiDB では、自動インクリメンタル列の値 (ID) はグローバルに一意です。これらは単一の TiDBサーバー上で増分されます。複数の TiDB サーバー間で ID を増分したい場合は、 [<a href="/auto-increment.md#mysql-compatibility-mode">`AUTO_INCREMENT` MySQL 互換モード</a>](/auto-increment.md#mysql-compatibility-mode)を使用できます。ただし、ID は必ずしも連続して割り当てられる必要はありません。デフォルト値とカスタム値を混合しないことをお勧めします。そうしないと、 `Duplicated Error`エラー メッセージが表示される可能性があります。

-   `tidb_allow_remove_auto_inc`システム変数を使用して、 `AUTO_INCREMENT`列属性の削除を許可または禁止できます。列属性を削除する構文は`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`です。

-   TiDB は`AUTO_INCREMENT`列属性の追加をサポートしておらず、この属性は削除されると回復できません。

-   TiDB v6.6.0 以前のバージョンの場合、TiDB は MySQL InnoDB と同じように動作します。これには、自動インクリメント列が主キーまたはインデックス プレフィックスである必要があります。 v7.0.0 以降、TiDB では、自動インクリメント列はインデックスまたはインデックス プレフィックスでなければならないという制限が削除され、テーブルの主キーをより柔軟に定義できるようになりました。 [<a href="https://github.com/pingcap/tidb/issues/40580">#40580</a>](https://github.com/pingcap/tidb/issues/40580)

詳細については、 [<a href="/auto-increment.md">`AUTO_INCREMENT`</a>](/auto-increment.md)を参照してください。

> **ノート：**
>
> -   テーブルの作成時に主キーを指定しなかった場合、TiDB は`_tidb_rowid`を使用して行を識別します。この値の割り当ては、自動インクリメント列 (そのような列が存在する場合) とアロケーターを共有します。自動インクリメント列を主キーとして指定すると、TiDB はこの列を使用して行を識別します。この状況では、次の状況が発生する可能性があります。

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

ご覧のとおり、共有アロケーターにより、 `id`は毎回 2 ずつ増加します。この動作は[<a href="/auto-increment.md#mysql-compatibility-mode">MySQL互換モード</a>](/auto-increment.md#mysql-compatibility-mode)で変更され、共有アロケータがないため、数値のスキップは行われません。

<CustomContent platform="tidb">

> **ノート：**
>
> `AUTO_INCREMENT`属性は、本番環境でホットスポットを引き起こす可能性があります。詳細は[<a href="/troubleshoot-hot-spot-issues.md">ホットスポットの問題のトラブルシューティング</a>](/troubleshoot-hot-spot-issues.md)参照してください。代わりに[<a href="/auto-random.md">`AUTO_RANDOM`</a>](/auto-random.md)を使用することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> `AUTO_INCREMENT`属性は、本番環境でホットスポットを引き起こす可能性があります。詳細は[<a href="https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random">ホットスポットの問題のトラブルシューティング</a>](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)参照してください。代わりに[<a href="/auto-random.md">`AUTO_RANDOM`</a>](/auto-random.md)を使用することをお勧めします。

</CustomContent>

### パフォーマンススキーマ {#performance-schema}

<CustomContent platform="tidb">

TiDB は、 [<a href="/tidb-monitoring-api.md">プロメテウスとグラファナ</a>](/tidb-monitoring-api.md)の組み合わせを使用して、パフォーマンス監視メトリクスを保存およびクエリします。パフォーマンス スキーマ テーブルは、TiDB で空の結果を返します。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB Cloudのパフォーマンス メトリックを確認するには、 TiDB Cloudコンソールのクラスター概要ページを確認するか、 [<a href="/tidb-cloud/third-party-monitoring-integrations.md">サードパーティの監視統合</a>](/tidb-cloud/third-party-monitoring-integrations.md)を使用します。パフォーマンス スキーマ テーブルは、TiDB で空の結果を返します。

</CustomContent>

### クエリ実行計画 {#query-execution-plan}

TiDB におけるクエリ実行プラン ( `EXPLAIN` / `EXPLAIN FOR` ) の出力形式、出力内容、権限設定は MySQL とは大きく異なります。

MySQL システム変数`optimizer_switch` TiDB では読み取り専用であり、クエリ プランには影響しません。 MySQL と同様の構文で[<a href="/optimizer-hints.md">オプティマイザーのヒント</a>](/optimizer-hints.md)使用することもできますが、利用可能なヒントと実装が異なる場合があります。

詳細については[<a href="/explain-overview.md">クエリ実行計画を理解する</a>](/explain-overview.md)参照してください。

### 内蔵関数 {#built-in-functions}

TiDB は、ほとんどの MySQL 組み込み関数をサポートしていますが、すべてではありません。ステートメント`SHOW BUILTINS`は、使用可能な関数のリストを提供します。

[<a href="https://pingcap.github.io/sqlgram/#functioncallkeyword">TiDB SQL文法</a>](https://pingcap.github.io/sqlgram/#functioncallkeyword)も参照してください。

### DDL {#ddl}

TiDB では、サポートされているすべての DDL 変更はオンラインで実行されます。 MySQL の DDL 操作と比較して、TiDB の DDL 操作には次のような大きな制限があります。

-   単一の`ALTER TABLE`ステートメントを使用してテーブルの複数のスキーマ オブジェクト (列やインデックスなど) を変更する場合、複数の変更で同じオブジェクトを指定することはサポートされません。たとえば、 `ALTER TABLE t1 MODIFY COLUMN c1 INT, DROP COLUMN c1`コマンドを実行すると、 `Unsupported operate same column/index`エラーが出力されます。
-   `TIFLASH REPLICA` 、 `SHARD_ROW_ID_BITS` 、 `AUTO_ID_CACHE`などの単一の`ALTER TABLE`ステートメントを使用して複数の TiDB 固有のスキーマ オブジェクトを変更することはサポートされていません。
-   TiDB の`ALTER TABLE`は、一部のデータ型の変更をサポートしていません。たとえば、TiDB は`DECIMAL`タイプから`DATE`タイプへの変更をサポートしていません。データ型の変更がサポートされていない場合、TiDB は`Unsupported modify column: type %d not match origin %d`エラーを報告します。詳細については[<a href="/sql-statements/sql-statement-modify-column.md">`ALTER TABLE`</a>](/sql-statements/sql-statement-modify-column.md)を参照してください。
-   `ALGORITHM={INSTANT,INPLACE,COPY}`構文は TiDB のアサーションとしてのみ関数、 `ALTER`アルゴリズムは変更しません。詳細については、 [<a href="/sql-statements/sql-statement-alter-table.md">`ALTER TABLE`</a>](/sql-statements/sql-statement-alter-table.md)参照してください。
-   `CLUSTERED`タイプの主キーの追加/削除はサポートされていません。 `CLUSTERED`種類の主キーの詳細については、 [<a href="/clustered-indexes.md">クラスター化インデックス</a>](/clustered-indexes.md)を参照してください。
-   異なるタイプのインデックス ( `HASH|BTREE|RTREE|FULLTEXT` ) はサポートされていないため、指定しても解析され無視されます。
-   TiDB は、 `HASH` 、 `RANGE` 、 `LIST` 、および`KEY`パーティション化タイプをサポートします。現在、 `KEY`パーティション タイプは、空のパーティション列リストを含むパーティション ステートメントをサポートしていません。サポートされていないパーティション タイプの場合、TiDB は`Warning: Unsupported partition type %s, treat as normal table`を返します。ここで`%s` 、サポートされていない特定のパーティション タイプです。
-   Range、Range COLUMNS、List、および List COLUMNS パーティション テーブルは、 `ADD` 、 `DROP` 、 `TRUNCATE` 、および`REORGANIZE`操作をサポートします。他のパーティション操作は無視されます。
-   ハッシュおよびキー パーティション テーブルは、 `ADD` 、 `COALESCE` 、および`TRUNCATE`操作をサポートします。他のパーティション操作は無視されます。
-   次の構文はパーティション テーブルではサポートされていません。

    -   `SUBPARTITION`
    -   `{CHECK|OPTIMIZE|REPAIR|IMPORT|DISCARD|REBUILD} PARTITION`

    詳細については、 [<a href="/partitioned-table.md">パーティショニング</a>](/partitioned-table.md)を参照してください。

### 分析テーブル {#analyze-table}

[<a href="/statistics.md#manual-collection">統計収集</a>](/statistics.md#manual-collection)は、MySQL とは異なり TiDB で動作します。MySQL/InnoDB では比較的軽量で有効期間が短い操作ですが、TiDB ではテーブルの統計を完全に再構築するため、完了までにはるかに時間がかかることがあります。

これらの違いについては、 [<a href="/sql-statements/sql-statement-analyze-table.md">`ANALYZE TABLE`</a>](/sql-statements/sql-statement-analyze-table.md)で詳しく説明します。

### <code>SELECT</code>構文の制限事項 {#limitations-of-code-select-code-syntax}

-   構文`SELECT ... INTO @variable`はサポートされていません。
-   構文`SELECT ... GROUP BY ... WITH ROLLUP`はサポートされていません。
-   MySQL 5.7のように、構文`SELECT .. GROUP BY expr` `GROUP BY expr ORDER BY expr`を意味しません。

詳細については、 [<a href="/sql-statements/sql-statement-select.md">`SELECT`</a>](/sql-statements/sql-statement-select.md)ステートメントのリファレンスを参照してください。

### <code>UPDATE</code>ステートメント {#code-update-code-statement}

[<a href="/sql-statements/sql-statement-update.md">`UPDATE`</a>](/sql-statements/sql-statement-update.md)ステートメントのリファレンスを参照してください。

### ビュー {#views}

TiDB のビューは更新できません。 `UPDATE` 、 `INSERT` 、 `DELETE`などの書き込み操作はサポートされていません。

### 一時テーブル {#temporary-tables}

詳細は[<a href="/temporary-tables.md#compatibility-with-mysql-temporary-tables">TiDB ローカル一時テーブルと MySQL 一時テーブル間の互換性</a>](/temporary-tables.md#compatibility-with-mysql-temporary-tables)を参照してください。

### 文字セットと照合順序 {#character-sets-and-collations}

-   TiDB でサポートされる文字セットと照合順序の詳細については、 [<a href="/character-set-and-collation.md">文字セットと照合順序の概要</a>](/character-set-and-collation.md)を参照してください。

-   GBK 文字セットの MySQL 互換性については、 [<a href="/character-set-gbk.md#mysql-compatibility">GBKの互換性</a>](/character-set-gbk.md#mysql-compatibility)を参照してください。

-   TiDB は、テーブルで使用されている文字セットを各国語文字セットとして継承します。

### ストレージエンジン {#storage-engines}

互換性の理由から、TiDB は代替storageエンジンを使用してテーブルを作成する構文をサポートしています。実装では、TiDB はメタデータを InnoDBstorageエンジンとして記述します。

<CustomContent platform="tidb">

TiDB は MySQL と同様のstorageエンジンの抽象化をサポートしますが、TiDBサーバーの起動時に[<a href="/command-line-flags-for-tidb-configuration.md#--store">`--store`</a>](/command-line-flags-for-tidb-configuration.md#--store)オプションを使用してstorageエンジンを指定する必要があります。

</CustomContent>

### SQLモード {#sql-modes}

TiDB はほとんどの[<a href="/sql-mode.md">SQLモード</a>](/sql-mode.md)をサポートします:

-   `Oracle`や`PostgreSQL`などの互換モードは解析されますが、無視されます。互換モードはMySQL 5.7で非推奨となり、MySQL 8.0 では削除されました。
-   `ONLY_FULL_GROUP_BY`モードにはMySQL 5.7のマイナー[<a href="/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql">意味上の違い</a>](/functions-and-operators/aggregate-group-by-functions.md#differences-from-mysql)があります。
-   MySQL の`NO_DIR_IN_CREATE`および`NO_ENGINE_SUBSTITUTION` SQL モードは互換性のために受け入れられていますが、TiDB には適用できません。

### デフォルトの違い {#default-differences}

-   デフォルトの文字セット:
    -   TiDB のデフォルト値は`utf8mb4`です。
    -   MySQL 5.7のデフォルト値は`latin1`です。
    -   MySQL 8.0 のデフォルト値は`utf8mb4`です。
-   デフォルトの照合順序:
    -   TiDB のデフォルトの照合順序`utf8mb4`は`utf8mb4_bin`です。
    -   MySQL 5.7のデフォルトの照合順序`utf8mb4`は`utf8mb4_general_ci`です。
    -   MySQL 8.0 のデフォルトの照合順序`utf8mb4`は`utf8mb4_0900_ai_ci`です。
-   デフォルトの SQL モード:
    -   TiDB のデフォルト SQL モードには`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`のモードが含まれます。
    -   MySQL のデフォルトの SQL モード:
        -   MySQL 5.7のデフォルトの SQL モードは TiDB と同じです。
        -   MySQL 8.0 のデフォルトの SQL モードには`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`のモードが含まれます。
-   デフォルト値`lower_case_table_names` :
    -   TiDB のデフォルト値は`2`で、現在 TiDB は`2`のみをサポートしています。
    -   MySQL のデフォルト値:
        -   Linux の場合: `0` .これは、テーブル名とデータベース名が、 `CREATE TABLE`または`CREATE DATABASE`ステートメントで指定された大文字と小文字を使用してディスクに保存されることを意味します。名前の比較では大文字と小文字が区別されます。
        -   Windows の場合: `1` .これは、テーブル名がディスク上に小文字で保存され、名前の比較では大文字と小文字が区別されないことを意味します。 MySQL は、storageおよび検索時にすべてのテーブル名を小文字に変換します。この動作は、データベース名とテーブルの別名にも適用されます。
        -   macOS の場合: `2` .これは、テーブル名とデータベース名が`CREATE TABLE`または`CREATE DATABASE`ステートメントで指定された大文字を使用してディスクに保存されますが、MySQL は検索時にそれらを小文字に変換することを意味します。名前の比較では大文字と小文字は区別されません。
-   デフォルト値`explicit_defaults_for_timestamp` :
    -   TiDB のデフォルト値は`ON`で、現在 TiDB は`ON`のみをサポートしています。
    -   MySQL のデフォルト値:
        -   MySQL 5.7の場合: `OFF` 。
        -   MySQL 8.0 の場合: `ON` .

### 日時 {#date-and-time}

#### 名前付きタイムゾーン {#named-timezone}

-   TiDB は、現在システムにインストールされているすべてのタイム ゾーン ルールを計算に使用します (通常は`tzdata`パッケージ)。タイム ゾーン テーブル データをインポートしなくても、すべてのタイム ゾーン名を使用できます。タイムゾーンテーブルデータをインポートして計算ルールを変更することはできません。
-   MySQL はデフォルトでローカル タイム ゾーンを使用し、計算にはシステムに組み込まれている現在のタイム ゾーン ルール (夏時間の開始時期など) に依存します。また、タイム ゾーンは[<a href="https://dev.mysql.com/doc/refman/5.7/en/time-zone-support.html#time-zone-installation">タイムゾーンテーブルデータのインポート</a>](https://dev.mysql.com/doc/refman/5.7/en/time-zone-support.html#time-zone-installation)なしのタイム ゾーン名で指定できません。

### 型システムの違い {#type-system-differences}

次の列タイプは MySQL ではサポートされていますが、TiDB ではサポート**されていません**。

-   FLOAT4/FLOAT8
-   `SQL_TSI_*` (SQL_TSI_MONTH、SQL_TSI_WEEK、SQL_TSI_DAY、SQL_TSI_HOUR、SQL_TSI_MINUTE、および SQL_TSI_SECOND を含む、SQL_TSI_YEAR を除く)

### 非推奨の機能による非互換性 {#incompatibility-caused-by-deprecated-features}

TiDB は、MySQL で非推奨としてマークされている次のような特定の機能を実装していません。

-   浮動小数点型の精度を指定します。 MySQL 8.0 [<a href="https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html">廃止される</a>](https://dev.mysql.com/doc/refman/8.0/en/floating-point-types.html)この機能があり、代わりに`DECIMAL`タイプを使用することをお勧めします。
-   `ZEROFILL`の属性。 MySQL 8.0 [<a href="https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html">廃止される</a>](https://dev.mysql.com/doc/refman/8.0/en/numeric-type-attributes.html)この機能が使用されるため、代わりにアプリケーション内で数値を埋め込むことをお勧めします。

### <code>CREATE RESOURCE GROUP</code> 、 <code>DROP RESOURCE GROUP</code> 、および<code>ALTER RESOURCE GROUP</code>ステートメント {#code-create-resource-group-code-code-drop-resource-group-code-and-code-alter-resource-group-code-statements}

リソース グループの作成、変更、削除のステートメントでは、サポートされるパラメーターが MySQL のパラメーターとは異なります。詳細については、次のドキュメントを参照してください。

-   [<a href="/sql-statements/sql-statement-create-resource-group.md">`CREATE RESOURCE GROUP`</a>](/sql-statements/sql-statement-create-resource-group.md)
-   [<a href="/sql-statements/sql-statement-drop-resource-group.md">`DROP RESOURCE GROUP`</a>](/sql-statements/sql-statement-drop-resource-group.md)
-   [<a href="/sql-statements/sql-statement-alter-resource-group.md">`ALTER RESOURCE GROUP`</a>](/sql-statements/sql-statement-alter-resource-group.md)
