---
title: Migrate Incremental Data from MySQL-Compatible Databases
summary: Learn how to migrate incremental data from MySQL-compatible databases to TiDB Cloud.
---

# MySQL 互換データベースからの増分データの移行 {#migrate-incremental-data-from-mysql-compatible-databases}

このドキュメントでは、MySQL 互換データベースからTiDB Cloudに増分データを移行する方法について説明します。

## あなたが始める前に {#before-you-begin}

増分データ移行を実行する前に、MySQL 互換データベースからTiDB Cloudへの完全なデータ移行を完了しておく必要があります。詳細については、 [MySQL 互換データベースからデータを移行する](/tidb-cloud/migrate-data-into-tidb.md)を参照してください。

## ステップ 1.DM クラスターをデプロイ {#step-1-deploy-a-dm-cluster}

TiDB Cloudコンソールは、増分データ移行機能をまだ提供していません。 TiDB Cloudへの増分移行を実行するには、手動で[TiDB データ移行](https://docs.pingcap.com/tidb/stable/dm-overview) (DM) をデプロイする必要があります。インストール手順については、 [TiUPを使用して DMクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/deploy-a-dm-cluster-using-tiup)を参照してください。

## 手順 2. データ ソース構成ファイルを作成する {#step-2-create-a-data-source-configuration-file}

まず、データ ソース構成ファイルを作成する必要があります。データ ソースは、データの移行元の MySQL インスタンスです。以下は、データ ソース構成ファイルの作成例です。ファイル内の MySQL IP アドレス、ポート、ユーザー名、およびパスワードの値を独自の値に置き換える必要があります。

```shell
# Encrypt MySQL password
[root@localhost ~]# tiup dmctl encrypt {mysq-user-password}
mZMkdjbRztSag6qEgoh8UkDY6X13H48=

[root@localhost ~]# cat dm-source1.yaml
```

```yaml
# MySQL Configuration.
source-id: "mysql-replica-01"

# Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs.
# To enable this mode, the upstream MySQL must also enable GTID.
# If the upstream MySQL service is configured to switch master between different nodes automatically, GTID mode is required.
enable-gtid: true

from:
  host: "192.168.10.101"
  user: "user01"
  password: "mZMkdjbRztSag6qEgoh8UkDY6X13H48="
  port: 3307
```

次のコマンドを実行して、 `tiup dmctl`を使用してデータ ソース構成を DM クラスターに読み込みます。

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} operate-source create dm-source1.yaml
```

上記のコマンドで使用されるパラメーターは、次のとおりです。

| パラメータ                   | 説明                                                                           |
| ----------------------- | ---------------------------------------------------------------------------- |
| `--master-addr`         | `dmctl`が接続されるクラスター内の任意の DM マスター ノードの`{advertise-addr}` 。例: 172.16.7.140:9261 |
| `operate-source create` | データ ソースを DM クラスターに読み込みます。                                                    |

次に出力例を示します。

```
tiup is checking updates for component dmctl ...
Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 192.168.11.110:9261 operate-source create dm-source1.yaml
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "dm-192.168.11.120-9262"
        }
    ]
}
```

## ステップ 3.移行タスクを作成する {#step-3-create-a-migration-task}

移行用の`dm-task1.yaml`ファイルを作成します。増分移行モードとデータ ソースの開始点をファイルに構成します。

[Dumpling](/dumpling-overview.md)によってエクスポートされたメタデータ ファイルで開始点を見つけることができます。例えば：

```toml
# Get the contents of the metadata in the file exported by Dumpling
# Use it to configure the incremental migration starting point
# cat metadata
Started dump at: 2022-05-24 11:19:37
SHOW MASTER STATUS:
    Log: mysql-bin.000001
    Pos: 77092852
    GTID:b631bcad-bb10-11ec-9eee-fec83cf2b903:1-640

Finished dump at: 2022-05-24 11:19:53
```

上記の開始点情報に基づいて、次のように移行タスクを作成します。

```toml
## ********* Task Configuration *********
name: test-task1
# shard-mode: "pessimistic"
# Task mode. The "incremental" mode only performs incremental data migration.
task-mode: incremental
# timezone: "UTC"

## ******** Data Source Configuration **********
## (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data migration error.
##  This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
syncers:         # The running configurations of the sync processing unit.
  global:        # Configuration name.
  safe-mode: false   # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental migration task, DM automatically enables the safe mode.

mysql-instances:
  - source-id: "mysql-replica-01"
    block-allow-list:  "bw-rule-1"
    route-rules: ["route-rule-1"]
    filter-rules: ["tpcc-filter-rule"]
    syncer-config-name: "global"                   # You can use the syncers incremental data configuration above.
    meta:                                          # When task-mode is "incremental" and the target database does not have a checkpoint, DM uses the binlog position as the starting point. If the target database has a checkpoint, DM uses the checkpoint as the starting point.
    binlog-name: "mysql-bin.000001"
    binlog-pos: 77092852
    binlog-gtid: "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-640"

## ******** Configuration of the target TiDB cluster on TiDB Cloud **********
target-database:    # The target TiDB cluster on TiDB Cloud
  host: "tidb.70593805.b973b556.ap-northeast-1.prod.aws.tidbcloud.com"
  port: 4000
  user: "root"
  password: "oSWRLvR3F5GDIgm+l+9h3kB72VFWBUwzOw=="     # If the password is not empty, it is recommended to use a dmctl-encrypted cipher.

## ******** Function Configuration **********
block-allow-list:
  bw-rule-1:
    do-dbs: ["~^tpcc.*"]

routes:                       # Table renaming rules ('routes') from upstream to downstream tables, in order to support merging different tables into a single target table.
  route-rule-1:               # Rule name.
    schema-pattern: "tpcc"    # Rule for matching upstream schema names. It supports the wildcards "*" and "?".
    target-schema: "tpdd"     # Name of the target schema.

filters:
  tpcc-filter-rule:
    schema-pattern: "tpcc"
    events: ["drop database"]
    action: Ignore

##  ******** Ignore check items **********
ignore-checking-items: ["table_schema"]
```

詳細なタスク構成については、 [DM タスク構成](https://docs.pingcap.com/tidb/stable/task-configuration-file-full)を参照してください。

データ移行タスクをスムーズに実行するために、DM はタスクの開始時に事前チェックを自動的にトリガーし、チェック結果を返します。 DM は、事前チェックに合格した後にのみ移行を開始します。事前チェックを手動でトリガーするには、次の`check-task`コマンドを実行します。

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} check-task dm-task1.yaml
```

次に出力例を示します。

```
tiup is checking updates for component dmctl ...
Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 192.168.11.110:9261 check-task dm-task1.yaml
{
    "result": true,
    "msg": "check pass!!!"
}
```

## ステップ 4. 移行タスクを開始する {#step-4-start-the-migration-task}

次のコマンドを実行して、移行タスクを開始します。

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} start-task dm-task1.yaml
```

上記のコマンドで使用されるパラメーターは、次のとおりです。

| パラメータ           | 説明                                                                           |
| --------------- | ---------------------------------------------------------------------------- |
| `--master-addr` | `dmctl`が接続されるクラスター内の任意の DM マスター ノードの`{advertise-addr}` 。例: 172.16.7.140:9261 |
| `start-task`    | 移行タスクを開始します。                                                                 |

次に出力例を示します。

```
tiup is checking updates for component dmctl ...
Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 192.168.11.110:9261 start-task dm-task1.yaml
{
    "result": true,
    "msg": "",
    "sources": [
        {
           "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "dm-192.168.11.120-9262"
        }
    ],
    "checkResult": ""
}
```

タスクの開始に失敗した場合は、プロンプト メッセージを確認し、構成を修正します。その後、上記のコマンドを再実行してタスクを開始できます。

問題が発生した場合は、 [DM エラー処理](https://docs.pingcap.com/tidb/stable/dm-error-handling)および[DMFAQ](https://docs.pingcap.com/tidb/stable/dm-faq)を参照してください。

## ステップ 5. 移行タスクのステータスを確認する {#step-5-check-the-migration-task-status}

DM クラスターに進行中の移行タスクがあるかどうかを確認し、タスクのステータスを表示するには、 `tiup dmctl`使用して`query-status`コマンドを実行します。

```shell
[root@localhost ~]# tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

次に出力例を示します。

```
tiup is checking updates for component dmctl ...
Starting component `dmctl`: /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl /root/.tiup/components/dmctl/v6.0.0/dmctl/dmctl --master-addr 192.168.11.110:9261 query-status test-task1
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "sourceStatus": {
                "source": "mysql-replica-01",
                "worker": "dm-192.168.11.120-9262",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [
                {
                    "name": "test-task1",
                    "stage": "Running",
                    "unit": "Sync",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "sync": {
                        "totalEvents": "3",
                        "totalTps": "0",
                        "recentTps": "0",
                        "masterBinlog": "(mysql-bin.000001, 77093211)",
                        "masterBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-641",
                        "syncerBinlog": "(mysql-bin.000001, 77093211)",
                        "syncerBinlogGtid": "b631bcad-bb10-11ec-9eee-fec83cf2b903:1-641",
                        "blockingDDLs": [
                        ],
                       "unresolvedGroups": [
                        ],
                        "synced": true,
                        "binlogType": "remote",
                        "secondsBehindMaster": "0",
                        "blockDDLOwner": "",
                     "conflictMsg": ""
                    }
                }
            ]
        ]
}
```

結果の詳細な解釈については、 [クエリのステータス](https://docs.pingcap.com/tidb/stable/dm-query-status)を参照してください。
