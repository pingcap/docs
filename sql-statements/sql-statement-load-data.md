---
title: LOAD DATA | TiDB SQL Statement Reference
summary: An overview of the usage of LOAD DATA for the TiDB database.
---

# データを読み込む {#load-data}

`LOAD DATA`ステートメントのバッチはデータを TiDB テーブルにロードします。

TiDB v7.0.0 以降、 `LOAD DATA` SQL ステートメントは次の機能をサポートします。

-   S3 および GCS からのデータのインポートをサポート
-   新しいパラメータを追加`FIELDS DEFINED NULL BY`

> **警告：**
>
> 新しいパラメータ`FIELDS DEFINED NULL BY`と、S3 および GCS からのデータのインポートのサポートは実験的ものです。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

## あらすじ {#synopsis}

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt

LocalOpt ::= ('LOCAL')?

Fields ::=
    ('TERMINATED' 'BY' stringLit
    | ('OPTIONALLY')? 'ENCLOSED' 'BY' stringLit
    | 'ESCAPED' 'BY' stringLit
    | 'DEFINED' 'NULL' 'BY' stringLit ('OPTIONALLY' 'ENCLOSED')?)?
```

## パラメーター {#parameters}

### <code>LOCAL</code> {#code-local-code}

`LOCAL`を使用して、インポートするクライアント上のデータ ファイルを指定できます。この場合、file パラメーターはクライアント上のファイル システム パスである必要があります。

TiDB Cloudを使用している場合、 `LOAD DATA`ステートメントを使用してローカル データ ファイルをロードするには、 TiDB Cloudに接続するときに接続文字列に`--local-infile`オプションを追加する必要があります。

-   以下は、TiDB サーバーレスの接続文字列の例です。

        mysql --connect-timeout 15 -u '<user_name>' -h <host_name> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p<your_password> --local-infile

-   以下は、TiDB Dended の接続文字列の例です。

        mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_path> --tls-version="TLSv1.2" -u root -h <host_name> -P 4000 -D test -p<your_password> --local-infile

### S3 および GCSstorage {#s3-and-gcs-storage}

<CustomContent platform="tidb">

`LOCAL`を指定しない場合、 [外部storage](/br/backup-and-restore-storages.md)で詳しく説明されているように、 file パラメーターは有効な S3 または GCS パスである必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

`LOCAL`を指定しない場合、 [外部storage](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)で詳しく説明されているように、 file パラメーターは有効な S3 または GCS パスである必要があります。

</CustomContent>

データ ファイルが S3 または GCS に保存されている場合、個々のファイルをインポートすることも、ワイルドカード文字`*`を使用してインポートする複数のファイルに一致させることもできます。ワイルドカードはサブディレクトリ内のファイルを再帰的に処理しないことに注意してください。以下にいくつかの例を示します。

-   単一のファイルをインポートする: `s3://<bucket-name>/path/to/data/foo.csv`
-   指定されたパスにあるすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/*`
-   指定されたパスにある`.csv`で終わるすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/*.csv`
-   指定されたパスの下にプレフィックス`foo`が付いたすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/foo*`
-   指定されたパスにある、接頭辞`foo`と末尾`.csv`のすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/foo*.csv`

### <code>Fields</code> 、 <code>Lines</code> 、および<code>Ignore Lines</code> {#code-fields-code-code-lines-code-and-code-ignore-lines-code}

`Fields`および`Lines`パラメータを使用して、データ形式の処理方法を指定できます。

-   `FIELDS TERMINATED BY` : データ区切り文字を指定します。
-   `FIELDS ENCLOSED BY` : データの囲み文字を指定します。
-   `LINES TERMINATED BY` : 特定の文字で行を終了する場合は、行終端文字を指定します。

`DEFINED NULL BY`を使用すると、データ ファイル内で NULL 値を表現する方法を指定できます。

-   MySQL の動作と一致して、 `ESCAPED BY`が null でない場合、たとえばデフォルト値`\`が使用されている場合、 `\N` NULL 値とみなされます。
-   `DEFINED NULL BY 'my-null'`などの`DEFINED NULL BY`使用する場合、 `my-null`は NULL 値とみなされます。
-   `DEFINED NULL BY 'my-null' OPTIONALLY ENCLOSED`などの`DEFINED NULL BY ... OPTIONALLY ENCLOSED`を使用する場合、 `my-null`および`"my-null"` ( `ENCLOSED BY '"`仮定) は NULL 値とみなされます。
-   `DEFINED NULL BY`や`DEFINED NULL BY ... OPTIONALLY ENCLOSED`使用せず、 `ENCLOSED BY '"'`などの`ENCLOSED BY`使用する場合、 `NULL`は NULL 値とみなされます。この動作は MySQL と一致しています。
-   それ以外の場合は、NULL 値とは見なされません。

次のデータ形式を例として取り上げます。

    "bob","20","street 1"\r\n
    "alice","33","street 1"\r\n

`bob` 、および`street 1` `20`抽出する場合は、フィールド区切り文字を`','`に、囲み文字を`'\"'`に指定します。

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

前述のパラメータを指定しない場合、インポートされたデータはデフォルトで次の方法で処理されます。

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

`IGNORE <number> LINES`パラメータを設定すると、ファイルの最初の`number`行を無視できます。たとえば、 `IGNORE 1 LINES`を構成すると、ファイルの最初の行は無視されます。

## 例 {#examples}

次の例では、 `LOAD DATA`を使用してデータをインポートします。フィールド区切り文字としてカンマを指定します。データを囲む二重引用符は無視されます。ファイルの最初の行は無視されます。

<CustomContent platform="tidb">

`ERROR 1148 (42000): the used command is not allowed with this TiDB version`表示された場合は、トラブルシューティングについて[エラー 1148 (42000): 使用されたコマンドは、この TiDB バージョンでは許可されていません](/error-codes.md#mysql-native-error-messages)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ERROR 1148 (42000): the used command is not allowed with this TiDB version`表示された場合は、トラブルシューティングについて[エラー 1148 (42000): 使用されたコマンドは、この TiDB バージョンでは許可されていません](https://docs.pingcap.com/tidb/stable/error-codes#mysql-native-error-messages)を参照してください。

</CustomContent>

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```sql
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA` 、 `FIELDS ENCLOSED BY`および`FIELDS TERMINATED BY`のパラメータとして 16 進 ASCII 文字式または 2 進 ASCII 文字式の使用もサポートします。次の例を参照してください。

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

上の例では、 `x'2c'`は`,`文字の 16 進表現で、 `b'100010'`は`"`文字の 2 進表現です。

## MySQLの互換性 {#mysql-compatibility}

`LOAD DATA`ステートメントの構文は、解析されても無視される文字セット オプションを除き、MySQL の構文と互換性があります。構文の互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support)を実行できます。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB v4.0.0 より前のバージョンでは、20000 行ごとに`LOAD DATA`コミットされます。
> -   TiDB v4.0.0 から v6.6.0 までのバージョンの場合、TiDB はデフォルトで 1 つのトランザクションですべての行をコミットします。
> -   TiDB v4.0.0 以前のバージョンからアップグレードした後、 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`が発生する可能性があります。このエラーを解決する推奨方法は、 `tidb.toml`ファイルの[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)値を増やすことです。この制限を増やすことができない場合は、 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)から`20000`に設定することで、アップグレード前の動作を復元することもできます。 v7.0.0 以降、 `tidb_dml_batch_size` `LOAD DATA`ステートメントに影響しなくなることに注意してください。
> -   トランザクションでコミットされた行の数に関係なく、明示的なトランザクションの[`ROLLBACK`](/sql-statements/sql-statement-rollback.md)ステートメントによって`LOAD DATA`ロールバックされません。
> -   `LOAD DATA`ステートメントは、TiDB トランザクション モードの構成に関係なく、常に楽観的トランザクション モードで実行されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB v4.0.0 より前のバージョンでは、20000 行ごとに`LOAD DATA`コミットされます。
> -   TiDB v4.0.0 から v6.6.0 までのバージョンの場合、TiDB はデフォルトで 1 つのトランザクションですべての行をコミットします。
> -   TiDB v7.0.0 以降、バッチでコミットされる行数は`LOAD DATA`ステートメントの`WITH batch_size=<number>`パラメーターによって制御され、デフォルトではコミットあたり 1000 行になります。
> -   TiDB v4.0.0 以前のバージョンからアップグレードした後、 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`が発生する可能性があります。このエラーを解決するには、 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)を`20000`に設定することで、アップグレード前の動作を復元できます。
> -   トランザクションでコミットされた行の数に関係なく、明示的なトランザクションの[`ROLLBACK`](/sql-statements/sql-statement-rollback.md)ステートメントによって`LOAD DATA`ロールバックされません。
> -   `LOAD DATA`ステートメントは、TiDB トランザクション モードの構成に関係なく、常に楽観的トランザクション モードで実行されます。

</CustomContent>

## こちらも参照 {#see-also}

<CustomContent platform="tidb">

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [TiDB 楽観的トランザクションモデル](/optimistic-transaction.md)
-   [TiDB ペシミスティックトランザクションモード](/pessimistic-transaction.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [TiDB 楽観的トランザクションモデル](/optimistic-transaction.md)
-   [TiDB ペシミスティックトランザクションモード](/pessimistic-transaction.md)

</CustomContent>
