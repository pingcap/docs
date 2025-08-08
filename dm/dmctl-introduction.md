---
title: Maintain DM Clusters Using dmctl
summary: dmctl を使用して DM クラスターを保守する方法を学習します。
---

# dmctl を使用して DM クラスターを管理 {#maintain-dm-clusters-using-dmctl}

> **注記：**
>
> TiUPを使用してデプロイされた DM クラスターの場合は、クラスターを維持するために[`tiup dmctl`](/dm/maintain-dm-using-tiup.md#dmctl)直接使用することをお勧めします。

dmctl は、DM クラスタのメンテナンスに使用するコマンドラインツールです。対話モードとコマンドモードの両方をサポートしています。

## インタラクティブモード {#interactive-mode}

DM マスターと対話するには、対話モードに入ります。

> **注記：**
>
> 対話型モードではBashの機能をサポートしていません。例えば、文字列フラグは引用符で囲むのではなく、直接渡す必要があります。

```bash
./dmctl --master-addr 172.16.30.14:8261
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
      binlog          manage or show binlog operations
      binlog-schema   manage or show table schema in schema tracker
      check-task      Checks the configuration file of the task
      config          manage config operations
      encrypt         Encrypts plain text to cipher text
      help            Gets help about any command
      list-member     Lists member information
      offline-member  Offlines member which has been closed
      operate-leader  `evict`/`cancel-evict` the leader
      operate-source  `create`/`stop`/`show` upstream MySQL/MariaDB source
      pause-relay     Pauses DM-worker's relay unit
      pause-task      Pauses a specified running task or all (sub)tasks bound to a source
      purge-relay     Purges relay log files of the DM-worker according to the specified filename
      query-status    Queries task status
      resume-relay    Resumes DM-worker's relay unit
      resume-task     Resumes a specified paused task or all (sub)tasks bound to a source
      shard-ddl-lock  maintain or show shard-ddl locks information
      start-relay     Starts workers pulling relay log for a source
      start-task      Starts a task as defined in the configuration file
      stop-relay      Stops workers pulling relay log for a source
      stop-task       Stops a specified task or all (sub)tasks bound to a source
      transfer-source Transfers a upstream MySQL/MariaDB source to a free worker

    Flags:
      -h, --help             Help for dmctl.
      -s, --source strings   MySQL Source ID.

    Use "dmctl [command] --help" for more information about a command.

## コマンドモード {#command-mode}

コマンドモードは対話モードとは異なり、dmctlコマンドの直後にタスク操作を追加する必要があります。コマンドモードでのタスク操作のパラメータは、対話モードの場合と同じです。

> **注記：**
>
> -   dmctl コマンドの後には 1 つのタスク操作のみが続く必要があります。
> -   v2.0.4 以降、DM は環境変数`DM_MASTER_ADDR`から`-master-addr`パラメータの読み取りをサポートします。

```bash
./dmctl --master-addr 172.16.30.14:8261 start-task task.yaml
./dmctl --master-addr 172.16.30.14:8261 stop-task task
./dmctl --master-addr 172.16.30.14:8261 query-status

export DM_MASTER_ADDR="172.16.30.14:8261"
./dmctl query-status
```

    Available Commands:
      binlog          manage or show binlog operations
      binlog-schema   manage or show table schema in schema tracker
      check-task      Checks the configuration file of the task
      config          manage config operations
      encrypt         Encrypts plain text to cipher text
      help            Gets help about any command
      list-member     Lists member information
      offline-member  Offlines member which has been closed
      operate-leader  `evict`/`cancel-evict` the leader
      operate-source  `create`/`stop`/`show` upstream MySQL/MariaDB source
      pause-relay     Pauses DM-worker's relay unit
      pause-task      Pauses a specified running task or all (sub)tasks bound to a source
      purge-relay     Purges relay log files of the DM-worker according to the specified filename
      query-status    Queries task status
      resume-relay    Resumes DM-worker's relay unit
      resume-task     Resumes a specified paused task or all (sub)tasks bound to a source
      shard-ddl-lock  maintain or show shard-ddl locks information
      start-relay     Starts workers pulling relay log for a source
      start-task      Starts a task as defined in the configuration file
      stop-relay      Stops workers pulling relay log for a source
      stop-task       Stops a specified task or all (sub)tasks bound to a source
      transfer-source Transfers a upstream MySQL/MariaDB source to a free worker

    Flags:
          --config string        Path to config file.
      -h, --help                 help for dmctl
          --master-addr string   Master API server address, this parameter is required when interacting with the dm-master
          --rpc-timeout string   RPC timeout, default is 10m. (default "10m")
      -s, --source strings       MySQL Source ID.
          --ssl-ca string        Path of file that contains list of trusted SSL CAs for connection.
          --ssl-cert string      Path of file that contains X509 certificate in PEM format for connection.
          --ssl-key string       Path of file that contains X509 key in PEM format for connection.
      -V, --version              Prints version and exit.

    Use "dmctl [command] --help" for more information about a command.
