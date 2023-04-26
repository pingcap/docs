---
title: Deploy and Maintain TiCDC
summary: Learn the hardware and software recommendations for deploying and running TiCDC, and how to deploy and maintain it.
---

# TiCDC のデプロイと管理 {#deploy-and-maintain-ticdc}

このドキュメントでは、ハードウェアとソフトウェアの推奨事項を含め、TiCDC クラスターをデプロイおよび維持する方法について説明します。 TiCDC を新しい TiDB クラスターと共にデプロイするか、TiCDCコンポーネントを既存の TiDB クラスターに追加することができます。

## ソフトウェアとハードウェアの推奨事項 {#software-and-hardware-recommendations}

本番環境では、TiCDC のソフトウェアとハードウェアの推奨事項は次のとおりです。

| Linux OS              |     バージョン    |
| :-------------------- | :----------: |
| レッドハット エンタープライズ リナックス | 7.3 以降のバージョン |
| CentOS                | 7.3 以降のバージョン |

| CPU   | メモリー   | ディスクタイプ | 通信網                    | TiCDC クラスタ インスタンスの数 (本番環境の最小要件) |
| :---- | :----- | :------ | :--------------------- | :------------------------------ |
| 16コア+ | 64GB以上 | SSD     | 10ギガビットネットワークカード（2枚推奨） | 2                               |

詳細については、 [ソフトウェアおよびハードウェアの推奨事項](/hardware-and-software-requirements.md)を参照してください。

## TiUPを使用して TiCDC を含む新しい TiDB クラスターをデプロイ {#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup}

TiUPを使用して新しい TiDB クラスターをデプロイすると、TiCDC も同時にデプロイできます。 TiUP がTiDB クラスターを開始するために使用する構成ファイルに`cdc_servers`セクションを追加するだけで済みます。次に例を示します。

```shell
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
    data_dir: "/cdc-data"
  - host: 10.0.1.21
    gc-ttl: 86400
    data_dir: "/cdc-data"
```

その他の参照:

-   詳細な操作については、 [初期設定ファイルの編集](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)を参照してください。
-   設定可能なフィールドの詳細については、 [TiUPを使用して`cdc_servers`を構成する](/tiup/tiup-cluster-topology-reference.md#cdc_servers)を参照してください。
-   TiDB クラスターをデプロイする詳細な手順については、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)を参照してください。

> **ノート：**
>
> TiCDC をインストールする前に、 TiUP制御マシンと TiCDC ホストの間に[パスワードなしで SSH 相互信頼と sudo を手動で構成](/check-before-deployment.md#manually-configure-the-ssh-mutual-trust-and-sudo-without-password)があることを確認してください。

## TiUPを使用して TiCDC を既存の TiDB クラスターに追加またはスケールアウトする {#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup}

TiCDC クラスターをスケールアウトする方法は、デプロイする方法と似ています。 TiUP を使用してスケールアウトを実行することをお勧めします。

1.  TiCDC ノード情報を追加する`scale-out.yml`ファイルを作成します。次に例を示します。

    ```shell
    cdc_servers:
      - host: 10.1.1.1
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
      - host: 10.1.1.2
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
      - host: 10.0.1.4:8300
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
    ```

2.  TiUPコントロール マシンでスケールアウト コマンドを実行します。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

その他の使用例については、 [TiCDC クラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster)を参照してください。

## TiUPを使用して既存の TiDB クラスターから TiCDC を削除またはスケーリングする {#delete-or-scale-in-ticdc-from-an-existing-tidb-cluster-using-tiup}

TiUP を使用して TiCDC ノードをスケーリングすることをお勧めします。スケールイン コマンドは次のとおりです。

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
```

その他の使用例については、 [TiCDC クラスターでスケールイン](/scale-tidb-using-tiup.md#scale-in-a-ticdc-cluster)を参照してください。

## TiUPを使用して TiCDC をアップグレードする {#upgrade-ticdc-using-tiup}

TiUP を使用して TiDB クラスターをアップグレードできます。その間、TiCDC もアップグレードされます。 upgrade コマンドを実行すると、 TiUP は自動的に TiCDCコンポーネントをアップグレードします。次に例を示します。

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> <version> --transfer-timeout 600
```

> **ノート：**
>
> 上記のコマンドで、 `<cluster-name>`と`<version>`を実際のクラスター名とクラスター バージョンに置き換える必要があります。たとえば、バージョンは`v6.5.2`です。

### アップグレードの注意事項 {#upgrade-cautions}

TiCDC クラスターをアップグレードするときは、次の点に注意する必要があります。

-   TiCDC v4.0.2 再構成`changefeed` .詳細については、 [コンフィグレーションファイルの互換性に関する注意事項](/ticdc/ticdc-compatibility.md#cli-and-configuration-file-compatibility)を参照してください。

-   アップグレード中に問題が発生した場合は、解決策について[アップグレードに関するよくある質問](/upgrade-tidb-using-tiup.md#faq)を参照できます。

-   v6.3.0 以降、TiCDC はローリング アップグレードをサポートしています。アップグレード中、レプリケーションのレイテンシーは安定しており、大きく変動することはありません。次の条件が満たされている場合、ローリング アップグレードは自動的に有効になります。

-   TiCDC は v6.3.0 以降です。
    -   TiUPは v1.11.0 以降です。
    -   少なくとも 2 つの TiCDC インスタンスがクラスターで実行されています。

## TiUPを使用して TiCDC クラスター構成を変更する {#modify-ticdc-cluster-configurations-using-tiup}

このセクションでは、 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)コマンドを使用して TiCDC の構成を変更する方法について説明します。次の例では、デフォルト値の`gc-ttl`を`86400`から`172800` (48 時間) に変更する必要があると想定しています。

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

    上記のコマンドでは、 `gc-ttl`は 48 時間に設定されています。

3.  `tiup cluster reload -R cdc`コマンドを実行して構成をリロードします。

## TiUP を使用して TiCDC を停止および開始する {#stop-and-start-ticdc-using-tiup}

TiUP を使用すると、TiCDC ノードを簡単に停止および開始できます。コマンドは次のとおりです。

-   TiCDC を停止: `tiup cluster stop -R cdc`
-   TiCDC の開始: `tiup cluster start -R cdc`
-   TiCDC の再起動: `tiup cluster restart -R cdc`

## TiCDC の TLS を有効にする {#enable-tls-for-ticdc}

[TiDB コンポーネント間の TLS を有効にする](/enable-tls-between-components.md)を参照してください。

## コマンドライン ツールを使用して TiCDC ステータスをビュー {#view-ticdc-status-using-the-command-line-tool}

次のコマンドを実行して、TiCDC クラスターのステータスを表示します。 `v<CLUSTER_VERSION>` `v6.5.2`などの TiCDC クラスター バージョンに置き換える必要があることに注意してください。

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
-   `is-owner` : サービスプロセスがオーナーノードかどうかを示します。
-   `address` : サービスプロセスが外部とのインタフェースを提供するアドレスを示します。
-   `cluster-id` : TiCDC クラスターの ID を示します。デフォルト値は`default`です。
