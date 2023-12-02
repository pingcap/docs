---
title: SQL Mode
summary: Learn SQL mode.
---

# SQLモード {#sql-mode}

TiDB サーバーはさまざまな SQL モードで動作し、これらのモードをクライアントごとに異なる方法で適用します。 SQL モードは、以下で説明するように、TiDB がサポートする SQL 構文と実行するデータ検証チェックのタイプを定義します。

TiDB が開始されたら、 `SET [ SESSION | GLOBAL ] sql_mode='modes'`を変更して SQL モードを設定します。

SQL モードを`GLOBAL`レベルに設定する場合は、 `SUPER`権限を持っていることを確認してください。このレベルでの設定は、その後に確立される接続にのみ影響します。 `SESSION`レベルの SQL モードへの変更は、現在のクライアントにのみ影響します。

`Modes`は、カンマ (「,」) で区切られた一連の異なるモードです。 `SELECT @@sql_mode`ステートメントを使用して、現在の SQL モードを確認できます。 SQL モードのデフォルト値: `ONLY_FULL_GROUP_BY, STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, NO_ENGINE_SUBSTITUTION` 。

## 重要な<code>sql_mode</code>値 {#important-code-sql-mode-code-values}

-   `ANSI` : このモードは標準 SQL に準拠します。このモードでは、データがチェックされます。データが定義されたタイプまたは長さに準拠していない場合、データタイプは調整またはトリミングされ、 `warning`が返されます。
-   `STRICT_TRANS_TABLES` : データが厳密にチェックされる厳密モード。データが正しくない場合、そのデータをテーブルに挿入できず、エラーが返されます。
-   `TRADITIONAL` : このモードでは、TiDB は「従来の」SQL データベース システムのように動作します。不正な値が列に挿入されると、警告ではなくエラーが返されます。その後、 `INSERT`または`UPDATE`ステートメントは直ちに停止されます。

## SQLモードテーブル {#sql-mode-table}

| 名前                           | 説明                                                                                                                                                                               |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PIPES_AS_CONCAT`            | 「||」を扱います`OR` (完全サポート) としてではなく、文字列連結演算子 ( `+` ) ( `CONCAT()`と同じ) として                                                                                                             |
| `ANSI_QUOTES`                | `"`識別子として扱います。 `ANSI_QUOTES`が有効な場合、一重引用符のみが文字列リテラルとして扱われ、二重引用符は識別子として扱われます。したがって、二重引用符を使用して文字列を引用することはできません。 （フルサポート）                                                            |
| `IGNORE_SPACE`               | このモードが有効な場合、システムはスペースを無視します。たとえば、「user」と「user」は同じです。 （フルサポート）                                                                                                                    |
| `ONLY_FULL_GROUP_BY`         | `SELECT` 、 `HAVING` 、または`ORDER BY`で参照される非集計列が`GROUP BY`に存在しない場合、この SQL ステートメントは無効になります。これは、列が`GROUP BY`に存在しないのにクエリによって表示されるのは異常であるためです。 （フルサポート）                                 |
| `NO_UNSIGNED_SUBTRACTION`    | オペランドに減算のシンボルがない場合、結果を`UNSIGNED`としてマークしません。 （フルサポート）                                                                                                                             |
| `NO_DIR_IN_CREATE`           | テーブルの作成時に`INDEX DIRECTORY`と`DATA DIRECTORY`ディレクティブをすべて無視します。このオプションはセカンダリ レプリケーション サーバーにのみ役立ちます (構文サポートのみ)                                                                       |
| `NO_KEY_OPTIONS`             | `SHOW CREATE TABLE`ステートメントを使用すると、 `ENGINE`などの MySQL 固有の構文はエクスポートされません。 mysqldump を使用して DB タイプ間で移行する場合は、このオプションを検討してください。 (構文サポートのみ)                                              |
| `NO_FIELD_OPTIONS`           | `SHOW CREATE TABLE`ステートメントを使用すると、 `ENGINE`などの MySQL 固有の構文はエクスポートされません。 mysqldump を使用して DB タイプ間で移行する場合は、このオプションを検討してください。 (構文サポートのみ)                                              |
| `NO_TABLE_OPTIONS`           | `SHOW CREATE TABLE`ステートメントを使用すると、 `ENGINE`などの MySQL 固有の構文はエクスポートされません。 mysqldump を使用して DB タイプ間で移行する場合は、このオプションを検討してください。 (構文サポートのみ)                                              |
| `NO_AUTO_VALUE_ON_ZERO`      | このモードが有効な場合、 `AUTO_INCREMENT`列に渡された値が`0`または特定の値である場合、システムはこの値をこの列に直接書き込みます。 `NULL`が渡されると、システムは次のシリアル番号を自動的に生成します。 （フルサポート）                                                       |
| `NO_BACKSLASH_ESCAPES`       | このモードが有効な場合、 `\`バックスラッシュ記号はそれ自体を表すだけです。 （フルサポート）                                                                                                                                 |
| `STRICT_TRANS_TABLES`        | トランザクションstorageエンジンの厳密モードを有効にし、不正な値が挿入された後にステートメント全体をロールバックします。 （フルサポート）                                                                                                         |
| `STRICT_ALL_TABLES`          | トランザクション テーブルの場合、不正な値が挿入された後、トランザクション ステートメント全体をロールバックします。 （フルサポート）                                                                                                              |
| `NO_ZERO_IN_DATE`            | 厳密モードでは、月または日の部分が`0`である日付は受け入れられません。 `IGNORE`オプションを使用すると、TiDB は同様の日付として「0000-00-00」を挿入します。非厳密モードでは、この日付は受け入れられますが、警告が返されます。 （フルサポート）                                             |
| `NO_ZERO_DATE`               | 厳密モードでは、「0000-00-00」を有効な日付として使用しません。 `IGNORE`オプションを使用しても、ゼロの日付を挿入できます。非厳密モードでは、この日付は受け入れられますが、警告が返されます。 （フルサポート）                                                                 |
| `ALLOW_INVALID_DATES`        | このモードでは、システムはすべての日付の有効性をチェックしません。 `1`から`12`範囲の月の値と`1`から`31`の範囲の日付の値のみがチェックされます。このモードは`DATE`と`DATATIME`列にのみ適用されます。 `TIMESTAMP`列すべてに完全な有効性チェックが必要です。 （フルサポート）                      |
| `ERROR_FOR_DIVISION_BY_ZERO` | このモードが有効な場合、データ変更操作 ( `INSERT`または`UPDATE` ) で`0`による除算を処理するときに、システムはエラーを返します。<br/>このモードが有効になっていない場合、システムは警告を返し、代わりに`NULL`が使用されます。 （フルサポート）                                        |
| `NO_AUTO_CREATE_USER`        | 指定されたパスワードを除き、 `GRANT`新しいユーザーを自動的に作成しないようにします (完全サポート)                                                                                                                           |
| `HIGH_NOT_PRECEDENCE`        | NOT 演算子の優先順位は、 `NOT a BETWEEN b AND c`などの式が`NOT (a BETWEEN b AND c)`として解析されるようなものです。 MySQL の一部の古いバージョンでは、この式は`(NOT a) BETWEEN b AND c`として解析されます。 （フルサポート）                        |
| `NO_ENGINE_SUBSTITUTION`     | 必要なstorageエンジンが無効になっているかコンパイルされていない場合、storageエンジンの自動置換を防止します。 (構文サポートのみ)                                                                                                         |
| `PAD_CHAR_TO_FULL_LENGTH`    | このモードが有効な場合、システムは`CHAR`タイプの末尾のスペースをトリミングしません。 (構文サポートのみ。このモードは[MySQL 8.0 では非推奨になりました](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_pad_char_to_full_length)です。) |
| `REAL_AS_FLOAT`              | `REAL` `DOUBLE`の同義語ではなく、 `FLOAT`の同義語として扱います (完全サポート)                                                                                                                             |
| `POSTGRESQL`                 | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS`と同等 (構文サポートのみ)                                                    |
| `MSSQL`                      | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS`と同等 (構文サポートのみ)                                                    |
| `DB2`                        | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS`と同等 (構文サポートのみ)                                                    |
| `MAXDB`                      | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS` 、 `NO_AUTO_CREATE_USER`に相当 (フルサポート)                              |
| `MySQL323`                   | `NO_FIELD_OPTIONS` 、 `HIGH_NOT_PRECEDENCE`と同等 (構文サポートのみ)                                                                                                                         |
| `MYSQL40`                    | `NO_FIELD_OPTIONS` 、 `HIGH_NOT_PRECEDENCE`と同等 (構文サポートのみ)                                                                                                                         |
| `ANSI`                       | `REAL_AS_FLOAT` 、 `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE`と同等 (構文サポートのみ)                                                                                               |
| `TRADITIONAL`                | `STRICT_TRANS_TABLES` 、 `STRICT_ALL_TABLES` 、 `NO_ZERO_IN_DATE` 、 `NO_ZERO_DATE` 、 `ERROR_FOR_DIVISION_BY_ZERO` 、 `NO_AUTO_CREATE_USER`と同等 (構文サポートのみ)                            |
| `ORACLE`                     | `PIPES_AS_CONCAT` 、 `ANSI_QUOTES` 、 `IGNORE_SPACE` 、 `NO_KEY_OPTIONS` 、 `NO_TABLE_OPTIONS` 、 `NO_FIELD_OPTIONS` 、 `NO_AUTO_CREATE_USER`と同等 (構文サポートのみ)                            |
