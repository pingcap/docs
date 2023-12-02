---
title: IMPORT INTO
summary: An overview of the usage of IMPORT INTO in TiDB.
---

# にインポート {#import-into}

`IMPORT INTO`ステートメントは、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を介して、 `CSV` 、 `SQL` 、 `PARQUET`などの形式のデータを TiDB の空のテーブルにインポートするために使用されます。

> **注記：**
>
> このステートメントは TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

`IMPORT INTO` Amazon S3、GCS、TiDB ローカルstorageに保存されているファイルからのデータのインポートをサポートします。

-   Amazon S3、GCS、または Azure Blob Storage に保存されているデータ ファイルの場合、 `IMPORT INTO` [TiDB バックエンド タスク分散実行フレームワーク](/tidb-distributed-execution-framework.md)での実行をサポートします。

    -   このフレームワークが有効な場合 ( [tidb_enable_dist_task](/system-variables.md#tidb_enable_dist_task-new-in-v710)が`ON` )、 `IMPORT INTO`データ インポート ジョブを複数のサブジョブに分割し、これらのサブジョブを異なる TiDB ノードに分散して実行し、インポート効率を向上させます。
    -   このフレームワークが無効になっている場合、 `IMPORT INTO`現在のユーザーが接続している TiDB ノードでの実行のみをサポートします。

-   TiDB にローカルに保存されているデータ ファイルの場合、 `IMPORT INTO`現在のユーザーが接続している TiDB ノードでの実行のみをサポートします。したがって、データ ファイルは、現在のユーザーが接続している TiDB ノードに配置する必要があります。プロキシまたはロード バランサ経由で TiDB にアクセスする場合、TiDB にローカルに保存されているデータ ファイルをインポートできません。

## 制限 {#restrictions}

-   現在、 `IMPORT INTO` 10 TiB 以内のデータのインポートをサポートしています。
-   `IMPORT INTO`データベース内の既存の空のテーブルへのデータのインポートのみをサポートします。
-   `IMPORT INTO`はトランザクションやロールバックをサポートしません。明示的なトランザクション ( `BEGIN` / `END` ) 内で`IMPORT INTO`を実行すると、エラーが返されます。
-   `IMPORT INTO`を実行すると、インポートが完了するまで現在の接続がブロックされます。ステートメントを非同期的に実行するには、 `DETACHED`オプションを追加します。
-   `IMPORT INTO` [復元する](/br/backup-and-restore-overview.md) 、 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) 、 [インデックス追加の高速化](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) 、 TiDB Lightningを使用したデータ インポート、 TiCDC を使用したデータ レプリケーション、または[ポイントインタイムリカバリ (PITR)](/br/br-log-architecture.md)などの機能との同時作業をサポートしていません。
-   クラスター上で一度に実行できるジョブは`IMPORT INTO`つだけです。 `IMPORT INTO`実行中のジョブの事前チェックを実行しますが、これは厳密な制限ではありません。複数のクライアントが同時に実行する場合、 `IMPORT INTO`のインポート ジョブの開始が機能する可能性がありますが、データの不整合やインポートの失敗が発生する可能性があるため、それを回避する必要があります。
-   データ インポート プロセス中は、ターゲット テーブルに対して DDL または DML 操作を実行しないでください。また、ターゲット データベースに対して[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)を実行しないでください。これらの操作により、インポートの失敗やデータの不整合が発生する可能性があります。また、読み取られるデータに一貫性がない可能性があるため、インポート プロセス中に読み取り操作を実行することは**お**勧めできません。インポートが完了した後にのみ、読み取りおよび書き込み操作を実行してください。
-   インポート プロセスはシステム リソースを大幅に消費します。パフォーマンスを向上させるには、少なくとも 32 コアと 64 GiB のメモリを備えた TiDB ノードを使用することをお勧めします。 TiDB はインポート中にソートされたデータを TiDB [一時ディレクトリ](/tidb-configuration-file.md#temp-dir-new-in-v630)に書き込むため、フラッシュメモリなどの高性能storageメディアを構成することをお勧めします。詳細については、 [物理インポートモードの制限事項](/tidb-lightning/tidb-lightning-physical-import-mode.md#requirements-and-restrictions)を参照してください。
-   TiDB [一時ディレクトリ](/tidb-configuration-file.md#temp-dir-new-in-v630) 、少なくとも 90 GiB の使用可能なスペースがあることが予想されます。インポートするデータの量と同じかそれ以上のstorageスペースを割り当てることをお勧めします。
-   1 つのインポート ジョブは、1 つのターゲット テーブルへのデータのみのインポートをサポートします。複数のターゲット テーブルにデータをインポートするには、ターゲット テーブルのインポートが完了した後、次のターゲット テーブルの新しいジョブを作成する必要があります。
-   `IMPORT INTO`は、TiDB クラスターのアップグレード中はサポートされません。
-   [グローバルソート](/tidb-global-sort.md)機能を使用してデータをインポートする場合、エンコード後の 1 行のデータ サイズは 32 MiB を超えてはなりません。
-   データのインポートにグローバル ソート機能を使用する場合、インポート タスクが完了する前にターゲット TiDB クラスターが削除されると、グローバル ソートに使用された一時データが Amazon S3 に残る可能性があります。この場合、S3storageコストの増加を避けるために、残留データを手動で削除する必要があります。
-   インポートするデータに、主キーまたは NULL 以外の一意のインデックスが競合するレコードが含まれていないことを確認してください。そうしないと、競合によりインポート タスクが失敗する可能性があります。
-   既知の問題: TiDB ノード構成ファイル内の PD アドレスがクラスターの現在の PD トポロジーと一致しない場合、 `IMPORT INTO`タスクが失敗する可能性があります。この不一致は、PD が以前にスケールインされたが、それに応じて TiDB 構成ファイルが更新されなかったり、構成ファイルの更新後に TiDB ノードが再起動されなかった場合などに発生する可能性があります。

## インポートの前提条件 {#prerequisites-for-import}

`IMPORT INTO`を使用してデータをインポートする前に、次の要件が満たされていることを確認してください。

-   インポート対象のテーブルはすでに TiDB に作成されており、空です。
-   ターゲット クラスターには、インポートするデータを保存するのに十分なスペースがあります。
-   現在のセッションに接続されている TiDB ノードの[一時ディレクトリ](/tidb-configuration-file.md#temp-dir-new-in-v630)には、少なくとも 90 GiB の使用可能なスペースがあります。 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)が有効な場合は、クラスター内の各 TiDB ノードの一時ディレクトリに十分なディスク容量があることも確認してください。

## 必要な権限 {#required-privileges}

`IMPORT INTO`を実行するには、ターゲット テーブルに対する`SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、および`ALTER`の権限が必要です。 TiDB ローカルstorageにファイルをインポートするには、 `FILE`権限も必要です。

## あらすじ {#synopsis}

```ebnf+diagram
ImportIntoStmt ::=
    'IMPORT' 'INTO' TableName ColumnNameOrUserVarList? SetClause? FROM fileLocation Format? WithOptions?

ColumnNameOrUserVarList ::=
    '(' ColumnNameOrUserVar (',' ColumnNameOrUserVar)* ')'

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

データ ファイルの各フィールドがターゲット テーブルの列にどのように対応するかを指定します。また、これを使用してフィールドを変数にマップし、インポートの特定のフィールドをスキップしたり、 `SetClause`で使用したりすることもできます。

-   このパラメーターが指定されていない場合、データ ファイルの各行のフィールドの数はターゲット テーブルの列の数と一致する必要があり、フィールドは対応する列に順番にインポートされます。
-   このパラメーターを指定する場合、指定された列または変数の数は、データ ファイルの各行のフィールドの数と一致する必要があります。

### SetClause {#setclause}

ターゲット列の値がどのように計算されるかを指定します。 `SET`の式の右側では、 `ColumnNameOrUserVarList`で指定した変数を参照できます。

`SET`式の左側では、 `ColumnNameOrUserVarList`に含まれない列名のみを参照できます。ターゲット列名が`ColumnNameOrUserVarList`にすでに存在する場合、 `SET`の式は無効です。

### ファイルの場所 {#filelocation}

データ ファイルのstorage場所を指定します。Amazon S3、GCS、Azure Blob Storage の URI パス、または TiDB ローカル ファイル パスを指定できます。

-   Amazon S3、GCS、または Azure Blob Storage URI パス: URI 構成の詳細については、 [外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。
-   TiDB ローカル ファイル パス: 絶対パスである必要があり、ファイル拡張子は`.csv` 、 `.sql` 、または`.parquet`である必要があります。このパスに対応するファイルが現在のユーザーが接続している TiDB ノードに保存されていること、およびユーザーが`FILE`権限を持っていることを確認してください。

> **注記：**
>
> 対象クラスタで[SEM](/system-variables.md#tidb_enable_enhanced_security)が有効な場合、 `fileLocation`ローカルファイルパスとして指定できません。

`fileLocation`パラメータでは、単一のファイルを指定することも、ワイルドカード`*`を使用して複数のファイルをインポート対象に一致させることもできます。ワイルドカードはディレクトリと一致したり、サブディレクトリ内のファイルと再帰的に一致したりしないため、ワイルドカードはファイル名でのみ使用できることに注意してください。 Amazon S3 に保存されているファイルを例として、パラメータを次のように設定できます。

-   単一のファイルをインポートする: `s3://<bucket-name>/path/to/data/foo.csv`
-   指定されたパスにあるすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/*`
-   指定されたパスにあるサフィックス`.csv`を持つすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/*.csv`
-   指定されたパスにプレフィックス`foo`を持つすべてのファイルをインポートします: `s3://<bucket-name>/path/to/data/foo*`
-   プレフィックス`foo`とサフィックス`.csv`持つすべてのファイルを指定したパスにインポートします: `s3://<bucket-name>/path/to/data/foo*.csv`

### フォーマット {#format}

`IMPORT INTO`ステートメントは、 `CSV` 、 `SQL` 、および`PARQUET`の 3 つのデータ ファイル形式をサポートします。指定しない場合、デフォルトの形式は`CSV`です。

### オプションあり {#withoptions}

`WithOptions`を使用すると、インポート オプションを指定し、データ インポート プロセスを制御できます。たとえば、バックエンドでインポートを非同期に実行するには、 `IMPORT INTO`ステートメントに`WITH DETACHED`オプションを追加して、インポートの`DETACHED`モードを有効にします。

サポートされているオプションは次のとおりです。

| オプション名                              | サポートされるデータ形式 | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| :---------------------------------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `CHARACTER_SET='<string>'`          | CSV          | データファイルの文字セットを指定します。デフォルトの文字セットは`utf8mb4`です。サポートされている文字セットには`binary` 、 `utf8` 、 `utf8mb4` 、 `gb18030` 、 `gbk` 、 `latin1` 、および`ascii`が含まれます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `FIELDS_TERMINATED_BY='<string>'`   | CSV          | フィールド区切り文字を指定します。デフォルトの区切り文字は`,`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `FIELDS_ENCLOSED_BY='<char>'`       | CSV          | フィールド区切り文字を指定します。デフォルトの区切り文字は`"`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `FIELDS_ESCAPED_BY='<char>'`        | CSV          | フィールドのエスケープ文字を指定します。デフォルトのエスケープ文字は`\`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `FIELDS_DEFINED_NULL_BY='<string>'` | CSV          | フィールドに`NULL`を表す値を指定します。デフォルト値は`\N`です。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `LINES_TERMINATED_BY='<string>'`    | CSV          | 行末文字を指定します。デフォルトでは、 `IMPORT INTO` `\n` 、 `\r` 、または`\r\n`を行終端記号として自動的に識別します。行終端文字がこれら 3 つのいずれかである場合、このオプションを明示的に指定する必要はありません。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `SKIP_ROWS=<number>`                | CSV          | スキップする行数を指定します。デフォルト値は`0`です。このオプションを使用すると、CSV ファイルのヘッダーをスキップできます。ワイルドカードを使用してインポートするソース ファイルを指定する場合、このオプションは`fileLocation`のワイルドカードに一致するすべてのソース ファイルに適用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `SPLIT_FILE`                        | CSV          | 単一の CSV ファイルを約 256 MiB の複数の小さなチャンクに分割して並列処理し、インポート効率を向上させます。このパラメータは**非圧縮**CSV ファイルに対してのみ機能し、 TiDB Lightning [`strict-format`](/tidb-lightning/tidb-lightning-data-source.md#strict-format)と同じ使用制限があります。                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `DISK_QUOTA='<string>'`             | すべてのフォーマット   | データの並べ替え中に使用できるディスク容量のしきい値を指定します。デフォルト値は、TiDB [一時ディレクトリ](/tidb-configuration-file.md#temp-dir-new-in-v630)のディスク容量の 80% です。合計ディスク サイズを取得できない場合、デフォルト値は 50 GiB です。明示的に`DISK_QUOTA`を指定する場合は、その値が TiDB 一時ディレクトリのディスク容量の 80% を超えないようにしてください。                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `DISABLE_TIKV_IMPORT_MODE`          | すべてのフォーマット   | インポート プロセス中に TiKV をインポート モードに切り替えることを無効にするかどうかを指定します。デフォルトでは、TiKV をインポート モードに切り替えることは無効になっていません。クラスター内で読み取り/書き込み操作が進行中の場合は、このオプションを有効にして、インポート プロセスによる影響を回避できます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `THREAD=<number>`                   | すべてのフォーマット   | インポートの同時実行性を指​​定します。デフォルト値は CPU コアの 50% で、最小値は 1 です。このオプションを明示的に指定してリソース使用量を制御できますが、値が CPU コアの数を超えないようにしてください。データをまったく含まない新しいクラスターにデータをインポートするには、この同時実行数を適切に増やしてインポートのパフォーマンスを向上させることをお勧めします。ターゲット クラスターが本番環境ですでに使用されている場合は、アプリケーションの要件に応じてこの同時実行性を調整することをお勧めします。                                                                                                                                                                                                                                                                                                                                                                                       |
| `MAX_WRITE_SPEED='<string>'`        | すべてのフォーマット   | TiKV ノードへの書き込み速度を制御します。デフォルトでは、速度制限はありません。たとえば、このオプションを`1MiB`に指定すると、書き込み速度を 1 MiB/s に制限できます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `CHECKSUM_TABLE='<string>'`         | すべてのフォーマット   | インポート後にターゲットテーブルに対してチェックサムチェックを実行して、インポートの整合性を検証するかどうかを構成します。サポートされている値には、 `"required"` (デフォルト)、 `"optional"` 、および`"off"`が含まれます。 `"required"`インポート後にチェックサム チェックを実行することを意味します。チェックサム チェックが失敗した場合、TiDB はエラーを返し、インポートは終了します。 `"optional"`インポート後にチェックサム チェックを実行することを意味します。エラーが発生した場合、TiDB は警告を返し、エラーを無視します。 `"off"`インポート後にチェックサム チェックを実行しないことを意味します。                                                                                                                                                                                                                                                                                                        |
| `DETACHED`                          | すべてのフォーマット   | `IMPORT INTO`非同期で実行するかどうかを制御します。このオプションが有効な場合、 `IMPORT INTO`を実行するとインポート ジョブ ( `Job_ID`など) の情報がすぐに返され、ジョブはバックエンドで非同期的に実行されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `CLOUD_STORAGE_URI`                 | すべてのフォーマット   | [グローバルソート](/tidb-global-sort.md)のエンコードされたKVデータが格納されるターゲットアドレスを指定します。 `CLOUD_STORAGE_URI`が指定されていない場合、 `IMPORT INTO`システム変数[`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)の値に基づいてグローバル ソートを使用するかどうかを決定します。このシステム変数がターゲットstorageアドレスを指定している場合、 `IMPORT INTO`このアドレスをグローバル ソートに使用します。 `CLOUD_STORAGE_URI`空ではない値で指定された場合、 `IMPORT INTO`その値をターゲットstorageアドレスとして使用します。空の値で`CLOUD_STORAGE_URI`指定すると、ローカル ソートが適用されます。現在、ターゲットstorageアドレスは S3 のみをサポートしています。 URI設定の詳細については、 [Amazon S3 URI 形式](/external-storage-uri.md#amazon-s3-uri-format)を参照してください。この機能を使用する場合、すべての TiDB ノードはターゲット S3 バケットに対する読み取りおよび書き込みアクセス権を持っている必要があります。 |

## 圧縮ファイル {#compressed-files}

`IMPORT INTO`圧縮`CSV`および`SQL`ファイルのインポートをサポートします。ファイルが圧縮されているかどうか、およびファイル拡張子に基づいて圧縮形式を自動的に判断できます。

| 拡大             | 圧縮形式            |
| :------------- | :-------------- |
| `.gz` `.gzip`  | gzip圧縮形式        |
| `.zstd` `.zst` | ZStd圧縮形式        |
| `.snappy`      | きびきびとした圧縮フォーマット |

> **注記：**
>
> Snappy 圧縮ファイルは[公式の Snappy フォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。

## グローバルソート {#global-sort}

> **警告：**
>
> グローバル ソート機能は実験的です。本番環境での使用はお勧めできません。

`IMPORT INTO`ソース データ ファイルのデータ インポート ジョブを複数のサブジョブに分割し、各サブジョブはインポート前にデータを個別にエンコードおよび並べ替えます。これらのサブジョブのエンコードされた KV 範囲に大幅な重複がある場合 (TiDB がデータを KV にエンコードする方法については、 [TiDB コンピューティング](/tidb-computing.md)を参照)、TiKV はインポート中に圧縮を維持する必要があり、インポートのパフォーマンスと安定性の低下につながります。

次のシナリオでは、KV 範囲に大幅な重複が存在する可能性があります。

-   各サブジョブに割り当てられたデータ ファイル内の行に重複する主キー範囲がある場合、各サブジョブのエンコードによって生成されるデータ KV も重複します。
    -   `IMPORT INTO` 、データ ファイルの走査順序に基づいてサブジョブを分割します。通常はファイル名によって辞書順に並べ替えられます。
-   対象テーブルに多くのインデックスがある場合、またはインデックス列の値がデータ ファイル内に分散している場合、各サブジョブのエンコードによって生成されるインデックス KV も重複します。

[バックエンドタスク分散実行フレームワーク](/tidb-distributed-execution-framework.md)が有効な場合、 `IMPORT INTO`ステートメントで`CLOUD_STORAGE_URI`オプションを指定するか、システム変数[`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740)を使用してエンコードされた KV データのターゲットstorageアドレスを指定することにより、 [グローバルソート](/tidb-global-sort.md)有効にできます。現在、グローバル ソートstorageアドレスとしてサポートされているのは S3 のみであることに注意してください。グローバル ソートが有効な場合、 `IMPORT INTO`エンコードされた KV データをクラウドstorageに書き込み、クラウドstorageでグローバル ソートを実行してから、グローバルにソートされたインデックスとテーブル データを TiKV に並行してインポートします。これにより、KV の重複によって引き起こされる問題が防止され、インポートの安定性が向上します。

グローバル ソートは大量のメモリリソースを消費します。データをインポートする前に、変数[`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)と[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を設定することをお勧めします。これにより、golang GC が頻繁にトリガーされてインポ​​ート効率に影響が出るのを回避できます。

```sql
SET GLOBAL tidb_server_memory_limit_gc_trigger=0.99;
SET GLOBAL tidb_server_memory_limit='88%';
```

> **注記：**
>
> -   ソース データ ファイル内の KV 範囲の重複が少ない場合、グローバル ソートを有効にするとインポートのパフォーマンスが低下する可能性があります。これは、グローバル ソートが有効な場合、TiDB はグローバル ソート操作とその後のインポートを続行する前に、すべてのサブジョブでローカル ソートが完了するまで待機する必要があるためです。
> -   Global Sort を使用したインポート ジョブが完了すると、Global Sort のクラウドstorageに保存されたファイルがバックグラウンド スレッドで非同期的にクリーンアップされます。

## 出力 {#output}

`IMPORT INTO`インポートを完了するか、 `DETACHED`モードが有効になっている場合、次の例に示すように、 `IMPORT INTO`出力で現在のジョブ情報を返します。各フィールドの説明については、 [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)を参照してください。

`IMPORT INTO`がインポートを完了すると、出力例は次のようになります。

```sql
IMPORT INTO t FROM '/path/to/small.csv';
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|  60002 | /path/to/small.csv | `test`.`t`   |      363 |       | finished | 16B              |             2 |                | 2023-06-08 16:01:22.095698 | 2023-06-08 16:01:22.394418 | 2023-06-08 16:01:26.531821 | root@%     |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
```

`DETACHED`モードが有効な場合、 `IMPORT INTO`ステートメントを実行すると、出力でジョブ情報がすぐに返されます。出力から、ジョブのステータスが`pending`であることがわかります。これは、実行待ちを意味します。

```sql
IMPORT INTO t FROM '/path/to/small.csv' WITH DETACHED;
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
```

## インポートジョブのビューと管理 {#view-and-manage-import-jobs}

`DETACHED`モードが有効になっているインポート ジョブの場合、 [`SHOW IMPORT`](/sql-statements/sql-statement-show-import-job.md)使用して現在のジョブの進行状況を表示できます。

インポート ジョブの開始後は、 [`CANCEL IMPORT JOB &#x3C;job-id>`](/sql-statements/sql-statement-cancel-import-job.md)を使用してキャンセルできます。

## 例 {#examples}

### ヘッダー付きの CSV ファイルをインポートする {#import-a-csv-file-with-headers}

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH skip_rows=1;
```

### <code>DETACHED</code>モードでファイルを非同期にインポートする {#import-a-file-asynchronously-in-the-code-detached-code-mode}

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH DETACHED;
```

### データ ファイル内の特定のフィールドのインポートをスキップする {#skip-importing-a-specific-field-in-your-data-file}

データ ファイルが CSV 形式であり、その内容が次のとおりであると仮定します。

    id,name,age
    1,Tom,23
    2,Jack,44

また、インポートのターゲット表スキーマが`CREATE TABLE t(id int primary key, name varchar(100))`であると仮定します。データ ファイルの`age`フィールドのテーブル`t`へのインポートをスキップするには、次の SQL ステートメントを実行します。

```sql
IMPORT INTO t(id, name, @1) FROM '/path/to/file.csv' WITH skip_rows=1;
```

### ワイルドカード<code>*</code>を使用して複数のデータ ファイルをインポートします {#import-multiple-data-files-using-the-wildcard-code-code}

`/path/to/`ディレクトリに`file-01.csv` 、 `file-02.csv` 、および`file-03.csv`という名前の 3 つのファイルがあると仮定します。 `IMPORT INTO`を使用してこれら 3 つのファイルをターゲット テーブル`t`にインポートするには、次の SQL ステートメントを実行できます。

```sql
IMPORT INTO t FROM '/path/to/file-*.csv'
```

### Amazon S3、GCS、または Azure Blob Storage からデータ ファイルをインポートする {#import-data-files-from-amazon-s3-gcs-or-azure-blob-storage}

-   Amazon S3 からデータ ファイルをインポートします。

    ```sql
    IMPORT INTO t FROM 's3://bucket-name/test.csv?access-key=XXX&secret-access-key=XXX';
    ```

-   GCS からデータ ファイルをインポートします。

    ```sql
    IMPORT INTO t FROM 'gs://import/test.csv?credentials-file=${credentials-file-path}';
    ```

-   Azure Blob Storage からデータ ファイルをインポートします。

    ```sql
    IMPORT INTO t FROM 'azure://import/test.csv?credentials-file=${credentials-file-path}';
    ```

Amazon S3、GCS、または Azure Blob Storage の URI パス設定の詳細については、 [外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。

### SetClause を使用して列の値を計算する {#calculate-column-values-using-setclause}

データ ファイルが CSV 形式であり、その内容が次のとおりであると仮定します。

    id,name,val
    1,phone,230
    2,book,440

また、インポートのターゲット表スキーマが`CREATE TABLE t(id int primary key, name varchar(100), val int)`であると仮定します。インポート中に`val`列の値を 100 倍する場合は、次の SQL ステートメントを実行できます。

```sql
IMPORT INTO t(id, name, @1) SET val=@1*100 FROM '/path/to/file.csv' WITH skip_rows=1;
```

### SQL形式のデータファイルをインポートする {#import-a-data-file-in-the-sql-format}

```sql
IMPORT INTO t FROM '/path/to/file.sql' FORMAT 'sql';
```

### 書き込み速度を TiKV に制限する {#limit-the-write-speed-to-tikv}

TiKV ノードへの書き込み速度を 10 MiB/s に制限するには、次の SQL ステートメントを実行します。

```sql
IMPORT INTO t FROM 's3://bucket/path/to/file.parquet?access-key=XXX&secret-access-key=XXX' FORMAT 'parquet' WITH MAX_WRITE_SPEED='10MiB';
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)
-   [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
