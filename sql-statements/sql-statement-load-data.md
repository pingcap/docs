---
title: LOAD DATA | TiDB SQL Statement Reference
summary: TiDB データベースの LOAD DATA の使用法の概要。
---

# データをロード {#load-data}

`LOAD DATA`ステートメント バッチは、データを TiDB テーブルにロードします。

TiDB v7.0.0 以降、 `LOAD DATA` SQL ステートメントは次の機能をサポートします。

-   S3およびGCSからのデータのインポートをサポート
-   新しいパラメータ`FIELDS DEFINED NULL BY`追加する

> **警告：**
>
> 新しいパラメータ`FIELDS DEFINED NULL BY`と S3 および GCS からのデータのインポートのサポートは実験的ものです。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

## 概要 {#synopsis}

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

## パラメータ {#parameters}

### <code>LOCAL</code> {#code-local-code}

`LOCAL`を使用して、インポートするクライアント上のデータ ファイルを指定できます。ファイル パラメーターは、クライアント上のファイル システム パスである必要があります。

TiDB Cloud を使用している場合、 `LOAD DATA`ステートメントを使用してローカル データ ファイルをロードするには、 TiDB Cloudに接続するときに接続文字列に`--local-infile`オプションを追加する必要があります。

-   以下は、 TiDB Cloud Serverless の接続文字列の例です。

        mysql --connect-timeout 15 -u '<user_name>' -h <host_name> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p<your_password> --local-infile

-   以下は、 TiDB Cloud Dedicated の接続文字列の例です。

        mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_path> --tls-version="TLSv1.2" -u root -h <host_name> -P 4000 -D test -p<your_password> --local-infile

### S3 および GCSstorage {#s3-and-gcs-storage}

<CustomContent platform="tidb">

`LOCAL`指定しない場合は、ファイル パラメータは[外部storage](/br/backup-and-restore-storages.md)で詳述されているように、有効な S3 または GCS パスである必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

`LOCAL`指定しない場合は、ファイル パラメータは[外部storage](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)で詳述されているように、有効な S3 または GCS パスである必要があります。

</CustomContent>

データ ファイルが S3 または GCS に保存されている場合は、個々のファイルをインポートするか、ワイルドカード文字`*`を使用してインポートする複数のファイルを一致させることができます。ワイルドカードはサブディレクトリ内のファイルを再帰的に処理しないことに注意してください。次に例をいくつか示します。

-   1つのファイルをインポートする: `s3://<bucket-name>/path/to/data/foo.csv`
-   指定されたパス内のすべてのファイルをインポート: `s3://<bucket-name>/path/to/data/*`
-   指定されたパスの下にある`.csv`で終わるすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/*.csv`
-   指定されたパスの下にある`foo`で始まるすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/foo*`
-   指定されたパスの下にある、先頭が`foo`で末尾が`.csv`のすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/foo*.csv`

### <code>Fields</code> 、 <code>Lines</code> 、 <code>Ignore Lines</code> {#code-fields-code-code-lines-code-and-code-ignore-lines-code}

`Fields`および`Lines`パラメータを使用して、データ形式の処理方法を指定できます。

-   `FIELDS TERMINATED BY` : データ区切り文字を指定します。
-   `FIELDS ENCLOSED BY` : データの囲み文字を指定します。
-   `LINES TERMINATED BY` : 特定の文字で行を終了する場合に、行末文字を指定します。

`DEFINED NULL BY`使用して、データ ファイル内で NULL 値をどのように表現するかを指定できます。

-   MySQL の動作と一致して、 `ESCAPED BY` null でない場合、たとえばデフォルト値`\`が使用されると、 `\N` NULL 値と見なされます。
-   `DEFINED NULL BY 'my-null'`のように`DEFINED NULL BY`使用すると、 `my-null` NULL 値と見なされます。
-   `DEFINED NULL BY ... OPTIONALLY ENCLOSED`使用する場合、 `DEFINED NULL BY 'my-null' OPTIONALLY ENCLOSED` 、 `my-null` 、 `"my-null"` ( `ENCLOSED BY '"`と想定) は NULL 値と見なされます。
-   `DEFINED NULL BY`や`DEFINED NULL BY ... OPTIONALLY ENCLOSED`使用せず、 `ENCLOSED BY '"'`などの`ENCLOSED BY`を使用する場合、 `NULL` NULL 値と見なされます。この動作は MySQL と一致しています。
-   それ以外の場合は、NULL 値とは見なされません。

次のデータ形式を例に挙げます。

    "bob","20","street 1"\r\n
    "alice","33","street 1"\r\n

`bob` 、 `20` 、 `street 1`を抽出する場合は、フィールド区切り文字を`','` 、囲み文字を`'\"'`に指定します。

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

上記のパラメータを指定しない場合、インポートされたデータはデフォルトで次のように処理されます。

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

`IGNORE <number> LINES`パラメータを設定すると、ファイルの最初の`number`行を無視できます。たとえば、 `IGNORE 1 LINES`設定すると、ファイルの最初の行は無視されます。

## 例 {#examples}

次の例では、 `LOAD DATA`を使用してデータをインポートします。フィールド区切り文字としてコンマが指定されています。データを囲む二重引用符は無視されます。ファイルの最初の行は無視されます。

<CustomContent platform="tidb">

`ERROR 1148 (42000): the used command is not allowed with this TiDB version`表示された場合は、トラブルシューティングについては[エラー 1148 (42000): 使用されたコマンドはこの TiDB バージョンでは許可されていません](/error-codes.md#mysql-native-error-messages)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ERROR 1148 (42000): the used command is not allowed with this TiDB version`表示された場合は、トラブルシューティングについては[エラー 1148 (42000): 使用されたコマンドはこの TiDB バージョンでは許可されていません](https://docs.pingcap.com/tidb/stable/error-codes#mysql-native-error-messages)を参照してください。

</CustomContent>

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```sql
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA` 、 `FIELDS ENCLOSED BY`および`FIELDS TERMINATED BY`パラメータとして、16 進 ASCII 文字式またはバイナリ ASCII 文字式の使用もサポートします。次の例を参照してください。

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

上記の例では、 `x'2c'` `,`文字の 16 進表現であり、 `b'100010'` `"`文字の 2 進表現です。

## MySQL 互換性 {#mysql-compatibility}

`LOAD DATA`ステートメントの構文は、解析されても無視される文字セット オプションを除き、MySQL の構文と互換性があります。構文の互換性に違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)実行できます。

<CustomContent platform="tidb">

> **注記：**
>
> -   TiDB v4.0.0 より前のバージョンでは、20000 行ごとに`LOAD DATA`コミットが行われ、これを構成することはできません。
> -   TiDB v4.0.0 から v6.6.0 までのバージョンでは、TiDB はデフォルトで 1 つのトランザクションですべての行をコミットします。ただし、固定数の行ごとに`LOAD DATA`ステートメントでコミットする必要がある場合は、必要な行数を[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)に設定できます。
> -   TiDB v7.0.0 以降では、 `tidb_dml_batch_size` `LOAD DATA`には影響しなくなり、TiDB は 1 つのトランザクションですべての行をコミットします。
> -   TiDB v4.0.0 以前のバージョンからアップグレードすると、 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`発生する可能性があります。このエラーを解決するには、 `tidb.toml`ファイルの[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)値を増やすことをお勧めします。
> -   トランザクションでコミットされる行数に関係なく、明示的なトランザクションの[`ROLLBACK`](/sql-statements/sql-statement-rollback.md)のステートメントによって`LOAD DATA`ロールバックされることはありません。
> -   `LOAD DATA`ステートメントは、TiDB トランザクション モードの構成に関係なく、常に楽観的トランザクション モードで実行されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDB v4.0.0 より前のバージョンでは、20000 行ごとに`LOAD DATA`コミットが行われ、これを構成することはできません。
> -   TiDB v4.0.0 から v6.6.0 までのバージョンでは、TiDB はデフォルトで 1 つのトランザクションですべての行をコミットします。ただし、固定数の行ごとに`LOAD DATA`ステートメントでコミットする必要がある場合は、必要な行数を[`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)に設定できます。
> -   v7.0.0 以降では、 `tidb_dml_batch_size` `LOAD DATA`には影響しなくなり、 TiDB は 1 つのトランザクションですべての行をコミットします。
> -   TiDB v4.0.0 以前のバージョンからアップグレードすると、 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`発生する可能性があります。このエラーを解決するには、 [TiDB Cloudサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)に連絡して[`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit)値を増やすことができます。
> -   トランザクションでコミットされる行数に関係なく、明示的なトランザクションの[`ROLLBACK`](/sql-statements/sql-statement-rollback.md)のステートメントによって`LOAD DATA`ロールバックされることはありません。
> -   `LOAD DATA`ステートメントは、TiDB トランザクション モードの構成に関係なく、常に楽観的トランザクション モードで実行されます。

</CustomContent>

## 参照 {#see-also}

<CustomContent platform="tidb">

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [TiDB 楽観的トランザクションモデル](/optimistic-transaction.md)
-   [TiDB 悲観的トランザクションモード](/pessimistic-transaction.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [TiDB 楽観的トランザクションモデル](/optimistic-transaction.md)
-   [TiDB 悲観的トランザクションモード](/pessimistic-transaction.md)

</CustomContent>
