---
title: Manage Data Source Configurations
summary: Learn how to manage upstream MySQL instances in TiDB Data Migration.
---

# データソース構成の管理 {#manage-data-source-configurations}

このドキュメントでは、MySQLパスワードの暗号化、データソースの操作、 [dmctl](/dm/dmctl-introduction.md)を使用したアップストリームMySQLインスタンスとDMワーカー間のバインディングの変更など、データソース構成を管理する方法を紹介します。

## データベースのパスワードを暗号化する {#encrypt-the-database-password}

DM構成ファイルでは、dmctlで暗号化されたパスワードを使用することをお勧めします。 1つの元のパスワードの場合、暗号化されたパスワードは暗号化ごとに異なります。

{{< copyable "" >}}

```bash
./dmctl -encrypt 'abc!@#123'
```

```
MKxn0Qo3m3XOyjCnhEMtsUCm83EhGQDZ/T4=
```

## データソースを操作する {#operate-data-source}

`operate-source`コマンドを使用して、データソース構成をDMクラスタにロード、リスト、または削除できます。

{{< copyable "" >}}

```bash
help operate-source
```

```
`create`/`update`/`stop`/`show` upstream MySQL/MariaDB source.

Usage:
  dmctl operate-source <operate-type> [config-file ...] [--print-sample-config] [flags]

Flags:
  -h, --help                  help for operate-source
  -p, --print-sample-config   print sample config file of source

Global Flags:
  -s, --source strings   MySQL Source ID
```

### フラグの説明 {#flags-description}

-   `create` ：1つ以上のアップストリームデータベースソースを作成します。複数のデータソースの作成に失敗すると、DMはコマンドが実行されなかった状態にロールバックします。

-   `update` ：アップストリームデータベースソースを更新します。

-   `stop` ：1つ以上のアップストリームデータベースソースを停止します。複数のデータソースの停止に失敗すると、一部のデータソースが停止する場合があります。

-   `show` ：追加されたデータソースと対応するDMワーカーを表示します。

-   `config-file` ： `source.yaml`のファイルパスを指定し、複数のファイルパスを渡すことができます。

-   `--print-sample-config` ：サンプル設定ファイルを出力します。このパラメーターは他のパラメーターを無視します。

### 使用例 {#usage-example}

次の`operate-source`のコマンドを使用して、ソース構成ファイルを作成します。

{{< copyable "" >}}

```bash
operate-source create ./source.yaml
```

`source.yaml`の構成については、 [アップストリームデータベースConfiguration / コンフィグレーションファイルの概要](/dm/dm-source-configuration-file.md)を参照してください。

返される結果の例を次に示します。

{{< copyable "" >}}

```
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
```

### データソース構成を確認する {#check-data-source-configurations}

> **ノート：**
>
> `config`コマンドは、DMv6.0以降のバージョンでのみサポートされます。以前のバージョンでは、 `get-config`コマンドを使用する必要があります。

`source-id`がわかっている場合は、 `dmctl --master-addr <master-addr> config source <source-id>`を実行してデータソース構成を取得できます。

{{< copyable "" >}}

```bash
config source mysql-replica-01
```

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
```

`source-id`がわからない場合は、 `dmctl --master-addr <master-addr> operate-source show`を実行して、最初にすべてのデータソースを一覧表示できます。

{{< copyable "" >}}

```bash
operate-source show
```

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
```

## アップストリームのMySQLインスタンスとDMワーカー間のバインディングを変更します {#change-the-bindings-between-upstream-mysql-instances-and-dm-workers}

`transfer-source`コマンドを使用して、アップストリームのMySQLインスタンスとDMワーカー間のバインディングを変更できます。

{{< copyable "" >}}

```bash
help transfer-source
```

```
Transfers an upstream MySQL/MariaDB source to a free worker.
Usage:
  dmctl transfer-source <source-id> <worker-id> [flags]
Flags:
  -h, --help   help for transfer-source
Global Flags:
  -s, --source strings   MySQL Source ID.
```

DMは、転送する前に、バインド解除するワーカーにまだ実行中のタスクがあるかどうかを確認します。ワーカーに実行中のタスクがある場合は、最初に[タスクを一時停止します](/dm/dm-pause-task.md)を実行し、バインディングを変更してから[タスクを再開する](/dm/dm-resume-task.md)を実行する必要があります。

### 使用例 {#usage-example}

DMワーカーのバインディングがわからない場合は、 `dmctl --master-addr <master-addr> list-member --worker`を実行して、すべてのワーカーの現在のバインディングを一覧表示できます。

{{< copyable "" >}}

```bash
list-member --worker
```

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
```

上記の例では、 `mysql-replica-01`は`dm-worker-1`にバインドされています。以下のコマンドは、 `mysql-replica-01`から`dm-worker-2`のバインディングワーカーを転送します。

{{< copyable "" >}}

```bash
transfer-source mysql-replica-01 dm-worker-2
```

```
{
    "result": true,
    "msg": ""
}
```

`dmctl --master-addr <master-addr> list-member --worker`を実行して、コマンドが有効になるかどうかを確認します。

{{< copyable "" >}}

```bash
list-member --worker
```

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
```
