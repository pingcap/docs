---
title: TiDB Data Migration Quick Start
summary: Learn how to quickly deploy a DM cluster using binary packages.
---

# TiDBデータ移行のクイックスタートガイド {#quick-start-guide-for-tidb-data-migration}

このドキュメントでは、 [TiDBデータ移行](https://github.com/pingcap/dm) （DM）を使用してMySQLからTiDBにデータを移行する方法について説明します。

DMを実稼働環境にデプロイする必要がある場合は、次のドキュメントを参照してください。

-   [TiUPを使用してDMクラスタをデプロイする](/dm/deploy-a-dm-cluster-using-tiup.md)
-   [データソースを作成する](/dm/quick-start-create-source.md)
-   [データ移行タスクを作成する](/dm/quick-create-migration-task.md)

## サンプルシナリオ {#sample-scenario}

オンプレミス環境にDM-masterインスタンスとDM-workerインスタンスをデプロイし、データをアップストリームのMySQLインスタンスからダウンストリームのTiDBインスタンスに移行するとします。

各インスタンスの詳細情報は次のとおりです。

| 実例         | サーバーアドレス  | ポート              |
| :--------- | :-------- | :--------------- |
| DMマスター     | 127.0.0.1 | 8261、8291（内部ポート） |
| DMワーカー     | 127.0.0.1 | 8262             |
| MySQL-3306 | 127.0.0.1 | 3306             |
| TiDB       | 127.0.0.1 | 4000             |

## バイナリパッケージを使用してDMをデプロイ {#deploy-dm-using-the-binary-package}

### DMバイナリパッケージをダウンロード {#download-dm-binary-package}

DMの最新のバイナリパッケージをダウンロードするか、パッケージを手動でコンパイルします。

#### 方法1：最新バージョンのバイナリパッケージをダウンロードする {#method-1-download-the-latest-version-of-binary-package}

{{< copyable "" >}}

```bash
wget http://download.pingcap.org/dm-nightly-linux-amd64.tar.gz
tar -xzvf dm-nightly-linux-amd64.tar.gz
cd dm-nightly-linux-amd64
```

#### 方法2：最新バージョンのバイナリパッケージをコンパイルする {#method-2-compile-the-latest-version-of-binary-package}

{{< copyable "" >}}

```bash
git clone https://github.com/pingcap/dm.git
cd dm
make
```

### DMマスターをデプロイ {#deploy-dm-master}

次のコマンドを実行して、DMマスターを起動します。

{{< copyable "" >}}

```bash
nohup bin/dm-master --master-addr='127.0.0.1:8261' --log-file=/tmp/dm-master.log --name="master1" >> /tmp/dm-master.log 2>&1 &
```

### DM-workerをデプロイ {#deploy-dm-worker}

次のコマンドを実行して、DM-workerを起動します。

{{< copyable "" >}}

```bash
nohup bin/dm-worker --worker-addr='127.0.0.1:8262' --log-file=/tmp/dm-worker.log --join='127.0.0.1:8261' --name="worker1" >> /tmp/dm-worker.log 2>&1 &
```

### 展開ステータスを確認する {#check-deployment-status}

DMクラスタが正常にデプロイされたかどうかを確認するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
bin/dmctl --master-addr=127.0.0.1:8261 list-member
```

通常のDMクラスタは、次の情報を返します。

```bash
{
    "result": true,
    "msg": "",
    "members": [
        {
            "leader": {
                "msg": "",
                "name": "master1",
                "addr": "127.0.0.1:8261"
            }
        },
        {
            "master": {
                "msg": "",
                "masters": [
                    {
                        "name": "master1",
                        "memberID": "11007177379717700053",
                        "alive": true,
                        "peerURLs": [
                            "http://127.0.0.1:8291"
                        ],
                        "clientURLs": [
                            "http://127.0.0.1:8261"
                        ]
                    }
                ]
            }
        },
        {
            "worker": {
                "msg": "",
                "workers": [
                    {
                        "name": "worker1",
                        "addr": "127.0.0.1:8262",
                        "stage": "free",
                        "source": ""
                    }
                ]
            }
        }
    ]
}
```

## MySQLからTiDBにデータを移行する {#migrate-data-from-mysql-to-tidb}

### サンプルデータを準備する {#prepare-sample-data}

DMを使用する前に、次のサンプルデータを`MySQL-3306`に挿入します。

{{< copyable "" >}}

```sql
drop database if exists `testdm`;
create database `testdm`;
use `testdm`;
create table t1 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
create table t2 (id bigint, uid int, name varchar(80), info varchar(100), primary key (`id`), unique key(`uid`)) DEFAULT CHARSET=utf8mb4;
insert into t1 (id, uid, name) values (1, 10001, 'Gabriel García Márquez'), (2, 10002, 'Cien años de soledad');
insert into t2 (id, uid, name) values (3, 20001, 'José Arcadio Buendía'), (4, 20002, 'Úrsula Iguarán'), (5, 20003, 'José Arcadio');
```

### データソース構成をロードする {#load-data-source-configurations}

データ移行タスクを実行する前に、まず対応するデータソース（つまり、例では`MySQL-3306` ）の構成ファイルをDMにロードする必要があります。

#### データソースのパスワードを暗号化する {#encrypt-the-data-source-password}

> **ノート：**
>
> -   データソースにパスワードがない場合は、この手順をスキップできます。
> -   プレーンテキストのパスワードを使用して、DMv2.0以降のバージョンでデータソース情報を構成できます。

安全上の理由から、データソースに暗号化されたパスワードを設定して使用することをお勧めします。パスワードが「123456」であるとします。

{{< copyable "" >}}

```bash
./bin/dmctl --encrypt "123456"
```

```
fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=
```

この暗号化された値を保存し、次の手順でMySQLデータソースを作成するために使用します。

#### MySQLインスタンスのソース構成ファイルを編集します {#edit-the-source-configuration-file-of-the-mysql-instance}

次の構成を`conf/source1.yaml`に書き込みます。

```yaml
# MySQL1 Configuration.
source-id: "mysql-replica-01"
from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

#### データソース構成ファイルをロードします {#load-data-source-configuration-file}

dmctlを使用してMySQLのデータソース構成ファイルをDMクラスタにロードするには、ターミナルで次のコマンドを実行します。

{{< copyable "" >}}

```bash
./bin/dmctl --master-addr=127.0.0.1:8261 operate-source create conf/source1.yaml
```

返される結果の例を次に示します。

```bash
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        }
    ]
}
```

これで、データソース`MySQL-3306`がDMクラスタに正常に追加されました。

### データ移行タスクを作成する {#create-a-data-migration-task}

[サンプルデータ](#prepare-sample-data)を`MySQL-3306`に挿入した後、次の手順を実行してテーブル`testdm`を移行します。 `t1`と`testdm` 。 `t2`ダウンストリームTiDBインスタンスへ：

1.  タスク構成ファイル`testdm-task.yaml`を作成し、次の構成をファイルに追加します。

    {{< copyable "" >}}

    ```yaml
    ---
    name: testdm
    task-mode: all
    target-database:
      host: "127.0.0.1"
      port: 4000
      user: "root"
      password: "" # If the password is not null, it is recommended to use password encrypted with dmctl.
    mysql-instances:
      - source-id: "mysql-replica-01"
        block-allow-list:  "ba-rule1"
    block-allow-list:
      ba-rule1:
        do-dbs: ["testdm"]
    ```

2.  dmctlを使用してタスク構成ファイルをロードします。

    {{< copyable "" >}}

    ```bash
    ./bin/dmctl --master-addr 127.0.0.1:8261 start-task testdm-task.yaml
    ```

    返される結果の例を次に示します。

    ```bash
    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "worker1"
            }
        ]
    }
    ```

これで、データを`MySQL-3306`からダウンストリームTiDBインスタンスに移行するデータ移行タスクを正常に作成できました。

### データ移行タスクのステータスを確認する {#check-status-of-the-data-migration-task}

データ移行タスクが作成されたら、 `dmtcl query-status`を使用してタスクのステータスを確認できます。次の例を参照してください。

{{< copyable "" >}}

```bash
./bin/dmctl --master-addr 127.0.0.1:8261 query-status
```

返される結果の例を次に示します。

```bash
{
    "result": true,
    "msg": "",
    "tasks": [
        {
            "taskName": "testdm",
            "taskStatus": "Running",
            "sources": [
                "mysql-replica-01"
            ]
        }
    ]
}
```
