---
title: SQL Mode
summary: SQL モードを学習します。
---

# SQL モード {#sql-mode}

TiDB サーバーはさまざまな SQL モードで動作し、クライアントごとに異なるモードでこれらのモードを適用します。SQL モードは、以下に示すように、TiDB がサポートする SQL 構文と実行するデータ検証チェックの種類を定義します。

TiDB を起動した後、 `SET [ SESSION | GLOBAL ] sql_mode='modes'`ステートメントを使用して SQL モードを設定できます。

-   SQL モードを`GLOBAL`レベルに設定するときは、権限が`SUPER`あることを確認してください。このレベルでの設定は、その後に確立される接続にのみ影響します。

-   `SESSION`レベルでの SQL モードの変更は、現在のクライアントにのみ影響します。

このステートメントでは、 `modes`カンマ (&#39;,&#39;) で区切られたモードのセットです。3 ステートメントを使用して、現在の SQL モードを`SELECT @@sql_mode`できます。SQL モードのデフォルト値: `ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, NO_ENGINE_SUBSTITUTION` 。

## 重要な<code>sql_mode</code>値 {#important-code-sql-mode-code-values}

-   `ANSI` : このモードは標準 SQL に準拠しています。このモードでは、データがチェックされます。データが定義されたタイプまたは長さに準拠していない場合、データ型が調整またはトリミングされ、 `warning`が返されます。
-   `STRICT_TRANS_TABLES` : 厳密モード。データが厳密にチェックされます。データに誤りがある場合は、テーブルに挿入できず、エラーが返されます。
-   `TRADITIONAL` : このモードでは、TiDB は「従来の」SQL データベース システムのように動作します。列に不正な値が挿入されると、警告ではなくエラーが返されます。その後、 `INSERT`または`UPDATE`ステートメントは直ちに停止されます。

## SQL モード テーブル {#sql-mode-table}

| 名前                           | 説明                                                                                                                                                                                                                                                                     |
| :--------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PIPES_AS_CONCAT`            | 「||」を文字列連結演算子（ `+` ）（ `CONCAT()`と同じ）として扱い、 `OR` （完全サポート）としては扱いません。                                                                                                                                                                                                     |
| `ANSI_QUOTES`                | `"`識別子として扱います。3 `ANSI_QUOTES`有効にすると、一重引用符のみが文字列リテラルとして扱われ、二重引用符は識別子として扱われます。したがって、二重引用符は文字列を引用するのに使用できません。(完全サポート)                                                                                                                                                     |
| `IGNORE_SPACE`               | このモードを有効にすると、システムはスペースを無視します。たとえば、「user」と「user 」は同じです。(完全サポート)                                                                                                                                                                                                         |
| `ONLY_FULL_GROUP_BY`         | `SELECT` 、 `HAVING` 、または`ORDER BY`列を参照する SQL 文は、集計も`GROUP BY`句にも含まれていない場合は無効です。これは、クエリ結果にそのような列を表示することが異常であるためです。この設定は、 [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-new-in-v610)システム変数の影響を受けます。(フルサポート) |
| `NO_UNSIGNED_SUBTRACTION`    | 減算時にオペランドに記号がない場合、結果を`UNSIGNED`としてマークしません。(完全サポート)                                                                                                                                                                                                                     |
| `NO_DIR_IN_CREATE`           | テーブルの作成時に、 `INDEX DIRECTORY`と`DATA DIRECTORY`のすべてのディレクティブを無視します。このオプションは、セカンダリ レプリケーション サーバーにのみ有効です (構文サポートのみ)                                                                                                                                                         |
| `NO_KEY_OPTIONS`             | `SHOW CREATE TABLE`ステートメントを使用すると、 `ENGINE`などの MySQL 固有の構文はエクスポートされません。mysqldump を使用して DB タイプ間で移行する場合は、このオプションを検討してください。(構文サポートのみ)                                                                                                                                      |
| `NO_FIELD_OPTIONS`           | `SHOW CREATE TABLE`ステートメントを使用すると、 `ENGINE`などの MySQL 固有の構文はエクスポートされません。mysqldump を使用して DB タイプ間で移行する場合は、このオプションを検討してください。(構文サポートのみ)                                                                                                                                      |
| `NO_TABLE_OPTIONS`           | `SHOW CREATE TABLE`ステートメントを使用すると、 `ENGINE`などの MySQL 固有の構文はエクスポートされません。mysqldump を使用して DB タイプ間で移行する場合は、このオプションを検討してください。(構文サポートのみ)                                                                                                                                      |
| `NO_AUTO_VALUE_ON_ZERO`      | このモードを有効にすると、 [`AUTO_INCREMENT`](/auto-increment.md)列に渡された値が`0`または特定の値の場合、システムはこの値を直接この列に書き込みます。5 `NULL`渡されると、システムは次のシリアル番号を自動的に生成します。(フルサポート)                                                                                                                         |
| `NO_BACKSLASH_ESCAPES`       | このモードを有効にすると、 `\`バックスラッシュ記号はそれ自体のみを表します。(完全サポート)                                                                                                                                                                                                                       |
| `STRICT_TRANS_TABLES`        | トランザクションstorageエンジンの厳密モードを有効にし、不正な値が挿入された後にステートメント全体をロールバックします。(完全サポート)                                                                                                                                                                                                |
| `STRICT_ALL_TABLES`          | トランザクション テーブルの場合、不正な値が挿入された後にトランザクション ステートメント全体をロールバックします。(完全サポート)                                                                                                                                                                                                     |
| `NO_ZERO_IN_DATE`            | 厳密モードでは、月または日の部分が`0`の日付は受け入れられません。3 オプションを使用すると、TiDB は同様の日付として &#39;0000-00-00&#39; を挿入します。非厳密モードでは、この日付は受け入れ`IGNORE`ますが、警告が返されます。(完全サポート)                                                                                                                             |
| `NO_ZERO_DATE`               | 厳密モードでは`IGNORE` &#39;0000-00-00&#39; を有効な日付として使用しません。1 オプションを使用して、日付ゼロを挿入することはできます。非厳密モードでは、この日付は受け入れられますが、警告が返されます。(完全サポート)                                                                                                                                           |
| `ALLOW_INVALID_DATES`        | このモードでは、システムはすべての日付の有効性をチェックしません。 `1`から`12`までの月の値と`1`から`31`までの日付の値のみをチェックします。 このモードは`DATE`と`DATATIME`列にのみ適用されます。 `TIMESTAMP`列すべてで完全な有効性チェックが必要です。 (完全サポート)                                                                                                             |
| `ERROR_FOR_DIVISION_BY_ZERO` | このモードを有効にすると、データ変更操作 ( `INSERT`または`UPDATE` ) で`0`による除算を処理するときにエラーが返されます。<br/>このモードが有効になっていない場合、システムは警告を返し、代わりに`NULL`が使用されます。(完全サポート)                                                                                                                                   |
| `NO_AUTO_CREATE_USER`        | 指定されたパスワードを除いて、 `GRANT`新しいユーザーを自動的に作成するのを防ぎます (完全サポート)                                                                                                                                                                                                                 |
| `HIGH_NOT_PRECEDENCE`        | NOT 演算子の優先順位は、 `NOT a BETWEEN b AND c`などの式が`NOT (a BETWEEN b AND c)`として解析されるというものです。MySQL の古いバージョンでは、この式は`(NOT a) BETWEEN b AND c`として解析されます。(完全サポート)                                                                                                                   |
| `NO_ENGINE_SUBSTITUTION`     | 必要なstorageエンジンが無効になっているかコンパイルされていない場合は、storageエンジンの自動置換を防止します。(構文サポートのみ)                                                                                                                                                                                               |
| `PAD_CHAR_TO_FULL_LENGTH`    | このモードを有効にすると、システムは`CHAR`種類の末尾のスペースをトリミングしません。(構文サポートのみ。このモードは[MySQL 8.0 では非推奨](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_pad_char_to_full_length)です。)                                                                                              |
| `REAL_AS_FLOAT`              | `REAL` `FLOAT`の同義語として扱い、 `DOUBLE`の同義語としては扱いません (完全サポート)                                                                                                                                                                                                                |
| `POSTGRESQL`                 | `PIPES_AS_CONCAT` `ANSI_QUOTES`相当`NO_FIELD_OPTIONS` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` `IGNORE_SPACE` ）                                                                                                                                                               |
| `MSSQL`                      | `PIPES_AS_CONCAT` `ANSI_QUOTES`相当`NO_FIELD_OPTIONS` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` `IGNORE_SPACE` ）                                                                                                                                                               |
| `DB2`                        | `PIPES_AS_CONCAT` `ANSI_QUOTES`相当`NO_FIELD_OPTIONS` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` `IGNORE_SPACE` ）                                                                                                                                                               |
| `MAXDB`                      | `PIPES_AS_CONCAT` `ANSI_QUOTES` `NO_TABLE_OPTIONS` `NO_AUTO_CREATE_USER` `IGNORE_SPACE` `NO_FIELD_OPTIONS` `NO_KEY_OPTIONS`                                                                                                                                            |
| `MySQL323`                   | `NO_FIELD_OPTIONS` `HIGH_NOT_PRECEDENCE`同等（構文サポートのみ）                                                                                                                                                                                                                   |
| `MYSQL40`                    | `NO_FIELD_OPTIONS` `HIGH_NOT_PRECEDENCE`同等（構文サポートのみ）                                                                                                                                                                                                                   |
| `ANSI`                       | `REAL_AS_FLOAT` `PIPES_AS_CONCAT`相当（ `ANSI_QUOTES` `IGNORE_SPACE`のみ）                                                                                                                                                                                                   |
| `TRADITIONAL`                | `STRICT_TRANS_TABLES` `STRICT_ALL_TABLES`相当`NO_AUTO_CREATE_USER` `NO_ZERO_DATE` `ERROR_FOR_DIVISION_BY_ZERO` `NO_ZERO_IN_DATE` ）                                                                                                                                       |
| `ORACLE`                     | `PIPES_AS_CONCAT` `ANSI_QUOTES`相当`NO_AUTO_CREATE_USER` `NO_TABLE_OPTIONS` `NO_FIELD_OPTIONS` `IGNORE_SPACE` `NO_KEY_OPTIONS`                                                                                                                                           |
