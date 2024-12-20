---
title: RESTORE | TiDB SQL Statement Reference
summary: TiDB データベースの RESTORE の使用法の概要。
---

# 復元する {#restore}

このステートメントは、 [`BACKUP`ステートメント](/sql-statements/sql-statement-backup.md)によって以前に作成されたバックアップ アーカイブからの分散復元を実行します。

> **警告：**
>
> -   この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。
> -   この機能は[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

`RESTORE`ステートメントは[BRツール](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)と同じエンジンを使用しますが、復元プロセスは別のBRツールではなく TiDB 自体によって実行されます。BR のすべての利点と注意事項もここで適用されます。特に、RESTORE は現在BR **`RESTORE`ACIDしていません**`RESTORE`実行する前に、次の要件が満たされていることを確認してください。

-   クラスターは「オフライン」であり、現在の TiDB セッションは復元されるすべてのテーブルにアクセスするための唯一のアクティブな SQL 接続です。
-   完全な復元を実行する場合、既存のデータが上書きされ、データとインデックスの間に不整合が生じる可能性があるため、復元するテーブルがすでに存在していてはいけません。
-   増分復元が実行されている場合、テーブルはバックアップが作成された時点の`LAST_BACKUP`番目のタイムスタンプとまったく同じ状態になっている必要があります。

`RESTORE`実行するには、 `RESTORE_ADMIN`または`SUPER`権限が必要です。さらに、復元を実行する TiDB ノードとクラスター内のすべての TiKV ノードの両方に、宛先からの読み取り権限が必要です。

`RESTORE`ステートメントはブロックしており、復元タスク全体が完了、失敗、またはキャンセルされた後にのみ終了します。 `RESTORE`を実行するには、長時間持続する接続を準備する必要があります。 タスクは[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

一度に実行できるタスク`BACKUP`と`RESTORE` 1 つだけです。同じ TiDBサーバー上でタスク`BACKUP`または`RESTORE`すでに実行されている場合、新しいタスク`RESTORE`の実行は、以前のタスクがすべて完了するまで待機します。

`RESTORE` 「tikv」storageエンジンでのみ使用できます。「unistore」エンジンで`RESTORE`使用すると失敗します。

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

上記の例では、すべてのデータはローカル ファイル システムのバックアップ アーカイブから復元されます。データは、すべての TiDB ノードと TiKV ノードに分散された`/mnt/backup/2020/04/`ディレクトリから SST ファイルとして読み取られます。

上記の結果の最初の行は次のように説明されます。

| カラム              | 説明                                               |
| :--------------- | :----------------------------------------------- |
| `Destination`    | 読み取る先のURL                                        |
| `Size`           | バックアップアーカイブの合計サイズ（バイト単位）                         |
| `BackupTS`       | (未使用)                                            |
| `Queue Time`     | `RESTORE`番目のタスクがキューに入れられたときのタイムスタンプ (現在のタイムゾーン)。 |
| `Execution Time` | `RESTORE`のタスクの実行が開始されたときのタイムスタンプ (現在のタイム ゾーン)。   |

### 部分的な復元 {#partial-restore}

復元するデータベースまたはテーブルを指定できます。バックアップ アーカイブにデータベースまたはテーブルが欠落している場合、それらは無視され、 `RESTORE`もせずに完了します。

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

<CustomContent platform="tidb">

URL 構文については[外部ストレージサービスの URI 形式](/external-storage-uri.md)でさらに詳しく説明します。

</CustomContent>

<CustomContent platform="tidb-cloud">

URL 構文については[外部storageURI](https://docs.pingcap.com/tidb/stable/external-storage-uri)でさらに詳しく説明します。

</CustomContent>

資格情報を配布しないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定します。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`使用すると、TiKV ノードあたりの平均ダウンロード速度が制限され、ネットワーク帯域幅が削減されます。

復元が完了する前に、 `RESTORE`デフォルトでバックアップ ファイルのデータに対してチェックサムを実行し、正確性を検証します。 1 つのテーブルに対するチェックサム タスクのデフォルトの同時実行数は 4 ですが、 `CHECKSUM_CONCURRENCY`パラメータを使用して調整できます。 データ検証が不要であることが確実な場合は、 `CHECKSUM`パラメータを`FALSE`に設定してチェックを無効にすることができます。

統計がバックアップされている場合、復元時にデフォルトで復元されます。統計を復元する必要がない場合は、 `LOAD_STATS`パラメータを`FALSE`に設定できます。

<CustomContent platform="tidb">

システム[権限テーブル](/privilege-management.md#privilege-table)はデフォルトで復元されます。システム権限テーブルを復元する必要がない場合は、 `WITH_SYS_TABLE`パラメータを`FALSE`に設定できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

システム[権限テーブル](https://docs.pingcap.com/tidb/stable/privilege-management#privilege-table)はデフォルトで復元されます。システム権限テーブルを復元する必要がない場合は、 `WITH_SYS_TABLE`パラメータを`FALSE`に設定できます。

</CustomContent>

デフォルトでは、復元タスクは、 TiFlashレプリカが完全に作成されるまで待機せずに完了します。復元タスクを待機させる必要がある場合は、 `WAIT_TIFLASH_READY`パラメータを`TRUE`に設定できます。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### 増分復元 {#incremental-restore}

増分復元を実行するための特別な構文はありません。TiDB は、バックアップ アーカイブが完全か増分かを認識し、適切なアクションを実行します。各増分復元を正しい順序で適用するだけです。

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

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [バックアップ](/sql-statements/sql-statement-backup.md)
-   [復元を表示](/sql-statements/sql-statement-show-backups.md)
