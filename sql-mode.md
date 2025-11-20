---
title: SQL Mode
summary: SQL モードを学習します。
---

# SQLモード {#sql-mode}

TiDB サーバーは異なる SQL モードで動作し、クライアントごとに異なるモードを適用します。SQL モードは、TiDB がサポートする SQL 構文と、実行するデータ検証チェックの種類を定義します。以下に説明します。

TiDB を起動した後、 `SET [ SESSION | GLOBAL ] sql_mode='modes'`ステートメントを使用して SQL モードを設定できます。

-   SQL モードを`GLOBAL`レベルに設定するときは、権限が`SUPER`あることを確認してください。このレベルでの設定は、その後に確立される接続にのみ影響します。

-   `SESSION`レベルでの SQL モードの変更は、現在のクライアントにのみ影響します。

この文では、 `modes`カンマ (&#39;,&#39;) で区切られたモードのセットです。3 `SELECT @@sql_mode`を使用して現在のSQLモードを確認できます。SQLモードのデフォルト値は`ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, NO_ENGINE_SUBSTITUTION` 。

## 重要な<code>sql_mode</code>値 {#important-code-sql-mode-code-values}

-   `ANSI` : このモードは標準SQLに準拠しています。このモードでは、データがチェックされます。データが定義された型または長さに準拠していない場合、データ型は調整またはトリミングされ、 `warning`返されます。
-   `STRICT_TRANS_TABLES` : 厳密モード。データは厳密にチェックされます。データに誤りがある場合は、テーブルに挿入できず、エラーが返されます。
-   `TRADITIONAL` : このモードでは、TiDBは「従来の」SQLデータベースシステムのように動作します。列に不正な値が挿入された場合、警告ではなくエラーが返されます。その後、 `INSERT`または`UPDATE`ステートメントは直ちに停止されます。

## SQLモードテーブル {#sql-mode-table}

| 名前                           | 説明                                                                                                                                                                                                                                                              |
| :--------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PIPES_AS_CONCAT`            | 「||」を文字列連結演算子（ `+` ）（ `CONCAT()`と同じ）として扱い、 `OR` （完全サポート）としては扱いません。                                                                                                                                                                                              |
| `ANSI_QUOTES`                | `"`識別子として扱います。3 `ANSI_QUOTES`有効にすると、一重引用符のみが文字列リテラルとして扱われ、二重引用符は識別子として扱われます。したがって、二重引用符は文字列を引用符で囲むために使用することはできません。(完全サポート)                                                                                                                                      |
| `IGNORE_SPACE`               | このモードを有効にすると、システムはスペースを無視します。例：「user」と「user 」は同じ意味になります。（完全サポート）                                                                                                                                                                                                |
| `ONLY_FULL_GROUP_BY`         | `SELECT` 、 `HAVING` 、または`ORDER BY`列を参照するSQL文は、集計も`GROUP BY`節にも含まれず、無効です。これは、そのような列をクエリ結果に表示することが異常であるためです。この設定は、 [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-new-in-v610)システム変数の影響を受けます。(完全サポート) |
| `NO_UNSIGNED_SUBTRACTION`    | 減算においてオペランドに記号がない場合、結果を`UNSIGNED`としてマークしません。(完全サポート)                                                                                                                                                                                                            |
| `NO_DIR_IN_CREATE`           | テーブル作成時に`INDEX DIRECTORY`と`DATA DIRECTORY`ディレクティブをすべて無視します。このオプションはセカンダリレプリケーションサーバー（構文サポートのみ）でのみ有効です。                                                                                                                                                          |
| `NO_KEY_OPTIONS`             | `SHOW CREATE TABLE`文を使用すると、 `ENGINE`ような MySQL 固有の構文はエクスポートされません。mysqldump を使用してデータベースタイプ間で移行する場合は、このオプションを検討してください。(構文サポートのみ)                                                                                                                                   |
| `NO_FIELD_OPTIONS`           | `SHOW CREATE TABLE`文を使用すると、 `ENGINE`ような MySQL 固有の構文はエクスポートされません。mysqldump を使用してデータベースタイプ間で移行する場合は、このオプションを検討してください。(構文サポートのみ)                                                                                                                                   |
| `NO_TABLE_OPTIONS`           | `SHOW CREATE TABLE`文を使用すると、 `ENGINE`ような MySQL 固有の構文はエクスポートされません。mysqldump を使用してデータベースタイプ間で移行する場合は、このオプションを検討してください。(構文サポートのみ)                                                                                                                                   |
| `NO_AUTO_VALUE_ON_ZERO`      | このモードを有効にすると、 [`AUTO_INCREMENT`](/auto-increment.md)列目に渡された値が`0`または特定の値の場合、システムはその値を直接この列に書き込みます。5 `NULL`渡された場合、システムは自動的に次のシリアル番号を生成します。（フルサポート）                                                                                                                |
| `NO_BACKSLASH_ESCAPES`       | このモードを有効にすると、 `\`バックスラッシュ記号はそれ自体のみを表します。(完全サポート)                                                                                                                                                                                                                |
| `STRICT_TRANS_TABLES`        | トランザクションstorageエンジンの厳密モードを有効にし、無効な値が挿入された後にステートメント全体をロールバックします。(完全サポート)                                                                                                                                                                                         |
| `STRICT_ALL_TABLES`          | トランザクション テーブルの場合、無効な値が挿入された後にトランザクション ステートメント全体をロールバックします。(完全サポート)                                                                                                                                                                                              |
| `NO_ZERO_IN_DATE`            | 厳密モードでは、月または日が`0`である日付は受け入れられません。オプション`IGNORE`を使用すると、TiDBは類似の日付として「0000-00-00」を挿入します。非厳密モードでは、この日付は受け入れられますが、警告が返されます。(完全サポート)                                                                                                                                  |
| `NO_ZERO_DATE`               | 厳密モードでは、「0000-00-00」を有効な日付として使用しません。ただし、 `IGNORE`オプションを使用して日付を0として入力することは可能です。非厳密モードでは、この日付は受け入れられますが、警告が返されます。(完全サポート)                                                                                                                                         |
| `ALLOW_INVALID_DATES`        | このモードでは、システムはすべての日付の有効性をチェックしません。1から`1` `12`の月の値と`1`から`31`までの日の値のみをチェックします。このモードは`DATE`目と`DATATIME`列目にのみ適用されます。13列`TIMESTAMP`について完全な有効性チェックが必要です。（フルサポート）                                                                                                       |
| `ERROR_FOR_DIVISION_BY_ZERO` | このモードを有効にすると、データ変更操作 ( `INSERT`または`UPDATE` ) で`0`による除算を処理するときにエラーが返されます。<br/>このモードが有効になっていない場合、システムは警告を返し、代わりに`NULL`使用されます。(完全サポート)                                                                                                                             |
| `NO_AUTO_CREATE_USER`        | 指定されたパスワード以外で、新しいユーザーを自動的に作成すること`GRANT`防止します（完全サポート）                                                                                                                                                                                                            |
| `HIGH_NOT_PRECEDENCE`        | NOT演算子の優先順位は、 `NOT a BETWEEN b AND c`のような式は`NOT (a BETWEEN b AND c)`として解析されるというものです。MySQLの古いバージョンでは、この式は`(NOT a) BETWEEN b AND c`として解析されます。（完全サポート）                                                                                                             |
| `NO_ENGINE_SUBSTITUTION`     | 必要なstorageエンジンが無効になっているかコンパイルされていない場合は、storageエンジンの自動置き換えを防止します。(構文サポートのみ)                                                                                                                                                                                      |
| `PAD_CHAR_TO_FULL_LENGTH`    | このモードを有効にすると、システムは`CHAR`種類の末尾のスペースをトリミングしません。(構文サポートのみ。このモードは[MySQL 8.0で非推奨](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_pad_char_to_full_length)なっています。)                                                                                     |
| `REAL_AS_FLOAT`              | `REAL` `FLOAT`の同義語として扱い、 `DOUBLE`の同義語としては扱いません (完全サポート)                                                                                                                                                                                                         |
| `POSTGRESQL`                 | `PIPES_AS_CONCAT` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` `IGNORE_SPACE`構文サポート`NO_FIELD_OPTIONS` `ANSI_QUOTES`                                                                                                                                                      |
| `MSSQL`                      | `PIPES_AS_CONCAT` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` `IGNORE_SPACE`構文サポート`NO_FIELD_OPTIONS` `ANSI_QUOTES`                                                                                                                                                      |
| `DB2`                        | `PIPES_AS_CONCAT` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` `IGNORE_SPACE`構文サポート`NO_FIELD_OPTIONS` `ANSI_QUOTES`                                                                                                                                                      |
| `MAXDB`                      | `PIPES_AS_CONCAT` `NO_KEY_OPTIONS` `IGNORE_SPACE` `NO_FIELD_OPTIONS` `NO_AUTO_CREATE_USER` `NO_TABLE_OPTIONS` `ANSI_QUOTES`                                                                                                                                     |
| `MySQL323`                   | `NO_FIELD_OPTIONS`と同等（構文サポートのみ`HIGH_NOT_PRECEDENCE`                                                                                                                                                                                                             |
| `MYSQL40`                    | `NO_FIELD_OPTIONS`と同等（構文サポートのみ`HIGH_NOT_PRECEDENCE`                                                                                                                                                                                                             |
| `ANSI`                       | `REAL_AS_FLOAT` `ANSI_QUOTES`相当（構文サポート`IGNORE_SPACE` `PIPES_AS_CONCAT`                                                                                                                                                                                          |
| `TRADITIONAL`                | `STRICT_TRANS_TABLES` `NO_ZERO_DATE` `ERROR_FOR_DIVISION_BY_ZERO` `NO_ZERO_IN_DATE`構文サポート`NO_AUTO_CREATE_USER` `STRICT_ALL_TABLES`                                                                                                                              |
| `ORACLE`                     | `PIPES_AS_CONCAT` `NO_TABLE_OPTIONS` `NO_KEY_OPTIONS` `IGNORE_SPACE`構文`NO_FIELD_OPTIONS` `NO_AUTO_CREATE_USER` `ANSI_QUOTES`                                                                                                                                    |
