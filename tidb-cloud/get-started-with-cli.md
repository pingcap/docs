---
title: TiDB Cloud CLI Quick Start
summary: Learn how to manage TiDB Cloud resources through the TiDB Cloud CLI.
---

# TiDB CloudCLI クイック スタート {#tidb-cloud-cli-quick-start}

TiDB Cloud は、数行のコマンドを使用して端末からTiDB Cloudと対話するためのコマンドライン インターフェイス (CLI) [`ticloud`](https://github.com/tidbcloud/tidbcloud-cli)を提供します。たとえば、 `ticloud`を使用して次の操作を簡単に実行できます。

-   クラスターを作成、削除、および一覧表示します。
-   Amazon S3 またはローカル ファイルからクラスターにデータをインポートします。

## あなたが始める前に {#before-you-begin}

-   TiDB Cloudアカウントを持っている。お持ちでない場合は、 [無料トライアルにサインアップする](https://tidbcloud.com/free-trial) .
-   [TiDB CloudAPI キーを作成する](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management) .

## インストール {#installation}

<SimpleTab>
<div label="macOS/Linux">

macOS または Linux の場合、次のいずれかの方法を使用して`ticloud`をインストールできます。

-   スクリプトによるインストール (推奨)

    ```shell
    curl https://raw.githubusercontent.com/tidbcloud/tidbcloud-cli/main/install.sh | sh
    ```

-   [TiUP](https://tiup.io/)経由でインストール

    ```shell
    tiup install cloud
    ```

-   手動でインストール

    コンパイル済みのバイナリを[リリース](https://github.com/tidbcloud/tidbcloud-cli/releases/latest)ページからダウンロードし、インストール先の場所にコピーします。

-   GitHub アクションにインストール

    GitHub Action で`ticloud`を設定するには、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)を使用します。

</div>

<div label="Windows">

Windows の場合、次のいずれかの方法を使用して`ticloud`をインストールできます。

-   手動でインストール

    コンパイル済みのバイナリを[リリース](https://github.com/tidbcloud/tidbcloud-cli/releases/latest)ページからダウンロードし、インストール先の場所にコピーします。

-   GitHub アクションにインストール

    GitHub Actions で`ticloud`設定するには、 [`setup-tidbcloud-cli`](https://github.com/tidbcloud/setup-tidbcloud-cli)を使用します。

</div>
</SimpleTab>

## TiDB CloudCLI を使用する {#use-the-tidb-cloud-cli}

使用可能なすべてのコマンドをビュー。

```shell
ticloud --help
```

最新バージョンを使用していることを確認します。

```shell
ticloud version
```

そうでない場合は、最新バージョンに更新します。

```shell
ticloud update
```

### TiUPを介してTiDB Cloud CLI を使用する {#use-the-tidb-cloud-cli-through-tiup}

TiDB Cloud CLI は、コンポーネント名が`cloud`の[TiUP](https://tiup.io/)からも利用できます。

使用可能なすべてのコマンドをビュー。

```shell
tiup cloud --help
```

`tiup cloud <command>`でコマンドを実行します。例えば：

```shell
tiup cloud cluster create
```

TiUPによる最新バージョンへの更新:

```shell
tiup update cloud
```

## クイックスタート {#quick-start}

TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) (ベータ) は、 TiDB Cloudを使い始めるための最良の方法です。このセクションでは、 TiDB Cloud CLI を使用してServerless Tierクラスターを作成する方法を学習します。

### ユーザー プロファイルを作成する {#create-a-user-profile}

クラスターを作成する前に、 TiDB Cloud API キーを使用してユーザー プロファイルを作成する必要があります。

```shell
ticloud config create
```

> **警告：**
>
> プロファイル名に`.`を含めて**はなりません**。

### Serverless Tierクラスターを作成する {#create-a-serverless-tier-cluster}

Serverless Tierクラスターを作成するには、次のコマンドを入力し、CLI プロンプトに従って必要な情報を入力し、パスワードを設定します。

```shell
ticloud cluster create
```

### クラスターに接続する {#connect-to-the-cluster}

クラスターが作成されたら、クラスターに接続できます。

```shell
ticloud cluster connect
```

デフォルトのユーザーを使用するかどうかを尋ねられたら、 `Y`を選択し、クラスターの作成時に設定したパスワードを入力します。

## 次は何ですか {#what-s-next}

[CLI リファレンス](/tidb-cloud/cli-reference.md)をチェックして、 TiDB Cloud CLI のその他の機能を調べてください。

## フィードバック {#feedback}

TiDB Cloud CLI について質問や提案がある場合は、気軽に[問題](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、あらゆる貢献を歓迎します。
