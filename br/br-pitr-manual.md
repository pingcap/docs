---
title: TiDB Log Backup and PITR Command Manual
summary: TiDB ログ バックアップとポイントインタイム リカバリ (PITR) で使用されるコマンドを紹介します。
---

# TiDB ログ バックアップと PITR コマンド マニュアル {#tidb-log-backup-and-pitr-command-manual}

このドキュメントでは、TiDB ログ バックアップとポイントインタイム リカバリ (PITR) で使用されるコマンドについて説明します。

ログ バックアップと PITR の詳細については、以下を参照してください。

-   [ログバックアップとPITRガイド](/br/br-pitr-guide.md)
-   [バックアップと復元のユースケース](/br/backup-and-restore-use-cases.md)

## ログバックアップを実行する {#perform-log-backup}

`tiup br log`コマンドを使用してログ バックアップを開始および管理できます。

```shell
tiup br log --help

backup stream log from TiDB/TiKV cluster

Usage:
  br log [command]

Available Commands:
  metadata   get the metadata of log dir
  pause      pause a log backup task
  resume     resume a log backup task
  start      start a log backup task
  status     get status for the log backup task
  stop       stop a log backup task
  truncate   truncate the log data until sometime
```

各サブコマンドの説明は次のとおりです。

-   `tiup br log start` : ログ バックアップ タスクを開始します。
-   `tiup br log status` : ログ バックアップ タスクのステータスを照会します。
-   `tiup br log pause` : ログ バックアップ タスクを一時停止します。
-   `tiup br log resume` : 一時停止されたログ バックアップ タスクを再開します。
-   `tiup br log stop` : ログ バックアップ タスクを停止し、タスク メタデータを削除します。
-   `tiup br log truncate` : バックアップstorageからログバックアップデータをクリーンアップします。
-   `tiup br log metadata` : ログ バックアップ データのメタデータを照会します。

### バックアップタスクを開始する {#start-a-backup-task}

`tiup br log start`コマンドを実行して、ログ バックアップ タスクを開始できます。このタスクは TiDB クラスターのバックグラウンドで実行され、KVstorageの変更ログをバックアップstorageに自動的にバックアップします。

ヘルプ情報を表示するには、 `tiup br log start --help`実行します。

```shell
tiup br log start --help
start a log backup task

Usage:
  br log start [flags]

Flags:
  -h, --help               help for start
  --start-ts string        usually equals last full backupTS, used for backup log. Default value is current ts. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'.
  --task-name string       The task name for the backup log task.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
 -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"

```

出力例には共通パラメータのみが表示されます。これらのパラメータの説明は次のとおりです。

-   `--start-ts` : ログ バックアップの開始タイムスタンプを指定します。このパラメータが指定されていない場合、バックアップ プログラムは現在の時刻を`start-ts`として使用します。
-   `task-name` : ログ バックアップのタスク名を指定します。この名前は、バックアップ タスクのクエリ、一時停止、再開にも使用されます。
-   `--ca` : TiKVおよびPDと通信するためのmTLS暗号`--key`方式`--cert`指定します。
-   `--pd` : バックアップ クラスターの PD アドレスを指定します。BRは、ログ バックアップ タスクを開始するために PD にアクセスする必要があります。
-   `--storage` : バックアップstorageアドレスを指定します。現在、 BR はログ バックアップのstorageとして Amazon S3、Google Cloud Storage (GCS)、または Azure Blob Storage をサポートしています。上記のコマンドでは、例として Amazon S3 を使用しています。詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

使用例:

```shell
tiup br log start --task-name=pitr --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

### バックアップステータスを照会する {#query-the-backup-status}

`tiup br log status`コマンドを実行してバックアップ ステータスを照会できます。

ヘルプ情報を表示するには、 `tiup br log status --help`実行します。

```shell
tiup br log status --help
get status for the log backup task

Usage:
  br log status [flags]

Flags:
  -h, --help           help for status
  --json               Print JSON as the output.
  --task-name string   The task name for backup stream log. If default, get status of all of tasks (default "*")

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])

```

出力例では、 `task-name`使用してバックアップ タスクの名前を指定しています。デフォルト値は`*`で、すべてのタスクのステータスを照会することを意味します。

使用例:

```shell
tiup br log status --task-name=pitr --pd="${PD_IP}:2379"
```

期待される出力:

```shell
● Total 1 Tasks.
> #1 <
              name: pitr
            status: ● NORMAL
             start: 2022-07-14 20:08:03.268 +0800
               end: 2090-11-18 22:07:45.624 +0800
           storage: s3://backup-101/logbackup
       speed(est.): 0.82 ops/s
checkpoint[global]: 2022-07-25 22:52:15.518 +0800; gap=2m52s
```

出力フィールドの説明は次のとおりです。

-   `status` : バックアップ タスクのステータス`NORMAL` 、または`ERROR` `PAUSE`なります。
-   `start` : バックアップ タスクの開始時刻。バックアップ タスクの開始時に指定される`start-ts`です。
-   `storage` : バックアップstorageアドレス。
-   `speed` : バックアップ タスクの合計 QPS。QPS は 1 秒あたりにバックアップされるログの数を意味します。
-   `checkpoint [global]` : このチェックポイントより前のすべてのデータがバックアップstorageにバックアップされます。これは、バックアップ データを復元するために使用できる最新のタイムスタンプです。
-   `error [store]` : ログ バックアップ プログラムがstorageノード上で検出したエラー。

### バックアップタスクを一時停止して再開する {#pause-and-resume-a-backup-task}

実行中のバックアップ タスクを一時停止するには、 `tiup br log pause`コマンドを実行します。

ヘルプ情報を表示するには、 `tiup br log pause --help`実行します。

```shell
tiup br log pause --help
pause a log backup task

Usage:
  br log pause [flags]

Flags:
  --gc-ttl int         the TTL (in seconds) that PD holds for BR's GC safepoint (default 86400)
  -h, --help           help for status
  --task-name string   The task name for backup stream log.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
```

> **注記：**
>
> -   ログ バックアップ タスクが一時停止された後、変更ログを生成する MVCC データが削除されないように、バックアップ プログラムは現在のバックアップ チェックポイントをサービス セーフポイントとして自動的に設定し、最新の 24 時間以内の MVCC データを保持します。バックアップ タスクが 24 時間以上一時停止された場合、対応するデータはガベージ コレクションされ、バックアップされません。
> -   MVCC データを過剰に保持すると、TiDB クラスターのstorage容量とパフォーマンスに悪影響が及ぶ可能性があります。そのため、バックアップ タスクを適切なタイミングで再開することをお勧めします。

使用例:

```shell
tiup br log pause --task-name=pitr --pd="${PD_IP}:2379"
```

一時停止したバックアップ タスクを再開するには、 `tiup br log resume`コマンドを実行します。

ヘルプ情報を表示するには、 `tiup br log resume --help`実行します。

```shell
tiup br log resume --help
resume a log backup task

Usage:
  br log resume [flags]

Flags:
  -h, --help           help for status
  --task-name string   The task name for backup stream log.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
```

バックアップ タスクが 24 時間以上一時停止された後、 `tiup br log resume`実行するとエラーが報告され、 BR はバックアップ データが失われたことを通知します。このエラーを処理するには、 [バックアップと復元に関するよくある質問](/faq/backup-and-restore-faq.md#what-should-i-do-if-the-error-message-errbackupgcsafepointexceeded-is-returned-when-using-the-br-log-resume-command-to-resume-a-suspended-task)を参照してください。

使用例:

```shell
tiup br log resume --task-name=pitr --pd="${PD_IP}:2379"
```

### バックアップタスクを停止して再開する {#stop-and-restart-a-backup-task}

`tiup br log stop`コマンドを実行してログ バックアップ タスクを停止し、元の`--storage`ディレクトリを使用して停止したバックアップ タスクを再開できます。

#### バックアップタスクを停止する {#stop-a-backup-task}

ログ バックアップ タスクを停止するには、 `tiup br log stop`コマンドを実行します。このコマンドは、バックアップ クラスター内のタスク メタデータをクリーンアップします。

ヘルプ情報を表示するには、 `tiup br log stop --help`実行します。

```shell
tiup br log stop --help
stop a log backup task

Usage:
  br log stop [flags]

Flags:
  -h, --help           help for status
  --task-name string   The task name for the backup log task.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
```

> **注記：**
>
> このコマンドは注意して使用してください。ログ バックアップ タスクを一時停止する必要がある場合は、代わりに`tiup br log pause`と`tiup br log resume`使用してください。

使用例:

```shell
tiup br log stop --task-name=pitr --pd="${PD_IP}:2379"
```

#### バックアップタスクを再開する {#restart-a-backup-task}

`tiup br log stop`コマンドを実行してログ バックアップ タスクを停止した後、別の`--storage`ディレクトリに新しいログ バックアップ タスクを作成するか、 `tiup br log start`コマンドを実行して元の`--storage`ディレクトリでログ バックアップ タスクを再開することができます。元の`--storage`ディレクトリでタスクを再開する場合は、次の点に注意してください。

-   タスクを再開するための`--storage`のディレクトリのパラメータは、停止されたタスクと同じである必要があります。
-   `--start-ts`指定する必要はありません。BRは最後のバックアップ チェックポイントから自動的にバックアップを開始します。
-   タスクが長時間停止し、データの複数のバージョンがガベージ コレクションされた場合、タスクを再開しようとするとエラー`BR:Backup:ErrBackupGCSafepointExceeded`が報告されます。この場合、別の`--storage`ディレクトリに新しいログ バックアップ タスクを作成する必要があります。

### バックアップデータをクリーンアップする {#clean-up-backup-data}

`tiup br log truncate`コマンドを実行して、古くなった、または不要になったログ バックアップ データをクリーンアップできます。

ヘルプ情報を表示するには、 `tiup br log truncate --help`実行します。

```shell
tiup br log truncate --help
truncate the incremental log until sometime.

Usage:
  br log truncate [flags]

Flags:
  --dry-run        Run the command but don't really delete the files.
  -h, --help       help for truncate
  --until string   Remove all backup data until this TS.(support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'.)
  -y, --yes        Skip all prompts and always execute the command.


Global Flags:
  -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

このコマンドはバックアップstorageにのみアクセスし、TiDB クラスターにはアクセスしません。一部のパラメータは次のように記述されます。

-   `--dry-run` : コマンドを実行しますが、実際にはファイルを削除しません。
-   `--until` : 指定されたタイムスタンプより前のすべてのログ バックアップ データを削除します。
-   `--storage` : バックアップstorageアドレス。現在、 BR はログバックアップのstorageとして Amazon S3、GCS、または Azure Blob Storage をサポートしています。詳細については[外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

使用例:

```shell
tiup br log truncate --until='2022-07-26 21:20:00+0800' \
–-storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

期待される出力:

```shell
Reading Metadata... DONE; take = 277.911599ms
We are going to remove 9 files, until 2022-07-26 21:20:00.0000.
Sure? (y/N) y
Clearing data files... DONE; take = 43.504161ms, kv-count = 53, kv-size = 4573(4.573kB)
Removing metadata... DONE; take = 24.038962ms
```

### バックアップメタデータをビュー {#view-the-backup-metadata}

`tiup br log metadata`コマンドを実行すると、復元できる最も古いタイムスタンプや最新のタイムスタンプなど、storageシステム内のバックアップ メタデータを表示できます。

ヘルプ情報を表示するには、 `tiup br log metadata --help`実行します。

```shell
tiup br log metadata --help
get the metadata of log backup storage

Usage:
  br log metadata [flags]

Flags:
  -h, --help       help for metadata

Global Flags:
  -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

このコマンドはバックアップstorageにのみアクセスし、TiDB クラスターにはアクセスしません。

`--storage`パラメータは、バックアップstorageのアドレスを指定するために使用されます。現在、 BR はログバックアップのstorageとして Amazon S3、GCS、または Azure Blob Storage をサポートしています。詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

使用例:

```shell
tiup br log metadata –-storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

期待される出力:

```shell
[2022/07/25 23:02:57.236 +08:00] [INFO] [collector.go:69] ["log metadata"] [log-min-ts=434582449885806593] [log-min-date="2022-07-14 20:08:03.268 +0800"] [log-max-ts=434834300106964993] [log-max-date="2022-07-25 23:00:15.618 +0800"]
```

## 指定した時点への復元 (PITR) {#restore-to-a-specified-point-in-time-pitr}

`tiup br restore point`コマンドを実行して、新しいクラスターで PITR を実行するか、ログ バックアップ データを復元することができます。

ヘルプ情報を表示するには、 `tiup br restore point --help`実行します。

```shell
tiup br restore point --help
restore data from log until specify commit timestamp

Usage:
  br restore point [flags]

Flags:
  --full-backup-storage string specify the backup full storage. fill it if want restore full backup before restore log.
  -h, --help                   help for point
  --restored-ts string         the point of restore, used for log restore. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'
  --start-ts string            the start timestamp which log restore from. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'


Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
 -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

出力例には共通パラメータのみが表示されます。これらのパラメータの説明は次のとおりです。

-   `--full-backup-storage` : スナップショット (フル) バックアップのstorageアドレス。PITR を使用するには、このパラメータを指定して、復元タイムスタンプより前の最新のスナップショット バックアップを選択します。ログ バックアップ データのみを復元する場合は、このパラメータを省略できます。リカバリ クラスターを初めて初期化するときは、スナップショット バックアップを指定する必要があることに注意してください。現在、 BR はログ バックアップのstorageとして Amazon S3、GCS、および Azure Blob Storage をサポートしています。詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。
-   `--restored-ts` : データを復元するタイムスタンプ。このパラメータを指定しない場合、 BR はログ バックアップで使用可能な最新のタイムスタンプ、つまりバックアップ データのチェックポイントにデータを復元します。
-   `--start-ts` : ログ バックアップ データを復元する開始タイムスタンプ。ログ バックアップ データのみを復元する必要がある場合は、このパラメーターを指定する必要があります。
-   `--pd` : 復元クラスターの PD アドレス。
-   `--ca` : TiKVおよびPDと通信するためのmTLS暗号`--key`方式`--cert`指定します。
-   `--storage` : ログバックアップのstorageアドレス。現在、 BR はログバックアップのstorageとして Amazon S3、GCS、または Azure Blob Storage をサポートしています。詳細については[外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

使用例:

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${access-key}&secret-access-key=${secret-access-key}"'

Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ***["Full Restore success summary"] ****** [total-take=3.112928252s] [restore-data-size(after-compressed)=5.056kB] [Size=5056] [BackupTS=434693927394607136] [total-kv=4] [total-kv-size=290B] [average-speed=93.16B/s]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
"restore log success summary"] [total-take=192.955533ms] [restore-from=434693681289625602] [restore-to=434693753549881345] [total-kv-count=33] [total-size=21551]
```

> **注記：**
>
> -   クラスターを初めて復元するときは、完全なスナップショット データを指定する必要があります。そうしないと、テーブル ID ルールの書き換えにより、新しく作成されたテーブルの一部のデータが不正確になる可能性があります。
> -   特定の期間のログバックアップデータを繰り返して復元することはできません。範囲`[t1=10, t2=20)`のログバックアップデータを繰り返して復元すると、復元されたデータに不整合が生じる可能性があります。
> -   異なる期間のログ データを複数のバッチで復元する場合は、ログ データが連続した順序で復元されるようにしてください。 `[t1, t2)` 、 `[t2, t3)` 、 `[t3, t4)`のログ バックアップ データを連続した順序で復元すると、復元されたデータは一貫性を保ちます。 ただし、 `[t1, t2)`復元してから`[t2, t3)`スキップして`[t3, t4)`復元すると、復元されたデータは一貫性を失っている可能性があります。
