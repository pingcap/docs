---
title: TiDB Log Backup and PITR Command Manual
summary: TiDB ログ バックアップとポイントインタイム リカバリ (PITR) で使用されるコマンドを紹介します。
---

# TiDB ログバックアップと PITR コマンドマニュアル {#tidb-log-backup-and-pitr-command-manual}

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

出力例には共通パラメータのみが表示されています。これらのパラメータは以下のように記述されます。

-   `--start-ts` : ログバックアップの開始タイムスタンプを指定します。このパラメータが指定されていない場合、バックアッププログラムは現在の時刻を`start-ts`として使用します。
-   `task-name` : ログバックアップのタスク名を指定します。この名前は、バックアップタスクのクエリ、一時停止、再開にも使用されます。
-   `--ca` : TiKVおよびPDと通信`--key`ためのmTLS暗号化方式`--cert`指定します。
-   `--pd` : バックアップ クラスターの PD アドレスを指定します。BRはログ バックアップ タスクを開始するために PD にアクセスする必要があります。
-   `--storage` : バックアップstorageのアドレスを指定します。現在、 BRはログバックアップのstorageとしてAmazon S3、Google Cloud Storage (GCS)、またはAzure Blob Storageをサポートしています。上記のコマンドではAmazon S3を例として使用しています。詳細は[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

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

-   `--log.crypter.method` : 暗号化アルゴリズム。2、4、6 `aes192-ctr` `aes128-ctr`かになります。デフォルト値は`aes256-ctr` `plaintext` 、データは暗号化されません。
-   `--log.crypter.key` : 16進文字列形式の暗号化キー。アルゴリズム`aes128-ctr`の場合は128ビット（16バイト）、アルゴリズム`aes192-ctr`の場合は24バイト、アルゴリズム`aes256-ctr`の場合は32バイトのキーです。
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

ただし、セキュリティ要件が高いシナリオでは、固定の暗号化キーをコマンドラインで直接渡すことは望ましくない場合があります。セキュリティをさらに強化するには、マスターキーベースの暗号化システムを使用して暗号化キーを管理できます。このシステムは、ログバックアップファイルごとに異なるデータキーを生成し、マスターキーのローテーションをサポートします。以下のパラメータを使用して設定できます。

-   `--master-key-crypter-method` : マスターキーに基づく暗号化アルゴリズム。2、4 `aes192-ctr`または`aes256-ctr` `aes128-ctr`かになります。デフォルト値は`plaintext`で、データは暗号化されません。
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
> -   暗号化機能は、 `br`および TiDB クラスター v8.4.0 以降で使用する必要があります。暗号化されたログバックアップデータは、v8.4.0 より前のクラスターでは復元できません。

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

-   `status` : バックアップ タスクのステータス。 `NORMAL` 、 `ERROR` 、または`PAUSE`になります。
-   `start` : バックアップタスクの開始時刻。バックアップタスクの開始時に指定された`start-ts`です。
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

ログバックアップタスクを停止するには、コマンド`tiup br log stop`を実行します。このコマンドは、バックアップクラスター内のタスクメタデータをクリーンアップします。

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
> `restore point`の増分バックアップ アドレスとして`--full-backup-storage`指定した場合、このバックアップと以前の増分バックアップを復元するには、増分バックアップと後続のログ バックアップとの互換性を確保するために、パラメータ`--allow-pitr-from-incremental` `true`に設定する必要があります。

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

出力例には共通パラメータのみが表示されています。これらのパラメータは以下のように記述されます。

-   `--full-backup-storage` : スナップショット（フル）バックアップのstorageアドレス。PITRを使用する場合は、このパラメータを指定して、復元タイムスタンプ前の最新のスナップショットバックアップを選択します。ログバックアップデータのみを復元する場合は、このパラメータを省略できます。リカバリクラスターを初めて初期化する場合は、スナップショットバックアップを指定する必要があります。現在、 BRはログバックアップのstorageとしてAmazon S3、GCS、Azure Blob Storageをサポートしています。詳細は[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。
-   `--pitr-batch-count` : ログデータを復元する際の、1バッチあたりのファイル数の上限。このしきい値に達すると、現在のバッチは直ちに終了し、次のバッチが開始されます。
-   `--pitr-batch-size` : ログデータを復元する際の単一バッチの最大データサイズ（バイト単位）。このしきい値に達すると、現在のバッチは直ちに終了し、次のバッチが開始されます。
-   `--pitr-concurrency` : ログ復元中の同時タスク数。各同時タスクは、一度に1バッチのログデータを復元します。
-   `--restored-ts` : データを復元するタイムスタンプ。このパラメータが指定されていない場合、 BRはログバックアップで利用可能な最新のタイムスタンプ、つまりバックアップデータのチェックポイントにデータを復元します。
-   `--start-ts` : ログバックアップデータを復元する開始タイムスタンプ。ログバックアップデータのみを復元する必要がある場合は、このパラメータを指定する必要があります。
-   `--pd` : 復元クラスターの PD アドレス。
-   `--ca` : TiKVおよびPDと通信`--key`ためのmTLS暗号化方式`--cert`指定します。
-   `--storage` : ログバックアップのstorageアドレス。現在、 BRはログバックアップのstorageとしてAmazon S3、GCS、またはAzure Blob Storageをサポートしています。詳細は[外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

使用例:

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${access-key}&secret-access-key=${secret-access-key}'

Split&Scatter Region <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Download&Ingest SST <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore Pipeline <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ***["Full Restore success summary"] ****** [total-take=3.112928252s] [restore-data-size(after-compressed)=5.056kB] [Size=5056] [BackupTS=434693927394607136] [total-kv=4] [total-kv-size=290B] [average-speed=93.16B/s]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
"restore log success summary"] [total-take=192.955533ms] [restore-from=434693681289625602] [restore-to=434693753549881345] [total-kv-count=33] [total-size=21551]
```

> **注記：**
>
> -   クラスターを初めて復元する際は、完全なスナップショットデータを指定する必要があります。そうしないと、テーブルIDルールの書き換えにより、新しく作成されたテーブルの一部のデータが正しくなくなる可能性があります。詳細については、GitHub の問題[＃54418](https://github.com/pingcap/tidb/issues/54418)をご覧ください。
> -   特定の期間のログバックアップデータを繰り返しリストアすることはできません。範囲`[t1=10, t2=20)`のログバックアップデータを繰り返しリストアすると、リストアされたデータに不整合が生じる可能性があります。
> -   異なる期間のログデータを複数のバッチで復元する場合は、ログデータが連続した順序で復元されるようにしてください。ログバックアップデータ`[t1, t2)` 、 `[t2, t3)` 、 `[t3, t4)`を連続した順序で復元すると、復元されたデータは整合性を保ちます。ただし、 `[t1, t2)`復元した後、 `[t2, t3)`スキップして`[t3, t4)`を復元すると、復元されたデータは不整合になる可能性があります。

### 暗号化されたログバックアップデータを復元する {#restore-encrypted-log-backup-data}

暗号化されたログバックアップデータを復元するには、復元コマンドで対応する復号パラメータを渡す必要があります。復号パラメータが暗号化に使用したパラメータと一致していることを確認してください。復号アルゴリズムまたはキーが正しくない場合、データを復元できません。

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

### フィルターを使用してデータを復元する {#restore-data-using-filters}

TiDB v8.5.5 以降では、PITR 中にフィルターを使用して特定のデータベースまたはテーブルを復元できるようになり、復元するデータをより細かく制御できるようになりました。

フィルタ パターンは他のBR操作と同じ[テーブルフィルタリング構文](/table-filter.md)に従います。

-   `'*.*'` : すべてのデータベースとテーブルに一致します。
-   `'db1.*'` : データベース`db1`内のすべてのテーブルに一致します。
-   `'db1.table1'` : データベース`db1`内の特定のテーブル`table1`と一致します。
-   `'db*.tbl*'` : `db`で始まるデータベースと`tbl`で始まるテーブルに一致します。
-   `'!mysql.*'` : `mysql`データベース内のすべてのテーブルを除外します。

使用例:

```shell
# restore specific databases
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db1.*' --filter 'db2.*'

# restore specific tables
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db1.users' --filter 'db1.orders'

# restore using pattern matching
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db*.tbl*'
```

> **注記：**
>
> -   フィルターを使用してデータを復元する前に、ターゲットクラスターにフィルターに一致するデータベースまたはテーブルが含まれていないことを確認してください。含まれていない場合、復元はエラーで失敗します。
> -   フィルター オプションは、スナップショット バックアップとログ バックアップの両方の復元フェーズ中に適用されます。
> -   複数の`--filter`オプションを指定して、異なるパターンを含めたり除外したりできます。
> -   PITRフィルタリングはシステムテーブルをまだサポートしていません。特定のシステムテーブルを復元する必要がある場合は、代わりにフィルターを指定した`br restore full`コマンドを使用してください。このコマンドはスナップショットバックアップデータのみを復元し、ログバックアップデータは復元しないことに注意してください。
> -   復元タスク内の正規表現は、 `restored-ts`番目の時点でのテーブル名と一致し、次の 3 つのケースが考えられます。
>     -   テーブルA（テーブルID = 1）：テーブル名は、 `restored-ts`番目の時点以前において、常に`--filter`正規表現と一致します。この場合、PITRはテーブルを復元します。
>     -   テーブルB（テーブルID = 2）：テーブル名は`restored-ts`より前の時点では`--filter`正規表現と一致しませんでしたが、 `restored-ts`番目の時点では一致しました。この場合、PITRはテーブルを復元します。
>     -   テーブルC（テーブルID = 3）：テーブル名は、 `restored-ts`より前の時点では正規表現`--filter`と一致していましたが、 `restored-ts`時点では一致**していません**。この場合、PITRはテーブルを復元しませ**ん**。
> -   データベースとテーブルのフィルタリング機能を使用して、データの一部をオンラインで復元できます。オンライン復元プロセス中は、復元されたオブジェクトと同じ名前のデータベースまたはテーブルを作成し**ないで**ください。そうしないと、競合が発生して復元タスクが失敗します。データの不整合を回避するため、この復元プロセス中にPITRによって作成されたテーブルは、復元タスクが完了するまで読み取りも書き込みもできません。

### 同時復元操作 {#concurrent-restore-operations}

TiDB v8.5.5以降では、複数のPITRリストアタスクを同時に実行できるようになりました。この機能により、異なるデータセットを並行してリストアできるため、大規模なリストアシナリオにおける効率が向上します。

同時復元の使用例:

```shell
# terminal 1 - restore database db1
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db1.*'

# terminal 2 - restore database db2 (can run simultaneously)
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db2.*'
```

> **注記：**
>
> -   各同時復元操作は、異なるデータベースまたは重複しないテーブルセットを対象とする必要があります。重複するデータセットを同時に復元しようとすると、エラーが発生します。
> -   複数の復元タスクはシステムリソースを大量に消費します。CPUとI/Oリソースが十分な場合にのみ、複数の復元タスクを同時に実行することをお勧めします。

### 進行中のログバックアップとスナップショット復元の互換性 {#compatibility-between-ongoing-log-backup-and-snapshot-restore}

v8.5.5 以降では、ログ バックアップ タスクの実行中に、次の条件がすべて満たされている場合は、スナップショット リストア ( `br restore [full|database|table]` ) を実行し、進行中のログ バックアップ (以下、「ログ バックアップ」) によってリストアされたデータを適切に記録することができます。

-   バックアップおよび復元操作を実行するノードには、次の必要な権限があります。
    -   スナップショットの復元のための、バックアップソースを含む外部storageへの読み取りアクセス
    -   ログバックアップで使用されるターゲット外部storageへの書き込みアクセス
-   ログバックアップの対象となる外部storageは、Amazon S3（ `s3://` ）、Google Cloud Storage（ `gcs://` ）、またはAzure Blob Storage（ `azblob://` ）です。
-   復元するデータは、ログ バックアップのターゲットstorageと同じ種類の外部storageを使用します。
-   復元対象のデータとログバックアップのどちらにもローカル暗号化が有効になっていません。詳細については、 [ログバックアップの暗号化](#encrypt-the-log-backup-data)と[スナップショットバックアップの暗号化](/br/br-snapshot-manual.md#encrypt-the-backup-data)参照してください。

上記の条件のいずれかが満たされていない場合は、次の手順に従ってデータを復元できます。

1.  [ログバックアップタスクを停止する](#stop-a-log-backup-task) 。
2.  データの復元を実行します。
3.  復元が完了したら、新しいスナップショット バックアップを実行します。
4.  [ログバックアップタスクを再開する](#restart-a-log-backup-task) 。

> **注記：**
>
> スナップショット（完全）復元データの記録を含むログバックアップを復元する場合は、 BR v8.5.5以降を使用する必要があります。そうでない場合、記録された完全復元データの復元が失敗する可能性があります。

### 進行中のログバックアップと PITR 操作間の互換性 {#compatibility-between-ongoing-log-backup-and-pitr-operations}

TiDB v8.5.5以降では、ログバックアップタスクの実行中にPITR操作をデフォルトで実行できるようになりました。これらの操作間の互換性はシステムによって自動的に処理されます。

#### 継続的なログバックアップを伴うPITRの重要な制限 {#important-limitation-for-pitr-with-ongoing-log-backup}

ログバックアップの実行中にPITR操作を実行すると、復元されたデータは進行中のログバックアップにも記録されます。ただし、ログ復元操作の性質上、復元ウィンドウ内でデータの不整合が発生する可能性があります。システムは、整合性が保証できない時間範囲とデータ範囲の両方を示すメタデータを外部storageに書き込みます。

期間`[t1, t2)`にこのような不整合が発生した場合、この期間のデータを直接復元することはできません。代わりに、以下のいずれかの方法を選択してください。

-   データを`t1`まで復元します（不整合期間前のデータを取得します）。
-   `t2`後に新しいスナップショット バックアップを実行し、それを将来の PITR 操作のベースとして使用します。

### 復元操作を中止する {#abort-restore-operations}

復元操作が失敗した場合、 `tiup br abort`コマンドを使用してレジストリエントリとチェックポイントデータをクリーンアップできます。このコマンドは、元の復元パラメータに基づいて、 `mysql.tidb_restore_registry`テーブルのエントリやチェックポイントデータ（ローカルデータベースに保存されているか外部storageに保存されているかに関係なく）を含む関連メタデータを自動的に検索して削除します。

> **注記：**
>
> `abort`コマンドはメタデータのみをクリーンアップします。復元された実際のデータはクラスターから手動で削除する必要があります。

次の例は、元の復元コマンドと同じパラメータを使用して復元操作を中止する方法を示しています。

```shell
# Abort a PITR operation
tiup br abort restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'

# Abort a PITR operation with filters
tiup br abort restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--filter 'db1.*'

# Abort a full restore
tiup br abort restore full --pd="${PD_IP}:2379" \
--storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'

# Abort a database restore
tiup br abort restore db --pd="${PD_IP}:2379" \
--storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--db database_name

# Abort a table restore
tiup br abort restore table --pd="${PD_IP}:2379" \
--storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--db database_name --table table_name
```
