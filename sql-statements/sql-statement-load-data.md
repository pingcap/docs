---
title: LOAD DATA | TiDB SQL Statement Reference
summary: An overview of the usage of LOAD DATA for the TiDB database.
---

# データを読み込む {#load-data}

`LOAD DATA`ステートメントのバッチはデータを TiDB テーブルにロードします。

## あらすじ {#synopsis}

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt
```

## パラメーター {#parameters}

### <code>LocalOpt</code> {#code-localopt-code}

`LocalOpt`パラメータを構成することで、インポートされたデータ ファイルがクライアント上にあるのか、サーバー上にあるのかを指定できます。現在、TiDB はクライアントからのデータ インポートのみをサポートしています。したがって、データをインポートするときは、 `LocalOpt`から`Local`の値を設定します。

### <code>Fields</code>と<code>Lines</code> {#code-fields-code-and-code-lines-code}

パラメータ`Fields`とパラメータ`Lines`を設定することで、データ形式の処理方法を指定できます。

-   `FIELDS TERMINATED BY` : 各データの区切り文字を指定します。
-   `FIELDS ENCLOSED BY` : 各データの囲み文字を指定します。
-   `LINES TERMINATED BY` : 行を特定の文字で終了する場合は、行終端文字を指定します。

次のデータ形式を例として取り上げます。

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

`bob` 、 `20` 、および`street 1`を抽出する場合は、区切り文字を`','` 、囲み文字を`'\"'`として指定します。

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

上記のパラメータを指定しない場合、インポートされたデータはデフォルトで次の方法で処理されます。

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY ''
LINES TERMINATED BY '\n'
```

### <code>IGNORE number LINES</code> {#code-ignore-number-lines-code}

`IGNORE number LINES`パラメータを設定すると、ファイルの最初の`number`行を無視できます。たとえば、 `IGNORE 1 LINES`を構成すると、ファイルの最初の行は無視されます。

さらに、TiDB は現在`DuplicateOpt` 、 `CharsetOpt` 、および`LoadDataSetSpecOpt`パラメーターの構文の解析のみをサポートしています。

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

次の例では、 `LOAD DATA`を使用してデータをインポートします。区切り文字としてカンマを指定します。データを囲む二重引用符は無視されます。ファイルの最初の行は無視されます。

エラー メッセージ`ERROR 1148 (42000): the used command is not allowed with this TiDB version`表示された場合は、 [エラー 1148 (42000): 使用されたコマンドは、この TiDB バージョンでは許可されていません](/faq/tidb-faq.md#error-1148-42000-the-used-command-is-not-allowed-with-this-tidb-version)を参照してください。

{{< copyable "" >}}

```
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA` 、 `FIELDS ENCLOSED BY`および`FIELDS TERMINATED BY`のパラメータとして 16 進 ASCII 文字式または 2 進 ASCII 文字式の使用もサポートします。次の例を参照してください。

{{< copyable "" >}}

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

上の例では、 `x'2c'`は`,`文字の 16 進表現で、 `b'100010'`は`"`文字の 2 進表現です。

## MySQLの互換性 {#mysql-compatibility}

このステートメントの構文は、 `LOAD DATA...REPLACE INTO`構文[#24515](https://github.com/pingcap/tidb/issues/24515)を除き、MySQL と互換性があります。その他の構文互換性の違いは、GitHub では[問題を通じて報告されました](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

> **ノート：**
>
> -   TiDB の以前のリリースでは、20000 行ごとに`LOAD DATA`がコミットされました。デフォルトでは、TiDB は 1 つのトランザクションですべての行をコミットするようになりました。これにより、TiDB 4.0 以前のバージョンからアップグレードした後にエラー`ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`が発生する可能性があります。このエラーを解決する推奨方法は、 `tidb.toml`ファイルの`txn-total-size-limit`値を増やすことです。この制限を増やすことができない場合は、 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size)から`20000`に設定することで以前の動作を復元することもできます。
> -   トランザクションでコミットされた行の数に関係なく、明示的なトランザクションの[`ROLLBACK`](/sql-statements/sql-statement-rollback.md)ステートメントによって`LOAD DATA`ロールバックされません。
> -   `LOAD DATA`ステートメントは、TiDB トランザクション モードの構成に関係なく、常に楽観的トランザクション モードで実行されます。

## こちらも参照 {#see-also}

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [サンプルデータベースのインポート](/import-example-data.md)
-   [TiDB 楽観的トランザクションモデル](/optimistic-transaction.md)
-   [TiDB ペシミスティックトランザクションモード](/pessimistic-transaction.md)
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
