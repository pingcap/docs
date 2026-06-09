---
title: Deploy and Maintain TiCDC
summary: TiCDCの導入と実行に関するハードウェアおよびソフトウェアの推奨事項、ならびに導入と保守の方法について学びましょう。
---

# TiCDCのデプロイと管理 {#deploy-and-maintain-ticdc}

このドキュメントでは、ハードウェアとソフトウェアに関する推奨事項を含め、TiCDCクラスタのデプロイと保守方法について説明します。TiCDCは、新しいTiDBクラスタと同時にデプロイすることも、既存のTiDBクラスタにTiCDCコンポーネントを追加することもできます。

## ソフトウェアとハ​​ードウェアの推奨事項 {#software-and-hardware-recommendations}

本番環境におけるTiCDCの推奨ハードウェア構成は以下のとおりです。

| CPU    | メモリ    | ディスク        | ネットワーク                 | TiCDCクラスタインスタンスの数（本番環境における最小要件） |
| :----- | :----- | :---------- | :--------------------- | :------------------------------ |
| 16コア以上 | 64GB以上 | 500GB以上のSSD | 10ギガビットネットワークカード（2枚推奨） | 2                               |

詳細については、[ソフトウェアおよびハードウェアに関する推奨事項](/hardware-and-software-requirements.md)を参照してください。

## TiUPを使用してTiCDCを含む新しいTiDBクラスタをデプロイ {#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup}

TiUPを使用して新しい TiDB クラスタをデプロイする場合、同時に TiCDC もデプロイできます。TiUPが TiUPクラスタの起動に使用する構成ファイルに`cdc_servers`セクションを追加するだけで済みます。以下に例を示します。

```shell
cdc_servers:
  - host: 10.0.1.20
    gc-ttl: 86400
    data_dir: "/cdc-data"
  - host: 10.0.1.21
    gc-ttl: 86400
    data_dir: "/cdc-data"
```

その他の参考文献：

-   詳しい操作については、 [初期化設定ファイルを編集します](/production-deployment-using-tiup.md#step-3-initialize-the-cluster-topology-file)ご覧ください。
-   設定可能なフィールドの詳細については、 [TiUPを使用して`cdc_servers`を設定する](/tiup/tiup-cluster-topology-reference.md#cdc_servers)を参照してください。
-   TiDB クラスターを展開する詳細な手順については、 [TiUPを使用してTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)参照してください。

> **注記：**
>
> TiCDC をインストールする前に、 TiUPコントロール マシンと TiCDC ホストの間に[SSH相互信頼とパスワードなしのsudoを手動で設定](/check-before-deployment.md#manually-configure-the-ssh-mutual-trust-and-sudo-without-password)いることを確認してください。

## TiUPを使用して、既存のTiDBクラスタにTiCDCを追加またはスケールアウトします。 {#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup}

TiCDCクラスタのスケールアウト方法は、新規デプロイ方法と同様です。スケールアウトにはTiUPを使用することをお勧めします。

1.  TiCDCノード情報を追加する`scale-out.yml`ファイルを作成します。以下に例を示します。

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

2.  TiUP制御マシンでスケールアウトコマンドを実行します。

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

その他の使用例については、 [TiCDCクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster)参照してください。

## TiUPを使用して既存のTiDBクラスタからTiCDCを削除またはスケーリングする {#delete-or-scale-in-ticdc-from-an-existing-tidb-cluster-using-tiup}

TiCDCノードの拡張にはTiUPを使用することをお勧めします。拡張コマンドは以下のとおりです。

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
```

その他の使用例については、 [TiCDCクラスタースケールイン](/scale-tidb-using-tiup.md#scale-in-a-ticdc-cluster)を参照してください。

## TiUPを使用してTiCDCをアップグレードする {#upgrade-ticdc-using-tiup}

TiUPを使用すると TiDB クラスタをアップグレードできます。この際、TiCDC も同時にアップグレードされます。アップグレード コマンドを実行すると、 TiUP は自動的に TiCDCコンポーネントをアップグレードします。以下に例を示します。

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> <version> --transfer-timeout 600
```

> **注記：**
>
> 上記のコマンドでは、 `<cluster-name>`と`<version>`実際のクラスタ名とクラスタバージョンに置き換える必要があります。たとえば、バージョンは v8.5.4 です。

### アップグレードに関する注意事項 {#upgrade-cautions}

TiCDCクラスタをアップグレードする際には、以下の点に注意してください。

-   TiCDC v4.0.2 は`changefeed`を再構成しました。詳細については、 [コンフィグレーションファイルの互換性に関する注意事項](/ticdc/ticdc-compatibility.md#cli-and-configuration-file-compatibility)を参照してください。
-   アップグレード中に問題が発生した場合は、解決策について[アップグレードに関するよくある質問](/upgrade-tidb-using-tiup.md#faq)を参照してください。
-   v6.3.0 以降、TiCDC はローリング アップグレードをサポートしています。マイナー バージョン間のローリング アップグレードを直接実行できます (たとえば、v8.5.0 -&gt; v8.5.3 はマイナー バージョン アップグレードであり、v8.1.x -&gt; v8.5.x はメジャー バージョン アップグレードです)。 TiCDC クラシックアーキテクチャの場合、メジャー バージョン間のアップグレード中に変更フィードを実行しないでください。クラシックアーキテクチャをアップグレードする前に、変更フィードを一時停止してください。新しい TiCDCアーキテクチャは、ローリング アップグレード プロセス中の変更フィードの実行をサポートします。詳細については、 [以前のTiCDCバージョンからのローリングアップグレードに関する互換性に関する注意事項](/ticdc/ticdc-compatibility.md#compatibility-notes-for-upgrading-from-earlier-versions)参照してください。次の条件が満たされる場合、ローリング アップグレードは自動的に有効になります。

    -   TiCDCはバージョン6.3.0以降です。
    -   TiUPはバージョン1.11.3以降です。
    -   クラスター内では、少なくとも2つのTiCDCインスタンスが稼働している。

## TiUPを使用してTiCDCクラスタ構成を変更します。 {#modify-ticdc-cluster-configurations-using-tiup}

このセクションでは[`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md)コマンドを使用して TiCDC の設定を変更する方法について説明します。次の例では、 `gc-ttl`のデフォルト値を`86400`から`172800` (48 時間) に変更する必要があると想定しています。

1.  `tiup cluster edit-config`コマンドを実行します。 `<cluster-name>`実際のクラスター名に置き換えてください。

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

    上記のコマンドでは、 `gc-ttl`が 48 時間に設定されています。

3.  `tiup cluster reload <cluster-name> -R cdc`コマンドを実行して設定を再読み込みします。

## TiUPを使用してTiCDCを停止および起動します。 {#stop-and-start-ticdc-using-tiup}

TiUPを使用すると、TiCDCノードを簡単に停止および起動できます。コマンドは次のとおりです。

-   TiCDCを停止します： `tiup cluster stop <cluster-name> -R cdc`
-   TiCDC を起動します: `tiup cluster start <cluster-name> -R cdc`
-   TiCDCを再起動します: `tiup cluster restart <cluster-name> -R cdc`

## TiCDCでTLSを有効にする {#enable-tls-for-ticdc}

[TiDBコンポーネント間でTLSを有効にする](/enable-tls-between-components.md)参照してください。

## コマンドラインツールを使用してTiCDCのステータスを表示する {#view-ticdc-status-using-the-command-line-tool}

TiCDCクラスタの状態を確認するには、次のコマンドを実行します。 `v<CLUSTER_VERSION>`を、 `v8.5.4`などのTiCDCクラスタのバージョンに置き換える必要があることに注意してください。

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

-   `id` : サービスプロセスのIDを示します。
-   `is-owner` : サービスプロセスがオーナーノードであるかどうかを示します。
-   `address` : サービスプロセスが外部とのインターフェースを提供するアドレスを示します。
-   `cluster-id` : TiCDC クラスターの ID を示します。デフォルト値は`default`です。
