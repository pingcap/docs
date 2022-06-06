---
title: Maintain DM Clusters Using dmctl
summary: Learn how to maintain a DM cluster using dmctl.
---

# dmctlを使用してDMクラスターを管理する {#maintain-dm-clusters-using-dmctl}

> **ノート：**
>
> TiUPを使用してデプロイされたDMクラスターの場合、クラスターを維持するために[`tiup dmctl`](/dm/maintain-dm-using-tiup.md#dmctl)を直接使用することをお勧めします。

dmctlは、DMクラスターを維持するために使用されるコマンドラインツールです。インタラクティブモードとコマンドモードの両方をサポートします。

## インタラクティブモード {#interactive-mode}

DMマスターと対話するには、対話モードに入ります。

> **ノート：**
>
> インタラクティブモードはBash機能をサポートしていません。たとえば、文字列フラグを引用符で囲むのではなく、直接渡す必要があります。

{{< copyable "" >}}

```bash
./dmctl --master-addr 172.16.30.14:8261
```

```
Welcome to dmctl
Release Version: ${version}
Git Commit Hash: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Git Branch: release-x.x
UTC Build Time: yyyy-mm-dd hh:mm:ss
Go Version: go version gox.xx linux/amd64

» help
DM control

Usage:
  dmctl [command]

Available Commands:
  check-task      Checks the configuration file of the task.
  config          Commands to import/export config.
  get-config      Gets the configuration.
  handle-error    `skip`/`replace`/`revert` the current error event or a specific binlog position (binlog-pos) event.
  help            Gets help about any command.
  list-member     Lists member information.
  offline-member  Offlines member which has been closed.
  operate-leader  `evict`/`cancel-evict` the leader.
  operate-schema  `get`/`set`/`remove` the schema for an upstream table.
  operate-source  `create`/`update`/`stop`/`show` upstream MySQL/MariaDB source.
  pause-relay     Pauses DM-worker's relay unit.
  pause-task      Pauses a specified running task.
  purge-relay     Purges relay log files of the DM-worker according to the specified filename.
  query-status    Queries task status.
  resume-relay    Resumes DM-worker's relay unit.
  resume-task     Resumes a specified paused task.
  show-ddl-locks  Shows un-resolved DDL locks.
  start-task      Starts a task as defined in the configuration file.
  stop-task       Stops a specified task.
  unlock-ddl-lock Unlocks DDL lock forcefully.

Flags:
  -h, --help             Help for dmctl.
  -s, --source strings   MySQL Source ID.

Use "dmctl [command] --help" for more information about a command.
```

## コマンドモード {#command-mode}

コマンドモードは、dmctlコマンドの直後にタスク操作を追加する必要があるという点でインタラクティブモードとは異なります。コマンドモードでのタスク操作のパラメータは、インタラクティブモードでのパラメータと同じです。

> **ノート：**
>
> -   dmctlコマンドの後には、1つのタスク操作のみを続ける必要があります。
> -   v2.0.4以降、DMは環境変数`DM_MASTER_ADDR`からの`-master-addr`パラメーターの読み取りをサポートします。

{{< copyable "" >}}

```bash
./dmctl --master-addr 172.16.30.14:8261 start-task task.yaml
./dmctl --master-addr 172.16.30.14:8261 stop-task task
./dmctl --master-addr 172.16.30.14:8261 query-status

export DM_MASTER_ADDR="172.16.30.14:8261"
./dmctl query-status
```

```
Available Commands:
  check-task            check-task <config-file> [--error count] [--warn count]
  config                commands to import/export config
  get-config            get-config <task | master | worker | source> <name> [--file filename]
  handle-error          handle-error <task-name | task-file> [-s source ...] [-b binlog-pos] <skip/replace/revert> [replace-sql1;replace-sql2;]
  list-member           list-member [--leader] [--master] [--worker] [--name master-name/worker-name ...]
  offline-member        offline-member <--master/--worker> <--name master-name/worker-name>
  operate-leader        operate-leader <operate-type>
  operate-schema        operate-schema <operate-type> <-s source ...> <task-name | task-file> <-d database> <-t table> [schema-file]
  operate-source        operate-source <operate-type> [config-file ...] [--print-sample-config]
  pause-relay           pause-relay <-s source ...>
  pause-task            pause-task [-s source ...] <task-name | task-file>
  purge-relay           purge-relay <-s source> <-f filename> [--sub-dir directory]
  query-status          query-status [-s source ...] [task-name | task-file] [--more]
  resume-relay          resume-relay <-s source ...>
  resume-task           resume-task [-s source ...] <task-name | task-file>
  show-ddl-locks        show-ddl-locks [-s source ...] [task-name | task-file]
  start-task            start-task [-s source ...] [--remove-meta] <config-file>
  stop-task             stop-task [-s source ...] <task-name | task-file>
  unlock-ddl-lock       unlock-ddl-lock <lock-ID>

Special Commands:
  --encrypt Encrypts plaintext to ciphertext.
  --decrypt Decrypts ciphertext to plaintext.

Global Options:
  --V Prints version and exit.
  --config Path to configuration file.
  --master-addr Master API server addr.
  --rpc-timeout RPC timeout, default is 10m.
  --ssl-ca Path of file that contains list of trusted SSL CAs for connection.
  --ssl-cert Path of file that contains X509 certificate in PEM format for connection.
  --ssl-key Path of file that contains X509 key in PEM format for connection.
```
