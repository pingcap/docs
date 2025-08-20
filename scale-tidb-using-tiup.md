---
title: Scale a TiDB Cluster Using TiUP
summary: TiUPを使用して TiDB クラスターをスケーリングする方法を学びます。
---

# TiUPを使用して TiDBクラスタをスケールする {#scale-a-tidb-cluster-using-tiup}

TiDB クラスターの容量は、オンライン サービスを中断することなく増減できます。

このドキュメントでは、 TiUPを使用して TiDB、TiKV、PD、TiCDC、またはTiFlashクラスターをスケーリングする方法について説明します。TiUPをインストールしていない場合は、 [ステップ2. 制御マシンにTiUPをデプロイ](/production-deployment-using-tiup.md#step-2-deploy-tiup-on-the-control-machine)の手順を参照してください。

現在のクラスター名リストを表示するには、 `tiup cluster list`実行します。

たとえば、クラスターの元のトポロジが次のようになっているとします。

| ホストIP    | サービス           |
| :------- | :------------- |
| 10.0.1.3 | TiDB + TiFlash |
| 10.0.1.4 | TiDB + PD      |
| 10.0.1.5 | TiKV + モニター    |
| 10.0.1.1 | TiKV           |
| 10.0.1.2 | TiKV           |

## TiDB/PD/TiKV クラスターをスケールアウトする {#scale-out-a-tidb-pd-tikv-cluster}

このセクションでは、 `10.0.1.5`ホストに TiDB ノードを追加する方法を例示します。

> **注記：**
>
> PDノードを追加する場合も同様の手順で可能です。TiKVノードを追加する前に、クラスターの負荷に応じてPDスケジューリングパラメータを事前に調整することをお勧めします。

1.  スケールアウト トポロジを構成します。

    > **注記：**
    >
    > -   デフォルトでは、ポートとディレクトリの情報は必要ありません。
    > -   複数のインスタンスを単一のマシンにデプロイする場合は、それぞれに異なるポートとディレクトリを割り当てる必要があります。ポートまたはディレクトリが競合する場合は、デプロイまたはスケーリング中に通知が表示されます。
    > -   TiUP v1.0.0 以降、スケールアウト構成は元のクラスターのグローバル構成を継承します。

    `scale-out.yml`ファイルにスケールアウト トポロジ構成を追加します。

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

    TiKV 構成ファイル テンプレートは次のとおりです。

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

    PD 構成ファイル テンプレートは次のとおりです。

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

    現在のクラスターの構成を表示するには、 `tiup cluster edit-config <cluster-name>`実行します。 `global`と`server_configs`のパラメータ設定は`scale-out.yml`に継承されるため、 `scale-out.yml`でも有効になります。

2.  スケールアウト コマンドを実行します。

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
    -   `[-i]`と`[-p]`オプションです。ターゲットマシンへのログインをパスワードなしで設定している場合、これらのパラメータは不要です。そうでない場合は、2つのパラメータのいずれかを選択してください。4 `[-i]` 、ターゲットマシンにアクセスできるルートユーザー（または`--user`で指定された他のユーザー）の秘密鍵です。8 `[-p]` 、ユーザーパスワードを対話的に入力するために使用されます。

    `Scaled cluster <cluster-name> out successfully`表示された場合、スケールアウト操作は成功しています。

3.  クラスター構成を更新します。

    > **注記：**
    >
    > -   PDノードを追加した後のみ、クラスター構成の更新が必要です。TiDBノードまたはTiKVノードのみを追加する場合は、この手順をスキップしてください。
    > -   TiUP v1.15.0以降をご利用の場合は、この手順はTiUPが実行するのでスキップしてください。TiUP v1.15.0より前のバージョンをご利用の場合は、以下のサブ手順を実行してください。

    1.  クラスター構成を更新します。

        ```shell
        tiup cluster reload <cluster-name> --skip-restart
        ```

    2.  Prometheus の設定を更新し、Prometheus を再起動します。

        ```shell
        tiup cluster reload <cluster-name> -R prometheus
        ```

4.  クラスターのステータスを確認します。

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

## TiFlashクラスターのスケールアウト {#scale-out-a-tiflash-cluster}

このセクションでは、 TiFlashノードを`10.0.1.4`ホストに追加する方法を説明します。

> **注記：**
>
> 既存の TiDB クラスターにTiFlashノードを追加する場合は、次の点に注意してください。
>
> -   現在の TiDB バージョンがTiFlashの使用をサポートしていることを確認してください。サポートしていない場合は、TiDB クラスターを v5.0 以降のバージョンにアップグレードしてください。
> -   配置ルール機能を有効にするには、 `tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> config set enable-placement-rules true`コマンドを実行します。または、 [pd-ctl](/pd-control.md)の対応するコマンドを実行します。

1.  `scale-out.yml`ファイルにノード情報を追加します。

    TiFlashノード情報を追加する`scale-out.yml`ファイルを作成します。

    ```ini
    tiflash_servers:
    - host: 10.0.1.4
    ```

    現在、IP アドレスのみを追加でき、ドメイン名は追加できません。

2.  スケールアウト コマンドを実行します。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

    > **注記：**
    >
    > 上記のコマンドは、コマンドを実行するユーザーと新しいマシンの間で相互信頼が構築されていることを前提としています。相互信頼を構築できない場合は、 `-p`オプションを使用して新しいマシンのパスワードを入力するか、 `-i`オプションを使用して秘密鍵ファイルを指定します。

3.  クラスターのステータスをビュー。

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスターと新しいノードのステータスを表示します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホストIP    | サービス                    |
| :------- | :---------------------- |
| 10.0.1.3 | TiDB + TiFlash          |
| 10.0.1.4 | TiDB + PD + **TiFlash** |
| 10.0.1.5 | TiDB + TiKV + モニター      |
| 10.0.1.1 | TiKV                    |
| 10.0.1.2 | TiKV                    |

## TiCDC クラスターをスケールアウトする {#scale-out-a-ticdc-cluster}

このセクションでは、ホスト`10.0.1.3`と`10.0.1.4`に 2 つの TiCDC ノードを追加する方法を例で説明します。

1.  `scale-out.yml`ファイルにノード情報を追加します。

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
    > 上記のコマンドは、コマンドを実行するユーザーと新しいマシンの間で相互信頼が構築されていることを前提としています。相互信頼を構築できない場合は、 `-p`オプションを使用して新しいマシンのパスワードを入力するか、 `-i`オプションを使用して秘密鍵ファイルを指定します。

3.  クラスターのステータスをビュー。

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスターと新しいノードのステータスを表示します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホストIP    | サービス                            |
| :------- | :------------------------------ |
| 10.0.1.3 | TiDB + TiFlash + **TiCDC**      |
| 10.0.1.4 | TiDB + PD + TiFlash + **TiCDC** |
| 10.0.1.5 | TiDB + TiKV + モニター              |
| 10.0.1.1 | TiKV                            |
| 10.0.1.2 | TiKV                            |

## TiDB/PD/TiKV クラスターのスケールイン {#scale-in-a-tidb-pd-tikv-cluster}

このセクションでは、 `10.0.1.5`ホストから TiKV ノードを削除する方法を例示します。

> **注記：**
>
> -   同様の手順で TiDB ノードまたは PD ノードを削除できます。
> -   TiKVおよびTiFlashコンポーネントは非同期的にオフラインになり、停止処理に時間がかかるため、 TiUPはこれらのコンポーネントを別の方法でオフラインにします。詳細については、 [コンポーネントのオフラインプロセスの特別な処理](/tiup/tiup-component-cluster-scale-in.md#particular-handling-of-components-offline-process)参照してください。
> -   TiKVのPDクライアントは、PDノードのリストをキャッシュします。現在のバージョンのTiKVには、PDノードを自動的かつ定期的に更新するメカニズムが搭載されており、TiKVによってキャッシュされたPDノードのリストが期限切れになる問題を軽減するのに役立ちます。ただし、PDをスケールアウトした後は、スケールアウト前に存在していたすべてのPDノードを一度に削除することは避けてください。必要に応じて、既存のPDノードをすべてオフラインにする前に、PDリーダーを新しく追加されたPDノードに切り替えてください。

1.  ノード ID 情報をビュー。

    ```shell
    tiup cluster display <cluster-name>
    ```

        Starting /root/.tiup/components/cluster/v1.12.3/cluster display <cluster-name>
        TiDB Cluster: <cluster-name>
        TiDB Version: v8.5.3
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

    `Scaled cluster <cluster-name> in successfully`表示された場合、スケールイン操作は成功しています。

3.  クラスター構成を更新します。

    > **注記：**
    >
    > -   PDノードを削除した後のみ、クラスター構成の更新が必要です。TiDBノードまたはTiKVノードのみを削除する場合は、この手順をスキップしてください。
    > -   TiUP v1.15.0以降をご利用の場合は、この手順はTiUPが実行するのでスキップしてください。TiUP v1.15.0より前のバージョンをご利用の場合は、以下のサブ手順を実行してください。

    1.  クラスター構成を更新します。

        ```shell
        tiup cluster reload <cluster-name> --skip-restart
        ```

    2.  Prometheus の設定を更新し、Prometheus を再起動します。

        ```shell
        tiup cluster reload <cluster-name> -R prometheus
        ```

4.  クラスターのステータスを確認します。

    スケールイン処理には時間がかかります。スケールインのステータスを確認するには、次のコマンドを実行してください。

    ```shell
    tiup cluster display <cluster-name>
    ```

    スケールインするノードが`Tombstone`になると、スケールイン操作は成功します。

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスターのステータスを表示します。

現在のトポロジは次のとおりです。

| ホストIP    | サービス                        |
| :------- | :-------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC      |
| 10.0.1.4 | TiDB + PD + TiFlash + TiCDC |
| 10.0.1.5 | TiDB + モニター**（TiKVは削除）**    |
| 10.0.1.1 | TiKV                        |
| 10.0.1.2 | TiKV                        |

## TiFlashクラスターのスケールイン {#scale-in-a-tiflash-cluster}

このセクションでは、 `10.0.1.4`ホストからTiFlashノードを削除する方法を例で説明します。

### 1. 残りのTiFlashノードの数に応じてテーブルのレプリカ数を調整する {#1-adjust-the-number-of-replicas-of-the-tables-according-to-the-number-of-remaining-tiflash-nodes}

1.  スケールイン後のTiFlashノード数を超えるTiFlashレプリカを持つテーブルがあるかどうかを照会します。1 `tobe_left_nodes`スケールイン後のTiFlashノード数を意味します。クエリ結果が空の場合、 TiFlashのスケールインを開始できます。クエリ結果が空でない場合は、関連テーブルのTiFlashレプリカ数を変更する必要があります。

    ```sql
    SELECT * FROM information_schema.tiflash_replica WHERE REPLICA_COUNT >  'tobe_left_nodes';
    ```

2.  スケールイン後のTiFlashノードの数より多いTiFlashレプリカを持つすべてのテーブルに対して次のステートメントを実行します。1 `new_replica_num` `tobe_left_nodes`である必要があります。

    ```sql
    ALTER TABLE <db-name>.<table-name> SET tiflash replica 'new_replica_num';
    ```

    このステートメントを実行すると、TiDBはそれに応じてPD [配置ルール](/configure-placement-rules.md)変更または削除します。その後、PDは更新された配置ルールに基づいてデータをスケジュールします。

3.  手順 1 を再度実行し、スケールイン後のTiFlashノードの数を超えるTiFlashレプリカを持つテーブルがないことを確認します。

### 2. スケールイン操作を実行する {#2-perform-the-scale-in-operation}

次のいずれかのソリューションを使用してスケールイン操作を実行します。

#### 解決策1. TiUPを使用してTiFlashノードを削除する {#solution-1-use-tiup-to-remove-a-tiflash-node}

1.  削除するノードの名前を確認します。

    ```shell
    tiup cluster display <cluster-name>
    ```

2.  TiFlashノードを削除します (手順 1 のノード名は`10.0.1.4:9000`であると想定します)。

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
    ```

3.  削除されたTiFlashノードのステータスをビュー。

    ```shell
    tiup cluster display <cluster-name>
    ```

4.  削除されたTiFlashノードのステータスが`Tombstone`になったら、削除されたノードの情報をTiUPトポロジから削除します (TiUP は`Tombstone`ノードの関連データ ファイルを自動的にクリーンアップします)。

    ```shell
    tiup cluster prune <cluster-name>
    ```

#### 解決策2. TiFlashノードを手動で削除する {#solution-2-manually-remove-a-tiflash-node}

特別な場合 (ノードを強制的に停止する必要がある場合など)、またはTiUPスケールイン操作が失敗した場合は、次の手順に従ってTiFlashノードを手動で削除できます。

1.  このTiFlashノードに対応するストア ID を表示するには、pd-ctl の store コマンドを使用します。

    -   [pd-ctl](/pd-control.md)に store コマンドを入力します (バイナリ ファイルは tidb-ansible ディレクトリの`resources/bin`の下にあります)。

    -   TiUPデプロイメントを使用する場合は、 `pd-ctl` `tiup ctl:v<CLUSTER_VERSION> pd`に置き換えます。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> store
    ```

    > **注記：**
    >
    > クラスター内に複数の PD インスタンスが存在する場合は、上記のコマンドでアクティブな PD インスタンスの IP アドレス:ポートのみを指定する必要があります。

2.  pd-ctl でTiFlashノードを削除します。

    -   pd-ctl に`store delete <store_id>`入力します ( `<store_id>`前の手順で見つかったTiFlashノードのストア ID です)。

    -   TiUPデプロイメントを使用する場合は、 `pd-ctl` `tiup ctl:v<CLUSTER_VERSION> pd`に置き換えます。

        ```shell
        tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> store delete <store_id>
        ```

    > **注記：**
    >
    > クラスター内に複数の PD インスタンスが存在する場合は、上記のコマンドでアクティブな PD インスタンスの IP アドレス:ポートのみを指定する必要があります。

3.  TiFlashプロセスを停止する前に、 TiFlashノードのストアが消えるか、 `state_name` `Tombstone`になるまで待ちます。

4.  削除されたノードの情報をTiUPトポロジから削除します (TiUP は`Tombstone`ノードの関連データ ファイルを自動的にクリーンアップします)。

    ```shell
    tiup cluster prune <cluster-name>
    ```

### 3. クラスターのステータスをビュー {#3-view-the-cluster-status}

```shell
tiup cluster display <cluster-name>
```

ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスターと新しいノードのステータスを表示します。

スケーリング後のクラスター トポロジは次のようになります。

| ホストIP    | サービス                               |
| :------- | :--------------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC             |
| 10.0.1.4 | TiDB + PD + TiCDC **(TiFlashは削除)** |
| 10.0.1.5 | TiDB+モニター                          |
| 10.0.1.1 | TiKV                               |
| 10.0.1.2 | TiKV                               |

## TiCDC クラスターのスケールイン {#scale-in-a-ticdc-cluster}

このセクションでは、 `10.0.1.4`ホストから TiCDC ノードを削除する方法を例示します。

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
| 10.0.1.4 | TiDB + PD + **（TiCDCは削除）** |
| 10.0.1.5 | TiDB + モニター                |
| 10.0.1.1 | TiKV                       |
| 10.0.1.2 | TiKV                       |
