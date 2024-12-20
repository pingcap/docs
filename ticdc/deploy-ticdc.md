---
title: Deploy and Maintain TiCDC
summary: TiCDC を展開および実行するためのハードウェアとソフトウェアの推奨事項、および展開と保守の方法について学習します。
---

# TiCDC のデプロイと管理 {#deploy-and-maintain-ticdc}

このドキュメントでは、ハードウェアとソフトウェアの推奨事項を含め、TiCDC クラスターを展開および保守する方法について説明します。新しい TiDB クラスターとともに TiCDC を展開するか、既存の TiDB クラスターに TiCDCコンポーネントを追加することができます。

## ソフトウェアとハードウェアの推奨事項 {#software-and-hardware-recommendations}

本番環境では、TiCDC のハードウェアに関する推奨事項は次のとおりです。

| CPU    | メモリ    | ディスク         | ネットワーク                 | TiCDC クラスター インスタンスの数 (本番環境の最小要件) |
| :----- | :----- | :----------- | :--------------------- | :------------------------------- |
| 16コア以上 | 64GB以上 | 500 GB以上のSSD | 10ギガビットネットワークカード（2枚推奨） | 2                                |

詳細については[ソフトウェアとハードウェアの推奨事項](/hardware-and-software-requirements.md)参照してください。

## TiUP を使用して TiCDC を含む新しい TiDB クラスターをデプロイ {#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup}

TiUPを使用して新しい TiDB クラスターをデプロイするときに、同時に TiCDC もデプロイできます。TiUPがTiDB クラスターを起動するために使用する`cdc_servers`セクションを構成ファイルに追加するだけです。次に例を示します。

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

-   詳しい操作については[初期化設定ファイルを編集する](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)参照してください。
-   設定可能なフィールドの詳細については、 [TiUP を使用して`cdc_servers`を構成する](/tiup/tiup-cluster-topology-reference.md#cdc_servers)参照してください。
-   TiDB クラスターをデプロイする詳細な手順については、 [TiUP を使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。

> **注記：**
>
> TiCDC をインストールする前に、 TiUP制御マシンと TiCDC ホストの間に[SSH相互信頼とパスワードなしのsudoを手動で設定しました](/check-before-deployment.md#manually-configure-the-ssh-mutual-trust-and-sudo-without-password)があることを確認してください。

## TiUP を使用して既存の TiDB クラスターに TiCDC を追加またはスケールアウトする {#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup}

TiCDC クラスターをスケールアウトする方法は、デプロイする方法と似ています。スケールアウトを実行するには、 TiUP を使用することをお勧めします。

1.  TiCDC ノード情報を追加するには、 `scale-out.yml`ファイルを作成します。次に例を示します。

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

その他の使用例については、 [TiCDC クラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster)参照してください。

## TiUP を使用して既存の TiDB クラスターから TiCDC を削除またはスケールインする {#delete-or-scale-in-ticdc-from-an-existing-tidb-cluster-using-tiup}

TiCDC ノードをスケールインするには、 TiUP を使用することをお勧めします。以下はスケールイン コマンドです。

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
```

その他の使用例については、 [TiCDC クラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-ticdc-cluster)参照してください。

## TiUP を使用して TiCDC をアップグレードする {#upgrade-ticdc-using-tiup}

TiUP を使用して TiDB クラスターをアップグレードできます。その際、TiCDC もアップグレードされます。アップグレード コマンドを実行すると、 TiUP はTiCDCコンポーネントを自動的にアップグレードします。次に例を示します。

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> <version> --transfer-timeout 600
```

> **注記：**
>
> 上記のコマンドでは、 `<cluster-name>`と`<version>`実際のクラスター名とクラスター バージョンに置き換える必要があります。たとえば、バージョンは v8.5.0 になります。

### アップグレードに関する注意事項 {#upgrade-cautions}

TiCDC クラスターをアップグレードするときは、次の点に注意する必要があります。

-   TiCDC v4.0.2 が再構成されました`changefeed` 。詳細については[コンフィグレーションファイルの互換性に関する注意事項](/ticdc/ticdc-compatibility.md#cli-and-configuration-file-compatibility)参照してください。

-   アップグレード中に問題が発生した場合は、解決策については[アップグレードに関するよくある質問](/upgrade-tidb-using-tiup.md#faq)を参照してください。

-   v6.3.0 以降、TiCDC はローリング アップグレードをサポートしています。アップグレード中、レプリケーションのレイテンシーは安定しており、大きく変動することはありません。ローリング アップグレードは、次の条件が満たされた場合に自動的に有効になります。

-   TiCDC は v6.3.0 以降です。
    -   TiUPはv1.11.3以降です。
    -   クラスター内で少なくとも 2 つの TiCDC インスタンスが実行されています。

## TiUP を使用して TiCDC クラスター構成を変更する {#modify-ticdc-cluster-configurations-using-tiup}

このセクションでは、 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)コマンドを使用して TiCDC の設定を変更する方法を説明します。次の例では、デフォルト値`gc-ttl`を`86400`から`172800` (48 時間) に変更する必要があると想定しています。

1.  `tiup cluster edit-config`コマンドを実行します。3 `<cluster-name>`実際のクラスター名に置き換えます。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2.  viエディタで、 `cdc` [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs)変更します。

    ```shell
    server_configs:
      tidb: {}
      tikv: {}
      pd: {}
      tiflash: {}
      tiflash-learner: {}
      cdc:
        gc-ttl: 172800
    ```

    上記のコマンドでは、 `gc-ttl` 48 時間に設定されています。

3.  `tiup cluster reload -R cdc`コマンドを実行して構成を再読み込みします。

## TiUP を使用して TiCDC を停止および起動する {#stop-and-start-ticdc-using-tiup}

TiUP を使用すると、TiCDC ノードを簡単に停止および起動できます。コマンドは次のとおりです。

-   TiCDCを停止: `tiup cluster stop -R cdc`
-   TiCDC を開始: `tiup cluster start -R cdc`
-   TiCDCを再起動: `tiup cluster restart -R cdc`

## TiCDC の TLS を有効にする {#enable-tls-for-ticdc}

[TiDB コンポーネント間の TLS を有効にする](/enable-tls-between-components.md)参照。

## コマンドラインツールを使用して TiCDC のステータスをビュー {#view-ticdc-status-using-the-command-line-tool}

次のコマンドを実行して、TiCDC クラスターのステータスを表示します。 `v<CLUSTER_VERSION>` `v8.5.0`などの TiCDC クラスターのバージョンに置き換える必要があることに注意してください。

```shell
tiup cdc:v<CLUSTER_VERSION> cli capture list --server=http://10.0.10.25:8300
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

-   `id` : サービス プロセスの ID を示します。
-   `is-owner` : サービス プロセスが所有者ノードであるかどうかを示します。
-   `address` : サービス プロセスが外部へのインターフェイスを提供するアドレスを示します。
-   `cluster-id` : TiCDC クラスターの ID を示します。デフォルト値は`default`です。
