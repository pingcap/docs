---
title: IMPORT INTO
summary: TiDB での IMPORT INTO の使用法の概要。
---

# インポート先 {#import-into}

`IMPORT INTO`ステートメントを使用すると、 TiDB Lightningの[物理インポートモード](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)を介して TiDB にデータをインポートできます。5 `IMPORT INTO`次の2つの方法で使用できます。

-   `IMPORT INTO ... FROM FILE` : `CSV`などの形式のデータ ファイル`SQL` `PARQUET`の空のテーブルにインポートします。
-   `IMPORT INTO ... FROM SELECT` : `SELECT`ステートメントのクエリ結果をTiDBの空のテーブルにインポートします。また、 [`AS OF TIMESTAMP`](/as-of-timestamp.md)でクエリされた履歴データをインポートすることもできます。

<CustomContent platform="tidb">

> **注記：**
>
> [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)と比較して、 `IMPORT INTO` TiDB ノード上で直接実行でき、自動化された分散タスクスケジューリングと[TiDB グローバルソート](/tidb-global-sort.md)サポートし、デプロイメント、リソース利用率、タスク設定の利便性、呼び出しと統合の容易さ、高可用性、スケーラビリティにおいて大幅な改善をもたらします。適切なシナリオでは、TiDB Lightningではなく`IMPORT INTO`使用を検討することをお勧めします。

</CustomContent>

## 制限 {#restrictions}

-   `IMPORT INTO` 、データベース内の既存の空のテーブルへのデータのインポートのみをサポートします。
-   `IMPORT INTO`では、同じテーブルの他のパーティションに既にデータが含まれている場合、空のパーティションへのデータのインポートはサポートされません。インポート操作を行うには、ターゲットテーブルが完全に空である必要があります。
-   `IMPORT INTO` 、 [一時テーブル](/temporary-tables.md)または[キャッシュされたテーブル](/cached-tables.md)へのデータのインポートをサポートしていません。
-   `IMPORT INTO` `END`やロールバックをサポートしていません。明示的なトランザクション（ `BEGIN` ）内で`IMPORT INTO`実行するとエラーが返されます。
-   `IMPORT INTO` 、 [バックアップと復元](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview) 、 [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) 、 [インデックス追加の高速化](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) 、 TiDB Lightningを使用したデータインポート、 TiCDC を使用したデータレプリケーション、 [ポイントインタイムリカバリ（PITR）](https://docs.pingcap.com/tidb/stable/br-log-architecture)などの機能との同時使用をサポートしていません。互換性に関する詳細は、 [TiDB Lightningと`IMPORT INTO`と TiCDC およびログバックアップとの互換性](https://docs.pingcap.com/tidb/stable/tidb-lightning-compatibility-and-scenarios)参照してください。
-   データのインポートプロセス中は、ターゲットテーブルに対してDDLまたはDML操作を実行しないでください。また、ターゲットデータベースに対して[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)実行しないでください。これらの操作は、インポートの失敗やデータの不整合につながる可能性があります。また、インポートプロセス中に読み取り操作を実行することは推奨**されません**。読み取り操作と書き込み操作は、インポートが完了した後にのみ実行してください。
-   インポートプロセスはシステムリソースを大量に消費します。TiDB Self-Managedでは、パフォーマンスを向上させるために、少なくとも32コアと64GiBのメモリを搭載したTiDBノードの使用を推奨します。TiDBはインポート時にソートされたデータをTiDB [一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)に書き込むため、フラッシュメモリなどの高性能storageメディアをTiDB Self-Managed用に構成することをお勧めします。詳細については、 [物理インポートモードの制限](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode#requirements-and-restrictions)参照してください。
-   TiDB Self-Managedの場合、TiDB [一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)は少なくとも90GiBの空き容量が必要です。インポートするデータの量と同等以上のstorage容量を割り当てることをお勧めします。
-   1 つのインポート ジョブでは、1 つのターゲット テーブルへのデータのインポートのみがサポートされます。
-   TiDB クラスターのアップグレード中は`IMPORT INTO`はサポートされません。
-   インポートするデータに、主キーまたは非NULLの一意のインデックスの競合を持つレコードが含まれていないことを確認してください。競合がある場合、インポートタスクが失敗する可能性があります。
-   既知の問題：TiDBノード構成ファイル内のPDアドレスがクラスタの現在のPDトポロジと一致していない場合、タスク`IMPORT INTO`失敗する可能性があります。この不一致は、PDが以前にスケールインされたにもかかわらず、TiDB構成ファイルがそれに応じて更新されていなかった場合や、構成ファイルの更新後にTiDBノードが再起動されていなかった場合などに発生する可能性があります。

### <code>IMPORT INTO ... FROM FILE</code>制限 {#code-import-into-from-file-code-restrictions}

-   TiDBセルフマネージドの場合、 `IMPORT INTO`タスクあたり10TiB以内のデータのインポートをサポートします。3機能を有効にすると、 [グローバルソート](/tidb-global-sort.md)タスク`IMPORT INTO` 40TiB以内のデータのインポートをサポートします。
-   [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)について、インポートするデータが 500 GiB を超える場合は、少なくとも 16 コアの TiDB ノードを使用し、 [グローバルソート](/tidb-global-sort.md)機能を有効にすることを推奨します。これにより、 `IMPORT INTO`タスクごとに 40 TiB 以内のデータのインポートがサポートされます。インポートするデータが 500 GiB 以内の場合、または TiDB ノードのコア数が 16 未満の場合、 [グローバルソート](/tidb-global-sort.md)機能を有効にすることは推奨されません。
-   `IMPORT INTO ... FROM FILE`を実行すると、インポートが完了するまで現在の接続がブロックされます。ステートメントを非同期で実行するには、 `DETACHED`オプションを追加できます。
-   各クラスターでは最大16 `IMPORT INTO`タスクを同時に実行できます（ [TiDB 分散実行フレームワーク (DXF) の使用制限](/tidb-distributed-execution-framework.md#limitation)参照）。クラスターのリソースが不足している場合、またはタスクの最大数に達した場合、新たに送信されたインポートタスクは実行キューに追加されます。
-   データのインポートに[グローバルソート](/tidb-global-sort.md)機能を使用する場合、 `THREAD`オプションの値は少なくとも`8`ある必要があります。
-   [グローバルソート](/tidb-global-sort.md)機能をデータのインポートに使用する場合、エンコード後の 1 行のデータ サイズは 32 MiB を超えてはなりません。
-   [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)有効化されていない場合に作成される`IMPORT INTO`タスクはすべて、タスクが送信されたノードで直接実行されます。これらのタスクは、後で DXF が有効化された後も、他の TiDB ノードで実行するようにスケジュールされません。DXF が有効化されると、S3 または GCS からデータをインポートする新規作成された`IMPORT INTO`タスクのみが、他の TiDB ノードに自動的にスケジュールまたはフェイルオーバーされて実行されます。

### <code>IMPORT INTO ... FROM SELECT</code>制限 {#code-import-into-from-select-code-restrictions}

-   `IMPORT INTO ... FROM SELECT` 、現在のユーザーが接続している TiDB ノードでのみ実行でき、インポートが完了するまで現在の接続をブロックします。
-   `IMPORT INTO ... FROM SELECT` [インポートオプション](#withoptions) : `THREAD`と`DISABLE_PRECHECK` 2 つだけをサポートします。
-   `IMPORT INTO ... FROM SELECT` 、 `SHOW IMPORT JOB(s)`や`CANCEL IMPORT JOB <job-id>`などのタスク管理ステートメントをサポートしていません。
-   TiDB の[一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)は、 `SELECT`ステートメントのクエリ結果全体を格納するのに十分なスペースが必要です ( `DISK_QUOTA`オプションの構成は現在サポートされていません)。
-   [`tidb_snapshot`](/read-historical-data.md)使用した履歴データのインポートはサポートされていません。
-   `SELECT`節の構文は複雑なため、 `IMPORT INTO`の`WITH`パラメータが 1 節と競合し、 `GROUP BY ... [WITH ROLLUP]`ような解析エラーが発生する可能性があります。複雑な`SELECT`文についてはビューを作成し、インポートには`IMPORT INTO ... FROM SELECT * FROM view_name`使用することをお勧めします。あるいは、 `SELECT`のスコープを`IMPORT INTO ... FROM (SELECT ...) WITH ...`ように括弧で囲んで明確にすることもできます。

## インポートの前提条件 {#prerequisites-for-import}

`IMPORT INTO`使用してデータをインポートする前に、次の要件が満たされていることを確認してください。

-   インポート対象のテーブルはすでに TiDB に作成されており、空です。
-   ターゲット クラスターには、インポートするデータを保存するのに十分なスペースがあります。
-   TiDBセルフマネージドの場合、現在のセッションに接続されているTiDBノードの[一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) 90GiB以上の空き容量が必要です[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)が有効で、インポートデータがS3またはGCSから取得されている場合は、クラスター内の各TiDBノードの一時ディレクトリに十分なディスク容量があることを確認してください。

## 必要な権限 {#required-privileges}

`IMPORT INTO`実行するには、対象テーブルに対する`SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、 `ALTER`権限が必要です。TiDB ローカルstorageにファイルをインポートするには、 `FILE`権限も必要です。

## 概要 {#synopsis}

```ebnf+diagram
ImportIntoStmt ::=
    'IMPORT' 'INTO' TableName ColumnNameOrUserVarList? SetClause? FROM fileLocation Format? WithOptions?
    |
    'IMPORT' 'INTO' TableName ColumnNameList? FROM SelectStatement WithOptions?

ColumnNameOrUserVarList ::=
    '(' ColumnNameOrUserVar (',' ColumnNameOrUserVar)* ')'

ColumnNameList ::=
    '(' ColumnName (',' ColumnName)* ')'

SetClause ::=
    'SET' SetItem (',' SetItem)*

SetItem ::=
    ColumnName '=' Expr

Format ::=
    'CSV' | 'SQL' | 'PARQUET'

WithOptions ::=
    'WITH' OptionItem (',' OptionItem)*

OptionItem ::=
    optionName '=' optionVal | optionName
```

## パラメータの説明 {#parameter-description}

### 列名またはユーザー変数リスト {#columnnameoruservarlist}

データファイル内の各フィールドがターゲットテーブルの列とどのように対応するかを指定します。また、フィールドを変数にマッピングしてインポート時に特定のフィールドをスキップしたり、 `SetClause`で使用したりすることもできます。

-   このパラメータを指定しない場合は、データ ファイルの各行のフィールド数がターゲット テーブルの列数と一致する必要があり、フィールドは対応する列に順番にインポートされます。
-   このパラメータを指定する場合、指定された列または変数の数は、データ ファイルの各行のフィールドの数と一致する必要があります。

### SetClause {#setclause}

対象列の値の計算方法を指定します。1 `SET`の右側では、 `ColumnNameOrUserVarList`で指定した変数を参照できます。

`SET`式の左側では、 `ColumnNameOrUserVarList`に含まれない列名のみを参照できます。対象の列名が`ColumnNameOrUserVarList`に既に存在する場合、 `SET`式は無効です。

### ファイルの場所 {#filelocation}

データ ファイルのstorage場所を指定します。Amazon S3 または GCS URI パス、あるいは TiDB ローカル ファイル パスを指定できます。

-   Amazon S3 または GCS URI パス: URI 設定の詳細については、 [外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

-   TiDBローカルファイルパス：絶対パスで、ファイル拡張子は`.csv` 、 `.sql` 、または`.parquet`である必要があります。このパスに対応するファイルが、現在のユーザーが接続しているTiDBノードに保存されていること、およびユーザーが`FILE`権限を持っていることを確認してください。

> **注記：**
>
> ターゲット クラスターで[SEM](/system-variables.md#tidb_enable_enhanced_security)有効になっている場合、 `fileLocation`ローカル ファイル パスとして指定することはできません。

`fileLocation`のパラメータでは、単一のファイルを指定するか、 `*`と`[]`ワイルドカードを使用して複数のファイルをインポート対象として指定できます。ワイルドカードはディレクトリやサブディレクトリ内のファイルとは一致しないため、ファイル名にのみ使用できます。Amazon S3に保存されているファイルを例にとると、パラメータは次のように設定できます。

-   1つのファイルをインポートする: `s3://<bucket-name>/path/to/data/foo.csv`
-   指定されたパス内のすべてのファイルをインポート: `s3://<bucket-name>/path/to/data/*`
-   指定されたパス内のサフィックスが`.csv`であるすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/*.csv`
-   指定されたパス内のプレフィックスが`foo`であるすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/foo*`
-   指定されたパスにある、プレフィックスが`foo` 、サフィックスが`.csv`すべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/foo*.csv`
-   指定されたパスに`1.csv`と`2.csv`インポート: `s3://<bucket-name>/path/to/data/[12].csv`

### 形式 {#format}

`IMPORT INTO`ステートメントは、 `CSV` 、 `SQL` 、 `PARQUET`の3つのデータファイル形式をサポートします。指定されていない場合は、デフォルトの形式は`CSV`です。

### オプション付き {#withoptions}

`WithOptions`使用すると、インポートオプションを指定し、データのインポートプロセスを制御できます。例えば、バックエンドでデータファイルのインポートを非同期に実行するには、 `IMPORT INTO`ステートメントに`WITH DETACHED`オプションを追加することで、インポートに`DETACHED`モードを有効にできます。

サポートされているオプションは次のとおりです。

| オプション名                              | サポートされているデータソースと形式      | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| :---------------------------------- | :---------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CHARACTER_SET='<string>'`          | CSV                     | データファイルの文字セットを指定します。デフォルトの文字セットは`utf8mb4`です。サポートされている文字セットは`binary` 、 `utf8` 、 `utf8mb4` 、 `gb18030` 、 `gbk` 、 `latin1` 、 `ascii`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `FIELDS_TERMINATED_BY='<string>'`   | CSV                     | フィールドセパレーターを指定します。デフォルトのセパレーターは`,`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `FIELDS_ENCLOSED_BY='<char>'`       | CSV                     | フィールド区切り文字を指定します。デフォルトの区切り文字は`"`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `FIELDS_ESCAPED_BY='<char>'`        | CSV                     | フィールドのエスケープ文字を指定します。デフォルトのエスケープ文字は`\`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `FIELDS_DEFINED_NULL_BY='<string>'` | CSV                     | フィールド内で`NULL`を表す値を指定します。デフォルト値は`\N`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `LINES_TERMINATED_BY='<string>'`    | CSV                     | 行末文字を指定します。デフォルトでは、 `IMPORT INTO`指定すると、 `\n` 、 `\r` 、または`\r\n`行末文字として自動的に識別されます。行末文字がこれら3つのいずれかである場合は、このオプションを明示的に指定する必要はありません。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `SKIP_ROWS=<number>`                | CSV                     | スキップする行数を指定します。デフォルト値は`0`です。このオプションを使用すると、CSVファイルのヘッダーをスキップできます。インポートするソースファイルをワイルドカードで指定する場合、このオプションは`fileLocation`のワイルドカードに一致するすべてのソースファイルに適用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `SPLIT_FILE`                        | CSV                     | 単一のCSVファイルを約256MiBの複数の小さなチャンクに分割し、並列処理することでインポート効率を向上させます。このパラメータは**非圧縮**CSVファイルに対してのみ機能し、 TiDB Lightning [`strict-format`](https://docs.pingcap.com/tidb/stable/tidb-lightning-data-source#strict-format)と同じ使用制限があります。このオプションには明示的に`LINES_TERMINATED_BY`指定する必要があります。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `DISK_QUOTA='<string>'`             | すべてのファイル形式              | データのソート時に使用できるディスク容量のしきい値を指定します。デフォルト値はTiDB [一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)のディスク容量の80%です。ディスク容量の合計が取得できない場合は、デフォルト値は50 GiBです。明示的に`DISK_QUOTA`指定する場合は、TiDBの一時ディレクトリのディスク容量の80%を超えないようにしてください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `DISABLE_TIKV_IMPORT_MODE`          | すべてのファイル形式              | インポートプロセス中にTiKVをインポートモードに切り替えることを無効にするかどうかを指定します。デフォルトでは、TiKVをインポートモードに切り替えることは無効になっていません。クラスター内で読み取り/書き込み操作が進行中の場合は、このオプションを有効にすることでインポートプロセスの影響を回避できます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `THREAD=<number>`                   | すべてのファイル形式と検索結果`SELECT` | インポートの同時実行性を指定します。 `IMPORT INTO ... FROM FILE`場合、デフォルト値`THREAD`は TiDB ノードの CPU コア数の 50% で、最小値は`1` 、最大値は CPU コア数です。 `IMPORT INTO ... FROM SELECT`場合、デフォルト値`THREAD`は`2`で、最小値は`1` 、最大値は TiDB ノードの CPU コア数の 2 倍です。 新しいクラスターにデータのない状態でデータをインポートする場合は、インポートのパフォーマンスを向上させるために、この同時実行性を適切に増やすことをお勧めします。 ターゲットクラスターがすでに本番環境で使用されている場合は、アプリケーションの要件に応じてこの同時実行性を調整することをお勧めします。                                                                                                                                                                                                                                                                                                                                                                                                        |
| `MAX_WRITE_SPEED='<string>'`        | すべてのファイル形式              | TiKVノードへの書き込み速度を制御します。デフォルトでは速度制限はありません。例えば、このオプションを`1MiB`に指定すると、書き込み速度が1MiB/sに制限されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `CHECKSUM_TABLE='<string>'`         | すべてのファイル形式              | インポート後にターゲットテーブルでチェックサムチェックを実行し、インポートの整合性を検証するかどうかを設定します。サポートされる値は`"required"` (デフォルト)、 `"optional"` 、 `"off"`です。 `"required"`インポート後にチェックサムチェックを実行することを意味します。チェックサムチェックに失敗した場合、TiDBはエラーを返し、インポートは終了します。 `"optional"`インポート後にチェックサムチェックを実行することを意味します。エラーが発生した場合、TiDBは警告を返し、エラーを無視します。 `"off"`インポート後にチェックサムチェックを実行しないことを意味します。                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `DETACHED`                          | すべてのファイル形式              | `IMPORT INTO`非同期で実行するかどうかを制御します。このオプションを有効にすると、 `IMPORT INTO`実行するとすぐにインポートジョブの情報（ `Job_ID`など）が返され、ジョブはバックエンドで非同期的に実行されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `CLOUD_STORAGE_URI`                 | すべてのファイル形式              | [グローバルソート](/tidb-global-sort.md)のエンコードされた KV データが格納されるターゲット アドレスを指定します。 `CLOUD_STORAGE_URI`指定されていない場合、 `IMPORT INTO` 、システム変数[`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)値に基づいてグローバル ソートを使用するかどうかを決定します。このシステム変数がターゲットstorageアドレスを指定している場合、 `IMPORT INTO`このアドレスをグローバル ソートに使用します。 `CLOUD_STORAGE_URI`空でない値で指定されている場合、 `IMPORT INTO`その値をターゲットstorageアドレスとして使用します。 `CLOUD_STORAGE_URI`空の値で指定されている場合、ローカル ソートが適用されます。現在、ターゲットstorageアドレスは S3 のみをサポートしています。URI 構成の詳細については、 [Amazon S3 URI 形式](/external-storage-uri.md#amazon-s3-uri-format)参照してください。この機能を使用する場合、すべての TiDB ノードに、少なくとも次の権限を含め、ターゲット S3 バケットに対する読み取りおよび書き込みアクセス権が必要です: `s3:ListBucket` 、 `s3:GetObject` 、 `s3:DeleteObject` 、 `s3:PutObject` 、 `s3: AbortMultipartUpload` 。 |
| `DISABLE_PRECHECK`                  | すべてのファイル形式と検索結果`SELECT` | このオプションを設定すると、CDC タスクまたは PITR タスクがあるかどうかのチェックなど、重要でない項目の事前チェックが無効になります。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

## <code>IMPORT INTO ... FROM FILE</code>使用法 {#code-import-into-from-file-code-usage}

TiDB Self-Managed の場合、 `IMPORT INTO ... FROM FILE` Amazon S3、GCS、および TiDB ローカルstorageに保存されているファイルからのデータのインポートをサポートします。3 [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)場合、 `IMPORT INTO ... FROM FILE` Amazon S3 および GCS に保存されているファイルからのデータのインポートをサポートします。7 [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)場合、 `IMPORT INTO ... FROM FILE` Amazon S3 および Alibaba Cloud OSS に保存されているファイルからのデータのインポートをサポートします。

-   Amazon S3 または GCS に保存されているデータ ファイルの場合、 `IMPORT INTO ... FROM FILE` [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)での実行をサポートします。

    -   DXF が有効になっている場合 ( [tidb_enable_dist_task](/system-variables.md#tidb_enable_dist_task-new-in-v710)が`ON` )、 `IMPORT INTO`データ インポート ジョブを複数のサブジョブに分割し、これらのサブジョブを異なる TiDB ノードに分散して実行することで、インポート効率を向上させます。
    -   DXF が無効になっている場合、 `IMPORT INTO ... FROM FILE`現在のユーザーが接続している TiDB ノードでの実行のみをサポートします。

-   TiDBにローカルに保存されているデータファイルについては、 `IMPORT INTO ... FROM FILE`現在のユーザーが接続しているTiDBノード上でのみ実行をサポートします。したがって、データファイルは現在のユーザーが接続しているTiDBノード上に配置する必要があります。プロキシまたはロードバランサを介してTiDBにアクセスする場合、TiDBにローカルに保存されているデータファイルをインポートすることはできません。

### 圧縮ファイル {#compressed-files}

`IMPORT INTO ... FROM FILE`圧縮された`CSV`および`SQL`ファイルのインポートをサポートしています。ファイル拡張子に基づいて、ファイルが圧縮されているかどうか、および圧縮形式を自動的に判断します。

| 拡大             | 圧縮形式     |
| :------------- | :------- |
| `.gz` `.gzip`  | gzip圧縮形式 |
| `.zstd` `.zst` | ZStd圧縮形式 |
| `.snappy`      | スナップ圧縮形式 |

> **注記：**
>
> -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。
> -   TiDB Lightningは単一の大きな圧縮ファイルを同時に解凍できないため、圧縮ファイルのサイズはインポート速度に影響します。解凍後のソースファイルは256MiB以下にすることをお勧めします。

### グローバルソート {#global-sort}

> **注記：**
>
> グローバルソートは[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

`IMPORT INTO ... FROM FILE`ソースデータファイルのデータインポートジョブを複数のサブジョブに分割し、各サブジョブはインポート前に独立してデータのエンコードとソートを行います。これらのサブジョブのエンコードされたKV範囲に大きな重複がある場合（TiDBがデータをKVにエンコードする方法については、 [TiDBコンピューティング](/tidb-computing.md)参照）、TiKVはインポート中に圧縮を維持する必要があり、インポートのパフォーマンスと安定性が低下します。

次のシナリオでは、KV 範囲に大きな重複が生じる可能性があります。

-   各サブジョブに割り当てられたデータ ファイル内の行の主キー範囲が重複している場合、各サブジョブのエンコードによって生成されるデータ KV も重複します。
    -   `IMPORT INTO` 、データ ファイルのトラバース順序に基づいてサブジョブを分割します。通常は、ファイル名で辞書順にソートされます。
-   対象テーブルに多数のインデックスがある場合や、インデックス列の値がデータファイル内に分散している場合、各サブジョブのエンコードによって生成されるインデックス KV も重複します。

[TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)有効になっている場合、 `IMPORT INTO`ステートメントで`CLOUD_STORAGE_URI`オプションを指定するか、システム変数[`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)使用してエンコードされた KV データのターゲットstorageアドレスを指定することで[グローバルソート](/tidb-global-sort.md)有効にできます。現在、グローバル ソートは、storageアドレスとして Amazon S3 の使用をサポートしています。グローバル ソートを有効にすると、 `IMPORT INTO`エンコードされた KV データをクラウドstorageに書き込み、クラウドstorage内でグローバル ソートを実行し、グローバルにソートされたインデックスとテーブル データを TiKV に並列インポートします。これにより、KV の重複による問題を防ぎ、インポートの安定性とパフォーマンスが向上します。

グローバルソートは大量のメモリリソースを消費します。データのインポート前に、変数[`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)と[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)設定することをお勧めします。これにより、Golang GCが頻繁にトリガーされ、インポート効率が低下するのを回避できます。

```sql
SET GLOBAL tidb_server_memory_limit_gc_trigger=1;
SET GLOBAL tidb_server_memory_limit='75%';
```

> **注記：**
>
> -   ソースデータファイル内のKV範囲の重複が少ない場合、グローバルソートを有効にするとインポートのパフォーマンスが低下する可能性があります。これは、グローバルソートを有効にすると、TiDBがグローバルソート操作とそれに続くインポートを実行する前に、すべてのサブジョブのローカルソートが完了するまで待機する必要があるためです。
> -   グローバル ソートを使用したインポート ジョブが完了すると、グローバル ソート用にクラウドstorageに保存されたファイルは、バックグラウンド スレッドで非同期的にクリーンアップされます。

### 出力 {#output}

`IMPORT INTO ... FROM FILE`インポートを完了するか、 `DETACHED`モードが有効になっている場合、TiDB は以下の例に示すように、現在のジョブ情報を出力に返します。各フィールドの説明については、 [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)参照してください。

`IMPORT INTO ... FROM FILE`インポートを完了すると、出力例は次のようになります。

```sql
IMPORT INTO t FROM '/path/to/small.csv';
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|  60002 | /path/to/small.csv | `test`.`t`   |      363 |       | finished | 16B              |             2 |                | 2023-06-08 16:01:22.095698 | 2023-06-08 16:01:22.394418 | 2023-06-08 16:01:26.531821 | root@%     |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
```

`DETACHED`モードが有効になっている場合、 `IMPORT INTO ... FROM FILE`ステートメントを実行するとすぐにジョブ情報が出力に返されます。出力から、ジョブのステータスが`pending` （実行待ち）であることがわかります。

```sql
IMPORT INTO t FROM '/path/to/small.csv' WITH DETACHED;
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
```

### インポートジョブのビューと管理 {#view-and-manage-import-jobs}

`DETACHED`モードが有効になっているインポート ジョブの場合、 [`SHOW IMPORT`](/sql-statements/sql-statement-show-import-job.md)使用して現在のジョブの進行状況を表示できます。

インポート ジョブが開始された後は、 [`CANCEL IMPORT JOB &#x3C;job-id>`](/sql-statements/sql-statement-cancel-import-job.md)使用してキャンセルできます。

### 例 {#examples}

#### ヘッダー付きのCSVファイルをインポートする {#import-a-csv-file-with-headers}

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### <code>DETACHED</code>モードでファイルを非同期にインポートする {#import-a-file-asynchronously-in-the-code-detached-code-mode}

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH DETACHED;
```

#### データファイル内の特定のフィールドのインポートをスキップする {#skip-importing-a-specific-field-in-your-data-file}

データ ファイルが CSV 形式であり、その内容が次のとおりであるとします。

    id,name,age
    1,Tom,23
    2,Jack,44

インポートのターゲットテーブルスキーマが`CREATE TABLE t(id int primary key, name varchar(100))`あると仮定します。データファイル内の`age`フィールドをテーブル`t`にインポートせずにスキップするには、次のSQL文を実行します。

```sql
IMPORT INTO t(id, name, @1) FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### ワイルドカードを使用して複数のデータファイルをインポートする {#import-multiple-data-files-using-wildcards}

`/path/to/`ディレクトリに`file-01.csv` 、 `file-02.csv` 、 `file-03.csv`という3つのファイルがあるとします。これらの3つのファイルを`IMPORT INTO`を使用してターゲットテーブル`t`にインポートするには、次のSQL文を実行します。

```sql
IMPORT INTO t FROM '/path/to/file-*.csv';
```

`file-01.csv`と`file-03.csv`をターゲット テーブルにインポートする必要がある場合は、次の SQL ステートメントを実行します。

```sql
IMPORT INTO t FROM '/path/to/file-0[13].csv';
```

#### Amazon S3 または GCS からデータファイルをインポートする {#import-data-files-from-amazon-s3-or-gcs}

-   Amazon S3 からデータ ファイルをインポートします。

    ```sql
    IMPORT INTO t FROM 's3://bucket-name/test.csv?access-key=XXX&secret-access-key=XXX';
    ```

-   GCS からデータ ファイルをインポートします。

    ```sql
    IMPORT INTO t FROM 'gs://import/test.csv?credentials-file=${credentials-file-path}';
    ```

Amazon S3 または GCS の URI パス設定の詳細については、 [外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

#### SetClauseを使用して列の値を計算する {#calculate-column-values-using-setclause}

データ ファイルが CSV 形式であり、その内容が次のとおりであるとします。

    id,name,val
    1,phone,230
    2,book,440

インポートのターゲットテーブルスキーマが`CREATE TABLE t(id int primary key, name varchar(100), val int)`であると仮定します。インポート中に`val`列の値を100倍にしたい場合は、次のSQL文を実行します。

```sql
IMPORT INTO t(id, name, @1) SET val=@1*100 FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### SQL形式のデータファイルをインポートする {#import-a-data-file-in-the-sql-format}

```sql
IMPORT INTO t FROM '/path/to/file.sql' FORMAT 'sql';
```

#### 書き込み速度をTiKVに制限する {#limit-the-write-speed-to-tikv}

TiKV ノードへの書き込み速度を 10 MiB/s に制限するには、次の SQL ステートメントを実行します。

```sql
IMPORT INTO t FROM 's3://bucket/path/to/file.parquet?access-key=XXX&secret-access-key=XXX' FORMAT 'parquet' WITH MAX_WRITE_SPEED='10MiB';
```

## <code>IMPORT INTO ... FROM SELECT</code>使用法 {#code-import-into-from-select-code-usage}

`IMPORT INTO ... FROM SELECT`使用すると、 `SELECT`ステートメントのクエリ結果をTiDBの空のテーブルにインポートできます。また、 [`AS OF TIMESTAMP`](/as-of-timestamp.md)でクエリされた履歴データをインポートすることもできます。

### <code>SELECT</code>のクエリ結果をインポートする {#import-the-query-result-of-code-select-code}

インポートの同時実行性を`8`に指定し、重要でない項目の事前チェックを無効にして、結果`UNION`ターゲット テーブル`t`にインポートするには、次の SQL ステートメントを実行します。

```sql
IMPORT INTO t FROM SELECT * FROM src UNION SELECT * FROM src2 WITH THREAD = 8, DISABLE_PRECHECK;
```

### 指定した時点の履歴データをインポートする {#import-historical-data-at-a-specified-time-point}

指定された時点の履歴データをターゲット テーブル`t`にインポートするには、次の SQL ステートメントを実行します。

```sql
IMPORT INTO t FROM SELECT * FROM src AS OF TIMESTAMP '2024-02-27 11:38:00';
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)
-   [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
-   [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)
-   [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)
