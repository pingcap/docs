---
title: RESTORE | TiDB SQL Statement Reference
summary: TiDB データベースの RESTORE の使用法の概要。
---

# 復元する {#restore}

このステートメントは、 [`BACKUP`ステートメント](/sql-statements/sql-statement-backup.md)によって以前に作成されたバックアップ アーカイブからの分散復元を実行します。

> **警告：**
>
> -   この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。
> -   この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

`RESTORE`ステートメントは[BRツール](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)と同じエンジンを使用しますが、リストアプロセスは別のBRツールではなく TiDB 自体によって実行されます。BRの利点と注意事項はすべてここにも適用されます。特に、 **`RESTORE`現在ACID準拠ではありません**。 `RESTORE`実行する前に、以下の要件が満たされていることを確認してください。

-   クラスターは「オフライン」であり、現在の TiDB セッションは復元中のすべてのテーブルにアクセスするための唯一のアクティブな SQL 接続です。
-   完全な復元を実行する場合、既存のデータが上書きされ、データとインデックスの間に不整合が生じる可能性があるため、復元対象のテーブルがすでに存在していてはいけません。
-   増分復元が実行されている場合、テーブルはバックアップが作成された時点の`LAST_BACKUP`のタイムスタンプとまったく同じ状態になっている必要があります。

`RESTORE`実行するには、 `RESTORE_ADMIN`または`SUPER`権限が必要です。さらに、リストアを実行するTiDBノードとクラスター内のすべてのTiKVノードの両方に、リストア先からの読み取り権限が必要です。

`RESTORE`文はブロッキングであり、復元タスク全体が完了、失敗、またはキャンセルされた後にのみ終了します。3 `RESTORE`を実行するには、長時間持続する接続を用意する必要があります。タスクは[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)文を使用してキャンセルできます。

一度に実行できるタスク`BACKUP`と`RESTORE` 1 つだけです。同じ TiDBサーバー上でタスク番号`BACKUP`または`RESTORE`既に実行されている場合、新しいタスク`RESTORE`実行は、前のタスクがすべて完了するまで待機します。

`RESTORE` 「tikv」storageエンジンでのみ使用できます。2 `RESTORE` 「unistore」エンジンで使用すると失敗します。

## 概要 {#synopsis}

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

### バックアップアーカイブからの復元 {#restore-from-backup-archive}

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

上記の例では、すべてのデータがローカルファイルシステムのバックアップアーカイブから復元されます。データは、すべてのTiDBノードとTiKVノードに分散された`/mnt/backup/2020/04/`ディレクトリからSSTファイルとして読み込まれます。

上記の結果の最初の行は次のように記述されます。

| カラム              | 説明                                             |
| :--------------- | :--------------------------------------------- |
| `Destination`    | 読み取る先のURL                                      |
| `Size`           | バックアップアーカイブの合計サイズ（バイト単位）                       |
| `BackupTS`       | （未使用）                                          |
| `Queue Time`     | `RESTORE`のタスクがキューに入れられたときのタイムスタンプ (現在のタイムゾーン)。 |
| `Execution Time` | `RESTORE`タスクの実行が開始されたときのタイムスタンプ (現在のタイムゾーン)。   |

### 部分的な復元 {#partial-restore}

復元するデータベースまたはテーブルを指定できます。バックアップアーカイブにデータベースまたはテーブルが欠落している場合、それらは無視され、 `RESTORE`もせずに完了します。

```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```

```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### 外部ストレージ {#external-storages}

BR はS3 または GCS からのデータの復元をサポートしています。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/';
```

URL 構文については[外部ストレージサービスのURI形式](/external-storage-uri.md)でさらに詳しく説明します。

資格情報を配布すべきでないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`使用すると、TiKV ノードあたりの平均ダウンロード速度が制限され、ネットワーク帯域幅が削減されます。

復元が完了する前に、 `RESTORE`指定すると、バックアップファイルのデータに対してチェックサムが実行され、データの正確性が検証されます。単一テーブルに対するチェックサムタスクのデフォルトの同時実行数は 4 ですが、 `CHECKSUM_CONCURRENCY`パラメータを使用して調整できます。データ検証が不要であると確信できる場合は、 `CHECKSUM`パラメータを`FALSE`に設定することでチェックを無効にすることができます。

統計情報がバックアップされている場合、復元時にデフォルトで復元されます。統計情報を復元する必要がない場合は、 `LOAD_STATS`パラメータを`FALSE`に設定できます。

<CustomContent platform="tidb">

システム[権限テーブル](/privilege-management.md#privilege-table)デフォルトで復元されます。システム権限テーブルを復元する必要がない場合は、パラメータ`WITH_SYS_TABLE` `FALSE`に設定できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

システム[権限テーブル](https://docs.pingcap.com/tidb/stable/privilege-management#privilege-table)デフォルトで復元されます。システム権限テーブルを復元する必要がない場合は、パラメータ`WITH_SYS_TABLE` `FALSE`に設定できます。

</CustomContent>

デフォルトでは、復元タスクはTiFlashレプリカが完全に作成されるまで待機せずに完了します。復元タスクを待機させる必要がある場合は、パラメータ`WAIT_TIFLASH_READY` `TRUE`に設定できます。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### 増分復元 {#incremental-restore}

増分リストアを実行するための特別な構文はありません。TiDBはバックアップアーカイブが完全か増分かを認識し、適切なアクションを実行します。各増分リストアを正しい順序で適用するだけで済みます。

たとえば、次のようにバックアップ タスクが作成されたとします。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

復元時にも同じ順序を適用する必要があります。

```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [復元を表示](/sql-statements/sql-statement-show-backups.md)
