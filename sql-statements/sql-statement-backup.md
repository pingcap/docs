---
title: BACKUP | TiDB SQL Statement Reference
summary: An overview of the usage of BACKUP for the TiDB database.
---

# バックアップ {#backup}

このステートメントは、TiDB クラスターの分散バックアップを実行するために使用されます。

`BACKUP`ステートメントは[BRツール](/br/backup-and-restore-overview.md)ステートメントと同じエンジンを使用しますが、バックアップ プロセスが別のBRツールではなく TiDB 自体によって駆動される点が異なります。 BRのすべての利点と警告は、このステートメントにも適用されます。

`BACKUP`を実行するには、 `BACKUP_ADMIN`または`SUPER`のいずれかの特権が必要です。さらに、バックアップを実行する TiDB ノードとクラスター内のすべての TiKV ノードの両方に、宛先への読み取りまたは書き込み権限が必要です。 [Security強化モード](/system-variables.md#tidb_enable_enhanced_security)が有効な場合、ローカルstorage( `local://`で始まるstorageパス) は許可されません。

`BACKUP`ステートメントは、バックアップ タスク全体が終了、失敗、またはキャンセルされるまでブロックされます。 `BACKUP`を実行するには、持続的な接続を準備する必要があります。タスクは[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

一度に実行できるタスクは`BACKUP`と[`RESTORE`](/sql-statements/sql-statement-restore.md)つだけです。 `BACKUP`または`RESTORE`ステートメントが同じ TiDBサーバーで既に実行されている場合、新しい`BACKUP`実行は、前のすべてのタスクが完了するまで待機します。

`BACKUP`は「tikv」storageエンジンでのみ使用できます。 「unistore」エンジンで`BACKUP`使用すると失敗します。

## あらすじ {#synopsis}

```ebnf+diagram
BackupStmt ::=
    "BACKUP" BRIETables "TO" stringLit BackupOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

BackupOption ::=
    "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
|   "LAST_BACKUP" '='? BackupTSO
|   "SNAPSHOT" '='? ( BackupTSO | LengthNum TimestampUnit "AGO" )

Boolean ::=
    NUM | "TRUE" | "FALSE"

BackupTSO ::=
    LengthNum | stringLit
```

## 例 {#examples}

### データベースのバックアップ {#back-up-databases}

{{< copyable "" >}}

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

上記の例では、 `test`データベースがローカル ファイルシステムにバックアップされます。データは、すべての TiDB および TiKV ノードに分散された`/mnt/backup/2020/04/`のディレクトリに SST ファイルとして保存されます。

上記の結果の最初の行は、次のように記述されます。

| カラム              | 説明                                                                    |
| :--------------- | :-------------------------------------------------------------------- |
| `Destination`    | リンク先 URL                                                              |
| `Size`           | バックアップ アーカイブの合計サイズ (バイト単位)                                            |
| `BackupTS`       | バックアップが作成されたときのスナップショットの TSO ( [増分バックアップ](#incremental-backup)に役立ちます) |
| `Queue Time`     | `BACKUP`のタスクがキューに入れられたときのタイムスタンプ (現在のタイム ゾーン)。                        |
| `Execution Time` | `BACKUP`のタスクの実行が開始されたときの (現在のタイム ゾーンでの) タイムスタンプ。                      |

### テーブルのバックアップ {#back-up-tables}

{{< copyable "" >}}

```sql
BACKUP TABLE `test`.`sbtest01` TO 'local:///mnt/backup/sbtest01/';
```

{{< copyable "" >}}

```sql
BACKUP TABLE sbtest02, sbtest03, sbtest04 TO 'local:///mnt/backup/sbtest/';
```

### クラスター全体をバックアップする {#back-up-the-entire-cluster}

{{< copyable "" >}}

```sql
BACKUP DATABASE * TO 'local:///mnt/backup/full/';
```

システム テーブル ( `mysql.*` 、 `INFORMATION_SCHEMA.*` 、 `PERFORMANCE_SCHEMA.*` 、…) はバックアップに含まれないことに注意してください。

### 外部ストレージ {#external-storages}

BR は、 S3 または GCS へのデータのバックアップをサポートしています。

{{< copyable "" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

URL 構文については、 [外部storageURL](/br/backup-and-restore-storages.md#url-format)で詳しく説明しています。

認証情報を配布してはならないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

{{< copyable "" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`を使用して、TiKV ノードごとの平均アップロード速度を制限し、ネットワーク帯域幅を減らします。

デフォルトでは、すべての TiKV ノードが 4 つのバックアップ スレッドを実行します。この値は`CONCURRENCY`オプションで調整できます。

バックアップが完了する前に、クラスタ上のデータに対してチェック`BACKUP`を実行して、正確性を確認します。これが不要であることが確実な場合は、オプション`CHECKSUM`を使用してこのステップを無効にすることができます。

{{< copyable "" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### スナップショット {#snapshot}

履歴データをバックアップするタイムスタンプ、TSO、または相対時間を指定します。

{{< copyable "" >}}

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

SQL 標準に従って、単位は常に単数であることに注意してください。

### 増分バックアップ {#incremental-backup}

最後のバックアップから現在のスナップショットまでの変更のみをバックアップするには、 `LAST_BACKUP`オプションを指定します。

{{< copyable "" >}}

```sql
-- timestamp (in current time zone)
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- timestamp oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [戻す](/sql-statements/sql-statement-restore.md)
-   [バックアップを表示](/sql-statements/sql-statement-show-backups.md)
