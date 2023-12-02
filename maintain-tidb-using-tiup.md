---
title: TiUP Common Operations
summary: Learn the common operations to operate and maintain a TiDB cluster using TiUP.
---

# TiUP共通操作 {#tiup-common-operations}

このドキュメントでは、 TiUP を使用して TiDB クラスターを運用および保守する場合の次の一般的な操作について説明します。

-   クラスターリストをビュー
-   クラスターを開始する
-   クラスターのステータスをビュー
-   構成を変更する
-   クラスターを停止する
-   クラスターを破壊する

## クラスターリストをビュー {#view-the-cluster-list}

TiUPクラスターコンポーネントを使用して、複数の TiDB クラスターを管理できます。 TiDB クラスターがデプロイされると、クラスターはTiUPクラスター リストに表示されます。

リストを表示するには、次のコマンドを実行します。

```bash
tiup cluster list
```

## クラスターを開始する {#start-the-cluster}

TiDB クラスター内のコンポーネントは次の順序で開始されます。

**PD &gt; TiKV &gt;Pump&gt; TiDB &gt; TiFlash &gt;Drainer&gt; TiCDC &gt; Prometheus &gt; Grafana &gt; Alertmanager**

クラスターを開始するには、次のコマンドを実行します。

```bash
tiup cluster start ${cluster-name}
```

> **注記：**
>
> `${cluster-name}`クラスターの名前に置き換えます。クラスター名を忘れた場合は、 `tiup cluster list`を実行して確認してください。

コマンドに`-R`または`-N`パラメータを追加することで、一部のコンポーネントのみを起動できます。例えば：

-   このコマンドは PDコンポーネントのみを開始します。

    ```bash
    tiup cluster start ${cluster-name} -R pd
    ```

-   このコマンドは、ホスト`1.2.3.4`とホスト`1.2.3.5`上の PD コンポーネントのみを起動します。

    ```bash
    tiup cluster start ${cluster-name} -N 1.2.3.4:2379,1.2.3.5:2379
    ```

> **注記：**
>
> `-R`または`-N`パラメータを使用して指定したコンポーネントを起動する場合は、起動順序が正しいことを確認してください。たとえば、TiKVコンポーネントの前に PDコンポーネントを開始します。そうしないと、起動に失敗する可能性があります。

## クラスターのステータスをビュー {#view-the-cluster-status}

クラスターを起動した後、各コンポーネントのステータスをチェックして、それらが正常に動作していることを確認します。 TiUP は`display`コマンドを提供するため、コンポーネントのステータスを表示するためにすべてのマシンにログインする必要はありません。

```bash
tiup cluster display ${cluster-name}
```

## 構成を変更する {#modify-the-configuration}

クラスターの動作中にコンポーネントのパラメーターを変更する必要がある場合は、 `edit-config`コマンドを実行します。詳細な手順は次のとおりです。

1.  編集モードでクラスターの構成ファイルを開きます。

    ```bash
    tiup cluster edit-config ${cluster-name}
    ```

2.  パラメータを設定します。

    -   構成がコンポーネントに対してグローバルに有効な場合は、 `server_configs`を編集します。

            server_configs:
              tidb:
                log.slow-threshold: 300

    -   構成が特定のノードで有効になる場合は、ノードの`config`で構成を編集します。

            tidb_servers:
            - host: 10.0.1.11
              port: 4000
              config:
                  log.slow-threshold: 300

    パラメータの形式については、 [TiUPパラメータテンプレート](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)を参照してください。

    **使用`.`構成アイテムの階層を表します**。

    コンポーネントの構成パラメータの詳細については、 [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/release-7.5/pkg/config/config.toml.example) 、 [TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/release-7.5/etc/config-template.toml) 、および[PD `config.toml.example`](https://github.com/tikv/pd/blob/release-7.5/conf/config.toml)を参照してください。

3.  `reload`コマンドを実行して、構成をローリング更新し、対応するコンポーネントを再起動します。

    ```bash
    tiup cluster reload ${cluster-name} [-N <nodes>] [-R <roles>]
    ```

### 例 {#example}

tidb-server でトランザクション サイズ制限パラメーター ( [パフォーマンス](https://github.com/pingcap/tidb/blob/release-7.5/pkg/config/config.toml.example)モジュールの`txn-total-size-limit` ) を`1G`に設定する場合は、次のように構成を編集します。

    server_configs:
      tidb:
        performance.txn-total-size-limit: 1073741824

次に、 `tiup cluster reload ${cluster-name} -R tidb`コマンドを実行して TiDBコンポーネントをローリング再起動します。

## 修正プログラムパッケージに置き換えます {#replace-with-a-hotfix-package}

通常のアップグレードについては、 [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md)を参照してください。ただし、デバッグなどの一部のシナリオでは、現在実行中のコンポーネントを一時パッケージに置き換える必要がある場合があります。これを実現するには、 `patch`コマンドを使用します。

```bash
tiup cluster patch --help
```

    Replace the remote package with a specified package and restart the service

    Usage:
      cluster patch <cluster-name> <package-path> [flags]

    Flags:
      -h, --help                   help for patch
      -N, --node strings           Specify the nodes
          --overwrite              Use this package in the future scale-out operations
      -R, --role strings           Specify the role
          --transfer-timeout int   Timeout in seconds when transferring PD and TiKV store leaders (default 600)

    Global Flags:

          --native-ssh        Use the system's native SSH client
          --wait-timeout int  Timeout of waiting the operation
          --ssh-timeout int   Timeout in seconds to connect host via SSH, ignored for operations that don't need an SSH connection. (default 5)
      -y, --yes               Skip all confirmations and assumes 'yes'

TiDB ホットフィックス パッケージが`/tmp/tidb-hotfix.tar.gz`にあり、クラスター内のすべての TiDB パッケージを置き換える場合は、次のコマンドを実行します。

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -R tidb
```

クラスター内の TiDB パッケージを 1 つだけ置き換えることもできます。

```bash
tiup cluster patch test-cluster /tmp/tidb-hotfix.tar.gz -N 172.16.4.5:4000
```

## クラスターの名前を変更する {#rename-the-cluster}

クラスターをデプロイして開始した後、 `tiup cluster rename`コマンドを使用してクラスターの名前を変更できます。

```bash
tiup cluster rename ${cluster-name} ${new-name}
```

> **注記：**
>
> -   クラスターの名前を変更する操作により、監視システム (Prometheus および Grafana) が再起動されます。
> -   クラスターの名前が変更された後、古いクラスター名の一部のパネルが Grafana 上に残る場合があります。手動で削除する必要があります。

## クラスターを停止する {#stop-the-cluster}

TiDB クラスター内のコンポーネントは次の順序で停止します (モニタリングコンポーネントも停止します)。

**アラートマネージャー &gt; Grafana &gt; Prometheus &gt; TiCDC &gt;Drainer&gt; TiFlash &gt; TiDB &gt;Pump&gt; TiKV &gt; PD**

クラスターを停止するには、次のコマンドを実行します。

```bash
tiup cluster stop ${cluster-name}
```

`start`コマンドと同様に、 `stop`コマンドは`-R`または`-N`パラメータを追加することで一部のコンポーネントの停止をサポートします。例えば：

-   このコマンドは、TiDBコンポーネントのみを停止します。

    ```bash
    tiup cluster stop ${cluster-name} -R tidb
    ```

-   このコマンドは、ホスト`1.2.3.4`とホスト`1.2.3.5`上の TiDB コンポーネントのみを停止します。

    ```bash
    tiup cluster stop ${cluster-name} -N 1.2.3.4:4000,1.2.3.5:4000
    ```

## クラスターデータのクリーンアップ {#clean-up-cluster-data}

クラスター データのクリーンアップ操作では、すべてのサービスが停止され、データ ディレクトリまたはログ ディレクトリ、あるいはその両方がクリーンアップされます。操作を元に戻すことはできないため、**注意して**続行してください。

-   クラスター内のすべてのサービスのデータをクリーンアップしますが、ログは保持します。

    ```bash
    tiup cluster clean ${cluster-name} --data
    ```

-   クラスター内のすべてのサービスのログをクリーンアップしますが、データは保持します。

    ```bash
    tiup cluster clean ${cluster-name} --log
    ```

-   クラスター内のすべてのサービスのデータとログをクリーンアップします。

    ```bash
    tiup cluster clean ${cluster-name} --all
    ```

-   Prometheus を除くすべてのサービスのログとデータをクリーンアップします。

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-role prometheus
    ```

-   `172.16.13.11:9000`インスタンスを除くすべてのサービスのログとデータをクリーンアップします。

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.11:9000
    ```

-   `172.16.13.12`ノードを除くすべてのサービスのログとデータをクリーンアップします。

    ```bash
    tiup cluster clean ${cluster-name} --all --ignore-node 172.16.13.12
    ```

## クラスターを破壊する {#destroy-the-cluster}

破棄操作によりサービスが停止され、データ ディレクトリとデプロイメント ディレクトリがクリアされます。操作を元に戻すことはできないため、**注意して**続行してください。

```bash
tiup cluster destroy ${cluster-name}
```
