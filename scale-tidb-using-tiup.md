---
title: Scale a TiDB Cluster Using TiUP
summary: Learn how to scale the TiDB cluster using TiUP.
---

# TiUPを使用して TiDBクラスタをスケーリングする {#scale-a-tidb-cluster-using-tiup}

TiDB クラスターの容量は、オンライン サービスを中断することなく増減できます。

このドキュメントでは、 TiUPを使用して TiDB、TiKV、PD、TiCDC、またはTiFlashクラスターをスケーリングする方法について説明します。 TiUPをインストールしていない場合は、 [ステップ 2. 制御マシンにTiUPをデプロイ](/production-deployment-using-tiup.md#step-2-deploy-tiup-on-the-control-machine)の手順を参照してください。

現在のクラスター名のリストを表示するには、 `tiup cluster list`を実行します。

たとえば、クラスタの元のトポロジが次の場合:

| ホスト IP   | サービス           |
| :------- | :------------- |
| 10.0.1.3 | TiDB + TiFlash |
| 10.0.1.4 | TiDB + PD      |
| 10.0.1.5 | TiKV + モニター    |
| 10.0.1.1 | TiKV           |
| 10.0.1.2 | TiKV           |

## TiDB/PD/TiKV クラスターをスケールアウトする {#scale-out-a-tidb-pd-tikv-cluster}

このセクションでは、TiDB ノードを`10.0.1.5`ホストに追加する方法を例示します。

> **ノート：**
>
> 同様の手順で PD ノードを追加できます。 TiKV ノードを追加する前に、クラスターの負荷に応じて事前に PD スケジューリング パラメーターを調整することをお勧めします。

1.  スケールアウト トポロジを構成します。

    > **ノート：**
    >
    > -   デフォルトでは、ポートとディレクトリの情報は必要ありません。
    > -   複数のインスタンスが単一のマシンにデプロイされている場合は、それらに異なるポートとディレクトリを割り当てる必要があります。ポートまたはディレクトリに競合がある場合は、デプロイまたはスケーリング中に通知を受け取ります。
    > -   TiUP v1.0.0 以降、スケールアウト構成は元のクラスターのグローバル構成を継承します。

    `scale-out.yml`のファイルにスケールアウト トポロジ構成を追加します。

    {{< copyable "" >}}

    ```shell
    vi scale-out.yml
    ```

    {{< copyable "" >}}

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

    {{< copyable "" >}}

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

    {{< copyable "" >}}

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

    現在のクラスターの構成を表示するには、 `tiup cluster edit-config <cluster-name>`を実行します。 `global`と`server_configs`のパラメーター構成は`scale-out.yml`によって継承され、したがって`scale-out.yml`でも有効になるためです。

2.  スケールアウト コマンドを実行します。

    `scale-out`コマンドを実行する前に、 `check`および`check --apply`コマンドを使用して、クラスター内の潜在的なリスクを検出し、自動的に修復します。

    1.  潜在的なリスクを確認します。

        {{< copyable "" >}}

        ```shell
        tiup cluster check <cluster-name> scale-out.yml --cluster --user root [-p] [-i /home/root/.ssh/gcp_rsa]
        ```

    2.  自動修復を有効にします。

        {{< copyable "" >}}

        ```shell
        tiup cluster check <cluster-name> scale-out.yml --cluster --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
        ```

    3.  `scale-out`コマンドを実行します。

        {{< copyable "" >}}

        ```shell
        tiup cluster scale-out <cluster-name> scale-out.yml [-p] [-i /home/root/.ssh/gcp_rsa]
        ```

    前述のコマンドでは:

    -   `scale-out.yml`はスケールアウト構成ファイルです。
    -   `--user root` 、ターゲット マシンに`root`ユーザーとしてログインして、クラスターのスケールアウトを完了することを示します。 `root`人のユーザーは、ターゲット マシンに対して`ssh`と`sudo`権限を持つことが期待されます。または、 `ssh`および`sudo`権限を持つ他のユーザーを使用して展開を完了することもできます。
    -   `[-i]`と`[-p]`はオプションです。パスワードなしでターゲット マシンへのログインを設定した場合、これらのパラメータは必要ありません。そうでない場合は、2 つのパラメーターのいずれかを選択します。 `[-i]`は、ターゲット マシンにアクセスできる root ユーザー (または`--user`で指定された他のユーザー) の秘密鍵です。 `[-p]`は、対話的にユーザーパスワードを入力するために使用されます。

    `Scaled cluster <cluster-name> out successfully`が表示された場合、スケールアウト操作は成功しています。

3.  クラスターのステータスを確認します。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)の監視プラットフォームにアクセスし、クラスタと新しいノードのステータスを監視します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホスト IP   | サービス                   |
| :------- | :--------------------- |
| 10.0.1.3 | TiDB + TiFlash         |
| 10.0.1.4 | TiDB + PD              |
| 10.0.1.5 | **TiDB** + TiKV + モニター |
| 10.0.1.1 | TiKV                   |
| 10.0.1.2 | TiKV                   |

## TiFlashクラスターをスケールアウトする {#scale-out-a-tiflash-cluster}

このセクションでは、 TiFlashノードを`10.0.1.4`ホストに追加する方法を例示します。

> **ノート：**
>
> TiFlashノードを既存の TiDB クラスターに追加する場合は、次の点に注意してください。
>
> -   現在の TiDB バージョンがTiFlashの使用をサポートしていることを確認します。それ以外の場合は、TiDB クラスターを v5.0 以降のバージョンにアップグレードしてください。
> -   `tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> config set enable-placement-rules true`コマンドを実行して、配置ルール機能を有効にします。または、対応するコマンドを[pd-ctl](/pd-control.md)で実行します。

1.  ノード情報を`scale-out.yml`ファイルに追加します。

    TiFlashノード情報を追加するファイルを`scale-out.yml`作成します。

    {{< copyable "" >}}

    ```ini
    tiflash_servers:
    - host: 10.0.1.4
    ```

    現在、追加できるのは IP アドレスのみで、ドメイン名は追加できません。

2.  スケールアウト コマンドを実行します。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

    > **ノート：**
    >
    > 上記のコマンドは、ユーザーがコマンドと新しいマシンを実行できるように相互信頼が構成されているという前提に基づいています。相互信頼を構成できない場合は、オプション`-p`を使用して新しいマシンのパスワードを入力するか、オプション`-i`を使用して秘密鍵ファイルを指定します。

3.  クラスターのステータスをビュー。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)モニタリング プラットフォームにアクセスし、クラスタと新しいノードのステータスを表示します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホスト IP   | サービス                    |
| :------- | :---------------------- |
| 10.0.1.3 | TiDB + TiFlash          |
| 10.0.1.4 | TiDB + PD + **TiFlash** |
| 10.0.1.5 | TiDB+ TiKV + モニター       |
| 10.0.1.1 | TiKV                    |
| 10.0.1.2 | TiKV                    |

## TiCDC クラスターをスケールアウトする {#scale-out-a-ticdc-cluster}

このセクションでは、2 つの TiCDC ノードを`10.0.1.3`と`10.0.1.4`ホストに追加する方法を例示します。

1.  ノード情報を`scale-out.yml`ファイルに追加します。

    TiCDC ノード情報を追加するファイルを`scale-out.yml`作成します。

    {{< copyable "" >}}

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

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

    > **ノート：**
    >
    > 上記のコマンドは、ユーザーがコマンドと新しいマシンを実行できるように相互信頼が構成されているという前提に基づいています。相互信頼を構成できない場合は、オプション`-p`を使用して新しいマシンのパスワードを入力するか、オプション`-i`を使用して秘密鍵ファイルを指定します。

3.  クラスターのステータスをビュー。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)モニタリング プラットフォームにアクセスし、クラスタと新しいノードのステータスを表示します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホスト IP   | サービス                            |
| :------- | :------------------------------ |
| 10.0.1.3 | TiDB + TiFlash + **TiCDC**      |
| 10.0.1.4 | TiDB + PD + TiFlash + **TiCDC** |
| 10.0.1.5 | TiDB+ TiKV + モニター               |
| 10.0.1.1 | TiKV                            |
| 10.0.1.2 | TiKV                            |

## TiDB/PD/TiKV クラスターのスケールイン {#scale-in-a-tidb-pd-tikv-cluster}

このセクションでは、 `10.0.1.5`ホストから TiKV ノードを削除する方法を例示します。

> **ノート：**
>
> -   同様の手順を実行して、TiDB または PD ノードを削除できます。
> -   TiKV、 TiFlash、および TiDB Binlogコンポーネントは非同期でオフラインになり、停止プロセスに時間がかかるため、 TiUPはさまざまな方法でそれらをオフラインにします。詳細については、 [コンポーネントのオフライン プロセスの特定の処理](/tiup/tiup-component-cluster-scale-in.md#particular-handling-of-components-offline-process)を参照してください。
> -   TiKV の PD クライアントは、PD ノードのリストをキャッシュします。 TiKV の現在のバージョンには、PD ノードを自動的かつ定期的に更新するメカニズムがあり、TiKV によってキャッシュされた PD ノードのリストが期限切れになる問題を軽減するのに役立ちます。ただし、PD をスケールアウトした後は、スケーリング前に存在するすべての PD ノードを一度に直接削除しないようにする必要があります。必要に応じて、既存のすべての PD ノードをオフラインにする前に、PD リーダーを新しく追加された PD ノードに切り替えてください。

1.  ノード ID 情報をビュー。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ```
    Starting /root/.tiup/components/cluster/v1.11.3/cluster display <cluster-name>
    TiDB Cluster: <cluster-name>
    TiDB Version: v6.5.2
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

2.  スケールイン コマンドを実行します。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.5:20160
    ```

    `--node`パラメーターは、オフラインにするノードの ID です。

    `Scaled cluster <cluster-name> in successfully`が表示された場合、スケールイン操作は成功しています。

3.  クラスターのステータスを確認します。

    スケールイン プロセスには時間がかかります。次のコマンドを実行して、スケールインのステータスを確認できます。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    スケールインするノードが`Tombstone`になると、スケールイン操作は成功します。

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)のモニタリング プラットフォームにアクセスし、クラスタのステータスを表示します。

現在のトポロジは次のとおりです。

| ホスト IP   | サービス                          |
| :------- | :---------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC        |
| 10.0.1.4 | TiDB + PD + TiFlash + TiCDC   |
| 10.0.1.5 | TiDB + Monitor **(TiKV は削除)** |
| 10.0.1.1 | TiKV                          |
| 10.0.1.2 | TiKV                          |

## TiFlashクラスターのスケールイン {#scale-in-a-tiflash-cluster}

このセクションでは、 `10.0.1.4`ホストからTiFlashノードを削除する方法を例示します。

### 1. 残りのTiFlashノードの数に応じて、テーブルのレプリカの数を調整します。 {#1-adjust-the-number-of-replicas-of-the-tables-according-to-the-number-of-remaining-tiflash-nodes}

1.  スケールイン後に、 TiFlashノードの数を超えるTiFlashレプリカを持つテーブルがあるかどうかをクエリします。 `tobe_left_nodes`スケールイン後のTiFlashノードの数を意味します。クエリ結果が空の場合、 TiFlashでスケーリングを開始できます。クエリ結果が空でない場合は、関連するテーブルのTiFlashレプリカの数を変更する必要があります。

    ```sql
    SELECT * FROM information_schema.tiflash_replica WHERE REPLICA_COUNT >  'tobe_left_nodes';
    ```

2.  スケールイン後に、 TiFlashノードの数を超えるTiFlashレプリカを持つすべてのテーブルに対して、次のステートメントを実行します。 `new_replica_num` `tobe_left_nodes`以下でなければなりません:

    ```sql
    ALTER TABLE <db-name>.<table-name> SET tiflash replica 'new_replica_num';
    ```

3.  ステップ 1 を再度実行し、スケールイン後にTiFlashノードの数を超えるTiFlashレプリカを持つテーブルがないことを確認します。

### 2. スケールイン操作を実行する {#2-perform-the-scale-in-operation}

次のいずれかのソリューションでスケールイン操作を実行します。

#### 解決策 1. TiUP を使用してTiFlashノードを削除する {#solution-1-use-tiup-to-remove-a-tiflash-node}

1.  停止するノードの名前を確認します。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

2.  TiFlashノードを削除します (ノード名がステップ 1 の`10.0.1.4:9000`であると仮定します)。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:9000
    ```

#### 解決策 2. TiFlashノードを手動で削除する {#solution-2-manually-remove-a-tiflash-node}

特別な場合 (ノードを強制的に停止する必要がある場合など)、またはTiUPスケールイン操作が失敗した場合は、次の手順でTiFlashノードを手動で削除できます。

1.  pd-ctl の store コマンドを使用して、このTiFlashノードに対応するストア ID を表示します。

    -   [pd-ctl](/pd-control.md)に store コマンドを入力します (バイナリ ファイルは tidb-ansible ディレクトリの`resources/bin`の下にあります)。

    -   TiUPデプロイメントを使用する場合は、 `pd-ctl` `tiup ctl:v<CLUSTER_VERSION> pd`に置き換えます。

    {{< copyable "" >}}

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> store
    ```

    > **ノート：**
    >
    > クラスター内に複数の PD インスタンスが存在する場合、上記のコマンドでアクティブな PD インスタンスの IP アドレス:ポートのみを指定する必要があります。

2.  pd-ctl でTiFlashノードを削除します。

    -   pd-ctl に`store delete <store_id>`入力します ( `<store_id>`は、前の手順で見つかったTiFlashノードのストア ID です。

    -   TiUPデプロイメントを使用する場合は、 `pd-ctl` `tiup ctl:v<CLUSTER_VERSION> pd`に置き換えます。

        {{< copyable "" >}}

        ```shell
        tiup ctl:v<CLUSTER_VERSION> pd -u http://<pd_ip>:<pd_port> store delete <store_id>
        ```

    > **ノート：**
    >
    > クラスター内に複数の PD インスタンスが存在する場合、上記のコマンドでアクティブな PD インスタンスの IP アドレス:ポートのみを指定する必要があります。

3.  TiFlashプロセスを停止する前に、 TiFlashノードのストアが消えるか、 `state_name`が`Tombstone`になるのを待ちます。

4.  TiFlashデータ ファイルを手動で削除します (場所は、クラスター トポロジ ファイルのTiFlash構成の下の`data_dir`ディレクトリにあります)。

5.  次のコマンドを使用して、ダウンしたTiFlashノードに関する情報をクラスター トポロジから削除します。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node <pd_ip>:<pd_port> --force
    ```

> **ノート：**
>
> クラスター内のすべてのTiFlashノードが実行を停止する前に、 TiFlashに複製されたすべてのテーブルが取り消されていない場合は、PD の複製ルールを手動でクリーンアップする必要があります。そうしないと、 TiFlashノードを正常に停止できません。

PD でレプリケーション ルールを手動でクリーンアップする手順は次のとおりです。

1.  現在の PD インスタンスのTiFlashに関連するすべてのデータ レプリケーション ルールをビュー。

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

2.  TiFlashに関連するすべてのデータ レプリケーション ルールを削除します。例として、 `id`が`table-45-r`であるルールを取り上げます。次のコマンドで削除します。

    {{< copyable "" >}}

    ```shell
    curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
    ```

3.  クラスターのステータスをビュー。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)モニタリング プラットフォームにアクセスし、クラスタと新しいノードのステータスを表示します。

スケールアウト後のクラスター トポロジは次のようになります。

| ホスト IP   | サービス                               |
| :------- | :--------------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC             |
| 10.0.1.4 | TiDB + PD + TiCDC **(TiFlashは削除)** |
| 10.0.1.5 | TiDB+ モニター                         |
| 10.0.1.1 | TiKV                               |
| 10.0.1.2 | TiKV                               |

## TiCDC クラスターでスケールイン {#scale-in-a-ticdc-cluster}

このセクションでは、 `10.0.1.4`ホストから TiCDC ノードを削除する方法を例示します。

1.  ノードをオフラインにします。

    {{< copyable "" >}}

    ```shell
    tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
    ```

2.  クラスターのステータスをビュー。

    {{< copyable "" >}}

    ```shell
    tiup cluster display <cluster-name>
    ```

    ブラウザを使用して[http://10.0.1.5:3000](http://10.0.1.5:3000)のモニタリング プラットフォームにアクセスし、クラスタのステータスを表示します。

現在のトポロジは次のとおりです。

| ホスト IP   | サービス                       |
| :------- | :------------------------- |
| 10.0.1.3 | TiDB + TiFlash + TiCDC     |
| 10.0.1.4 | TiDB + PD + **(TiCDCは削除）** |
| 10.0.1.5 | TiDB + モニター                |
| 10.0.1.1 | TiKV                       |
| 10.0.1.2 | TiKV                       |
