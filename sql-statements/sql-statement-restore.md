---
title: RESTORE | TiDB SQL Statement Reference
summary: An overview of the usage of RESTORE for the TiDB database.
---

# 復元する {#restore}

このステートメントは、 [`BACKUP`文](/sql-statements/sql-statement-backup.md)によって以前に作成されたバックアップ アーカイブから分散復元を実行します。

> **警告：**
>
> -   この機能は実験的です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。
> -   この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

`RESTORE`ステートメントは[BRツール](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)と同じエンジンを使用しますが、復元プロセスが別個のBRツールではなく TiDB 自体によって駆動される点が異なります。 BRのすべての利点と注意事項がここにも適用されます。特に、 **`RESTORE`現在ACIDに準拠していません**。 `RESTORE`を実行する前に、次の要件が満たされていることを確認してください。

-   クラスターは「オフライン」であり、現在の TiDB セッションは、復元されるすべてのテーブルにアクセスできる唯一のアクティブな SQL 接続です。
-   完全復元を実行する場合、既存のデータが上書きされ、データとインデックスの間で不整合が生じる可能性があるため、復元されるテーブルがまだ存在してはいけません。
-   増分復元が実行されている場合、テーブルはバックアップ作成時の`LAST_BACKUP`タイムスタンプとまったく同じ状態になっている必要があります。

`RESTORE`を実行するには、 `RESTORE_ADMIN`または`SUPER`権限が必要です。さらに、リストアを実行する TiDB ノードとクラスター内のすべての TiKV ノードの両方に、宛先からの読み取り権限が必要です。

`RESTORE`ステートメントはブロックされており、復元タスク全体が完了、失敗、またはキャンセルされた後にのみ終了します。 `RESTORE`を実行するには、長時間持続する接続を準備する必要があります。タスクは[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

`BACKUP`と`RESTORE`タスクは一度に 1 つだけ実行できます。 `BACKUP`または`RESTORE`タスクが同じ TiDBサーバー上ですでに実行されている場合、新しい`RESTORE`実行は、前のタスクがすべて完了するまで待機します。

`RESTORE` 「tikv」storageエンジンでのみ使用できます。 「unistore」エンジンで`RESTORE`使用すると失敗します。

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

### バックアップアーカイブから復元する {#restore-from-backup-archive}

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

上の例では、すべてのデータがローカル ファイル システムのバックアップ アーカイブから復元されます。データは、すべての TiDB および TiKV ノードに分散された`/mnt/backup/2020/04/`ディレクトリから SST ファイルとして読み込まれます。

上記の結果の最初の行は次のように説明されます。

| カラム              | 説明                                             |
| :--------------- | :--------------------------------------------- |
| `Destination`    | 読み取り先の URL                                     |
| `Size`           | バックアップ アーカイブの合計サイズ (バイト単位)                     |
| `BackupTS`       | （使用されていない）                                     |
| `Queue Time`     | `RESTORE`のタスクがキューに入れられたときのタイムスタンプ (現在のタイムゾーン)。 |
| `Execution Time` | `RESTORE`タスクの実行が開始されたときのタイムスタンプ (現在のタイムゾーン)。   |

### 部分復元 {#partial-restore}

どのデータベースまたはテーブルを復元するかを指定できます。一部のデータベースまたはテーブルがバックアップ アーカイブにない場合、それらは無視されるため、 `RESTORE`何もせずに完了します。

```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```

```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### 外部ストレージ {#external-storages}

BR は、 S3 または GCS からのデータの復元をサポートしています。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/';
```

<CustomContent platform="tidb">

URL 構文については、 [外部ストレージ サービスの URI 形式](/external-storage-uri.md)で詳しく説明します。

</CustomContent>

<CustomContent platform="tidb-cloud">

URL 構文については、 [外部storageURI](https://docs.pingcap.com/tidb/stable/external-storage-uri)で詳しく説明します。

</CustomContent>

認証情報を配布しないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`を使用すると、TiKV ノードごとの平均ダウンロード速度が制限され、ネットワーク帯域幅が削減されます。

デフォルトでは、TiDB ノードは 128 の復元スレッドを実行します。この値は`CONCURRENCY`オプションで調整できます。

復元が完了する前に、アーカイブのデータに対してチェック`RESTORE`を実行して、正確性を検証します。このステップが不要であると確信できる場合は、 `CHECKSUM`オプションを使用して無効にすることができます。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### 増分復元 {#incremental-restore}

増分復元を実行するための特別な構文はありません。 TiDB は、バックアップ アーカイブがフルであるか増分であるかを認識し、適切なアクションを実行します。各増分復元を正しい順序で適用するだけで済みます。

たとえば、バックアップ タスクが次のように作成されたとします。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

その場合は、復元でも同じ順序を適用する必要があります。

```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [復元を表示](/sql-statements/sql-statement-show-backups.md)
