---
title: TiDB Log Backup and PITR Command Manual
summary: Learn about the commands of TiDB log backup and point-in-time recovery.
---

# TiDB ログ バックアップと PITR コマンド マニュアル {#tidb-log-backup-and-pitr-command-manual}

このドキュメントでは、TiDB ログ バックアップおよびポイントインタイム リカバリ (PITR) で使用されるコマンドについて説明します。

ログ バックアップと PITR の詳細については、以下を参照してください。

-   [ログのバックアップと PITR ガイド](/br/br-pitr-guide.md)
-   [バックアップと復元の使用例](/br/backup-and-restore-use-cases.md)

## ログのバックアップを実行する {#perform-log-backup}

`br log`コマンドを使用してログ バックアップを開始および管理できます。

```shell
./br log --help

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

各サブコマンドは次のように説明されます。

-   `br log start` : ログ バックアップ タスクを開始します。
-   `br log status` : ログ バックアップ タスクのステータスをクエリします。
-   `br log pause` : ログ バックアップ タスクを一時停止します。
-   `br log resume` : 一時停止したログ バックアップ タスクを再開します。
-   `br log stop` : ログ バックアップ タスクを停止し、タスクのメタデータを削除します。
-   `br log truncate` : バックアップstorageからログ バックアップ データをクリーンアップします。
-   `br log metadata` : ログ バックアップ データのメタデータをクエリします。

### バックアップタスクを開始する {#start-a-backup-task}

`br log start`コマンドを実行してログ バックアップ タスクを開始できます。このタスクは TiDB クラスターのバックグラウンドで実行され、KVstorageの変更ログをバックアップstorageに自動的にバックアップします。

`br log start --help`を実行してヘルプ情報を表示します。

```shell
./br log start --help
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

出力例には、共通パラメータのみが示されています。これらのパラメータは次のように説明されます。

-   `--start-ts` : ログ バックアップの開始タイムスタンプを指定します。このパラメータが指定されていない場合、バックアップ プログラムは現在時刻を`start-ts`として使用します。
-   `task-name` : ログバックアップのタスク名を指定します。この名前は、バックアップ タスクのクエリ、一時停止、再開にも使用されます。
-   `--ca` 、 `--cert` 、 `--key` : TiKV および PD と通信するための mTLS 暗号化方式を指定します。
-   `--pd` : バックアップ クラスターの PD アドレスを指定します。ログ バックアップ タスクを開始するには、 BR がPD にアクセスする必要があります。
-   `--storage` : バックアップstorageアドレスを指定します。現在、 BR はログ バックアップ用のstorageとして Amazon S3、Google Cloud Storage (GCS)、または Azure Blob Storage をサポートしています。前述のコマンドでは、例として Amazon S3 を使用しています。詳細は[外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。

使用例：

```shell
./br log start --task-name=pitr --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

### バックアップステータスを問い合わせる {#query-the-backup-status}

`br log status`コマンドを実行してバックアップ ステータスをクエリできます。

`br log status --help`を実行してヘルプ情報を表示します。

```shell
./br log status --help
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

出力例では、バックアップ タスクの名前を指定するために`task-name`が使用されています。デフォルト値は`*`で、すべてのタスクのステータスをクエリすることを意味します。

使用例：

```shell
./br log status --task-name=pitr --pd="${PD_IP}:2379"
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

出力フィールドは次のように説明されます。

-   `status` : バックアップ タスクのステータス。 `NORMAL` 、 `ERROR` 、または`PAUSE`のいずれかです。
-   `start` : バックアップタスクの開始時刻。これは、バックアップ タスクの開始時に指定された`start-ts`値です。
-   `storage` : バックアップstorageアドレス。
-   `speed` : バックアップ タスクの合計 QPS。 QPS は、1 秒あたりにバックアップされるログの数を意味します。
-   `checkpoint [global]` : このチェックポイントより前のすべてのデータがバックアップstorageにバックアップされます。これは、バックアップ データの復元に使用できる最新のタイムスタンプです。
-   `error [store]` : ログ バックアップ プログラムがstorageノードで発生したエラー。

### バックアップタスクの一時停止と再開 {#pause-and-resume-a-backup-task}

`br log pause`コマンドを実行すると、実行中のバックアップ タスクを一時停止できます。

`br log pause --help`を実行してヘルプ情報を表示します。

```shell
./br log pause --help
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
> -   ログ バックアップ タスクが一時停止された後、変更ログを生成する MVCC データが削除されないように、バックアップ プログラムは現在のバックアップ チェックポイントをサービス セーフポイントとして自動的に設定します。これには、最新 24 時間以内の MVCC データが保持されます。バックアップ タスクが 24 時間以上一時停止された場合、対応するデータはガベージ コレクションされ、バックアップされません。
> -   MVCC データを保持しすぎると、TiDB クラスターのstorage容量とパフォーマンスに悪影響が生じます。したがって、時間内にバックアップ タスクを再開することをお勧めします。

使用例：

```shell
./br log pause --task-name=pitr --pd="${PD_IP}:2379"
```

`br log resume`コマンドを実行すると、一時停止したバックアップ タスクを再開できます。

`br log resume --help`を実行してヘルプ情報を表示します。

```shell
./br log resume --help
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

バックアップ タスクが 24 時間以上一時停止された後、 `br log resume`実行するとエラーが報告され、 BR はバックアップ データが失われたことを示すプロンプトを表示します。このエラーに対処するには、 [バックアップと復元に関するよくある質問](/faq/backup-and-restore-faq.md#what-should-i-do-if-the-error-message-errbackupgcsafepointexceeded-is-returned-when-using-the-br-log-resume-command-to-resume-a-suspended-task)を参照してください。

使用例：

```shell
./br log resume --task-name=pitr --pd="${PD_IP}:2379"
```

### バックアップタスクを停止して再開する {#stop-and-restart-a-backup-task}

`br log stop`コマンドを実行してログ バックアップ タスクを停止し、元の`--storage`ディレクトリを使用して停止したバックアップ タスクを再開できます。

#### バックアップタスクを停止する {#stop-a-backup-task}

`br log stop`コマンドを実行すると、ログ バックアップ タスクを停止できます。このコマンドは、バックアップ クラスター内のタスク メタデータをクリーンアップします。

`br log stop --help`を実行してヘルプ情報を表示します。

```shell
./br log stop --help
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
> このコマンドは注意して使用してください。ログ バックアップ タスクを一時停止する必要がある場合は、代わりに`br log pause`と`br log resume`を使用してください。

使用例：

```shell
./br log stop --task-name=pitr --pd="${PD_IP}:2379"
```

#### バックアップタスクを再開する {#restart-a-backup-task}

`br log stop`コマンドを実行してログ バックアップ タスクを停止した後、別の`--storage`ディレクトリに新しいログ バックアップ タスクを作成するか、 `br log start`コマンドを実行して元の`--storage`ディレクトリでログ バックアップ タスクを再開できます。元の`--storage`ディレクトリでタスクを再開する場合は、次の点に注意してください。

-   タスクを再開するための`--storage`ディレクトリのパラメータは、停止したタスクと同じである必要があります。
-   `--start-ts`指定する必要はありません。 BR は、最後のバックアップ チェックポイントからバックアップを自動的に開始します。
-   タスクが長期間停止され、複数のバージョンのデータがガベージ コレクションされた場合、タスクを再開しようとするとエラー`BR:Backup:ErrBackupGCSafepointExceeded`が報告されます。この場合、別`--storage`ディレクトリに新しいログ バックアップ タスクを作成する必要があります。

### バックアップデータをクリーンアップする {#clean-up-backup-data}

`br log truncate`コマンドを実行して、古いログ バックアップ データまたは不要になったログ バックアップ データをクリーンアップできます。

`br log truncate --help`を実行してヘルプ情報を表示します。

```shell
./br log truncate --help
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

このコマンドはバックアップstorageにのみアクセスし、TiDB クラスターにはアクセスしません。一部のパラメータは次のように説明されます。

-   `--dry-run` : コマンドを実行しますが、実際にはファイルを削除しません。
-   `--until` : 指定されたタイムスタンプより前のすべてのログ バックアップ データを削除します。
-   `--storage` : バックアップstorageアドレス。現在、 BR はログ バックアップ用のstorageとして Amazon S3、GCS、または Azure Blob Storage をサポートしています。詳細は[外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。

使用例：

```shell
./br log truncate --until='2022-07-26 21:20:00+0800' \
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

### バックアップのメタデータをビュー {#view-the-backup-metadata}

`br log metadata`コマンドを実行すると、復元可能な最も古いタイムスタンプと最新のタイムスタンプなど、storageシステム内のバックアップ メタデータを表示できます。

`br log metadata --help`を実行してヘルプ情報を表示します。

```shell
./br log metadata --help
get the metadata of log backup storage

Usage:
  br log metadata [flags]

Flags:
  -h, --help       help for metadata

Global Flags:
  -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

このコマンドはバックアップstorageにのみアクセスし、TiDB クラスターにはアクセスしません。

`--storage`パラメータは、バックアップstorageアドレスを指定するために使用されます。現在、 BR はログ バックアップ用のstorageとして Amazon S3、GCS、または Azure Blob Storage をサポートしています。詳細は[外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。

使用例：

```shell
./br log metadata –-storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}"'
```

期待される出力:

```shell
[2022/07/25 23:02:57.236 +08:00] [INFO] [collector.go:69] ["log metadata"] [log-min-ts=434582449885806593] [log-min-date="2022-07-14 20:08:03.268 +0800"] [log-max-ts=434834300106964993] [log-max-date="2022-07-25 23:00:15.618 +0800"]
```

## 指定した時点への復元 (PITR) {#restore-to-a-specified-point-in-time-pitr}

`br restore point`コマンドを実行して、新しいクラスターで PITR を実行するか、ログ バックアップ データを復元するだけです。

`br restore point --help`を実行してヘルプ情報を表示します。

```shell
./br restore point --help
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

出力例には、共通パラメータのみが示されています。これらのパラメータは次のように説明されます。

-   `--full-backup-storage` : スナップショット (フル) バックアップのstorageアドレス。 PITR を使用するには、このパラメータを指定し、復元タイムスタンプより前の最新のスナップショット バックアップを選択します。ログバックアップデータのみをリストアする場合は、このパラメータを省略できます。現在、 BR はログ バックアップ用のstorageとして Amazon S3、GCS、または Azure Blob Storage をサポートしています。詳細は[外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。
-   `--restored-ts` : データを復元するタイムスタンプ。このパラメータが指定されていない場合、 BR はログ バックアップで使用可能な最新のタイムスタンプ、つまりバックアップ データのチェックポイントにデータを復元します。
-   `--start-ts` : ログ バックアップ データを復元する開始タイムスタンプ。ログ バックアップ データのみを復元する必要がある場合は、このパラメータを指定する必要があります。
-   `--pd` : 復元クラスターの PD アドレス。
-   `--ca` 、 `--cert` 、 `--key` : TiKV および PD と通信するための mTLS 暗号化方式を指定します。
-   `--storage` : ログバックアップのstorageアドレス。現在、 BR はログ バックアップ用のstorageとして Amazon S3、GCS、または Azure Blob Storage をサポートしています。詳細は[外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。

使用例：

```shell
./br restore point --pd="${PD_IP}:2379"
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
> -   一定期間のログバックアップデータを繰り返し復元することはできません。範囲`[t1=10, t2=20)`のログバックアップデータを繰り返しリストアすると、リストアされたデータに不整合が生じる可能性があります。
> -   異なる期間のログ データを複数のバッチでリストアする場合は、ログ データが連続した順序でリストアされるようにしてください。 `[t1, t2)` 、 `[t2, t3)` 、 `[t3, t4)`のログ バックアップ データを連続した順序でリストアすると、リストアされたデータの整合性が保たれます。ただし、 `[t1, t2)`復元し、その後`[t2, t3)`スキップして`[t3, t4)`を復元すると、復元されたデータに不整合が生じる可能性があります。
