---
title: BACKUP | TiDB SQL Statement Reference
summary: TiDB データベースの BACKUP の使用法の概要。
---

# バックアップ {#backup}

このステートメントは、TiDB クラスターの分散バックアップを実行するために使用されます。

> **警告：**
>
> -   この機能は実験的ものです。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。
> -   この機能は[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

`BACKUP`ステートメントは[BRツール](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)と同じエンジンを使用しますが、バックアップ プロセスは別のBRツールではなく TiDB 自体によって実行されます。BR のすべての利点と警告は、このステートメントにも適用されます。

`BACKUP`を実行するには、 `BACKUP_ADMIN`または`SUPER`権限が必要です。さらに、バックアップを実行する TiDB ノードとクラスター内のすべての TiKV ノードの両方に、宛先への読み取りまたは書き込み権限が必要です。9 [Security強化モード](/system-variables.md#tidb_enable_enhanced_security)有効になっている場合、ローカルstorage( `local://`で始まるstorageパス) は許可されません。

`BACKUP`ステートメントは、バックアップ タスク全体が完了するか、失敗するか、キャンセルされるまでブロックされます。 `BACKUP`を実行するには、長時間持続する接続を準備する必要があります。 タスクは、 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

一度に実行できるタスク`BACKUP`と[`RESTORE`](/sql-statements/sql-statement-restore.md)は 1 つだけです。同じ TiDBサーバーで`BACKUP`または`RESTORE`ステートメントがすでに実行されている場合、新しい`BACKUP`実行は、以前のすべてのタスクが完了するまで待機します。

`BACKUP` 「tikv」storageエンジンでのみ使用できます。「unistore」エンジンで`BACKUP`を使用すると失敗します。

## 概要 {#synopsis}

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

上記の例では、 `test`データベースがローカル ファイル システムにバックアップされます。データは、すべての TiDB ノードと TiKV ノードに分散された`/mnt/backup/2020/04/`ディレクトリに SST ファイルとして保存されます。

上記の結果の最初の行は次のように説明されます。

| カラム              | 説明                                                             |
| :--------------- | :------------------------------------------------------------- |
| `Destination`    | リンク先URL                                                        |
| `Size`           | バックアップアーカイブの合計サイズ（バイト単位）                                       |
| `BackupTS`       | バックアップ作成時のスナップショットのTSO（ [増分バックアップ](#incremental-backup)の場合に便利） |
| `Queue Time`     | `BACKUP`タスクがキューに入れられたときのタイムスタンプ (現在のタイムゾーン)。                   |
| `Execution Time` | `BACKUP`タスクの実行が開始されたときのタイムスタンプ (現在のタイム ゾーン)。                   |

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

<CustomContent platform="tidb">

URL 構文については[外部ストレージサービスの URI 形式](/external-storage-uri.md)でさらに詳しく説明します。

</CustomContent>

<CustomContent platform="tidb-cloud">

URL 構文については[外部storageURI](https://docs.pingcap.com/tidb/stable/external-storage-uri)でさらに詳しく説明します。

</CustomContent>

資格情報を配布しないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`使用すると、TiKV ノードあたりの平均アップロード速度が制限され、ネットワーク帯域幅が削減されます。

デフォルトでは、すべての TiKV ノードは 4 つのバックアップ スレッドを実行します。この値は`CONCURRENCY`オプションで調整できます。

バックアップが完了する前に、 `BACKUP`クラスター上のデータに対してチェックサムを実行し、正確性を検証します。この手順は、不要であることが確実な場合は、 `CHECKSUM`オプションで無効にできます。

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

SQL 標準に従うと、単位は常に単数になることに注意してください。

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

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [復元する](/sql-statements/sql-statement-restore.md)
-   [バックアップを表示](/sql-statements/sql-statement-show-backups.md)
