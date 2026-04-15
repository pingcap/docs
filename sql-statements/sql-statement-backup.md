---
title: BACKUP | TiDB SQL Statement Reference
summary: TiDBデータベースにおけるBACKUPの使用方法の概要。
---

# バックアップ {#backup}

このステートメントは、TiDBクラスタの分散バックアップを実行するために使用されます。

> **警告：**
>
> -   この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。
> -   この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

`BACKUP`ステートメントは、 [BRツール](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)と同じエンジンを使用しますが、バックアップ処理は別のBRツールではなくBR自体によって実行されます。BR のすべての利点と警告は、このステートメントにも適用されます。

`BACKUP`を実行するには`BACKUP_ADMIN`または`SUPER`権限が必要です。さらに、バックアップを実行する TiDB ノードとクラスタ内のすべての TiKV ノードの両方が、宛先への読み取りまたは書き込み権限を持っている必要があります。 [Security強化モード](/system-variables.md#tidb_enable_enhanced_security)が有効になっている場合、ローカルstorage( `local://`で始まるstorageパス) は許可されません。

`BACKUP`ステートメントは、バックアップ タスク全体が完了、失敗、またはキャンセルされるまでブロックされます。 `BACKUP`を実行するには、長時間接続を準備する必要があります。タスクは、[`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md)ステートメントを使用してキャンセルできます。

`BACKUP`および[`RESTORE`](/sql-statements/sql-statement-restore.md)タスクは、一度に 1 つしか実行できません。 `BACKUP`または`RESTORE`ステートメントが同じ TiDBサーバーで既に実行されている場合、新しい`BACKUP`の実行は、以前のすべてのタスクが完了するまで待機します。

`BACKUP` 「tikv」storageエンジンでのみ使用できます。「unistore」エンジンで`BACKUP`を使用すると失敗します。

## あらすじ {#synopsis}

```ebnf+diagram
BackupStmt ::=
    "BACKUP" BRIETables "TO" stringLit BackupOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

BackupOption ::=
    "CHECKSUM" '='? Boolean
|   "CHECKSUM_CONCURRENCY" '='? LengthNum
|   "COMPRESSION_LEVEL" '='? LengthNum
|   "COMPRESSION_TYPE" '='? stringLit
|   "CONCURRENCY" '='? LengthNum
|   "IGNORE_STATS" '='? Boolean
|   "LAST_BACKUP" '='? BackupTSO
|   "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
|   "SNAPSHOT" '='? ( BackupTSO | LengthNum TimestampUnit "AGO" )

Boolean ::=
    NUM | "TRUE" | "FALSE"

BackupTSO ::=
    LengthNum | stringLit
```

## 例 {#examples}

### データベースのバックアップ {#back-up-databases}

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

上記の例では、 `test`データベースがローカルファイルシステムにバックアップされます。データは、すべての TiDB および TiKV ノードに分散された`/mnt/backup/2020/04/`ディレクトリに SST ファイルとして保存されます。

上記の結果の最初の行は、次のように説明されています。

| カラム              | 説明                                                              |
| :--------------- | :-------------------------------------------------------------- |
| `Destination`    | 宛先URL                                                           |
| `Size`           | バックアップアーカイブの合計サイズ（バイト単位）                                        |
| `BackupTS`       | バックアップ作成時のスナップショットの TSO ([増分バックアップ](#incremental-backup)に役立ちます) |
| `Queue Time`     | `BACKUP`タスクがキューに入れられたときのタイムスタンプ（現在のタイムゾーン）。                     |
| `Execution Time` | `BACKUP`タスクの実行が開始されたときのタイムスタンプ（現在のタイムゾーン）。                      |

### バックアップテーブル {#back-up-tables}

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

システムテーブル（ `mysql.*` 、 `INFORMATION_SCHEMA.*` 、 `PERFORMANCE_SCHEMA.*` 、…）はバックアップに含まれないことに注意してください。

### 外部ストレージ {#external-storages}

BRは、S3またはGCSへのデータバックアップをサポートしています。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

URL 構文については[外部ストレージサービスのURI形式](/external-storage-uri.md)で詳しく説明します。

認証情報を配布すべきでないクラウド環境で実行する場合は、 `SEND_CREDENTIALS_TO_TIKV`オプションを`FALSE`に設定してください。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### パフォーマンスの微調整 {#performance-fine-tuning}

`RATE_LIMIT`を使用して、TiKVノードあたりの平均アップロード速度を制限し、ネットワーク帯域幅を削減します。

バックアップが完了する前に、 `BACKUP`デフォルトでクラスタ上のデータに対してチェックサムを実行し、データの正当性を検証します。単一テーブルでのチェックサムタスクのデフォルトの同時実行数は 4 ですが、 `CHECKSUM_CONCURRENCY`パラメータを使用して調整できます。データの検証が不要であると確信している場合は、 `CHECKSUM`パラメータを`FALSE`に設定してチェックを無効にできます。

テーブルとインデックスのバックアップにおいて、 BRが同時に実行できるタスクの数を指定するには、 `CONCURRENCY`パラメーターを使用します。このパラメーターは、 BR内のスレッドプールサイズを制御し、バックアップ操作のパフォーマンスと効率を最適化します。

バックアップスキーマに応じて、1つのタスクは1つのテーブル範囲または1つのインデックス範囲を表します。1つのテーブルと1つのインデックスの場合、このテーブルをバックアップするために2つのタスクが使用されます。 `CONCURRENCY`のデフォルト値は`4`です。多数のテーブルまたはインデックスをバックアップする必要がある場合は、この値を増やしてください。

デフォルトでは統計はバックアップされません。統計情報をバックアップするには、 `IGNORE_STATS`パラメーターを`FALSE`に設定する必要があります。

デフォルトでは、バックアップによって生成される SST ファイルは`zstd`圧縮アルゴリズムを使用します。必要に応じて、 `COMPRESSION_TYPE`パラメータを使用して別の圧縮アルゴリズムを指定できます。サポートされているアルゴリズムには、 `lz4` 、 `zstd` 、および`snappy`あります。また`COMPRESSION_LEVEL`パラメータを使用して圧縮レベルを調整することもできます。レベル番号が大きいほど圧縮率は高くなりますが、CPU 消費量も高くなります。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### スナップショット {#snapshot}

履歴データをバックアップするために、タイムスタンプ、TSO、または相対時間を指定します。

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

相対時間でサポートされている単位は以下のとおりです。

-   マイクロ秒
-   2番
-   分
-   時間
-   日
-   週

SQL標準に従い、単位は常に単数形であることに注意してください。

### 増分バックアップ {#incremental-backup}

`LAST_BACKUP`オプションを指定すると、前回のバックアップから現在のスナップショットまでの変更点のみがバックアップされます。

```sql
-- timestamp (in current time zone)
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- timestamp oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [復元する](/sql-statements/sql-statement-restore.md)
-   [バックアップを表示](/sql-statements/sql-statement-show-backups.md)
