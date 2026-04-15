---
title: RESTORE | TiDB SQL Statement Reference
summary: TiDBデータベースにおけるRESTOREの使用方法の概要。
---

# 復元する {#restore}

このステートメントは[`BACKUP`ステートメント](/sql-statements/sql-statement-backup.md)によって以前に作成されたバックアップ アーカイブから分散復元を実行します。

> **警告：**
>
> -   この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。
> -   この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

`RESTORE`ステートメントは、 [BRツール](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)と同じエンジンを使用しますが、リストア プロセスは別のBRツールではなく TiDB 自体によって実行されます。BR のすべての利点と注意点もここに適用されます。特に、 **`RESTORE`は現在ACID準拠ではありません**。 `RESTORE`実行する前に、次の要件が満たされていることを確認してください。

-   クラスターは「オフライン」状態であり、現在有効なTiDBセッションは、復元中のすべてのテーブルにアクセスできる唯一のアクティブなSQL接続です。
-   完全復元を実行する場合、復元対象のテーブルは既に存在してはなりません。既存のデータが上書きされ、データとインデックス間の不整合が発生する可能性があるためです。
-   増分復元を実行する場合、テーブルはバックアップが作成された時点の`LAST_BACKUP`タイムスタンプとまったく同じ状態である必要があります。

`RESTORE`を実行するには`RESTORE_ADMIN`または`SUPER`権限が必要です。さらに、リストアを実行する TiDB ノードとクラスタ内のすべての TiKV ノードは、宛先からの読み取り権限を持っている必要があります。

`RESTORE`ステートメントはブロッキング処理であり、リストアタスク全体が完了、失敗、またはキャンセルされるまで終了しません。 `RESTORE`を実行するには、長時間接続を準備する必要があります。タスクは[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

`BACKUP`と`RESTORE`のタスクは、一度に 1 つしか実行できません。 `BACKUP`または`RESTORE`タスクが同じ TiDBサーバーで既に実行されている場合、新しい`RESTORE`実行は、以前のすべてのタスクが完了するまで待機します。

`RESTORE` 「tikv」storageエンジンでのみ使用できます。「unistore」エンジンで`RESTORE`を使用すると失敗します。

## あらすじ {#synopsis}

```ebnf+diagram
RestoreStmt ::=
    "RESTORE" BRIETables "FROM" stringLit RestoreOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

RestoreOption ::=
    "CHECKSUM_CONCURRENCY" '='? LengthNum
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "LOAD_STATS" '='? Boolean
|   "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
|   "WAIT_TIFLASH_READY" '='? Boolean
|   "WITH_SYS_TABLE" '='? Boolean

Boolean ::=
    NUM | "TRUE" | "FALSE"
```

## 例 {#examples}

### バックアップアーカイブから復元 {#restore-from-backup-archive}

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

上記の例では、すべてのデータはローカルファイルシステムのバックアップアーカイブから復元されます。データは、すべてのTiDBおよびTiKVノードに分散されている`/mnt/backup/2020/04/`ディレクトリからSSTファイルとして読み込まれます。

上記の結果の最初の行は、次のように説明されています。

| カラム              | 説明                                           |
| :--------------- | :------------------------------------------- |
| `Destination`    | 読み取り元の宛先URL                                  |
| `Size`           | バックアップアーカイブの合計サイズ（バイト単位）                     |
| `BackupTS`       | （未使用）                                        |
| `Queue Time`     | `RESTORE`タスクがキューに登録されたときのタイムスタンプ（現在のタイムゾーン）。 |
| `Execution Time` | `RESTORE`タスクの実行が開始されたときのタイムスタンプ（現在のタイムゾーン）。  |

### 部分的な修復 {#partial-restore}

復元するデータベースまたはテーブルを指定できます。バックアップ アーカイブに一部のデータベースまたはテーブルが存在しない場合でも、それらは無視されるため、 `RESTORE`は何もせずに完了します。

```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```

```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### 外部ストレージ {#external-storages}

BRはS3またはGCSからのデータ復元をサポートしています。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/';
```

URL 構文については[外部ストレージサービスのURI形式](/external-storage-uri.md)で詳しく説明します。

認証情報を配布すべきでないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定してください。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`を使用して、TiKVノードあたりの平均ダウンロード速度を制限し、ネットワーク帯域幅を削減します。

リストアが完了する前に、 `RESTORE`はデフォルトでバックアップ ファイル内のデータに対してチェックサムを実行し、データの正当性を検証します。単一テーブルに対するチェックサム タスクのデフォルトの同時実行数は 4 ですが、 `CHECKSUM_CONCURRENCY`パラメータを使用して調整できます。データの検証が不要であると確信している場合は、 `CHECKSUM`パラメータを`FALSE`に設定することでチェックを無効にできます。

統計情報がバックアップされている場合、復元時にデフォルトで復元されます。統計情報を復元する必要がない場合は、 `LOAD_STATS`パラメーターを`FALSE`に設定できます。

<CustomContent platform="tidb">

システム テーブルはデフォルトで復元されます。システム[権限テーブル](/privilege-management.md#privilege-table)テーブルを復元する必要がない場合は、 `WITH_SYS_TABLE`パラメーターを`FALSE`に設定できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

システム テーブルはデフォルトで復元されます。システム[権限テーブル](https://docs.pingcap.com/tidb/stable/privilege-management#privilege-table)テーブルを復元する必要がない場合は、 `WITH_SYS_TABLE`パラメーターを`FALSE`に設定できます。

</CustomContent>

デフォルトでは、復元タスクはTiFlashレプリカが完全に作成されるのを待たずに完了します。復元タスクを待機させる必要がある場合は、 `WAIT_TIFLASH_READY`パラメーターを`TRUE`に設定してください。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### 段階的復元 {#incremental-restore}

増分復元を実行するための特別な構文はありません。TiDBはバックアップアーカイブがフルバックアップか増分バックアップかを自動的に認識し、適切な処理を実行します。必要なのは、各増分復元を正しい順序で適用することだけです。

例えば、バックアップタスクが次のように作成された場合：

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

そして、復元時にも同じ順序を適用する必要があります。

```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [ショーが復元する](/sql-statements/sql-statement-show-backups.md)
