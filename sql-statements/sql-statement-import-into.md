---
title: IMPORT INTO
summary: TiDBにおけるIMPORT INTOの使用方法の概要。
---

# インポート先 {#import-into}

`IMPORT INTO`ステートメントを使用すると、 TiDB Lightningの[物理輸入モード](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode)を介して TiDB にデータをインポートできます。 `IMPORT INTO` 、次の 2 つの方法で使用できます。

-   `IMPORT INTO ... FROM FILE` : `CSV` 、 `SQL` 、 `PARQUET`などの形式のデータファイルを TiDB の空のテーブルにインポートします。
-   `IMPORT INTO ... FROM SELECT` : `SELECT`ステートメントのクエリ結果を TiDB の空のテーブルにインポートします。また、 [`AS OF TIMESTAMP`](/as-of-timestamp.md)でクエリされた履歴データをインポートするためにも使用できます。

<CustomContent platform="tidb">

> **注記：**
>
> [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)と比較して、 `IMPORT INTO` TiDBノード上で直接実行でき、自動分散タスクスケジューリングと[TiDB グローバルソート](/tidb-global-sort.md)グローバルをサポートし、デプロイ、リソース利用率、タスク構成の利便性、呼び出しと統合の容易さ、高可用性、スケーラビリティにおいて大幅な改善を提供します。適切なシナリオでは、 TiDB Lightningの代わりに`IMPORT INTO`の使用を検討することをお勧めします。

</CustomContent>

## 制限 {#restrictions}

-   `IMPORT INTO`データベース内の既存の空のテーブルへのデータのインポートのみをサポートしています。
-   `IMPORT INTO` 、同じテーブルの他のパーティションに既にデータが含まれている場合、空のパーティションへのデータインポートをサポートしていません。インポート操作を行うには、対象テーブルが完全に空である必要があります。
-   `IMPORT INTO`[一時テーブル](/temporary-tables.md)またはキャッシュ[キャッシュされたテーブル](/cached-tables.md)へのデータのインポートをサポートしていません。
-   `IMPORT INTO`トランザクションまたはロールバックをサポートしていません。明示的なトランザクション ( `IMPORT INTO` / { `BEGIN`内) で`END`を実行するとエラーが返されます。
-   `IMPORT INTO` [バックアップと復元](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)、 [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) 、 [インデックス追加処理の高速化](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)、 TiDB Lightning を使用したデータ インポート、TiCDC を使用したデータ レプリケーション、または[特定時点復旧（PITR）](https://docs.pingcap.com/tidb/stable/br-log-architecture)などの機能との同時作業をサポートしていません。互換性の詳細については、 [TiDB Lightningと`IMPORT INTO`のTiCDCおよびログバックアップとの互換性](https://docs.pingcap.com/tidb/stable/tidb-lightning-compatibility-and-scenarios)参照してください。
-   データインポート処理中は、対象テーブルに対してDDLまたはDML操作を実行したり、対象データベースに対して[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)を実行したりしないでください。これらの操作は、インポートの失敗やデータの不整合を引き起こす可能性があります。また、インポート処理中に読み取り操作を実行することも推奨さ**れません**。読み取られるデータに不整合が生じる可能性があるためです。読み取りおよび書き込み操作は、インポートが完了した後にのみ実行してください。
-   インポート プロセスはシステム リソースを大幅に消費します。 TiDB セルフマネージドの場合、パフォーマンスを向上させるために、少なくとも 32 コアと 64 GiB のメモリを備えた TiDB ノードを使用することをお勧めします。 TiDB はインポート中にソートされたデータを TiDB [一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)に書き込むため、フラッシュメモリなどの TiDB 自己管理用の高性能storageメディアを構成することをお勧めします。詳細については、 [物理輸入モードの制限](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode#requirements-and-restrictions)を参照してください。
-   TiDB Self-Managedの場合、TiDB [一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)は少なくとも90 GiBの空き容量が必要です。インポートするデータ量と同等以上のstorage容量を割り当てることをお勧めします。
-   1つのインポートジョブは、1つのターゲットテーブルへのデータインポートのみをサポートします。
-   `IMPORT INTO` TiDB クラスタのアップグレード時にはサポートされません。
-   インポートするデータに、主キーまたはNULL以外の一意インデックスの競合が発生するレコードが含まれていないことを確認してください。競合が発生すると、インポート処理が失敗する可能性があります。
-   既知の問題: TiDBノード構成ファイル内のPDアドレスがクラスタの現在のPDトポロジと一致しない場合`IMPORT INTO`タスクが失敗する可能性があります。この不一致は、PDが以前にスケールインされたものの、TiDB構成ファイルがそれに応じて更新されなかった場合や、構成ファイルの更新後にTiDBノードが再起動されなかった場合などに発生する可能性があります。

### <code>IMPORT INTO ... FROM FILE</code>制限 {#code-import-into-from-file-code-restrictions}

-   TiDB Self-Managedの場合、各`IMPORT INTO`タスクは10 TiB以内のデータインポートをサポートします。 機能を有効にすると、各`IMPORT INTO`タスク[グローバルソート](/tidb-global-sort.md)40 TiB以内のデータインポートをサポートします。
-   [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合、インポートするデータが 500 GiB を超える場合は、少なくとも 16 コアの TiDB ノードを使用し、[グローバルソート](/tidb-global-sort.md)機能を有効にすることをお勧めします。そうすると、各`IMPORT INTO`タスクは 40 TiB 以内のデータのインポートをサポートします。インポートするデータが 500 GiB 以内である場合、または TiDB ノードのコア数が 16 未満の場合は、[グローバルソート](/tidb-global-sort.md)機能を有効にしないことをお勧めします。
-   `IMPORT INTO ... FROM FILE`の実行は、インポートが完了するまで現在の接続をブロックします。ステートメントを非同期で実行するには、 `DETACHED`オプションを追加してください。
-   最大 16 個の`IMPORT INTO`タスクを各クラスターで同時に実行できます ( [TiDB分散実行フレームワーク（DXF）の使用制限](/tidb-distributed-execution-framework.md#limitation)を参照)。クラスターに十分なリソースが不足している場合、またはタスクの最大数に達している場合、新しく送信されたインポート タスクは実行のためにキューに入れられます。
-   データのインポートに[グローバルソート](/tidb-global-sort.md)機能を使用する場合、 `THREAD`オプションの値は少なくとも`8`である必要があります。
-   [グローバルソート](/tidb-global-sort.md)機能を使用してデータをインポートする場合、エンコード後の 1 行のデータ サイズは 32 MiB を超えてはなりません。
-   [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)が有効になっていないときに作成されたすべての`IMPORT INTO`タスクは、タスクが送信されたノードで直接実行され、後で DXF が有効になった後でも、他の TiDB ノードで実行するようにスケジュールされません。DXF が有効になった後は、S3 または GCS からデータをインポートする新しく作成された`IMPORT INTO`タスクのみが、自動的にスケジュールされるか、他の TiDB ノードにフェイルオーバーして実行されます。

### <code>IMPORT INTO ... FROM SELECT</code>制限 {#code-import-into-from-select-code-restrictions}

-   `IMPORT INTO ... FROM SELECT` 、現在のユーザーが接続している TiDB ノードでのみ実行でき、インポートが完了するまで現在の接続をブロックします。
-   `IMPORT INTO ... FROM SELECT` 、 `THREAD`と`DISABLE_PRECHECK` 2 つのインポート[インポートオプション](#withoptions)のみをサポートします。
-   `IMPORT INTO ... FROM SELECT` `SHOW IMPORT JOB(s)`や`CANCEL IMPORT JOB <job-id>`などのタスク管理ステートメントをサポートしていません。
-   TiDB では、 `SELECT`ステートメントのクエリ結果全体を格納するのに十分なスペースが必要です ( `DISK_QUOTA`オプション[一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)設定は現在サポートされていません)。
-   [`tidb_snapshot`](/read-historical-data.md)を使用した履歴データのインポートはサポートされていません。
-   `SELECT`句の構文は複雑なため、 `WITH`内の`IMPORT INTO`パラメーターがこれと競合し、 `GROUP BY ... [WITH ROLLUP]`のような解析エラーが発生する可能性があります。複雑な`SELECT`ステートメント用にビューを作成し、インポートには`IMPORT INTO ... FROM SELECT * FROM view_name`を使用することをお勧めします。または、 `SELECT` `IMPORT INTO ... FROM (SELECT ...) WITH ...`句のスコープを明確にすることもできます。

## インポートの前提条件 {#prerequisites-for-import}

`IMPORT INTO`を使用してデータをインポートする前に、以下の要件を満たしていることを確認してください。

-   インポート対象のテーブルは既にTiDB内に作成されており、空の状態です。
-   対象クラスターには、インポートするデータを保存するのに十分な空き容量があります。
-   TiDB Self-Managed の場合、 現在のセッションに接続されている TiDB ノードの空き容量[一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)90 GiB 以上必要です[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)が有効になっており、インポートするデータが S3 または GCS から取得される場合は、クラスタ内の各 TiDB ノードの一時ディレクトリに十分なディスク容量があることを確認してください。

## 必要な権限 {#required-privileges}

`IMPORT INTO`を実行するには、対象テーブルに対する`SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、および`ALTER`の権限。TiDB ローカルstorageにファイルをインポートするには、 `FILE`権限も必要です。

## あらすじ {#synopsis}

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
    'FORMAT' ('"CSV"' | '"SQL"' | '"PARQUET"')

WithOptions ::=
    'WITH' OptionItem (',' OptionItem)*

OptionItem ::=
    optionName '=' optionVal | optionName
```

## パラメータの説明 {#parameter-description}

### 列名またはユーザー変数リスト {#columnnameoruservarlist}

これは、データ ファイル内の各フィールドがターゲット テーブルの列にどのように対応するかを指定します。また、フィールドを変数にマッピングしてインポート時に特定のフィールドをスキップしたり、 `SetClause`で使用したりすることもできます。

-   このパラメータが指定されていない場合、データファイルの各行のフィールド数は、対象テーブルの列数と一致する必要があります。フィールドは、対応する列に順番にインポートされます。
-   このパラメータを指定する場合、指定する列数または変数数は、データファイルの各行のフィールド数と一致していなければなりません。

### セット条項 {#setclause}

これは、対象列の値がどのように計算されるかを指定します。 `SET`式の右側では、 `ColumnNameOrUserVarList`で指定された変数を参照できます。

`SET`式の左側では、 `ColumnNameOrUserVarList`に含まれていない列名のみを参照できます。対象の列名が既に`ColumnNameOrUserVarList`に存在する場合、 `SET`式は無効です。

### ファイルの場所 {#filelocation}

これはデータファイルのstorage場所を指定するもので、Amazon S3またはGCSのURIパス、あるいはTiDBのローカルファイルパスを指定できます。

-   Amazon S3 または GCS URI パス: URI 設定の詳細については、[外部ストレージサービスのURI形式](/external-storage-uri.md)を参照してください。

-   TiDB ローカルファイルパス: 絶対パスである必要があり、ファイル拡張子は`.csv` 、 `.sql` 、または`.parquet`である必要があります。このパスに対応するファイルが、現在のユーザーが接続している TiDB ノードに保存されていること、およびユーザーが`FILE`権限を持っていることを確認してください。

> **注記：**
>
> ターゲット クラスターで[SEM](/system-variables.md#tidb_enable_enhanced_security)が有効になっている場合、 `fileLocation`をローカル ファイル パスとして指定することはできません。

`fileLocation`パラメータでは、単一のファイルを指定するか、 `*`および`[]`ワイルドカードを使用して、インポートする複数のファイルに一致させることができます。ワイルドカードはファイル名にのみ使用できることに注意してください。ディレクトリには一致せず、サブディレクトリ内のファイルも再帰的に一致しません。Amazon S3 に保存されているファイルを例にとると、パラメータは次のように設定できます。

-   単一ファイルをインポートします: `s3://<bucket-name>/path/to/data/foo.csv`
-   指定されたパスにあるすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/*`
-   指定されたパスにある、 `.csv`サフィックスを持つすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/*.csv`
-   指定されたパスにある`foo`接頭辞を持つすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/foo*`
-   指定されたパス`foo`という接頭辞と`.csv`という接尾辞を持つすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/foo*.csv`
-   `1.csv`と`2.csv`を指定されたパス`s3://<bucket-name>/path/to/data/[12].csv`にインポートします。

### 形式 {#format}

`IMPORT INTO`ステートメントは、 `CSV` 、 `SQL` 、および`PARQUET`データ ファイル形式をサポートしています。指定しない場合、デフォルトの形式は`CSV`です。

### オプション付き {#withoptions}

`WithOptions`を使用すると、インポートオプションを指定し、データインポートプロセスを制御できます。たとえば、バックエンドでデータファイルのインポートを非同期で実行するには、 `DETACHED`ステートメントに`WITH DETACHED`オプションを追加して、インポートの`IMPORT INTO`モードを有効にします。

サポートされているオプションは以下のとおりです。

| オプション名                              | サポートされているデータソースとフォーマット    | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| :---------------------------------- | :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CHARACTER_SET='<string>'`          | CSV                       | データファイルの文字セットを指定します。デフォルトの文字セットは`utf8mb4`です。サポートされている文字セットには、 `binary` 、 `utf8` 、 `utf8mb4` 、 `gb18030` 、 `gbk` 、 `latin1` 、および`ascii`があります。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `FIELDS_TERMINATED_BY='<string>'`   | CSV                       | フィールド区切り文字を指定します。デフォルトの区切り文字は`,`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `FIELDS_ENCLOSED_BY='<char>'`       | CSV                       | フィールド区切り文字を指定します。デフォルトの区切り文字は`"`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `FIELDS_ESCAPED_BY='<char>'`        | CSV                       | フィールドのエスケープ文字を指定します。デフォルトのエスケープ文字は`\`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `FIELDS_DEFINED_NULL_BY='<string>'` | CSV                       | フィールド内の`NULL`を表す値を指定します。デフォルト値は`\N`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `LINES_TERMINATED_BY='<string>'`    | CSV                       | 行末文字を指定します。デフォルトでは、 `IMPORT INTO`は、 `\n` 、 `\r` 、または`\r\n`行末文字として自動的に識別します。行末文字がこれら 3 つのいずれかである場合は、このオプションを明示的に指定する必要はありません。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `SKIP_ROWS=<number>`                | CSV                       | スキップする行数を指定します。デフォルト値は`0`です。このオプションを使用すると、CSV ファイルのヘッダーをスキップできます。インポートするソース ファイルを指定するためにワイルド カードを使用する場合、このオプションは`fileLocation`のワイルド カードに一致するすべてのソース ファイルに適用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `SPLIT_FILE`                        | CSV                       | インポート効率を向上させるため、単一のCSVファイルを約256MiBの複数の小さなチャンクに分割し、並列処理を行います。このパラメータは**非圧縮**CSVファイルでのみ有効で、 TiDB Lightning [`strict-format`](https://docs.pingcap.com/tidb/stable/tidb-lightning-data-source#strict-format)と同様の使用制限があります。このオプションを使用するには`LINES_TERMINATED_BY`明示的に指定する必要があることに注意してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `DISK_QUOTA='<string>'`             | すべてのファイル形式                | データソート中に使用できるディスク容量のしきい値を指定します。デフォルト値は、TiDB のディスク容量の 80% です。 ディスクの合計サイズを取得できない場合は、デフォルト値は 50 GiB です。 `DISK_QUOTA`を明示的に指定する場合は、その値が TiDB [一時ディレクトリ](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)ディレクトリのディスク容量の 80% を超えないようにしてください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `DISABLE_TIKV_IMPORT_MODE`          | すべてのファイル形式                | インポート処理中に TiKV をインポートモードに切り替える機能を無効にするかどうかを指定します。デフォルトでは、TiKV をインポートモードに切り替える機能は無効になっていません。クラスタ内で読み書き操作が進行中の場合は、このオプションを有効にすることで、インポート処理による影響を回避できます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `THREAD=<number>`                   | `SELECT`のすべてのファイル形式とクエリ結果 | インポートの同時実行数を指定します。 `IMPORT INTO ... FROM FILE`の場合、 `THREAD`のデフォルト値は TiDB ノードの CPU コア数の 50%、最小値は`1` 、最大値は CPU コア数です。 `IMPORT INTO ... FROM SELECT`の場合、 `THREAD`のデフォルト値は`2` 、最小値は`1` 、最大値は TiDB ノードの CPU コア数の 2 倍です。データのない新しいクラスタにデータをインポートする場合は、インポートのパフォーマンスを向上させるために、この同時実行数を適切に増やすことをお勧めします。対象クラスターが既に本番環境で使用されている場合は、アプリケーションの要件に応じてこの同時実行数を調整することをお勧めします。                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `MAX_WRITE_SPEED='<string>'`        | すべてのファイル形式                | TiKVノードへの書き込み速度を制御します。デフォルトでは速度制限はありません。たとえば、このオプションを`1MiB`と指定すると、書き込み速度を1 MiB/sに制限できます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `CHECKSUM_TABLE='<string>'`         | すべてのファイル形式                | インポート後にターゲット テーブルに対してチェックサム チェックを実行してインポートの整合性を検証するかどうかを設定します。サポートされている値は、 `"required"` (デフォルト)、 `"optional"` 、および`"off"`です。 `"required"`インポート後にチェックサム チェックを実行することを意味します。チェックサム チェックが失敗した場合、TiDB はエラーを返し、インポートは終了します。 `"optional"`インポート後にチェックサム チェックを実行することを意味します。エラーが発生した場合、TiDB は警告を返し、エラーを無視します。 `"off"`インポート後にチェックサム チェックを実行しないことを意味します。                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `DETACHED`                          | すべてのファイル形式                | `IMPORT INTO`非同期で実行するかどうかを制御します。このオプションを有効にすると、 `IMPORT INTO`の実行によりインポートジョブの情報 ( `Job_ID`など) がすぐに返され、ジョブはバックエンドで非同期に実行されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `CLOUD_STORAGE_URI`                 | すべてのファイル形式                | [グローバルソート](/tidb-global-sort.md)用のエンコードされた KV データが保存されるターゲット アドレスを指定します。 `CLOUD_STORAGE_URI`が指定されていない場合、 `IMPORT INTO`システム変数[`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)の値に基づいてグローバル ソートを使用するかどうかを決定します。このシステム変数でターゲットstorageアドレスが指定されている場合、 `IMPORT INTO`このアドレスをグローバル ソートに使用します。 `CLOUD_STORAGE_URI`に空でない値が指定されている場合、 `IMPORT INTO`その値をターゲットstorageアドレスとして使用します。 `CLOUD_STORAGE_URI`に空の値が指定されている場合、ローカル ソートが適用されます。現在、ターゲットstorageアドレスは S3 のみをサポートしています。URI 構成の詳細については、 [Amazon S3 URI形式](/external-storage-uri.md#amazon-s3-uri-format)参照してください。この機能を使用する場合、すべての TiDB ノードは、対象の S3 バケットに対する読み取りおよび書き込みアクセス権を持っている必要があり、少なくとも次の権限が必要です: `s3:ListBucket` 、 `s3:GetObject` 、 {{B- `s3:DeleteObject` 、 `s3:PutObject` 、 `s3: AbortMultipartUpload` 。 |
| `DISABLE_PRECHECK`                  | `SELECT`のすべてのファイル形式とクエリ結果 | このオプションを設定すると、CDCやPITRタスクの有無など、重要度の低い項目の事前チェックが無効になります。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

<CustomContent platform="tidb-cloud" plan="premium">

> **注記：**
>
> TiDB Cloud Premium では、 `DISK_QUOTA` 、 `THREAD` 、 `MAX_WRITE_SPEED` 、および`CLOUD_STORAGE_URI`つのオプションは、適切な値に自動的に調整されるため、ユーザーが変更することはできません。これらの設定を調整する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

</CustomContent>

## <code>IMPORT INTO ... FROM FILE</code>方法 {#code-import-into-from-file-code-usage}

TiDB Self-Managed の場合、 `IMPORT INTO ... FROM FILE`は Amazon S3、GCS、および TiDB ローカルstorageに保存されているファイルからのデータインポートをサポートしています。 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)の場合、 `IMPORT INTO ... FROM FILE`は Amazon S3 および GCS に保存されているファイルからのデータインポートをサポートしています。 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)の場合、 `IMPORT INTO ... FROM FILE`は Amazon S3 および Alibaba Cloud OSS に保存されているファイルからのデータインポートをサポートしています。

-   Amazon S3 または GCS に保存されているデータ ファイルの場合、 `IMPORT INTO ... FROM FILE` [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)での実行をサポートしています。

    -   DXF が有効になっている場合 ( [tidb_enable_dist_task](/system-variables.md#tidb_enable_dist_task-new-in-v710)が`ON`の場合)、 `IMPORT INTO`データインポートジョブを複数のサブジョブに分割し、これらのサブジョブを異なる TiDB ノードに分散して実行することで、インポート効率を向上させます。
    -   DXF が無効になっている場合、 `IMPORT INTO ... FROM FILE`現在のユーザーが接続している TiDB ノードでの実行のみをサポートします。

-   TiDBにローカルに保存されているデータファイルについては、 `IMPORT INTO ... FROM FILE`現在ユーザーが接続しているTiDBノードでのみ実行がサポートされます。そのため、データファイルは現在ユーザーが接続しているTiDBノードに配置する必要があります。プロキシまたはロードバランサー経由でTiDBにアクセスする場合、TiDBにローカルに保存されているデータファイルをインポートすることはできません。

### 圧縮ファイル {#compressed-files}

`IMPORT INTO ... FROM FILE`は、圧縮された`CSV`および`SQL`ファイルのインポートをサポートしています。ファイル拡張子に基づいて、ファイルが圧縮されているかどうか、および圧縮形式を自動的に判別できます。

| 拡大               | 圧縮形式          |
| :--------------- | :------------ |
| `.gz` 、 `.gzip`  | gzip圧縮形式      |
| `.zstd` 、 `.zst` | ZStd圧縮フォーマット  |
| `.snappy`        | スナッピー圧縮フォーマット |

> **注記：**
>
> -   Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。
> -   TiDB Lightningは単一の大きな圧縮ファイルを同時に解凍できないため、圧縮ファイルのサイズがインポート速度に影響します。解凍後のソースファイルのサイズは256MiB以下にすることをお勧めします。

### グローバルソート {#global-sort}

> **注記：**
>
> [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスでは、グローバルソートは利用できません。

`IMPORT INTO ... FROM FILE` 、ソースデータファイルのデータインポートジョブを複数のサブジョブに分割し、各サブジョブはインポート前にデータを個別にエンコードおよびソートします。これらのサブジョブのエンコードされた KV 範囲に大きな重複がある場合 (TiDB がデータを KV にエンコードする方法については、 [TiDBコンピューティング](/tidb-computing.md)参照)、TiKV はインポート中に圧縮を維持する必要があり、インポートのパフォーマンスと安定性が低下します。

以下のシナリオでは、KV値の範囲が大きく重複する可能性があります。

-   各サブジョブに割り当てられたデータファイルの行に重複する主キー範囲がある場合、各サブジョブのエンコードによって生成されるデータKVも重複します。
    -   `IMPORT INTO` 、データファイルの走査順序に基づいてサブジョブを分割します。通常は、ファイル名で辞書順にソートされます。
-   対象テーブルに多数のインデックスが存在する場合、またはインデックス列の値がデータファイル内に分散している場合、各サブジョブのエンコードによって生成されるインデックスKVも重複します。

[TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)が有効になっている場合、 `CLOUD_STORAGE_URI` `IMPORT INTO`を指定するか、システム変数[`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)を使用してエンコードされた KV データのターゲットstorageアドレスを指定することで、[グローバルソート](/tidb-global-sort.md)を有効にできます。現在、グローバル ソートはstorageアドレスとして Amazon S3 の使用をサポートしています。グローバル ソートが有効になっている場合、 `IMPORT INTO`はエンコードされた KV データをクラウドstorageに書き込み、クラウドstorageでグローバル ソートを実行し、グローバルにソートされたインデックスとテーブル データを TiKV に並列にインポートします。これにより、KV の重複によって発生する問題が防止され、インポートの安定性とパフォーマンスが向上します。

グローバルソートは大量のメモリリソースを消費します。データインポートの前に、 [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)および[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)変数を設定することをお勧めします。これにより、Go言語のガベージコレクションが頻繁にトリガーされることを防ぎ、インポート効率への影響を軽減できます。

```sql
SET GLOBAL tidb_server_memory_limit_gc_trigger=1;
SET GLOBAL tidb_server_memory_limit='75%';
```

> **注記：**
>
> -   ソースデータファイル内のキーバリュー範囲の重複が少ない場合、グローバルソートを有効にするとインポートのパフォーマンスが低下する可能性があります。これは、グローバルソートを有効にすると、TiDB はグローバルソート操作とそれに続くインポートに進む前に、すべてのサブジョブにおけるローカルソートの完了を待つ必要があるためです。
> -   Global Sortを使用したインポート処理が完了すると、Global Sort用にクラウドstorageに保存されたファイルは、バックグラウンドスレッドで非同期的にクリーンアップされます。

### 出力 {#output}

`IMPORT INTO ... FROM FILE`インポートを完了したとき、または`DETACHED`モードが有効になっている場合、TiDB は次の例に示すように、出力に現在のジョブ情報を返します。各フィールドの説明については、 [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)を参照してください。

`IMPORT INTO ... FROM FILE`インポートを完了すると、出力例は次のようになります。

```sql
IMPORT INTO t FROM '/path/to/small.csv';
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|  60002 | /path/to/small.csv | `test`.`t`   |      363 |       | finished | 16B              |             2 |                | 2023-06-08 16:01:22.095698 | 2023-06-08 16:01:22.394418 | 2023-06-08 16:01:26.531821 | root@%     |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
```

`DETACHED`モードが有効になっている場合、 `IMPORT INTO ... FROM FILE`ステートメントを実行すると、出力にジョブ情報がすぐに返されます。出力から、ジョブの状態が`pending`であることがわかります。これは、実行待ち状態であることを意味します。

```sql
IMPORT INTO t FROM '/path/to/small.csv' WITH DETACHED;
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
```

### インポートジョブのビューと管理 {#view-and-manage-import-jobs}

`DETACHED`モードが有効になっているインポート ジョブの場合、 [`SHOW IMPORT`](/sql-statements/sql-statement-show-import-job.md)を使用して現在のジョブの進行状況を表示できます。

インポートジョブが開始された後、 [`CANCEL IMPORT JOB &#x3C;job-id>`](/sql-statements/sql-statement-cancel-import-job.md)を使用してキャンセルできます。

### 例 {#examples}

#### ヘッダー付きのCSVファイルをインポートする {#import-a-csv-file-with-headers}

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### ファイルを非同期で<code>DETACHED</code>モードでインポートする {#import-a-file-asynchronously-in-the-code-detached-code-mode}

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH DETACHED;
```

#### データファイル内の特定のフィールドのインポートをスキップする {#skip-importing-a-specific-field-in-your-data-file}

データファイルがCSV形式で、その内容が以下のようになっていると仮定します。

    id,name,age
    1,Tom,23
    2,Jack,44

インポート対象のテーブルスキーマが`CREATE TABLE t(id int primary key, name varchar(100))`であると仮定します。データファイル内の`age`フィールドをテーブル`t`にインポートしないようにするには、次の SQL ステートメントを実行します。

```sql
IMPORT INTO t(id, name, @1) FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### ワイルドカードを使用して複数のデータファイルをインポートする {#import-multiple-data-files-using-wildcards}

`file-01.csv`ディレクトリに`file-02.csv` 、 `file-03.csv` 、 `/path/to/` -PLACEHOLDER-E}} という名前のファイルが 3 つあるとします。これらの 3 つのファイルを`t`を使用してターゲット テーブル`IMPORT INTO`にインポートするには、次の SQL ステートメントを実行します。

```sql
IMPORT INTO t FROM '/path/to/file-*.csv';
```

`file-01.csv`と`file-03.csv`のみを対象テーブルにインポートする必要がある場合は、次の SQL ステートメントを実行してください。

```sql
IMPORT INTO t FROM '/path/to/file-0[13].csv';
```

#### Amazon S3またはGCSからデータファイルをインポートする {#import-data-files-from-amazon-s3-or-gcs}

-   Amazon S3からデータファイルをインポートする：

    ```sql
    IMPORT INTO t FROM 's3://bucket-name/test.csv?access-key=XXX&secret-access-key=XXX';
    ```

-   GCSからデータファイルをインポートする：

    ```sql
    IMPORT INTO t FROM 'gs://import/test.csv?credentials-file=${credentials-file-path}';
    ```

Amazon S3 または GCS の URI パス設定の詳細については、[外部ストレージサービスのURI形式](/external-storage-uri.md)を参照してください。

#### SetClauseを使用して列の値を計算する {#calculate-column-values-using-setclause}

データファイルがCSV形式で、その内容が以下のようになっていると仮定します。

    id,name,val
    1,phone,230
    2,book,440

インポート対象のテーブルスキーマが`CREATE TABLE t(id int primary key, name varchar(100), val int)`であると仮定します。インポート中に`val`列の値を 100 倍にしたい場合は、次の SQL ステートメントを実行できます。

```sql
IMPORT INTO t(id, name, @1) SET val=@1*100 FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### SQL形式のデータファイルをインポートする {#import-a-data-file-in-the-sql-format}

```sql
IMPORT INTO t FROM '/path/to/file.sql' FORMAT 'sql';
```

#### 書き込み速度をTiKVに制限する {#limit-the-write-speed-to-tikv}

TiKVノードへの書き込み速度を10 MiB/sに制限するには、次のSQL文を実行します。

```sql
IMPORT INTO t FROM 's3://bucket/path/to/file.parquet?access-key=XXX&secret-access-key=XXX' FORMAT 'parquet' WITH MAX_WRITE_SPEED='10MiB';
```

## <code>IMPORT INTO ... FROM SELECT</code>使用法 {#code-import-into-from-select-code-usage}

`IMPORT INTO ... FROM SELECT`使用すると`SELECT`ステートメントのクエリ結果を TiDB の空のテーブルにインポートできます。また、 [`AS OF TIMESTAMP`](/as-of-timestamp.md)でクエリされた履歴データをインポートするためにも使用できます。

### <code>SELECT</code>クエリの結果をインポートします {#import-the-query-result-of-code-select-code}

`UNION`の結果をターゲットテーブル`t`にインポートするには、インポート同時実行数を`8`に指定し、重要でない項目の事前チェックを無効に設定して、次のSQLステートメントを実行します。

```sql
IMPORT INTO t FROM SELECT * FROM src UNION SELECT * FROM src2 WITH THREAD = 8, DISABLE_PRECHECK;
```

### 指定した時点の履歴データをインポートする {#import-historical-data-at-a-specified-time-point}

指定した時点の履歴データをターゲットテーブル`t`にインポートするには、次の SQL ステートメントを実行します。

```sql
IMPORT INTO t FROM SELECT * FROM src AS OF TIMESTAMP '2024-02-27 11:38:00';
```

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)
-   [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
-   [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)
-   [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)
