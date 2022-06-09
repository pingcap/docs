---
title: LOAD DATA | TiDB SQL Statement Reference
summary: An overview of the usage of LOAD DATA for the TiDB database.
---

# データを読み込む {#load-data}

`LOAD DATA`ステートメントバッチはデータをTiDBテーブルにロードします。

## あらすじ {#synopsis}

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt
```

## パラメーター {#parameters}

### <code>LocalOpt</code> {#code-localopt-code}

`LocalOpt`パラメーターを構成することにより、インポートされたデータファイルがクライアントまたはサーバーに配置されるように指定できます。現在、TiDBはクライアントからのデータインポートのみをサポートしています。したがって、データをインポートするときは、値`LocalOpt`を設定して`Local` 。

### <code>Fields</code>と<code>Lines</code> {#code-fields-code-and-code-lines-code}

`Fields`および`Lines`パラメーターを構成することにより、データ形式の処理方法を指定できます。

-   `FIELDS TERMINATED BY` ：各データの区切り文字を指定します。
-   `FIELDS ENCLOSED BY` ：各データの囲み文字を指定します。
-   `LINES TERMINATED BY` ：特定の文字で行を終了する場合は、行末記号を指定します。

例として、次のデータ形式を取り上げます。

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

`bob` 、および`20`を抽出する場合は、区切り文字を`street 1`として指定し、囲み文字を`','`として指定し`'\"'` 。

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

上記のパラメータを指定しない場合、インポートされたデータはデフォルトで次の方法で処理されます。

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY ''
LINES TERMINATED BY '\n'
```

### <code>IGNORE number LINES</code> {#code-ignore-number-lines-code}

`IGNORE number LINES`パラメータを設定することにより、ファイルの最初の`number`行を無視できます。たとえば、 `IGNORE 1 LINES`を設定すると、ファイルの最初の行は無視されます。

さらに、TiDBは現在、 `DuplicateOpt` 、および`CharsetOpt`パラメーターの構文解析のみをサポートして`LoadDataSetSpecOpt`ます。

## 例 {#examples}

{{< copyable "" >}}

```sql
CREATE TABLE trips (
    trip_id bigint NOT NULL PRIMARY KEY AUTO_INCREMENT,
    duration integer not null,
    start_date datetime,
    end_date datetime,
    start_station_number integer,
    start_station varchar(255),
    end_station_number integer,
    end_station varchar(255),
    bike_number varchar(255),
    member_type varchar(255)
    );
```

```
Query OK, 0 rows affected (0.14 sec)
```

次の例では、 `LOAD DATA`を使用してデータをインポートします。区切り文字としてコンマを指定します。データを囲む二重引用符は無視されます。ファイルの最初の行は無視されます。

エラーメッセージ`ERROR 1148 (42000): the used command is not allowed with this TiDB version`が表示された場合は、 [エラー1148（42000）：使用されているコマンドはこのTiDBバージョンでは許可されていません](/faq/tidb-faq.md#error-1148-42000-the-used-command-is-not-allowed-with-this-tidb-version)を参照してください。

{{< copyable "" >}}

```
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA`は、 `FIELDS ENCLOSED BY`および`FIELDS TERMINATED BY`のパラメーターとして16進ASCII文字式または2進ASCII文字式の使用もサポートします。次の例を参照してください。

{{< copyable "" >}}

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

上記の例では、 `x'2c'`は`,`文字の16進表現であり、 `b'100010'`は`"`文字の2進表現です。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、 `LOAD DATA...REPLACE INTO`の構文[＃24515](https://github.com/pingcap/tidb/issues/24515)を除いて、MySQLと完全に互換性があると理解されています。その他の互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

> **ノート：**
>
> TiDBの以前のリリースでは、20000行ごとに`LOAD DATA`コミットされていました。デフォルトでは、TiDBは1つのトランザクションですべての行をコミットするようになりました。これにより、TiDB4.0以前のバージョンからアップグレードした後にエラー`ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`が発生する可能性があります。
>
> このエラーを解決するための推奨される方法は、 `tidb.toml`ファイルの`txn-total-size-limit`の値を増やすことです。この制限を増やすことができない場合は、 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)を`20000`に設定して、以前の動作を復元することもできます。

## も参照してください {#see-also}

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [サンプルデータベースのインポート](/import-example-data.md)
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
