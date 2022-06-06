---
title: SQL Mode
summary: Learn SQL mode.
---

# SQLモード {#sql-mode}

TiDBサーバーはさまざまなSQLモードで動作し、これらのモードをクライアントごとに異なる方法で適用します。 SQLモードは、以下に説明するように、TiDBがサポートするSQL構文と、実行するデータ検証チェックのタイプを定義します。

TiDBの起動後、 `SET [ SESSION | GLOBAL ] sql_mode='modes'`を変更してSQLモードを設定します。

SQLモードを`GLOBAL`レベルで設定する場合は、 `SUPER`の特権があることを確認してください。このレベルでの設定は、後で確立される接続にのみ影響します。 `SESSION`レベルでのSQLモードへの変更は、現在のクライアントにのみ影響します。

`Modes`は、コンマ（&#39;、&#39;）で区切られた一連の異なるモードです。 `SELECT @@sql_mode`ステートメントを使用して、現在のSQLモードを確認できます。 SQLモードのデフォルト値： `ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, NO_ENGINE_SUBSTITUTION` 。

## 重要な<code>sql_mode</code>値 {#important-code-sql-mode-code-values}

-   `ANSI` ：このモードは標準SQLに準拠しています。このモードでは、データがチェックされます。データが定義されたタイプまたは長さに準拠していない場合、データタイプは調整またはトリミングされ、 `warning`が返されます。
-   `STRICT_TRANS_TABLES` ：データが厳密にチェックされる厳密モード。誤ったデータがテーブルに挿入されると、エラーが返されます。
-   `TRADITIONAL` ：このモードでは、TiDBは「従来の」SQLデータベースシステムのように動作します。誤った値が列に挿入されると、警告ではなくエラーが返されます。次に、 `INSERT`または`UPDATE`ステートメントはすぐに停止されます。

## SQLモードテーブル {#sql-mode-table}

| 名前                           | 説明                                                                                                                                                                                 |
| :--------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PIPES_AS_CONCAT`            | 「||」を扱います`OR` （完全サポート）としてではなく、文字列連結演算子（ `+` ）（ `CONCAT()`と同じ）として                                                                                                                   |
| `ANSI_QUOTES`                | `"`を識別子として扱います。 `ANSI_QUOTES`が有効になっている場合、一重引用符のみが文字列リテラルとして扱われ、二重引用符は識別子として扱われます。したがって、二重引用符を使用して文字列を引用することはできません。 （フルサポート）                                                        |
| `IGNORE_SPACE`               | このモードが有効になっている場合、システムはスペースを無視します。例：「user」と「user」は同じです。 （フルサポート）                                                                                                                    |
| `ONLY_FULL_GROUP_BY`         | `SELECT` 、または`HAVING`で参照される非集約列が`ORDER BY`に存在しない場合、このSQLステートメントは無効です。これは、列が`GROUP BY`に存在し`GROUP BY`が、クエリによって表示されるのは異常であるためです。 （フルサポート）                                             |
| `NO_UNSIGNED_SUBTRACTION`    | オペランドに減算の記号がない場合、結果を`UNSIGNED`としてマークしません。 （フルサポート）                                                                                                                                 |
| `NO_DIR_IN_CREATE`           | テーブルの作成時に、 `INDEX DIRECTORY`および`DATA DIRECTORY`のディレクティブをすべて無視します。このオプションは、セカンダリレプリケーションサーバーでのみ役立ちます（構文サポートのみ）。                                                                     |
| `NO_KEY_OPTIONS`             | `SHOW CREATE TABLE`ステートメントを使用する場合、 `ENGINE`などのMySQL固有の構文はエクスポートされません。 mysqldumpを使用してDBタイプ間で移行する場合は、このオプションを検討してください。 （構文サポートのみ）                                                    |
| `NO_FIELD_OPTIONS`           | `SHOW CREATE TABLE`ステートメントを使用する場合、 `ENGINE`などのMySQL固有の構文はエクスポートされません。 mysqldumpを使用してDBタイプ間で移行する場合は、このオプションを検討してください。 （構文サポートのみ）                                                    |
| `NO_TABLE_OPTIONS`           | `SHOW CREATE TABLE`ステートメントを使用する場合、 `ENGINE`などのMySQL固有の構文はエクスポートされません。 mysqldumpを使用してDBタイプ間で移行する場合は、このオプションを検討してください。 （構文サポートのみ）                                                    |
| `NO_AUTO_VALUE_ON_ZERO`      | このモードが有効になっている場合、 `AUTO_INCREMENT`列に渡される値が`0`または特定の値であると、システムはこの値をこの列に直接書き込みます。 `NULL`が渡されると、システムは自動的に次のシリアル番号を生成します。 （フルサポート）                                                     |
| `NO_BACKSLASH_ESCAPES`       | このモードが有効になっている場合、 `\`の円記号はそれ自体を表すだけです。 （フルサポート）                                                                                                                                    |
| `STRICT_TRANS_TABLES`        | トランザクションストレージエンジンの厳密モードを有効にし、不正な値が挿入された後、ステートメント全体をロールバックします。 （フルサポート）                                                                                                             |
| `STRICT_ALL_TABLES`          | トランザクションテーブルの場合、不正な値が挿入された後、トランザクションステートメント全体をロールバックします。 （フルサポート）                                                                                                                  |
| `NO_ZERO_IN_DATE`            | 月または日の部分が`0`の日付は受け入れられない厳密モード。 `IGNORE`オプションを使用する場合、TiDBは同様の日付に「0000-00-00」を挿入します。非厳密モードでは、この日付は受け入れられますが、警告が返されます。 （フルサポート）                                                       |
| `NO_ZERO_DATE`               | 厳密モードでは、有効な日付として「0000-00-00」を使用しません。 `IGNORE`オプションを使用しても、ゼロの日付を挿入できます。非厳密モードでは、この日付は受け入れられますが、警告が返されます。 （フルサポート）                                                                   |
| `ALLOW_INVALID_DATES`        | このモードでは、システムはすべての日付の有効性をチェックしません。 `1`から`12`の範囲の月の値と`1`から`31`の範囲の日付の値のみをチェックします。このモードは、 `DATE`列と`DATATIME`列にのみ適用されます。 `TIMESTAMP`列すべてに完全な妥当性チェックが必要です。 （フルサポート）                     |
| `ERROR_FOR_DIVISION_BY_ZERO` | このモードが有効になっている場合、データ変更操作（ `INSERT`または`UPDATE` ）で`0`による除算を処理すると、システムはエラーを返します。<br/>このモードが有効になっていない場合、システムは警告を返し、代わりに`NULL`が使用されます。 （フルサポート）                                         |
| `NO_AUTO_CREATE_USER`        | 指定されたパスワードを除いて、 `GRANT`が新しいユーザーを自動的に作成しないようにします（完全サポート）                                                                                                                            |
| `HIGH_NOT_PRECEDENCE`        | NOT演算子の優先順位は、 `NOT a BETWEEN b AND c`などの式が`NOT (a BETWEEN b AND c)`として解析されるようなものです。 MySQLの一部の古いバージョンでは、この式は`(NOT a) BETWEEN b AND c`として解析されます。 （フルサポート）                            |
| `NO_ENGINE_SUBSTITUTION`     | 必要なストレージエンジンが無効になっているか、コンパイルされていない場合に、ストレージエンジンが自動的に置き換えられないようにします。 （構文サポートのみ）                                                                                                     |
| `PAD_CHAR_TO_FULL_LENGTH`    | このモードが有効になっている場合、システムは`CHAR`のタイプの末尾のスペースをトリミングしません。 （構文サポートのみ。このモードは[MySQL8.0で非推奨](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_pad_char_to_full_length)になっています。） |
| `REAL_AS_FLOAT`              | `REAL`を`DOUBLE`の同義語ではなく、 `FLOAT`の同義語として扱います（完全サポート）                                                                                                                                |
| `POSTGRESQL`                 | `PIPES_AS_CONCAT` `NO_FIELD_OPTIONS` `ANSI_QUOTES` （ `IGNORE_SPACE` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` ）                                                                          |
| `MSSQL`                      | `PIPES_AS_CONCAT` `NO_FIELD_OPTIONS` `ANSI_QUOTES` （ `IGNORE_SPACE` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` ）                                                                          |
| `DB2`                        | `PIPES_AS_CONCAT` `NO_FIELD_OPTIONS` `ANSI_QUOTES` （ `IGNORE_SPACE` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` ）                                                                          |
| `MAXDB`                      | `PIPES_AS_CONCAT` `NO_TABLE_OPTIONS` `ANSI_QUOTES` `NO_FIELD_OPTIONS` `IGNORE_SPACE` `NO_KEY_OPTIONS` `NO_AUTO_CREATE_USER`                                                        |
| `MySQL323`                   | `NO_FIELD_OPTIONS`に`HIGH_NOT_PRECEDENCE` （構文サポートのみ）                                                                                                                                |
| `MYSQL40`                    | `NO_FIELD_OPTIONS`に`HIGH_NOT_PRECEDENCE` （構文サポートのみ）                                                                                                                                |
| `ANSI`                       | `REAL_AS_FLOAT`に`PIPES_AS_CONCAT` （ `ANSI_QUOTES` `IGNORE_SPACE`のみ）                                                                                                                |
| `TRADITIONAL`                | `STRICT_TRANS_TABLES` `NO_AUTO_CREATE_USER` `STRICT_ALL_TABLES` （ `NO_ZERO_IN_DATE` `NO_ZERO_DATE` `ERROR_FOR_DIVISION_BY_ZERO` ）                                                  |
| `ORACLE`                     | `PIPES_AS_CONCAT` `NO_FIELD_OPTIONS` `ANSI_QUOTES` `NO_AUTO_CREATE_USER` `IGNORE_SPACE` `NO_KEY_OPTIONS` `NO_TABLE_OPTIONS` ）                                                      |
