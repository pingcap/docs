---
title: sync-diff-inspector User Guide
summary: sync-diff-inspectorを使用してデータを比較し、不整合なデータを修復します。
---

# sync-diff-inspector ユーザーガイド {#sync-diff-inspector-user-guide}

[同期差分検査ツール](https://github.com/pingcap/tiflow/tree/master/sync_diff_inspector)は、データベースに保存されているデータをMySQLプロトコルと比較するためのツールです。例えば、MySQLのデータとTiDBのデータ、MySQLのデータとMySQLのデータ、またはTiDBのデータとTiDBのデータを比較できます。さらに、少量のデータに不整合がある場合、このツールを使用してデータを修復することもできます。

このガイドでは、sync-diff-inspectorの主な機能を紹介し、このツールの設定方法と使用方法について説明します。

## 主な機能 {#key-features}

-   テーブルスキーマとデータを比較する
-   データ不整合が存在する場合に、データ修復に使用するSQLステートメントを生成します。
-   サポート[スキーマ名またはテーブル名が異なるテーブルのデータチェック](/sync-diff-inspector/route-diff.md)
-   Support[シャーディングシナリオにおけるデータチェック](/sync-diff-inspector/shard-diff.md)
-   [TiDBアップストリーム/ダウンストリームクラスタのデータチェック](/ticdc/ticdc-upstream-downstream-check.md)サポート
-   Support [DMレプリケーションシナリオにおけるデータチェック](/sync-diff-inspector/dm-diff.md)

## sync-diff-inspectorをインストールしてください。 {#install-sync-diff-inspector}

インストール方法は、TiDBのバージョンによって異なります。

TiDB v8.5.6以降の場合：

-   TiUPを使用してインストールしてください：

    ```shell
    tiup install sync-diff-inspector
    ```

-   バイナリ パッケージ: TiDB Toolkitに含まれています。ツールキットをダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。

-   Dockerイメージ：以下のコマンドを実行してダウンロードしてください。

    ```shell
    docker pull pingcap/sync-diff-inspector:latest
    ```

バージョン8.5.6より前のバージョンの場合：

-   バイナリ パッケージ: TiDB Toolkitに含まれています (従来の[`tidb-tools`](https://github.com/pingcap/tidb-tools)リポジトリから)。ツールキットをダウンロードするには、 [TiDBツールをダウンロード](/download-ecosystem-tools.md)参照してください。

-   Dockerイメージ（旧バージョン）：以下のコマンドを実行してダウンロードしてください。

    ```shell
    docker pull pingcap/tidb-tools:latest
    ```

## sync-diff-inspectorの制限事項 {#restrictions-of-sync-diff-inspector}

-   MySQL と TiDB 間のデータ移行では、オンラインチェックはサポートされていません。アップストリーム/ダウンストリームチェックリストにデータが書き込まれていないこと、および特定の範囲のデータが変更されていないことを確認してください。 `range`を設定することで、この範囲のデータをチェックできます。

-   TiDB と MySQL では、 `FLOAT` 、 `DOUBLE`およびその他の浮動小数点型の実装が異なります。 `FLOAT`と`DOUBLE`は、それぞれチェックサムの計算に 6 桁と 15 桁の有効数字を使用します。この機能を使用しない場合は、 `ignore-columns`を設定して、これらの列のチェックをスキップしてください。

-   主キーまたは一意インデックスを含まないテーブルのチェックをサポートします。ただし、データに矛盾がある場合、生成されたSQL文ではデータを正しく修復できない可能性があります。

## sync-diff-inspector のデータベース権限 {#database-privileges-for-sync-diff-inspector}

テーブルスキーマにアクセスしてデータをクエリするには、sync-diff-inspector は特定のデータベース権限を必要とします。アップストリームデータベースとダウンストリームデータベースの両方で、以下の権限を付与してください。

-   `SELECT` : データを比較するために必要です。
-   `RELOAD` : テーブルスキーマを表示するために必要です。
-   `PROCESS` : アップストリームとダウンストリームの両方が TiDB クラスタである場合に必須です。これは`INFORMATION_SCHEMA.CLUSTER_INFO`テーブルをクエリするために使用されます。

> **注記**：
>
> -   すべてのデータベースに対して[`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md)権限を付与**しないでください**( `*.*` )。そうしないと、sync-diff-inspector がアクセスできないデータベースにアクセスしようとしてエラーが発生します。
> -   MySQLデータソースの場合、 [`skip_show_database`](https://dev.mysql.com/doc/refman/8.4/en/server-system-variables.html#sysvar_skip_show_database)システム変数が`OFF`に設定されていることを確認してください。この変数が`ON`に設定されている場合、チェックが失敗する可能性があります。

## コンフィグレーションファイルの説明 {#configuration-file-description}

sync-diff-inspectorの設定は、以下の部分から構成されます。

-   `Global config` : 一般的な設定。チェックするスレッド数、不整合なテーブルを修正するために SQL ステートメントをエクスポートするかどうか、データを比較するかどうか、上流または下流に存在しないテーブルのチェックをスキップするかどうかなど。
-   `Databases config` : アップストリームおよびダウンストリームのデータベースのインスタンスを設定します。
-   `Routes` : 上流の複数のスキーマ名が下流の単一のスキーマ名と一致するようにするためのルール**(オプション)** 。
-   `Task config` : チェック対象のテーブルを設定します。一部のテーブルが上流データベースと下流データベース間で特定のマッピング関係を持っている場合、または特別な要件がある場合は、これらのテーブルを設定する必要があります。
-   `Table config` : 特定のテーブルに対する特別な設定。例えば、無視する範囲や列を指定する**（オプション）** 。

以下に、完全な設定ファイルの説明を示します。

-   注: 名前の後に`s`が付いている設定には複数の値が含まれる可能性があるため、設定値を含めるには角括弧`[]`を使用する必要があります。

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

## sync-diff-inspector を実行します {#run-sync-diff-inspector}

以下のコマンドを実行してください。

```bash
./sync_diff_inspector --config=./config.toml
```

このコマンドは`summary.txt`の`output-dir`にチェック レポート`config.toml`とログ`sync_diff.log`を出力します。また、 `output-dir` }} には、 `config. toml`ファイルのハッシュ値で命名されたフォルダも生成されます。このフォルダには、ブレークポイントのチェックポイント ノード情報と、データに不整合が生じた場合に生成される SQL ファイルが含まれます。

### 進捗状況 {#progress-information}

sync-diff-inspector は実行時に`stdout`に進行状況情報を送信します。進行状況情報には、テーブル構造の比較結果、テーブルデータの比較結果、およびプログレスバーが含まれます。

> **注記：**
>
> 表示効果を確保するため、表示ウィンドウの幅は80文字以上にしてください。

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

出力ファイルのディレクトリ構造は以下のとおりです。

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

sync-diff-inspector のログは`${output}/sync_diff.log`に保存され、その中で`${output}`は`output-dir`ファイル内の`config.toml`の値です。

### 進捗 {#progress}

実行中の sync-diff-inspector は定期的に (10 秒ごと) チェックポイントの進行状況を出力。チェックポイントは`${output}/checkpoint/sync_diff_checkpoints.pb`にあり、その中で`${output}`は`output-dir`ファイル内の`config.toml`の値です。

### 結果 {#result}

チェックが完了すると、sync-diff-inspector はレポートを出力します。レポートは`${output}/summary.txt`にあり、 `${output}`は`output-dir`ファイル内の`config.toml` } の値です。

    +---------------------+--------------------+----------------+---------+-----------+
    |        TABLE        | STRUCTURE EQUALITY | DATA DIFF ROWS | UPCOUNT | DOWNCOUNT |
    +---------------------+--------------------+----------------+---------+-----------+
    | `sbtest`.`sbtest99` | true               | +97/-97        |  999999 |    999999 |
    | `sbtest`.`sbtest96` | true               | +0/-101        |  999999 |   1000100 |
    +---------------------+--------------------+----------------+---------+-----------+
    Time Cost: 16.75370462s
    Average Speed: 113.277149MB/s

-   `TABLE` : 対応するデータベース名とテーブル名
-   `RESULT` : チェックが完了したかどうか。 `skip-non-existing-table = true`を設定している場合、上流または下流に存在しないテーブルでは、この列の値は`skipped`になります。
-   `STRUCTURE EQUALITY` : テーブル構造が同じかどうかを確認します
-   `DATA DIFF ROWS` : `rowAdd` / `rowDelete` 。テーブルを修正するために追加/削除する必要のある行数を示します。
-   `UPCOUNT` : アップストリームデータソースのこのテーブルの行数
-   `DOWNCOUNT` : 下流データソースにおけるこのテーブルの行数

### 不整合なデータを修正するためのSQLステートメント {#sql-statements-to-fix-inconsistent-data}

データチェック処理中に異なる行が存在する場合、それらを修正するための SQL ステートメントが生成されます。データの不整合がチャンク内に存在する場合、 `chunk.Index`という名前の SQL ファイルが生成されます。この SQL ファイルは`${output}/fix-on-${instance}`にあり、 `${instance}`は`task.target-instance`ファイル内の`config.toml`の値です。

SQLファイルには、チャンクが属するテーブルと範囲情報が含まれています。SQLファイルについては、次の3つの状況を考慮する必要があります。

-   下流データベースに該当する行が欠落している場合、REPLACE文が適用されます。
-   下流データベースの行が冗長な場合、DELETE文が適用されます。
-   下流データベースの行データの一部に不整合がある場合、REPLACE文が適用され、不整合な列はSQLファイル内で注釈付きでマークされます。

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

-   sync-diff-inspectorは、データチェック時に一定量のサーバーリソースを消費します。業務のピーク時間帯には、sync-diff-inspectorを使用してデータチェックを行うことは避けてください。
-   MySQL のデータと TiDB のデータを比較する前に、テーブルの文字セットと`collation`構成を確認してください。これは、テーブルの主キーまたは一意キーが`varchar`型である場合に特に重要です。上流データベースと下流データベースで照合順序ルールが異なると、ソートの問題が発生し、検証結果が不正確になる可能性があります。たとえば、MySQL のデフォルトの照合順序は大文字小文字を区別しませんが、TiDB のデフォルトの照合順序は大文字小文字を区別します。この不一致により、修復 SQL で同一の削除レコードと挿入レコードが発生する可能性があります。この問題を回避するには、 `index-fields`構成を使用して、大文字小文字の区別に影響されないインデックス列を指定します。 sync-diff-inspector 設定ファイルで`collation`を設定し、チャンクベースの比較時にアップストリームとダウンストリームの両方で同じ照合順序を明示的に使用する場合、インデックス フィールドの順序はテーブルの照合順序設定に依存することに注意してください。照合順序が異なると、一方の側でインデックスを使用できなくなる可能性があります。さらに、アップストリームとダウンストリームで文字セットが異なる場合 (たとえば、MySQL が UTF-8 を使用し、TiDB が UTF-8MB4 を使用する場合)、照合順序設定を統一することはできません。
-   アップストリームテーブルとダウンストリームテーブルで主キーが異なる場合、sync-diff-inspector は元の主キー列を使用してチャンクを分割しません。たとえば、MySQL のシャーディングされたテーブルが、元の主キーとシャードキーを含む複合主キーを使用して TiDB にマージされる場合などです。この場合、 `index-fields`を使用して元の主キー列を構成し、 `check-data-only`を`true`に設定します。
-   sync-diff-inspector は、まず TiDB の統計情報に基づいてデータをチャンクに分割します。統計情報の正確性を保証する必要があります。TiDB サーバーの*ワークロードが軽い*場合は、 `analyze table {table_name}`コマンドを手動で実行できます。
-   `table-rules`に特に注意してください。 `schema-pattern="test1"` 、 `table-pattern = "t_1"` 、 `target-schema="test2"` 、 `target-table = "t_2"`構成すると、ソース データベースの`test1` 、 `t_1`スキーマと、ターゲット データベースの`test2` 、 `t_2`スキーマが比較されます。 sync-diff-inspector ではシャーディングがデフォルトで有効になっているため、ソース データベースに`test2` . `t_2`テーブルがある場合、シャーディングとして機能しているソース データベースの`test1` . `t_1`テーブルと`test2` . `t_2`テーブルが、ターゲット データベースの`test2` . `t_2`テーブルと比較されます。
-   生成されたSQLファイルは、データ修復の際の参照としてのみ使用されます。データ修復のためにこれらのSQL文を実行する前に、必ず内容を確認してください。
