---
title: Scale PD Microservice Nodes Using TiUP
summary: TiUPを使用してクラスター内の PD マイクロサービス ノードをスケーリングする方法と、PD の動作モードを切り替える方法を学習します。
---

# TiUPを使用して PD マイクロサービス ノードをスケールする {#scale-pd-microservices-nodes-using-tiup}

このドキュメントでは、クラスター内の[PDマイクロサービス](/pd-microservices.md)ノード (TSO ノードとスケジューリング ノードを含む) をスケーリングする方法と、 TiUPを使用して PD 動作モードを切り替える方法について説明します。

現在のクラスター名リストを表示するには、 `tiup cluster list`実行します。

たとえば、クラスターの元のトポロジは次のようになります。

| ホストIP    | サービス        |
| :------- | :---------- |
| 10.0.1.4 | TiDB + PD   |
| 10.0.1.5 | TiKV + モニター |
| 10.0.1.1 | TiKV        |
| 10.0.1.2 | TiKV        |
| 10.0.1.6 | TSO         |
| 10.0.1.7 | スケジュール      |

## TSO/スケジューリングノードを追加する {#add-tso-scheduling-nodes}

> **注記：**
>
> PD マイクロサービスがまだ有効になっていない TiDB クラスターに TSO/スケジューリング ノードを追加するには、代わりに[通常モードからマイクロサービスモードに切り替える](#switch-from-regular-mode-to-microservices-mode)の手順に従ってください。

このセクションでは、PD マイクロサービスが有効になっている TiDB クラスターに TSO ノード (IP アドレス`10.0.1.8` ) とスケジューリング ノード (IP アドレス`10.0.1.9` ) を追加する方法を例示します。

### 1. スケールアウトトポロジを構成する {#1-configure-the-scale-out-topology}

> **注記：**
>
> -   デフォルトでは、ポートとディレクトリの情報は必要ありません。ただし、1台のマシンに複数のインスタンスがある場合は、各インスタンスに異なるポートとディレクトリを割り当てる必要があります。ポートまたはディレクトリが競合する場合は、デプロイまたはスケーリング中に通知が表示されます。
> -   TiUP v1.0.0 以降、スケールアウト構成は元のクラスターの`global`構成を継承します。

`scale-out.yml`ファイルにスケールアウト トポロジ構成を追加します。

```shell
vi scale-out.yml
```

以下は TSO ノードの構成例です。

```ini
tso_servers:
  - host: 10.0.1.8
    port: 3379
```

以下はスケジューリング ノードの構成例です。

```ini
scheduling_servers:
  - host: 10.0.1.9
    port: 3379
```

現在のクラスターの構成を表示するには、 `tiup cluster edit-config <cluster-name>`実行します。 `global`と`server_configs`のパラメータ設定は`scale-out.yml`に継承されるため、 `scale-out.yml`でも有効になります。

### 2.スケールアウトコマンドを実行する {#2-run-the-scale-out-command}

`scale-out`コマンドを実行する前に、 `check`コマンドと`check --apply`コマンドを使用して、クラスター内の潜在的なリスクを検出し、自動的に修復します。

1.  潜在的なリスクを確認します。

    ```shell
    tiup cluster check <cluster-name> scale-out.yml --cluster --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2.  自動修復を有効にする:

    ```shell
    tiup cluster check <cluster-name> scale-out.yml --cluster --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

3.  `scale-out`コマンドを実行します。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

上記のコマンドでは、

-   `scale-out.yml`はスケールアウト構成ファイルです。
-   `--user root` 、クラスタのスケールアウトを完了するために、ターゲットマシンに`root`ユーザーとしてログインすることを示します。4 `root`ユーザーは、ターゲットマシンに対して`ssh`と`sudo`権限を持つことが想定されています。または、 `ssh`と`sudo`権限を持つ他のユーザーを使用してデプロイを完了することもできます。
-   `[-i]`と`[-p]`オプションです。ターゲットマシンへのログインにパスワードを使用しない設定をしている場合は、これらのパラメータは不要です。そうでない場合は、2つのパラメータのいずれかを選択してください。4 `[-i]` 、ターゲットマシンにアクセスできるルートユーザー（または`--user`で指定された他のユーザー）の秘密鍵です。8 `[-p]` 、ユーザーパスワードを対話的に入力するために使用されます。

`Scaled cluster <cluster-name> out successfully`表示された場合、スケールアウト操作は成功しています。

### 3. クラスターのステータスを確認する {#3-check-the-cluster-status}

```shell
tiup cluster display <cluster-name>
```

ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスターと新しいノードのステータスを監視します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホストIP    | サービス        |
| :------- | :---------- |
| 10.0.1.4 | TiDB + PD   |
| 10.0.1.5 | TiKV + モニター |
| 10.0.1.1 | TiKV        |
| 10.0.1.2 | TiKV        |
| 10.0.1.6 | TSO         |
| 10.0.1.7 | スケジュール      |
| 10.0.1.8 | TSO         |
| 10.0.1.9 | スケジュール      |

## TSO/スケジューリングノードを削除する {#remove-tso-scheduling-nodes}

> **注記：**
>
> PD マイクロサービスが有効になっているクラスターを非マイクロサービス モードに切り替える必要がある場合は、代わりに[マイクロサービスモードから通常モードに切り替える](#switch-from-microservices-mode-to-regular-mode)の手順に従ってください。

このセクションでは、複数の TSO ノードまたはスケジューリング ノードを持つ TiDB クラスターから TSO ノード (IP アドレス`10.0.1.8` ) とスケジューリング ノード (IP アドレス`10.0.1.9` ) を削除する方法を例示します。

### 1. ノードID情報をビュー {#1-view-the-node-id-information}

```shell
tiup cluster display <cluster-name>
```

    Starting /root/.tiup/components/cluster/v1.16/cluster display <cluster-name>

    TiDB Cluster: <cluster-name>

    TiDB Version: v8.5.3

    ID       Role         Host    Ports                            Status  Data Dir        Deploy Dir

    --       ----         ----      -----                            ------  --------        ----------

    10.0.1.4:2379  pd           10.0.1.4    2379/2380                        Healthy data/pd-2379      deploy/pd-2379

    10.0.1.1:20160 tikv         10.0.1.1    20160/20180                      Up      data/tikv-20160     deploy/tikv-20160

    10.0.1.2:20160 tikv         10.0.1.2    20160/20180                      Up      data/tikv-20160     deploy/tikv-20160

    10.0.1.5:20160 tikv        10.0.1.5    20160/20180                     Up      data/tikv-20160     deploy/tikv-20160

    10.0.1.4:4000  tidb        10.0.1.4    4000/10080                      Up      -                 deploy/tidb-4000

    10.0.1.5:9090  prometheus   10.0.1.5    9090                             Up      data/prometheus-9090  deploy/prometheus-9090

    10.0.1.5:3000  grafana      10.0.1.5    3000                             Up      -            deploy/grafana-3000

    10.0.1.5:9093  alertmanager 10.0.1.5    9093/9094                        Up      data/alertmanager-9093 deploy/alertmanager-9093

    10.0.1.6:3379  tso          10.0.1.6    3379                            Up|P     data/tso-3379     deploy/tso-3379

    10.0.1.8:3379  tso          10.0.1.8    3379                            Up       data/tso-3379    deploy/tso-3379

    10.0.1.7:3379  scheduling   10.0.1.7    3379                            Up|P     data/scheduling-3379     deploy/scheduling-3379

    10.0.1.9:3379  scheduling   10.0.1.9    3379                            Up       data/scheduling-3379     deploy/scheduling-3379

### 2. スケールインコマンドを実行する {#2-run-scale-in-commands}

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.8:3379
tiup cluster scale-in <cluster-name> --node 10.0.1.9:3379
```

`--node`パラメータは、オフラインにするノードの ID です。

`Scaled cluster <cluster-name> in successfully`表示された場合、スケールイン操作は成功しています。

### 3. クラスターのステータスを確認する {#3-check-the-cluster-status}

次のコマンドを実行して、ノードが正常に削除されたかどうかを確認します。

```shell
tiup cluster display <cluster-name>
```

ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスター全体のステータスを監視します。

スケールイン後、現在のトポロジは次のようになります。

| ホストIP    | サービス        |
| :------- | :---------- |
| 10.0.1.4 | TiDB + PD   |
| 10.0.1.5 | TiKV + モニター |
| 10.0.1.1 | TiKV        |
| 10.0.1.2 | TiKV        |
| 10.0.1.6 | TSO         |
| 10.0.1.7 | スケジュール      |

## PD動作モードを切り替える {#switch-the-pd-working-mode}

PD サービスを次の 2 つの動作モード間で切り替えることができます。

-   通常モード: PD ノードのみでルーティング サービス、タイムスタンプ割り当て、およびクラスター スケジューリング関数を提供します。
-   マイクロサービスモード：PDタイムスタンプ割り当て機能をTSOノード（ `tso`マイクロサービスを提供）に、クラスタースケジューリング機能をスケジューリングノード（ `scheduling`マイクロサービスを提供）にそれぞれ個別にデプロイできます。これにより、これら2つの関数はPDのルーティング機能から分離され、PDノードはメタデータのルーティングサービスに集中できます。

> **注記：**
>
> モード切り替え中は、PD サービスが数分間利用できなくなります。

### 通常モードからマイクロサービスモードに切り替える {#switch-from-regular-mode-to-microservices-mode}

PD マイクロサービスが有効になっていないクラスターの場合は、次のように PD マイクロサービス モードに切り替えて、TSO ノード (IP アドレス`10.0.1.8` ) とスケジューリング ノード (IP アドレス`10.0.1.9` ) を追加できます。

1.  `scale-out.yml`ファイルにスケールアウト トポロジ構成を追加します。

    ```shell
    vi scale-out.yml
    ```

    以下は設定例です。

    ```ini
    tso_servers:
      - host: 10.0.1.8
        port: 3379
    scheduling_servers:
      - host: 10.0.1.9
        port: 3379
    ```

2.  クラスター構成を変更し、クラスターを PD マイクロサービス モードに切り替えます。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    `pd_mode: ms`に`global`加算します:

    ```ini
    global:
      user: tidb
       ssh_port: 22
       listen_host: 0.0.0.0
       deploy_dir: /tidb-deploy
       data_dir: /tidb-data
       os: linux
       arch: amd64
       systemd_mode: system
       pd_mode: ms
    ```

3.  PD ノード構成のローリング アップデートを実行します。

    ```shell
    tiup cluster reload <cluster-name> -R pd
    ```

    > **注記：**
    >
    > 前の`reload`コマンドを実行した後、PD タイムスタンプ割り当てサービスは利用できなくなりますが、次のステップの`scale-out`コマンドの実行が完了すると再び利用できるようになります。

4.  `scale-out`コマンドを実行して PD マイクロサービス ノードを追加します。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

### マイクロサービスモードから通常モードに切り替える {#switch-from-microservices-mode-to-regular-mode}

PD マイクロサービスが有効になっているクラスター (IP アドレス`10.0.1.8`に TSO ノードがあり、IP アドレス`10.0.1.9`にスケジューリング ノードがあると想定) の場合は、次のように非マイクロサービス モードに切り替えることができます。

1.  クラスター構成を変更し、クラスターを非マイクロサービス モードに切り替えます。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

    `global`から`pd_mode: ms`削除します:

    ```ini
    global:
      user: tidb
       ssh_port: 22
       listen_host: 0.0.0.0
       deploy_dir: /tidb-deploy
       data_dir: /tidb-data
       os: linux
       arch: amd64
       systemd_mode: system
    ```

2.  `scale-in`コマンドを実行して、すべての PD マイクロサービス ノードを削除します。

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.8:3379,10.0.1.9:3379
    ```

    > **注記：**
    >
    > 前の`scale-in`コマンドを実行した後、PD タイムスタンプ割り当てサービスは利用できなくなりますが、次のステップの`reload`コマンドの実行が完了すると再び利用できるようになります。

3.  PD ノード構成のローリング アップデートを実行します。

    ```shell
    tiup cluster reload <cluster-name> -R pd
    ```
