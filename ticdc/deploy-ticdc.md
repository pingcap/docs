---
title: Deploy and Maintain TiCDC
summary: TiCDC を展開および実行するためのハードウェアとソフトウェアの推奨事項、および展開と保守の方法について説明します。
---

# TiCDCのデプロイと管理 {#deploy-and-maintain-ticdc}

このドキュメントでは、TiCDC クラスタの導入と保守方法について、ハードウェアとソフトウェアの推奨事項を含めて説明します。TiCDC は、新しい TiDB クラスタと同時に導入することも、既存の TiDB クラスタに TiCDCコンポーネントを追加することもできます。

## ソフトウェアとハードウェアの推奨事項 {#software-and-hardware-recommendations}

本番環境では、TiCDC のハードウェアに関する推奨事項は次のとおりです。

| CPU    | メモリ     | ディスク         | ネットワーク                 | TiCDC クラスター インスタンスの数 (本番環境の最小要件) |
| :----- | :------ | :----------- | :--------------------- | :------------------------------- |
| 16コア以上 | 64 GB以上 | 500 GB以上のSSD | 10ギガビットネットワークカード（2枚推奨） | 2                                |

詳細については[ソフトウェアとハードウェアの推奨事項](/hardware-and-software-requirements.md)参照してください。

## TiUPを使用して TiCDC を含む新しい TiDB クラスターをデプロイ。 {#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup}

TiUPを使用して新しい TiDB クラスタをデプロイする際に、同時に TiCDC もデプロイできます。設定ファイルに、 TiUPが TiDB クラスタの起動に使用するセクションを`cdc_servers`追加するだけで済みます。以下に例を示します。

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

-   詳しい操作については[初期化設定ファイルを編集する](/production-deployment-using-tiup.md#step-3-initialize-the-cluster-topology-file)参照してください。
-   設定可能なフィールドの詳細については、 [TiUPを使用して`cdc_servers`を構成する](/tiup/tiup-cluster-topology-reference.md#cdc_servers)参照してください。
-   TiDB クラスターをデプロイする詳細な手順については、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。

> **注記：**
>
> TiCDC をインストールする前に、 TiUP制御マシンと TiCDC ホストの間に[SSH相互信頼とパスワードなしのsudoを手動で設定しました](/check-before-deployment.md#manually-configure-the-ssh-mutual-trust-and-sudo-without-password)あることを確認してください。

## TiUPを使用して既存の TiDB クラスターに TiCDC を追加またはスケールアウトする {#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup}

TiCDC クラスターのスケールアウト方法は、デプロイ方法と似ています。スケールアウトにはTiUPを使用することをお勧めします。

1.  TiCDCノード情報を追加するファイル`scale-out.yml`を作成します。以下に例を示します。

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

## TiUPを使用して既存の TiDB クラスターから TiCDC を削除またはスケールインする {#delete-or-scale-in-ticdc-from-an-existing-tidb-cluster-using-tiup}

TiCDCノードをスケールインするには、 TiUPを使用することをお勧めします。スケールインコマンドは次のとおりです。

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
```

その他の使用例については、 [TiCDC クラスターのスケールイン](/scale-tidb-using-tiup.md#scale-in-a-ticdc-cluster)参照してください。

## TiUPを使用して TiCDC をアップグレードする {#upgrade-ticdc-using-tiup}

TiUPを使用して TiDB クラスターをアップグレードすると、TiCDC もアップグレードされます。アップグレードコマンドを実行すると、 TiUP はTiCDCコンポーネントを自動的にアップグレードします。以下は例です。

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> <version> --transfer-timeout 600
```

> **注記：**
>
> 上記のコマンドで、 `<cluster-name>`と`<version>`実際のクラスター名とクラスターバージョンに置き換える必要があります。例えば、バージョンはv8.5.3となります。

### アップグレードに関する注意事項 {#upgrade-cautions}

TiCDC クラスターをアップグレードする場合は、次の点に注意する必要があります。

-   TiCDC v4.0.2 が再構成されました`changefeed` 。詳細については[コンフィグレーションファイルの互換性に関する注意事項](/ticdc/ticdc-compatibility.md#cli-and-configuration-file-compatibility)参照してください。

-   アップグレード中に問題が発生した場合は、解決策については[アップグレードに関するよくある質問](/upgrade-tidb-using-tiup.md#faq)を参照してください。

-   TiCDCはv6.3.0以降、ローリングアップグレードをサポートしています。アップグレード中、レプリケーションのレイテンシーは安定しており、大きな変動はありません。ローリングアップグレードは、以下の条件が満たされた場合に自動的に有効になります。

-   TiCDC は v6.3.0 以降です。
    -   TiUPはv1.11.3以降です。
    -   クラスター内で少なくとも 2 つの TiCDC インスタンスが実行されています。

## TiUPを使用して TiCDC クラスター構成を変更する {#modify-ticdc-cluster-configurations-using-tiup}

このセクションでは、 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)コマンドを使用して TiCDC の設定を変更する方法を説明します。以下の例では、デフォルト値の`gc-ttl` `86400`から`172800` (48 時間) に変更する必要があると想定しています。

1.  `tiup cluster edit-config`コマンドを実行します。3 `<cluster-name>`実際のクラスター名に置き換えます。

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2.  viエディタで`cdc` [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs)変更します。

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

3.  `tiup cluster reload <cluster-name> -R cdc`コマンドを実行して構成を再読み込みします。

## TiUPを使用して TiCDC を停止および起動する {#stop-and-start-ticdc-using-tiup}

TiUPを使用すると、TiCDCノードを簡単に停止および起動できます。コマンドは以下のとおりです。

-   TiCDCを停止: `tiup cluster stop <cluster-name> -R cdc`
-   TiCDC を開始: `tiup cluster start <cluster-name> -R cdc`
-   TiCDC を再起動: `tiup cluster restart <cluster-name> -R cdc`

## TiCDC の TLS を有効にする {#enable-tls-for-ticdc}

[TiDB コンポーネント間の TLS を有効にする](/enable-tls-between-components.md)参照。

## コマンドラインツールを使用して TiCDC のステータスをビュー {#view-ticdc-status-using-the-command-line-tool}

TiCDC クラスターのステータスを表示するには、以下のコマンドを実行します。1 `v<CLUSTER_VERSION>` TiCDC クラスターのバージョン（例： `v8.5.3` ）に置き換える必要があります。

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
-   `cluster-id` : TiCDCクラスタのIDを示します。デフォルト値は`default`です。
