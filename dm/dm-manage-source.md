---
title: Manage Data Source Configurations in TiDB Data Migration
summary: TiDB データ移行でアップストリーム MySQL インスタンスを管理する方法を学習します。
---

# TiDB データ移行におけるデータソース構成の管理 {#manage-data-source-configurations-in-tidb-data-migration}

このドキュメントでは、MySQL パスワードの暗号化、データ ソースの操作、 [dmctl](/dm/dmctl-introduction.md)を使用したアップストリーム MySQL インスタンスと DM ワーカー間のバインディングの変更など、データ ソース構成を管理する方法について説明します。

## データベースのパスワードを暗号化する {#encrypt-the-database-password}

DM設定ファイルでは、dmctlで暗号化されたパスワードを使用することをお勧めします。元のパスワードは1つですが、暗号化されるたびに暗号化されたパスワードは異なります。

> **注記：**
>
> v8.0.0 以降では、 `dmctl encrypt`コマンドを使用する前に、DM-master に[`secret-key-path`](/dm/dm-master-configuration-file.md)設定する必要があります。

```bash
./dmctl encrypt 'abc!@#123'
```

    MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=

## データソースを操作する {#operate-data-source}

`operate-source`コマンドを使用して、データ ソース構成を DM クラスターにロード、一覧表示、または削除できます。

```bash
help operate-source
```

    `create`/`stop`/`show` upstream MySQL/MariaDB source.

    Usage:
      dmctl operate-source <operate-type> [config-file ...] [--print-sample-config] [flags]

    Flags:
      -h, --help                  help for operate-source
      -p, --print-sample-config   print sample config file of source

    Global Flags:
      -s, --source strings   MySQL Source ID

### フラグの説明 {#flags-description}

-   `create` : 1つ以上の上流データベースソースを作成します。複数のデータソースの作成に失敗した場合、DMはコマンドが実行されなかった状態にロールバックします。

-   `stop` : 1つ以上の上流データベースソースを停止します。複数のデータソースの停止に失敗した場合、一部のデータソースが停止される可能性があります。

-   `show` : 追加されたデータ ソースと対応する DM ワーカーを表示します。

-   `config-file` : `source.yaml`のファイル パスを指定し、複数のファイル パスを渡すことができます。

-   `--print-sample-config` : サンプル設定ファイルを印刷します。このパラメータは他のパラメータを無視します。

### 使用例 {#usage-example}

次の`operate-source`コマンドを使用して、ソース構成ファイルを作成します。

```bash
operate-source create ./source.yaml
```

`source.yaml`の設定については[アップストリームデータベースコンフィグレーションファイルの概要](/dm/dm-source-configuration-file.md)を参照してください。

返される結果の例を次に示します。

    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "dm-worker-1"
            }
        ]
    }

### データソースの構成を確認する {#check-data-source-configurations}

> **注記：**
>
> `config`コマンドは DM v6.0 以降のバージョンでのみサポートされます。それ以前のバージョンでは、 `get-config`コマンドを使用する必要があります。

`source-id`わかっている場合は、 `dmctl --master-addr <master-addr> config source <source-id>`実行してデータ ソース構成を取得できます。

```bash
config source mysql-replica-01
```

    {
      "result": true,
        "msg": "",
        "cfg": "enable-gtid: false
          flavor: mysql
          source-id: mysql-replica-01
          from:
            host: 127.0.0.1
            port: 8407
            user: root
            password: '******'
    }

`source-id`わからない場合は、まず`dmctl --master-addr <master-addr> operate-source show`を実行してすべてのデータ ソースを一覧表示できます。

```bash
operate-source show
```

    {
        "result": true,
        "msg": "",
        "sources": [
            {
                "result": true,
                "msg": "source is added but there is no free worker to bound",
                "source": "mysql-replica-02",
                "worker": ""
            },
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-01",
                "worker": "dm-worker-1"
            }
        ]
    }

## アップストリームのMySQLインスタンスとDMワーカー間のバインディングを変更する {#change-the-bindings-between-upstream-mysql-instances-and-dm-workers}

`transfer-source`コマンドを使用して、アップストリーム MySQL インスタンスと DM ワーカー間のバインディングを変更できます。

```bash
help transfer-source
```

    Transfers an upstream MySQL/MariaDB source to a free worker.
    Usage:
      dmctl transfer-source <source-id> <worker-id> [flags]
    Flags:
      -h, --help   help for transfer-source
    Global Flags:
      -s, --source strings   MySQL Source ID.

転送前に、DM はバインド解除するワーカーに実行中のタスクがあるかどうかを確認します。ワーカーに実行中のタスクがある場合は、まず[タスクを一時停止する](/dm/dm-pause-task.md)実行し、バインドを変更してから[タスクを再開する](/dm/dm-resume-task.md)実行する必要があります。

### 使用例 {#usage-example}

DM ワーカーのバインディングがわからない場合は、 `dmctl --master-addr <master-addr> list-member --worker`実行して、すべてのワーカーの現在のバインディングを一覧表示できます。

```bash
list-member --worker
```

    {
        "result": true,
        "msg": "",
        "members": [
            {
                "worker": {
                    "msg": "",
                    "workers": [
                        {
                            "name": "dm-worker-1",
                            "addr": "127.0.0.1:8262",
                            "stage": "bound",
                            "source": "mysql-replica-01"
                        },
                        {
                            "name": "dm-worker-2",
                            "addr": "127.0.0.1:8263",
                            "stage": "free",
                            "source": ""
                        }
                    ]
                }
            }
        ]
    }

上記の例では、 `mysql-replica-01` `dm-worker-1`にバインドされています。以下のコマンドは、 `mysql-replica-01`のバインドワーカーを`dm-worker-2`に転送します。

```bash
transfer-source mysql-replica-01 dm-worker-2
```

    {
        "result": true,
        "msg": ""
    }

`dmctl --master-addr <master-addr> list-member --worker`実行して、コマンドが有効になるかどうかを確認します。

```bash
list-member --worker
```

    {
        "result": true,
        "msg": "",
        "members": [
            {
                "worker": {
                    "msg": "",
                    "workers": [
                        {
                            "name": "dm-worker-1",
                            "addr": "127.0.0.1:8262",
                            "stage": "free",
                            "source": ""
                        },
                        {
                            "name": "dm-worker-2",
                            "addr": "127.0.0.1:8263",
                            "stage": "bound",
                            "source": "mysql-replica-01"
                        }
                    ]
                }
            }
        ]
    }
