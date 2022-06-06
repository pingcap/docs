---
title: Scale the TiDB Cluster Using TiUP
summary: Learn how to scale the TiDB cluster using TiUP.
---

# TiUPを使用してTiDBクラスターをスケーリングする {#scale-the-tidb-cluster-using-tiup}

TiDBクラスタの容量は、オンラインサービスを中断することなく増減できます。

このドキュメントでは、TiUPを使用してTiDB、TiKV、PD、TiCDC、またはTiFlashクラスタをスケーリングする方法について説明します。 TiUPをインストールしていない場合は、 [制御マシンにTiUPをインストールします](/production-deployment-using-tiup.md#step-2-install-tiup-on-the-control-machine)の手順を参照してください。

現在のクラスタ名リストを表示するには、 `tiup cluster list`を実行します。

たとえば、クラスタの元のトポロジが次の場合です。

| ホストIP    | サービス           |
| :------- | :------------- |
| 10.0.1.3 | TiDB + TiFlash |
| 10.0.1.4 | TiDB + PD      |
| 10.0.1.5 | TiKV+モニター      |
| 10.0.1.1 | TiKV           |
| 10.0.1.2 | TiKV           |

## TiDB / PD/TiKVクラスタをスケールアウトする {#scale-out-a-tidb-pd-tikv-cluster}

`10.0.1.5`のホストにTiDBノードを追加する場合は、次の手順を実行します。

> **ノート：**
>
> 同様の手順でPDノードを追加できます。 TiKVノードを追加する前に、クラスタの負荷に応じてPDスケジューリングパラメーターを事前に調整することをお勧めします。

1.  スケールアウトトポロジを構成します。

    > **ノート：**
    >
    > -   デフォルトでは、ポートとディレクトリの情報は必要ありません。
    > -   1台のマシンに複数のインスタンスがデプロイされている場合は、それらに異なるポートとディレクトリを割り当てる必要があります。ポートまたはディレクトリに競合がある場合は、展開またはスケーリング中に通知を受け取ります。
    > -   TiUP v1.0.0以降、スケールアウト構成は元のクラスタのグローバル構成を継承します。

    `scale-out.yaml`のファイルにスケールアウトトポロジ構成を追加します。

    {{< copyable "" >}}

    ```shell
    vi scale-out.yaml
    ```

    {{< copyable "" >}}

    ```ini
    tidb_servers:
    - host: 10.0.1.5
      ssh_port: 22
      port: 4000
      status_port: 10080
      deploy_dir: /data/deploy/install/deploy/tidb-4000
      log_dir: /data/deploy/install/log/tidb-4000
    ```

    TiKV構成ファイルテンプレートは次のとおりです。

    {{< copyable "" >}}

    ```ini
    tikv_servers:
    - host: 10.0.1.5
      ssh_port: 22
      port: 20160
      status_port: 20180
      deploy_dir: /data/deploy/install/deploy/tikv-20160
      data_dir: /data/deploy/install/data/tikv-20160
      log_dir: /data/deploy/install/log/tikv-20160
    ```

    PD構成ファイルテンプレートは次のとおりです。

    {{< copyable "" >}}

    ```ini
    pd_servers:
    - host: 10.0.1.5
      ssh_port: 22
      name: pd-1
      client_port: 2379
      peer_port: 2380
      deploy_dir: /data/deploy/install/deploy/pd-2379
      data_dir: /data/deploy/install/data/pd-2379
      log_dir: /data/deploy/install/log/pd-2379
    ```

    現在のクラスタの構成を表示するには、 `tiup cluster edit-config <cluster-name>`を実行します。 `global`と`server_configs`のパラメータ設定は`scale-out.yaml`に継承され、 `scale-out.yaml`でも有効になるためです。

    構成後、クラスタの現在のトポロジーは次のようになります。

    | ホストIP    | サービス                |
    | :------- | :------------------ |
    | 10.0.1.3 | TiDB + TiFlash      |
    | 10.0.1.4 | TiDB + PD           |
    | 10.0.1.5 | **TiDB** +TiKV+モニター |
    | 10.0.1.1 | TiKV                |
    | 10.0.1.2 | TiKV                |

2.  scale-outコマンドを実行します。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

    > **ノート：**
    >
    > 上記のコマンドは、ユーザーがコマンドと新しいマシンを実行するための相互信頼が構成されていることを前提としています。相互信頼を設定できない場合は、 `-p`オプションを使用して新しいマシンのパスワードを入力するか、 `-i`オプションを使用して秘密鍵ファイルを指定します。

    `Scaled cluster <cluster-name> out successfully`が表示されている場合、スケールアウト操作は正常に完了しています。

3.  クラスタのステータスを確認します。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して監視プラットフォーム[http://10.0.1.5:3000](http://10.0.1.5:3000)にアクセスし、クラスタと新しいノードのステータスを監視します。

スケールアウト後のクラスタトポロジは次のとおりです。

| ホストIP    | サービス                |
| :------- | :------------------ |
| 10.0.1.3 | TiDB + TiFlash      |
| 10.0.1.4 | TiDB + PD           |
| 10.0.1.5 | **TiDB** +TiKV+モニター |
| 10.0.1.1 | TiKV                |
| 10.0.1.2 | TiKV                |

## TiFlashクラスタをスケールアウトする {#scale-out-a-tiflash-cluster}

`10.0.1.4`のホストにTiFlashノードを追加する場合は、次の手順を実行します。

> **ノート：**
>
> TiFlashノードを既存のTiDBクラスタに追加するときは、次の点に注意する必要があります。
>
> 1.  現在のTiDBバージョンがTiFlashの使用をサポートしていることを確認します。それ以外の場合は、TiDBクラスタをv5.0以降のバージョンにアップグレードします。
> 2.  `tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> config set enable-placement-rules true`コマンドを実行して、配置ルール機能を有効にします。または、 [pd-ctl](/pd-control.md)で対応するコマンドを実行します。

1.  ノード情報を`scale-out.yaml`のファイルに追加します。

    `scale-out.yaml`のファイルを作成して、TiFlashノード情報を追加します。

    {{< copyable "" >}}

    ```ini
    tiflash_servers:
      - host: 10.0.1.4
    ```

    現在、IPのみを追加できますが、ドメイン名は追加できません。

2.  scale-outコマンドを実行します。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

    > **ノート：**
    >
    > 上記のコマンドは、ユーザーがコマンドと新しいマシンを実行するための相互信頼が構成されていることを前提としています。相互信頼を設定できない場合は、 `-p`オプションを使用して新しいマシンのパスワードを入力するか、 `-i`オプションを使用して秘密鍵ファイルを指定します。

3.  クラスタステータスを表示します。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスタと新しいノードのステータスを表示します。

スケールアウト後のクラスタトポロジは次のとおりです。

| ホストIP    | サービス                    |
| :------- | :---------------------- |
| 10.0.1.3 | TiDB + TiFlash          |
| 10.0.1.4 | TiDB + PD + **TiFlash** |
| 10.0.1.5 | TiDB +TiKV+モニター         |
| 10.0.1.1 | TiKV                    |
| 10.0.1.2 | TiKV                    |

## TiCDCクラスタをスケールアウトする {#scale-out-a-ticdc-cluster}

`10.0.1.3`つおよび`10.0.1.4`のホストに2つのTiCDCノードを追加する場合は、次の手順を実行します。

1.  ノード情報を`scale-out.yaml`のファイルに追加します。

    `scale-out.yaml`のファイルを作成して、TiCDCノード情報を追加します。

    {{< copyable "" >}}

    ```ini
    cdc_servers:
      - host: 10.0.1.3
        gc-ttl: 86400
        data_dir: /data/deploy/install/data/cdc-8300
      - host: 10.0.1.4
        gc-ttl: 86400
        data_dir: /data/deploy/install/data/cdc-8300
    ```

2.  scale-outコマンドを実行します。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yaml
    ```

    > **ノート：**
    >
    > 上記のコマンドは、ユーザーがコマンドと新しいマシンを実行するための相互信頼が構成されていることを前提としています。相互信頼を設定できない場合は、 `-p`オプションを使用して新しいマシンのパスワードを入力するか、 `-i`オプションを使用して秘密鍵ファイルを指定します。

3.  クラスタステータスを表示します。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスタと新しいノードのステータスを表示します。

スケールアウト後のクラスタトポロジは次のとおりです。

| ホストIP    | サービス                            |
| :------- | :------------------------------ |
| 10.0.1.3 | TiDB + TiFlash + **TiCDC**      |
| 10.0.1.4 | TiDB + PD + TiFlash + **TiCDC** |
| 10.0.1.5 | TiDB +TiKV+モニター                 |
| 10.0.1.1 | TiKV                            |
| 10.0.1.2 | TiKV                            |

## TiDB / PD/TiKVクラスタでのスケーリング {#scale-in-a-tidb-pd-tikv-cluster}

`10.0.1.5`のホストからTiKVノードを削除する場合は、次の手順を実行します。

> **ノート：**
>
> -   同様の手順を実行して、TiDBおよびPDノードを削除できます。
> -   TiKV、TiFlash、およびTiDB Binlogコンポーネントは非同期でオフラインになり、停止プロセスに長い時間がかかるため、TiUPはさまざまな方法でそれらをオフラインにします。詳細については、 [コンポーネントのオフラインプロセスの特定の処理](/tiup/tiup-component-cluster-scale-in.md#particular-handling-of-components-offline-process)を参照してください。

> **ノート：**
>
> TiKVのPDクライアントは、PDノードのリストをキャッシュします。 TiKVの現在のバージョンには、PDノードを自動的かつ定期的に更新するメカニズムがあり、TiKVによってキャッシュされたPDノードの期限切れリストの問題を軽減するのに役立ちます。ただし、PDをスケールアウトした後は、スケールアウトの前に存在するすべてのPDノードを一度に直接削除しないようにする必要があります。必要に応じて、既存のすべてのPDノードをオフラインにする前に、PDリーダーを新しく追加されたPDノードに切り替えてください。

1.  ノードID情報を表示します。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ```
    Starting /root/.tiup/components/cluster/v1.9.0/cluster display <cluster-name>
    TiDB Cluster: <cluster-name>
    TiDB Version: v5.4.1
    ID              Role         Host        Ports                            Status  Data Dir                Deploy Dir
    --              ----         ----        -----                            ------  --------                ----------
    10.0.1.3:8300   cdc          10.0.1.3    8300                             Up      data/cdc-8300           deploy/cdc-8300
    10.0.1.4:8300   cdc          10.0.1.4    8300                             Up      data/cdc-8300           deploy/cdc-8300
    10.0.1.4:2379   pd           10.0.1.4    2379/2380                        Healthy data/pd-2379            deploy/pd-2379
    10.0.1.1:20160  tikv         10.0.1.1    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
    10.0.1.2:20160  tikv         10.0.1.2    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
    10.0.1.5:20160  tikv         10.0.1.5    20160/20180                      Up      data/tikv-20160         deploy/tikv-20160
    10.0.1.3:4000   tidb         10.0.1.3    4000/10080                       Up      -                       deploy/tidb-4000
    10.0.1.4:4000   tidb         10.0.1.4    4000/10080                       Up      -                       deploy/tidb-4000
    10.0.1.5:4000   tidb         10.0.1.5    4000/10080                       Up      -                       deploy/tidb-4000
    10.0.1.3:9000   tiflash      10.0.1.3    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000
    10.0.1.4:9000   tiflash      10.0.1.4    9000/8123/3930/20170/20292/8234  Up      data/tiflash-9000       deploy/tiflash-9000
    10.0.1.5:9090   prometheus   10.0.1.5    9090                             Up      data/prometheus-9090    deploy/prometheus-9090
    10.0.1.5:3000   grafana      10.0.1.5    3000                             Up      -                       deploy/grafana-3000
    10.0.1.5:9093   alertmanager 10.0.1.5    9093/9294                        Up      data/alertmanager-9093  deploy/alertmanager-9093
    ```

2.  スケールインコマンドを実行します。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.5:20160
    ```

    `--node`パラメーターは、オフラインにするノードのIDです。

    `Scaled cluster <cluster-name> in successfully`が表示されている場合、スケールイン操作は正常に完了しています。

3.  クラスタのステータスを確認します。

    スケールインプロセスには時間がかかります。スケールインするノードのステータスが`Tombstone`になった場合は、スケールイン操作が成功したことを意味します。

    スケールインステータスを確認するには、次のコマンドを実行します。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスタのステータスを表示します。

現在のトポロジは次のとおりです。

| ホストIP    | サービス                        |
| :------- | :-------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC      |
| 10.0.1.4 | TiDB + PD + TiFlash + TiCDC |
| 10.0.1.5 | TiDB +モニター**（TiKVは削除されます）** |
| 10.0.1.1 | TiKV                        |
| 10.0.1.2 | TiKV                        |

## TiFlashクラスタでのスケーリング {#scale-in-a-tiflash-cluster}

`10.0.1.4`のホストからTiFlashノードを削除する場合は、次の手順を実行します。

### 1.残りのTiFlashノードの数に応じて、テーブルのレプリカの数を調整します {#1-adjust-the-number-of-replicas-of-the-tables-according-to-the-number-of-remaining-tiflash-nodes}

ノードがダウンする前に、TiFlashクラスタの残りのノードの数がすべてのテーブルのレプリカの最大数以上であることを確認してください。それ以外の場合は、関連するテーブルのTiFlashレプリカの数を変更します。

1.  レプリカがクラスタの残りのTiFlashノードの数よりも大きいすべてのテーブルに対して、TiDBクライアントで次のコマンドを実行します。

    {{< copyable "" >}}

    ```sql
    alter table <db-name>.<table-name> set tiflash replica 0;
    ```

2.  関連するテーブルのTiFlashレプリカが削除されるのを待ちます。 [テーブルの複製の進行状況を確認する](/tiflash/use-tiflash.md#check-replication-progress)であり、関連するテーブルのレプリケーション情報が見つからない場合、レプリカは削除されます。

### 2.スケールイン操作を実行します {#2-perform-the-scale-in-operation}

次に、次のいずれかの解決策を使用してスケールイン操作を実行します。

#### 解決策1：TiUPを使用してTiFlashノードを削除する {#solution-1-use-tiup-to-remove-a-tiflash-node}

1.  まず、削除するノードの名前を確認します。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

2.  TiFlashノードを削除します（ステップ1のノード名が`10.0.1.4:9000`であると想定します）。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
    ```

#### 解決策2：TiFlashノードを手動で削除する {#solution-2-manually-remove-a-tiflash-node}

特別な場合（ノードを強制的に停止する必要がある場合など）、またはTiUPスケールイン操作が失敗した場合は、次の手順でTiFlashノードを手動で削除できます。

1.  pd-ctlのstoreコマンドを使用して、このTiFlashノードに対応するストアIDを表示します。

    -   [pd-ctl](/pd-control.md)にstoreコマンドを入力します（バイナリファイルはtidb-ansibleディレクトリの`resources/bin`未満です）。

    -   TiUPデプロイメントを使用する場合は、 `pd-ctl`を`tiup ctl pd`に置き換えます。

        {{< copyable "" >}}

        ```shell
        tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> store
        ```

        > **ノート：**
        >
        > クラスタに複数のPDインスタンスが存在する場合は、上記のコマンドでアクティブなPDインスタンスのIPアドレス：ポートを指定するだけで済みます。

2.  pd-ctlでTiFlashノードを削除します。

    -   pd-ctlに`store delete <store_id>`を入力します（ `<store_id>`は、前の手順で見つかったTiFlashノードのストアIDです。

    -   TiUPデプロイメントを使用する場合は、 `pd-ctl`を`tiup ctl pd`に置き換えます。

        {{< copyable "" >}}

        ```shell
        tiup ctl:<cluster-version> pd -u http://<pd_ip>:<pd_port> store delete <store_id>
        ```

        > **ノート：**
        >
        > クラスタに複数のPDインスタンスが存在する場合は、上記のコマンドでアクティブなPDインスタンスのIPアドレス：ポートを指定するだけで済みます。

3.  TiFlashプロセスを停止する前に、TiFlashノードのストアが消えるのを待つか、 `state_name`が`Tombstone`になるのを待ちます。

4.  TiFlashデータファイルを手動で削除します（その場所は、クラスタトポロジファイルのTiFlash構成の下の`data_dir`ディレクトリにあります）。

5.  TiUPのクラスタ構成ファイルを手動で更新します（編集モードでダウンするTiFlashノードの情報を削除します）。

    {{< copyable "" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

> **ノート：**
>
> クラスタのすべてのTiFlashノードの実行を停止する前に、TiFlashにレプリケートされたすべてのテーブルがキャンセルされない場合は、PDのレプリケーションルールを手動でクリーンアップする必要があります。そうしないと、TiFlashノードを正常に停止できません。

PDのレプリケーションルールを手動でクリーンアップする手順は次のとおりです。

1.  現在のPDインスタンスのTiFlashに関連するすべてのデータレプリケーションルールを表示します。

    {{< copyable "" >}}

    ```shell
    curl http://<pd_ip>:<pd_port>/pd/api/v1/config/rules/group/tiflash
    ```

    ```
    [
      {
        "group_id": "tiflash",
        "id": "table-45-r",
        "override": true,
        "start_key": "7480000000000000FF2D5F720000000000FA",
        "end_key": "7480000000000000FF2E00000000000000F8",
        "role": "learner",
        "count": 1,
        "label_constraints": [
          {
            "key": "engine",
            "op": "in",
            "values": [
              "tiflash"
            ]
          }
        ]
      }
    ]
    ```

2.  TiFlashに関連するすべてのデータ複製ルールを削除します。例として、 `id`が`table-45-r`であるルールを取り上げます。次のコマンドで削除します。

    {{< copyable "" >}}

    ```shell
    curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
    ```

## TiCDCクラスタでのスケーリング {#scale-in-a-ticdc-cluster}

`10.0.1.4`のホストからTiCDCノードを削除する場合は、次の手順を実行します。

1.  ノードをオフラインにします。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
    ```

2.  クラスタステータスを表示します。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスタのステータスを表示します。

現在のトポロジは次のとおりです。

| ホストIP    | サービス                           |
| :------- | :----------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC         |
| 10.0.1.4 | TiDB + PD + **（TiCDCは削除されます）** |
| 10.0.1.5 | TiDB+モニター                      |
| 10.0.1.1 | TiKV                           |
| 10.0.1.2 | TiKV                           |
