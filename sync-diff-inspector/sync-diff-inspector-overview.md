---
title: sync-diff-inspector User Guide
summary: Use sync-diff-inspector to compare data and repair inconsistent data.
---

# sync-diff-inspectorユーザーガイド {#sync-diff-inspector-user-guide}

[sync-diff-inspector](https://github.com/pingcap/tidb-tools/tree/master/sync_diff_inspector)は、データベースに保存されているデータをMySQLプロトコルと比較するために使用されるツールです。たとえば、MySQLのデータとTiDBのデータ、MySQLのデータとMySQLのデータ、またはTiDBのデータとTiDBのデータを比較できます。さらに、このツールを使用して、少量のデータに一貫性がないシナリオでデータを修復することもできます。

このガイドでは、sync-diff-inspectorの主な機能を紹介し、このツールを構成して使用する方法について説明します。 sync-diff-inspectorをダウンロードするには、次のいずれかの方法を使用します。

-   バイナリパッケージ。 sync-diff-inspectorバイナリパッケージはTiDBツールキットに含まれています。 TiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロードする](/download-ecosystem-tools.md)を参照してください。
-   Dockerイメージ。次のコマンドを実行してダウンロードします。

    {{< copyable "" >}}

    ```shell
    docker pull pingcap/tidb-enterprise-tools:nightly
    ```

## 主な機能 {#key-features}

-   テーブルスキーマとデータを比較します
-   データの不整合が存在する場合にデータを修復するために使用されるSQLステートメントを生成します
-   サポート[スキーマ名またはテーブル名が異なるテーブルのデータチェック](/sync-diff-inspector/route-diff.md)
-   サポート[シャーディングシナリオでのデータチェック](/sync-diff-inspector/shard-diff.md)
-   サポート[TiDBアップストリーム-ダウンストリームクラスターのデータチェック](/sync-diff-inspector/upstream-downstream-diff.md)
-   サポート[DMレプリケーションシナリオでのデータチェック](/sync-diff-inspector/dm-diff.md)

## sync-diff-inspectorの制限 {#restrictions-of-sync-diff-inspector}

-   MySQLとTiDB間のデータ移行では、オンラインチェックはサポートされていません。アップストリーム-ダウンストリームチェックリストにデータが書き込まれていないこと、および特定の範囲のデータが変更されていないことを確認してください。 `range`を設定すると、この範囲のデータを確認できます。

-   `JSON` `BLOB` `BIT`の`BINARY`のデータはサポートされていません。データチェックを実行する場合、これらのタイプのデータのチェックをスキップするには、 `ignore-columns`を設定する必要があります。

-   TiDBとMySQL `DOUBLE` `FLOAT`およびその他の浮動小数点型の実装が異なります。 `FLOAT`と`DOUBLE`は、チェックサムの計算にそれぞれ6桁と15桁の有効数字を使用します。この機能を使用したくない場合は、 `ignore-columns`を設定して、これらの列のチェックをスキップします。

-   主キーまたは一意のインデックスを含まないテーブルのチェックをサポートします。ただし、データに一貫性がない場合、生成されたSQLステートメントはデータを正しく修復できない可能性があります。

## sync-diff-inspectorのデータベース権限 {#database-privileges-for-sync-diff-inspector}

sync-diff-inspectorは、テーブルスキーマの情報を取得し、データをクエリする必要があります。必要なデータベース権限は次のとおりです。

-   アップストリームデータベース
    -   `SELECT` （比較のためにデータをチェックします）
    -   `SHOW_DATABASES` （データベース名を表示）
    -   `RELOAD` （テーブルスキーマを表示）
-   下流データベース
    -   `SELECT` （比較のためにデータをチェックします）
    -   `SHOW_DATABASES` （データベース名を表示）
    -   `RELOAD` （テーブルスキーマを表示）

## Configuration / コンフィグレーションファイルの説明 {#configuration-file-description}

sync-diff-inspectorの構成は、次の部分で構成されています。

-   `Global config` ：チェックするスレッドの数、矛盾するテーブルを修正するためにSQLステートメントをエクスポートするかどうか、データをキャンプするかどうかなどの一般的な構成。
-   `Databases config` ：アップストリームおよびダウンストリームデータベースのインスタンスを構成します。
-   `Routes` ：ダウンストリームの単一スキーマ名と一致するアップストリームの複数のスキーマ名のルール**（オプション）** 。
-   `Task config` ：チェックするテーブルを構成します。一部のテーブルにアップストリームデータベースとダウンストリームデータベースの間に特定のマッピング関係がある場合、または特別な要件がある場合は、これらのテーブルを構成する必要があります。
-   `Table config` ：無視する指定された範囲や列など、特定のテーブルの特別な構成**（オプション）** 。

以下は、完全な構成ファイルの説明です。

-   注：名前の後に`s`が付いている構成には複数の値が含まれる可能性があるため、構成値を含めるには角括弧`[]`を使用する必要があります。

```toml
# Diff Configuration.

######################### Global config #########################
# The number of goroutines created to check data. The number of connections between sync-diff-inspector and upstream/downstream databases is slightly greater than this value.
check-thread-count = 4

# If enabled, SQL statements is exported to fix inconsistent tables.
export-fix-sql = true

# Only compares the table structure instead of the data.
check-struct-only = false

######################### Datasource config #########################
[data-sources]
[data-sources.mysql1] # mysql1 is the only custom ID for the database instance. It is used for the following `task.source-instances/task.target-instance` configuration.
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    # (optional) Use mapping rules to match multiple upstream sharded tables. Rule1 and rule2 are configured in the following Routes section.
    route-rules = ["rule1", "rule2"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
    # (optional) Uses the snapshot feature. If enabled, historical data is used for comparison
    # snapshot = "386902609362944000"

########################### Routes ##############################
# To compare the data of a large number of tables with different schema names or table names, or check the data of multiple upstream sharded tables and downstream table family, use the table-rule to configure the mapping relationship. You can configure the mapping rule only for the schema or table. Also, you can configure the mapping rules for both the schema and the table.
[routes]
[routes.rule1] # rule1 is the only custom ID for the configuration. It is used for the above `data-sources.route-rules` configuration.
schema-pattern = "test_*"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "t_*"          # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test"         # The name of the schema in the target database
target-table = "t"             # The name of the target table
[routes.rule2]
schema-pattern = "test2_*"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "t2_*"          # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test2"         # The name of the schema in the target database
target-table = "t2"             # The name of the target table

######################### task config #########################
# Configures the tables of the target database that need to be compared.
[task]
    # output-dir saves the following information:
    # 1 sql: The SQL file to fix tables that is generated after error is detected. One chunk corresponds to one SQL file.
    # 2 log: sync-diff.log
    # 3 summary: summary.txt
    # 4 checkpoint: a dir
    output-dir = "./output"
    # The upstream database. The value is the unique ID declared by data-sources.
    source-instances = ["mysql1"]
    # The downstream database. The value is the unique ID declared by data-sources.
    target-instance = "tidb0"
    # The tables of downstream databases to be compared. Each table needs to contain the schema name and the table name, separated by '.'
    # Use "?" to match any character and "*" to match characters of any length.
    # For detailed match rules, refer to golang regexp pkg: https://github.com/google/re2/wiki/Syntax.
    target-check-tables = ["schema*.table*", "!c.*", "test2.t2"]
    # (optional) Extra configurations for some tables, Config1 is defined in the following table config example.
    target-configs = ["config1"]

######################### Table config #########################
# Special configurations for specific tables. The tables to be configured must be in `task.target-check-tables`.
[table-configs.config1] # config1  is the only custom ID for this configuration. It is used for the above `task.target-configs` configuration.
# The name of the target table, you can use regular expressions to match multiple tables, but one table is not allowed to be matched by multiple special configurations at the same time.
target-tables = ["schema*.test*", "test2.t2"]
# (optional) Specifies the range of the data to be checked
# It needs to comply with the syntax of the WHERE clause in SQL.
range = "age > 10 AND age < 20"
# (optional) Specifies the column used to divide data into chunks. If you do not configure it,
# sync-diff-inspector chooses an appropriate column (primary key, unique key, or a field with index).
index-fields = ["col1","col2"]
# (optional) Ignores checking some columns such as some types (json, bit, blob, etc.)
# that sync-diff-inspector does not currently support.
# The floating-point data type behaves differently in TiDB and MySQL. You can use
# `ignore-columns` to skip checking these columns.
ignore-columns = ["",""]
# (optional) Specifies the size of the chunk for dividing the table. If not specified, this configuration can be deleted or be set as 0.
chunk-size = 0
# (optional) Specifies the "collation" for the table. If not specified, this configuration can be deleted or be set as an empty string.
collation = ""
```

## sync-diff-inspectorを実行します {#run-sync-diff-inspector}

次のコマンドを実行します。

{{< copyable "" >}}

```bash
./sync_diff_inspector --config=./config.toml
```

このコマンドは、 `output-dir`のチェックレポート`summary.txt`とログ`sync_diff.log`を出力し`config.toml` 。 `output-dir`では、 `config. toml`ファイルのハッシュ値で指定されたフォルダも生成されます。このフォルダーには、ブレークポイントのチェックポイントノード情報と、データに一貫性がない場合に生成されるSQLファイルが含まれます。

### 進捗情報 {#progress-information}

sync-diff-inspectorは、実行時に進行状況情報を`stdout`に送信します。進行状況情報には、テーブル構造の比較結果、テーブルデータの比較結果、および進行状況バーが含まれます。

> **ノート：**
>
> 表示効果を確保するには、表示ウィンドウの幅を80文字以上に保ちます。

```progress
A total of 2 tables need to be compared

Comparing the table structure of ``sbtest`.`sbtest96`` ... equivalent
Comparing the table structure of ``sbtest`.`sbtest99`` ... equivalent
Comparing the table data of ``sbtest`.`sbtest96`` ... failure
Comparing the table data of ``sbtest`.`sbtest99`` ...
_____________________________________________________________________________
Progress [==========================================================>--] 98% 193/200
```

```progress
A total of 2 tables need to be compared

Comparing the table structure of ``sbtest`.`sbtest96`` ... equivalent
Comparing the table structure of ``sbtest`.`sbtest99`` ... equivalent
Comparing the table data of ``sbtest`.`sbtest96`` ... failure
Comparing the table data of ``sbtest`.`sbtest99`` ... failure
_____________________________________________________________________________
Progress [============================================================>] 100% 0/0
The data of `sbtest`.`sbtest99` is not equal
The data of `sbtest`.`sbtest96` is not equal

The rest of tables are all equal.
The patch file has been generated in
        'output/fix-on-tidb2/'
You can view the comparision details through 'output/sync_diff.log'
```

### 出力ファイル {#output-file}

出力ファイルのディレクトリ構造は次のとおりです。

```
output/
|-- checkpoint # Saves the breakpoint information
| |-- bbfec8cc8d1f58a5800e63aa73e5 # Config hash. The placeholder file which identifies the configuration file corresponding to the output directory (output/)
│ |-- DO_NOT_EDIT_THIS_DIR
│ └-- sync_diff_checkpoints.pb # The breakpoint information
|
|-- fix-on-target # Saves SQL files to fix data inconsistency
| |-- xxx.sql
| |-- xxx.sql
| └-- xxx.sql
|
|-- summary.txt # Saves the summary of the check results
└-- sync_diff.log # Saves the output log informatiion when sync-diff-inspector is running
```

### ログ {#log}

sync-diff-inspectorのログは`${output}/sync_diff.log`に保存され、そのうち`${output}`は`config.toml`ファイルの`output-dir`の値です。

### 進捗 {#progress}

実行中のsync-diff-inspectorは、定期的に（10秒ごとに）チェックポイントの進行状況を出力します。チェックポイントは`${output}/checkpoint/sync_diff_checkpoints.pb`にあり、そのうち`${output}`は`config.toml`ファイルの`output-dir`の値です。

### 結果 {#result}

チェックが終了すると、sync-diff-inspectorはレポートを出力します。これは`${output}/summary.txt`にあり、 `${output}`は`config.toml`ファイルの`output-dir`の値です。

```summary
+---------------------+--------------------+----------------+
|        TABLE        | STRUCTURE EQUALITY | DATA DIFF ROWS |
+---------------------+--------------------+----------------+
| `sbtest`.`sbtest99` | true               | +97/-97        |
| `sbtest`.`sbtest96` | true               | +0/-101        |
+---------------------+--------------------+----------------+
Time Cost: 16.75370462s
Average Speed: 113.277149MB/s
```

-   TABLE：対応するデータベースとテーブルの名前

-   構造の同等性：テーブルの構造が同じかどうかを確認します

-   データ差分`rowDelete` ： `rowAdd` 。テーブルを修正するために追加/削除する必要がある行数を示します

### 一貫性のないデータを修正するSQLステートメント {#sql-statements-to-fix-inconsistent-data}

データチェックプロセス中に異なる行が存在する場合、それらを修正するためにSQLステートメントが生成されます。データの不整合がチャンクに存在する場合、 `chunk.Index`という名前のSQLファイルが生成されます。 SQLファイルは`${output}/fix-on-${instance}`にあり、 `${instance}`は`config.toml`ファイルの`task.target-instance`の値です。

SQLファイルには、チャンクが属する物語と範囲情報が含まれています。 SQLファイルの場合、次の3つの状況を考慮する必要があります。

-   ダウンストリームデータベースの行が欠落している場合、REPLACEステートメントが適用されます
-   ダウンストリームデータベースの行が冗長である場合、DELETEステートメントが適用されます
-   ダウンストリームデータベースの行の一部のデータに一貫性がない場合、REPLACEステートメントが適用され、一貫性のない列にSQLファイルの注釈が付けられます。

```SQL
-- table: sbtest.sbtest99
-- range in sequence: (3690708) < (id) <= (3720581)
/*
  DIFF COLUMNS ╏   `K`   ╏                `C`                 ╏               `PAD`
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
  source data  ╏ 2501808 ╏ 'hello'                            ╏ 'world'
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
  target data  ╏ 5003616 ╏ '0709824117-9809973320-4456050422' ╏ '1714066100-7057807621-1425865505'
╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╋╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍
*/
REPLACE INTO `sbtest`.`sbtest99`(`id`,`k`,`c`,`pad`) VALUES (3700000,2501808,'hello','world');
```

## ノート {#note}

-   sync-diff-inspectorは、データをチェックするときに一定量のサーバーリソースを消費します。ピーク営業時間中にデータをチェックするためにsync-diff-inspectorを使用することは避けてください。
-   MySQLのデータをTiDBのデータと比較する前に、テーブルの照合順序構成に注意してください。主キーまたは一意キーが`varchar`タイプであり、MySQLの照合順序構成がTiDBの構成と異なる場合、照合順序の問題が原因で最終チェック結果が正しくない可能性があります。 sync-diff-inspector構成ファイルに照合順序を追加する必要があります。
-   sync-diff-inspectorは、最初にTiDB統計に従ってデータをチャンクに分割し、統計の精度を保証する必要があります。 TiDBサーバーの*ワークロードが軽い*場合は、 `analyze table {table_name}`コマンドを手動で実行できます。
-   `table-rules`に特に注意してください。 `schema-pattern="test1"` 、および`table-pattern = "t_1"`を`target-table = "t_2"`する`test1` `target-schema="test2"`ソースデータベースの`t_1`スキーマと`test2` 。ターゲットデータベースの`t_2`のスキーマが比較されます。シャーディングはsync-diff-inspectorでデフォルトで有効になっているため、ソースデータベースに`test2`がある場合。 `t_2`テーブル、 `test1` 。 `t_1`テーブルと`test2` 。シャーディングとして機能するソースデータベースの`t_2`テーブルが`test2`と比較されます。ターゲットデータベースの`t_2`テーブル。
-   生成されたSQLファイルは、データを修復するための参照としてのみ使用され、データを修復するためにこれらのSQLステートメントを実行する前に確認する必要があります。
