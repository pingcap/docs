---
title: sync-diff-inspector User Guide
summary: sync-diff-inspector を使用してデータを比較し、不一致なデータを修復します。
---

# sync-diff-inspector ユーザーガイド {#sync-diff-inspector-user-guide}

[同期差分インスペクター](https://github.com/pingcap/tidb-tools/tree/master/sync_diff_inspector)は、MySQLプロトコルを使用してデータベースに保存されたデータを比較するためのツールです。例えば、MySQLのデータとTiDBのデータ、MySQLのデータとMySQLのデータ、TiDBのデータとTiDBのデータを比較できます。また、少量のデータに不整合がある場合の修復にも使用できます。

このガイドでは、sync-diff-inspector の主な機能を紹介し、このツールの設定方法と使用方法について説明します。sync-diff-inspector をダウンロードするには、以下のいずれかの方法を使用してください。

-   バイナリパッケージ。sync-diff-inspectorバイナリパッケージはTiDB Toolkitに含まれています。TiDBTiDB Toolkitをダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。
-   Dockerイメージ。ダウンロードするには、次のコマンドを実行します。

    ```shell
    docker pull pingcap/tidb-tools:latest
    ```

## 主な特徴 {#key-features}

-   テーブルスキーマとデータを比較する
-   データの不整合が存在する場合にデータを修復するために使用されるSQL文を生成します。
-   サポート[異なるスキーマまたはテーブル名を持つテーブルのデータチェック](/sync-diff-inspector/route-diff.md)
-   サポート[シャーディングシナリオにおけるデータチェック](/sync-diff-inspector/shard-diff.md)
-   サポート[TiDB 上流下流クラスターのデータチェック](/ticdc/ticdc-upstream-downstream-check.md)
-   サポート[DMレプリケーションシナリオにおけるデータチェック](/sync-diff-inspector/dm-diff.md)

## sync-diff-inspector の制限 {#restrictions-of-sync-diff-inspector}

-   MySQLとTiDB間のデータ移行では、オンラインチェックはサポートされていません。上流・下流チェックリストにデータが書き込まれていないこと、および特定の範囲のデータが変更されていないことを確認してください`range`を設定することで、この範囲のデータをチェックできます。

-   TiDBとMySQLでは、 `FLOAT` `DOUBLE`およびその他の浮動小数点型の実装が異なります。5と`DOUBLE` `FLOAT`チェックサムの計算にそれぞれ6桁と15桁の有効桁数を使用します。この機能を使用しない場合は、 `ignore-columns`を設定してこれらの列のチェックをスキップしてください。

-   主キーまたは一意のインデックスを含まないテーブルのチェックをサポートします。ただし、データに不整合がある場合、生成されたSQL文でデータを正しく修復できない可能性があります。

## sync-diff-inspector のデータベース権限 {#database-privileges-for-sync-diff-inspector}

テーブルスキーマにアクセスし、データをクエリするには、sync-diff-inspector に特定のデータベース権限が必要です。上流データベースと下流データベースの両方に以下の権限を付与してください。

-   `SELECT` : データを比較するために必要です。
-   `RELOAD` : テーブル スキーマを表示するために必要です。
-   `PROCESS` : アップストリームとダウンストリームの両方がTiDBクラスタの場合に必須。2 `INFORMATION_SCHEMA.CLUSTER_INFO`テーブルをクエリするために使用されます。

> **注記**：
>
> -   すべてのデータベース（ `*.*` ）に[`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md)権限を付与**しないでください**。そうしないと、sync-diff-inspectorはアクセスできないデータベースにアクセスしようとし、エラーが発生します。
> -   MySQLデータソースの場合、システム変数[`skip_show_database`](https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_skip_show_database) `OFF`に設定されていることを確認してください。この変数が`ON`に設定されていると、チェックが失敗する可能性があります。

## コンフィグレーションファイルの説明 {#configuration-file-description}

sync-diff-inspector の構成は次の部分で構成されます。

-   `Global config` : チェックするスレッド数、不一致なテーブルを修正するために SQL ステートメントをエクスポートするかどうか、データを比較するかどうか、上流または下流に存在しないテーブルのチェックをスキップするかどうかなどの一般的な構成。
-   `Databases config` : アップストリーム データベースとダウンストリーム データベースのインスタンスを構成します。
-   `Routes` : 上流の複数のスキーマ名が下流の単一のスキーマ名と一致するようにするためのルール**(オプション)** 。
-   `Task config` : チェック対象テーブルを設定します。一部のテーブルが上流データベースと下流データベース間で特定のマッピング関係にある場合、または特別な要件がある場合は、これらのテーブルを設定する必要があります。
-   `Table config` : 指定された範囲や無視される列など、特定のテーブルに対する特別な構成**(オプション)** 。

以下に完全な構成ファイルの説明を示します。

-   注意: 名前の後に`s`が付く構成には複数の値が含まれる可能性があるため、構成値を含めるには角括弧`[]`使用する必要があります。

```toml
# Diff Configuration.

######################### Global config #########################
# The number of goroutines created to check data. The number of connections between sync-diff-inspector and upstream/downstream databases is slightly greater than this value.
check-thread-count = 4

# If enabled, SQL statements is exported to fix inconsistent tables.
export-fix-sql = true

# Only compares the data instead of the table structure. This configuration item is an experimental feature. It is not recommended that you use it in the production environment.
check-data-only = false

# Only compares the table structure instead of the data.
check-struct-only = false

# If enabled, sync-diff-inspector skips checking tables that do not exist in the upstream or downstream.
skip-non-existing-table = false

######################### Datasource config #########################
[data-sources]
[data-sources.mysql1] # mysql1 is the only custom ID for the database instance. It is used for the following `task.source-instances/task.target-instance` configuration.
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""  # The password for connecting to the upstream database. It can be plain text or Base64-encoded.

    # (optional) Use mapping rules to match multiple upstream sharded tables. Rule1 and rule2 are configured in the following Routes section.
    route-rules = ["rule1", "rule2"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""  # The password for connecting to the downstream database. It can be plain text or Base64-encoded.

    # (optional) Use TLS to connect TiDB.
    # security.ca-path = ".../ca.crt"
    # security.cert-path = ".../cert.crt"
    # security.key-path = ".../key.crt"

    # (optional) Use the snapshot feature. If enabled, historical data is used for comparison.
    # snapshot = "386902609362944000"
    # When "snapshot" is set to "auto", the last syncpoints generated by TiCDC in the upstream and downstream are used for comparison. For details, see <https://github.com/pingcap/tidb-tools/issues/663>.
    # snapshot = "auto"

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

## sync-diff-inspectorを実行する {#run-sync-diff-inspector}

次のコマンドを実行します。

```bash
./sync_diff_inspector --config=./config.toml
```

このコマンドは、 `config.toml`の`output-dir`にチェックレポート`summary.txt`とログ`sync_diff.log`を出力します。また、 `output-dir`には、 `config. toml`ファイルのハッシュ値で命名されたフォルダが生成されます。このフォルダには、ブレークポイントのチェックポイントノード情報と、データに不整合が発生した際に生成されたSQLファイルが含まれます。

### 進捗情報 {#progress-information}

sync-diff-inspector は実行時に進捗情報を`stdout`に送信します。進捗情報には、テーブル構造の比較結果、テーブルデータの比較結果、およびプログレスバーが含まれます。

> **注記：**
>
> 表示効果を確実にするために、表示ウィンドウの幅は 80 文字以上にしてください。

    A total of 2 tables need to be compared

    Comparing the table structure of ``sbtest`.`sbtest96`` ... equivalent
    Comparing the table structure of ``sbtest`.`sbtest99`` ... equivalent
    Comparing the table data of ``sbtest`.`sbtest96`` ... failure
    Comparing the table data of ``sbtest`.`sbtest99`` ...
    _____________________________________________________________________________
    Progress [==========================================================>--] 98% 193/200

<!---->

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

    A total of 2 tables have been compared, 0 tables finished, 2 tables failed, 0 tables skipped.
    The patch file has been generated in
            'output/fix-on-tidb2/'
    You can view the comparison details through 'output/sync_diff.log'

### 出力ファイル {#output-file}

出力ファイルのディレクトリ構造は次のとおりです。

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
    └-- sync_diff.log # Saves the output log information when sync-diff-inspector is running

### ログ {#log}

sync-diff-inspector のログは`${output}/sync_diff.log`に保存されますが、そのうち`${output}` `config.toml`ファイルの`output-dir`の値です。

### 進捗 {#progress}

実行中の sync-diff-inspector は、定期的に (10 秒ごとに) チェックポイントの進行状況を出力。チェックポイントは`${output}/checkpoint/sync_diff_checkpoints.pb`にあり、そのうち`${output}` `config.toml`ファイルの`output-dir`の値です。

### 結果 {#result}

チェックが完了すると、sync-diff-inspector はレポートを出力します。レポートの値は`${output}/summary.txt`で、 `${output}` `config.toml`ファイルの`output-dir`の値です。

    +---------------------+--------------------+----------------+---------+-----------+
    |        TABLE        | STRUCTURE EQUALITY | DATA DIFF ROWS | UPCOUNT | DOWNCOUNT |
    +---------------------+--------------------+----------------+---------+-----------+
    | `sbtest`.`sbtest99` | true               | +97/-97        |  999999 |    999999 |
    | `sbtest`.`sbtest96` | true               | +0/-101        |  999999 |   1000100 |
    +---------------------+--------------------+----------------+---------+-----------+
    Time Cost: 16.75370462s
    Average Speed: 113.277149MB/s

-   `TABLE` : 対応するデータベース名とテーブル名
-   `RESULT` : チェックが完了したかどうか。2 `skip-non-existing-table = true`設定した場合、上流または下流に存在しないテーブルの場合、この列の値は`skipped`になります。
-   `STRUCTURE EQUALITY` : テーブル構造が同じかどうかをチェックする
-   `DATA DIFF ROWS` : `rowAdd` / `rowDelete` 。テーブルを修正するために追加/削除する必要がある行数を示します。
-   `UPCOUNT` : 上流データソース内のこのテーブルの行数
-   `DOWNCOUNT` : 下流データソース内のこのテーブルの行数

### 不整合なデータを修正するためのSQL文 {#sql-statements-to-fix-inconsistent-data}

データチェック処理中に異なる行が存在する場合、それらを修正するためのSQL文が生成されます。チャンク内にデータの不整合が存在する場合、 `chunk.Index`という名前のSQLファイルが生成されます。このSQLファイルは`${output}/fix-on-${instance}`に配置され、 `${instance}`は`config.toml`ファイルの`task.target-instance`の値です。

SQLファイルには、チャンクが属するテーブルと範囲情報が含まれています。SQLファイルでは、以下の3つの状況を考慮する必要があります。

-   下流データベースの行が欠落している場合は、REPLACE文が適用されます。
-   下流データベースの行が冗長な場合は、DELETE文が適用されます。
-   下流データベースの行の一部のデータが不整合の場合、REPLACE文が適用され、不整合のある列はSQLファイル内で注釈でマークされます。

```sql
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

## 注記 {#note}

-   sync-diff-inspector はデータチェック時に一定量のサーバーリソースを消費します。業務のピーク時間帯に sync-diff-inspector を使用してデータをチェックすることは避けてください。
-   MySQL のデータと TiDB のデータを比較する前に、テーブルの文字セットと`collation`設定を確認してください。これは、テーブルの主キーまたは一意のキーが`varchar`タイプの場合に特に重要です。上流データベースと下流データベース間で照合順序ルールが異なると、ソートの問題が発生し、検証結果が不正確になる可能性があります。たとえば、MySQL のデフォルトの照合順序では大文字と小文字が区別されませんが、TiDB のデフォルトの照合順序では大文字と小文字が区別されます。この不一致により、修復 SQL で同一の削除レコードと挿入レコードが発生する可能性があります。この問題を回避するには、 `index-fields`設定を使用して、大文字と小文字の区別の影響を受けないインデックス列を指定します。sync-diff-inspector 設定ファイルで`collation`設定し、チャンクベースの比較中に上流と下流の両方で明示的に同じ照合順序を使用する場合、インデックス フィールドの順序はテーブルの照合順序設定によって決まることに注意してください。照合が異なると、片側でインデックスを使用できない可能性があります。さらに、アップストリームとダウンストリームの文字セットが異なる場合 (たとえば、MySQL は UTF-8 を使用し、TiDB は UTF-8MB4 を使用する)、照合順序構成を統一することはできません。
-   上流テーブルと下流テーブルで主キーが異なる場合、sync-diff-inspectorは元の主キー列をチャンク分割に使用しません。例えば、MySQLのシャードテーブルを、元の主キーとシャードキーを含む複合主キーを使用してTiDBにマージする場合などです。この場合、元の主キー列を`index-fields`に設定し、 `check-data-only`を`true`に設定します。
-   sync-diff-inspector はまず TiDB 統計情報に基づいてデータをチャンクに分割します。統計情報の精度を保証する必要があります。TiDB サーバーの*負荷が低い*場合は、 `analyze table {table_name}`コマンドを手動で実行できます。
-   `table-rules`に特に注意してください。3、5、7、9 `schema-pattern="test1"`設定すると、ソースデータベースの`target-table = "t_2"` `test1` `t_1`スキーマとターゲットデータベースの`test2` . `t_2`スキーマ`target-schema="test2"`比較されます。sync-diff-inspector ではシャーディング`table-pattern = "t_1"`デフォルトで有効になっているため、ソースデータベースに`test2` . `t_2`テーブルがある場合、シャーディングとして機能するソースデータベースの`test1` . `t_1`テーブルと`test2` . `t_2`テーブルが、ターゲットデータベースの`test2` . `t_2`テーブルと比較されます。
-   生成された SQL ファイルは、データを修復するための参照としてのみ使用されるため、これらの SQL ステートメントを実行してデータを修復する前に確認する必要があります。
