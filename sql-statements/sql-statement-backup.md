---
title: BACKUP | TiDB SQL Statement Reference
summary: TiDB データベースの BACKUP の使用法の概要。
---

# バックアップ {#backup}

このステートメントは、TiDB クラスターの分散バックアップを実行するために使用されます。

> **警告：**
>
> -   この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。
> -   この機能は[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは利用できません。

`BACKUP`ステートメントは[BRツール](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)と同じエンジンを使用しますが、バックアッププロセスは別のBRツールではなく TiDB 自体によって実行されますBRの利点と警告はすべてこのステートメントにも適用されます。

`BACKUP`実行するには、 `BACKUP_ADMIN`または`SUPER`権限が必要です。さらに、バックアップを実行する TiDB ノードとクラスター内のすべての TiKV ノードの両方に、バックアップ先への読み取りまたは書き込み権限が必要です。9 [Security強化モード](/system-variables.md#tidb_enable_enhanced_security)有効になっている場合、ローカルstorage（ `local://`で始まるstorageパス）は許可されません。

`BACKUP`文は、バックアップタスク全体が完了、失敗、またはキャンセルされるまでブロックされます。3 `BACKUP`実行するには、長時間持続する接続を準備する必要があります。タスクは[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)文を使用してキャンセルできます。

一度に実行できるタスク`BACKUP`と[`RESTORE`](/sql-statements/sql-statement-restore.md) 1 つだけです。同じ TiDBサーバー上で既に`BACKUP`または`RESTORE`ステートメントが実行中の場合、新しい`BACKUP`実行は、前のすべてのタスクが完了するまで待機します。

`BACKUP` 「tikv」storageエンジンでのみ使用できます。2 `BACKUP` 「unistore」エンジンで使用すると失敗します。

## 概要 {#synopsis}

```ebnf+diagram
BackupStmt ::=
    "BACKUP" BRIETables "TO" stringLit BackupOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

BackupOption ::=
    "CHECKSUM" '='? Boolean
|   "CHECKSUM_CONCURRENCY" '='? LengthNum
|   "COMPRESSION_LEVEL" '='? LengthNum
|   "COMPRESSION_TYPE" '='? stringLit
|   "CONCURRENCY" '='? LengthNum
|   "IGNORE_STATS" '='? Boolean
|   "LAST_BACKUP" '='? BackupTSO
|   "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
|   "SNAPSHOT" '='? ( BackupTSO | LengthNum TimestampUnit "AGO" )

Boolean ::=
    NUM | "TRUE" | "FALSE"

BackupTSO ::=
    LengthNum | stringLit
```

## 例 {#examples}

### データベースのバックアップ {#back-up-databases}

```sql
BACKUP DATABASE `test` TO 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+-----------------+---------------------+---------------------+
| Destination                  | Size      | BackupTS        | Queue Time          | Execution Time      |
+------------------------------+-----------+-----------------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 416099531454472 | 2020-04-12 23:09:48 | 2020-04-12 23:09:48 |
+------------------------------+-----------+-----------------+---------------------+---------------------+
1 row in set (58.453 sec)
```

上記の例では、 `test`データベースがローカルファイルシステムにバックアップされています。データは、すべてのTiDBノードとTiKVノードに分散された`/mnt/backup/2020/04/`ディレクトリにSSTファイルとして保存されます。

上記の結果の最初の行は次のように記述されます。

| カラム              | 説明                                                            |
| :--------------- | :------------------------------------------------------------ |
| `Destination`    | リンク先URL                                                       |
| `Size`           | バックアップアーカイブの合計サイズ（バイト単位）                                      |
| `BackupTS`       | バックアップ作成時のスナップショットのTSO（ [増分バックアップ](#incremental-backup)場合に便利） |
| `Queue Time`     | `BACKUP`のタスクがキューに入れられたときのタイムスタンプ (現在のタイムゾーン)。                 |
| `Execution Time` | `BACKUP`タスクの実行が開始されたときのタイムスタンプ (現在のタイムゾーン)。                   |

### テーブルのバックアップ {#back-up-tables}

```sql
BACKUP TABLE `test`.`sbtest01` TO 'local:///mnt/backup/sbtest01/';
```

```sql
BACKUP TABLE sbtest02, sbtest03, sbtest04 TO 'local:///mnt/backup/sbtest/';
```

### クラスター全体をバックアップする {#back-up-the-entire-cluster}

```sql
BACKUP DATABASE * TO 'local:///mnt/backup/full/';
```

システム テーブル ( `mysql.*` `PERFORMANCE_SCHEMA.*` …) `INFORMATION_SCHEMA.*`バックアップに含まれないことに注意してください。

### 外部ストレージ {#external-storages}

BR はS3 または GCS へのデータのバックアップをサポートしています。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

URL 構文については[外部ストレージサービスのURI形式](/external-storage-uri.md)でさらに詳しく説明します。

資格情報を配布すべきでないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`使用すると、TiKV ノードあたりの平均アップロード速度が制限され、ネットワーク帯域幅が削減されます。

バックアップが完了する前に、 `BACKUP`指定すると、クラスタ上のデータに対してチェックサムが実行され、データの正確性が検証されます。デフォルトでは、単一テーブルに対するチェックサムタスクの同時実行数は4ですが、 `CHECKSUM_CONCURRENCY`パラメータを使用して調整できます。データ検証が不要であると確信できる場合は、 `CHECKSUM`パラメータを`FALSE`に設定することで、チェックを無効にすることができます。

BR がテーブルとインデックスのバックアップに同時に実行できるタスク数を指定するには、パラメータ`CONCURRENCY`使用します。このパラメータはBR内のスレッドプールサイズを制御し、バックアップ操作のパフォーマンスと効率を最適化します。

1つのタスクは、バックアップスキーマに応じて、1つのテーブル範囲または1つのインデックス範囲を表します。1つのテーブルと1つのインデックスの場合、このテーブルのバックアップには2つのタスクが使用されます。デフォルト値は`CONCURRENCY`で、 `4`です。多数のテーブルまたはインデックスをバックアップする必要がある場合は、この値を増やしてください。

統計はデフォルトではバックアップされません。統計情報をバックアップするには、 `IGNORE_STATS`パラメータを`FALSE`に設定する必要があります。

デフォルトでは、バックアップによって生成されるSSTファイルは`zstd`圧縮アルゴリズムを使用します。必要に応じて、 `COMPRESSION_TYPE`パラメータを使用して別の圧縮アルゴリズムを指定できます。サポートされているアルゴリズムは`lz4` `zstd` 。また、 `COMPRESSION_LEVEL`パラメータを使用して圧縮レベルを調整することもできます。レベル番号が大きいほど圧縮率は高くなりますが、CPU消費量`snappy`増加します。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### スナップショット {#snapshot}

履歴データをバックアップするには、タイムスタンプ、TSO、または相対時間を指定します。

```sql
-- relative time
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist01'
    SNAPSHOT = 36 HOUR AGO;

-- timestamp (in current time zone)
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    SNAPSHOT = '2020-04-01 12:00:00';

-- timestamp oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    SNAPSHOT = 415685305958400;
```

相対時間でサポートされている単位は次のとおりです。

-   マイクロ秒
-   2番
-   分
-   時間
-   日
-   週

SQL 標準に従うと、単位は常に単数形になることに注意してください。

### 増分バックアップ {#incremental-backup}

最後のバックアップから現在のスナップショットまでの変更のみをバックアップするには、 `LAST_BACKUP`オプションを指定します。

```sql
-- timestamp (in current time zone)
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- timestamp oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [復元する](/sql-statements/sql-statement-restore.md)
-   [バックアップを表示](/sql-statements/sql-statement-show-backups.md)
