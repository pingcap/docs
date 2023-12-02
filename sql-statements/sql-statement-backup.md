---
title: BACKUP | TiDB SQL Statement Reference
summary: An overview of the usage of BACKUP for the TiDB database.
---

# バックアップ {#backup}

このステートメントは、TiDB クラスターの分散バックアップを実行するために使用されます。

> **警告：**
>
> -   この機能は実験的です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。
> -   この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

`BACKUP`ステートメントは[BRツール](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)と同じエンジンを使用しますが、バックアップ プロセスが別個のBRツールではなく TiDB 自体によって駆動される点が異なります。 BRのすべての利点と警告は、この声明にも当てはまります。

`BACKUP`を実行するには、 `BACKUP_ADMIN`または`SUPER`権限が必要です。さらに、バックアップを実行する TiDB ノードとクラスター内のすべての TiKV ノードの両方に、宛先への読み取りまたは書き込み権限が必要です。 [Security強化モード](/system-variables.md#tidb_enable_enhanced_security)が有効な場合、ローカルstorage( `local://`で始まるstorageパス) は許可されません。

`BACKUP`ステートメントは、バックアップ タスク全体が完了するか、失敗するか、キャンセルされるまでブロックされます。 `BACKUP`を実行するには、長時間持続する接続を準備する必要があります。タスクは[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

`BACKUP`と[`RESTORE`](/sql-statements/sql-statement-restore.md)タスクは一度に 1 つだけ実行できます。 `BACKUP`または`RESTORE`ステートメントが同じ TiDBサーバー上ですでに実行されている場合、新しい`BACKUP`ステートメントの実行は、前のタスクがすべて完了するまで待機します。

`BACKUP` 「tikv」storageエンジンでのみ使用できます。 「unistore」エンジンで`BACKUP`使用すると失敗します。

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

### データベースをバックアップする {#back-up-databases}

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

上の例では、 `test`データベースがローカル ファイルシステムにバックアップされます。データは、すべての TiDB ノードと TiKV ノードに分散された`/mnt/backup/2020/04/`のディレクトリに SST ファイルとして保存されます。

上記の結果の最初の行は次のように説明されます。

| カラム              | 説明                                                               |
| :--------------- | :--------------------------------------------------------------- |
| `Destination`    | リンク先の URL                                                        |
| `Size`           | バックアップ アーカイブの合計サイズ (バイト単位)                                       |
| `BackupTS`       | バックアップ作成時のスナップショットの TSO ( [増分バックアップ](#incremental-backup)に役立ちます) |
| `Queue Time`     | `BACKUP`のタスクがキューに入れられたときのタイムスタンプ (現在のタイムゾーン)。                    |
| `Execution Time` | `BACKUP`タスクの実行が開始されたときのタイムスタンプ (現在のタイムゾーン)。                      |

### テーブルをバックアップする {#back-up-tables}

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

システム テーブル ( `mysql.*` 、 `INFORMATION_SCHEMA.*` 、 `PERFORMANCE_SCHEMA.*` 、…) はバックアップに含まれないことに注意してください。

### 外部ストレージ {#external-storages}

BR は、 S3 または GCS へのデータのバックアップをサポートしています。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

<CustomContent platform="tidb">

URL 構文については、 [外部ストレージ サービスの URI 形式](/external-storage-uri.md)で詳しく説明します。

</CustomContent>

<CustomContent platform="tidb-cloud">

URL 構文については、 [外部storageURI](https://docs.pingcap.com/tidb/stable/external-storage-uri)で詳しく説明します。

</CustomContent>

認証情報を配布しないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`を使用すると、TiKV ノードごとの平均アップロード速度が制限され、ネットワーク帯域幅が削減されます。

デフォルトでは、すべての TiKV ノードは 4 つのバックアップ スレッドを実行します。この値は`CONCURRENCY`オプションで調整できます。

バックアップが完了する前に、クラスター上のデータに対してチェック`BACKUP`を実行して、正確さを検証します。このステップが不要であると確信できる場合は、 `CHECKSUM`オプションを使用して無効にすることができます。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### スナップショット {#snapshot}

履歴データをバックアップするタイムスタンプ、TSO、または相対時間を指定します。

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

サポートされている相対時間の単位は次のとおりです。

-   マイクロ秒
-   2番
-   分
-   時間
-   日
-   週

SQL 標準に従って、単位は常に単数であることに注意してください。

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

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [復元する](/sql-statements/sql-statement-restore.md)
-   [バックアップを表示](/sql-statements/sql-statement-show-backups.md)
