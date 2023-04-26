---
title: SQL Mode
summary: Learn SQL mode.
---

# SQL モード {#sql-mode}

TiDB サーバーはさまざまな SQL モードで動作し、これらのモードをクライアントごとに異なる方法で適用します。 SQL モードは、TiDB がサポートする SQL 構文と、実行するデータ検証チェックのタイプを定義します。以下で説明します。

TiDB の起動後、 `SET [ SESSION | GLOBAL ] sql_mode='modes'`を変更して SQL モードを設定します。

SQL モードを`GLOBAL`レベルに設定するときは、 `SUPER`特権を持っていることを確認してください。このレベルでの設定は、その後確立される接続にのみ影響します。 `SESSION`レベルでの SQL モードへの変更は、現在のクライアントにのみ影響します。

`Modes`コンマ (&#39;,&#39;) で区切られた一連の異なるモードです。 `SELECT @@sql_mode`ステートメントを使用して、現在の SQL モードを確認できます。 SQL モードのデフォルト値: `ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, NO_ENGINE_SUBSTITUTION` 。

## 重要な<code>sql_mode</code>値 {#important-code-sql-mode-code-values}

-   `ANSI` : このモードは標準 SQL に準拠します。このモードでは、データがチェックされます。データが定義された型または長さに準拠していない場合、データ型は調整または削除され、 `warning`が返されます。
-   `STRICT_TRANS_TABLES` : Strict モード。データが厳密にチェックされます。データに誤りがあると、テーブルに挿入できず、エラーが返されます。
-   `TRADITIONAL` : このモードでは、TiDB は「従来の」SQL データベース システムのように動作します。不正な値が列に挿入されると、警告ではなくエラーが返されます。次に、 `INSERT`または`UPDATE`ステートメントがすぐに停止します。

## SQL モード テーブル {#sql-mode-table}

| 名前                           | 説明                                                                                                                                                                      |
| :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PIPES_AS_CONCAT`            | 「||」を扱います`OR`としてではなく、文字列連結演算子 ( `+` ) ( `CONCAT()`と同じ) として (完全サポート)                                                                                                     |
| `ANSI_QUOTES`                | `"`識別子として扱います。 `ANSI_QUOTES`が有効な場合、一重引用符のみが文字列リテラルとして扱われ、二重引用符は識別子として扱われます。したがって、二重引用符を使用して文字列を引用することはできません。 （フルサポート）                                                   |
| `IGNORE_SPACE`               | このモードが有効な場合、システムはスペースを無視します。例: &quot;user&quot; と &quot;user &quot; は同じです。 （フルサポート）                                                                                     |
| `ONLY_FULL_GROUP_BY`         | `SELECT` 、 `HAVING` 、または`ORDER BY`で参照されている集計されていない列が`GROUP BY`に存在しない場合、 `GROUP BY`に存在しない列がクエリによって表示されるのは異常であるため、この SQL ステートメントは無効です。 （フルサポート）                           |
| `NO_UNSIGNED_SUBTRACTION`    | オペランドに減算の記号がない場合、結果を`UNSIGNED`としてマークしません。 （フルサポート）                                                                                                                      |
| `NO_DIR_IN_CREATE`           | テーブルの作成時に、 `INDEX DIRECTORY`と`DATA DIRECTORY`ディレクティブをすべて無視します。このオプションは、セカンダリ レプリケーション サーバーに対してのみ有効です (構文サポートのみ)。                                                        |
| `NO_KEY_OPTIONS`             | `SHOW CREATE TABLE`ステートメントを使用すると、 `ENGINE`などの MySQL 固有の構文はエクスポートされません。 mysqldump を使用して DB タイプ間で移行する場合は、このオプションを検討してください。 (構文サポートのみ)                                     |
| `NO_FIELD_OPTIONS`           | `SHOW CREATE TABLE`ステートメントを使用すると、 `ENGINE`などの MySQL 固有の構文はエクスポートされません。 mysqldump を使用して DB タイプ間で移行する場合は、このオプションを検討してください。 (構文サポートのみ)                                     |
| `NO_TABLE_OPTIONS`           | `SHOW CREATE TABLE`ステートメントを使用すると、 `ENGINE`などの MySQL 固有の構文はエクスポートされません。 mysqldump を使用して DB タイプ間で移行する場合は、このオプションを検討してください。 (構文サポートのみ)                                     |
| `NO_AUTO_VALUE_ON_ZERO`      | このモードが有効な場合、 `AUTO_INCREMENT`列に渡された値が`0`または特定の値の場合、システムはこの値をこの列に直接書き込みます。 `NULL`が渡されると、システムは次のシリアル番号を自動的に生成します。 （フルサポート）                                                |
| `NO_BACKSLASH_ESCAPES`       | このモードが有効な場合、 `\`バックスラッシュ記号はそれ自体のみを表します。 （フルサポート）                                                                                                                        |
| `STRICT_TRANS_TABLES`        | トランザクションstorageエンジンの厳密モードを有効にし、不正な値が挿入された後にステートメント全体をロールバックします。 （フルサポート）                                                                                                |
| `STRICT_ALL_TABLES`          | トランザクション テーブルの場合、不正な値が挿入された後、トランザクション ステートメント全体をロールバックします。 （フルサポート）                                                                                                     |
| `NO_ZERO_IN_DATE`            | 厳密モード。月または日の部分が`0`の日付は受け入れられません。 `IGNORE`オプションを使用すると、TiDB は同様の日付に「0000-00-00」を挿入します。非厳密モードでは、この日付は受け入れられますが、警告が返されます。 （フルサポート）                                          |
| `NO_ZERO_DATE`               | 厳密モードで有効な日付として「0000-00-00」を使用しません。 `IGNORE`オプションを使用してゼロの日付を挿入することもできます。非厳密モードでは、この日付は受け入れられますが、警告が返されます。 （フルサポート）                                                       |
| `ALLOW_INVALID_DATES`        | このモードでは、システムはすべての日付の有効性をチェックしません。 `1`から`12`までの月の値と`1`から`31`までの日付の値のみをチェックします。モードは`DATE`と`DATATIME`列にのみ適用されます。 `TIMESTAMP`列すべてで完全な有効性チェックが必要です。 （フルサポート）                 |
| `ERROR_FOR_DIVISION_BY_ZERO` | このモードが有効な場合、システムはデータ変更操作 ( `INSERT`または`UPDATE` ) で`0`による除算を処理するときにエラーを返します。<br/>このモードが有効になっていない場合、システムは警告を返し、代わりに`NULL`が使用されます。 （フルサポート）                                |
| `NO_AUTO_CREATE_USER`        | 指定されたパスワードを除いて、 `GRANT`が新しいユーザーを自動的に作成するのを防ぎます (完全サポート)                                                                                                                 |
| `HIGH_NOT_PRECEDENCE`        | NOT 演算子の優先順位は、 `NOT a BETWEEN b AND c`などの式が`NOT (a BETWEEN b AND c)`として解析されるようなものです。一部の古いバージョンの MySQL では、この式は`(NOT a) BETWEEN b AND c`として解析されます。 （フルサポート）               |
| `NO_ENGINE_SUBSTITUTION`     | 必要なstorageエンジンが無効になっているかコンパイルされていない場合、storageエンジンの自動置換を防ぎます。 (構文サポートのみ)                                                                                                 |
| `PAD_CHAR_TO_FULL_LENGTH`    | このモードが有効な場合、システムは`CHAR`タイプの末尾のスペースをトリムしません。 (構文サポートのみ。このモードは[MySQL 8.0 で非推奨](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_pad_char_to_full_length)です。) |
| `REAL_AS_FLOAT`              | `REAL` `DOUBLE`のシノニムではなく、 `FLOAT`のシノニムとして扱います (完全サポート)                                                                                                                  |
| `POSTGRESQL`                 | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS`と同等 (構文サポートのみ)                                           |
| `MSSQL`                      | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS`と同等 (構文サポートのみ)                                           |
| `DB2`                        | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS`と同等 (構文サポートのみ)                                           |
| `MAXDB`                      | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS` 、 `NO_AUTO_CREATE_USER`に相当 (完全サポート)                     |
| `MySQL323`                   | `NO_FIELD_OPTIONS` 、 `HIGH_NOT_PRECEDENCE`と同等 (構文サポートのみ)                                                                                                                |
| `MYSQL40`                    | `NO_FIELD_OPTIONS` 、 `HIGH_NOT_PRECEDENCE`と同等 (構文サポートのみ)                                                                                                                |
| `ANSI`                       | `REAL_AS_FLOAT` 、 `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE`と同等 (構文サポートのみ)                                                                                      |
| `TRADITIONAL`                | `STRICT_TRANS_TABLES` 、 `STRICT_ALL_TABLES` 、 `NO_ZERO_IN_DATE` 、 `NO_ZERO_DATE` 、 `ERROR_FOR_DIVISION_BY_ZERO` 、 `NO_AUTO_CREATE_USER`と同等 (構文サポートのみ)                   |
| `ORACLE`                     | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS` 、 `NO_AUTO_CREATE_USER`と同等 (構文サポートのみ)                   |
