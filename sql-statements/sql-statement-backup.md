---
title: BACKUP | TiDB SQL Statement Reference
summary: An overview of the usage of BACKUP for the TiDB database.
---

# バックアップ {#backup}

このステートメントは、TiDBクラスタの分散バックアップを実行するために使用されます。

`BACKUP`のステートメントは、バックアッププロセスが個別のBRツールではなく、TiDB自体によって駆動されることを除いて、 [BRツール](/br/backup-and-restore-tool.md)と同じエンジンを使用します。 BRのすべての利点と警告は、このステートメントにも適用されます。

`BACKUP`を実行するには、 `BACKUP_ADMIN`または`SUPER`の特権が必要です。さらに、バックアップを実行するTiDBノードとクラスタのすべてのTiKVノードの両方に、宛先への読み取りまたは書き込み権限が必要です。 [セキュリティ強化モード](/system-variables.md#tidb_enable_enhanced_security)が有効になっている場合、ローカルストレージ（ `local://`で始まるストレージパス）は許可されません。

`BACKUP`ステートメントは、バックアップタスク全体が終了するか、失敗するか、キャンセルされるまでブロックされます。 `BACKUP`を実行するために、長続きする接続を準備する必要があります。タスクは、 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

一度に実行できるタスクは`BACKUP`つと[`RESTORE`](/sql-statements/sql-statement-restore.md)つだけです。 `BACKUP`または`RESTORE`ステートメントが同じTiDBサーバーですでに実行されている場合、新しい`BACKUP`の実行は、前のすべてのタスクが終了するまで待機します。

`BACKUP`は、「tikv」ストレージエンジンでのみ使用できます。 「unistore」エンジンで`BACKUP`を使用すると失敗します。

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

上記の例では、 `test`のデータベースがローカルファイルシステムにバックアップされています。データは、すべてのTiDBノードとTiKVノードに分散された`/mnt/backup/2020/04/`のディレクトリにSSTファイルとして保存されます。

上記の結果の最初の行は次のように説明されています。

| 桁                | 説明                                                                  |
| :--------------- | :------------------------------------------------------------------ |
| `Destination`    | 宛先URL                                                               |
| `Size`           | バックアップアーカイブの合計サイズ（バイト単位）                                            |
| `BackupTS`       | バックアップが作成されたときのスナップショットのTSO（ [増分バックアップ](#incremental-backup)に役立ちます） |
| `Queue Time`     | `BACKUP`のタスクがキューに入れられたときのタイムスタンプ（現在のタイムゾーン）。                        |
| `Execution Time` | `BACKUP`のタスクが実行を開始したときのタイムスタンプ（現在のタイムゾーン）。                          |

### テーブルをバックアップする {#back-up-tables}

{{< copyable "" >}}

```sql
BACKUP TABLE `test`.`sbtest01` TO 'local:///mnt/backup/sbtest01/';
```

{{< copyable "" >}}

```sql
BACKUP TABLE sbtest02, sbtest03, sbtest04 TO 'local:///mnt/backup/sbtest/';
```

### クラスタ全体をバックアップする {#back-up-the-entire-cluster}

{{< copyable "" >}}

```sql
BACKUP DATABASE * TO 'local:///mnt/backup/full/';
```

システムテーブル（ `mysql.*` 、 `INFORMATION_SCHEMA.*` ）はバックアップに含まれないことに注意して`PERFORMANCE_SCHEMA.*` 。

### 外部ストレージ {#external-storages}

BRは、S3またはGCSへのデータのバックアップをサポートしています。

{{< copyable "" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?region=us-west-2&access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

URL構文については、 [外部ストレージ](/br/backup-and-restore-storages.md)で詳しく説明しています。

クレデンシャルを配布してはならないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

{{< copyable "" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?region=us-west-2'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`を使用して、TiKVノードあたりの平均アップロード速度を制限し、ネットワーク帯域幅を減らします。

デフォルトでは、すべてのTiKVノードが4つのバックアップスレッドを実行します。この値は、 `CONCURRENCY`オプションで調整できます。

バックアップが完了する前に、 `BACKUP`はクラスタ上のデータに対してチェックサムを実行して、正確性を検証します。これが不要であると確信している場合は、 `CHECKSUM`オプションを使用してこの手順を無効にすることができます。

{{< copyable "" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### スナップショット {#snapshot}

履歴データをバックアップするためのタイムスタンプ、TSO、または相対時間を指定します。

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

相対時間でサポートされる単位は次のとおりです。

-   マイクロ秒
-   2番目
-   分
-   時間
-   日
-   週

SQL標準に従って、単位は常に単数であることに注意してください。

### 増分バックアップ {#incremental-backup}

最後のバックアップから現在のスナップショットまでの変更のみをバックアップする`LAST_BACKUP`のオプションを指定します。

{{< copyable "" >}}

```sql
-- timestamp (in current time zone)
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- timestamp oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [戻す](/sql-statements/sql-statement-restore.md)
-   [バックアップを表示する](/sql-statements/sql-statement-show-backups.md)
