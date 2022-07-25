---
title: RESTORE | TiDB SQL Statement Reference
summary: An overview of the usage of RESTORE for the TiDB database.
---

# 戻す {#restore}

このステートメントは、以前に[`BACKUP`ステートメント](/sql-statements/sql-statement-backup.md)によって作成されたバックアップアーカイブから分散復元を実行します。

`RESTORE`ステートメントは[BRツール](/br/backup-and-restore-overview.md)と同じエンジンを使用しますが、復元プロセスが個別のBRツールではなくTiDB自体によって駆動される点が異なります。 BRのすべての利点と警告もここに適用されます。特に、 **`RESTORE`は現在ACIDに準拠していません**。 `RESTORE`を実行する前に、次の要件が満たされていることを確認してください。

-   クラスタは「オフライン」であり、現在のTiDBセッションは、復元されるすべてのテーブルにアクセスするための唯一のアクティブなSQL接続です。
-   完全な復元が実行されている場合、既存のデータが上書きされ、データとインデックスの間に不整合が生じる可能性があるため、復元されるテーブルはまだ存在していないはずです。
-   インクリメンタルリストアが実行されているとき、テーブルはバックアップが作成されたときの`LAST_BACKUP`タイムスタンプとまったく同じ状態である必要があります。

`RESTORE`を実行するには、 `RESTORE_ADMIN`または`SUPER`の特権が必要です。さらに、復元を実行するTiDBノードとクラスタのすべてのTiKVノードの両方に、宛先からの読み取りアクセス許可が必要です。

`RESTORE`のステートメントはブロックされており、復元タスク全体が終了、失敗、またはキャンセルされた後にのみ終了します。 `RESTORE`を実行するために、長期的な接続を準備する必要があります。タスクは、 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

一度に実行できるタスクは`BACKUP`つと`RESTORE`つだけです。 `BACKUP`または`RESTORE`のタスクが同じTiDBサーバーですでに実行されている場合、新しい`RESTORE`の実行は、前のすべてのタスクが完了するまで待機します。

`RESTORE`は、「tikv」ストレージエンジンでのみ使用できます。 「unistore」エンジンで`RESTORE`を使用すると失敗します。

## あらすじ {#synopsis}

```ebnf+diagram
RestoreStmt ::=
    "RESTORE" BRIETables "FROM" stringLit RestoreOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

RestoreOption ::=
    "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean

Boolean ::=
    NUM | "TRUE" | "FALSE"
```

## 例 {#examples}

### バックアップアーカイブから復元 {#restore-from-backup-archive}

{{< copyable "" >}}

```sql
RESTORE DATABASE * FROM 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+----------+---------------------+---------------------+
| Destination                  | Size      | BackupTS | Queue Time          | Execution Time      |
+------------------------------+-----------+----------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 0        | 2020-04-21 17:16:55 | 2020-04-21 17:16:55 |
+------------------------------+-----------+----------+---------------------+---------------------+
1 row in set (28.961 sec)
```

上記の例では、すべてのデータがローカルファイルシステムのバックアップアーカイブから復元されます。データは、すべてのTiDBノードとTiKVノードに分散された`/mnt/backup/2020/04/`のディレクトリからSSTファイルとして読み取られます。

上記の結果の最初の行は次のように説明されています。

| カラム              | 説明                                            |
| :--------------- | :-------------------------------------------- |
| `Destination`    | 読み取る先URL                                      |
| `Size`           | バックアップアーカイブの合計サイズ（バイト単位）                      |
| `BackupTS`       | （使用されていない）                                    |
| `Queue Time`     | `RESTORE`のタスクがキューに入れられたときのタイムスタンプ（現在のタイムゾーン）。 |
| `Execution Time` | `RESTORE`のタスクが実行を開始したときのタイムスタンプ（現在のタイムゾーン）。   |

### 部分的な復元 {#partial-restore}

復元するデータベースまたはテーブルを指定できます。一部のデータベースまたはテーブルがバックアップアーカイブから欠落している場合、それらは無視されるため、 `RESTORE`は何もせずに完了します。

{{< copyable "" >}}

```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```

{{< copyable "" >}}

```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### 外部ストレージ {#external-storages}

BRは、S3またはGCSからのデータの復元をサポートしています。

{{< copyable "" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/?region=us-west-2';
```

URL構文については、 [外部ストレージ](/br/backup-and-restore-storages.md)で詳しく説明しています。

クレデンシャルを配布してはならないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

{{< copyable "" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/?region=us-west-2'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`を使用して、TiKVノードごとの平均ダウンロード速度を制限し、ネットワーク帯域幅を減らします。

デフォルトでは、TiDBノードは128の復元スレッドを実行します。この値は、 `CONCURRENCY`オプションで調整できます。

復元が完了する前に、 `RESTORE`はアーカイブからのデータに対してチェックサムを実行して、正確性を検証します。これが不要であると確信できる場合は、 `CHECKSUM`オプションを使用してこの手順を無効にすることができます。

{{< copyable "" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### インクリメンタルリストア {#incremental-restore}

インクリメンタルリストアを実行するための特別な構文はありません。 TiDBは、バックアップアーカイブがフルかインクリメンタルかを認識し、適切なアクションを実行します。各増分復元を正しい順序で適用するだけで済みます。

たとえば、バックアップタスクが次のように作成された場合：

{{< copyable "" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

次に、同じ順序を復元に適用する必要があります。

{{< copyable "" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [復元を表示](/sql-statements/sql-statement-show-backups.md)
