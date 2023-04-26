---
title: RESTORE | TiDB SQL Statement Reference
summary: An overview of the usage of RESTORE for the TiDB database.
---

# 戻す {#restore}

このステートメントは、以前に[`BACKUP`ステートメント](/sql-statements/sql-statement-backup.md)によって作成されたバックアップ アーカイブから分散復元を実行します。

`RESTORE`ステートメントは[BRツール](/br/backup-and-restore-overview.md)と同じエンジンを使用しますが、復元プロセスが別のBRツールではなく TiDB 自体によって駆動される点が異なります。 BRのすべての利点と注意事項がここにも適用されます。特に、 **`RESTORE`現在ACIDに準拠していません**。 `RESTORE`を実行する前に、次の要件が満たされていることを確認してください。

-   クラスターは「オフライン」であり、現在の TiDB セッションは、復元中のすべてのテーブルにアクセスできる唯一のアクティブな SQL 接続です。
-   既存のデータが上書きされ、データとインデックスの間で不整合が生じる可能性があるため、完全復元が実行されている場合、復元されるテーブルはまだ存在していてはなりません。
-   増分復元が実行されている場合、テーブルは、バックアップが作成されたときのタイムスタンプ`LAST_BACKUP`とまったく同じ状態である必要があります。

`RESTORE`を実行するには、 `RESTORE_ADMIN`または`SUPER`特権が必要です。さらに、復元を実行する TiDB ノードとクラスター内のすべての TiKV ノードの両方に、復元先からの読み取り権限が必要です。

`RESTORE`ステートメントはブロックされており、復元タスク全体が終了、失敗、またはキャンセルされた後にのみ終了します。 `RESTORE`を実行するには、持続的な接続を準備する必要があります。タスクは[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

一度に実行できるタスクは`BACKUP`と`RESTORE`つだけです。 `BACKUP`または`RESTORE`タスクが同じ TiDBサーバーで既に実行されている場合、新しい`RESTORE`実行は、前のすべてのタスクが完了するまで待機します。

`RESTORE`は「tikv」storageエンジンでのみ使用できます。 「unistore」エンジンで`RESTORE`使用すると失敗します。

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

### バックアップ アーカイブからの復元 {#restore-from-backup-archive}

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

上記の例では、すべてのデータがローカル ファイル システムのバックアップ アーカイブから復元されます。データは、すべての TiDB および TiKV ノードに分散された`/mnt/backup/2020/04/`のディレクトリから SST ファイルとして読み取られます。

上記の結果の最初の行は、次のように記述されます。

| カラム              | 説明                                                 |
| :--------------- | :------------------------------------------------- |
| `Destination`    | 読み取り元の宛先 URL                                       |
| `Size`           | バックアップ アーカイブの合計サイズ (バイト単位)                         |
| `BackupTS`       | （使用されていない）                                         |
| `Queue Time`     | `RESTORE`のタスクがキューに入れられたときの (現在のタイム ゾーンでの) タイムスタンプ。 |
| `Execution Time` | `RESTORE`のタスクの実行が開始されたときの (現在のタイム ゾーンでの) タイムスタンプ。  |

### 部分復元 {#partial-restore}

復元するデータベースまたはテーブルを指定できます。一部のデータベースまたはテーブルがバックアップ アーカイブにない場合、それらは無視されるため、 `RESTORE`何もせずに完了します。

{{< copyable "" >}}

```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```

{{< copyable "" >}}

```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### 外部ストレージ {#external-storages}

BR は、 S3 または GCS からのデータの復元をサポートしています。

{{< copyable "" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/';
```

URL 構文については、 [外部storageURL](/br/backup-and-restore-storages.md#url-format)で詳しく説明しています。

認証情報を配布してはならないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

{{< copyable "" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`を使用して、TiKV ノードごとの平均ダウンロード速度を制限し、ネットワーク帯域幅を減らします。

デフォルトでは、TiDB ノードは 128 の復元スレッドを実行します。この値は`CONCURRENCY`オプションで調整できます。

復元が完了する前に、アーカイブからのデータに対してチェック`RESTORE`を実行して、正確性を検証します。これが不要であることが確実な場合は、オプション`CHECKSUM`を使用してこのステップを無効にすることができます。

{{< copyable "" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### 増分復元 {#incremental-restore}

増分復元を実行するための特別な構文はありません。 TiDB は、バックアップ アーカイブが完全か増分かを認識し、適切なアクションを実行します。それぞれの増分復元を正しい順序で適用するだけで済みます。

たとえば、次のようにバックアップ タスクを作成するとします。

{{< copyable "" >}}

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

次に、復元時に同じ順序を適用する必要があります。

{{< copyable "" >}}

```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [復元を表示](/sql-statements/sql-statement-show-backups.md)
