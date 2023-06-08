---
title: TiDB Cloud CLI Quick Start
summary: Learn how to manage TiDB Cloud resources through the TiDB Cloud CLI.
---

# TiDB CloudCLI クイック スタート {#tidb-cloud-cli-quick-start}

TiDB Cloud は、数行のコマンドを使用してターミナルからTiDB Cloudと対話できるコマンドライン インターフェイス (CLI) [<a href="https://github.com/tidbcloud/tidbcloud-cli">`ticloud`</a>](https://github.com/tidbcloud/tidbcloud-cli)を提供します。たとえば、 `ticloud`を使用すると、次の操作を簡単に実行できます。

-   クラスターを作成、削除、リストします。
-   Amazon S3 またはローカル ファイルからクラスターにデータをインポートします。

## あなたが始める前に {#before-you-begin}

-   TiDB Cloudアカウントを持っていること。お持ちでない場合は、 [<a href="https://tidbcloud.com/free-trial">無料トライアルにサインアップする</a>](https://tidbcloud.com/free-trial) 。
-   [<a href="https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management">TiDB CloudAPI キーを作成する</a>](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management) 。

## インストール {#installation}

<SimpleTab>
<div label="macOS/Linux">

macOS または Linux の場合は、次のいずれかの方法を使用して`ticloud`をインストールできます。

-   スクリプト経由でインストールする (推奨)

    ```shell
    curl https://raw.githubusercontent.com/tidbcloud/tidbcloud-cli/main/install.sh | sh
    ```

-   [<a href="https://tiup.io/">TiUP</a>](https://tiup.io/)経由でインストールする

    ```shell
    tiup install cloud
    ```

-   手動でインストールする

    [<a href="https://github.com/tidbcloud/tidbcloud-cli/releases/latest">リリース</a>](https://github.com/tidbcloud/tidbcloud-cli/releases/latest)ページからコンパイル済みのバイナリをダウンロードし、インストールする場所にコピーします。

-   GitHub アクションにインストールする

    GitHub Action で`ticloud`を設定するには、 [<a href="https://github.com/tidbcloud/setup-tidbcloud-cli">`setup-tidbcloud-cli`</a>](https://github.com/tidbcloud/setup-tidbcloud-cli)を使用します。

</div>

<div label="Windows">

Windows の場合、次のいずれかの方法を使用して`ticloud`をインストールできます。

-   手動でインストールする

    [<a href="https://github.com/tidbcloud/tidbcloud-cli/releases/latest">リリース</a>](https://github.com/tidbcloud/tidbcloud-cli/releases/latest)ページからコンパイル済みのバイナリをダウンロードし、インストールする目的の場所にコピーします。

-   GitHub アクションにインストールする

    GitHub Actions で`ticloud`設定するには、 [<a href="https://github.com/tidbcloud/setup-tidbcloud-cli">`setup-tidbcloud-cli`</a>](https://github.com/tidbcloud/setup-tidbcloud-cli)を使用します。

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

### TiUPを通じてTiDB Cloud CLI を使用する {#use-the-tidb-cloud-cli-through-tiup}

TiDB Cloud CLI は、コンポーネント名`cloud`を使用して[<a href="https://tiup.io/">TiUP</a>](https://tiup.io/)からも使用できます。

使用可能なすべてのコマンドをビュー。

```shell
tiup cloud --help
```

`tiup cloud <command>`でコマンドを実行します。例えば：

```shell
tiup cloud cluster create
```

TiUPによって最新バージョンに更新します。

```shell
tiup update cloud
```

## クイックスタート {#quick-start}

[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverless</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta) (ベータ) は、 TiDB Cloudを開始するための最良の方法です。このセクションでは、 TiDB Cloud CLI を使用して TiDB Serverless クラスターを作成する方法を学習します。

### ユーザープロファイルを作成する {#create-a-user-profile}

クラスターを作成する前に、 TiDB CloudAPI キーを使用してユーザー プロファイルを作成する必要があります。

```shell
ticloud config create
```

> **警告：**
>
> プロファイル名に`.`を含める**ことはできません**。

### TiDB Serverlessクラスターを作成する {#create-a-tidb-serverless-cluster}

TiDB Serverless クラスターを作成するには、次のコマンドを入力し、CLI プロンプトに従って必要な情報を入力し、パスワードを設定します。

```shell
ticloud cluster create
```

### クラスターに接続する {#connect-to-the-cluster}

クラスターが作成されたら、クラスターに接続できます。

```shell
ticloud cluster connect
```

デフォルトのユーザーを使用するかどうかを尋ねるプロンプトが表示されたら、 `Y`を選択し、クラスターの作成時に設定したパスワードを入力します。

## 次は何ですか {#what-s-next}

TiDB Cloud CLI の機能をさらに詳しく調べるには、 [<a href="/tidb-cloud/cli-reference.md">CLI リファレンス</a>](/tidb-cloud/cli-reference.md)を確認してください。

## フィードバック {#feedback}

TiDB Cloud CLI に関して質問や提案がある場合は、お気軽に[<a href="https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose">問題</a>](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)を作成してください。また、貢献も歓迎します。
