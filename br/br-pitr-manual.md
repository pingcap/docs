---
title: TiDB Log Backup and PITR Command Manual
summary: TiDB ログ バックアップとポイントインタイム リカバリ (PITR) で使用されるコマンドを紹介します。
---

# TiDB ログバックアップおよび PITR コマンドマニュアル {#tidb-log-backup-and-pitr-command-manual}

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
-   `tiup br log truncate` : バックアップstorageからログ バックアップ データをクリーンアップします。
-   `tiup br log metadata` : ログ バックアップ データのメタデータを照会します。

### ログバックアップタスクを開始する {#start-a-log-backup-task}

`tiup br log start`コマンドを実行すると、ログバックアップタスクを開始できます。このタスクはTiDBクラスターのバックグラウンドで実行され、KVstorageの変更ログをバックアップstorageに自動的にバックアップします。

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

出力例には共通パラメータのみが表示されています。これらのパラメータの説明は以下のとおりです。

-   `--start-ts` : ログバックアップの開始タイムスタンプを指定します。このパラメータが指定されていない場合、バックアッププログラムは現在の時刻を`start-ts`として使用します。
-   `task-name` : ログバックアップのタスク名を指定します。この名前は、バックアップタスクのクエリ、一時停止、再開にも使用されます。
-   `--ca` : TiKVおよびPDと通信するためのmTLS暗号化`--key` `--cert`指定します。
-   `--pd` : バックアップ クラスターの PD アドレスを指定します。BRはログ バックアップ タスクを開始するために PD にアクセスする必要があります。
-   `--storage` : バックアップstorageのアドレスを指定します。現在、 BRはログバックアップのstorageとしてAmazon S3、Google Cloud Storage（GCS）、またはAzure Blob Storageをサポートしています。上記のコマンドではAmazon S3を例として使用しています。詳細は[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

使用例:

```shell
tiup br log start \
  --task-name=pitr \
  --pd="${PD_IP}:2379" \
  --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

### ログバックアップデータを暗号化する {#encrypt-the-log-backup-data}

BR を使用すると、ログ バックアップ データをバックアップstorageにアップロードする前に暗号化できます。

TiDB v8.4.0 以降では、ログ バックアップ コマンドで次のパラメータ ( [スナップショットバックアップの暗号化](/br/br-snapshot-manual.md#encrypt-the-backup-data)に類似) を渡すことで、ログ バックアップ データを暗号化できます。

-   `--log.crypter.method` : 暗号化アルゴリズム。2、4、6 `aes192-ctr` `aes128-ctr`か`aes256-ctr`なります。デフォルト値は`plaintext`で、データは暗号化されません。
-   `--log.crypter.key` : 16進文字列形式の暗号化キー。アルゴリズム`aes128-ctr`の場合は128ビット（16バイト）、アルゴリズム`aes192-ctr`の場合は24バイト、アルゴリズム`aes256-ctr`の場合は32バイトのキーとなります。
-   `--log.crypter.key-file` : キーファイル。2 `crypter.key`渡さずに、キーが保存されているファイルパスをパラメータとして直接渡すこともできます。

次に例を示します。

```shell
tiup br log start \
    --task-name=pitr-with-encryption
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --log.crypter.method aes128-ctr \
    --log.crypter.key 0123456789abcdef0123456789abcdef
```

ただし、セキュリティ要件が高いシナリオでは、固定の暗号化キーをコマンドラインで直接渡すことを望まない場合があります。セキュリティをさらに強化するには、マスターキーベースの暗号化システムを使用して暗号化キーを管理できます。このシステムは、ログバックアップファイルごとに異なるデータキーを生成し、マスターキーのローテーションをサポートします。以下のパラメータを使用して設定できます。

-   `--master-key-crypter-method` : マスターキーに基づく暗号化アルゴリズム`aes128-ctr` 、または`aes256-ctr` `aes192-ctr`かになります。デフォルト値は`plaintext`で、データは暗号化されません。
-   `--master-key` ：マスターキーの設定。ローカルディスクに保存されたマスターキー、またはクラウドキー管理サービス（KMS）によって管理されたマスターキーを使用できます。

ローカル ディスクに保存されているマスター キーを使用して暗号化します。

```shell
tiup br log start \
    --task-name=pitr-with-encryption \
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --master-key-crypter-method aes128-ctr \
    --master-key "local:///path/to/master.key"
```

AWS KMS によって管理されるマスターキーを使用して暗号化します。

```shell
tiup br log start \
    --task-name=pitr-with-encryption \
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --master-key-crypter-method aes128-ctr \
    --master-key "aws-kms:///${AWS_KMS_KEY_ID}?AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY}&AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}&REGION=${AWS_REGION}"
```

Google Cloud KMS によって管理されるマスターキーを使用して暗号化します。

```shell
tiup br log start \
    --task-name=pitr-with-encryption \
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --master-key-crypter-method aes128-ctr \
    --master-key "gcp-kms:///projects/$GCP_PROJECT_ID/locations/$GCP_LOCATION/keyRings/$GCP_KEY_RING/cryptoKeys/$GCP_KEY_NAME?AUTH=specified&CREDENTIALS=$GCP_CREDENTIALS_PATH"
```

> **注記：**
>
> -   キーが失われると、ログ バックアップ データをクラスターに復元できなくなります。
> -   暗号化機能は、 `br`および TiDB クラスター v8.4.0 以降で使用する必要があります。暗号化されたログバックアップデータは、v8.4.0 より前のバージョンのクラスターでは復元できません。

### ログバックアップのステータスを照会する {#query-the-log-backup-status}

`tiup br log status`コマンドを実行して、ログ バックアップの状態を照会できます。

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

出力例では、 `task-name`バックアップタスクの名前を指定するために使用されています。デフォルト値は`*`で、これはすべてのタスクのステータスを照会することを意味します。

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

-   `status` : バックアップ タスクのステータス`NORMAL` 、または`PAUSE` `ERROR`なります。
-   `start` : バックアップタスクの開始時刻。これは、バックアップタスクの開始時に指定された`start-ts`です。
-   `storage` : バックアップstorageアドレス。
-   `speed` : バックアップタスクの合計 QPS。QPS は 1 秒あたりにバックアップされるログの数を意味します。
-   `checkpoint [global]` : このチェックポイントより前のすべてのデータがバックアップstorageにバックアップされています。これは、バックアップデータの復元に使用できる最新のタイムスタンプです。
-   `error [store]` : ログ バックアップ プログラムがstorageノード上で検出したエラー。

### ログバックアップタスクを一時停止して再開する {#pause-and-resume-a-log-backup-task}

実行中のログ バックアップ タスクを一時停止するには、 `tiup br log pause`コマンドを実行します。

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
> -   ログバックアップタスクが一時停止された後、変更ログを生成するMVCCデータが削除されるのを防ぐため、バックアッププログラムは現在のバックアップチェックポイントをサービスセーフポイントとして自動的に設定します。このサービスセーフポイントには、過去24時間以内のMVCCデータが保持されます。バックアップタスクが24時間以上一時停止された場合、対応するデータはガベージコレクションされ、バックアップされません。
> -   MVCCデータを過剰に保持すると、TiDBクラスターのstorage容量とパフォーマンスに悪影響を及ぼします。そのため、バックアップタスクを適切なタイミングで再開することをお勧めします。

使用例:

```shell
tiup br log pause --task-name=pitr --pd="${PD_IP}:2379"
```

一時停止されたバックアップ タスクを再開するには、 `tiup br log resume`コマンドを実行します。

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

バックアップタスクが24時間以上一時停止された後、 `tiup br log resume`実行するとエラーが発生し、 BRはバックアップデータが失われたというメッセージを表示します。このエラーに対処するには、 [バックアップと復元に関するよくある質問](/faq/backup-and-restore-faq.md#what-should-i-do-if-the-error-message-errbackupgcsafepointexceeded-is-returned-when-using-the-br-log-resume-command-to-resume-a-suspended-task)を参照してください。

使用例:

```shell
tiup br log resume --task-name=pitr --pd="${PD_IP}:2379"
```

### ログバックアップタスクを停止して再開する {#stop-and-restart-a-log-backup-task}

`tiup br log stop`コマンドを実行してログ バックアップ タスクを停止し、元の`--storage`ディレクトリを使用して停止したログ バックアップ タスクを再開できます。

### ログバックアップタスクを停止する {#stop-a-log-backup-task}

ログバックアップタスクを停止するには、コマンド`tiup br log stop`実行します。このコマンドは、バックアップクラスター内のタスクメタデータをクリーンアップします。

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
> このコマンドは注意して使用してください。ログバックアップタスクを一時停止する必要がある場合は、代わりに`tiup br log pause`と`tiup br log resume`使用してください。

使用例:

```shell
tiup br log stop --task-name=pitr --pd="${PD_IP}:2379"
```

#### ログバックアップタスクを再開する {#restart-a-log-backup-task}

`tiup br log stop`コマンドを実行してログバックアップタスクを停止した後、別の`--storage`ディレクトリに新しいログバックアップタスクを作成するか、 `tiup br log start`コマンドを実行して元の`--storage`ディレクトリでログバックアップタスクを再開できます。元の`--storage`ディレクトリでタスクを再開する場合は、以下の点に注意してください。

-   タスクを再開するための`--storage`ディレクトリのパラメータは、停止されたタスクと同じである必要があります。
-   `--start-ts`指定する必要はありません。BRは最後のバックアップ チェックポイントから自動的にバックアップを開始します。
-   タスクが長時間停止し、複数のバージョンのデータがガベージコレクションされている場合、タスクを再開しようとするとエラー`BR:Backup:ErrBackupGCSafepointExceeded`が報告されます。この場合、別のディレクトリ`--storage`に新しいログバックアップタスクを作成する必要があります。

### ログバックアップデータをクリーンアップする {#clean-up-log-backup-data}

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

このコマンドはバックアップstorageにのみアクセスし、TiDBクラスターにはアクセスしません。パラメータの説明は以下のとおりです。

-   `--dry-run` : コマンドを実行しますが、実際にはファイルを削除しません。
-   `--until` : 指定されたタイムスタンプより前のすべてのログ バックアップ データを削除します。
-   `--storage` : バックアップstorageのアドレス。現在、 BRはログバックアップのstorageとしてAmazon S3、GCS、またはAzure Blob Storageをサポートしています。詳細は[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

使用例:

```shell
tiup br log truncate --until='2022-07-26 21:20:00+0800' \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

期待される出力:

```shell
Reading Metadata... DONE; take = 277.911599ms
We are going to remove 9 files, until 2022-07-26 21:20:00.0000.
Sure? (y/N) y
Clearing data files... DONE; take = 43.504161ms, kv-count = 53, kv-size = 4573(4.573kB)
Removing metadata... DONE; take = 24.038962ms
```

### ログバックアップのメタデータをビュー {#view-the-log-backup-metadata}

`tiup br log metadata`コマンドを実行すると、復元できる最も古いタイムスタンプや最新のタイムスタンプなど、storageシステム内のログ バックアップ メタデータを表示できます。

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

`--storage`パラメータはバックアップstorageのアドレスを指定するために使用されます。現在、 BR はログバックアップのstorageとして Amazon S3、GCS、または Azure Blob Storage をサポートしています。詳細については[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

使用例:

```shell
tiup br log metadata --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

期待される出力:

```shell
[2022/07/25 23:02:57.236 +08:00] [INFO] [collector.go:69] ["log metadata"] [log-min-ts=434582449885806593] [log-min-date="2022-07-14 20:08:03.268 +0800"] [log-max-ts=434834300106964993] [log-max-date="2022-07-25 23:00:15.618 +0800"]
```

## 指定した時点への復元 (PITR) {#restore-to-a-specified-point-in-time-pitr}

> **注記：**
>
> `restore point`の増分バックアップ アドレスとして`--full-backup-storage`指定した場合、このバックアップと以前の増分バックアップを復元するには、増分バックアップと後続のログ バックアップとの互換性を確保するために、パラメータ`--allow-pitr-from-incremental`を`true`に設定する必要があります。

`tiup br restore point`コマンドを実行して、新しいクラスターで PITR を実行したり、ログ バックアップ データを復元したりできます。

ヘルプ情報を表示するには、 `tiup br restore point --help`実行します。

```shell
tiup br restore point --help
restore data from log until specify commit timestamp

Usage:
  br restore point [flags]

Flags:
  --full-backup-storage string specify the backup full storage. fill it if want restore full backup before restore log.
  -h, --help                   help for point
  --pitr-batch-count uint32    specify the batch count to restore log. (default 8)
  --pitr-batch-size uint32     specify the batch size to restore log. (default 16777216)
  --pitr-concurrency uint32    specify the concurrency to restore log. (default 16)
  --restored-ts string         the point of restore, used for log restore. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'
  --start-ts string            the start timestamp which log restore from. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'


Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
 -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

出力例には共通パラメータのみが表示されています。これらのパラメータの説明は以下のとおりです。

-   `--full-backup-storage` : スナップショット（フル）バックアップのstorageアドレス。PITRを使用する場合は、このパラメータを指定し、復元タイムスタンプ前の最新のスナップショットバックアップを選択します。ログバックアップデータのみを復元する場合は、このパラメータを省略できます。リカバリクラスターを初めて初期化する場合は、スナップショットバックアップを指定する必要があります。現在、 BRはログバックアップのstorageとしてAmazon S3、GCS、Azure Blob Storageをサポートしています。詳細は[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。
-   `--pitr-batch-count` : ログデータを復元する際の、1 回のバッチで処理できるファイルの最大数。このしきい値に達すると、現在のバッチは直ちに終了し、次のバッチが開始されます。
-   `--pitr-batch-size` : ログデータを復元する際の、1バッチあたりの最大データサイズ（バイト単位）。このしきい値に達すると、現在のバッチは直ちに終了し、次のバッチが開始されます。
-   `--pitr-concurrency` : ログ復元中の同時タスク数。各同時タスクは、一度に1バッチのログデータを復元します。
-   `--restored-ts` : データを復元するタイムスタンプ。このパラメータが指定されていない場合、 BRはログバックアップで利用可能な最新のタイムスタンプ、つまりバックアップデータのチェックポイントにデータを復元します。
-   `--start-ts` : ログバックアップデータを復元する開始タイムスタンプ。ログバックアップデータのみを復元する必要がある場合は、このパラメータを指定する必要があります。
-   `--pd` : 復元クラスターの PD アドレス。
-   `--ca` : TiKVおよびPDと通信するためのmTLS暗号化`--key` `--cert`指定します。
-   `--storage` : ログバックアップのstorageアドレス。現在、 BRはログバックアップのstorageとしてAmazon S3、GCS、またはAzure Blob Storageをサポートしています。詳細は[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

使用例:

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${access-key}&secret-access-key=${secret-access-key}'

Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ***["Full Restore success summary"] ****** [total-take=3.112928252s] [restore-data-size(after-compressed)=5.056kB] [Size=5056] [BackupTS=434693927394607136] [total-kv=4] [total-kv-size=290B] [average-speed=93.16B/s]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
"restore log success summary"] [total-take=192.955533ms] [restore-from=434693681289625602] [restore-to=434693753549881345] [total-kv-count=33] [total-size=21551]
```

> **注記：**
>
> -   クラスターを初めて復元する際は、完全なスナップショットデータを指定する必要があります。そうしないと、テーブルIDルールの書き換えにより、新しく作成されたテーブルの一部のデータが不正確になる可能性があります。詳細については、GitHub の問題[＃54418](https://github.com/pingcap/tidb/issues/54418)ご覧ください。
> -   特定の期間のログバックアップデータを繰り返しリストアすることはできません。範囲`[t1=10, t2=20)`のログバックアップデータを繰り返しリストアすると、リストアされたデータに不整合が生じる可能性があります。
> -   異なる期間のログデータを複数のバッチで復元する場合は、ログデータが連続した順序で復元されるようにしてください。ログバックアップデータ`[t1, t2)` 、 `[t2, t3)` 、 `[t3, t4)`連続した順序で復元すると、復元されたデータの整合性が保たれます。ただし、 `[t1, t2)`復元した後、 `[t2, t3)`スキップして`[t3, t4)`復元すると、復元されたデータの整合性が失われる可能性があります。

### 暗号化されたログバックアップデータを復元する {#restore-encrypted-log-backup-data}

暗号化されたログバックアップデータを復元するには、復元コマンドで対応する復号パラメータを渡す必要があります。復号パラメータが暗号化に使用されたものと同じであることを確認してください。復号アルゴリズムまたはキーが正しくない場合、データを復元できません。

次に例を示します。

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--crypter.method aes128-ctr
--crypter.key 0123456789abcdef0123456789abcdef
--log.crypter.method aes128-ctr
--log.crypter.key 0123456789abcdef0123456789abcdef
```

ログ バックアップがマスター キーを使用して暗号化されている場合は、次のコマンドを使用してバックアップ データを復号化して復元できます。

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--crypter.method aes128-ctr
--crypter.key 0123456789abcdef0123456789abcdef
--master-key-crypter-method aes128-ctr
--master-key "local:///path/to/master.key"
```
