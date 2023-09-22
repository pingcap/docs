---
title: Scale a TiDB Cluster Using TiUP
summary: Learn how to scale the TiDB cluster using TiUP.
---

# TiUPを使用して TiDBクラスタをスケールする {#scale-a-tidb-cluster-using-tiup}

TiDB クラスターの容量は、オンライン サービスを中断することなく増減できます。

このドキュメントでは、 TiUPを使用して TiDB、TiKV、PD、TiCDC、またはTiFlashクラスターをスケーリングする方法について説明します。 TiUPをインストールしていない場合は、 [ステップ 2. 制御マシンにTiUPをデプロイ](/production-deployment-using-tiup.md#step-2-deploy-tiup-on-the-control-machine)の手順を参照してください。

現在のクラスター名のリストを表示するには、 `tiup cluster list`を実行します。

たとえば、クラスターの元のトポロジが次のとおりであるとします。

| ホストIP    | サービス           |
| :------- | :------------- |
| 10.0.1.3 | TiDB + TiFlash |
| 10.0.1.4 | TiDB + PD      |
| 10.0.1.5 | TiKV+モニター      |
| 10.0.1.1 | TiKV           |
| 10.0.1.2 | TiKV           |

## TiDB/PD/TiKV クラスターをスケールアウトする {#scale-out-a-tidb-pd-tikv-cluster}

このセクションでは、TiDB ノードを`10.0.1.5`ホストに追加する方法を例に説明します。

> **注記：**
>
> 同様の手順を実行して PD ノードを追加できます。 TiKV ノードを追加する前に、クラスターの負荷に応じて PD スケジューリング パラメーターを事前に調整することをお勧めします。

1.  スケールアウト トポロジを構成します。

    > **注記：**
    >
    > -   デフォルトでは、ポートとディレクトリの情報は必要ありません。
    > -   複数のインスタンスが 1 台のマシンにデプロイされている場合は、それらに異なるポートとディレクトリを割り当てる必要があります。ポートまたはディレクトリに競合がある場合は、展開またはスケーリング中に通知を受け取ります。
    > -   TiUP v1.0.0 以降、スケールアウト構成は元のクラスターのグローバル構成を継承します。

    スケールアウト トポロジ構成を`scale-out.yml`ファイルに追加します。

    ```shell
    vi scale-out.yml
    ```

    ```ini
    tidb_servers:
    - host: 10.0.1.5
      ssh_port: 22
      port: 4000
      status_port: 10080
      deploy_dir: /tidb-deploy/tidb-4000
      log_dir: /tidb-deploy/tidb-4000/log
    ```

    TiKV 構成ファイルのテンプレートは次のとおりです。

    ```ini
    tikv_servers:
    - host: 10.0.1.5
      ssh_port: 22
      port: 20160
      status_port: 20180
      deploy_dir: /tidb-deploy/tikv-20160
      data_dir: /tidb-data/tikv-20160
      log_dir: /tidb-deploy/tikv-20160/log
    ```

    PD 構成ファイルのテンプレートは次のとおりです。

    ```ini
    pd_servers:
    - host: 10.0.1.5
      ssh_port: 22
      name: pd-1
      client_port: 2379
      peer_port: 2380
      deploy_dir: /tidb-deploy/pd-2379
      data_dir: /tidb-data/pd-2379
      log_dir: /tidb-deploy/pd-2379/log
    ```

    現在のクラスターの構成を表示するには、 `tiup cluster edit-config <cluster-name>`を実行します。 `global`と`server_configs`のパラメータ設定は`scale-out.yml`に継承され、 `scale-out.yml`にも反映されるためです。

2.  スケールアウト コマンドを実行します。

    `scale-out`コマンドを実行する前に、 `check`と`check --apply`のコマンドを使用して、クラスター内の潜在的なリスクを検出し、自動的に修復します。

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

    前述のコマンドでは次のようになります。

    -   `scale-out.yml`はスケールアウト構成ファイルです。
    -   `--user root`クラスターのスケールアウトを完了するために`root`ユーザーとしてターゲット マシンにログインすることを示します。 `root`ユーザーは、ターゲット マシンに対する`ssh`および`sudo`権限を持つことが期待されます。あるいは、 `ssh`および`sudo`権限を持つ他のユーザーを使用して展開を完了することもできます。
    -   `[-i]`と`[-p]`はオプションです。パスワードなしでターゲット マシンへのログインを設定した場合、これらのパラメータは必要ありません。そうでない場合は、2 つのパラメータのいずれかを選択します。 `[-i]`は、ターゲット マシンにアクセスできる root ユーザー (または`--user`で指定された他のユーザー) の秘密キーです。 `[-p]`は、ユーザーのパスワードを対話的に入力するために使用されます。

    `Scaled cluster <cluster-name> out successfully`が表示されれば、スケールアウト操作は成功しています。

3.  クラスターのステータスを確認します。

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスターと新しいノードのステータスを監視します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホストIP    | サービス                   |
| :------- | :--------------------- |
| 10.0.1.3 | TiDB + TiFlash         |
| 10.0.1.4 | TiDB + PD              |
| 10.0.1.5 | **TiDB** + TiKV + モニター |
| 10.0.1.1 | TiKV                   |
| 10.0.1.2 | TiKV                   |

## TiFlashクラスターをスケールアウトする {#scale-out-a-tiflash-cluster}

このセクションでは、 TiFlashノードを`10.0.1.4`ホストに追加する方法を例に説明します。

> **注記：**
>
> TiFlashノードを既存の TiDB クラスターに追加する場合は、次の点に注意してください。
>
> -   現在の TiDB バージョンがTiFlashの使用をサポートしていることを確認します。それ以外の場合は、TiDB クラスターを v5.0 以降のバージョンにアップグレードします。
> -   `tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> config set enable-placement-rules true`コマンドを実行して、配置ルール機能を有効にします。または、 [PD-CTL](/pd-control.md)で対応するコマンドを実行します。

1.  ノード情報を`scale-out.yml`ファイルに追加します。

    TiFlashノード情報を追加する`scale-out.yml`ファイルを作成します。

    ```ini
    tiflash_servers:
    - host: 10.0.1.4
    ```

    現在、追加できるのは IP アドレスのみで、ドメイン名は追加できません。

2.  スケールアウト コマンドを実行します。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

    > **注記：**
    >
    > 前述のコマンドは、ユーザーがコマンドと新しいマシンを実行できるように相互信頼が構成されているという前提に基づいています。相互信頼を構成できない場合は、 `-p`オプションを使用して新しいマシンのパスワードを入力するか、 `-i`オプションを使用して秘密キー ファイルを指定します。

3.  クラスターのステータスをビュー。

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)監視プラットフォームにアクセスし、クラスターと新しいノードのステータスを表示します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホストIP    | サービス                    |
| :------- | :---------------------- |
| 10.0.1.3 | TiDB + TiFlash          |
| 10.0.1.4 | TiDB + PD + **TiFlash** |
| 10.0.1.5 | TiDB+ TiKV+ モニター        |
| 10.0.1.1 | TiKV                    |
| 10.0.1.2 | TiKV                    |

## TiCDC クラスターをスケールアウトする {#scale-out-a-ticdc-cluster}

このセクションでは、2 つの TiCDC ノードをホスト`10.0.1.3`とホスト`10.0.1.4`に追加する方法を例に示します。

1.  ノード情報を`scale-out.yml`ファイルに追加します。

    TiCDC ノード情報を追加する`scale-out.yml`ファイルを作成します。

    ```ini
    cdc_servers:
      - host: 10.0.1.3
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
      - host: 10.0.1.4
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
    ```

2.  スケールアウト コマンドを実行します。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

    > **注記：**
    >
    > 前述のコマンドは、ユーザーがコマンドと新しいマシンを実行できるように相互信頼が構成されているという前提に基づいています。相互信頼を構成できない場合は、 `-p`オプションを使用して新しいマシンのパスワードを入力するか、 `-i`オプションを使用して秘密キー ファイルを指定します。

3.  クラスターのステータスをビュー。

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)監視プラットフォームにアクセスし、クラスターと新しいノードのステータスを表示します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホストIP    | サービス                            |
| :------- | :------------------------------ |
| 10.0.1.3 | TiDB + TiFlash + **TiCDC**      |
| 10.0.1.4 | TiDB + PD + TiFlash + **TiCDC** |
| 10.0.1.5 | TiDB+ TiKV+ モニター                |
| 10.0.1.1 | TiKV                            |
| 10.0.1.2 | TiKV                            |

## TiDB/PD/TiKV クラスターでのスケールイン {#scale-in-a-tidb-pd-tikv-cluster}

このセクションでは、 `10.0.1.5`ホストから TiKV ノードを削除する方法を例に示します。

> **注記：**
>
> -   同様の手順を実行して、TiDB または PD ノードを削除できます。
> -   TiKV、 TiFlash、および TiDB Binlogコンポーネントは非同期でオフラインになり、停止プロセスに時間がかかるため、 TiUPはさまざまな方法でこれらをオフラインにします。詳細は[コンポーネントのオフラインプロセスの特別な処理](/tiup/tiup-component-cluster-scale-in.md#particular-handling-of-components-offline-process)を参照してください。
> -   TiKV の PD クライアントは、PD ノードのリストをキャッシュします。 TiKV の現在のバージョンには、PD ノードを自動的かつ定期的に更新するメカニズムがあり、TiKV によってキャッシュされた PD ノードの期限切れリストの問題を軽減するのに役立ちます。ただし、PD をスケールアウトした後は、スケーリング前に存在していたすべての PD ノードを一度に直接削除しないようにする必要があります。必要に応じて、既存のすべての PD ノードをオフラインにする前に、必ず PD リーダーを新しく追加した PD ノードに切り替えてください。

1.  ノード ID 情報をビュー。

    ```shell
    tiup cluster display <cluster-name>
    ```

        Starting /root/.tiup/components/cluster/v1.11.3/cluster display <cluster-name>
        TiDB Cluster: <cluster-name>
        TiDB Version: v7.1.1
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

2.  スケールイン コマンドを実行します。

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.5:20160
    ```

    `--node`パラメータは、オフラインにするノードの ID です。

    `Scaled cluster <cluster-name> in successfully`が表示されれば、スケールイン操作は成功します。

3.  クラスターのステータスを確認します。

    スケールインプロセスには時間がかかります。次のコマンドを実行して、スケールインのステータスを確認できます。

    ```shell
    tiup cluster display <cluster-name>
    ```

    スケールインするノードが`Tombstone`になれば、スケールイン操作は成功します。

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスターのステータスを表示します。

現在のトポロジは次のとおりです。

| ホストIP    | サービス                          |
| :------- | :---------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC        |
| 10.0.1.4 | TiDB + PD + TiFlash + TiCDC   |
| 10.0.1.5 | TiDB + モニター**(TiKV は削除されます)** |
| 10.0.1.1 | TiKV                          |
| 10.0.1.2 | TiKV                          |

## TiFlashクラスターでのスケールイン {#scale-in-a-tiflash-cluster}

このセクションでは、 `10.0.1.4`ホストからTiFlashノードを削除する方法を例に示します。

### 1. 残りのTiFlashノードの数に応じて、テーブルのレプリカの数を調整します。 {#1-adjust-the-number-of-replicas-of-the-tables-according-to-the-number-of-remaining-tiflash-nodes}

1.  スケールイン後に、テーブルにTiFlashノードの数を超えるTiFlashレプリカがあるかどうかをクエリします。 `tobe_left_nodes`スケールイン後のTiFlashノードの数を意味します。クエリ結果が空の場合は、 TiFlashでスケーリングを開始できます。クエリ結果が空でない場合は、関連テーブルのTiFlashレプリカの数を変更する必要があります。

    ```sql
    SELECT * FROM information_schema.tiflash_replica WHERE REPLICA_COUNT >  'tobe_left_nodes';
    ```

2.  スケールイン後、 TiFlashノードの数を超えるTiFlashレプリカを持つすべてのテーブルに対して次のステートメントを実行します。 `new_replica_num` `tobe_left_nodes`以下でなければなりません。

    ```sql
    ALTER TABLE <db-name>.<table-name> SET tiflash replica 'new_replica_num';
    ```

3.  手順 1 を再度実行し、スケールイン後にTiFlashノードの数を超えるTiFlashレプリカを含むテーブルがないことを確認します。

### 2. スケールイン操作を実行する {#2-perform-the-scale-in-operation}

次のいずれかのソリューションを使用してスケールイン操作を実行します。

#### 解決策 1. TiUP を使用してTiFlashノードを削除する {#solution-1-use-tiup-to-remove-a-tiflash-node}

1.  削除するノードの名前を確認します。

    ```shell
    tiup cluster display <cluster-name>
    ```

2.  TiFlashノードを削除します (ステップ 1 のノード名が`10.0.1.4:9000`であると仮定します)。

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
    ```

#### 解決策 2. TiFlashノードを手動で削除する {#solution-2-manually-remove-a-tiflash-node}

特殊な場合 (ノードを強制的に停止する必要がある場合など)、またはTiUPスケールイン操作が失敗した場合は、次の手順でTiFlashノードを手動で削除できます。

1.  pd-ctlのstoreコマンドを使用して、このTiFlashノードに対応するストアIDを表示します。

    -   [PD-CTL](/pd-control.md)に store コマンドを入力します (バイナリ ファイルは tidb-ansible ディレクトリの`resources/bin`の下にあります)。

    -   TiUPデプロイメントを使用する場合は、 `pd-ctl` `tiup ctl:v<CLUSTER_VERSION> pd`に置き換えます。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> store
    ```

    > **注記：**
    >
    > クラスター内に複数の PD インスタンスが存在する場合、上記のコマンドでアクティブな PD インスタンスの IP アドレス:ポートを指定するだけで済みます。

2.  pd-ctl でTiFlashノードを削除します。

    -   pd-ctl に`store delete <store_id>`入力します ( `<store_id>`は、前の手順で見つかったTiFlashノードのストア ID です)。

    -   TiUPデプロイメントを使用する場合は、 `pd-ctl` `tiup ctl:v<CLUSTER_VERSION> pd`に置き換えます。

        ```shell
        tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> store delete <store_id>
        ```

    > **注記：**
    >
    > クラスター内に複数の PD インスタンスが存在する場合、上記のコマンドでアクティブな PD インスタンスの IP アドレス:ポートを指定するだけで済みます。

3.  TiFlashノードのストアが消えるか、 `state_name`が`Tombstone`になるまで待ってから、 TiFlashプロセスを停止します。

4.  TiFlashデータ ファイルを手動で削除します (場所は、クラスター トポロジ ファイルのTiFlash構成の下の`data_dir`ディレクトリにあります)。

5.  次のコマンドを使用して、クラスター トポロジからダウンしたTiFlashノードに関する情報を削除します。

    ```shell
    tiup cluster scale-in <cluster-name> --node <pd_ip>:<pd_port> --force
    ```

> **注記：**
>
> クラスター内のすべてのTiFlashノードの実行が停止する前に、 TiFlashにレプリケートされたすべてのテーブルがキャンセルされていない場合は、PD のレプリケーション ルールを手動でクリーンアップする必要があります。そうしないと、 TiFlashノードは正常にダウンできません。

PD のレプリケーション ルールを手動でクリーンアップする手順は次のとおりです。

1.  現在の PD インスタンスのTiFlashに関連するすべてのデータ レプリケーション ルールをビュー。

    ```shell
    curl http://<pd_ip>:<pd_port>/pd/api/v1/config/rules/group/tiflash
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

2.  TiFlashに関連するすべてのデータ複製ルールを削除します。例として、 `id`が`table-45-r`であるルールを考えてみましょう。次のコマンドで削除します。

    ```shell
    curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
    ```

3.  クラスターのステータスをビュー。

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)監視プラットフォームにアクセスし、クラスターと新しいノードのステータスを表示します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホストIP    | サービス                               |
| :------- | :--------------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC             |
| 10.0.1.4 | TiDB + PD + TiCDC **(TiFlashは削除)** |
| 10.0.1.5 | TiDB+ モニター                         |
| 10.0.1.1 | TiKV                               |
| 10.0.1.2 | TiKV                               |

## TiCDC クラスターでのスケールイン {#scale-in-a-ticdc-cluster}

このセクションでは、 `10.0.1.4`ホストから TiCDC ノードを削除する方法を例に示します。

1.  ノードをオフラインにします。

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
    ```

2.  クラスターのステータスをビュー。

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスターのステータスを表示します。

現在のトポロジは次のとおりです。

| ホストIP    | サービス                       |
| :------- | :------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC     |
| 10.0.1.4 | TiDB + PD + **(TiCDCは削除）** |
| 10.0.1.5 | TiDB + モニター                |
| 10.0.1.1 | TiKV                       |
| 10.0.1.2 | TiKV                       |
