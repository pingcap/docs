---
title: Perform Log Backup and Restoration Using BR
summary: Learn how to perform log backup and restoration from the log backup data using the br log command line tool.
---

# BR を使用してログのバックアップと復元を実行する {#perform-log-backup-and-restoration-using-br}

`br log`コマンドを使用して、TiDB クラスターでログのバックアップと復元を実行できます。このドキュメントでは、 `br log`コマンドの使用法について説明します。

## 前提条件 {#prerequisites}

### BRをインストール {#install-br}

ログ バックアップを実行する前に、Backup &amp; Restore (BR) をインストールする必要があります。次のいずれかの方法で BR をインストールできます。

-   [TiUP を使用して BR をオンラインでインストールする](/migration-tools.md#install-tools-using-tiup) (推奨)
-   [TiDB バイナリ パッケージをダウンロードする](/download-ecosystem-tools.md)

### ログのバックアップを有効にする {#enable-log-backup}

ログ バックアップを使用する前に、TiKV 構成ファイルで[`log-backup.enable`](/tikv-configuration-file.md#enable-new-in-v620)を`true`に設定します。設定変更方法は[構成を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

## ログのバックアップを実行する {#perform-log-backup}

`br log`コマンドを使用して、ログのバックアップを実行できます。このコマンドには、次の操作に役立つ一連のサブコマンドがあります。

-   ログのバックアップを開始する
-   バックアップ ステータスのクエリ
-   バックアップを一時停止して再開する
-   バックアップ タスクを停止し、バックアップ データを削除します
-   バックアップ データのクリーンアップ
-   メタデータをビューする

このセクションでは、 `br log`のサブコマンドを紹介し、コマンドの使用例を示します。

### <code>br log</code>サブコマンド {#code-br-log-code-subcommands}

次のコマンドを実行すると、 `br log`コマンドのヘルプ情報を表示できます。

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

各サブコマンドの説明は次のとおりです。

-   `br log start` : ログ バックアップ タスクを開始します。
-   `br log status` : ログ バックアップ タスクのステータスを照会します。
-   `br log pause` : ログ バックアップ タスクを一時停止します。
-   `br log resume` : 一時停止したログ バックアップ タスクを再開します。
-   `br log stop` : ログ バックアップ タスクを停止し、タスク メタデータを削除します。
-   `br log truncate` : バックアップ ストレージからログ バックアップ データをクリーンアップします。
-   `br log metadata` : ログ バックアップ データのメタデータを照会します。

### バックアップ タスクを開始する {#start-a-backup-task}

`br log start`コマンドを実行して、ログ バックアップ タスクを開始できます。このタスクは、TiDB クラスターのバックグラウンドで実行され、KV ストレージの変更ログをバックアップ ストレージに自動的にバックアップします。

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

出力例は、共通のパラメーターのみを示しています。これらのパラメータは次のように説明されています。

-   `--task-name` : ログ バックアップのタスク名を指定します。この名前は、バックアップ タスクのクエリ、一時停止、および再開にも使用されます。
-   `--start-ts` : ログ バックアップの開始タイムスタンプを指定します。これが指定されていない場合、バックアップ プログラムは現在の時刻を`start-ts`として使用します。
-   `--pd` : バックアップ クラスタの PD アドレスを指定します。ログ バックアップ タスクを開始するには、BR が PD にアクセスする必要があります。
-   `--ca` 、 `--cert` 、 `--key` : TiKV および PD と通信するための mTLS 暗号化方式を指定します。
-   `--storage` : バックアップ ストレージ アドレスを指定します。現在、BR は共有ファイル システムと Amazon S3 のみをログ バックアップ用のストレージとしてサポートしています。詳細については、 [Amazon S3 ストレージ](/br/backup-storage-S3.md)を参照してください。

使用例:

```shell
./br log start --task-name=pitr --pd=172.16.102.95:2379 --storage='s3://tidb-pitr-bucket/backup-data/log-backup'
```

### バックアップ ステータスのクエリ {#query-the-backup-status}

`br log status`コマンドを実行して、バックアップ ステータスを照会できます。

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

出力例では、バックアップ タスクの名前を指定するために`task-name`が使用されています。デフォルト値は`*`で、これはすべてのタスクのステータスを照会することを意味します。

使用例:

```shell
./br log status --task-name=pitr --pd=172.16.102.95:2379
● Total 1 Tasks.
> #1 <
              name: pitr
            status: ● NORMAL
             start: 2022-07-14 20:08:03.268 +0800
               end: 2090-11-18 22:07:45.624 +0800
           storage: s3://tmp/store-by-storeid/log1
       speed(est.): 0.82 ops/s
checkpoint[global]: 2022-07-25 22:52:15.518 +0800; gap=2m52s
```

出力フィールドは次のとおりです。

-   `status` : バックアップ タスクのステータス。ステータスは`NORMAL` 、 `ERROR` 、または`PAUSE`です。
-   `start` : バックアップ タスクの開始時刻。これは、バックアップ タスクの開始時に指定された`start-ts`の値です。
-   `storage` : バックアップ ストレージ アドレス。
-   `speed` : バックアップ タスクの合計 QPS。 QPS は、1 秒あたりにバックアップされるログの数を意味します。
-   `checkpoint[global]` : このチェックポイントより前のすべてのデータがバックアップ ストレージにバックアップされます。これは、バックアップ データの復元に使用できる最新のタイムスタンプです。
-   `error[store]` : ストレージ ノードでログ バックアップ プログラムが検出したエラー。

### バックアップ タスクの一時停止と再開 {#pause-and-resume-the-backup-task}

`br log pause`コマンドを実行して、実行中のバックアップ タスクを一時停止できます。

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

> **ノート：**
>
> -   ログ バックアップ タスクが一時停止された後、変更ログを生成する MVCC データが削除されるのを防ぐために、バックアップ プログラムは現在のバックアップ チェックポイントをサービス セーフポイントとして自動的に設定し、MVCC データを最新の 24 時間以内に保持します。バックアップ タスクが 24 時間以上一時停止された場合、対応するデータはガベージ コレクションされ、バックアップされません。
> -   保持する MVCC データが多すぎると、TiDB クラスターのストレージ容量とパフォーマンスに悪影響を及ぼします。したがって、時間内にバックアップ タスクを再開することをお勧めします。

使用例:

```shell
./br log pause --task-name=pitr --pd=172.16.102.95:2379
```

`br log resume`コマンドを実行して、一時停止したバックアップ タスクを再開できます。

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

バックアップ タスクが 24 時間以上一時停止された後、 `br log resume`を実行するとエラーが報告され、BR はバックアップ データが失われたことを通知します。このエラーを処理するには、 [PITR ログ バックアップのトラブルシューティング](/br/pitr-troubleshoot.md#what-should-i-do-if-the-error-message-errbackupgcsafepointexceeded-is-returned-when-using-the-br-log-resume-command-to-resume-the-suspended-task)を参照してください。

使用例:

```shell
./br log resume --task-name=pitr --pd=172.16.102.95:2379
```

### バックアップ タスクを (完全に) 停止します。 {#stop-the-backup-task-permanently}

`br log stop`コマンドを実行して、ログ バックアップ タスクを完全に停止できます。このコマンドは、バックアップ クラスター内のタスク メタデータをクリーンアップします。

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

> **警告：**
>
> -   このコマンドは注意して使用してください。 PITR が必要なくなったことが確実な場合にのみ、ログ バックアップ タスクを停止します。ログ バックアップ タスクを一時停止する必要がある場合は、代わりに`br log pause`と`br log resume`を使用してください。
> -   `br log stop`を使用してログ バックアップ タスクを停止し、 `br log start`を使用してタスクを再開する場合は、元のパスとは異なるログ バックアップ ストレージ パスを指定する必要があります。ただし、ログ バックアップ パスが異なると、 `br restore point`を使用してデータを復元できない状況が発生します。

使用例:

```shell
./br log stop --task-name=pitr --pd=172.16.102.95:2379
```

### バックアップ データのクリーンアップ {#clean-up-the-backup-data}

`br log truncate`コマンドを実行して、古くなった、または不要になったログ バックアップ データをクリーンアップできます。

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

このコマンドは、バックアップ ストレージにのみアクセスし、TiDB クラスターにはアクセスしません。

一部のパラメータは次のように説明されています。

-   `--dry-run` : コマンドを実行しますが、実際にはファイルを削除しません。
-   `--until` : 指定されたタイムスタンプより前のすべてのログ バックアップ データを削除します。
-   `--storage` : バックアップ ストレージ アドレス。ログ バックアップ データは、共有ファイル システムまたは Amazon S3 にのみ保存できます。詳細については、 [Amazon S3 ストレージ](/br/backup-storage-S3.md)を参照してください。

使用例:

```shell
./br log truncate --until='2022-07-26 21:20:00+0800' –-storage='s3://tidb-pitr-bucket/backup-data/log-backup'
```

期待される出力:

```shell
Reading Metadata... DONE; take = 277.911599ms
We are going to remove 9 files, until 2022-07-26 21:20:00.0000.
Sure? (y/N) y
Clearing data files... DONE; take = 43.504161ms, kv-count = 53, kv-size = 4573(4.573kB)
Removing metadata... DONE; take = 24.038962ms
```

### バックアップ メタデータをビューする {#view-the-backup-metadata}

`br log metadata`コマンドを実行して、復元可能な最も古いタイムスタンプと最新のタイムスタンプなど、バックアップ ストレージ内のログ バックアップのメタデータを表示できます。

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

このコマンドは、バックアップ ストレージにのみアクセスし、TiDB クラスターにはアクセスしません。

`--storage`パラメータは、バックアップ ストレージ アドレスを指定するために使用されます。ログ バックアップ データは、共有ファイル システムまたは Amazon S3 にのみ保存できます。詳細は[Amazon S3 ストレージ](/br/backup-storage-S3.md)を参照してください。

使用例:

```shell
./br log metadata –-storage='s3://tidb-pitr-bucket/backup-data/log-backup'
```

期待される出力:

```shell
[2022/07/25 23:02:57.236 +08:00] [INFO] [collector.go:69] ["log metadata"] [log-min-ts=434582449885806593] [log-min-date="2022-07-14 20:08:03.268 +0800"] [log-max-ts=434834300106964993] [log-max-date="2022-07-25 23:00:15.618 +0800"]
```

## ログ バックアップ データを復元する {#restore-the-log-backup-data}

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

出力例は、共通のパラメーターのみを示しています。これらのパラメータは次のように説明されています。

-   `--full-backup-storage` : スナップショット (完全) バックアップのストレージ アドレス。 PITR を使用する必要がある場合は、このパラメーターを指定し、復元タイムスタンプより前の最新のスナップショット バックアップを選択する必要があります。ログ バックアップ データのみを復元する必要がある場合は、このパラメーターを省略できます。 Amazon S3 をストレージとして使用するには、 [Amazon S3 ストレージ](/br/backup-storage-S3.md)を参照してください。
-   `--restored-ts` : データを復元するタイムスタンプ。このパラメーターが指定されていない場合、BR はログ バックアップで使用可能な最新のタイムスタンプ、つまりバックアップ データのチェックポイントにデータを復元します。
-   `--start-ts` : ログ バックアップ データを復元する開始タイムスタンプ。ログ バックアップ データのみを復元する必要があり、スナップショット バックアップ データは必要ない場合は、このパラメーターを指定する必要があります。
-   `--pd` : 復元クラスタの PD アドレス。
-   `--ca` 、 `--cert` 、 `--key` : TiKV および PD と通信するための mTLS 暗号化方式を指定します。
-   `--storage` : ログ バックアップのストレージ アドレス。ログ バックアップ データは、共有ファイル システムまたは Amazon S3 にのみ保存できます。詳細については、 [Amazon S3 ストレージ](/br/backup-storage-S3.md)を参照してください。

使用例:

```shell
./br restore point --pd=172.16.102.95:2379
--storage='s3://tidb-pitr-bucket/backup-data/log-backup'
--full-backup-storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220512000000'
Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/07/19 18:15:39.132 +08:00] [INFO] [collector.go:69] ["Full Restore success summary"] [total-ranges=12] [ranges-succeed=12] [ranges-failed=0] [split-region=546.663µs] [restore-ranges=3] [total-take=3.112928252s] [restore-data-size(after-compressed)=5.056kB] [Size=5056] [BackupTS=434693927394607136] [total-kv=4] [total-kv-size=290B] [average-speed=93.16B/s]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/07/19 18:15:39.325 +08:00] [INFO] [collector.go:69] ["restore log success summary"] [total-take=192.955533ms] [restore-from=434693681289625602] [restore-to=434693753549881345] [total-kv-count=33] [total-size=21551]
```

> **ノート：**
>
> -   `br restore point`を使用して PITR を実行することをお勧めします ( [PITRの概要](/br/point-in-time-recovery.md)を参照)。ある期間のログ データをクラスターに直接復元することはお勧めしません。
> -   一定期間のログバックアップデータを繰り返し復元することはできません。範囲`[t1=10, t2=20)`のログ バックアップ データを繰り返し復元すると、復元されたデータが不整合になる可能性があります。
> -   複数のバッチで異なる期間のログ データを復元する場合は、ログ データが連続した順序で復元されるようにする必要があります。 [t1, t2)、[t2, t3)、および [t3, t4)] のログ バックアップ データを連続して復元すると、復元されたデータの一貫性が保たれます。ただし、[t1, t2) を復元し、[t2, t3) をスキップして [t3, t4)] を復元すると、復元されたデータが不整合になる可能性があります。
