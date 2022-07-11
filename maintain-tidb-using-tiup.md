---
title: TiUP Common Operations
summary: Learn the common operations to operate and maintain a TiDB cluster using TiUP.
---

# TiUPの一般的な操作 {#tiup-common-operations}

このドキュメントでは、TiUPを使用してTiDBクラスタを操作および保守する場合の次の一般的な操作について説明します。

-   クラスタリストをビューする
-   クラスタを開始します
-   クラスタのステータスをビューする
-   構成を変更する
-   クラスタを停止します
-   クラスタを破壊する

## クラスタリストをビューする {#view-the-cluster-list}

TiUPクラスタコンポーネントを使用して、複数のTiDBクラスターを管理できます。 TiDBクラスタがデプロイされると、クラスタはTiUPクラスタリストに表示されます。

リストを表示するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup cluster list
```

## クラスタを開始します {#start-the-cluster}

TiDBクラスタのコンポーネントは、次の順序で開始されます。

**PD&gt;TiKV&gt;Pump&gt;TiDB&gt;TiFlash&gt;Drainer&gt;TiCDC&gt;プロメテウス&gt;Grafana&gt;Alertmanager**

クラスタを起動するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup cluster start ${cluster-name}
```

> **ノート：**
>
> `${cluster-name}`をクラスタの名前に置き換えます。クラスタ名を忘れた場合は、 `tiup cluster list`を実行して確認してください。

コマンドに`-R`つまたは`-N`のパラメーターを追加することにより、一部のコンポーネントのみを開始できます。例えば：

-   このコマンドは、PDコンポーネントのみを起動します。

    {{< copyable "" >}}

    ```bash
    tiup cluster start ${cluster-name} -R pd
    ```

-   このコマンドは、 `1.2.3.4`および`1.2.3.5`ホスト上のPDコンポーネントのみを開始します。

    {{< copyable "" >}}

    ```bash
    tiup cluster start ${cluster-name} -N 1.2.3.4:2379,1.2.3.5:2379
    ```

> **ノート：**
>
> `-R`つまたは`-N`のパラメーターを使用して指定されたコンポーネントを開始する場合は、開始順序が正しいことを確認してください。たとえば、TiKVコンポーネントの前にPDコンポーネントを開始します。そうしないと、起動が失敗する可能性があります。

## クラスタのステータスをビューする {#view-the-cluster-status}

クラスタを起動した後、各コンポーネントのステータスをチェックして、正常に動作することを確認します。 TiUPは`display`コマンドを提供するため、コンポーネントのステータスを表示するためにすべてのマシンにログインする必要はありません。

{{< copyable "" >}}

```bash
tiup cluster display ${cluster-name}
```

## 構成を変更する {#modify-the-configuration}

クラスタが動作しているときに、コンポーネントのパラメータを変更する必要がある場合は、 `edit-config`コマンドを実行します。詳細な手順は次のとおりです。

1.  クラスタの構成ファイルを編集モードで開きます。

    {{< copyable "" >}}

    ```bash
    tiup cluster edit-config ${cluster-name}
    ```

2.  パラメータを設定します。

    -   構成がコンポーネントに対してグローバルに有効である場合は、 `server_configs`を編集します。

        ```
        server_configs:
          tidb:
            log.slow-threshold: 300
        ```

    -   構成が特定のノードで有効になる場合は、ノードの`config`で構成を編集します。

        ```
        tidb_servers:
        - host: 10.0.1.11
          port: 4000
          config:
              log.slow-threshold: 300
        ```

    パラメータの形式については、 [TiUPパラメータテンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)を参照してください。

    **を使用し`.`構成アイテムの階層を表します**。

    コンポーネントの構成パラメーターの詳細については、 [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) 、および[TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/master/etc/config-template.toml)を参照して[PD `config.toml.example`](https://github.com/tikv/pd/blob/master/conf/config.toml) 。

3.  `reload`コマンドを実行して、構成をローリング更新し、対応するコンポーネントを再起動します。

    {{< copyable "" >}}

    ```bash
    tiup cluster reload ${cluster-name} [-N <nodes>] [-R <roles>]
    ```

### 例 {#example}

tidb-serverでトランザクションサイズ制限パラメーター（ [パフォーマンス](https://github.com/pingcap/tidb/blob/master/config/config.toml.example)モジュールの`txn-total-size-limit` ）を`1G`に設定する場合は、次のように構成を編集します。

```
server_configs:
  tidb:
    performance.txn-total-size-limit: 1073741824
```

次に、 `tiup cluster reload ${cluster-name} -R tidb`コマンドを実行して、TiDBコンポーネントをローリングリスタートします。

## 修正プログラムパッケージと交換してください {#replace-with-a-hotfix-package}

通常のアップグレードについては、 [TiUPを使用してTiDBをアップグレードする](/upgrade-tidb-using-tiup.md)を参照してください。ただし、デバッグなどの一部のシナリオでは、現在実行中のコンポーネントを一時パッケージに置き換える必要がある場合があります。これを実現するには、次の`patch`のコマンドを使用します。

{{< copyable "" >}}

```bash
tiup cluster patch --help
```

```
Replace the remote package with a specified package and restart the service

Usage:
  cluster patch <cluster-name> <package-path> [flags]

Flags:
  -h, --help                   help for patch
  -N, --node strings           Specify the nodes
      --overwrite              Use this package in the future scale-out operations
  -R, --role strings           Specify the role
      --transfer-timeout int   Timeout in seconds when transferring PD and TiKV store leaders (default 300)

Global Flags:

      --native-ssh        Use the system's native SSH client
      --wait-timeout int  Timeout of waiting the operation
      --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
  -y, --yes               Skip all confirmations and assumes 'yes'
```

TiDBホットフィックスパッケージが`/tmp/tidb-hotfix.tar.gz`に含まれていて、クラスタのすべてのTiDBパッケージを置き換える場合は、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

クラスタの1つのTiDBパッケージのみを置き換えることもできます。

{{< copyable "" >}}

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## クラスタの名前を変更します {#rename-the-cluster}

クラスタをデプロイして開始した後、 `tiup cluster rename`コマンドを使用してクラスタの名前を変更できます。

{{< copyable "" >}}

```bash
tiup cluster rename ${cluster-name} ${new-name}
```

> **ノート：**
>
> -   クラスタの名前を変更する操作により、監視システム（PrometheusおよびGrafana）が再起動します。
> -   クラスタクラスタの一部のパネルがGrafanaに残る場合があります。手動で削除する必要があります。

## クラスタを停止します {#stop-the-cluster}

TiDBクラスタのコンポーネントは、次の順序で停止します（監視コンポーネントも停止します）。

**Alertmanager&gt; Grafana&gt; Prometheus&gt; TiCDC&gt; Drainer &gt; TiFlash&gt; TiDB&gt; Pump &gt; TiKV&gt; PD**

クラスタを停止するには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
tiup cluster stop ${cluster-name}
```

`start`コマンドと同様に、 `stop`コマンドは、 `-R`または`-N`個のパラメーターを追加することにより、一部のコンポーネントの停止をサポートします。例えば：

-   このコマンドは、TiDBコンポーネントのみを停止します。

    {{< copyable "" >}}

    ```bash
    tiup cluster stop ${cluster-name} -R tidb
    ```

-   このコマンドは、 `1.2.3.4`および`1.2.3.5`ホスト上のTiDBコンポーネントのみを停止します。

    {{< copyable "" >}}

    ```bash
    tiup cluster stop ${cluster-name} -N 1.2.3.4:4000,1.2.3.5:4000
    ```

## クラスタデータをクリーンアップする {#clean-up-cluster-data}

クラスタデータをクリーンアップする操作は、すべてのサービスを停止し、データディレクトリまたはログディレクトリ、あるいはその両方をクリーンアップします。操作を元に戻すことはできませんので**、注意して進めてください**。

-   クラスタのすべてのサービスのデータをクリーンアップしますが、ログは保持します。

    {{< copyable "" >}}

    ```bash
    tiup cluster clean ${cluster-name} --data
    ```

-   クラスタのすべてのサービスのログをクリーンアップしますが、データは保持します。

    {{< copyable "" >}}

    ```bash
    tiup cluster clean ${cluster-name} --log
    ```

-   クラスタのすべてのサービスのデータとログをクリーンアップします。

    {{< copyable "" >}}

    ```bash
    tiup cluster clean ${cluster-name} --all
    ```

-   Prometheusを除くすべてのサービスのログとデータをクリーンアップします。

    {{< copyable "" >}}

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-role prometheus
    ```

-   `172.16.13.11:9000`つのインスタンスを除くすべてのサービスのログとデータをクリーンアップします。

    {{< copyable "" >}}

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.11:9000
    ```

-   `172.16.13.12`のノードを除くすべてのサービスのログとデータをクリーンアップします。

    {{< copyable "" >}}

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.12
    ```

## クラスタを破壊する {#destroy-the-cluster}

破棄操作はサービスを停止し、データディレクトリとデプロイメントディレクトリをクリアします。操作を元に戻すことはできませんので**、注意して進めてください**。

{{< copyable "" >}}

```bash
tiup cluster destroy ${cluster-name}
```
