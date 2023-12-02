---
title: Deploy and Maintain TiCDC
summary: Learn the hardware and software recommendations for deploying and running TiCDC, and how to deploy and maintain it.
---

# TiCDC のデプロイと管理 {#deploy-and-maintain-ticdc}

このドキュメントでは、ハードウェアとソフトウェアの推奨事項を含め、TiCDC クラスターを展開および維持する方法について説明します。 TiCDC を新しい TiDB クラスターとともにデプロイすることも、TiCDCコンポーネントを既存の TiDB クラスターに追加することもできます。

## ソフトウェアとハ​​ードウェアの推奨事項 {#software-and-hardware-recommendations}

本番環境での TiCDC のソフトウェアとハ​​ードウェアの推奨事項は次のとおりです。

| Linux OS              |    バージョン    |
| :-------------------- | :---------: |
| レッドハット エンタープライズ リナックス | 7.3以降のバージョン |
| CentOS                | 7.3以降のバージョン |

| CPU    | メモリ    | ディスク        | 通信網                    | TiCDC クラスター インスタンスの数 (本番環境の最小要件) |
| :----- | :----- | :---------- | :--------------------- | :------------------------------- |
| 16コア以上 | 64GB以上 | 500GB以上のSSD | 10ギガビットネットワークカード（2枚推奨） | 2                                |

詳細については、 [ソフトウェアとハ​​ードウェアの推奨事項](/hardware-and-software-requirements.md)を参照してください。

## TiUPを使用して TiCDC を含む新しい TiDB クラスターをデプロイ {#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup}

TiUPを使用して新しい TiDB クラスターをデプロイする場合、同時に TiCDC をデプロイすることもできます。 TiUP がTiDB クラスターを開始するために使用する構成ファイルに`cdc_servers`セクションを追加するだけで済みます。以下は例です。

```shell
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
    data_dir: "/cdc-data"
  - host: 10.0.1.21
    gc-ttl: 86400
    data_dir: "/cdc-data"
```

その他の参考資料:

-   詳しい操作方法は[初期化設定ファイルを編集する](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)を参照してください。
-   設定可能なフィールドの詳細については、 [TiUPを使用して`cdc_servers`を構成する](/tiup/tiup-cluster-topology-reference.md#cdc_servers)を参照してください。
-   TiDB クラスターをデプロイする詳細な手順については、 [TiUPを使用した TiDBクラスタのデプロイ](/production-deployment-using-tiup.md)を参照してください。

> **注記：**
>
> TiCDC をインストールする前に、 TiUPコントロール マシンと TiCDC ホストの間に[パスワードなしで SSH 相互信頼と sudo を手動で設定しました](/check-before-deployment.md#manually-configure-the-ssh-mutual-trust-and-sudo-without-password)があることを確認してください。

## TiUPを使用して、TiCDC を既存の TiDB クラスターに追加またはスケールアウトする {#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup}

TiCDC クラスターをスケールアウトする方法は、TiCDC クラスターをデプロイする方法と似ています。スケールアウトを実行するにはTiUPを使用することをお勧めします。

1.  TiCDC ノード情報を追加する`scale-out.yml`ファイルを作成します。以下は例です。

    ```shell
    cdc_servers:
      - host: 10.1.1.1
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
      - host: 10.1.1.2
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
      - host: 10.0.1.4
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
    ```

2.  TiUPコントロール マシンでスケールアウト コマンドを実行します。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

その他の使用例については、 [TiCDC クラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster)を参照してください。

## TiUPを使用して既存の TiDB クラスターから TiCDC を削除またはスケールインする {#delete-or-scale-in-ticdc-from-an-existing-tidb-cluster-using-tiup}

TiUP を使用して TiCDC ノードをスケールインすることをお勧めします。スケールイン コマンドは次のとおりです。

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
```

その他の使用例については、 [TiCDC クラスターでのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-ticdc-cluster)を参照してください。

## TiUPを使用して TiCDC をアップグレードする {#upgrade-ticdc-using-tiup}

TiUP を使用して TiDB クラスターをアップグレードでき、その際に TiCDC もアップグレードされます。アップグレード コマンドを実行すると、 TiUP はTiCDCコンポーネントを自動的にアップグレードします。以下は例です。

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> <version> --transfer-timeout 600
```

> **注記：**
>
> 前述のコマンドでは、 `<cluster-name>`と`<version>`実際のクラスター名とクラスターのバージョンに置き換える必要があります。たとえば、バージョンは v7.5.0 になります。

### アップグレードに関する注意事項 {#upgrade-cautions}

TiCDC クラスターをアップグレードするときは、次の点に注意する必要があります。

-   TiCDC v4.0.2 が再構成されました`changefeed` 。詳細は[コンフィグレーションファイルの互換性に関する注意事項](/ticdc/ticdc-compatibility.md#cli-and-configuration-file-compatibility)を参照してください。

-   アップグレード中に問題が発生した場合は、解決策について[アップグレードに関するよくある質問](/upgrade-tidb-using-tiup.md#faq)を参照してください。

-   v6.3.0 以降、TiCDC はローリング アップグレードをサポートしています。アップグレード中、レプリケーションのレイテンシーは安定しており、大幅に変動しません。次の条件が満たされる場合、ローリング アップグレードは自動的に有効になります。

-   TiCDC は v6.3.0 以降です。
    -   TiUPは v1.11.3 以降です。
    -   少なくとも 2 つの TiCDC インスタンスがクラスター内で実行されています。

## TiUPを使用して TiCDC クラスター構成を変更する {#modify-ticdc-cluster-configurations-using-tiup}

このセクションでは、 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)コマンドを使用して TiCDC の構成を変更する方法について説明します。次の例では、デフォルト値`gc-ttl`を`86400`から`172800` (48 時間) に変更する必要があると想定しています。

1.  `tiup cluster edit-config`コマンドを実行します。 `<cluster-name>`実際のクラスター名に置き換えます。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2.  vi エディターで、 `cdc` [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs)を変更します。

    ```shell
    server_configs:
      tidb: {}
      tikv: {}
      pd: {}
      tiflash: {}
      tiflash-learner: {}
      pump: {}
      drainer: {}
      cdc:
        gc-ttl: 172800
    ```

    前述のコマンドでは、 `gc-ttl`が 48 時間に設定されています。

3.  `tiup cluster reload -R cdc`コマンドを実行して構成を再ロードします。

## TiUP を使用して TiCDC を停止および開始する {#stop-and-start-ticdc-using-tiup}

TiUP を使用すると、TiCDC ノードを簡単に停止および起動できます。コマンドは次のとおりです。

-   TiCDC を停止: `tiup cluster stop -R cdc`
-   TiCDC を開始します: `tiup cluster start -R cdc`
-   TiCDC を再起動します: `tiup cluster restart -R cdc`

## TiCDC の TLS を有効にする {#enable-tls-for-ticdc}

[TiDB コンポーネント間で TLS を有効にする](/enable-tls-between-components.md)を参照してください。

## コマンドライン ツールを使用して TiCDC ステータスをビュー {#view-ticdc-status-using-the-command-line-tool}

次のコマンドを実行して、TiCDC クラスターのステータスを表示します。 `v<CLUSTER_VERSION>` TiCDC クラスターのバージョン ( `v7.5.0`など) に置き換える必要があることに注意してください。

```shell
tiup ctl:v<CLUSTER_VERSION> cdc capture list --server=http://10.0.10.25:8300
```

```shell
[
  {
    "id": "806e3a1b-0e31-477f-9dd6-f3f2c570abdd",
    "is-owner": true,
    "address": "127.0.0.1:8300",
    "cluster-id": "default"
  },
  {
    "id": "ea2a4203-56fe-43a6-b442-7b295f458ebc",
    "is-owner": false,
    "address": "127.0.0.1:8301",
    "cluster-id": "default"
  }
]
```

-   `id` : サービスプロセスのIDを示します。
-   `is-owner` : サービスプロセスがオーナーノードであるかどうかを示します。
-   `address` : サービスプロセスが外部とのインターフェースを提供する際に経由するアドレスを示します。
-   `cluster-id` : TiCDC クラスターの ID を示します。デフォルト値は`default`です。
